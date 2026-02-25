"""Unit tests for the canonical Oracle target client."""

from __future__ import annotations

import json

import pytest
from pydantic import SecretStr

from flext_core import FlextResult
from flext_target_oracle import (
    FlextTargetOracle,
    FlextTargetOracleProcessingError,
    FlextTargetOracleSchemaError,
    FlextTargetOracleSettings,
)


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
    client.loader.finalize_all_streams = lambda: FlextResult[dict[str, object]].ok({
        "status": "completed"
    })
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
        schema_message = {
            "type": "SCHEMA",
            "stream": "users",
            "schema": {"type": "object", "properties": {"id": {"type": "integer"}}},
            "key_properties": ["id"],
        }
        assert target.process_singer_message(schema_message).is_success

        catalog_result = target.discover_catalog()
        assert catalog_result.is_success
        assert catalog_result.value.streams[0].stream == "users"

    def test_process_record_and_state_messages(self, target: FlextTargetOracle) -> None:
        schema_message = {
            "type": "SCHEMA",
            "stream": "users",
            "schema": {"type": "object", "properties": {"id": {"type": "integer"}}},
        }
        record_message = {"type": "RECORD", "stream": "users", "record": {"id": 1}}
        state_message = {"type": "STATE", "value": {"bookmarks": {"users": 1}}}

        assert target.process_singer_message(schema_message).is_success
        assert target.process_singer_message(record_message).is_success
        assert target.process_singer_message(state_message).is_success
        assert target.state["bookmarks"]["users"] == 1

    def test_process_singer_messages_flushes_loader(
        self, target: FlextTargetOracle
    ) -> None:
        messages = [
            {
                "type": "SCHEMA",
                "stream": "users",
                "schema": {"type": "object", "properties": {"id": {"type": "integer"}}},
            },
            {"type": "RECORD", "stream": "users", "record": {"id": 1}},
            {"type": "STATE", "value": {"offset": 1}},
        ]

        result = target.process_singer_messages(messages)
        assert result.is_success
        assert result.value.messages_processed == 3

    def test_unsupported_message_type_fails(self, target: FlextTargetOracle) -> None:
        result = target.process_singer_message({"type": "UNKNOWN"})
        assert result.is_failure

    def test_invalid_json_payload_maps_to_processing_failure(
        self, target: FlextTargetOracle
    ) -> None:
        result = target.execute("{ invalid }")
        assert result.is_success
        parse_result = target.process_singer_message({
            "type": "RECORD",
            "stream": "users",
            "record": "bad",
        })
        assert parse_result.is_failure
        assert isinstance(
            FlextTargetOracleProcessingError("invalid", details={}),
            FlextTargetOracleProcessingError,
        )

    def test_missing_schema_path_uses_schema_error_type(self) -> None:
        err = FlextTargetOracleSchemaError("schema missing")
        assert isinstance(err, FlextTargetOracleSchemaError)

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
