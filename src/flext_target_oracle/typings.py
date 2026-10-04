"""Target Oracle type facade.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_target_oracle/typings
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleTypes
from flext_meltano import FlextMeltanoTypes

from flext_target_oracle._typings.base import FlextTargetOracleTypesBase


class FlextTargetOracleTypes(FlextMeltanoTypes, FlextDbOracleTypes):
    """Oracle target type facade."""

    class TargetOracle(FlextTargetOracleTypesBase):
        """Oracle target type namespace."""


t = FlextTargetOracleTypes

__all__: list[str] = ["FlextTargetOracleTypes", "t"]
