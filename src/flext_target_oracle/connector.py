"""Oracle Connector - Database Connection Management using SQLAlchemy 2.0.

IMPLEMENTATION:
    Complete SQLAlchemy 2.0 implementation with Oracle-specific optimizations.
Enterprise-grade connection management and query execution.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    MetaData,
    create_engine,
    text,
)
from sqlalchemy.exc import SQLAlchemyError

from flext_observability.logging import get_logger

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.engine import Connection, Engine

logger = get_logger(__name__)


class OracleConnector:
    """Oracle database connector using SQLAlchemy 2.0."""

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize Oracle connector with configuration."""
        self.config = config
        self._engine: Engine | None = None
        self._metadata = MetaData()

    def get_connection_url(self) -> str:
        """Build Oracle connection URL."""
        host = self.config.get("host", "localhost")
        port = self.config.get("port", 1521)
        service_name = self.config.get("service_name", "XE")
        username = self.config.get("username")
        password = self.config.get("password")

        if not username or not password:
            msg = "Oracle username and password are required"
            raise ValueError(msg)

        return f"oracle+oracledb://{username}:{password}@{host}:{port}/{service_name}"

    def get_engine(self) -> Engine:
        """Get or create SQLAlchemy engine."""
        if self._engine is None:
            connection_url = self.get_connection_url()

            engine_options = {
                "pool_size": self.config.get("pool_size", 5),
                "max_overflow": self.config.get("max_overflow", 10),
                "pool_timeout": self.config.get("pool_timeout", 30),
                "pool_pre_ping": True,
                "pool_recycle": 3600,
                "echo": self.config.get("log_sql", False),
            }

            logger.info("Creating Oracle engine: %s:%s/%s",
                       self.config.get("host"), self.config.get("port"),
                       self.config.get("service_name"))

            self._engine = create_engine(connection_url, **engine_options)

        return self._engine

    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator[Connection]:
        """Get database connection from pool."""
        engine = self.get_engine()

        with engine.connect() as conn:
            try:
                yield conn
            except Exception:
                conn.rollback()
                raise
            else:
                conn.commit()

    async def execute_query(
        self, query: str, parameters: dict[str, Any] | None = None,
    ) -> list[Any]:
        """Execute SQL query on Oracle database."""
        try:
            logger.debug("Executing Oracle query: %s...", query[:100])

            async with self.get_connection() as conn:
                result = conn.execute(text(query), parameters or {})
                return list(result.fetchall())

        except SQLAlchemyError:
            logger.exception("Query execution failed")
            raise

    async def execute_scalar(
        self, query: str, parameters: dict[str, Any] | None = None,
    ) -> str | int | float | None:
        """Execute SQL query and return scalar result."""
        try:
            logger.debug("Executing scalar query: %s...", query[:100])

            async with self.get_connection() as conn:
                result = conn.execute(text(query), parameters or {})
                return result.scalar()

        except SQLAlchemyError:
            logger.exception("Scalar query execution failed")
            raise

    async def bulk_insert(self, table_name: str, records: list[dict[str, Any]]) -> None:
        """Perform bulk insert operation using SQLAlchemy."""
        if not records:
            return

        logger.info("Bulk inserting %d records into %s", len(records), table_name)

        try:
            async with self.get_connection() as conn:
                # Use Oracle-optimized bulk insert
                schema_name = self.config.get("default_target_schema", "").upper()
                full_table_name = f"{schema_name}.{table_name.upper()}"

                # Get table structure
                columns_query = """
                    SELECT column_name, data_type
                    FROM all_tab_columns
                    WHERE owner = :schema_name AND table_name = :table_name
                    ORDER BY column_id
                """

                column_result = conn.execute(text(columns_query), {
                    "schema_name": schema_name,
                    "table_name": table_name.upper(),
                })

                columns = [(row[0].lower(), row[1]) for row in column_result]

                if not columns:
                    msg = f"Table {full_table_name} not found"
                    raise ValueError(msg)

                # Build parameterized INSERT
                column_names = [col[0] for col in columns]
                placeholders = [f":{col}" for col in column_names]

                insert_sql = f"""
                    INSERT INTO {full_table_name}
                    ({', '.join([f'"{col.upper()}"' for col in column_names])})
                    VALUES ({', '.join(placeholders)})
                """

                # Execute batch insert
                conn.execute(text(insert_sql), records)

            logger.info("Successfully inserted %d records", len(records))

        except SQLAlchemyError:
            logger.exception("Bulk insert failed")
            raise

    async def create_table_if_not_exists(
        self, table_name: str, schema: dict[str, Any],
    ) -> None:
        """Create Oracle table if it doesn't exist using SQLAlchemy."""
        logger.info("Ensuring table exists: %s", table_name)

        try:
            async with self.get_connection() as conn:
                schema_name = self.config.get("default_target_schema", "").upper()

                # Check if table exists
                check_query = """
                    SELECT COUNT(*)
                    FROM all_tables
                    WHERE owner = :schema_name AND table_name = :table_name
                """

                result = conn.execute(text(check_query), {
                    "schema_name": schema_name,
                    "table_name": table_name.upper(),
                })

                scalar_result = result.scalar()
                exists = scalar_result is not None and scalar_result > 0

                if not exists:
                    # Create table with proper column types
                    columns = []

                    # Add schema-defined columns
                    properties = schema.get("properties", {})
                    for prop_name, prop_def in properties.items():
                        if prop_name.startswith("_sdc_"):
                            continue

                        oracle_type = self._map_singer_type_to_oracle(prop_def)
                        columns.append(f'"{prop_name.upper()}" {oracle_type}')

                    # Add Singer metadata columns
                    columns.extend([
                        '"_SDC_EXTRACTED_AT" TIMESTAMP',
                        '"_SDC_ENTITY" VARCHAR2(100)',
                        '"_SDC_SEQUENCE" NUMBER',
                        '"_SDC_BATCHED_AT" TIMESTAMP',
                    ])

                    # Create table
                    create_sql = f"""
                        CREATE TABLE {schema_name}.{table_name.upper()} (
                            {', '.join(columns)}
                        )
                    """

                    conn.execute(text(create_sql))
                    logger.info("Created table: %s.%s", schema_name, table_name.upper())
                else:
                    logger.debug("Table already exists: %s.%s", schema_name, table_name.upper())

        except SQLAlchemyError:
            logger.exception("Table creation failed")
            raise

    def _map_singer_type_to_oracle(self, prop_def: dict[str, Any]) -> str:
        """Map Singer property type to Oracle column type."""
        prop_type = prop_def.get("type", "string")

        if isinstance(prop_type, list):
            # Handle nullable types like ["null", "string"]
            prop_type = next((t for t in prop_type if t != "null"), "string")

        # Check for format hints
        prop_format = prop_def.get("format", "")

        # Enhanced type mapping
        if prop_type == "string":
            if prop_format == "date-time":
                return "TIMESTAMP"
            if prop_format == "date":
                return "DATE"
            return "VARCHAR2(4000)"

        type_mapping = {
            "integer": "NUMBER",
            "number": "NUMBER",
            "boolean": "NUMBER(1)",
            "array": "CLOB",
            "object": "CLOB",
        }

        return type_mapping.get(prop_type, "CLOB")

    async def disconnect(self) -> None:
        """Close Oracle database engine."""
        try:
            if self._engine:
                self._engine.dispose()
                self._engine = None
                logger.info("Oracle engine disposed")

        except Exception:
            logger.exception("Error disposing Oracle engine")
            raise
