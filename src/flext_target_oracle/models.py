"""Models for Oracle target operations."""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleModels
from flext_meltano import FlextMeltanoModels

from ._models.commands import FlextTargetOracleModelsCommands
from ._models.results import FlextTargetOracleModelsResults
from ._models.settings import FlextTargetOracleModelsSettings
from ._models.singer import FlextTargetOracleModelsSinger


class FlextTargetOracleModels(FlextMeltanoModels, FlextDbOracleModels):
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
