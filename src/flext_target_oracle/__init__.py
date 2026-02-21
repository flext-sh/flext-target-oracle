"""Production-Grade Singer Target for Oracle Database data loading.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextResult
from flext_meltano import (
    FlextMeltanoSettings,
    FlextMeltanoTargetAbstractions,
    FlextMeltanoTypes,
)

from flext_target_oracle.models import FlextTargetOracleModels, m
from flext_target_oracle.protocols import FlextTargetOracleProtocols
from flext_target_oracle.settings import FlextTargetOracleSettings, LoadMethod
from flext_target_oracle.target_client import FlextTargetOracle
from flext_target_oracle.target_commands import OracleTargetCommandFactory
from flext_target_oracle.target_exceptions import (
    FlextTargetOracleAuthenticationError,
    FlextTargetOracleConnectionError,
    FlextTargetOracleError,
    FlextTargetOracleProcessingError,
    FlextTargetOracleSchemaError,
)
from flext_target_oracle.target_loader import FlextTargetOracleLoader
from flext_target_oracle.target_models import (
    LoadMethodModel,
    LoadStatisticsModel,
    OracleConnectionModel,
    SingerStreamModel,
    StorageModeModel,
)
from flext_target_oracle.target_observability import (
    FlextOracleError,
    FlextOracleObs,
    configure_oracle_observability,
)
from flext_target_oracle.target_refactored import FlextTargetOracleCliService
from flext_target_oracle.target_services import (
    BatchServiceProtocol,
    ConnectionServiceProtocol,
    OracleBatchService,
    OracleConnectionService,
    OracleRecordService,
    OracleSchemaService,
    OracleTargetServiceFactory,
    RecordServiceProtocol,
    SchemaServiceProtocol,
)
from flext_target_oracle.typings import FlextTargetOracleTypes, t
from flext_target_oracle.utilities import (
    FlextTargetOracleUtilities,
    FlextTargetOracleUtilities as u,
)

# Version imports removed - not available

# Version constants removed - not available

__all__ = [
    "BatchServiceProtocol",
    "ConnectionServiceProtocol",
    "FlextMeltanoSettings",
    "FlextMeltanoTargetAbstractions",
    "FlextMeltanoTypes",
    "FlextOracleError",
    "FlextOracleObs",
    "FlextResult",
    "FlextTargetOracle",
    "FlextTargetOracleAuthenticationError",
    "FlextTargetOracleCliService",
    "FlextTargetOracleConnectionError",
    "FlextTargetOracleError",
    "FlextTargetOracleLoader",
    "FlextTargetOracleModels",
    "FlextTargetOracleProcessingError",
    "FlextTargetOracleProtocols",
    "FlextTargetOracleSchemaError",
    "FlextTargetOracleSettings",
    "FlextTargetOracleTypes",
    "FlextTargetOracleUtilities",
    "LoadMethod",
    "LoadMethodModel",
    "LoadStatisticsModel",
    "OracleBatchService",
    "OracleConnectionModel",
    "OracleConnectionService",
    "OracleRecordService",
    "OracleSchemaService",
    "OracleTargetCommandFactory",
    "OracleTargetServiceFactory",
    "RecordServiceProtocol",
    "SchemaServiceProtocol",
    "SingerStreamModel",
    "StorageModeModel",
    "configure_oracle_observability",
    "m",
    "t",
    "u",
]
