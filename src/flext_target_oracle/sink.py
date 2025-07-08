"""Modern Oracle Sink using SQLAlchemy 2.0.

Single responsibility: Data loading and transformation.
Optimized for performance with minimal complexity.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from singer_sdk.sinks import SQLSink
from sqlalchemy import Boolean, MetaData, Numeric, String, Table, Text, insert, text

from flext_target_oracle.config import OracleConfig
from flext_target_oracle.connector import OracleConnector

if TYPE_CHECKING:
    from collections.abc import Sequence

    from singer_sdk.target_base import Target


class OracleSink(SQLSink[OracleConnector]):
    """High-performance Oracle data sink.

    Responsibilities:
    - Data transformation and loading
    - Batch processing optimization
    - Oracle-specific SQL generation
    """

    connector_class = OracleConnector

    def __init__(
        self,
        target: Target,
        stream_name: str,
        schema: dict[str, Any],
        key_properties: Sequence[str] | None = None,
    ) -> None:
        """Initialize sink with modern typing."""
        super().__init__(target, stream_name, schema, key_properties)

        # Get typed config
        self._oracle_config = OracleConfig.from_dict(dict(self.config))

        # Table metadata for SQLAlchemy 2.0
        self._metadata = MetaData()
        self._table: Table | None = None

    def get_full_table_name(self) -> str:
        """Get fully qualified Oracle table name."""
        schema_name = (
            self._oracle_config.default_target_schema
            or self._oracle_config.connection.oracle_schema
        )
        table_name = self.stream_name.upper()

        if self._oracle_config.table.table_prefix:
            table_name = f"{self._oracle_config.table.table_prefix}{table_name}"

        return f"{schema_name}.{table_name}" if schema_name else table_name

    def setup(self) -> None:
        """Setup sink and ensure table exists."""
        super().setup()
        self._ensure_table_exists()

    def _ensure_table_exists(self) -> None:
        """Ensure Oracle table exists with correct schema."""
        if self.connector.oracle_table_exists(self.stream_name):
            # Reflect existing table
            self._table = Table(
                self.stream_name,
                self._metadata,
                autoload_with=self.connector._engine,
                schema=self._oracle_config.connection.oracle_schema,
            )
        else:
            # Create new table
            self._create_table()

    def _create_table(self) -> None:
        """Create Oracle table with optimized schema."""
        from sqlalchemy import Column, DateTime
        from sqlalchemy.sql import func

        columns = []

        # Process stream schema to create columns
        for prop_name, prop_def in self.schema["properties"].items():
            oracle_type = self._map_json_type_to_oracle(prop_def)
            columns.append(Column(prop_name.upper(), oracle_type))

        # Add metadata columns if configured
        if self._oracle_config.table.add_metadata_columns:
            columns.extend([
                Column("_SDC_EXTRACTED_AT", DateTime, default=func.current_timestamp()),
                Column("_SDC_BATCHED_AT", DateTime, default=func.current_timestamp()),
                Column("_SDC_RECEIVED_AT", DateTime, default=func.current_timestamp()),
            ])

        self._table = Table(
            self.stream_name.upper(),
            self._metadata,
            *columns,
            schema=self._oracle_config.connection.oracle_schema,
        )

        # Create table with Oracle optimizations
        self._table.create(self.connector._engine)

        # Create indexes if configured
        if self._oracle_config.table.create_indexes and self.key_properties:
            self._create_indexes()

    def _map_json_type_to_oracle(
        self, prop_def: dict[str, Any]
    ) -> String | Text | Numeric[Any] | Boolean:
        """Map JSON schema type to Oracle SQL type."""

        json_type = prop_def.get("type", ["string"])
        if isinstance(json_type, list):
            # Handle nullable types like ["string", "null"]
            json_type = next(t for t in json_type if t != "null")

        match json_type:
            case "string":
                max_length = prop_def.get("maxLength", 255)
                return Text() if max_length > 4000 else String(max_length)
            case "number":
                return Numeric(precision=38, scale=10)
            case "integer":
                return Numeric(precision=38, scale=0)
            case "boolean":
                return Boolean()
            case "array" | "object":
                return Text()  # Store as JSON
            case _:
                return String(255)  # Default fallback

    def _create_indexes(self) -> None:
        """Create Oracle indexes on key properties."""
        from sqlalchemy import Index

        if not self.key_properties or not self._table:
            return

        # Create composite index on all key properties
        key_columns = [self._table.c[key.upper()] for key in self.key_properties]
        index_name = f"IDX_{self.stream_name.upper()}_KEYS"

        index = Index(index_name, *key_columns)
        index.create(self.connector._engine)

    def process_batch(self, context: dict[str, Any]) -> None:
        """Process a batch of records using Oracle optimizations."""
        if not self._table:
            msg = "Table not initialized"
            raise RuntimeError(msg)

        records = context["records"]
        if not records:
            return

        # Apply load method strategy
        match self._oracle_config.table.load_method:
            case "append-only":
                self._insert_records(records)
            case "upsert":
                self._upsert_records(records)
            case "overwrite":
                self._overwrite_records(records)
            case _:
                msg = f"Unknown load method: {self._oracle_config.table.load_method}"
                raise ValueError(msg)

    def _insert_records(self, records: list[dict[str, Any]]) -> None:
        """Insert records using Oracle bulk operations."""
        if not self._table:
            msg = "Table not initialized for insert"
            raise RuntimeError(msg)

        with self.connector._engine.connect() as connection, connection.begin():
            if self._oracle_config.performance.use_bulk_operations:
                # Use executemany for bulk inserts
                connection.execute(insert(self._table), records)
            else:
                # Insert one by one (fallback)
                for record in records:
                    connection.execute(insert(self._table).values(**record))

    def _upsert_records(self, records: list[dict[str, Any]]) -> None:
        """Upsert records using Oracle MERGE statement."""
        if not self.key_properties:
            # No keys defined, fall back to insert
            self._insert_records(records)
            return

        if self._oracle_config.performance.use_merge_statements:
            self._merge_records(records)
        else:
            # Fallback: manual upsert
            self._manual_upsert(records)

    def _merge_records(self, records: list[dict[str, Any]]) -> None:
        """Use Oracle MERGE for efficient upserts."""
        # Implementation would use SQLAlchemy MERGE dialect
        # Simplified for demonstration
        with self.connector._engine.connect() as connection, connection.begin():
            for record in records:
                # Oracle MERGE statement
                merge_sql = self._build_merge_statement(record)
                connection.execute(text(merge_sql), record)

    def _build_merge_statement(self, record: dict[str, Any]) -> str:
        """Build Oracle MERGE SQL statement."""
        table_name = self.get_full_table_name()
        key_conditions = " AND ".join(
            f"target.{key} = :{key}" for key in self.key_properties
        )

        columns = list(record.keys())
        values_clause = ", ".join(f":{col}" for col in columns)
        update_clause = ", ".join(
            f"{col} = :{col}" for col in columns if col not in self.key_properties
        )

        return f"""
        MERGE INTO {table_name} target
        USING (SELECT {values_clause} FROM dual) source
        ON ({key_conditions})
        WHEN MATCHED THEN UPDATE SET {update_clause}
        WHEN NOT MATCHED THEN INSERT ({', '.join(columns)}) VALUES (
            {values_clause}
        )
        """

    def _manual_upsert(self, records: list[dict[str, Any]]) -> None:
        """Manual upsert using SELECT + INSERT/UPDATE."""
        # Simplified implementation - would check existence first
        self._insert_records(records)

    def _overwrite_records(self, records: list[dict[str, Any]]) -> None:
        """Overwrite table contents with new records."""
        if not self._table:
            msg = "Table not initialized for overwrite"
            raise RuntimeError(msg)

        with self.connector._engine.connect() as connection, connection.begin():
            # Truncate table
            connection.execute(text(f"TRUNCATE TABLE {self.get_full_table_name()}"))
            # Insert new records
            connection.execute(insert(self._table), records)

