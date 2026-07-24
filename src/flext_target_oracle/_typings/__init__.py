# AUTO-GENERATED FILE — Regenerate with: make gen
"""Typings package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_target_oracle._typings.base import (
        FlextTargetOracleTypesBase as FlextTargetOracleTypesBase,
    )
_LAZY_IMPORTS = build_lazy_import_map({".base": ("FlextTargetOracleTypesBase",)})


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
