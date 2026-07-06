# AUTO-GENERATED FILE — Regenerate with: make gen
"""Utilities package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_target_oracle._utilities.base import FlextTargetOracleUtilitiesBase
    from flext_target_oracle._utilities.client import FlextTargetOracle
    from flext_target_oracle._utilities.errors import (
        FlextTargetOracleErrorMetadata,
        FlextTargetOracleExceptions,
    )
    from flext_target_oracle._utilities.loader import FlextTargetOracleLoader
    from flext_target_oracle._utilities.observability import (
        FlextTargetOracleUtilitiesObservability,
    )
    from flext_target_oracle._utilities.services import (
        FlextTargetOracleBatchService,
        FlextTargetOracleConnectionService,
        FlextTargetOracleRecordService,
        FlextTargetOracleSchemaService,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
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
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
