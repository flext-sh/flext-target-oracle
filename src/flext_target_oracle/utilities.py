"""Utility helpers for Oracle Singer target integration."""

from __future__ import annotations
from flext_target_oracle._utilities.client import FlextTargetOracle

from flext_db_oracle import FlextDbOracleUtilities
from flext_meltano import u
from flext_target_oracle._utilities.base import FlextTargetOracleUtilitiesBase
from flext_target_oracle._utilities.observability import (
    FlextTargetOracleUtilitiesObservability,
)


class FlextTargetOracleUtilities(u, FlextDbOracleUtilities):
    """Focused utility namespace used by Oracle target modules."""

    class TargetOracle(
        FlextTargetOracleUtilitiesObservability, FlextTargetOracleUtilitiesBase
    ):
        """Oracle target utility namespace."""


u = FlextTargetOracleUtilities

__all__: list[str] = ["FlextTargetOracle", "FlextTargetOracleUtilities", "u"]
