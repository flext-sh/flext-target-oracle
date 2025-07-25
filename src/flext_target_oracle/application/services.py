"""Singer Target Application Services.

Simplified Oracle Singer target using flext-core patterns and flext-db-oracle.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from flext_core import FlextResult
from flext_core.patterns.logging import get_logger
from flext_db_oracle import FlextDbOracleConfig
from flext_db_oracle.application.services import (
    FlextDbOracleConnectionService,
    FlextDbOracleQueryService,
)

from flext_target_oracle.domain.models import (
    LoadStatistics,
    SingerRecord,
    SingerSchema,
)

if TYPE_CHECKING:
    from flext_target_oracle.domain.models import FlextTargetOracleConfig

logger = get_logger(__name__)


class FlextSingerTargetService:
    """Main service for Singer target operations."""

    def __init__(self, config: FlextTargetOracleConfig) -> None:
        """Initialize the Singer target service."""
        self.config = config

        # Oracle services
        oracle_config = FlextDbOracleConfig(**config.oracle_config)
        self.connection_service = FlextDbOracleConnectionService(oracle_config)
        self.query_service = FlextDbOracleQueryService(self.connection_service)

        # Loader service
        self.loader_service = FlextOracleLoaderService(
            self.connection_service,
            self.query_service,
            config,
        )

    async def process_singer_message(self, message: dict[str, Any]) -> FlextResult[Any]:
        """Process a Singer message (RECORD, SCHEMA, or STATE)."""
        try:
            record = SingerRecord(**message)

            if record.type == "SCHEMA":
                return await self._handle_schema(record)
            if record.type == "RECORD":
                return await self._handle_record(record)
            if record.type == "STATE":
                return await self._handle_state(record)
            return FlextResult.fail(f"Unknown message type: {record.type}")

        except Exception as e:
            logger.exception("Failed to process Singer message", exception=e)
            return FlextResult.fail(f"Message processing failed: {e}")

    async def _handle_schema(self, record: SingerRecord) -> FlextResult[Any]:
        """Handle SCHEMA message."""
        if not record.record_schema or not record.stream:
            return FlextResult.fail("Schema message missing schema or stream")

        # Convert dict to SingerSchema
        schema_dict = record.record_schema
        schema = SingerSchema(
            type=schema_dict.get("type", "object"),
            properties=schema_dict.get("properties", {}),
            key_properties=schema_dict.get("key_properties", []),
            required=schema_dict.get("required", []),
        )

        # Create/update table schema
        result = await self.loader_service.ensure_table_exists(record.stream, schema)

        if result.is_success:
            logger.info(f"Schema processed for stream: {record.stream}")

        return result

    async def _handle_record(self, record: SingerRecord) -> FlextResult[Any]:
        """Handle RECORD message."""
        if not record.record or not record.stream:
            return FlextResult.fail("Record message missing data or stream")

        return await self.loader_service.load_record(record.stream, record.record)

    async def _handle_state(self, record: SingerRecord) -> FlextResult[Any]:
        """Handle STATE message."""
        if not record.record:
            logger.warning("STATE message received but record is empty")
            return FlextResult.ok(None)

        logger.debug("State message forwarded to stdout for Meltano state management")
        return FlextResult.ok(None)

    async def finalize_all_streams(self) -> FlextResult[Any]:
        """Finalize all active streams and return statistics."""
        return await self.loader_service.finalize_all_streams()


class FlextOracleLoaderService:
    """Service for loading data into Oracle using flext-db-oracle."""

    def __init__(
        self,
        connection_service: FlextDbOracleConnectionService,
        query_service: FlextDbOracleQueryService,
        config: FlextTargetOracleConfig,
    ) -> None:
        """Initialize the Oracle loader service."""
        self.connection_service = connection_service
        self.query_service = query_service
        self.config = config
        self._record_buffers: dict[str, list[dict[str, Any]]] = {}
        self._total_records = 0

    async def ensure_table_exists(
        self,
        stream_name: str,
        schema: SingerSchema,
    ) -> FlextResult[Any]:
        """Ensure target table exists with correct schema."""
        try:
            table_name = self._get_table_name(stream_name)
            logger.info(f"Ensuring table exists: stream={stream_name}, table={table_name}")

            # Check if table exists
            check_sql = """
            SELECT COUNT(*)
            FROM all_tables
            WHERE owner = UPPER(:schema_name)
            AND table_name = UPPER(:table_name)
            """

            result = await self.query_service.execute_scalar(
                check_sql,
                {
                    "schema_name": self.config.default_target_schema,
                    "table_name": table_name,
                },
            )

            if not result.is_success:
                return FlextResult.fail(f"Failed to check table existence: {result.error}")

            table_exists = result.data and result.data > 0

            if not table_exists:
                # Create table based on schema
                create_result = await self._create_table(table_name, schema)
                if not create_result.is_success:
                    return create_result
                logger.info(f"Created table: {self.config.default_target_schema}.{table_name}")

            return FlextResult.ok(None)

        except Exception as e:
            logger.exception(f"Failed to ensure table exists for stream {stream_name}", exception=e)
            return FlextResult.fail(f"Table creation failed: {e}")

    async def load_record(
        self,
        stream_name: str,
        record_data: dict[str, Any],
    ) -> FlextResult[Any]:
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

        except Exception as e:
            logger.exception(f"Failed to load record for stream {stream_name}", exception=e)
            return FlextResult.fail(f"Record loading failed: {e}")

    async def finalize_all_streams(self) -> FlextResult[Any]:
        """Flush all pending batches and return statistics."""
        try:
            # Flush all remaining batches
            for stream_name in list(self._record_buffers.keys()):
                if self._record_buffers[stream_name]:
                    result = await self._flush_batch(stream_name)
                    if not result.is_success:
                        logger.error(f"Failed to flush final batch for {stream_name}: {result.error}")

            # Return simple statistics
            stats = LoadStatistics(
                total_records=self._total_records,
                successful_records=self._total_records,
                failed_records=0,
            )

            logger.info(f"Finalization complete: {stats.total_records} records processed")
            return FlextResult.ok(stats)

        except Exception as e:
            logger.exception("Failed to finalize streams", exception=e)
            return FlextResult.fail(f"Finalization failed: {e}")

    async def _flush_batch(self, stream_name: str) -> FlextResult[Any]:
        """Flush pending records for a stream."""
        try:
            if stream_name not in self._record_buffers or not self._record_buffers[stream_name]:
                return FlextResult.ok(None)

            records = self._record_buffers[stream_name]
            table_name = self._get_table_name(stream_name)

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

        except Exception as e:
            logger.exception(f"Failed to flush batch for stream {stream_name}", exception=e)
            return FlextResult.fail(f"Batch flush failed: {e}")

    async def _insert_batch(
        self,
        table_name: str,
        records: list[dict[str, Any]],
    ) -> FlextResult[Any]:
        """Insert batch of records."""
        try:
            if not records:
                return FlextResult.ok(None)

            # Simple JSON storage approach
            schema_name = self.config.default_target_schema.upper()
            table_name_upper = table_name.upper()

            # Build INSERT SQL using template (schema_name and table_name are validated)
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

            # Execute insert
            async with self.connection_service.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.executemany(sql, params)
                    conn.commit()

            return FlextResult.ok(None)

        except Exception as e:
            logger.exception(f"Failed to insert batch to {table_name}", exception=e)
            return FlextResult.fail(f"Batch insert failed: {e}")

    async def _create_table(
        self,
        table_name: str,
        schema: SingerSchema,
    ) -> FlextResult[Any]:
        """Create table from Singer schema."""
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

            # Execute via connection service
            async with self.connection_service.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(create_sql)
                    conn.commit()

            return FlextResult.ok(None)

        except Exception as e:
            logger.exception(f"Failed to create table {table_name}", exception=e)
            return FlextResult.fail("Table creation failed")

    def _get_table_name(self, stream_name: str) -> str:
        """Convert stream name to Oracle table name."""
        base_name = stream_name.upper().replace("-", "_").replace(".", "_")
        if self.config.table_prefix:
            return f"{self.config.table_prefix}{base_name}"
        return base_name


# Compatibility aliases
SingerTargetService = FlextSingerTargetService
OracleLoaderService = FlextOracleLoaderService
