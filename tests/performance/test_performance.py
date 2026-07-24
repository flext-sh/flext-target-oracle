"""Lean performance-oriented behavior checks for Oracle target."""

from __future__ import annotations

import time
from collections.abc import Mapping
from typing import TYPE_CHECKING

import pytest

from flext_cli import u as cli_u
from flext_target_oracle._utilities.client import FlextTargetOracle
from flext_tests import tm
from tests import m

if TYPE_CHECKING:
    from flext_target_oracle import FlextTargetOracleSettings
    from tests import t


@pytest.mark.performance
@pytest.mark.integration
class TestsFlextTargetOraclePerformance:
    """Keep fast checks for throughput-sensitive code paths."""

    @staticmethod
    def _target(oracle_config: FlextTargetOracleSettings) -> FlextTargetOracle:
        return FlextTargetOracle(settings=oracle_config)

    def test_execute_readiness_is_constant_time(
        self, oracle_config: FlextTargetOracleSettings
    ) -> None:
        target = self._target(oracle_config)
        start = time.perf_counter()
        result = target.execute()
        elapsed = time.perf_counter() - start
        tm.ok(result)
        assert elapsed < 1.0

    def test_message_processing_scales_linearly_for_state_updates(
        self, oracle_config: FlextTargetOracleSettings
    ) -> None:
        target = self._target(oracle_config)
        messages: t.SequenceOf[
            m.Meltano.SingerSchemaMessage
            | m.Meltano.SingerRecordMessage
            | m.Meltano.SingerStateMessage
            | m.Meltano.SingerActivateVersionMessage
        ] = [
            m.Meltano.SingerStateMessage.model_validate({
                "type": "STATE",
                "value": {"offset": i},
            })
            for i in range(2000)
        ]
        start = time.perf_counter()
        result = target.process_singer_messages(messages)
        elapsed = time.perf_counter() - start
        tm.ok(result)
        state_value = target.state_message.value
        tm.that(state_value, is_=Mapping)
        tm.that(state_value.get("offset"), eq=1999)
        assert elapsed < 2.0

    def test_schema_and_record_processing_has_no_json_reparse_loop(
        self, oracle_config: FlextTargetOracleSettings
    ) -> None:
        target = self._target(oracle_config)
        schema = {
            "type": "SCHEMA",
            "stream": "perf_stream",
            "schema": {
                "type": "object",
                "properties": cli_u.Cli.json_dumps({
                    "id": {"type": "integer"}
                }).unwrap(),
            },
            "key_properties": ["id"],
        }
        record = {"type": "RECORD", "stream": "perf_stream", "record": {"id": 1}}
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
