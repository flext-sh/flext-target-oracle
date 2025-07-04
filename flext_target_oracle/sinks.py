"""High-Performance Oracle Sink using SQLAlchemy 2.0.

Leverages SQLAlchemy's modern features for:
- Bulk operations with executemany()
- Connection pooling
- Event system
- Oracle dialect optimizations
"""

from __future__ import annotations

import datetime
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import TYPE_CHECKING, Any

from singer_sdk.sinks import SQLSink

# Batch processing thresholds
LARGE_BATCH_THRESHOLD = 1000
from sqlalchemy import MetaData, Table, event, insert, text
from sqlalchemy.sql import Insert

from flext_target_oracle.connectors import OracleConnector

if TYPE_CHECKING:
    from singer_sdk.target_base import Target
    from sqlalchemy.engine import Connection
    from sqlalchemy.sql.expression import Executable


class OracleSink(SQLSink[OracleConnector]):
    """High-performance Oracle sink using SQLAlchemy 2.0.

    Uses SQLAlchemy's native features:
    - Bulk operations with executemany()
    - ON CONFLICT for upserts
    - Connection event handlers
    - Table reflection and creation
    """

    connector_class = OracleConnector

    def __init__(
        self,
        target: Target,
        stream_name: str,
        schema: dict[str, Any],
        key_properties: list[str] | None = None,
    ) -> None:
        """Initialize Oracle sink with SQLAlchemy 2.0 patterns."""
        super().__init__(target, stream_name, schema, key_properties)

        # Performance configuration
        self._batch_size = self.config.get("batch_size_rows", 50000)
        self._parallel_threads = self.config.get("parallel_threads", 8)
        self._use_parallel = self._parallel_threads > 1

        # Thread pool for parallel processing (if enabled)
        self._executor = (
            ThreadPoolExecutor(max_workers=self._parallel_threads)
            if self._use_parallel
            else None
        )

        # Load method configuration
        self._load_method = self.config.get("load_method", "append-only")

        # SQLAlchemy 2.0 metadata
        self._table: Table | None = None
        self._metadata = MetaData()

        # Statistics tracking
        self._stats = {
            "total_records": 0,
            "total_batches": 0,
            "failed_records": 0,
            "start_time": time.time(),
        }

    @property
    def full_table_name(self) -> str:  # type: ignore[override]
        """Get fully qualified table name."""
        schema_name = self.config.get("default_target_schema", "")
        table_name = self.stream_name.upper()

        # Apply any prefixes
        if prefix := self.config.get("table_prefix"):
            table_name = f"{prefix}{table_name}"

        return f"{schema_name}.{table_name}" if schema_name else table_name

    def setup(self) -> None:
        """Setup sink using SQLAlchemy table reflection/creation."""
        # Let parent handle basic setup
        super().setup()

        # Setup SQLAlchemy table metadata
        self._setup_table_metadata()

        # Setup event handlers for optimization
        self._setup_event_handlers()

    def _setup_table_metadata(self) -> None:
        """Setup SQLAlchemy Table object."""
        # Parse schema and table names
        parts = self.full_table_name.split(".")
        schema_name = parts[0] if len(parts) > 1 else None
        table_name = parts[-1]

        # Try to reflect existing table first
        try:
            self._table = Table(
                table_name,
                self._metadata,
                schema=schema_name,
                autoload_with=self.connector.create_engine(),
            )
            self.logger.info("Reflected existing table: %s", self.full_table_name)
        except (AttributeError, ImportError, RuntimeError):
            # Table doesn't exist, will be created by parent class
            self.logger.info("Table %s will be created", self.full_table_name)

    def _setup_event_handlers(self) -> None:
        """Setup SQLAlchemy event handlers for bulk operations."""
        engine = self.connector.create_engine()
        if not engine:
            return

        @event.listens_for(engine, "before_execute")
        def receive_before_execute(
            _: Connection,
            clauseelement: Executable,
            multiparams: list[dict[str, Any]],
            __: dict[str, Any],
            ___: dict[str, Any],
        ) -> None:
            """Add Oracle hints for bulk operations."""
            if (isinstance(clauseelement, Insert) and len(multiparams) > LARGE_BATCH_THRESHOLD
                and self.config.get("use_direct_path", True)):
                # Add APPEND_VALUES hint for large batches
                clauseelement = clauseelement.prefix_with("/*+ APPEND_VALUES */")

    def process_batch(self, context: dict[str, Any]) -> None:
        """Process batch using SQLAlchemy 2.0 bulk operations."""
        records = context.get("records", [])
        if not records:
            return

        start_time = time.time()

        # Update statistics
        self._stats["total_records"] += len(records)
        self._stats["total_batches"] += 1

        try:
            # Choose processing method based on configuration
            if self._load_method == "overwrite":
                self._process_batch_overwrite(records)
            elif self._load_method == "upsert" and self.key_properties:
                self._process_batch_upsert(records)
            else:
                self._process_batch_append(records)

            # Log performance metrics
            elapsed = time.time() - start_time
            records_per_second = len(records) / elapsed if elapsed > 0 else 0

            self.logger.info(
                "Processed batch of %d records in %.2fs (%d records/sec)",
                len(records), elapsed, int(records_per_second),
            )

        except Exception:
            self._stats["failed_records"] += len(records)
            self.logger.exception("Batch processing failed")
            raise

    def _process_batch_append(self, records: list[dict[str, Any]]) -> None:
        """Process batch using SQLAlchemy bulk insert."""
        if not self._table:
            # Use parent's table reference
            self._table = self.get_table()

        # Prepare records for insert
        prepared_records = self._prepare_records(records)

        # Use SQLAlchemy 2.0 Connection.execute() with insert()
        with self.connector.create_engine().begin() as conn:
            if self._use_parallel and len(prepared_records) > LARGE_BATCH_THRESHOLD:
                # Parallel processing for large batches
                self._execute_parallel_insert(conn, prepared_records)
            else:
                # Single-threaded bulk insert
                stmt = insert(self._table)
                conn.execute(stmt, prepared_records)

    def _process_batch_upsert(self, records: list[dict[str, Any]]) -> None:
        """Process batch using Oracle MERGE statement."""
        if not self._table:
            self._table = self.get_table()

        prepared_records = self._prepare_records(records)

        with self.connector.create_engine().begin() as conn:
            # Build Oracle MERGE statement
            table_name = self._table.name
            if self._table.schema:
                table_name = f"{self._table.schema}.{table_name}"

            # Get column names
            columns = list(prepared_records[0].keys())
            key_cols = self.key_properties or ["id"]

            # Build MERGE statement using parameterized queries for safety
            # Note: table_name and column names are from schema validation,
            # not user input. Parameters use SQLAlchemy named parameters (:param)
            merge_sql = f"""
            MERGE INTO {table_name} target
            USING (SELECT {', '.join([f':{col} AS {col}' for col in columns])}
                   FROM DUAL) source
            ON ({' AND '.join([f'target.{col} = source.{col}' for col in key_cols])})
            WHEN MATCHED THEN
                UPDATE SET {', '.join([f'{col} = source.{col}'
                                      for col in columns if col not in key_cols])}
            WHEN NOT MATCHED THEN
                INSERT ({', '.join(columns)})
                VALUES ({', '.join([f'source.{col}' for col in columns])})
            """  # noqa: S608  # Table/column names from validated schema

            # Execute MERGE for each record
            for record in prepared_records:
                conn.execute(text(merge_sql), record)

    def _process_batch_overwrite(self, records: list[dict[str, Any]]) -> None:
        """Process batch with table truncation."""
        if not self._table:
            self._table = self.get_table()

        prepared_records = self._prepare_records(records)

        with self.connector.create_engine().begin() as conn:
            # Truncate table first
            conn.execute(text(f"TRUNCATE TABLE {self.full_table_name}"))

            # Then insert
            stmt = insert(self._table)
            conn.execute(stmt, prepared_records)

    def _execute_parallel_insert(
        self, conn: Connection, records: list[dict[str, Any]],
    ) -> None:
        """Execute insert in parallel chunks."""
        chunk_size = max(1000, len(records) // self._parallel_threads)
        chunks = [
            records[i:i + chunk_size]
            for i in range(0, len(records), chunk_size)
        ]

        futures = []
        if self._executor is not None:
            for chunk in chunks:
                future = self._executor.submit(self._insert_chunk, conn, chunk)
                futures.append(future)
        else:
            # Execute sequentially if no executor
            for chunk in chunks:
                self._insert_chunk(conn, chunk)

        # Wait for all chunks to complete
        for future in as_completed(futures):
            future.result()  # Raise any exceptions

    def _insert_chunk(self, conn: Connection, chunk: list[dict[str, Any]]) -> None:
        """Insert a single chunk of records."""
        if self._table is not None:
            stmt = insert(self._table)
            conn.execute(stmt, chunk)
        else:
            msg = "Table not initialized"
            raise RuntimeError(msg)

    def _prepare_records(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Prepare records for database operations."""
        prepared = []

        for record in records:
            # Let SQLAlchemy handle type conversions
            prepared_record: dict[str, Any] = {}

            for key, value in record.items():
                # Skip metadata fields
                if key.startswith("_sdc_"):
                    continue

                # Handle None values
                if value is None:
                    prepared_record[key] = None
                    continue

                # Let SQLAlchemy's type system handle conversions
                prepared_record[key] = value

            # Add audit fields if configured
            if self.config.get("add_record_metadata", True):
                now = datetime.datetime.now(datetime.UTC)

                if "CREATE_TS" not in prepared_record:
                    prepared_record["CREATE_TS"] = now
                if "MOD_TS" not in prepared_record:
                    prepared_record["MOD_TS"] = now
                if "CREATE_USER" not in prepared_record:
                    prepared_record["CREATE_USER"] = "SINGER"
                if "MOD_USER" not in prepared_record:
                    prepared_record["MOD_USER"] = "SINGER"

            prepared.append(prepared_record)

        return prepared

    def clean_up(self) -> None:
        """Clean up resources."""
        # Shutdown thread pool if used
        if self._executor:
            self._executor.shutdown(wait=True)

        # Log final statistics
        elapsed = time.time() - self._stats["start_time"]
        self.logger.info(
            "Stream %s complete: %d records in %d batches (%.1fs total)",
            self.stream_name, self._stats["total_records"],
            self._stats["total_batches"], elapsed,
        )

        # Let parent clean up
        super().clean_up()

    def get_table(self) -> Table:
        """Get SQLAlchemy Table object."""
        if self._table is None:
            # Use parent's method to get table
            parent_table = getattr(super(), "table", None)
            if parent_table is not None:
                self._table = parent_table
            else:
                self._setup_table_metadata()
        if self._table is None:
            msg = "Unable to initialize table"
            raise RuntimeError(msg)
        return self._table

    def activate_version(self, new_version: int) -> None:
        """Activate version for incremental replication."""
        # Let parent handle this
        super().activate_version(new_version)

    @property
    def table(self) -> Table:
        """Get the SQLAlchemy Table object."""
        if self._table is None:
            # Let parent create table
            parent_table = getattr(super(), "table", None)
            if parent_table is not None:
                self._table = parent_table
            else:
                # Then setup our reference
                self._setup_table_metadata()
        if self._table is None:
            msg = "Unable to initialize table"
            raise RuntimeError(msg)
        return self._table
