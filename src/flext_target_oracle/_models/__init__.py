# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Oracle. Models package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_target_oracle._models.commands import FlextTargetOracleModelsCommands
    from flext_target_oracle._models.config import FlextTargetOracleConfigModels
    from flext_target_oracle._models.results import FlextTargetOracleModelsResults
    from flext_target_oracle._models.settings import FlextTargetOracleModelsSettings
    from flext_target_oracle._models.singer import FlextTargetOracleModelsSinger


__all__: tuple[str, ...] = (
    "FlextTargetOracleConfigModels",
    "FlextTargetOracleModelsCommands",
    "FlextTargetOracleModelsResults",
    "FlextTargetOracleModelsSettings",
    "FlextTargetOracleModelsSinger",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".commands": ("FlextTargetOracleModelsCommands",),
            ".config": ("FlextTargetOracleConfigModels",),
            ".results": ("FlextTargetOracleModelsResults",),
            ".settings": ("FlextTargetOracleModelsSettings",),
            ".singer": ("FlextTargetOracleModelsSinger",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
