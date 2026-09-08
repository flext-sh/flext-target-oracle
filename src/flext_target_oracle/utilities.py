"""Utility helpers for Oracle Singer target integration."""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleUtilities
from flext_meltano import u

from ._utilities.base import FlextTargetOracleUtilitiesBase
from ._utilities.client import FlextTargetOracle
from ._utilities.errors import FlextTargetOracleExceptions
from ._utilities.loader import FlextTargetOracleLoader
from ._utilities.observability import FlextTargetOracleUtilitiesObservability


class FlextTargetOracleUtilities(u, FlextDbOracleUtilities):
    """Focused utility namespace used by Oracle target modules."""

    class TargetOracle(
        FlextTargetOracleUtilitiesObservability, FlextTargetOracleUtilitiesBase
    ):
        """Oracle target utility namespace."""


u = FlextTargetOracleUtilities

__all__: list[str] = [
    "FlextTargetOracle",
    "FlextTargetOracleExceptions",
    "FlextTargetOracleLoader",
    "FlextTargetOracleUtilities",
    "u",
]
