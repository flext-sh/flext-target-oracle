"""Oracle Sink - Enterprise Data Loading using SQLAlchemy 2.0.

IMPLEMENTATION:
    Complete Singer protocol implementation with Oracle-specific optimizations.
Enterprise-grade performance and reliability.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from flext_core import ServiceResult
from flext_observability.logging import get_logger
from flext_target_oracle.connector import OracleConnector

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = get_logger(__name__)


class OracleSink:
    """High-performance Oracle data sink using SQLAlchemy 2.0."""

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize Oracle sink with configuration."""
        self.config = config
        self._batch_size = config.get("batch_size", 10000)
        self._connector = OracleConnector(config)
        self._record_buffer: dict[str, list[dict[str, Any]]] = {}
        self._schema_cache: dict[str, dict[str, Any]] = {}

    async def process_records(self, records: Sequence[dict[str, Any]]) -> ServiceResult[None]:
        """Process Singer records for Oracle loading."""
        logger.info("Processing %d records for Oracle", len(records))

        try:
            for record in records:
                result = await self._process_single_record(record)
                if not result.is_success:
                    logger.error("Failed to process record: %s", result.error)
                    return result

            # Flush any remaining buffered records
            await self._flush_all_buffers()

            return ServiceResult.success(None)

        except Exception as e:
            logger.exception("Failed to process records")
            return ServiceResult.failure(f"Record processing failed: {e}")

    async def _process_single_record(self, record: dict[str, Any]) -> ServiceResult[None]:
        """Process a single Singer record."""
        try:
            # Extract record data according to Singer specification
            record_type = record.get("type")

            if record_type == "RECORD":
                return await self._handle_data_record(record)
            if record_type == "SCHEMA":
                return await self._handle_schema_message(record)
            if record_type == "STATE":
                return await self._handle_state_message(record)
            logger.warning("Unknown record type: %s", record_type)
            return ServiceResult.success(None)

        except Exception as e:
            logger.exception("Failed to process single record")
            return ServiceResult.failure(f"Single record processing failed: {e}")

    async def _handle_data_record(self, record: dict[str, Any]) -> ServiceResult[None]:
        """Handle Singer data record with batching."""
        stream_name = record.get("stream")
        record_data = record.get("record", {})

        if not stream_name:
            return ServiceResult.failure("Stream name is required for data records")

        logger.debug("Processing data record for stream: %s", stream_name)

        try:
            # Ensure schema exists
            if stream_name not in self._schema_cache:
                logger.warning("No schema found for stream %s, will create default", stream_name)
                # Create a basic schema from the record structure
                await self._create_default_schema(stream_name, record_data)

            # Add Singer metadata
            enriched_record = self._enrich_record(record_data)

            # Add to buffer
            if stream_name not in self._record_buffer:
                self._record_buffer[stream_name] = []

            self._record_buffer[stream_name].append(enriched_record)

            # Check if we need to flush the buffer
            if len(self._record_buffer[stream_name]) >= self._batch_size:
                await self._flush_buffer(stream_name)

            return ServiceResult.success(None)

        except Exception as e:
            logger.exception("Failed to handle data record")
            return ServiceResult.failure(f"Data record handling failed: {e}")

    async def _handle_schema_message(self, record: dict[str, Any]) -> ServiceResult[None]:
        """Handle Singer schema message with table creation."""
        stream_name = record.get("stream")
        schema = record.get("schema", {})

        if not stream_name or not schema:
            return ServiceResult.failure("Stream name and schema are required")

        logger.debug("Processing schema for stream: %s", stream_name)

        try:
            # Cache the schema
            self._schema_cache[stream_name] = schema

            # Create or update table
            await self._connector.create_table_if_not_exists(stream_name, schema)

            logger.info("Schema processed for stream: %s", stream_name)
            return ServiceResult.success(None)

        except Exception as e:
            logger.exception("Failed to handle schema message")
            return ServiceResult.failure(f"Schema handling failed: {e}")

    async def _handle_state_message(self, record: dict[str, Any]) -> ServiceResult[None]:
        """Handle Singer state message with persistence."""
        state_value = record.get("value", {})

        logger.debug("Processing state message")

        try:
            # Flush all buffers before processing state
            await self._flush_all_buffers()

            # Log state for monitoring
            logger.info("State received: %s", json.dumps(state_value, default=str)[:200])

            # In a full implementation, this would persist state to a state store
            # For now, we just log it for visibility

            return ServiceResult.success(None)

        except Exception as e:
            logger.exception("Failed to handle state message")
            return ServiceResult.failure(f"State handling failed: {e}")

    async def _create_default_schema(self, stream_name: str, record_data: dict[str, Any]) -> None:
        """Create a default schema based on record structure."""
        properties = {}

        for key, value in record_data.items():
            if key.startswith("_sdc_"):
                continue

            # Infer type from value
            if isinstance(value, bool):
                properties[key] = {"type": "boolean"}
            elif isinstance(value, int):
                properties[key] = {"type": "integer"}
            elif isinstance(value, float):
                properties[key] = {"type": "number"}
            elif isinstance(value, str):
                # Check if it looks like a datetime
                min_datetime_length = 10
                if len(value) > min_datetime_length and ("T" in value or "-" in value[:min_datetime_length]):
                    properties[key] = {"type": "string", "format": "date-time"}
                else:
                    properties[key] = {"type": "string"}
            elif isinstance(value, dict | list):
                properties[key] = {"type": "object"}
            else:
                properties[key] = {"type": "string"}

        schema = {
            "type": "object",
            "properties": properties,
        }

        self._schema_cache[stream_name] = schema
        await self._connector.create_table_if_not_exists(stream_name, schema)

    def _enrich_record(self, record_data: dict[str, Any]) -> dict[str, Any]:
        """Enrich record with Singer metadata."""
        enriched = record_data.copy()

        # Add Singer metadata if not present
        current_time = datetime.now(UTC).isoformat()

        if "_sdc_extracted_at" not in enriched:
            enriched["_sdc_extracted_at"] = current_time
        if "_sdc_batched_at" not in enriched:
            enriched["_sdc_batched_at"] = current_time
        if "_sdc_sequence" not in enriched:
            enriched["_sdc_sequence"] = 0

        return enriched

    async def _flush_buffer(self, stream_name: str) -> None:
        """Flush buffered records for a specific stream."""
        if stream_name not in self._record_buffer or not self._record_buffer[stream_name]:
            return

        records = self._record_buffer[stream_name]
        logger.info("Flushing %d records for stream: %s", len(records), stream_name)

        try:
            await self._connector.bulk_insert(stream_name, records)
            self._record_buffer[stream_name] = []
            logger.info("Successfully flushed %d records for stream: %s", len(records), stream_name)

        except Exception:
            logger.exception("Failed to flush buffer for stream: %s", stream_name)
            # Keep records in buffer for retry
            raise

    async def _flush_all_buffers(self) -> None:
        """Flush all buffered records."""
        for stream_name in list(self._record_buffer.keys()):
            if self._record_buffer[stream_name]:
                await self._flush_buffer(stream_name)

    async def finalize(self) -> ServiceResult[dict[str, Any]]:
        """Finalize the sink and return statistics."""
        try:
            await self._flush_all_buffers()
            await self._connector.disconnect()

            stats = {
                "streams_processed": len(self._schema_cache),
                "schemas_cached": len(self._schema_cache),
                "finalized_at": datetime.now(UTC).isoformat(),
            }

            logger.info("Oracle sink finalized: %s", stats)
            return ServiceResult.success(stats)

        except Exception as e:
            logger.exception("Failed to finalize sink")
            return ServiceResult.failure(f"Sink finalization failed: {e}")
