# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Internal utilities subpackage for flext-target-oracle."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_oracle._utilities.cli import *
    from flext_target_oracle._utilities.client import *
    from flext_target_oracle._utilities.errors import *
    from flext_target_oracle._utilities.loader import *
    from flext_target_oracle._utilities.observability import *
    from flext_target_oracle._utilities.service import *
    from flext_target_oracle._utilities.services import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
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
    "FlextTargetOracleService": "flext_target_oracle._utilities.service",
    "FlextTargetOracleServiceFactory": "flext_target_oracle._utilities.services",
    "cli": "flext_target_oracle._utilities.cli",
    "client": "flext_target_oracle._utilities.client",
    "configure_oracle_observability": "flext_target_oracle._utilities.observability",
    "errors": "flext_target_oracle._utilities.errors",
    "loader": "flext_target_oracle._utilities.loader",
    "main": "flext_target_oracle._utilities.cli",
    "observability": "flext_target_oracle._utilities.observability",
    "service": "flext_target_oracle._utilities.service",
    "services": "flext_target_oracle._utilities.services",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
