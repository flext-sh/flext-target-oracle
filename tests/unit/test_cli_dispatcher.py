"""Tests for dispatcher integration in FlextTargetOracleCliService."""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from unittest.mock import patch

import pytest

pytest.importorskip(
    "flext_meltano",
    reason="Dispatcher pilot test requires flext-meltano optional dependency",
)
from flext_target_oracle import FlextTargetOracleCliService
from flext_target_oracle.constants import FlextTargetOracleConstants


@contextmanager
def _enable_dispatcher(enabled: bool) -> Generator[None]:
    """Patch the ENABLE_DISPATCHER flag at runtime."""
    with patch.object(
        FlextTargetOracleConstants.FeatureFlags,
        "ENABLE_DISPATCHER",
        enabled,
    ):
        yield


def test_cli_service_uses_dispatcher_when_flag_enabled() -> None:
    """CLI still executes command when dispatcher flag is enabled."""
    with _enable_dispatcher(True):
        service = FlextTargetOracleCliService()
        result = service.run_cli(["about"])
        assert not result.is_failure


def test_cli_service_falls_back_to_bus_when_flag_disabled() -> None:
    """CLI still executes command when dispatcher flag is disabled."""
    with _enable_dispatcher(False):
        service = FlextTargetOracleCliService()
        result = service.run_cli(["about"])
        assert not result.is_failure
