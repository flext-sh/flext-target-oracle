"""Tests for dispatcher integration in FlextTargetOracleCliService."""

from __future__ import annotations

from contextlib import contextmanager
from unittest.mock import patch

import pytest

pytest.importorskip(
    "flext_meltano",
    reason="Dispatcher pilot test requires flext-meltano optional dependency",
)
from flext_target_oracle import FlextTargetOracleCliService, OracleTargetCommandFactory
from flext_target_oracle.constants import FlextTargetOracleConstants


@contextmanager
def _enable_dispatcher(enabled: bool) -> None:
    """Patch the ENABLE_DISPATCHER flag at runtime."""
    with patch.object(
        FlextTargetOracleConstants.FeatureFlags,
        "ENABLE_DISPATCHER",
        enabled,
    ):
        yield


def test_cli_service_uses_dispatcher_when_flag_enabled() -> None:
    """Test that CLI service uses dispatcher when flag is enabled."""
    with _enable_dispatcher(True):
        service = FlextTargetOracleCliService()
        assert service._dispatcher is not None
        command = OracleTargetCommandFactory.create_validate_command()
        result = service._dispatch(command)
        assert not result.is_failure


def test_cli_service_falls_back_to_bus_when_flag_disabled() -> None:
    """Test that CLI service falls back to bus when flag is disabled."""
    with _enable_dispatcher(False):
        service = FlextTargetOracleCliService()
        assert service._dispatcher is None
        command = OracleTargetCommandFactory.create_validate_command()
        result = service._dispatch(command)
        assert not result.is_failure
