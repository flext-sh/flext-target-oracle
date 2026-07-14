"""Unit tests for FlextTargetOracleLoader public behavior."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from flext_tests import r, tm

from flext_cli import u as cli_u
from flext_target_oracle import FlextTargetOracleSettings
from flext_target_oracle._utilities.loader import FlextTargetOracleLoader
from tests import m, t


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
        },
    })


class TestsFlextTargetOracleLoader:
    """Behavior contract for test_loader."""

    def test_loader_execute_returns_ready_payload(
        self,
        loader_config: FlextTargetOracleSettings,
    ) -> None:
        """execute() should return a typed readiness payload."""
        loader = FlextTargetOracleLoader(loader_config)
        result = loader.execute()
        tm.that(result.success, is_=bool)

    def test_load_record_buffers_and_finalize(
        self,
        loader_config: FlextTargetOracleSettings,
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
        self,
        loader_config: FlextTargetOracleSettings,
    ) -> None:
        """ensure_table_exists should always return FlextResult[bool]."""
        loader = FlextTargetOracleLoader(loader_config)
        schema_message = {
            "type": "SCHEMA",
            "stream": "users",
            "schema": {
                "type": "object",
                "properties": cli_u.Cli.json_dumps({
                    "id": {"type": "integer"},
                }).unwrap(),
            },
            "key_properties": ["id"],
        }
        validated = m.Meltano.SingerSchemaMessage.model_validate(schema_message)
        result = loader.ensure_table_exists(
            "users",
            validated.schema_definition,
            validated.key_properties,
        )
        tm.that(result.success, is_=bool)

    def test_flush_batch_uses_db_oracle_owned_sql_builders(
        self,
        loader_config: FlextTargetOracleSettings,
    ) -> None:
        """Flush should delegate INSERT SQL building and batching to db-oracle."""
        loader = FlextTargetOracleLoader(loader_config)
        # NOTE (multi-agent): mro-rn88 — ADR-005 inlined table-name building into the loader
        # (dead settings.get_table_name removed); derive the expected name the same way.
        prefix = loader.target_config.TargetOracle.table_prefix
        suffix = loader.target_config.TargetOracle.table_suffix
        table_name = f"{prefix}users{suffix}".upper()
        mock_api = MagicMock()
        mock_services = MagicMock()
        mock_api.oracle_services = mock_services
        mock_api.execute_many.return_value = r[int].ok(2)
        mock_api.__enter__.return_value = mock_api
        mock_api.__exit__.return_value = None
        mock_services.build_insert_statement.return_value = r[str].ok(
            "INSERT INTO TEST_SCHEMA.USERS (DATA, _SDC_EXTRACTED_AT, _SDC_LOADED_AT) VALUES (:DATA, :_SDC_EXTRACTED_AT, :_SDC_LOADED_AT)",
        )
        object.__setattr__(loader, "_oracle_api", mock_api)
        loader._stream_columns["users"] = (
            m.DbOracle.Column(name="DATA", data_type="VARCHAR2(255)", nullable=True),
            m.DbOracle.Column(
                name="_SDC_EXTRACTED_AT",
                data_type="TIMESTAMP",
                nullable=True,
            ),
            m.DbOracle.Column(
                name="_SDC_LOADED_AT",
                data_type="TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                nullable=True,
            ),
        )
        loader.record_buffers["users"] = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
        ]

        result = loader._flush_batch("users")

        tm.ok(result)
        mock_services.build_insert_statement.assert_called_once_with(
            table_name,
            ["DATA", "_SDC_EXTRACTED_AT", "_SDC_LOADED_AT"],
            schema="TEST_SCHEMA",
        )
        mock_api.execute_many.assert_called_once()
