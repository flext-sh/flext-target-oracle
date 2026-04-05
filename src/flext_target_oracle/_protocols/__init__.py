# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Protocols package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_target_oracle._protocols.base as _flext_target_oracle__protocols_base

    base = _flext_target_oracle__protocols_base
    from flext_target_oracle._protocols.base import FlextTargetOracleProtocolsBase
_LAZY_IMPORTS = {
    "FlextTargetOracleProtocolsBase": "flext_target_oracle._protocols.base",
    "base": "flext_target_oracle._protocols.base",
}

__all__ = [
    "FlextTargetOracleProtocolsBase",
    "base",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
