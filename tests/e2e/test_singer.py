"""End-to-end Singer flow checks for canonical target behavior."""

from __future__ import annotations

import json
from collections.abc import Mapping
from unittest.mock import Mock

import pytest
from flext_core import FlextResult
from flext_target_oracle import FlextTargetOracle, FlextTargetOracleSettings, m


@pytest.mark.e2e
class TestSingerWorkflowE2E:
    """Validate SCHEMA -> RECORD -> STATE happy path."""

    def _target(self) -> FlextTargetOracle:
        config = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_service_name="XE",
            oracle_user="test",
            oracle_password="test",
        )
        target = FlextTargetOracle(config=config)
        mock_oracle_api = Mock()
        mock_oracle_api.__enter__ = Mock(return_value=mock_oracle_api)
        mock_oracle_api.__exit__ = Mock(return_value=None)
        mock_oracle_api.get_tables.return_value = FlextResult[list[str]].ok([])
        mock_oracle_api.execute_sql.return_value = FlextResult[bool].ok(value=True)
        object.__setattr__(target.loader, "_oracle_api", mock_oracle_api)
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
        assert target.process_singer_message(
            m.TargetOracle.SingerStateMessage.model_validate(
                json.loads(json.dumps(state))
            ),
        ).is_success

        finalize_result = target.finalize()
        assert finalize_result.is_success
        assert "orders" in target.schemas
        state_value = target.state_message.value
        assert isinstance(state_value, Mapping)
        bookmarks_value = state_value.get("bookmarks")
        assert isinstance(bookmarks_value, Mapping)
        orders_value = bookmarks_value.get("orders")
        assert isinstance(orders_value, Mapping)
        assert orders_value.get("version") == 1
