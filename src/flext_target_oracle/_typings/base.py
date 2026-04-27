"""Base typings for Target Oracle module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano import m, t


class FlextTargetOracleTypesBase:
    """TargetOracle domain types namespace."""

    FLAT_CONTAINER_MAP_ADAPTER: m.TypeAdapter[t.JsonMapping] = m.TypeAdapter(
        t.JsonMapping
    )
    STR_MAP_ADAPTER: m.TypeAdapter[t.StrMapping] = m.TypeAdapter(t.StrMapping)


__all__: list[str] = ["FlextTargetOracleTypesBase"]
