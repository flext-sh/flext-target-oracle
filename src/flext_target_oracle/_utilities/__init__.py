# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Oracle. Utilities package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .base import FlextTargetOracleUtilitiesBase as FlextTargetOracleUtilitiesBase
    from .client import FlextTargetOracle as FlextTargetOracle
    from .errors import FlextTargetOracleErrorMetadata as FlextTargetOracleErrorMetadata
    from .errors import FlextTargetOracleExceptions as FlextTargetOracleExceptions
    from .loader import FlextTargetOracleLoader as FlextTargetOracleLoader
    from .observability import (
        FlextTargetOracleUtilitiesObservability as FlextTargetOracleUtilitiesObservability,
    )
    from .services import FlextTargetOracleBatchService as FlextTargetOracleBatchService
    from .services import (
        FlextTargetOracleConnectionService as FlextTargetOracleConnectionService,
    )
    from .services import (
        FlextTargetOracleRecordService as FlextTargetOracleRecordService,
    )
    from .services import (
        FlextTargetOracleSchemaService as FlextTargetOracleSchemaService,
    )

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    ".base": ("FlextTargetOracleUtilitiesBase",),
    ".client": ("FlextTargetOracle",),
    ".errors": ("FlextTargetOracleErrorMetadata", "FlextTargetOracleExceptions"),
    ".loader": ("FlextTargetOracleLoader",),
    ".observability": ("FlextTargetOracleUtilitiesObservability",),
    ".services": (
        "FlextTargetOracleBatchService",
        "FlextTargetOracleConnectionService",
        "FlextTargetOracleRecordService",
        "FlextTargetOracleSchemaService",
    ),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextTargetOracle",
    "FlextTargetOracleBatchService",
    "FlextTargetOracleConnectionService",
    "FlextTargetOracleErrorMetadata",
    "FlextTargetOracleExceptions",
    "FlextTargetOracleLoader",
    "FlextTargetOracleRecordService",
    "FlextTargetOracleSchemaService",
    "FlextTargetOracleUtilitiesBase",
    "FlextTargetOracleUtilitiesObservability",
)

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
