"""FLEXT Target Oracle Types — MRO composition of parent type namespaces.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pydantic import TypeAdapter

from flext_db_oracle import FlextDbOracleTypes
from flext_meltano import FlextMeltanoTypes


class FlextTargetOracleTypes(FlextMeltanoTypes, FlextDbOracleTypes):
    """MRO facade composing Meltano + DbOracle type namespaces."""

    FLAT_CONTAINER_MAP_ADAPTER: TypeAdapter[FlextMeltanoTypes.ContainerValueMapping] = (
        TypeAdapter(FlextMeltanoTypes.ContainerValueMapping)
    )
    STR_MAP_ADAPTER: TypeAdapter[FlextMeltanoTypes.StrMapping] = TypeAdapter(
        FlextMeltanoTypes.StrMapping
    )


t = FlextTargetOracleTypes
__all__ = ["FlextTargetOracleTypes", "t"]
