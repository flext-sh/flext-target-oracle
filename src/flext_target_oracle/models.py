"""Models for Oracle target operations."""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleModels
from flext_meltano import FlextMeltanoModels
from flext_target_oracle import (
    FlextTargetOracleModelsCommands,
    FlextTargetOracleModelsConfig,
    FlextTargetOracleModelsResults,
    FlextTargetOracleModelsSinger,
)


class FlextTargetOracleModels(FlextMeltanoModels, FlextDbOracleModels):
    """Complete models for Oracle target operations extending FlextModels."""

    class TargetOracle(
        FlextTargetOracleModelsCommands,
        FlextTargetOracleModelsConfig,
        FlextTargetOracleModelsResults,
        FlextTargetOracleModelsSinger,
    ):
        """TargetOracle domain namespace composed from _models/ submodules."""


m = FlextTargetOracleModels

__all__ = ["FlextTargetOracleModels", "m"]
