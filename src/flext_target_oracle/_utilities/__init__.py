# AUTO-GENERATED FILE — Regenerate with: make gen
"""Utilities package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".base": ("FlextTargetOracleUtilitiesBase",),
        ".cli": (
            "FlextTargetOracleCliService",
            "main",
        ),
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
            "FlextTargetOracleServiceFactory",
        ),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
