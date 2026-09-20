"""Runtime settings for flext-target-oracle tests."""

from __future__ import annotations

from typing import ClassVar

from flext_tests import FlextTestsSettings

from flext_target_oracle import FlextTargetOracleSettings, m


class TestsFlextTargetOracleSettings(FlextTargetOracleSettings, FlextTestsSettings):
    """Target Oracle settings extended with the shared test namespace."""

    model_config: ClassVar[m.SettingsConfigDict]


__all__: list[str] = ["TestsFlextTargetOracleSettings"]
