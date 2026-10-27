# AUTO-GENERATED FILE — Regenerate with: make gen
"""Target Oracle type facade.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_target_oracle/typings
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_db_oracle import t
from flext_meltano import t as flext_meltano_t

from flext_target_oracle._typings import FlextTargetOracleTypesBase


class FlextTargetOracleTypes(flext_meltano_t, t):
    """Oracle target type facade."""

    class TargetOracle(FlextTargetOracleTypesBase):
        """Oracle target type namespace."""


t = FlextTargetOracleTypes
__all__: list[str] = ["FlextTargetOracleTypes", "t"]
