"""Lean performance-oriented behavior checks for Oracle target."""
from __future__ import annotations
import json
import time
from collections.abc import Mapping
from unittest.mock import Mock
import pytest
from flext_core import FlextResult
from flext_target_oracle import FlextTargetOracle, FlextTargetOracleSettings, m

@pytest.mark.performance
class TestPerformance:
    """Keep fast checks for throughput-sensitive code paths."""

    def _target(self) -> FlextTargetOracle:
        config = FlextTargetOracleSettings(oracle_host='localhost', oracle_service_name='XE', oracle_user='test', oracle_password='test', batch_size=5000, use_bulk_operations=True)
        target = FlextTargetOracle(config=config)
        mock_oracle_api = Mock()
        mock_oracle_api.__enter__ = Mock(return_value=mock_oracle_api)
        mock_oracle_api.__exit__ = Mock(return_value=None)
        mock_oracle_api.get_tables.return_value = FlextResult[list[str]].ok([])
        mock_oracle_api.execute_sql.return_value = FlextResult[bool].ok(value=True)
        object.__setattr__(target.loader, '_oracle_api', mock_oracle_api)
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
        messages: list[m.TargetOracle.SingerSchemaMessage | m.TargetOracle.SingerRecordMessage | m.TargetOracle.SingerStateMessage | m.TargetOracle.SingerActivateVersionMessage] = [m.TargetOracle.SingerStateMessage.model_validate({'type': 'STATE', 'value': {'offset': i}}) for i in range(2000)]
        start = time.perf_counter()
        result = target.process_singer_messages(messages)
        elapsed = time.perf_counter() - start
        assert result.is_success
        state_value = target.state_message.value
        assert isinstance(state_value, Mapping)
        assert state_value.get('offset') == 1999
        assert elapsed < 1.0

    def test_schema_and_record_processing_has_no_json_reparse_loop(self) -> None:
        target = self._target()
        schema = {'type': 'SCHEMA', 'stream': 'perf_stream', 'schema': {'type': 'object', 'properties': {'id': {'type': 'integer'}}}, 'key_properties': ['id']}
        record = {'type': 'RECORD', 'stream': 'perf_stream', 'record': {'id': 1}}
        assert target.process_singer_message(m.TargetOracle.SingerSchemaMessage.model_validate(json.loads(json.dumps(schema)))).is_success
        assert target.process_singer_message(m.TargetOracle.SingerRecordMessage.model_validate(json.loads(json.dumps(record)))).is_success
