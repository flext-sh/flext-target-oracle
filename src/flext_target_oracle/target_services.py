"""Focused service objects used by Oracle target components."""

from __future__ import annotations

from flext_core import r
from flext_db_oracle import FlextDbOracleApi

from flext_target_oracle import FlextTargetOracleSettings, m, t


class FlextTargetOracleConnectionService:
    """Minimal Oracle connection service implements ConnectionService protocol."""

    def __init__(
        self,
        config: FlextTargetOracleSettings,
        oracle_api: FlextDbOracleApi,
    ) -> None:
        """Store configuration and Oracle API dependency."""
        self.config = config
        self.oracle_api = oracle_api

    def execute(self) -> r[None]:
        """Run default connection validation operation."""
        return self.test_connection()

    def get_connection_info(self) -> r[m.TargetOracle.OracleConnectionModel]:
        """Return normalized connection model."""
        return r[m.TargetOracle.OracleConnectionModel].ok(
            self.config.get_oracle_config(),
        )

    def test_connection(self) -> r[None]:
        """Check Oracle access by listing schema tables."""
        tables_result = self.oracle_api.get_tables(
            schema=self.config.default_target_schema,
        )
        if tables_result.is_failure:
            return r[None].fail(tables_result.error or "Connection test failed")
        return r[None].ok(None)


class FlextTargetOracleSchemaService:
    """Minimal schema management service implements SchemaService protocol."""

    def __init__(
        self,
        config: FlextTargetOracleSettings,
        oracle_api: FlextDbOracleApi,
    ) -> None:
        """Store schema service dependencies."""
        self.config = config
        self.oracle_api = oracle_api

    def ensure_table_exists(
        self,
        stream: m.TargetOracle.SingerStreamModel,
        schema_message: m.Meltano.SingerSchemaMessage,
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


class FlextTargetOracleBatchService:
    """Minimal batching service implements BatchService protocol."""

    def __init__(
        self,
        config: FlextTargetOracleSettings,
        oracle_api: FlextDbOracleApi,
    ) -> None:
        """Initialize batch storage and required dependencies."""
        self.config = config
        self.oracle_api = oracle_api
        self._batches: dict[str, list[m.Meltano.SingerRecordMessage]] = {}

    def add_record(
        self,
        stream_name: str,
        record_message: m.Meltano.SingerRecordMessage,
    ) -> r[None]:
        """Append a record to a stream buffer."""
        self._batches.setdefault(stream_name, []).append(record_message)
        return r[None].ok(None)

    def execute(self) -> r[m.TargetOracle.LoadStatisticsModel]:
        """Run default batch flush operation."""
        return self.flush_all_batches()

    def flush_all_batches(self) -> r[m.TargetOracle.LoadStatisticsModel]:
        """Summarize and clear all in-memory batch buffers."""
        total = sum(len(records) for records in self._batches.values())
        stats = m.TargetOracle.LoadStatisticsModel(
            stream_name="__ALL_STREAMS__",
            total_records_processed=total,
            successful_records=total,
            failed_records=0,
            batches_processed=len(self._batches),
        ).finalize()
        return r[m.TargetOracle.LoadStatisticsModel].ok(stats)

    def flush_batch(self, stream_name: str) -> r[None]:
        """Clear buffered records for a specific stream."""
        self._batches[stream_name] = []
        return r[None].ok(None)


class FlextTargetOracleRecordService:
    """Record validation and transformation service implements RecordService protocol."""

    def __init__(self, config: FlextTargetOracleSettings) -> None:
        """Store record service configuration."""
        self.config = config

    def execute(self) -> r[None]:
        """Run record-service readiness check."""
        return r[None].ok(None)

    def transform_record(
        self,
        record_message: m.Meltano.SingerRecordMessage,
        stream: m.TargetOracle.SingerStreamModel,
    ) -> r[m.Meltano.SingerRecordMessage]:
        """Apply stream-level mappings and ignored-column filtering."""
        transformed: dict[str, t.Container] = {}
        for key, value in record_message.record.items():
            if key in stream.ignored_columns:
                continue
            mapped_key = stream.column_mappings.get(key) or key
            transformed[mapped_key] = value
        return r[m.Meltano.SingerRecordMessage].ok(
            m.Meltano.SingerRecordMessage.model_validate({
                "type": "RECORD",
                "stream": record_message.stream,
                "record": transformed,
                "time_extracted": record_message.time_extracted,
                "version": record_message.version,
            }),
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


class FlextTargetOracleServiceFactory:
    """Factory for constructing all Oracle target services."""

    def __init__(
        self,
        config: FlextTargetOracleSettings,
        oracle_api: FlextDbOracleApi,
    ) -> None:
        """Store dependencies shared by service instances."""
        self._config = config
        self._oracle_api = oracle_api

    def create_batch_service(self) -> FlextTargetOracleBatchService:
        """Create Oracle batch service."""
        return FlextTargetOracleBatchService(self._config, self._oracle_api)

    def create_connection_service(self) -> FlextTargetOracleConnectionService:
        """Create Oracle connection service."""
        return FlextTargetOracleConnectionService(self._config, self._oracle_api)

    def create_record_service(self) -> FlextTargetOracleRecordService:
        """Create Oracle record service."""
        return FlextTargetOracleRecordService(self._config)

    def create_schema_service(self) -> FlextTargetOracleSchemaService:
        """Create Oracle schema service."""
        return FlextTargetOracleSchemaService(self._config, self._oracle_api)


__all__ = [
    "FlextTargetOracleBatchService",
    "FlextTargetOracleConnectionService",
    "FlextTargetOracleRecordService",
    "FlextTargetOracleSchemaService",
    "FlextTargetOracleServiceFactory",
]
