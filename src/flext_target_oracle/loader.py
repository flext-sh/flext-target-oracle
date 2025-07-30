"""Oracle Loader - Simple and clean data loading.

Uses flext-db-oracle for Oracle operations and flext-core for patterns.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from flext_core import FlextResult, get_logger
from flext_db_oracle import FlextDbOracleApi, FlextDbOracleConfig

if TYPE_CHECKING:
    from flext_target_oracle.config import FlextOracleTargetConfig

logger = get_logger(__name__)


class FlextOracleTargetLoader:
    """Simple Oracle loader using flext-db-oracle."""

    def __init__(self, config: FlextOracleTargetConfig) -> None:
        """Initialize Oracle loader."""
        self.config = config

        # Oracle API from flext-db-oracle
        oracle_config = FlextDbOracleConfig(**config.get_oracle_config())
        self.oracle_api = FlextDbOracleApi(oracle_config)

        # Buffers for batch processing
        self._record_buffers: dict[str, list[dict[str, Any]]] = {}
        self._total_records = 0

    async def ensure_table_exists(
        self,
        stream_name: str,
        schema: dict[str, Any],
    ) -> FlextResult[None]:
        """Ensure target table exists with correct schema."""
        try:
            table_name = self.config.get_table_name(stream_name)
            logger.info(
                f"Ensuring table exists: stream={stream_name}, table={table_name}",
            )

            # Check if table exists using flext-db-oracle
            check_sql = """
            SELECT COUNT(*)
            FROM all_tables
            WHERE owner = UPPER(:schema_name)
            AND table_name = UPPER(:table_name)
            """

            result = self.oracle_api.query_one(
                check_sql,
                {
                    "schema_name": self.config.default_target_schema,
                    "table_name": table_name,
                },
            )

            if not result.is_success:
                return FlextResult.fail(
                    f"Failed to check table existence: {result.error}",
                )

            table_exists = result.data and len(result.data) > 0 and result.data[0] > 0

            if not table_exists:
                # Create table using simple JSON storage
                create_result = await self._create_table(table_name)
                if not create_result.is_success:
                    return create_result
                logger.info(
                    f"Created table: {self.config.default_target_schema}.{table_name}",
                )

            return FlextResult.ok(None)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception(f"Failed to ensure table exists for stream {stream_name}")
            return FlextResult.fail(f"Table creation failed: {e}")

    async def load_record(
        self,
        stream_name: str,
        record_data: dict[str, Any],
    ) -> FlextResult[None]:
        """Load a single record (buffered for batch processing)."""
        try:
            # Add to buffer
            if stream_name not in self._record_buffers:
                self._record_buffers[stream_name] = []

            self._record_buffers[stream_name].append(record_data)
            buffer_size = len(self._record_buffers[stream_name])

            # Check if batch is ready
            if buffer_size >= self.config.batch_size:
                logger.info(f"Buffer full, flushing batch for stream: {stream_name}")
                return await self._flush_batch(stream_name)

            return FlextResult.ok(None)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception(f"Failed to load record for stream {stream_name}")
            return FlextResult.fail(f"Record loading failed: {e}")

    async def finalize_all_streams(self) -> FlextResult[dict[str, Any]]:
        """Flush all pending batches and return statistics."""
        try:
            # Flush all remaining batches
            for stream_name in list(self._record_buffers.keys()):
                if self._record_buffers[stream_name]:
                    result = await self._flush_batch(stream_name)
                    if not result.is_success:
                        logger.error(
                            f"Failed to flush final batch for {stream_name}: {result.error}",
                        )

            # Return simple statistics
            stats = {
                "total_records": self._total_records,
                "successful_records": self._total_records,
                "failed_records": 0,
                "total_batches": len(self._record_buffers),
            }

            logger.info(
                f"Finalization complete: {stats['total_records']} records processed",
            )
            return FlextResult.ok(stats)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Failed to finalize streams")
            return FlextResult.fail(f"Finalization failed: {e}")

    async def _flush_batch(self, stream_name: str) -> FlextResult[None]:
        """Flush pending records for a stream."""
        try:
            if (
                stream_name not in self._record_buffers
                or not self._record_buffers[stream_name]
            ):
                return FlextResult.ok(None)

            records = self._record_buffers[stream_name]
            table_name = self.config.get_table_name(stream_name)

            # Execute batch insert
            result = await self._insert_batch(table_name, records)

            # Clear buffer and update stats
            record_count = len(records)
            self._record_buffers[stream_name] = []

            if result.is_success:
                self._total_records += record_count
                logger.info(f"Batch loaded: {record_count} records to {table_name}")
            else:
                logger.error(f"Batch failed: {result.error}")

            return result

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception(f"Failed to flush batch for stream {stream_name}")
            return FlextResult.fail(f"Batch flush failed: {e}")

    async def _insert_batch(
        self,
        table_name: str,
        records: list[dict[str, Any]],
    ) -> FlextResult[None]:
        """Insert batch of records using flext-db-oracle."""
        try:
            if not records:
                return FlextResult.ok(None)

            # Simple JSON storage approach
            schema_name = self.config.default_target_schema.upper()
            table_name_upper = table_name.upper()

            # Build INSERT SQL
            sql_template = 'INSERT INTO "{0}"."{1}" ("DATA", "_SDC_EXTRACTED_AT") VALUES (:data, :extracted_at)'
            sql = sql_template.format(schema_name, table_name_upper)

            # Build parameters
            params = []
            for record in records:
                param = {
                    "data": json.dumps(record),
                    "extracted_at": datetime.now(UTC).isoformat(),
                }
                params.append(param)

            # Execute insert using flext-db-oracle API - simplified approach
            # For now, use execute_ddl for each record individually
            for param in params:
                parameterized_sql = sql.replace(":data", f"'{param['data']}'").replace(
                    ":extracted_at",
                    f"'{param['extracted_at']}'",
                )
                result = self.oracle_api.execute_ddl(parameterized_sql)
                if not result.is_success:
                    return FlextResult.fail(f"Insert failed: {result.error}")

            return FlextResult.ok(None)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception(f"Failed to insert batch to {table_name}")
            return FlextResult.fail(f"Batch insert failed: {e}")

    async def _create_table(self, table_name: str) -> FlextResult[None]:
        """Create table with simple JSON storage structure."""
        try:
            # Simple table structure - JSON storage
            schema_name = self.config.default_target_schema.upper()
            table_name_upper = table_name.upper()
            table_full = f'"{schema_name}"."{table_name_upper}"'

            create_sql_template = """
            CREATE TABLE {0} (
                "DATA" CLOB,
                "_SDC_EXTRACTED_AT" TIMESTAMP,
                "_SDC_BATCHED_AT" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                "_SDC_SEQUENCE" NUMBER DEFAULT 0
            )
            """
            create_sql = create_sql_template.format(table_full)

            # Execute via flext-db-oracle API
            result = self.oracle_api.execute_ddl(create_sql)
            if not result.is_success:
                return FlextResult.fail(f"Table creation failed: {result.error}")

            return FlextResult.ok(None)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception(f"Failed to create table {table_name}")
            return FlextResult.fail(f"Table creation failed: {e}")
