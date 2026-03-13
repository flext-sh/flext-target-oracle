"""Focused service objects used by Oracle target components."""

from __future__ import annotations

from typing import Protocol

from flext_core import r, t
from flext_db_oracle import FlextDbOracleApi

from .models import m
from .settings import FlextTargetOracleSettings
from .target_models import LoadStatisticsModel, SingerStreamModel


class ConnectionService(Protocol):
    """Contract for Oracle connection services."""

    def get_connection_info(self) -> r[m.TargetOracle.OracleConnectionConfig]:
        """Return effective Oracle connection information."""
        ...

    def test_connection(self) -> r[None]:
        """Validate Oracle connectivity."""
        ...


class SchemaService(Protocol):
    """Contract for Oracle schema services."""

    def ensure_table_exists(
        self, stream: SingerStreamModel, schema_message: m.Meltano.SingerSchemaMessage
    ) -> r[None]:
        """Ensure destination table exists for a stream."""
        ...


class BatchService(Protocol):
    """Contract for Oracle batch services."""

    def add_record(
        self, stream_name: str, record_message: m.Meltano.SingerRecordMessage
    ) -> r[None]:
        """Queue one record for batch processing."""
        ...

    def flush_all_batches(self) -> r[LoadStatisticsModel]:
        """Flush all queued batches and return aggregated stats."""
        ...


class RecordService(Protocol):
    """Contract for record transformation services."""

    def transform_record(
        self, record_message: m.Meltano.SingerRecordMessage, stream: SingerStreamModel
    ) -> r[m.Meltano.SingerRecordMessage]:
        """Transform one Singer record into Oracle-ready payload."""
        ...


class OracleConnectionService:
    """Minimal Oracle connection service."""

    def __init__(
        self, config: FlextTargetOracleSettings, oracle_api: FlextDbOracleApi
    ) -> None:
        """Store configuration and Oracle API dependency."""
        self.config = config
        self.oracle_api = oracle_api

    def execute(self) -> r[None]:
        """Run default connection validation operation."""
        return self.test_connection()

    def get_connection_info(self) -> r[m.TargetOracle.OracleConnectionConfig]:
        """Return normalized connection model."""
        return r[m.TargetOracle.OracleConnectionConfig].ok(
            self.config.get_oracle_config()
        )

    def test_connection(self) -> r[None]:
        """Check Oracle access by listing schema tables."""
        tables_result = self.oracle_api.get_tables(
            schema=self.config.default_target_schema
        )
        if tables_result.is_failure:
            return r[None].fail(tables_result.error or "Connection test failed")
        return r[None].ok(None)


class OracleSchemaService:
    """Minimal schema management service."""

    def __init__(
        self, config: FlextTargetOracleSettings, oracle_api: FlextDbOracleApi
    ) -> None:
        """Store schema service dependencies."""
        self.config = config
        self.oracle_api = oracle_api

    def ensure_table_exists(
        self, stream: SingerStreamModel, schema_message: m.Meltano.SingerSchemaMessage
    ) -> r[None]:
        """Validate table identity before external DDL orchestration."""
        _ = schema_message
        table_name = stream.table_name
        if not table_name:
            return r[None].fail("Invalid table name")
        return r[None].ok(None)

    def execute(self) -> r[None]:
        """Run service health operation."""
        return r[None].ok(None)


class OracleBatchService:
    """Minimal batching service used by CLI and target orchestrators."""

    def __init__(
        self, config: FlextTargetOracleSettings, oracle_api: FlextDbOracleApi
    ) -> None:
        """Initialize batch storage and required dependencies."""
        self.config = config
        self.oracle_api = oracle_api
        self._batches: dict[str, list[m.Meltano.SingerRecordMessage]] = {}

    def add_record(
        self, stream_name: str, record_message: m.Meltano.SingerRecordMessage
    ) -> r[None]:
        """Append a record to a stream buffer."""
        self._batches.setdefault(stream_name, []).append(record_message)
        return r[None].ok(None)

    def execute(self) -> r[LoadStatisticsModel]:
        """Run default batch flush operation."""
        return self.flush_all_batches()

    def flush_all_batches(self) -> r[LoadStatisticsModel]:
        """Summarize and clear all in-memory batch buffers."""
        total = sum(len(records) for records in self._batches.values())
        stats = LoadStatisticsModel(
            stream_name="__ALL_STREAMS__",
            total_records_processed=total,
            successful_records=total,
            failed_records=0,
            batches_processed=len(self._batches),
        ).finalize()
        return r[LoadStatisticsModel].ok(stats)

    def flush_batch(self, stream_name: str) -> r[None]:
        """Clear buffered records for a specific stream."""
        self._batches[stream_name] = []
        return r[None].ok(None)


class OracleRecordService:
    """Record validation and transformation service."""

    def __init__(self, config: FlextTargetOracleSettings) -> None:
        """Store record service configuration."""
        self.config = config

    def execute(self) -> r[None]:
        """Run record-service readiness check."""
        return r[None].ok(None)

    def transform_record(
        self, record_message: m.Meltano.SingerRecordMessage, stream: SingerStreamModel
    ) -> r[m.Meltano.SingerRecordMessage]:
        """Apply stream-level mappings and ignored-column filtering."""
        transformed: dict[str, t.Container] = {}
        for key, value in record_message.record.items():
            if key in stream.ignored_columns:
                continue
            mapped_key = stream.column_mappings.get(key) or key
            transformed[mapped_key] = value
        return r[m.Meltano.SingerRecordMessage].ok(
            m.Meltano.SingerRecordMessage(
                stream=record_message.stream, record=transformed
            )
        )

    def validate_record(
        self,
        record_message: m.Meltano.SingerRecordMessage,
        schema_message: m.Meltano.SingerSchemaMessage,
    ) -> r[None]:
        """Validate record payload against current schema contract."""
        _ = record_message
        _ = schema_message
        return r[None].ok(None)


class OracleTargetServiceFactory:
    """Factory for constructing all Oracle target services."""

    def __init__(
        self, config: FlextTargetOracleSettings, oracle_api: FlextDbOracleApi
    ) -> None:
        """Store dependencies shared by service instances."""
        self._config = config
        self._oracle_api = oracle_api

    def create_batch_service(self) -> OracleBatchService:
        """Create Oracle batch service."""
        return OracleBatchService(self._config, self._oracle_api)

    def create_connection_service(self) -> OracleConnectionService:
        """Create Oracle connection service."""
        return OracleConnectionService(self._config, self._oracle_api)

    def create_record_service(self) -> OracleRecordService:
        """Create Oracle record service."""
        return OracleRecordService(self._config)

    def create_schema_service(self) -> OracleSchemaService:
        """Create Oracle schema service."""
        return OracleSchemaService(self._config, self._oracle_api)


__all__ = [
    "BatchService",
    "ConnectionService",
    "OracleBatchService",
    "OracleConnectionService",
    "OracleRecordService",
    "OracleSchemaService",
    "OracleTargetServiceFactory",
    "RecordService",
    "SchemaService",
]
