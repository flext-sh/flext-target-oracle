"""FLEXT Target Oracle Types — MRO composition of parent type namespaces.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleTypes
from flext_meltano import FlextMeltanoTypes
from flext_target_oracle._typings.base import FlextTargetOracleTypesBase


class FlextTargetOracleTypes(FlextMeltanoTypes, FlextDbOracleTypes):
    """MRO facade composing Meltano + DbOracle type namespaces."""

    class TargetOracle(FlextTargetOracleTypesBase):
        """TargetOracle types namespace."""


t = FlextTargetOracleTypes

__all__ = ["FlextTargetOracleTypes", "t"]
