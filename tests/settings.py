"""Runtime settings for flext-target-oracle tests."""

from __future__ import annotations

from flext_tests.settings import FlextTestsSettings

from flext_target_oracle import FlextTargetOracleSettings


class TestsFlextTargetOracleSettings(
    FlextTargetOracleSettings,
    FlextTestsSettings,
):
    """Target Oracle settings extended with the shared test namespace."""


__all__: list[str] = ["TestsFlextTargetOracleSettings"]
