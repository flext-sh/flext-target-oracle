# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Constants package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_target_oracle._constants.base as _flext_target_oracle__constants_base

    base = _flext_target_oracle__constants_base
    from flext_target_oracle._constants.base import FlextTargetOracleConstantsBase
_LAZY_IMPORTS = {
    "FlextTargetOracleConstantsBase": "flext_target_oracle._constants.base",
    "base": "flext_target_oracle._constants.base",
}

__all__ = [
    "FlextTargetOracleConstantsBase",
    "base",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
