"""Base typings for Target Oracle module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pydantic import TypeAdapter

from flext_meltano import FlextMeltanoTypes


class FlextTargetOracleTypesBase:
    """TargetOracle domain types namespace."""

    FLAT_CONTAINER_MAP_ADAPTER: TypeAdapter[FlextMeltanoTypes.ContainerValueMapping] = (
        TypeAdapter(FlextMeltanoTypes.ContainerValueMapping)
    )
    STR_MAP_ADAPTER: TypeAdapter[FlextMeltanoTypes.StrMapping] = TypeAdapter(
        FlextMeltanoTypes.StrMapping
    )
