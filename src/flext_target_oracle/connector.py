"""Modern Oracle Connector using SQLAlchemy 2.0.

Single responsibility: Oracle database connectivity.
Clean implementation following SOLID principles.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from singer_sdk.connectors import SQLConnector
from sqlalchemy import create_engine

from flext_target_oracle.config import OracleConfig

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine


class OracleConnector(SQLConnector):
    """Modern Oracle database connector.

    Responsibilities:
    - Database connection management
    - SQLAlchemy engine configuration
    - Oracle-specific optimizations
    """

    # Oracle capabilities
    allow_column_add: bool = True
    allow_column_rename: bool = True
    allow_column_alter: bool = True
    allow_merge_upsert: bool = True
    allow_temp_tables: bool = True

    def __init__(self, config: dict[str, Any] | OracleConfig) -> None:
        """Initialize connector with typed configuration."""
        if isinstance(config, OracleConfig):
            self._oracle_config = config
            super().__init__(config.model_dump())
        else:
            self._oracle_config = OracleConfig.from_dict(config)
            super().__init__(config)

    def create_engine(self) -> Engine:
        """Create optimized SQLAlchemy engine for Oracle."""
        url = self._oracle_config.to_sqlalchemy_url()
        engine_options = self._oracle_config.get_engine_options()

        engine = create_engine(url, **engine_options)

        # Oracle-specific optimizations
        self._configure_oracle_session(engine)

        return engine

    def _configure_oracle_session(self, engine: Engine) -> None:
        """Configure Oracle session-level optimizations."""
        from sqlalchemy import event

        @event.listens_for(engine, "connect")
        def set_oracle_session_options(
            dbapi_connection: Any, connection_record: Any  # noqa: ANN401
        ) -> None:
            """Set Oracle session options for performance."""
            cursor = dbapi_connection.cursor()

            # Enable parallel DML if configured
            if self._oracle_config.performance.parallel_degree > 1:
                parallel_degree = self._oracle_config.performance.parallel_degree
                cursor.execute(
                    f"ALTER SESSION ENABLE PARALLEL DML PARALLEL {parallel_degree}"
                )

            # Set array size for bulk operations
            cursor.arraysize = self._oracle_config.performance.array_size

            cursor.close()

    def prepare_schema(self, schema_name: str) -> None:
        """Prepare Oracle schema for data loading."""
        if not schema_name:
            return

        with self._engine.connect() as connection:
            # Oracle schemas are created implicitly with first table
            # Just verify we can access it
            from sqlalchemy import text
            connection.execute(text("SELECT 1 FROM dual WHERE ROWNUM = 1"))

    def get_oracle_table_columns(
        self, table_name: str, schema_name: str | None = None
    ) -> list[dict[str, Any]]:
        """Get Oracle table column information."""
        schema = (
            schema_name
            or self._oracle_config.connection.oracle_schema
            or self._oracle_config.connection.username
        )

        query = """
        SELECT
            column_name,
            data_type,
            data_length,
            data_precision,
            data_scale,
            nullable
        FROM all_tab_columns
        WHERE table_name = :table_name
        AND owner = :schema
        ORDER BY column_id
        """

        with self._engine.connect() as connection:
            from sqlalchemy import text
            result = connection.execute(
                text(query),
                {"table_name": table_name.upper(), "schema": schema.upper()},
            )
            return [dict(row._mapping) for row in result]

    def oracle_table_exists(
        self, table_name: str, schema_name: str | None = None
    ) -> bool:
        """Check if Oracle table exists."""
        schema = (
            schema_name
            or self._oracle_config.connection.oracle_schema
            or self._oracle_config.connection.username
        )

        query = """
        SELECT 1 FROM all_tables
        WHERE table_name = :table_name
        AND owner = :schema
        AND ROWNUM = 1
        """

        with self._engine.connect() as connection:
            from sqlalchemy import text
            result = connection.execute(
                text(query),
                {"table_name": table_name.upper(), "schema": schema.upper()},
            )
            return result.fetchone() is not None

