"""End-to-end Singer flow checks for canonical target behavior."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from flext_cli import u as cli_u
from flext_target_oracle._utilities.client import FlextTargetOracle
from flext_tests import tm
from tests import m

if TYPE_CHECKING:
    from flext_target_oracle import FlextTargetOracleSettings


@pytest.mark.e2e
@pytest.mark.integration
class TestsFlextTargetOracleSinger:
    """Validate SCHEMA -> RECORD -> STATE happy path against real Oracle."""

    @staticmethod
    def _target(oracle_config: FlextTargetOracleSettings) -> FlextTargetOracle:
        return FlextTargetOracle(settings=oracle_config)

    def test_complete_singer_flow(
        self, oracle_config: FlextTargetOracleSettings
    ) -> None:
        target = self._target(oracle_config)
        schema = {
            "type": "SCHEMA",
            "stream": "orders",
            "schema": {
                "type": "object",
                "properties": cli_u.Cli.json_dumps({
                    "id": {"type": "integer"},
                    "amount": {"type": "number"},
                }).unwrap(),
            },
            "key_properties": ["id"],
        }
        record = {
            "type": "RECORD",
            "stream": "orders",
            "record": {"id": 1, "amount": 10.5},
        }
        state = {"type": "STATE", "value": {"bookmarks": {"orders": {"version": 1}}}}
        tm.ok(target.execute())
        tm.ok(
            target.process_singer_message(
                m.Meltano.SingerSchemaMessage.model_validate(schema)
            )
        )
        tm.ok(
            target.process_singer_message(
                m.Meltano.SingerRecordMessage.model_validate(record)
            )
        )
        tm.ok(
            target.process_singer_message(
                m.Meltano.SingerStateMessage.model_validate(state)
            )
        )
        finalize_result = target.finalize()
        tm.ok(finalize_result)
        tm.that(target.schemas, has="orders")
        state_value = target.state_message.value
        assert isinstance(state_value, dict)
        bookmarks_obj = state_value.get("bookmarks")
        assert isinstance(bookmarks_obj, dict)
        orders_obj = bookmarks_obj.get("orders")
        assert isinstance(orders_obj, dict)
        tm.that(orders_obj.get("version"), eq=1)
