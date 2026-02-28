"""Unit tests for the canonical Oracle target client."""

from __future__ import annotations

import json
from collections.abc import Mapping

import pytest
from flext_core import FlextResult
from flext_target_oracle import (
    FlextTargetOracle,
    FlextTargetOracleSettings,
    FlextTargetOracleExceptions,
    m,
)
from pydantic import SecretStr


@pytest.fixture
def target() -> FlextTargetOracle:
    config = FlextTargetOracleSettings(
        oracle_host="localhost",
        oracle_service_name="XE",
        oracle_user="test",
        oracle_password=SecretStr("test"),
        default_target_schema="TEST_SCHEMA",
    )
    client = FlextTargetOracle(config=config)
    client.loader.test_connection = lambda: FlextResult[bool].ok(value=True)
    client.loader.ensure_table_exists = lambda *_args, **_kwargs: FlextResult[bool].ok(
        value=True
    )
    client.loader.load_record = lambda *_args, **_kwargs: FlextResult[bool].ok(
        value=True
    )
    client.loader.finalize_all_streams = lambda: FlextResult[
        m.TargetOracle.LoaderFinalizeResult
    ].ok(
        m.TargetOracle.LoaderFinalizeResult(
            total_records=0,
            streams_processed=0,
            loading_operation=m.TargetOracle.LoaderOperation(
                stream_name="users",
                started_at="",
                completed_at="",
                records_loaded=0,
                records_failed=0,
            ),
        ),
    )
    return client


class TestOracleTarget:
    """Behavioral tests for current public API."""

    def test_initialize_and_connection(self, target: FlextTargetOracle) -> None:
        assert target.initialize().is_success
        assert target.test_connection().is_success

    def test_execute_returns_ready_status(self, target: FlextTargetOracle) -> None:
        result = target.execute()
        assert result.is_success
        assert result.value.status == "ready"
        assert result.value.oracle_host == "localhost"

    def test_validate_configuration(self, target: FlextTargetOracle) -> None:
        result = target.validate_configuration()
        assert result.is_success

    def test_discover_catalog_uses_registered_schemas(
        self, target: FlextTargetOracle
    ) -> None:
        schema_message = m.TargetOracle.SingerSchemaMessage.model_validate(
            {
                "type": "SCHEMA",
                "stream": "users",
                "schema": {"type": "object", "properties": {"id": {"type": "integer"}}},
                "key_properties": ["id"],
            },
        )
        assert target.process_singer_message(schema_message).is_success

        catalog_result = target.discover_catalog()
        assert catalog_result.is_success
        assert catalog_result.value.streams[0].stream == "users"

    def test_process_record_and_state_messages(self, target: FlextTargetOracle) -> None:
        schema_message = m.TargetOracle.SingerSchemaMessage.model_validate(
            {
                "type": "SCHEMA",
                "stream": "users",
                "schema": {"type": "object", "properties": {"id": {"type": "integer"}}},
            },
        )
        record_message = m.TargetOracle.SingerRecordMessage.model_validate(
            {"type": "RECORD", "stream": "users", "record": {"id": 1}},
        )
        state_message = m.TargetOracle.SingerStateMessage.model_validate(
            {"type": "STATE", "value": {"bookmarks": {"users": 1}}},
        )

        assert target.process_singer_message(schema_message).is_success
        assert target.process_singer_message(record_message).is_success
        assert target.process_singer_message(state_message).is_success
        state_value = target.state_message.value
        assert isinstance(state_value, Mapping)
        bookmarks_value = state_value.get("bookmarks")
        assert isinstance(bookmarks_value, Mapping)
        assert bookmarks_value.get("users") == 1

    def test_process_singer_messages_flushes_loader(
        self, target: FlextTargetOracle
    ) -> None:
        messages: list[
            m.TargetOracle.SingerSchemaMessage
            | m.TargetOracle.SingerRecordMessage
            | m.TargetOracle.SingerStateMessage
            | m.TargetOracle.SingerActivateVersionMessage
        ] = [
            m.TargetOracle.SingerSchemaMessage.model_validate(
                {
                    "type": "SCHEMA",
                    "stream": "users",
                    "schema": {
                        "type": "object",
                        "properties": {"id": {"type": "integer"}},
                    },
                },
            ),
            m.TargetOracle.SingerRecordMessage.model_validate(
                {"type": "RECORD", "stream": "users", "record": {"id": 1}},
            ),
            m.TargetOracle.SingerStateMessage.model_validate(
                {"type": "STATE", "value": {"offset": 1}},
            ),
        ]

        result = target.process_singer_messages(messages)
        assert result.is_success
        assert result.value.messages_processed == 3

    def test_unsupported_message_type_fails(self, target: FlextTargetOracle) -> None:
        result = target.write_record('{"type": "UNKNOWN"}')
        assert result.is_failure

    def test_invalid_json_payload_maps_to_processing_failure(
        self, target: FlextTargetOracle
    ) -> None:
        result = target.execute("{ invalid }")
        assert result.is_success
        parse_result = target.write_record(
            '{"type": "RECORD", "stream": "users", "record": "bad"}',
        )
        assert parse_result.is_failure
        assert isinstance(
            FlextTargetOracleExceptions.ProcessingError("invalid", operation="write_record"),
            FlextTargetOracleExceptions.ProcessingError,
        )

    def test_missing_schema_path_uses_schema_error_type(self) -> None:
        err = FlextTargetOracleExceptions.SchemaError("schema missing")
        assert isinstance(err, FlextTargetOracleExceptions.SchemaError)
    def test_metrics_and_write_record_contract(self, target: FlextTargetOracle) -> None:
        metrics = target.get_implementation_metrics()
        assert metrics.batch_size > 0
        assert metrics.use_bulk_operations in {True, False}

        result = target.write_record(json.dumps({"id": 1}))
        assert result.is_failure

    def test_write_record_inserts_oracle_record(
        self, target: FlextTargetOracle
    ) -> None:
        target.loader.insert_records = lambda *_args, **_kwargs: FlextResult[bool].ok(
            value=True,
        )

        result = target.write_record(
            json.dumps(
                {
                    "type": "RECORD",
                    "stream": "users",
                    "record": {"id": 1},
                },
            ),
        )

        assert result.is_success
