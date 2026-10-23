"""End-to-end Singer flow checks for canonical target behavior.

Copyright (c) 2026 FLEXT Team. All rights reserved.
tests/e2e/test_singer
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from flext_cli import u as cli_u

from flext_target_oracle import FlextTargetOracle
from tests import m, tm

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
        self,
        oracle_config: FlextTargetOracleSettings,
    ) -> None:
        """Test complete singer flow."""
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
        tm.ok(target.run())
        tm.ok(
            target.process_singer_message(
                m.Meltano.SingerSchemaMessage.model_validate(schema),
            ),
        )
        tm.ok(
            target.process_singer_message(
                m.Meltano.SingerRecordMessage.model_validate(record),
            ),
        )
        tm.ok(
            target.process_singer_message(
                m.Meltano.SingerStateMessage.model_validate(state),
            ),
        )
        finalize_result = target.finalize()
        tm.ok(finalize_result)
        tm.that(target.schemas, has="orders")
        state_value = target.state_message.value
        tm.that(state_value, is_=dict)
        bookmarks_obj = tm.instance(state_value.get("bookmarks"), dict)
        orders_obj = tm.instance(bookmarks_obj.get("orders"), dict)
        tm.that(orders_obj.get("version"), eq=1)
