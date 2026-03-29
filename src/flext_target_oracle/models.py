"""Models for Oracle target operations."""

from __future__ import annotations

from flext_core import r
from flext_db_oracle.models import FlextDbOracleModels
from flext_meltano import FlextMeltanoModels

from flext_target_oracle._models.commands import (
    FlextTargetOracleModelsCommands,
    load_target_settings,
)
from flext_target_oracle._models.config import FlextTargetOracleModelsConfig
from flext_target_oracle._models.results import FlextTargetOracleModelsResults
from flext_target_oracle._models.singer import FlextTargetOracleModelsSinger


class FlextTargetOracleModels(FlextMeltanoModels, FlextDbOracleModels):
    """Complete models for Oracle target operations extending FlextModels."""

    class TargetOracle(
        FlextTargetOracleModelsCommands,
        FlextTargetOracleModelsConfig,
        FlextTargetOracleModelsResults,
        FlextTargetOracleModelsSinger,
    ):
        """TargetOracle domain namespace composed from _models/ submodules."""

    @staticmethod
    def _load_target_settings(
        config_file: str | None,
    ) -> r[FlextTargetOracleModelsConfig.OracleSettingsProtocol]:
        """Load settings from JSON file or environment defaults."""
        return load_target_settings(config_file)


m = FlextTargetOracleModels

__all__ = ["FlextTargetOracleModels", "m"]
