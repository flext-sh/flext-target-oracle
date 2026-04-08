# AUTO-GENERATED FILE — Regenerate with: make gen
from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "FlextTargetOracle": ".client",
    "FlextTargetOracleBatchService": ".services",
    "FlextTargetOracleCliService": ".cli",
    "FlextTargetOracleConnectionService": ".services",
    "FlextTargetOracleErrorMetadata": ".errors",
    "FlextTargetOracleExceptions": ".errors",
    "FlextTargetOracleLoader": ".loader",
    "FlextTargetOracleRecordService": ".services",
    "FlextTargetOracleSchemaService": ".services",
    "FlextTargetOracleServiceFactory": ".services",
    "FlextTargetOracleUtilitiesBase": ".base",
    "FlextTargetOracleUtilitiesObservability": ".observability",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
