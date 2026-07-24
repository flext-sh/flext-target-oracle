"""Lean performance-oriented behavior checks for Oracle target."""

from __future__ import annotations

import time
from collections.abc import Mapping
from unittest.mock import Mock

import pytest
from flext_tests import tm

from flext_target_oracle import FlextTargetOracleSettings
from flext_target_oracle._utilities.client import FlextTargetOracle
from tests import m, p, r, t, u


@pytest.mark.performance
class TestsFlextTargetOraclePerformance:
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
        empty_tables: list[str] = []
        mock_oracle_api.get_tables.return_value = r[list[str]].ok(empty_tables)
        mock_oracle_api.fetch_tables.return_value = r[list[str]].ok(empty_tables)
        mock_oracle_api.execute_sql.return_value = r[bool].ok(value=True)
        type_mapping = m.DbOracle.TypeMapping.model_validate({
            "mapping": {"id": "NUMBER"}
        })
        mock_oracle_api.oracle_services.map_singer_schema.return_value = r[
            m.DbOracle.TypeMapping
        ].ok(type_mapping)
        mock_oracle_api.oracle_services.create_table_ddl.return_value = r[str].ok(
            "CREATE TABLE perf_stream (id NUMBER)"
        )
        mock_oracle_api.oracle_services.build_insert_statement.return_value = r[str].ok(
            "INSERT INTO perf_stream (id) VALUES (:id)"
        )
        mock_oracle_api.execute_statement.return_value = r[int].ok(1)
        mock_oracle_api.execute_many.return_value = r[int].ok(1)
        object.__setattr__(target.loader, "_oracle_api", mock_oracle_api)
        return target

    def test_execute_readiness_is_constant_time(self) -> None:
        target = self._target()
        start = time.perf_counter()
        result = target.execute()
        elapsed = time.perf_counter() - start
        tm.ok(result)
        assert elapsed < 0.05

    def test_message_processing_scales_linearly_for_state_updates(self) -> None:
        target = self._target()
        messages: t.SequenceOf[
            m.Meltano.SingerSchemaMessage
            | p.Meltano.SingerRecordMessage
            | p.Meltano.SingerStateMessage
            | p.Meltano.SingerActivateVersionMessage
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

    def test_schema_and_record_processing_has_no_json_reparse_loop(self) -> None:
        target = self._target()
        schema = {
            "type": "SCHEMA",
            "stream": "perf_stream",
            "schema": {
                "type": "object",
                "properties": u.Cli.json_dumps({"id": {"type": "integer"}}).unwrap(),
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
