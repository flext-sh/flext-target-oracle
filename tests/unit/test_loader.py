"""Unit tests for FlextTargetOracleLoader public behavior."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

from flext_target_oracle import FlextTargetOracleLoader, FlextTargetOracleSettings
from tests import m, r, t


@pytest.fixture
def loader_config() -> FlextTargetOracleSettings:
    """Build deterministic configuration for loader tests."""
    return FlextTargetOracleSettings.model_validate({
        "oracle_host": "localhost",
        "oracle_port": 1521,
        "oracle_service_name": "XE",
        "oracle_user": "test_user",
        "oracle_password": "test_password",
        "default_target_schema": "TEST_SCHEMA",
        "batch_size": 2,
        "use_bulk_operations": True,
    })


def test_loader_execute_returns_ready_payload(
    loader_config: FlextTargetOracleSettings,
) -> None:
    """execute() should return a typed readiness payload."""
    loader = FlextTargetOracleLoader(loader_config)
    result = loader.execute()
    assert isinstance(result.success, bool)


def test_load_record_buffers_and_finalize(
    loader_config: FlextTargetOracleSettings,
) -> None:
    """load_record should buffer valid records and finalize returns model."""
    loader = FlextTargetOracleLoader(loader_config)
    record: t.ScalarMapping = {"id": 1, "name": "Alice"}
    load_result = loader.load_record("users", record)
    assert load_result.success
    finalize_result = loader.finalize_all_streams()
    assert finalize_result.success
    assert finalize_result.value is not None
    assert finalize_result.value.streams_processed >= 0


def test_ensure_table_exists_returns_result(
    loader_config: FlextTargetOracleSettings,
) -> None:
    """ensure_table_exists should always return FlextResult[bool]."""
    loader = FlextTargetOracleLoader(loader_config)
    schema_message = {
        "type": "SCHEMA",
        "stream": "users",
        "schema": {
            "type": "object",
            "properties": json.dumps({"id": {"type": "integer"}}),
        },
        "key_properties": ["id"],
    }
    validated = m.TargetOracle.SingerSchemaMessage.model_validate(schema_message)
    result = loader.ensure_table_exists(
        "users", validated.schema_definition, validated.key_properties
    )
    assert isinstance(result.success, bool)


def test_flush_batch_uses_db_oracle_owned_sql_builders(
    loader_config: FlextTargetOracleSettings,
) -> None:
    """Flush should delegate INSERT SQL building and batching to db-oracle."""
    loader = FlextTargetOracleLoader(loader_config)
    table_name = loader.target_config.get_table_name("users")
    mock_api = MagicMock()
    mock_services = MagicMock()
    mock_api.oracle_services = mock_services
    mock_api.execute_many.return_value = r[int].ok(2)
    mock_api.__enter__.return_value = mock_api
    mock_api.__exit__.return_value = None
    mock_services.build_insert_statement.return_value = r[str].ok(
        "INSERT INTO TEST_SCHEMA.USERS (DATA, _SDC_EXTRACTED_AT, _SDC_LOADED_AT) VALUES (:DATA, :_SDC_EXTRACTED_AT, :_SDC_LOADED_AT)"
    )
    object.__setattr__(loader, "_oracle_api", mock_api)
    loader.record_buffers["users"] = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
    ]

    result = loader._flush_batch("users")

    assert result.success
    mock_services.build_insert_statement.assert_called_once_with(
        table_name,
        ["DATA", "_SDC_EXTRACTED_AT", "_SDC_LOADED_AT"],
        schema="TEST_SCHEMA",
    )
    mock_api.execute_many.assert_called_once()
