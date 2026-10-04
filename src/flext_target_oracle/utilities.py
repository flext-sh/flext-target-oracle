"""Utility helpers for Oracle Singer target integration.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_target_oracle/utilities
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleUtilities
from flext_meltano import FlextMeltanoUtilities

from flext_target_oracle._utilities.base import FlextTargetOracleUtilitiesBase
from flext_target_oracle._utilities.client import FlextTargetOracle
from flext_target_oracle._utilities.errors import FlextTargetOracleUtilitiesErrors
from flext_target_oracle._utilities.loader import FlextTargetOracleLoader
from flext_target_oracle._utilities.observability import (
    FlextTargetOracleUtilitiesObservability,
)


class FlextTargetOracleUtilities(FlextMeltanoUtilities, FlextDbOracleUtilities):
    """Focused utility namespace used by Oracle target modules."""

    class TargetOracle(
        FlextTargetOracleUtilitiesObservability,
        FlextTargetOracleUtilitiesBase,
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
