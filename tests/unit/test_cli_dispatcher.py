"""Tests for dispatcher integration in FlextTargetOracleCliService."""

from __future__ import annotations

import os
from contextlib import contextmanager

import pytest

pytest.importorskip(
    "flext_meltano",
    reason="Dispatcher pilot test requires flext-meltano optional dependency",
)
from flext_target_oracle import FlextTargetOracleCliService, OracleTargetCommandFactory


@contextmanager
def _flag(value: str) -> None:
    original = os.environ.get("FLEXT_TARGET_ORACLE_ENABLE_DISPATCHER")
    os.environ["FLEXT_TARGET_ORACLE_ENABLE_DISPATCHER"] = value
    try:
        yield
    finally:
        if original is None:
            os.environ.pop("FLEXT_TARGET_ORACLE_ENABLE_DISPATCHER", None)
        else:
            os.environ["FLEXT_TARGET_ORACLE_ENABLE_DISPATCHER"] = original


def test_cli_service_uses_dispatcher_when_flag_enabled() -> None:
    """Test that CLI service uses dispatcher when flag is enabled."""
    with _flag("1"):
        service = FlextTargetOracleCliService()
        assert service._dispatcher is not None
        command = OracleTargetCommandFactory.create_validate_command()
        result = service._dispatch(command)
        assert not result.is_failure


def test_cli_service_falls_back_to_bus_when_flag_disabled() -> None:
    """Test that CLI service falls back to bus when flag is disabled."""
    with _flag("0"):
        service = FlextTargetOracleCliService()
        assert service._dispatcher is None
        command = OracleTargetCommandFactory.create_validate_command()
        result = service._dispatch(command)
        assert not result.is_failure
