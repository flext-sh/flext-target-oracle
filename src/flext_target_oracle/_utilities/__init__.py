# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Utilities package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_target_oracle._utilities.cli as _flext_target_oracle__utilities_cli

    cli = _flext_target_oracle__utilities_cli
    import flext_target_oracle._utilities.client as _flext_target_oracle__utilities_client
    from flext_target_oracle._utilities.cli import FlextTargetOracleCliService, main

    client = _flext_target_oracle__utilities_client
    import flext_target_oracle._utilities.errors as _flext_target_oracle__utilities_errors
    from flext_target_oracle._utilities.client import FlextTargetOracle

    errors = _flext_target_oracle__utilities_errors
    import flext_target_oracle._utilities.loader as _flext_target_oracle__utilities_loader
    from flext_target_oracle._utilities.errors import (
        FlextTargetOracleErrorMetadata,
        FlextTargetOracleExceptions,
    )

    loader = _flext_target_oracle__utilities_loader
    import flext_target_oracle._utilities.observability as _flext_target_oracle__utilities_observability
    from flext_target_oracle._utilities.loader import FlextTargetOracleLoader

    observability = _flext_target_oracle__utilities_observability
    import flext_target_oracle._utilities.services as _flext_target_oracle__utilities_services
    from flext_target_oracle._utilities.observability import (
        FlextOracleError,
        FlextOracleObs,
        configure_oracle_observability,
    )

    services = _flext_target_oracle__utilities_services
    from flext_target_oracle._utilities.services import (
        FlextTargetOracleBatchService,
        FlextTargetOracleConnectionService,
        FlextTargetOracleRecordService,
        FlextTargetOracleSchemaService,
        FlextTargetOracleServiceFactory,
    )
_LAZY_IMPORTS = {
    "FlextOracleError": "flext_target_oracle._utilities.observability",
    "FlextOracleObs": "flext_target_oracle._utilities.observability",
    "FlextTargetOracle": "flext_target_oracle._utilities.client",
    "FlextTargetOracleBatchService": "flext_target_oracle._utilities.services",
    "FlextTargetOracleCliService": "flext_target_oracle._utilities.cli",
    "FlextTargetOracleConnectionService": "flext_target_oracle._utilities.services",
    "FlextTargetOracleErrorMetadata": "flext_target_oracle._utilities.errors",
    "FlextTargetOracleExceptions": "flext_target_oracle._utilities.errors",
    "FlextTargetOracleLoader": "flext_target_oracle._utilities.loader",
    "FlextTargetOracleRecordService": "flext_target_oracle._utilities.services",
    "FlextTargetOracleSchemaService": "flext_target_oracle._utilities.services",
    "FlextTargetOracleServiceFactory": "flext_target_oracle._utilities.services",
    "cli": "flext_target_oracle._utilities.cli",
    "client": "flext_target_oracle._utilities.client",
    "configure_oracle_observability": "flext_target_oracle._utilities.observability",
    "errors": "flext_target_oracle._utilities.errors",
    "loader": "flext_target_oracle._utilities.loader",
    "main": "flext_target_oracle._utilities.cli",
    "observability": "flext_target_oracle._utilities.observability",
    "services": "flext_target_oracle._utilities.services",
}

__all__ = [
    "FlextOracleError",
    "FlextOracleObs",
    "FlextTargetOracle",
    "FlextTargetOracleBatchService",
    "FlextTargetOracleCliService",
    "FlextTargetOracleConnectionService",
    "FlextTargetOracleErrorMetadata",
    "FlextTargetOracleExceptions",
    "FlextTargetOracleLoader",
    "FlextTargetOracleRecordService",
    "FlextTargetOracleSchemaService",
    "FlextTargetOracleServiceFactory",
    "cli",
    "client",
    "configure_oracle_observability",
    "errors",
    "loader",
    "main",
    "observability",
    "services",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
