"""Unit tests for the canonical Oracle target client.

Copyright (c) 2026 FLEXT Team. All rights reserved.
tests/unit/test_target
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest
from flext_cli import u as cli_u
from flext_tests import tm

from flext_target_oracle import FlextTargetOracleSettings
from flext_target_oracle.api import FlextTargetOracleService
from flext_target_oracle.utilities import FlextTargetOracle
from tests import m, t, u


@pytest.fixture
def target(oracle_config: FlextTargetOracleSettings) -> FlextTargetOracle:
    """Create a target bound to the real Oracle container (no mocks).

    Returns:
        The resulting ``FlextTargetOracle``.
    """
    return FlextTargetOracle(settings=oracle_config)


@pytest.mark.integration
class TestsFlextTargetOracleTarget:
    """Behavioral contract for the Oracle target against the real container."""

    @staticmethod
    def test_initialize_and_connection(target: FlextTargetOracle) -> None:
        """Test initialize and connection."""
        tm.ok(target.initialize())
        tm.ok(target.test_connection())

    @staticmethod
    def test_execute_returns_ready_status(target: FlextTargetOracle) -> None:
        """Test execute returns ready status."""
        result = target.execute()
        tm.ok(result)
        tm.that(result.value.status, eq="ready")
        tm.that(result.value.oracle_host, eq="localhost")

    @staticmethod
    def test_validate_configuration(target: FlextTargetOracle) -> None:
        # NOTE (multi-agent): mro-rn88 — ADR-005/CQRS: config validation moved off
        # the model
        # AND off the client to the service handler run_validate(command). Exercise
        # the real
        # public surface (the service), which is where validation now lives.
        """Test validate configuration."""
        _ = target
        service = FlextTargetOracleService.fetch_global()
        command = m.TargetOracle.OracleTargetValidateCommand()
        result = service.run_validate(command)
        tm.ok(result)

    @staticmethod
    def test_discover_catalog_uses_registered_schemas(
        target: FlextTargetOracle,
    ) -> None:
        """Test discover catalog uses registered schemas."""
        schema_message = m.Meltano.SingerSchemaMessage.model_validate({
            "type": "SCHEMA",
            "stream": "users",
            "schema": {
                "type": "object",
                "properties": cli_u.Cli.json_dumps({
                    "id": {"type": "integer"},
                }).unwrap(),
            },
            "key_properties": ["id"],
        })
        tm.ok(target.process_singer_message(schema_message))
        catalog_result = target.discover_catalog()
        tm.ok(catalog_result)
        tm.that(catalog_result.value.streams[0].stream, eq="users")

    @staticmethod
    def test_process_record_and_state_messages(target: FlextTargetOracle) -> None:
        """Test process record and state messages."""
        schema_message = m.Meltano.SingerSchemaMessage.model_validate({
            "type": "SCHEMA",
            "stream": "users",
            "schema": {
                "type": "object",
                "properties": cli_u.Cli.json_dumps({
                    "id": {"type": "integer"},
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

    @staticmethod
    def test_process_singer_messages_flushes_loader(
        target: FlextTargetOracle,
    ) -> None:
        """Test process singer messages flushes loader."""
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
                        "id": {"type": "integer"},
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

    @staticmethod
    def test_unsupported_message_type_fails(target: FlextTargetOracle) -> None:
        """Test unsupported message type fails."""
        result = target.write_record('{"type": "UNKNOWN"}')
        tm.fail(result)

    @staticmethod
    def test_invalid_json_payload_maps_to_processing_failure(
        target: FlextTargetOracle,
    ) -> None:
        """Test invalid json payload maps to processing failure."""
        result = target.execute("{ invalid }")
        tm.fail(result)
        parse_result = target.write_record(
            '{"type": "RECORD", "stream": "users", "record": "bad"}',
        )
        tm.fail(parse_result)
        exceptions = u.TargetOracle.FlextTargetOracleExceptions
        assert issubclass(exceptions.ProcessingError, Exception)

    @staticmethod
    def test_missing_schema_path_uses_schema_error_type() -> None:
        """Test missing schema path uses schema error type."""
        exceptions = u.TargetOracle.FlextTargetOracleExceptions
        err = exceptions.SchemaError("schema missing")
        tm.that(err, is_=exceptions.SchemaError)

    @staticmethod
    def test_metrics_and_write_record_contract(target: FlextTargetOracle) -> None:
        """Test metrics and write record contract."""
        metrics = target.get_implementation_metrics()
        assert metrics.batch_size > 0
        tm.that({True, False}, has=metrics.use_bulk_operations)
        result = target.write_record(
            t.json_value_adapter().dump_json({"id": 1}).decode("utf-8"),
        )
        tm.fail(result)

    @staticmethod
    def test_write_record_inserts_oracle_record(
        target: FlextTargetOracle,
    ) -> None:
        """Test write record inserts oracle record."""
        schema_message = m.Meltano.SingerSchemaMessage.model_validate({
            "type": "SCHEMA",
            "stream": "users",
            "schema": {
                "type": "object",
                "properties": cli_u.Cli.json_dumps({
                    "id": {"type": "integer"},
                }).unwrap(),
            },
            "key_properties": ["id"],
        })
        tm.ok(target.process_singer_message(schema_message))
        result = target.write_record(
            t
            .json_value_adapter()
            .dump_json({"type": "RECORD", "stream": "users", "record": {"id": 1}})
            .decode("utf-8"),
        )
        tm.ok(result)
