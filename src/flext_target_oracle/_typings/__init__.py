# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Typings package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_target_oracle._typings.base as _flext_target_oracle__typings_base

    base = _flext_target_oracle__typings_base
    from flext_target_oracle._typings.base import FlextTargetOracleTypesBase
_LAZY_IMPORTS = {
    "FlextTargetOracleTypesBase": (
        "flext_target_oracle._typings.base",
        "FlextTargetOracleTypesBase",
    ),
    "base": "flext_target_oracle._typings.base",
}

__all__ = [
    "FlextTargetOracleTypesBase",
    "base",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
