"""Production-Grade Singer Target for Oracle Database data loading.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextResult
from flext_meltano import (
    FlextMeltanoBridge,
    FlextMeltanoConfig,
    FlextMeltanoTypes,
    FlextSingerTypes,
    FlextTargetAbstractions,
)
from flext_target_oracle.config import FlextTargetOracleConfig, LoadMethod

# Standardized [Project]Models and [Project]Utilities patterns
from flext_target_oracle.models import FlextTargetOracleModels
from flext_target_oracle.protocols import FlextTargetOracleProtocols
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

# Legacy model imports for backward compatibility
from flext_target_oracle.target_models import (
    BatchProcessingModel,
    LoadMethodModel,
    LoadStatisticsModel,
    OracleConnectionModel,
    OracleTableMetadataModel,
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
from flext_target_oracle.typings import FlextTargetOracleTypes
from flext_target_oracle.utilities import FlextTargetOracleUtilities

__version__ = "0.9.0"
__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

__all__: FlextTargetOracleTypes.Core.StringList = [
    # Data Models
    "BatchProcessingModel",
    "BatchServiceProtocol",
    "ConnectionServiceProtocol",
    # Core Integration
    "FlextMeltanoBridge",
    "FlextMeltanoConfig",
    "FlextMeltanoTypes",
    # Observability
    "FlextOracleError",
    "FlextOracleObs",
    # Core Classes
    "FlextResult",
    "FlextSingerTypes",
    "FlextTargetAbstractions",
    "FlextTargetOracle",
    "FlextTargetOracleAuthenticationError",
    "FlextTargetOracleCliService",
    "FlextTargetOracleConfig",
    "FlextTargetOracleConnectionError",
    "FlextTargetOracleError",
    "FlextTargetOracleLoader",
    # Standardized Patterns
    "FlextTargetOracleModels",
    "FlextTargetOracleProcessingError",
    "FlextTargetOracleProtocols",
    "FlextTargetOracleSchemaError",
    "FlextTargetOracleUtilities",
    "LoadMethod",
    "LoadMethodModel",
    "LoadStatisticsModel",
    # Services
    "OracleBatchService",
    "OracleConnectionModel",
    "OracleConnectionService",
    "OracleRecordService",
    "OracleSchemaService",
    "OracleTableMetadataModel",
    "OracleTargetCommandFactory",
    "OracleTargetServiceFactory",
    "RecordServiceProtocol",
    "SchemaServiceProtocol",
    "SingerStreamModel",
    "StorageModeModel",
    # Metadata
    "__version__",
    "__version_info__",
    "configure_oracle_observability",
]
