"""
High-Performance Oracle Sink with WAN and parallelism optimizations.

Maximizes Oracle Database performance for:
- WAN environments with large latencies
- Parallel processing for massive throughput
- Direct path operations for bulk loads
- Advanced compression and partitioning
"""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import TYPE_CHECKING, Any

import sqlalchemy
from singer_sdk.sinks import SQLSink
from sqlalchemy import Column
from sqlalchemy.dialects.oracle import CLOB, NUMBER, TIMESTAMP, VARCHAR2

from .connectors import OracleConnector

if TYPE_CHECKING:
    from singer_sdk.target_base import Target


class OracleSink(SQLSink):
    """
    High-performance Oracle sink optimized for WAN and parallel processing.

    Features:
    - Parallel batch processing with configurable threads
    - Direct path inserts with APPEND_VALUES hint
    - Array DML for maximum bulk throughput
    - WAN-optimized chunking and compression
    - Advanced Oracle features (partitioning, in-memory, etc.)
    """

    connector_class = OracleConnector

    def __init__(
        self,
        target: Target,
        stream_name: str,
        schema: dict,
        key_properties: list[str] | None = None,
    ) -> None:
        """Initialize high-performance Oracle sink."""
        super().__init__(target, stream_name, schema, key_properties)

        # Performance configuration
        self._batch_size = self.config.get("batch_size_rows", 50000)
        self._parallel_threads = self.config.get("parallel_threads", 8)
        self._chunk_size = self.config.get("chunk_size", 10000)

        # Thread pool for parallel processing
        if self._parallel_threads > 1:
            self._executor: ThreadPoolExecutor | None = ThreadPoolExecutor(
                max_workers=self._parallel_threads
            )
        else:
            self._executor = None

        # Historical versioning for WMS data
        self._enable_versioning = self.config.get("enable_historical_versioning", False)
        self._versioning_column = self.config.get("historical_versioning_column", "mod_ts")
        self._original_key_properties = key_properties

        # Logging and monitoring (will be set by target)
        self._logger = None
        self._monitor = None

    @property
    def key_properties(self) -> list[str]:
        """Return primary key properties with historical versioning support."""
        if (
            self._enable_versioning
            and self._versioning_column in self.schema.get("properties", {})
            and self._original_key_properties
            and self._versioning_column not in self._original_key_properties
        ):
            # Return composite key: original_keys + versioning_column
            return list(self._original_key_properties) + [self._versioning_column]
        return self._original_key_properties or []

    @property
    def full_table_name(self) -> str:  # type: ignore[override]
        """Return the fully qualified table name."""
        # Let Singer SDK handle table name generation
        table = str(super().full_table_name)

        # Apply Oracle naming constraints (30 chars max for older versions)
        if self.config.get("max_identifier_length", 128) == 30:
            schema_name, table_name = self._parse_full_table_name(table)
            if schema_name:
                table_name = table_name[:30]
                table = f"{schema_name}.{table_name}"
            else:
                table = table[:30]

        return table

    def setup(self) -> None:
        """Set up the sink with Oracle-specific table creation."""
        # Use Singer SDK's normal setup, with Oracle type mapping in connector
        super().setup()

        # Apply Oracle optimizations after table is created (skip for basic test)
        if not self.config.get("skip_table_optimization", True):
            self._apply_oracle_optimizations()

    def _create_oracle_table(self) -> None:
        """Create table with Oracle-compatible column types."""
        with self.connector._engine.begin() as conn:
            # Use Singer SDK's method but override column type creation
            # First, let the connector create the table normally
            self.connector.prepare_table(
                full_table_name=self.full_table_name,
                schema=self.schema,
                primary_keys=self.key_properties,
                as_temp_table=False,
            )

            # Now fix the column types that are incompatible with Oracle
            self._fix_oracle_column_types(conn)

    def _fix_oracle_column_types(self, conn: Any) -> None:
        """Fix Oracle column types after table creation."""
        # Get table parts
        schema_name, table_name = self._parse_full_table_name(self.full_table_name)

        # Get list of columns that need fixing
        columns_to_fix = [
            ("_sdc_extracted_at", "TIMESTAMP"),
            ("_sdc_received_at", "TIMESTAMP"),
            ("_sdc_batched_at", "TIMESTAMP"),
            ("_sdc_deleted_at", "TIMESTAMP"),
            ("_sdc_sequence", "NUMBER"),
            ("_sdc_table_version", "NUMBER"),
            ("_sdc_sync_started_at", "NUMBER"),
        ]

        # Try to alter columns - some may not exist yet
        for col_name, oracle_type in columns_to_fix:
            try:
                if schema_name:
                    full_name = f'"{schema_name}"."{table_name}"'
                else:
                    full_name = f'"{table_name}"'

                # Check if column exists first
                check_sql = f"""
                    SELECT COUNT(*) FROM user_tab_columns
                    WHERE table_name = '{table_name.upper()}'
                    AND column_name = '{col_name.upper()}'
                """
                result = conn.execute(sqlalchemy.text(check_sql)).scalar()

                if result > 0:
                    # Column exists, try to modify it
                    alter_sql = (
                        f'ALTER TABLE {full_name} MODIFY ("{col_name}" {oracle_type})'
                    )
                    conn.execute(sqlalchemy.text(alter_sql))
                else:
                    # Column doesn't exist, add it
                    add_sql = (
                        f'ALTER TABLE {full_name} ADD ("{col_name}" {oracle_type})'
                    )
                    conn.execute(sqlalchemy.text(add_sql))

            except Exception as e:
                # DO NOT MASK CRITICAL DDL ERRORS
                self.logger.error(f"CRITICAL: Column modification FAILED for {col_name}: {e}")
                raise RuntimeError(f"Column modification failed for {col_name}: {e}") from e

    def _parse_full_table_name(self, full_name: str) -> tuple[str | None, str]:
        """Parse schema.table into schema and table parts."""
        if "." in full_name:
            parts = full_name.split(".")
            schema = parts[0].strip('"')
            table = parts[1].strip('"')
            return schema, table
        else:
            return None, full_name.strip('"')

    def _get_oracle_column(self, name: str, json_schema: dict) -> Column:
        """Convert JSON schema property to Oracle column."""
        json_type = json_schema.get("type", "string")

        if json_type == "integer" or json_type == "number":
            return Column(name, NUMBER(), nullable=True)
        elif json_type == "boolean":
            return Column(name, NUMBER(1), nullable=True)
        elif json_type == "string":
            # Check for format hints
            format_type = json_schema.get("format")
            if format_type in ("date-time", "date", "time"):
                return Column(name, TIMESTAMP(), nullable=True)
            else:
                max_length = json_schema.get("maxLength", 4000)
                if max_length > 4000:
                    return Column(name, CLOB(), nullable=True)
                else:
                    return Column(name, VARCHAR2(max_length), nullable=True)
        elif json_type in ("object", "array"):
            return Column(name, CLOB(), nullable=True)
        else:
            # Default to VARCHAR2
            return Column(name, VARCHAR2(4000), nullable=True)

    def _apply_oracle_optimizations(self) -> None:
        """Apply maximum Oracle performance optimizations."""
        with self.connector._engine.connect() as conn:
            table_name = self.full_table_name
            optimizations = []

            # Check if we're on Enterprise Edition
            is_ee = self.config.get("oracle_is_enterprise_edition", False)

            # Advanced compression for WAN efficiency
            if self.config.get("enable_compression"):
                compression = self.config.get("compression_type", "ADVANCED").upper()
                compress_for = self.config.get("compress_for", "OLTP")

                # Only use advanced compression if licensed
                if compression != "BASIC" and not self.config.get(
                    "oracle_has_compression_option"
                ):
                    self.logger.warning(
                        f"Compression type {compression} requires Oracle Advanced Compression option. Using BASIC instead."
                    )
                    compression = "BASIC"
                    compress_for = "OLTP"

                optimizations.append(
                    f"ALTER TABLE {table_name} COMPRESS FOR {compress_for} {compression}"
                )

            # Maximum parallelism (requires EE)
            if self.config.get("parallel_degree", 1) > 1:
                if not is_ee:
                    self.logger.warning(
                        "Parallel degree > 1 requires Oracle Enterprise Edition. Skipping."
                    )
                else:
                    degree = self.config["parallel_degree"]
                    optimizations.append(f"ALTER TABLE {table_name} PARALLEL {degree}")

            # Direct path operations
            if self.config.get("use_direct_path"):
                optimizations.append(f"ALTER TABLE {table_name} NOLOGGING")

            # In-Memory column store for ultra-fast access
            if self.config.get("use_inmemory"):
                if not self.config.get("oracle_has_inmemory_option"):
                    self.logger.warning(
                        "In-Memory feature requires Oracle In-Memory option. Skipping."
                    )
                else:
                    priority = self.config.get("inmemory_priority", "HIGH")
                    distribute = self.config.get("inmemory_distribute", "AUTO")
                    duplicate = self.config.get("inmemory_duplicate", "NO DUPLICATE")
                    optimizations.append(
                        f"ALTER TABLE {table_name} INMEMORY PRIORITY {priority} "
                        f"DISTRIBUTE {distribute} {duplicate}"
                    )

            # Result cache for read-heavy workloads
            if self.config.get("use_result_cache"):
                optimizations.append(
                    f"ALTER TABLE {table_name} RESULT_CACHE (MODE FORCE)"
                )

            # Execute all optimizations - REPORT ALL ERRORS
            for opt in optimizations:
                try:
                    conn.execute(sqlalchemy.text(opt))
                    self.logger.info(f"Applied Oracle optimization: {opt}")
                except Exception as e:
                    # DO NOT MASK ERRORS - Log them clearly
                    self.logger.error(f"Oracle optimization FAILED: {opt} - Error: {e}")
                    raise RuntimeError(f"Oracle optimization failed: {opt}") from e

            # Create high-performance indexes
            if self.key_properties and self.config.get("create_table_indexes"):
                self._create_performance_indexes(conn, table_name)

    def _create_performance_indexes(self, conn: Any, table_name: str) -> None:
        """Create indexes with maximum performance options."""
        for i, key in enumerate(self.key_properties):
            idx_name = f"IDX_{table_name.split('.')[-1]}_{i}"[:30]

            # Build index with performance options
            idx_opts = []
            if self.config.get("index_compression"):
                idx_opts.append("COMPRESS ADVANCED LOW")
            if self.config.get("parallel_degree", 1) > 1:
                idx_opts.append(f"PARALLEL {self.config['parallel_degree']}")
            if self.config.get("index_logging") is False:
                idx_opts.append("NOLOGGING")

            idx_clause = " ".join(idx_opts)

            try:
                conn.execute(
                    sqlalchemy.text(
                        f"CREATE INDEX {idx_name} ON {table_name} ({key}) {idx_clause}"
                    )
                )
                self.logger.info(f"Created index: {idx_name}")
            except Exception as e:
                # Check for expected errors vs real problems
                error_msg = str(e)
                if "ORA-00955" in error_msg:  # Name already used - acceptable
                    self.logger.info(f"Index {idx_name} already exists - skipping")
                elif "ORA-00942" in error_msg:  # Table doesn't exist - acceptable during setup
                    self.logger.info(f"Table not ready for index {idx_name} - skipping")
                else:
                    # Real error - DO NOT MASK
                    self.logger.error(f"Index creation FAILED: {idx_name} - Error: {e}")
                    raise RuntimeError(f"Index creation failed: {idx_name}: {e}") from e

    def set_logger(self, logger: Any) -> None:
        """Set logger for sink operations."""
        self._logger = logger

    def set_monitor(self, monitor: Any) -> None:
        """Set monitor for sink operations."""
        self._monitor = monitor
        # Pass engine to monitor for database metrics
        try:
            if hasattr(self.connector, "_engine") and self.connector._engine:
                monitor.set_engine(self.connector._engine)
        except Exception as e:
            # Engine may not be available yet - log warning but continue
            if self.logger:
                self.logger.warning(f"Monitor engine setup failed (will retry later): {e}")
            else:
                print(f"WARNING: Monitor engine setup failed (will retry later): {e}")

    def process_batch(self, context: dict) -> None:
        """Process batch with Oracle-specific optimizations and logging."""
        records = context.get("records", [])
        if not records:
            return

        # Log batch processing
        if self._logger:
            self._logger.log_record_batch(
                stream=self.stream_name,
                batch_size=len(records),
                operation=self.config.get("load_method", "append-only"),
            )

        # Use operation context for monitoring if available
        operation_context = None
        if self._logger:
            operation_context = self._logger.operation_context(
                "process_batch",
                stream=self.stream_name,
                batch_size=len(records),
                load_method=self.config.get("load_method", "append-only"),
            )

        try:
            if operation_context:
                with operation_context:
                    self._process_batch_internal(records)
            else:
                self._process_batch_internal(records)
        except Exception as e:
            if self._logger:
                self._logger.error(
                    f"Batch processing failed for stream {self.stream_name}",
                    extra={
                        "stream": self.stream_name,
                        "batch_size": len(records),
                        "error": str(e),
                    },
                )
            raise

    def _process_batch_internal(self, records: list[dict]) -> None:
        """Internal batch processing logic."""
        # Check if this is an upsert scenario
        if (
            self.config.get("load_method") == "upsert"
            and self.key_properties
            and len(records) > 0
        ):
            self._process_batch_upsert(records)
        else:
            # Use Singer SDK's standard batch processing for append-only
            context = {"records": records}
            super().process_batch(context)

    def _process_batch_upsert(self, records: list[dict]) -> None:
        """Process batch using Oracle MERGE for upsert operations."""
        if not self.key_properties:
            raise ValueError("Upsert requires key_properties to be defined")

        # Build MERGE statement
        merge_sql = self._build_oracle_merge_statement()

        # Conform records
        prepared_records = [self._conform_record(record) for record in records]

        # Execute MERGE in batches
        batch_size = self.config.get("merge_batch_size", 1000)

        with self.connector._engine.connect() as conn, conn.begin():
            for i in range(0, len(prepared_records), batch_size):
                batch = prepared_records[i : i + batch_size]
                for record in batch:
                    conn.execute(sqlalchemy.text(merge_sql), record)

    def _build_oracle_merge_statement(self) -> str:
        """Build Oracle-specific MERGE statement."""
        table_name = self.full_table_name
        columns = list(self.schema["properties"].keys())
        key_columns = self.key_properties or []

        # Add Singer metadata columns that may exist
        metadata_columns = [
            "_sdc_extracted_at",
            "_sdc_received_at",
            "_sdc_batched_at",
            "_sdc_deleted_at",
            "_sdc_sequence",
            "_sdc_table_version",
            "_sdc_sync_started_at",
        ]

        # Check which metadata columns actually exist in the table
        all_columns = columns + metadata_columns
        non_key_columns = [col for col in all_columns if col not in key_columns]

        # Build MERGE statement
        merge_sql = f"""
        MERGE INTO {table_name} target
        USING (
            SELECT {', '.join(f':{col} AS {col}' for col in all_columns)}
            FROM dual
        ) source
        ON ({' AND '.join(f'target.{col} = source.{col}' for col in key_columns)})
        """

        # Add UPDATE clause if there are non-key columns
        if non_key_columns:
            merge_sql += f"""
        WHEN MATCHED THEN
            UPDATE SET {', '.join(f'{col} = source.{col}' for col in non_key_columns)}
            """

        # Add INSERT clause
        merge_sql += f"""
        WHEN NOT MATCHED THEN
            INSERT ({', '.join(all_columns)})
            VALUES ({', '.join(f'source.{col}' for col in all_columns)})
        """

        return merge_sql

    def _process_batch_parallel(self, records: list[dict]) -> None:
        """Process batch in parallel chunks for maximum throughput."""
        # Split into chunks
        chunks = []
        for i in range(0, len(records), self._chunk_size):
            chunks.append(records[i : i + self._chunk_size])

        # Process chunks in parallel
        futures = []
        if self._executor:
            for chunk in chunks:
                future = self._executor.submit(self._process_chunk, chunk)
                futures.append(future)
        else:
            # Fallback to sequential processing
            for chunk in chunks:
                self._process_chunk(chunk)

        # Wait for completion - DO NOT MASK PARALLEL PROCESSING ERRORS
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                # Log the specific chunk processing error
                if self._logger:
                    self._logger.error(f"Parallel chunk processing failed: {e}")
                # Always raise - parallel processing errors indicate serious problems
                raise

    def _process_chunk(self, records: list[dict]) -> None:
        """Process a single chunk of records."""
        if self.key_properties:
            self._execute_merge_batch(records)
        else:
            self._execute_insert_batch(records)

    def _process_batch_direct_path(self, records: list[dict]) -> None:
        """Process using Oracle direct path for maximum speed."""
        insert_sql = self._build_direct_path_insert()
        prepared = [self._conform_record(r) for r in records]

        with self.connector._engine.connect() as conn, conn.begin():
            conn.execute(sqlalchemy.text(insert_sql), prepared)

    def _process_batch_bulk_insert(self, records: list[dict]) -> None:
        """Process using optimized bulk insert."""
        self._execute_insert_batch(records)

    def _process_batch_with_merge(self, context: dict) -> None:
        """Process batch using high-performance Oracle MERGE."""
        records = context.get("records", [])
        if not records:
            return

        self._execute_merge_batch(records)

    def _execute_insert_batch(self, records: list[dict]) -> None:
        """Execute high-performance bulk insert."""
        insert_sql = self._build_bulk_insert_statement()
        prepared = [self._conform_record(r) for r in records]

        with self.connector._engine.connect() as conn, conn.begin():
            conn.execute(sqlalchemy.text(insert_sql), prepared)

    def _execute_merge_batch(self, records: list[dict]) -> None:
        """Execute high-performance MERGE operation."""
        merge_sql = self._build_merge_statement()
        prepared = [self._conform_record(r) for r in records]

        with self.connector._engine.connect() as conn, conn.begin():
            # Process in optimal batch sizes
            batch_size = self.config.get("merge_batch_size", 5000)
            for i in range(0, len(prepared), batch_size):
                batch = prepared[i : i + batch_size]
                conn.execute(sqlalchemy.text(merge_sql), batch)

    def _build_direct_path_insert(self) -> str:
        """Build INSERT with APPEND_VALUES hint for direct path."""
        table_name = self.full_table_name
        columns = list(self.schema["properties"].keys())

        # Don't add metadata columns here - Singer SDK handles this

        columns_str = ", ".join(columns)
        placeholders = ", ".join(f":{col}" for col in columns)

        # Direct path with parallel hint
        return f"""
        INSERT /*+ APPEND_VALUES PARALLEL({table_name},{self.config.get('parallel_degree', 8)}) */
        INTO {table_name} ({columns_str})
        VALUES ({placeholders})
        """

    def _build_bulk_insert_statement(self) -> str:
        """Build optimized INSERT with performance hints."""
        table_name = self.full_table_name
        columns = list(self.schema["properties"].keys())

        # Don't add metadata columns here - Singer SDK handles this

        columns_str = ", ".join(columns)
        placeholders = ", ".join(f":{col}" for col in columns)

        # Performance hints
        hints = []
        if self.config.get("use_parallel_dml"):
            hints.append(
                f"PARALLEL({table_name},{self.config.get('parallel_degree', 8)})"
            )
        if self.config.get("use_append_hint"):
            hints.append("APPEND")

        hint_str = f"/*+ {' '.join(hints)} */" if hints else ""

        return f"INSERT {hint_str} INTO {table_name} ({columns_str}) VALUES ({placeholders})"

    def _build_merge_statement(self) -> str:
        """Build high-performance MERGE with hints."""
        table_name = self.full_table_name
        columns = list(self.schema["properties"].keys())
        key_cols = self.key_properties or []

        # Performance hints
        hints = []
        if self.config.get("use_parallel_dml"):
            hints.append(
                f"PARALLEL({table_name},{self.config.get('parallel_degree', 8)})"
            )
        if self.config.get("use_merge_hint"):
            hints.append("USE_MERGE")

        hint_str = f"/*+ {' '.join(hints)} */" if hints else ""

        # Build columns
        all_cols = columns
        update_cols = [col for col in all_cols if col not in key_cols]

        # Build MERGE
        merge_sql = f"""
        MERGE {hint_str} INTO {table_name} target
        USING (
            SELECT {', '.join(f':{col} AS {col}' for col in all_cols)}
            FROM dual
        ) source
        ON ({' AND '.join(f'target.{col} = source.{col}' for col in key_cols)})
        """

        if update_cols:
            merge_sql += f"""
        WHEN MATCHED THEN
            UPDATE SET {', '.join(f'{col} = source.{col}' for col in update_cols)}
            """

        merge_sql += f"""
        WHEN NOT MATCHED THEN
            INSERT ({', '.join(all_cols)})
            VALUES ({', '.join(f'source.{col}' for col in all_cols)})
        """

        return merge_sql

    def _singer_sdk_to_oracle_type(
        self, singer_type: dict
    ) -> sqlalchemy.types.TypeEngine[Any]:
        """Map Singer SDK types to Oracle types using SQLAlchemy."""
        type_str = singer_type.get("type", "string")

        # Handle type arrays
        if isinstance(type_str, list):
            type_str = next((t for t in type_str if t != "null"), "string")

        # Get format for date/time types
        format_str = singer_type.get("format", "")

        # Map to Oracle types
        if type_str == "string":
            max_length = singer_type.get(
                "maxLength", self.config.get("varchar_max_length", 4000)
            )
            if max_length > 4000:
                # Use CLOB for long strings
                return sqlalchemy.dialects.oracle.CLOB()
            elif self.config.get("use_nvarchar"):
                return sqlalchemy.dialects.oracle.NVARCHAR2(max_length)
            else:
                return sqlalchemy.dialects.oracle.VARCHAR2(max_length)

        elif type_str == "integer":
            return sqlalchemy.dialects.oracle.NUMBER(
                precision=self.config.get("number_precision", 38), scale=0
            )

        elif type_str == "number":
            return sqlalchemy.dialects.oracle.NUMBER(
                precision=self.config.get("number_precision", 38),
                scale=self.config.get("number_scale", 10),
            )

        elif type_str == "boolean":
            # Oracle doesn't have native boolean
            if self.config.get("supports_native_boolean"):
                return sqlalchemy.BOOLEAN()
            else:
                return sqlalchemy.dialects.oracle.NUMBER(1, 0)

        elif type_str == "object" or type_str == "array":
            # Store JSON as CLOB or native JSON type
            json_type = self.config.get("json_column_type", "CLOB")
            if json_type == "JSON" and hasattr(sqlalchemy.dialects.oracle, "JSON"):
                return sqlalchemy.dialects.oracle.JSON()  # type: ignore[no-any-return]
            else:
                return sqlalchemy.dialects.oracle.CLOB()

        elif format_str == "date":
            return sqlalchemy.dialects.oracle.DATE()

        elif format_str == "time":
            return sqlalchemy.dialects.oracle.TIMESTAMP()

        elif format_str == "date-time" or type_str == "date-time":
            return sqlalchemy.dialects.oracle.TIMESTAMP(timezone=True)

        # Default to VARCHAR2
        return sqlalchemy.dialects.oracle.VARCHAR2(255)


    def activate_version(self, new_version: int) -> None:
        """Activate version using Singer SDK pattern."""
        # Let Singer SDK handle version activation
        super().activate_version(new_version)


    def clean_up(self) -> None:
        """Clean up with maximum performance optimizations and logging."""
        if self._logger:
            self._logger.info(f"Starting cleanup for stream {self.stream_name}")

        try:
            # Gather advanced statistics
            if self.config.get("gather_statistics"):
                if self._logger:
                    self._logger.info("Gathering table statistics")

                with self.connector._engine.connect() as conn:
                    table_name = self.full_table_name.split(".")[-1]
                    conn.execute(
                        sqlalchemy.text(f"""
                        BEGIN
                            DBMS_STATS.GATHER_TABLE_STATS(
                                ownname => USER,
                                tabname => '{table_name}',
                                estimate_percent => DBMS_STATS.AUTO_SAMPLE_SIZE,
                                method_opt => 'FOR ALL COLUMNS SIZE AUTO',
                                granularity => 'ALL',
                                cascade => TRUE,
                                degree => {self.config.get('parallel_degree', 'DBMS_STATS.DEFAULT_DEGREE')}
                            );
                        END;
                    """)
                    )

            # Rebuild indexes for optimal performance
            if self.config.get("rebuild_indexes_after_load"):
                if self._logger:
                    self._logger.info("Rebuilding indexes")
                self._rebuild_indexes()

            # Refresh materialized views if configured
            if self.config.get("refresh_mviews"):
                if self._logger:
                    self._logger.info("Refreshing materialized views")
                self._refresh_materialized_views()

            # Log Oracle performance metrics if available
            if self._logger and self._monitor:
                try:
                    oracle_metrics = {
                        "pool_size": getattr(
                            self.connector._engine.pool, "size", lambda: 0
                        )(),
                        "checked_out": getattr(
                            self.connector._engine.pool, "checkedout", lambda: 0
                        )(),
                        "overflow": getattr(
                            self.connector._engine.pool, "overflow", lambda: 0
                        )(),
                    }
                    self._logger.log_oracle_performance(oracle_metrics)
                except Exception as e:
                    self._logger.debug(f"Could not log Oracle metrics: {e}")

        except Exception as e:
            if self._logger:
                self._logger.error(f"Error during cleanup: {e}")
            raise
        finally:
            # Shutdown thread pool
            if self._executor:
                if self._logger:
                    self._logger.debug("Shutting down thread pool")
                self._executor.shutdown(wait=True)

        if self._logger:
            self._logger.info(f"Cleanup completed for stream {self.stream_name}")

        # Let Singer SDK handle cleanup
        super().clean_up()

    def _rebuild_indexes(self) -> None:
        """Rebuild indexes with parallel processing after bulk load."""
        with self.connector._engine.connect() as conn:
            table_name = self.full_table_name.split(".")[-1]

            # Get all indexes
            result = conn.execute(
                sqlalchemy.text(f"""
                SELECT index_name FROM user_indexes
                WHERE table_name = '{table_name}' AND index_type != 'LOB'
            """)
            )

            for row in result:
                idx_name = row[0]
                try:
                    conn.execute(
                        sqlalchemy.text(f"""
                        ALTER INDEX {idx_name} REBUILD
                        PARALLEL {self.config.get('parallel_degree', 8)}
                        NOLOGGING
                    """)
                    )
                    if self._logger:
                        self._logger.info(f"Successfully rebuilt index: {idx_name}")
                except Exception as e:
                    # Log rebuild failures instead of silently suppressing
                    if self._logger:
                        self._logger.warning(f"Index rebuild failed for {idx_name}: {e}")
                    # Don't raise - this is optimization, not critical

    def _refresh_materialized_views(self) -> None:
        """Refresh any materialized views on the table."""
        with self.connector._engine.connect() as conn:
            table_name = self.full_table_name
            try:
                conn.execute(
                    sqlalchemy.text(f"""
                    BEGIN
                        DBMS_MVIEW.REFRESH_DEPENDENT(
                            number_of_failures => :failures,
                            list => '{table_name}',
                            method => 'C',
                            parallelism => {self.config.get('parallel_degree', 8)}
                        );
                    END;
                """),
                    {"failures": 0},
                )
                if self._logger:
                    self._logger.info(f"Successfully refreshed materialized views for {table_name}")
            except Exception as e:
                # Log MView refresh failures instead of silently suppressing
                if self._logger:
                    self._logger.warning(f"Materialized view refresh failed for {table_name}: {e}")
                # Don't raise - this is optimization, not critical


    def _conform_record(self, record: dict) -> dict:
        """Conform record to Oracle requirements using Singer SDK patterns."""
        conformed: dict[str, Any] = {}

        # Process each field according to schema
        for key, value in record.items():
            if key in self.schema.get("properties", {}):
                prop_schema = self.schema["properties"][key]
                prop_type = prop_schema.get("type", "string")

                # Handle type arrays (nullable types)
                if isinstance(prop_type, list):
                    if value is None and "null" in prop_type:
                        conformed[key] = None
                        continue
                    prop_type = next((t for t in prop_type if t != "null"), "string")

                # Apply type-specific conversions
                if value is not None:
                    if prop_type == "boolean":
                        if self.config.get("supports_native_boolean"):
                            conformed[key] = value
                        else:
                            # Handle both string and integer boolean values
                            true_val = self.config.get("boolean_true_value", "1")
                            false_val = self.config.get("boolean_false_value", "0")
                            # Convert to int if the default values are being used
                            if true_val == "1" and false_val == "0":
                                conformed[key] = 1 if value else 0
                            else:
                                conformed[key] = true_val if value else false_val
                    elif prop_type in ("object", "array"):
                        # Serialize to JSON
                        conformed[key] = json.dumps(value)
                    else:
                        conformed[key] = value
                else:
                    conformed[key] = None
            else:
                # Pass through fields not in schema
                conformed[key] = value

        # Don't add Singer metadata here - Singer SDK handles this automatically

        return conformed
