"""Runtime settings for flext-target-oracle tests."""

from __future__ import annotations

from flext_target_oracle import FlextTargetOracleSettings
from flext_tests import FlextTestsSettings


class TestsFlextTargetOracleSettings(FlextTargetOracleSettings, FlextTestsSettings):
    """Target Oracle settings extended with the shared test namespace."""


__all__: list[str] = ["TestsFlextTargetOracleSettings"]
