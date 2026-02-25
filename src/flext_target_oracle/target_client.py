"""Oracle Singer target client implementation."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime


from flext_core import FlextLogger, FlextResult
from pydantic import ValidationError

from .models import m
from .settings import FlextTargetOracleSettings
from .target_loader import FlextTargetOracleLoader

logger = FlextLogger(__name__)


class FlextTargetOracle:
    """Singer target client that coordinates schema and record loading."""

    def __init__(self, config: FlextTargetOracleSettings) -> None:
        """Create target with validated settings and loader dependencies."""
        self.config = config
        self.loader = FlextTargetOracleLoader(config)
        self.schemas: dict[str, m.TargetOracle.SingerSchemaMessage] = {}
        self.state_message: m.TargetOracle.SingerStateMessage = (
            m.TargetOracle.SingerStateMessage()
        )
        self._record_batches: dict[str, list[dict[str, object]]] = {}

    def execute(
        self, payload: str | None = None
    ) -> FlextResult[m.TargetOracle.ExecuteResult]:
        """Execute target readiness check."""
        _ = payload
        connection_result = self.loader.test_connection()
        if connection_result.is_failure:
            return FlextResult[m.TargetOracle.ExecuteResult].fail(
                connection_result.error or "Connection test failed",
            )
        return FlextResult[m.TargetOracle.ExecuteResult].ok(
            m.TargetOracle.ExecuteResult(
                name="flext-target-oracle",
                oracle_host=self.config.oracle_host,
                oracle_service=self.config.oracle_service_name,
            )
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

    def discover_catalog(self) -> FlextResult[m.Meltano.SingerCatalog]:
        """Return Singer-style catalog for known schemas."""
        catalog_entries = [
            m.Meltano.SingerCatalogEntry(
                tap_stream_id=stream_name,
                stream=stream_name,
                schema=schema_message.schema_definition,
                metadata=[
                    m.Meltano.SingerCatalogMetadata(
                        breadcrumb=[],
                        metadata={
                            "inclusion": "available",
                            "table-name": self.config.get_table_name(stream_name),
                            "schema-name": self.config.default_target_schema,
                        },
                    )
                ],
            )
            for stream_name, schema_message in self.schemas.items()
        ]
        return FlextResult[m.Meltano.SingerCatalog].ok(
            m.Meltano.SingerCatalog(streams=catalog_entries)
        )

    def process_singer_messages(
        self,
        messages: list[
            m.TargetOracle.SingerSchemaMessage
            | m.TargetOracle.SingerRecordMessage
            | m.TargetOracle.SingerStateMessage
            | m.TargetOracle.SingerActivateVersionMessage
        ],
    ) -> FlextResult[m.TargetOracle.ProcessingSummary]:
        """Process SCHEMA/RECORD/STATE Singer messages."""
        processed = 0
        for message in messages:
            result = self.process_singer_message(message)
            if result.is_failure:
                return FlextResult[m.TargetOracle.ProcessingSummary].fail(
                    result.error or "Message processing failed",
                )
            processed += 1

        for stream_name in list(self._record_batches):
            flush_result = self._flush_record_batch(stream_name)
            if flush_result.is_failure:
                return FlextResult[m.TargetOracle.ProcessingSummary].fail(
                    flush_result.error or "Failed to flush Oracle records",
                )

        finalize_result = self.loader.finalize_all_streams()
        if finalize_result.is_failure:
            return FlextResult[m.TargetOracle.ProcessingSummary].fail(
                finalize_result.error or "Finalize failed",
            )

        return FlextResult[m.TargetOracle.ProcessingSummary].ok(
            m.TargetOracle.ProcessingSummary(
                messages_processed=processed,
                streams=list(self.schemas.keys()),
                state=self.state_message,
            )
        )

    def process_singer_message(
        self,
        message: (
            m.TargetOracle.SingerSchemaMessage
            | m.TargetOracle.SingerRecordMessage
            | m.TargetOracle.SingerStateMessage
            | m.TargetOracle.SingerActivateVersionMessage
        ),
    ) -> FlextResult[None]:
        """Process a single Singer message."""
        match message:
            case m.TargetOracle.SingerSchemaMessage() as schema_message:
                return self._handle_schema(schema_message)
            case m.TargetOracle.SingerRecordMessage() as record_message:
                return self._handle_record(record_message)
            case m.TargetOracle.SingerStateMessage() as state_message:
                return self._handle_state(state_message)
            case m.TargetOracle.SingerActivateVersionMessage() as activate_message:
                return self._handle_activate_version(activate_message)
            case _:
                return FlextResult[None].fail("Unsupported Singer message type")

    def finalize(self) -> FlextResult[m.TargetOracle.LoaderFinalizeResult]:
        """Flush remaining batches and return loader statistics."""
        for stream_name in list(self._record_batches):
            flush_result = self._flush_record_batch(stream_name)
            if flush_result.is_failure:
                return FlextResult[m.TargetOracle.LoaderFinalizeResult].fail(
                    flush_result.error or "Failed to flush Oracle records",
                )
        return self.loader.finalize_all_streams()

    def get_implementation_metrics(self) -> m.TargetOracle.ImplementationMetrics:
        """Return static target metrics."""
        return m.TargetOracle.ImplementationMetrics(
            streams_configured=len(self.schemas),
            batch_size=self.config.batch_size,
            use_bulk_operations=self.config.use_bulk_operations,
        )

    def write_record(self, record_data: str) -> FlextResult[None]:
        """Write one Singer record payload to Oracle."""
        try:
            try:
                payload = m.TargetOracle.SingerRecordMessage.model_validate_json(
                    record_data
                )
            except ValidationError:
                raw_payload = json.loads(record_data)
                payload = m.TargetOracle.SingerRecordMessage.model_validate(raw_payload)

            stream_batch = self._record_batches.setdefault(payload.stream, [])
            stream_batch.append(dict(payload.record))

            should_flush = (
                not self.config.use_bulk_operations
                or len(stream_batch) >= self.config.batch_size
            )
            if should_flush:
                flush_result = self._flush_record_batch(payload.stream)
                if flush_result.is_failure:
                    return flush_result

            return FlextResult[None].ok(None)
        except (ValueError, TypeError, ValidationError, json.JSONDecodeError) as exc:
            return FlextResult[None].fail(f"Invalid record payload: {exc}")

    def _flush_record_batch(self, stream_name: str) -> FlextResult[None]:
        batch = self._record_batches.get(stream_name, [])
        if not batch:
            return FlextResult[None].ok(None)

        connection = None
        try:
            connection = self._connect_oracle()
            with connection.cursor() as cursor:
                insert_sql = self._build_insert_sql(stream_name)
                for record in batch:
                    extracted_at = record.get(
                        "_sdc_extracted_at", datetime.now(UTC).isoformat()
                    )
                    cursor.execute(
                        insert_sql,
                        {
                            "data": json.dumps(record),
                            "extracted_at": extracted_at,
                            "loaded_at": datetime.now(UTC).isoformat(),
                        },
                    )

            if not self.config.autocommit:
                connection.commit()
            self._record_batches[stream_name] = []
            return FlextResult[None].ok(None)
        except (ValueError, TypeError, RuntimeError, AttributeError, OSError) as exc:
            return FlextResult[None].fail(f"Failed to insert Oracle records: {exc}")
        finally:
            if connection is not None:
                connection.close()

    def _build_insert_sql(self, stream_name: str) -> str:
        table_name = self.config.get_table_name(stream_name)
        full_table_name = f"{self.config.default_target_schema}.{table_name}"
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_$.]*", full_table_name):
            msg = "Invalid Oracle table identifier"
            raise ValueError(msg)
        return (
            f"INSERT INTO {full_table_name} "
            "(DATA, _SDC_EXTRACTED_AT, _SDC_LOADED_AT) "
            "VALUES (:data, :extracted_at, :loaded_at)"
        )

    def _connect_oracle(self):
        import oracledb

        dsn = oracledb.makedsn(
            self.config.oracle_host,
            self.config.oracle_port,
            service_name=self.config.oracle_service_name,
        )
        return oracledb.connect(
            user=self.config.oracle_user,
            password=self.config.oracle_password.get_secret_value(),
            dsn=dsn,
        )

    def _handle_schema(
        self,
        schema_message: m.TargetOracle.SingerSchemaMessage,
    ) -> FlextResult[None]:
        stream_name = schema_message.stream
        schema = schema_message.schema_definition

        ensure_result = self.loader.ensure_table_exists(
            stream_name,
            schema,
            schema_message.key_properties,
        )
        if ensure_result.is_failure:
            return FlextResult[None].fail(
                ensure_result.error or "Failed to ensure table",
            )
        self.schemas[stream_name] = schema_message
        return FlextResult[None].ok(None)

    def _handle_record(
        self,
        record_message: m.TargetOracle.SingerRecordMessage,
    ) -> FlextResult[None]:
        load_result = self.loader.load_record(
            record_message.stream,
            record_message.record,
        )
        if load_result.is_failure:
            return FlextResult[None].fail(load_result.error or "Failed to load record")
        return FlextResult[None].ok(None)

    def _handle_state(
        self,
        state_message: m.TargetOracle.SingerStateMessage,
    ) -> FlextResult[None]:
        self.state_message = state_message
        logger.debug("State updated for Oracle target")
        return FlextResult[None].ok(None)

    def _handle_activate_version(
        self,
        activate_message: m.TargetOracle.SingerActivateVersionMessage,
    ) -> FlextResult[None]:
        logger.info(
            "ACTIVATE_VERSION received for Oracle target",
            stream=activate_message.stream,
            version=activate_message.version,
        )
        return FlextResult[None].ok(None)


__all__ = ["FlextTargetOracle"]
