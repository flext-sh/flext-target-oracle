# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Internal utilities subpackage for flext-target-oracle."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_oracle._utilities import (
        cli as cli,
        client as client,
        errors as errors,
        loader as loader,
        observability as observability,
        service as service,
        services as services,
    )
    from flext_target_oracle._utilities.cli import (
        FlextTargetOracleCliService as FlextTargetOracleCliService,
        main as main,
    )
    from flext_target_oracle._utilities.client import (
        FlextTargetOracle as FlextTargetOracle,
    )
    from flext_target_oracle._utilities.errors import (
        FlextTargetOracleErrorMetadata as FlextTargetOracleErrorMetadata,
        FlextTargetOracleExceptions as FlextTargetOracleExceptions,
    )
    from flext_target_oracle._utilities.loader import (
        FlextTargetOracleLoader as FlextTargetOracleLoader,
    )
    from flext_target_oracle._utilities.observability import (
        FlextOracleError as FlextOracleError,
        FlextOracleObs as FlextOracleObs,
        configure_oracle_observability as configure_oracle_observability,
    )
    from flext_target_oracle._utilities.service import (
        FlextTargetOracleService as FlextTargetOracleService,
    )
    from flext_target_oracle._utilities.services import (
        FlextTargetOracleBatchService as FlextTargetOracleBatchService,
        FlextTargetOracleConnectionService as FlextTargetOracleConnectionService,
        FlextTargetOracleRecordService as FlextTargetOracleRecordService,
        FlextTargetOracleSchemaService as FlextTargetOracleSchemaService,
        FlextTargetOracleServiceFactory as FlextTargetOracleServiceFactory,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextOracleError": [
        "flext_target_oracle._utilities.observability",
        "FlextOracleError",
    ],
    "FlextOracleObs": [
        "flext_target_oracle._utilities.observability",
        "FlextOracleObs",
    ],
    "FlextTargetOracle": ["flext_target_oracle._utilities.client", "FlextTargetOracle"],
    "FlextTargetOracleBatchService": [
        "flext_target_oracle._utilities.services",
        "FlextTargetOracleBatchService",
    ],
    "FlextTargetOracleCliService": [
        "flext_target_oracle._utilities.cli",
        "FlextTargetOracleCliService",
    ],
    "FlextTargetOracleConnectionService": [
        "flext_target_oracle._utilities.services",
        "FlextTargetOracleConnectionService",
    ],
    "FlextTargetOracleErrorMetadata": [
        "flext_target_oracle._utilities.errors",
        "FlextTargetOracleErrorMetadata",
    ],
    "FlextTargetOracleExceptions": [
        "flext_target_oracle._utilities.errors",
        "FlextTargetOracleExceptions",
    ],
    "FlextTargetOracleLoader": [
        "flext_target_oracle._utilities.loader",
        "FlextTargetOracleLoader",
    ],
    "FlextTargetOracleRecordService": [
        "flext_target_oracle._utilities.services",
        "FlextTargetOracleRecordService",
    ],
    "FlextTargetOracleSchemaService": [
        "flext_target_oracle._utilities.services",
        "FlextTargetOracleSchemaService",
    ],
    "FlextTargetOracleService": [
        "flext_target_oracle._utilities.service",
        "FlextTargetOracleService",
    ],
    "FlextTargetOracleServiceFactory": [
        "flext_target_oracle._utilities.services",
        "FlextTargetOracleServiceFactory",
    ],
    "cli": ["flext_target_oracle._utilities.cli", ""],
    "client": ["flext_target_oracle._utilities.client", ""],
    "configure_oracle_observability": [
        "flext_target_oracle._utilities.observability",
        "configure_oracle_observability",
    ],
    "errors": ["flext_target_oracle._utilities.errors", ""],
    "loader": ["flext_target_oracle._utilities.loader", ""],
    "main": ["flext_target_oracle._utilities.cli", "main"],
    "observability": ["flext_target_oracle._utilities.observability", ""],
    "service": ["flext_target_oracle._utilities.service", ""],
    "services": ["flext_target_oracle._utilities.services", ""],
}

_EXPORTS: Sequence[str] = [
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
    "FlextTargetOracleService",
    "FlextTargetOracleServiceFactory",
    "cli",
    "client",
    "configure_oracle_observability",
    "errors",
    "loader",
    "main",
    "observability",
    "service",
    "services",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
