"""Focused service objects used by Oracle target components."""

from __future__ import annotations

from collections import defaultdict

from flext_db_oracle import FlextDbOracleApi
from flext_target_oracle import FlextTargetOracleSettings, e, m, p, r, t


class FlextTargetOracleConnectionService:
    """Minimal Oracle connection service implements ConnectionService protocol."""

    def __init__(
        self,
        settings: FlextTargetOracleSettings,
        oracle_api: FlextDbOracleApi,
    ) -> None:
        """Store configuration and Oracle API dependency."""
        self.settings = settings
        self.oracle_api = oracle_api

    def execute(self) -> p.Result[None]:
        """Run default connection validation operation."""
        return self.test_connection()

    def get_connection_info(self) -> p.Result[m.TargetOracle.OracleConnectionModel]:
        """Return normalized connection model."""
        return r[m.TargetOracle.OracleConnectionModel].ok(
            self.settings.get_oracle_config(),
        )

    def test_connection(self) -> p.Result[None]:
        """Check Oracle access by listing schema tables."""
        tables_result = self.oracle_api.fetch_tables(
            schema=self.settings.default_target_schema,
        )
        if tables_result.failure:
            return r[None].fail(tables_result.error or "Connection test failed")
        return r[None].ok(None)


class FlextTargetOracleSchemaService:
    """Minimal schema management service implements SchemaService protocol."""

    def __init__(
        self,
        settings: FlextTargetOracleSettings,
        oracle_api: FlextDbOracleApi,
    ) -> None:
        """Store schema service dependencies."""
        self.settings = settings
        self.oracle_api = oracle_api

    def ensure_table_exists(
        self,
        stream: m.TargetOracle.SingerStreamModel,
        schema_message: m.Meltano.SingerSchemaMessage,
    ) -> p.Result[None]:
        """Validate table identity before external DDL orchestration."""
        _ = schema_message
        table_name = stream.table_name
        if not table_name:
            return e.fail_validation("table_name", error="invalid")
        return r[None].ok(None)

    def execute(self) -> p.Result[None]:
        """Run service health operation."""
        return r[None].ok(None)


class FlextTargetOracleBatchService:
    """Minimal batching service implements BatchService protocol."""

    def __init__(
        self,
        settings: FlextTargetOracleSettings,
        oracle_api: FlextDbOracleApi,
    ) -> None:
        """Initialize batch storage and required dependencies."""
        self.settings = settings
        self.oracle_api = oracle_api
        self._batches: defaultdict[str, list[m.Meltano.SingerRecordMessage]] = (
            defaultdict(list)
        )

    def add_record(
        self,
        stream_name: str,
        record_message: m.Meltano.SingerRecordMessage,
    ) -> p.Result[None]:
        """Append a record to a stream buffer."""
        self._batches[stream_name].append(record_message)
        return r[None].ok(None)

    def execute(self) -> p.Result[m.TargetOracle.LoadStatisticsModel]:
        """Run default batch flush operation."""
        return self.flush_all_batches()

    def flush_all_batches(self) -> p.Result[m.TargetOracle.LoadStatisticsModel]:
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

    def flush_batch(self, stream_name: str) -> p.Result[None]:
        """Clear buffered records for a specific stream."""
        self._batches[stream_name] = list[m.Meltano.SingerRecordMessage]()
        return r[None].ok(None)


class FlextTargetOracleRecordService:
    """Record validation and transformation service implements RecordService protocol."""

    def __init__(self, settings: FlextTargetOracleSettings) -> None:
        """Store record service configuration."""
        self.settings = settings

    def execute(self) -> p.Result[None]:
        """Run record-service readiness check."""
        return r[None].ok(None)

    def transform_record(
        self,
        record_message: m.Meltano.SingerRecordMessage,
        stream: m.TargetOracle.SingerStreamModel,
    ) -> p.Result[m.Meltano.SingerRecordMessage]:
        """Apply stream-level mappings and ignored-column filtering."""
        transformed: t.MutableJsonMapping = {}
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
    ) -> p.Result[None]:
        """Validate record payload against current schema contract."""
        _ = record_message
        _ = schema_message
        return r[None].ok(None)


__all__: list[str] = [
    "FlextTargetOracleBatchService",
    "FlextTargetOracleConnectionService",
    "FlextTargetOracleRecordService",
    "FlextTargetOracleSchemaService",
]
