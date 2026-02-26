"""End-to-end Singer flow checks for canonical target behavior."""

from __future__ import annotations

import json
from collections.abc import Mapping

import pytest
from flext_core import FlextResult
from flext_target_oracle import FlextTargetOracle, FlextTargetOracleSettings, m
from pydantic import SecretStr


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
        target.loader.finalize_all_streams = lambda: FlextResult[
            m.TargetOracle.LoaderFinalizeResult
        ].ok(
            m.TargetOracle.LoaderFinalizeResult(
                total_records=0,
                streams_processed=0,
                loading_operation=m.TargetOracle.LoaderOperation(
                    stream_name="orders",
                    started_at="",
                    completed_at="",
                    records_loaded=0,
                    records_failed=0,
                ),
            )
        )
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
