# AUTO-GENERATED FILE — Regenerate with: make gen
"""Models package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_target_oracle._models.commands import FlextTargetOracleModelsCommands
    from flext_target_oracle._models.results import FlextTargetOracleModelsResults
    from flext_target_oracle._models.settings import FlextTargetOracleModelsSettings
    from flext_target_oracle._models.singer import FlextTargetOracleModelsSinger
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".commands": ("FlextTargetOracleModelsCommands",),
        ".results": ("FlextTargetOracleModelsResults",),
        ".settings": ("FlextTargetOracleModelsSettings",),
        ".singer": ("FlextTargetOracleModelsSinger",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
