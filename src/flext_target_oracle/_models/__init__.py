# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Oracle. Models package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .commands import (
        FlextTargetOracleModelsCommands as FlextTargetOracleModelsCommands,
    )
    from .results import (
        FlextTargetOracleModelsResults as FlextTargetOracleModelsResults,
    )
    from .settings import (
        FlextTargetOracleModelsSettings as FlextTargetOracleModelsSettings,
    )
    from .singer import FlextTargetOracleModelsSinger as FlextTargetOracleModelsSinger

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    ".commands": ("FlextTargetOracleModelsCommands",),
    ".results": ("FlextTargetOracleModelsResults",),
    ".settings": ("FlextTargetOracleModelsSettings",),
    ".singer": ("FlextTargetOracleModelsSinger",),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextTargetOracleModelsCommands",
    "FlextTargetOracleModelsResults",
    "FlextTargetOracleModelsSettings",
    "FlextTargetOracleModelsSinger",
)

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
