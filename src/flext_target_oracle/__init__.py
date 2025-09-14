"""Production-Grade Singer Target for Oracle Database data loading.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextResult, FlextTypes
from flext_meltano import (
    FlextMeltanoBridge,
    FlextMeltanoConfig,
    FlextMeltanoTypes,
    FlextSingerTypes,
    FlextTargetAbstractions,
)

from flext_target_oracle.target_client import (
    FlextTargetOracle,
    TargetOracle,
)
from flext_target_oracle.target_config import FlextTargetOracleConfig, LoadMethod
from flext_target_oracle.target_exceptions import (
    FlextTargetOracleAuthenticationError,
    FlextTargetOracleConnectionError,
    FlextTargetOracleError,
    FlextTargetOracleProcessingError,
    FlextTargetOracleSchemaError,
)
from flext_target_oracle.target_loader import FlextTargetOracleLoader
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

# Backward compatibility aliases
FlextOracleTargetConfig = FlextTargetOracleConfig
FlextOracleTargetError = FlextTargetOracleError
FlextOracleTargetAuthenticationError = FlextTargetOracleAuthenticationError
FlextOracleTargetConnectionError = FlextTargetOracleConnectionError
FlextOracleTargetProcessingError = FlextTargetOracleProcessingError
FlextOracleTargetSchemaError = FlextTargetOracleSchemaError
FlextOracleTargetLoader = FlextTargetOracleLoader

__version__ = "0.9.0"
__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

__all__: FlextTypes.Core.StringList = [
    # Data Models
    "BatchProcessingModel",
    "BatchServiceProtocol",
    "ConnectionServiceProtocol",
    # Core Integration
    "FlextMeltanoBridge",
    "FlextMeltanoConfig",
    "FlextMeltanoTypes",
    "FlextSingerTypes",
    "FlextTargetAbstractions",
    # Observability
    "FlextOracleError",
    "FlextOracleObs",
    "FlextOracleTargetAuthenticationError",
    "FlextOracleTargetConfig",
    "FlextOracleTargetConnectionError",
    "FlextOracleTargetError",
    "FlextOracleTargetLoader",
    "FlextOracleTargetProcessingError",
    "FlextOracleTargetSchemaError",
    # Core Classes
    "FlextResult",
    "FlextTargetOracle",
    "FlextTargetOracleAuthenticationError",
    "FlextTargetOracleConfig",
    "FlextTargetOracleConnectionError",
    "FlextTargetOracleError",
    "FlextTargetOracleLoader",
    "FlextTargetOracleProcessingError",
    "FlextTargetOracleSchemaError",
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
    "OracleTargetServiceFactory",
    "RecordServiceProtocol",
    "SchemaServiceProtocol",
    "SingerStreamModel",
    "StorageModeModel",
    # Core Classes
    "TargetOracle",
    # Metadata
    "__version__",
    "__version_info__",
    "configure_oracle_observability",
]: FlextTypes.Core.StringList = [
    # Data Models
    "BatchProcessingModel",
    "BatchServiceProtocol",
    "ConnectionServiceProtocol",
    # Core Integration
    "FlextMeltanoBridge",
    "FlextMeltanoConfig",
    "FlextTargetAbstractions",
    "FlextSingerTypes",
    "FlextMeltanoTypes",
    # Observability
    "FlextOracleError",
    "FlextOracleObs",
    "FlextOracleTargetAuthenticationError",
    "FlextOracleTargetConfig",
    "FlextOracleTargetConnectionError",
    "FlextOracleTargetError",
    "FlextOracleTargetLoader",
    "FlextOracleTargetProcessingError",
    "FlextOracleTargetSchemaError",
    # Core Classes
    "FlextResult",
    "FlextTargetOracle",
    "FlextTargetOracleAuthenticationError",
    "FlextTargetOracleConfig",
    "FlextTargetOracleConnectionError",
    "FlextTargetOracleError",
    "FlextTargetOracleLoader",
    "FlextTargetOracleProcessingError",
    "FlextTargetOracleSchemaError",
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
    "OracleTargetServiceFactory",
    "RecordServiceProtocol",
    "SchemaServiceProtocol",
    "SingerStreamModel",
    "StorageModeModel",
    # Core Classes
    "TargetOracle",
    # Metadata
    "__version__",
    "__version_info__",
    "configure_oracle_observability",
]
