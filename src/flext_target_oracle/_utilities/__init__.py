# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Utilities package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "FlextTargetOracle": ("flext_target_oracle._utilities.client", "FlextTargetOracle"),
    "FlextTargetOracleBatchService": (
        "flext_target_oracle._utilities.services",
        "FlextTargetOracleBatchService",
    ),
    "FlextTargetOracleCliService": (
        "flext_target_oracle._utilities.cli",
        "FlextTargetOracleCliService",
    ),
    "FlextTargetOracleConnectionService": (
        "flext_target_oracle._utilities.services",
        "FlextTargetOracleConnectionService",
    ),
    "FlextTargetOracleErrorMetadata": (
        "flext_target_oracle._utilities.errors",
        "FlextTargetOracleErrorMetadata",
    ),
    "FlextTargetOracleExceptions": (
        "flext_target_oracle._utilities.errors",
        "FlextTargetOracleExceptions",
    ),
    "FlextTargetOracleLoader": (
        "flext_target_oracle._utilities.loader",
        "FlextTargetOracleLoader",
    ),
    "FlextTargetOracleRecordService": (
        "flext_target_oracle._utilities.services",
        "FlextTargetOracleRecordService",
    ),
    "FlextTargetOracleSchemaService": (
        "flext_target_oracle._utilities.services",
        "FlextTargetOracleSchemaService",
    ),
    "FlextTargetOracleServiceFactory": (
        "flext_target_oracle._utilities.services",
        "FlextTargetOracleServiceFactory",
    ),
    "FlextTargetOracleUtilitiesBase": (
        "flext_target_oracle._utilities.base",
        "FlextTargetOracleUtilitiesBase",
    ),
    "FlextTargetOracleUtilitiesObservability": (
        "flext_target_oracle._utilities.observability",
        "FlextTargetOracleUtilitiesObservability",
    ),
    "base": "flext_target_oracle._utilities.base",
    "cli": "flext_target_oracle._utilities.cli",
    "client": "flext_target_oracle._utilities.client",
    "errors": "flext_target_oracle._utilities.errors",
    "loader": "flext_target_oracle._utilities.loader",
    "observability": "flext_target_oracle._utilities.observability",
    "services": "flext_target_oracle._utilities.services",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
