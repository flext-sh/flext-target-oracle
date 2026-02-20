"""End-to-end Singer flow checks for canonical target behavior."""

from __future__ import annotations

import json

import pytest
from pydantic import SecretStr

from flext_core import FlextResult
from flext_target_oracle import FlextTargetOracle, FlextTargetOracleSettings


@pytest.mark.e2e
class TestSingerWorkflowE2E:
    """Validate SCHEMA -> RECORD -> STATE happy path."""

    def _target(self) -> FlextTargetOracle:
        config = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_service_name="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
        )
        target = FlextTargetOracle(config=config)
        target.loader.test_connection = lambda: FlextResult[bool].ok(value=True)
        target.loader.ensure_table_exists = lambda *_args, **_kwargs: FlextResult[
            bool
        ].ok(value=True)
        target.loader.load_record = lambda *_args, **_kwargs: FlextResult[bool].ok(
            value=True
        )
        target.loader.finalize_all_streams = lambda: FlextResult[dict[str, object]].ok({
            "status": "completed"
        })
        return target

    def test_complete_singer_flow(self) -> None:
        target = self._target()

        schema = {
            "type": "SCHEMA",
            "stream": "orders",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "amount": {"type": "number"},
                },
            },
            "key_properties": ["id"],
        }
        record = {
            "type": "RECORD",
            "stream": "orders",
            "record": {"id": 1, "amount": 10.5},
        }
        state = {"type": "STATE", "value": {"bookmarks": {"orders": {"version": 1}}}}

        assert target.execute().is_success
        assert target.process_singer_message(json.loads(json.dumps(schema))).is_success
        assert target.process_singer_message(json.loads(json.dumps(record))).is_success
        assert target.process_singer_message(json.loads(json.dumps(state))).is_success

        finalize_result = target.finalize()
        assert finalize_result.is_success
        assert "orders" in target.schemas
        assert target.state["bookmarks"]["orders"]["version"] == 1
