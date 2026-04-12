"""Utility helpers for Oracle Singer target integration."""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleUtilities
from flext_meltano import FlextMeltanoUtilities
from flext_target_oracle import (
    FlextTargetOracleUtilitiesBase,
    FlextTargetOracleUtilitiesObservability,
)


class FlextTargetOracleUtilities(FlextMeltanoUtilities, FlextDbOracleUtilities):
    """Focused utility namespace used by Oracle target modules."""

    class TargetOracle(
        FlextTargetOracleUtilitiesObservability, FlextTargetOracleUtilitiesBase
    ):
        """Oracle target utility namespace."""


u = FlextTargetOracleUtilities
__all__: list[str] = ["FlextTargetOracleUtilities", "u"]
