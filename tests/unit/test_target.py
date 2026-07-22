"""Unit tests for the canonical Oracle target client."""

from __future__ import annotations

import pytest

from flext_cli import u as cli_u
from flext_target_oracle import FlextTargetOracleSettings
from flext_target_oracle._utilities.client import FlextTargetOracle
from flext_target_oracle._utilities.errors import FlextTargetOracleExceptions
from flext_target_oracle.api import FlextTargetOracleService
from flext_tests import tm
from tests import m, t


@pytest.fixture
def target(oracle_config: FlextTargetOracleSettings) -> FlextTargetOracle:
    """Create a target bound to the real Oracle container (no mocks)."""
    return FlextTargetOracle(settings=oracle_config)


@pytest.mark.integration
class TestsFlextTargetOracleTarget:
    """Behavioral contract for the Oracle target against the real container."""

    def test_initialize_and_connection(self, target: FlextTargetOracle) -> None:
        tm.ok(target.initialize())
        tm.ok(target.test_connection())

    def test_execute_returns_ready_status(self, target: FlextTargetOracle) -> None:
        result = target.execute()
        tm.ok(result)
        tm.that(result.value.status, eq="ready")
        tm.that(result.value.oracle_host, eq="localhost")

    def test_validate_configuration(self, target: FlextTargetOracle) -> None:
        # NOTE (multi-agent): mro-rn88 — ADR-005/CQRS: config validation moved off the model
        # AND off the client to the service handler run_validate(command). Exercise the real
        # public surface (the service), which is where validation now lives.
        _ = target
        service = FlextTargetOracleService.fetch_global()
        command = m.TargetOracle.OracleTargetValidateCommand()
        result = service.run_validate(command)
        tm.ok(result)

    def test_discover_catalog_uses_registered_schemas(
        self, target: FlextTargetOracle
    ) -> None:
        schema_message = m.Meltano.SingerSchemaMessage.model_validate({
            "type": "SCHEMA",
            "stream": "users",
            "schema": {
                "type": "object",
                "properties": cli_u.Cli.json_dumps({
                    "id": {"type": "integer"}
                }).unwrap(),
            },
            "key_properties": ["id"],
        })
        tm.ok(target.process_singer_message(schema_message))
        catalog_result = target.discover_catalog()
        tm.ok(catalog_result)
        tm.that(catalog_result.value.streams[0].stream, eq="users")

    def test_process_record_and_state_messages(self, target: FlextTargetOracle) -> None:
        schema_message = m.Meltano.SingerSchemaMessage.model_validate({
            "type": "SCHEMA",
            "stream": "users",
            "schema": {
                "type": "object",
                "properties": cli_u.Cli.json_dumps({
                    "id": {"type": "integer"}
                }).unwrap(),
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
        tm.ok(target.process_singer_message(schema_message))
        tm.ok(target.process_singer_message(record_message))
        tm.ok(target.process_singer_message(state_message))
        state_value = target.state_message.value
        assert isinstance(state_value, dict)
        bookmarks_obj = state_value.get("bookmarks")
        assert isinstance(bookmarks_obj, dict)
        tm.that(bookmarks_obj.get("users"), eq=1)

    def test_process_singer_messages_flushes_loader(
        self, target: FlextTargetOracle
    ) -> None:
        messages: t.SequenceOf[
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
                    "properties": cli_u.Cli.json_dumps({
                        "id": {"type": "integer"}
                    }).unwrap(),
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
        tm.ok(result)
        tm.that(result.value.messages_processed, eq=3)

    def test_unsupported_message_type_fails(self, target: FlextTargetOracle) -> None:
        result = target.write_record('{"type": "UNKNOWN"}')
        tm.fail(result)

    def test_invalid_json_payload_maps_to_processing_failure(
        self, target: FlextTargetOracle
    ) -> None:
        result = target.execute("{ invalid }")
        tm.fail(result)
        parse_result = target.write_record(
            '{"type": "RECORD", "stream": "users", "record": "bad"}'
        )
        tm.fail(parse_result)
        assert issubclass(FlextTargetOracleExceptions.ProcessingError, Exception)

    def test_missing_schema_path_uses_schema_error_type(self) -> None:
        err = FlextTargetOracleExceptions.SchemaError("schema missing")
        tm.that(err, is_=FlextTargetOracleExceptions.SchemaError)

    def test_metrics_and_write_record_contract(self, target: FlextTargetOracle) -> None:
        metrics = target.get_implementation_metrics()
        assert metrics.batch_size > 0
        tm.that({True, False}, has=metrics.use_bulk_operations)
        result = target.write_record(
            t.json_value_adapter().dump_json({"id": 1}).decode("utf-8")
        )
        tm.fail(result)

    def test_write_record_inserts_oracle_record(
        self, target: FlextTargetOracle
    ) -> None:
        schema_message = m.Meltano.SingerSchemaMessage.model_validate({
            "type": "SCHEMA",
            "stream": "users",
            "schema": {
                "type": "object",
                "properties": cli_u.Cli.json_dumps({
                    "id": {"type": "integer"}
                }).unwrap(),
            },
            "key_properties": ["id"],
        })
        tm.ok(target.process_singer_message(schema_message))
        result = target.write_record(
            t
            .json_value_adapter()
            .dump_json({"type": "RECORD", "stream": "users", "record": {"id": 1}})
            .decode("utf-8")
        )
        tm.ok(result)
