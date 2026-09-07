# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Oracle. Utilities package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .base import FlextTargetOracleUtilitiesBase
    from .client import FlextTargetOracle
    from .errors import FlextTargetOracleErrorMetadata, FlextTargetOracleExceptions
    from .loader import FlextTargetOracleLoader
    from .observability import FlextTargetOracleUtilitiesObservability
    from .services import (
        FlextTargetOracleBatchService,
        FlextTargetOracleConnectionService,
        FlextTargetOracleRecordService,
        FlextTargetOracleSchemaService,
    )
__all__: tuple[str, ...] = (
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

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("FlextTargetOracleUtilitiesBase",),
            ".client": ("FlextTargetOracle",),
            ".errors": (
                "FlextTargetOracleErrorMetadata",
                "FlextTargetOracleExceptions",
            ),
            ".loader": ("FlextTargetOracleLoader",),
            ".observability": ("FlextTargetOracleUtilitiesObservability",),
            ".services": (
                "FlextTargetOracleBatchService",
                "FlextTargetOracleConnectionService",
                "FlextTargetOracleRecordService",
                "FlextTargetOracleSchemaService",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
