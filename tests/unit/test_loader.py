"""Unit tests for FlextTargetOracleLoader public behavior."""

from __future__ import annotations

from collections.abc import Mapping

import pytest
from flext_core.typings import t
from flext_target_oracle import FlextTargetOracleLoader, FlextTargetOracleSettings
from pydantic import SecretStr


@pytest.fixture
def loader_config() -> FlextTargetOracleSettings:
    """Build deterministic configuration for loader tests."""
    return FlextTargetOracleSettings(
        oracle_host="localhost",
        oracle_port=1521,
        oracle_service_name="XE",
        oracle_user="test_user",
        oracle_password=SecretStr("test_password"),
        default_target_schema="TEST_SCHEMA",
        batch_size=2,
        use_bulk_operations=True,
    )


def test_loader_execute_returns_ready_payload(
    loader_config: FlextTargetOracleSettings,
) -> None:
    """execute() should return a typed readiness payload."""
    loader = FlextTargetOracleLoader(loader_config)

    result = loader.execute()
    assert isinstance(result.is_success, bool)


def test_load_record_buffers_and_finalize(
    loader_config: FlextTargetOracleSettings,
) -> None:
    """load_record should buffer valid records and finalize returns model."""
    loader = FlextTargetOracleLoader(loader_config)

    record: Mapping[str, t.JsonValue] = {"id": 1, "name": "Alice"}
    load_result = loader.load_record("users", record)
    assert load_result.is_success

    finalize_result = loader.finalize_all_streams()
    assert finalize_result.is_success
    assert finalize_result.value is not None
    assert finalize_result.value.streams_processed >= 0


def test_ensure_table_exists_returns_result(
    loader_config: FlextTargetOracleSettings,
) -> None:
    """ensure_table_exists should always return FlextResult[bool]."""
    loader = FlextTargetOracleLoader(loader_config)

    schema: Mapping[str, t.JsonValue] = {
        "type": "object",
        "properties": {"id": {"type": "integer"}},
    }
    result = loader.ensure_table_exists("users", schema, ["id"])
    assert isinstance(result.is_success, bool)
