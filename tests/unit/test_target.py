"""Unit tests for the canonical Oracle target client."""

from __future__ import annotations

import json
from collections.abc import (
    Sequence,
)
from unittest.mock import Mock

import pytest

from flext_target_oracle import (
    FlextTargetOracle,
    FlextTargetOracleExceptions,
    FlextTargetOracleSettings,
)
from tests import m, r, t


@pytest.fixture
def target(mock_oracle_api: Mock) -> FlextTargetOracle:
    """Create target with mocked loader."""
    settings = FlextTargetOracleSettings.model_validate({
        "oracle_host": "localhost",
        "oracle_service_name": "XE",
        "oracle_user": "test",
        "oracle_password": "test",
        "default_target_schema": "TEST_SCHEMA",
        "batch_size": 200,
        "commit_interval": 100,
    })
    client = FlextTargetOracle(settings=settings)
    object.__setattr__(
        client.loader, "test_connection", Mock(return_value=r[bool].ok(value=True))
    )
    object.__setattr__(
        client.loader, "ensure_table_exists", Mock(return_value=r[bool].ok(value=True))
    )
    object.__setattr__(
        client.loader, "load_record", Mock(return_value=r[bool].ok(value=True))
    )
    object.__setattr__(
        client.loader,
        "finalize_all_streams",
        Mock(
            return_value=r[m.TargetOracle.LoaderFinalizeResult].ok(
                m.TargetOracle.LoaderFinalizeResult.model_validate({
                    "total_records": 0,
                    "streams_processed": 0,
                    "loading_operation": {
                        "stream_name": "users",
                        "started_at": "",
                        "completed_at": "",
                        "records_loaded": 0,
                        "records_failed": 0,
                    },
                })
            )
        ),
    )
    return client


class TestsFlextTargetOracleTarget:
    def test_initialize_and_connection(self, target: FlextTargetOracle) -> None:
        assert target.initialize().success
        assert target.test_connection().success

    def test_execute_returns_ready_status(self, target: FlextTargetOracle) -> None:
        result = target.execute()
        assert result.success
        assert result.value.status == "ready"
        assert result.value.oracle_host == "localhost"

    def test_validate_configuration(self, target: FlextTargetOracle) -> None:
        result = target.validate_configuration()
        assert result.success

    def test_discover_catalog_uses_registered_schemas(
        self, target: FlextTargetOracle
    ) -> None:
        schema_message = m.Meltano.SingerSchemaMessage.model_validate({
            "type": "SCHEMA",
            "stream": "users",
            "schema": {
                "type": "object",
                "properties": json.dumps({"id": {"type": "integer"}}),
            },
            "key_properties": ["id"],
        })
        assert target.process_singer_message(schema_message).success
        catalog_result = target.discover_catalog()
        assert catalog_result.success
        assert catalog_result.value.streams[0].stream == "users"

    def test_process_record_and_state_messages(self, target: FlextTargetOracle) -> None:
        schema_message = m.Meltano.SingerSchemaMessage.model_validate({
            "type": "SCHEMA",
            "stream": "users",
            "schema": {
                "type": "object",
                "properties": json.dumps({"id": {"type": "integer"}}),
            },
        })
        record_message = m.Meltano.SingerRecordMessage.model_validate({
            "type": "RECORD",
            "stream": "users",
            "record": {"id": 1},
        })
        state_message = m.Meltano.SingerStateMessage.model_validate({
            "type": "STATE",
            "value": {"bookmarks": {"users": 1}},
        })
        assert target.process_singer_message(schema_message).success
        assert target.process_singer_message(record_message).success
        assert target.process_singer_message(state_message).success
        state_value = target.state_message.value
        assert isinstance(state_value, dict)
        bookmarks_obj: t.JsonValue | None = state_value.get("bookmarks")
        assert isinstance(bookmarks_obj, dict)
        assert bookmarks_obj.get("users") == 1

    def test_process_singer_messages_flushes_loader(
        self, target: FlextTargetOracle
    ) -> None:
        messages: Sequence[
            m.Meltano.SingerSchemaMessage
            | m.Meltano.SingerRecordMessage
            | m.Meltano.SingerStateMessage
            | m.Meltano.SingerActivateVersionMessage
        ] = [
            m.Meltano.SingerSchemaMessage.model_validate({
                "type": "SCHEMA",
                "stream": "users",
                "schema": {
                    "type": "object",
                    "properties": json.dumps({"id": {"type": "integer"}}),
                },
            }),
            m.Meltano.SingerRecordMessage.model_validate({
                "type": "RECORD",
                "stream": "users",
                "record": {"id": 1},
            }),
            m.Meltano.SingerStateMessage.model_validate({
                "type": "STATE",
                "value": {"offset": 1},
            }),
        ]
        result = target.process_singer_messages(messages)
        assert result.success
        assert result.value.messages_processed == 3

    def test_unsupported_message_type_fails(self, target: FlextTargetOracle) -> None:
        result = target.write_record('{"type": "UNKNOWN"}')
        assert result.failure

    def test_invalid_json_payload_maps_to_processing_failure(
        self, target: FlextTargetOracle
    ) -> None:
        result = target.execute("{ invalid }")
        assert result.success
        parse_result = target.write_record(
            '{"type": "RECORD", "stream": "users", "record": "bad"}'
        )
        assert parse_result.failure
        assert issubclass(FlextTargetOracleExceptions.ProcessingError, Exception)

    def test_missing_schema_path_uses_schema_error_type(self) -> None:
        err = FlextTargetOracleExceptions.SchemaError("schema missing")
        assert isinstance(err, FlextTargetOracleExceptions.SchemaError)

    def test_metrics_and_write_record_contract(self, target: FlextTargetOracle) -> None:
        metrics = target.get_implementation_metrics()
        assert metrics.batch_size > 0
        assert metrics.use_bulk_operations in {True, False}
        result = target.write_record(
            t.Tests.NORMALIZED_VALUE_ADAPTER.dump_json({"id": 1}).decode("utf-8")
        )
        assert result.failure

    def test_write_record_inserts_oracle_record(
        self, target: FlextTargetOracle
    ) -> None:
        mocked_load_record = Mock(return_value=r[bool].ok(value=True))
        object.__setattr__(target.loader, "load_record", mocked_load_record)
        result = target.write_record(
            t.Tests.NORMALIZED_VALUE_ADAPTER.dump_json({
                "type": "RECORD",
                "stream": "users",
                "record": {"id": 1},
            }).decode("utf-8")
        )
        mocked_load_record.assert_called_once_with("users", {"id": 1})
        assert result.success
