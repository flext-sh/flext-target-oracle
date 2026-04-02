"""Utility helpers for Oracle Singer target integration."""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleUtilities
from flext_meltano import FlextMeltanoUtilities


class FlextTargetOracleUtilities(FlextMeltanoUtilities, FlextDbOracleUtilities):
    """Focused utility namespace used by Oracle target modules."""

    class TargetOracle:
        """Oracle target utility namespace."""


u = FlextTargetOracleUtilities
__all__ = ["FlextTargetOracleUtilities", "u"]
