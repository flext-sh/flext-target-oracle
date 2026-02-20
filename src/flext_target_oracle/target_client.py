"""Oracle Singer target client implementation."""

from __future__ import annotations

from flext_core import FlextLogger, FlextResult, FlextTypes as t
from pydantic import ValidationError

from .models import RecordMessageModel, SchemaMessageModel, StateMessageModel
from .settings import FlextTargetOracleSettings
from .target_loader import FlextTargetOracleLoader

logger = FlextLogger(__name__)


class FlextTargetOracle:
    """Singer target client that coordinates schema and record loading."""

    def __init__(self, config: FlextTargetOracleSettings) -> None:
        """Create target with validated settings and loader dependencies."""
        self.config = config
        self.loader = FlextTargetOracleLoader(config)
        self.schemas: dict[str, dict[str, t.GeneralValueType]] = {}
        self.state: dict[str, t.GeneralValueType] = {}

    def execute(
        self, payload: str | None = None
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Execute target readiness check."""
        _ = payload
        connection_result = self.loader.test_connection()
        if connection_result.is_failure:
            return FlextResult[dict[str, t.GeneralValueType]].fail(
                connection_result.error or "Connection test failed",
            )
        return FlextResult[dict[str, t.GeneralValueType]].ok(
            {
                "name": "flext-target-oracle",
                "status": "ready",
                "oracle_host": self.config.oracle_host,
                "oracle_service": self.config.oracle_service_name,
            },
        )

    def initialize(self) -> FlextResult[bool]:
        """Initialize target by validating connectivity."""
        return self.loader.test_connection()

    def validate_configuration(self) -> FlextResult[bool]:
        """Validate target configuration rules."""
        return self.config.validate_business_rules()

    def test_connection(self) -> FlextResult[bool]:
        """Test Oracle connectivity through loader."""
        return self.loader.test_connection()

    def discover_catalog(self) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Return Singer-style catalog for known schemas."""
        streams: list[dict[str, t.GeneralValueType]] = []
        for stream_name, schema in self.schemas.items():
            streams.append({
                "tap_stream_id": stream_name,
                "stream": stream_name,
                "schema": schema,
                "metadata": [
                    {
                        "breadcrumb": [],
                        "metadata": {
                            "inclusion": "available",
                            "table-name": self.config.get_table_name(stream_name),
                            "schema-name": self.config.default_target_schema,
                        },
                    }
                ],
            })
        return FlextResult[dict[str, t.GeneralValueType]].ok({"streams": streams})

    def process_singer_messages(
        self,
        messages: list[dict[str, t.GeneralValueType]],
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Process SCHEMA/RECORD/STATE Singer messages."""
        processed = 0
        for message in messages:
            result = self.process_singer_message(message)
            if result.is_failure:
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    result.error or "Message processing failed",
                )
            processed += 1

        finalize_result = self.loader.finalize_all_streams()
        if finalize_result.is_failure:
            return FlextResult[dict[str, t.GeneralValueType]].fail(
                finalize_result.error or "Finalize failed",
            )

        return FlextResult[dict[str, t.GeneralValueType]].ok(
            {
                "messages_processed": processed,
                "streams": list(self.schemas.keys()),
                "state": self.state,
            },
        )

    def process_singer_message(
        self,
        message: dict[str, t.GeneralValueType],
    ) -> FlextResult[None]:
        """Process a single Singer message."""
        message_type = message.get("type")
        if message_type == "SCHEMA":
            return self._handle_schema(message)
        if message_type == "RECORD":
            return self._handle_record(message)
        if message_type == "STATE":
            return self._handle_state(message)
        return FlextResult[None].fail(f"Unsupported message type: {message_type}")

    def finalize(self) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Flush remaining batches and return loader statistics."""
        return self.loader.finalize_all_streams()

    def get_implementation_metrics(self) -> dict[str, t.GeneralValueType]:
        """Return static target metrics."""
        return {
            "streams_configured": len(self.schemas),
            "batch_size": self.config.batch_size,
            "use_bulk_operations": self.config.use_bulk_operations,
        }

    def write_record(self, _record_data: str) -> FlextResult[None]:
        """Backwards-compatibility write_record stub."""
        return FlextResult[None].fail("write_record is not implemented")

    def _handle_schema(
        self, message: dict[str, t.GeneralValueType]
    ) -> FlextResult[None]:
        try:
            schema_message = SchemaMessageModel.model_validate(message)
        except ValidationError as exc:
            return FlextResult[None].fail(f"Invalid SCHEMA message: {exc}")

        stream_name = schema_message.stream
        schema = schema_message.schema
        key_properties = schema_message.key_properties or None

        ensure_result = self.loader.ensure_table_exists(
            stream_name, schema, key_properties
        )
        if ensure_result.is_failure:
            return FlextResult[None].fail(
                ensure_result.error or "Failed to ensure table",
            )
        self.schemas[stream_name] = schema
        return FlextResult[None].ok(None)

    def _handle_record(
        self, message: dict[str, t.GeneralValueType]
    ) -> FlextResult[None]:
        try:
            record_message = RecordMessageModel.model_validate(message)
        except ValidationError as exc:
            return FlextResult[None].fail(f"Invalid RECORD message: {exc}")

        stream_name = record_message.stream
        record = record_message.record
        load_result = self.loader.load_record(stream_name, record)
        if load_result.is_failure:
            return FlextResult[None].fail(load_result.error or "Failed to load record")
        return FlextResult[None].ok(None)

    def _handle_state(
        self, message: dict[str, t.GeneralValueType]
    ) -> FlextResult[None]:
        try:
            state_message = StateMessageModel.model_validate(message)
        except ValidationError as exc:
            return FlextResult[None].fail(f"Invalid STATE message: {exc}")

        for key, value in state_message.value.items():
            self.state[str(key)] = value
        logger.debug("State updated for Oracle target")
        return FlextResult[None].ok(None)


__all__ = ["FlextTargetOracle"]
