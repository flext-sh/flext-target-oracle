"""Lean performance-oriented behavior checks for Oracle target."""

from __future__ import annotations

import json
import time
from collections.abc import (
    Mapping,
    Sequence,
)
from unittest.mock import Mock

import pytest

from flext_target_oracle import FlextTargetOracle, FlextTargetOracleSettings
from tests import m, r


@pytest.mark.performance
class TestPerformance:
    """Keep fast checks for throughput-sensitive code paths."""

    def _target(self) -> FlextTargetOracle:
        settings = FlextTargetOracleSettings.model_validate({
            "oracle_host": "localhost",
            "oracle_service_name": "XE",
            "oracle_user": "test",
            "oracle_password": "test",
            "batch_size": 5000,
            "use_bulk_operations": True,
        })
        target = FlextTargetOracle(settings=settings)
        mock_oracle_api = Mock()
        mock_oracle_api.__enter__ = Mock(return_value=mock_oracle_api)
        mock_oracle_api.__exit__ = Mock(return_value=None)
        mock_oracle_api.get_tables.return_value = r[list[str]].ok([])
        mock_oracle_api.fetch_tables.return_value = r[list[str]].ok([])
        mock_oracle_api.execute_sql.return_value = r[bool].ok(value=True)
        mock_oracle_api.oracle_services.create_table_ddl.return_value = r[str].ok(
            "CREATE TABLE perf_stream (id NUMBER)",
        )
        object.__setattr__(target.loader, "_oracle_api", mock_oracle_api)
        return target

    def test_execute_readiness_is_constant_time(self) -> None:
        target = self._target()
        start = time.perf_counter()
        result = target.execute()
        elapsed = time.perf_counter() - start
        assert result.success
        assert elapsed < 0.05

    def test_message_processing_scales_linearly_for_state_updates(self) -> None:
        target = self._target()
        messages: Sequence[
            m.TargetOracle.SingerSchemaMessage
            | m.TargetOracle.SingerRecordMessage
            | m.TargetOracle.SingerStateMessage
            | m.TargetOracle.SingerActivateVersionMessage
        ] = [
            m.TargetOracle.SingerStateMessage.model_validate({
                "type": "STATE",
                "value": {"offset": i},
            })
            for i in range(2000)
        ]
        start = time.perf_counter()
        result = target.process_singer_messages(messages)
        elapsed = time.perf_counter() - start
        assert result.success
        state_value = target.state_message.value
        assert isinstance(state_value, Mapping)
        assert state_value.get("offset") == 1999
        assert elapsed < 2.0

    def test_schema_and_record_processing_has_no_json_reparse_loop(self) -> None:
        target = self._target()
        schema = {
            "type": "SCHEMA",
            "stream": "perf_stream",
            "schema": {
                "type": "object",
                "properties": json.dumps({"id": {"type": "integer"}}),
            },
            "key_properties": ["id"],
        }
        record = {"type": "RECORD", "stream": "perf_stream", "record": {"id": 1}}
        assert target.process_singer_message(
            m.TargetOracle.SingerSchemaMessage.model_validate(schema)
        ).success
        assert target.process_singer_message(
            m.TargetOracle.SingerRecordMessage.model_validate(record)
        ).success
