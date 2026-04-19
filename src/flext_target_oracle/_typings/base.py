"""Base typings for Target Oracle module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano import FlextMeltanoTypes, m


class FlextTargetOracleTypesBase:
    """TargetOracle domain types namespace."""

    FLAT_CONTAINER_MAP_ADAPTER: m.TypeAdapter[
        FlextMeltanoTypes.ContainerValueMapping
    ] = m.TypeAdapter(FlextMeltanoTypes.ContainerValueMapping)
    STR_MAP_ADAPTER: m.TypeAdapter[FlextMeltanoTypes.StrMapping] = m.TypeAdapter(
        FlextMeltanoTypes.StrMapping
    )
