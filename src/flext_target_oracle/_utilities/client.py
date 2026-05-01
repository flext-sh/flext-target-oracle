"""Oracle Singer target client implementation."""

from __future__ import annotations

from collections.abc import (
    MutableMapping,
)
from typing import ClassVar, assert_never

from flext_meltano import u
from flext_target_oracle import (
    FlextTargetOracleLoader,
    FlextTargetOracleSettings,
    c,
    m,
    p,
    r,
    t,
)


class FlextTargetOracle:
    """Singer target client that coordinates schema and record loading."""

    logger: ClassVar[p.Logger] = u.fetch_logger(__name__)

    def __init__(self, settings: FlextTargetOracleSettings) -> None:
        """Create target with validated settings and loader dependencies."""
        self.settings = settings
        self.loader = FlextTargetOracleLoader(settings)
        self.schemas: MutableMapping[str, m.Meltano.SingerSchemaMessage] = {}
        self.state_message: m.Meltano.SingerStateMessage = m.Meltano.SingerStateMessage(
            type="STATE", value={}
        )

    def discover_catalog(self) -> p.Result[m.Meltano.SingerCatalog]:
        """Return Singer-style catalog for known schemas."""
        catalog_entries: list[m.Meltano.SingerCatalogEntry] = []
        for stream_name, schema_message in self.schemas.items():
            entry_result = u.Meltano.build_catalog_entry(
                stream_name=stream_name,
                schema=schema_message.schema_definition,
                key_properties=schema_message.key_properties,
            )
            if entry_result.failure or entry_result.value is None:
                return r[m.Meltano.SingerCatalog].fail(
                    entry_result.error
                    or f"Failed to build Singer catalog entry for {stream_name}",
                )
            catalog_entries.append(
                entry_result.value.model_copy(
                    update={
                        "metadata": [
                            m.Meltano.SingerCatalogMetadata(
                                breadcrumb=[],
                                metadata={
                                    "inclusion": "available",
                                    "table-name": self.settings.get_table_name(
                                        stream_name
                                    ),
                                    "schema-name": self.settings.default_target_schema,
                                },
                            )
                        ]
                    }
                )
            )
        return r[m.Meltano.SingerCatalog].ok(
            m.Meltano.SingerCatalog(type="CATALOG", streams=catalog_entries),
        )

    def execute(
        self, payload: str | None = None
    ) -> p.Result[m.TargetOracle.ExecuteResult]:
        """Execute target readiness check."""
        _ = payload
        connection_result = self.loader.test_connection()
        if connection_result.failure:
            return r[m.TargetOracle.ExecuteResult].fail(
                connection_result.error or "Connection test failed",
            )
        return r[m.TargetOracle.ExecuteResult].ok(
            m.TargetOracle.ExecuteResult(
                name="flext-target-oracle",
                status="ready",
                oracle_host=self.settings.oracle_host,
                oracle_service=self.settings.oracle_service_name,
            ),
        )

    def finalize(self) -> p.Result[m.TargetOracle.LoaderFinalizeResult]:
        """Flush remaining batches and return loader statistics."""
        return self.loader.finalize_all_streams()

    def get_implementation_metrics(self) -> m.TargetOracle.ImplementationMetrics:
        """Return static target metrics."""
        return m.TargetOracle.ImplementationMetrics(
            streams_configured=len(self.schemas),
            batch_size=self.settings.batch_size,
            use_bulk_operations=self.settings.use_bulk_operations,
        )

    def initialize(self) -> p.Result[bool]:
        """Initialize target by validating connectivity."""
        return self.loader.test_connection()

    def process_singer_message(
        self,
        message: m.Meltano.SingerSchemaMessage
        | m.Meltano.SingerRecordMessage
        | m.Meltano.SingerStateMessage
        | m.Meltano.SingerActivateVersionMessage,
    ) -> p.Result[bool]:
        """Process a single Singer message."""
        match message:
            case m.Meltano.SingerSchemaMessage() as schema_message:
                return self._handle_schema(schema_message)
            case m.Meltano.SingerRecordMessage() as record_message:
                return self._handle_record(record_message)
            case m.Meltano.SingerStateMessage() as state_message:
                return self._handle_state(state_message)
            case m.Meltano.SingerActivateVersionMessage() as activate_message:
                return self._handle_activate_version(activate_message)
        assert_never(message)

    def process_singer_messages(
        self,
        messages: t.SequenceOf[
            m.Meltano.SingerSchemaMessage
            | m.Meltano.SingerRecordMessage
            | m.Meltano.SingerStateMessage
            | m.Meltano.SingerActivateVersionMessage
        ],
    ) -> p.Result[m.TargetOracle.ProcessingSummary]:
        """Process SCHEMA/RECORD/STATE Singer messages."""
        processed = 0
        for message in messages:
            result = self.process_singer_message(message)
            if result.failure:
                return r[m.TargetOracle.ProcessingSummary].fail(
                    result.error or "Message processing failed",
                )
            processed += 1
        finalize_result = self.loader.finalize_all_streams()
        if finalize_result.failure:
            return r[m.TargetOracle.ProcessingSummary].fail(
                finalize_result.error or "Finalize failed",
            )
        return r[m.TargetOracle.ProcessingSummary].ok(
            m.TargetOracle.ProcessingSummary(
                messages_processed=processed,
                streams=list(self.schemas.keys()),
                state=self.state_message,
            ),
        )

    def test_connection(self) -> p.Result[bool]:
        """Test Oracle connectivity through loader."""
        return self.loader.test_connection()

    def validate_configuration(self) -> p.Result[bool]:
        """Validate target configuration rules."""
        return self.settings.validate_business_rules()

    def write_record(self, record_data: str) -> p.Result[bool]:
        """Write one Singer record payload to Oracle."""
        try:
            payload = m.Meltano.SingerRecordMessage.model_validate_json(
                record_data,
            )
            return self.loader.load_record(payload.stream, payload.record)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            return r[bool].fail(f"Invalid record payload: {exc}")

    def _handle_activate_version(
        self,
        activate_message: m.Meltano.SingerActivateVersionMessage,
    ) -> p.Result[bool]:
        self.logger.info(
            "ACTIVATE_VERSION received for Oracle target",
            stream=activate_message.stream,
            version=activate_message.version,
        )
        return r[bool].ok(True)

    def _handle_record(
        self,
        record_message: m.Meltano.SingerRecordMessage,
    ) -> p.Result[bool]:
        load_result = self.loader.load_record(
            record_message.stream,
            record_message.record,
        )
        if load_result.failure:
            return r[bool].fail(load_result.error or "Failed to load record")
        return r[bool].ok(True)

    def _handle_schema(
        self,
        schema_message: m.Meltano.SingerSchemaMessage,
    ) -> p.Result[bool]:
        stream_name = schema_message.stream
        schema = schema_message.schema_definition
        ensure_result = self.loader.ensure_table_exists(
            stream_name,
            schema,
            schema_message.key_properties,
        )
        if ensure_result.failure:
            return r[bool].fail(ensure_result.error or "Failed to ensure table")
        self.schemas[stream_name] = schema_message
        return r[bool].ok(True)

    def _handle_state(
        self,
        state_message: m.Meltano.SingerStateMessage,
    ) -> p.Result[bool]:
        self.state_message = state_message
        self.logger.debug("State updated for Oracle target")
        return r[bool].ok(True)


__all__: list[str] = ["FlextTargetOracle"]
