"""Base typings for Target Oracle module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano import t, u


class FlextTargetOracleTypesBase:
    """TargetOracle domain types namespace."""

    FLAT_CONTAINER_MAP_ADAPTER: u.type_adapter[t.JsonMapping] = u.json_mapping_adapter()
    STR_MAP_ADAPTER: u.type_adapter[t.StrMapping] = u.str_mapping_adapter()


__all__: list[str] = ["FlextTargetOracleTypesBase"]
