"""Models for Oracle target operations."""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleModels
from flext_meltano import m as meltano_m

from flext_target_oracle import (
    FlextTargetOracleModelsCommands,
    FlextTargetOracleModelsResults,
    FlextTargetOracleModelsSettings,
    FlextTargetOracleModelsSinger,
)


class FlextTargetOracleModels(
    meltano_m,
    FlextDbOracleModels,
):
    """Complete models for Oracle target operations extending FlextModels."""

    class TargetOracle(
        FlextTargetOracleModelsCommands,
        FlextTargetOracleModelsSettings,
        FlextTargetOracleModelsResults,
        FlextTargetOracleModelsSinger,
    ):
        """Namespace of models for Oracle target."""


m = FlextTargetOracleModels

__all__: list[str] = ["FlextTargetOracleModels", "m"]
