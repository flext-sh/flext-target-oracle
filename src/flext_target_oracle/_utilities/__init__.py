# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Utilities package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_target_oracle._utilities.base as _flext_target_oracle__utilities_base

    base = _flext_target_oracle__utilities_base
    import flext_target_oracle._utilities.cli as _flext_target_oracle__utilities_cli
    from flext_target_oracle._utilities.base import FlextTargetOracleUtilitiesBase

    cli = _flext_target_oracle__utilities_cli
    import flext_target_oracle._utilities.client as _flext_target_oracle__utilities_client
    from flext_target_oracle._utilities.cli import FlextTargetOracleCliService

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
        FlextTargetOracleUtilitiesObservability,
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

__all__ = [
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
    "FlextTargetOracleUtilitiesBase",
    "FlextTargetOracleUtilitiesObservability",
    "base",
    "cli",
    "client",
    "errors",
    "loader",
    "observability",
    "services",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
