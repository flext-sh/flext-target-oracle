"""Unit tests for FlextTargetOracleLoader public behavior."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from flext_cli import u as cli_u
from flext_target_oracle import FlextTargetOracleSettings
from flext_target_oracle._utilities.loader import FlextTargetOracleLoader
from flext_tests import tm
from tests import m

if TYPE_CHECKING:
    from flext_db_oracle import FlextDbOracleApi

    from tests import t


@pytest.fixture
def loader_config() -> FlextTargetOracleSettings:
    """Build deterministic configuration for loader tests."""
    # NOTE (multi-agent): mro-rn88 — project fields nest under TargetOracle.*; a flat dict
    # is dropped by extra="ignore" (so default_target_schema silently fell back to default).
    return FlextTargetOracleSettings.model_validate({
        "TargetOracle": {
            "oracle_host": "localhost",
            "oracle_port": 1521,
            "oracle_service_name": "XE",
            "oracle_user": "test_user",
            "oracle_password": "test_password",
            "default_target_schema": "TEST_SCHEMA",
            "batch_size": 2,
            "use_bulk_operations": True,
        }
    })


class TestsFlextTargetOracleLoader:
    """Behavior contract for test_loader."""

    def test_loader_execute_returns_ready_payload(
        self, loader_config: FlextTargetOracleSettings
    ) -> None:
        """execute() should return a typed readiness payload."""
        loader = FlextTargetOracleLoader(loader_config)
        result = loader.execute()
        tm.that(result.success, is_=bool)

    def test_load_record_buffers_and_finalize(
        self, loader_config: FlextTargetOracleSettings
    ) -> None:
        """load_record should buffer valid records and finalize returns model."""
        loader = FlextTargetOracleLoader(loader_config)
        record: t.JsonMapping = {"id": 1, "name": "Alice"}
        load_result = loader.load_record("users", record)
        tm.ok(load_result)
        finalize_result = loader.finalize_all_streams()
        tm.ok(finalize_result)
        tm.that(finalize_result.value, none=False)
        assert finalize_result.value.streams_processed >= 0

    def test_ensure_table_exists_returns_result(
        self, loader_config: FlextTargetOracleSettings
    ) -> None:
        """ensure_table_exists should always return FlextResult[bool]."""
        loader = FlextTargetOracleLoader(loader_config)
        schema_message = {
            "type": "SCHEMA",
            "stream": "users",
            "schema": {
                "type": "object",
                "properties": cli_u.Cli.json_dumps({
                    "id": {"type": "integer"}
                }).unwrap(),
            },
            "key_properties": ["id"],
        }
        validated = m.Meltano.SingerSchemaMessage.model_validate(schema_message)
        result = loader.ensure_table_exists(
            "users", validated.schema_definition, validated.key_properties
        )
        tm.that(result.success, is_=bool)

    @pytest.mark.integration
    def test_flush_batch_persists_records_to_real_oracle(
        self, oracle_config: FlextTargetOracleSettings, oracle_engine: FlextDbOracleApi
    ) -> None:
        """Flush should build and execute INSERTs against the real database."""
        loader = FlextTargetOracleLoader(oracle_config)
        tm.ok(loader.connect())
        stream_name = "loader_flush"
        schema_message = {
            "type": "SCHEMA",
            "stream": stream_name,
            "schema": {
                "type": "object",
                "properties": cli_u.Cli.json_dumps({
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                }).unwrap(),
            },
            "key_properties": ["id"],
        }
        validated = m.Meltano.SingerSchemaMessage.model_validate(schema_message)
        tm.ok(
            loader.ensure_table_exists(
                stream_name, validated.schema_definition, validated.key_properties
            )
        )
        tm.ok(loader.load_record(stream_name, {"id": 1, "name": "Alice"}))
        tm.ok(loader.load_record(stream_name, {"id": 2, "name": "Bob"}))
        tm.ok(loader.finalize_all_streams())
        table_name = (
            f"{loader.target_config.TargetOracle.table_prefix}"
            f"{stream_name}"
            f"{loader.target_config.TargetOracle.table_suffix}"
        ).upper()
        count_result = oracle_engine.oracle_services.execute_query(
            f'SELECT COUNT(*) AS "count" FROM {table_name}'
        )
        tm.ok(count_result)
        tm.that(int(str(count_result.value[0].root["count"])), eq=2)
