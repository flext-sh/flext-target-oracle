# AUTO-GENERATED FILE — Regenerate with: make gen
"""Utility helpers for Oracle Singer target integration.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_target_oracle/utilities
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_db_oracle import u
from flext_meltano import u as flext_meltano_u

from flext_target_oracle._utilities import (
    FlextTargetOracle,
    FlextTargetOracleUtilitiesBase,
    FlextTargetOracleUtilitiesBootstrap,
    FlextTargetOracleUtilitiesErrors,
    FlextTargetOracleUtilitiesObservability,
)


class FlextTargetOracleUtilities(flext_meltano_u, u):
    """Focused utility namespace used by Oracle target modules."""

    class TargetOracle(
        FlextTargetOracleUtilitiesBootstrap,
        FlextTargetOracleUtilitiesObservability,
        FlextTargetOracleUtilitiesBase,
        FlextTargetOracle,
        FlextTargetOracleUtilitiesErrors,
    ):
        """Oracle target utility namespace."""


u = FlextTargetOracleUtilities
__all__: list[str] = ["FlextTargetOracle", "FlextTargetOracleUtilities", "u"]
