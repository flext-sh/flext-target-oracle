"""Models for Oracle target operations."""

from __future__ import annotations

from flext_db_oracle import m as _db_oracle_m
from flext_meltano import m

from ._models.commands import FlextTargetOracleModelsCommands
from ._models.results import FlextTargetOracleModelsResults
from ._models.settings import FlextTargetOracleModelsSettings
from ._models.singer import FlextTargetOracleModelsSinger


class FlextTargetOracleModels(m, _db_oracle_m):
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
