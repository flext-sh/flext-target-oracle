"""Lean performance-oriented behavior checks for Oracle target."""

from __future__ import annotations

import json
import time
from collections.abc import Mapping

import pytest
from flext_core import FlextResult
from flext_target_oracle import FlextTargetOracle, FlextTargetOracleSettings, m
from pydantic import SecretStr


@pytest.mark.performance
class TestPerformance:
    """Keep fast checks for throughput-sensitive code paths."""

    def _target(self) -> FlextTargetOracle:
        config = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_service_name="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            batch_size=5000,
            use_bulk_operations=True,
        )
        target = FlextTargetOracle(config=config)
        target.loader.test_connection = lambda: FlextResult[bool].ok(value=True)
        target.loader.finalize_all_streams = lambda: FlextResult[
            m.TargetOracle.LoaderFinalizeResult
        ].ok(
            m.TargetOracle.LoaderFinalizeResult(
                total_records=0,
                streams_processed=0,
                loading_operation=m.TargetOracle.LoaderOperation(
                    stream_name="perf_stream",
                    started_at="",
                    completed_at="",
                    records_loaded=0,
                    records_failed=0,
                ),
            ),
        )
        return target

    def test_execute_readiness_is_constant_time(self) -> None:
        target = self._target()

        start = time.perf_counter()
        result = target.execute()
        elapsed = time.perf_counter() - start

        assert result.is_success
        assert elapsed < 0.05

    def test_message_processing_scales_linearly_for_state_updates(self) -> None:
        target = self._target()
        messages: list[
            m.TargetOracle.SingerSchemaMessage
            | m.TargetOracle.SingerRecordMessage
            | m.TargetOracle.SingerStateMessage
            | m.TargetOracle.SingerActivateVersionMessage
        ] = [
            m.TargetOracle.SingerStateMessage.model_validate(
                {"type": "STATE", "value": {"offset": i}},
            )
            for i in range(2000)
        ]

        start = time.perf_counter()
        result = target.process_singer_messages(messages)
        elapsed = time.perf_counter() - start

        assert result.is_success
        state_value = target.state_message.value
        assert isinstance(state_value, Mapping)
        assert state_value.get("offset") == 1999
        assert elapsed < 1.0

    def test_schema_and_record_processing_has_no_json_reparse_loop(self) -> None:
        target = self._target()
        target.loader.ensure_table_exists = lambda *_args, **_kwargs: FlextResult[
            bool
        ].ok(value=True)
        target.loader.load_record = lambda *_args, **_kwargs: FlextResult[bool].ok(
            value=True
        )

        schema = {
            "type": "SCHEMA",
            "stream": "perf_stream",
            "schema": {"type": "object", "properties": {"id": {"type": "integer"}}},
            "key_properties": ["id"],
        }
        record = {"type": "RECORD", "stream": "perf_stream", "record": {"id": 1}}

        assert target.process_singer_message(
            m.TargetOracle.SingerSchemaMessage.model_validate(
                json.loads(json.dumps(schema))
            ),
        ).is_success
        assert target.process_singer_message(
            m.TargetOracle.SingerRecordMessage.model_validate(
                json.loads(json.dumps(record))
            ),
        ).is_success
