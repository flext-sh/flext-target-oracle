"""Base typings for Target Oracle module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano import m, t as meltano_t


class FlextTargetOracleTypesBase:
    """TargetOracle domain types namespace."""

    FLAT_CONTAINER_MAP_ADAPTER: m.TypeAdapter[meltano_t.ContainerValueMapping] = (
        m.TypeAdapter(meltano_t.ContainerValueMapping)
    )
    STR_MAP_ADAPTER: m.TypeAdapter[meltano_t.StrMapping] = m.TypeAdapter(
        meltano_t.StrMapping
    )
