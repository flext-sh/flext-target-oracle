"""Production-Grade Singer Target for Oracle Database data loading.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final

from flext_core import FlextResult
from flext_meltano import (
    FlextMeltanoBridge,
    FlextMeltanoConfig,
    FlextMeltanoTargetAbstractions,
    FlextMeltanoTypes,
)

from flext_target_oracle.__version__ import __version__, __version_info__
from flext_target_oracle.config import FlextTargetOracleConfig, LoadMethod
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
from flext_target_oracle.version import VERSION, FlextTargetOracleVersion

PROJECT_VERSION: Final[FlextTargetOracleVersion] = VERSION

__version__: str = VERSION.version
__version_info__: tuple[int | str, ...] = VERSION.version_info

__all__ = [
    "PROJECT_VERSION",
    "VERSION",
    "BatchProcessingModel",
    "BatchServiceProtocol",
    "ConnectionServiceProtocol",
    "FlextMeltanoBridge",
    "FlextMeltanoConfig",
    "FlextMeltanoTargetAbstractions",
    "FlextMeltanoTypes",
    "FlextMeltanoTypes",
    "FlextOracleError",
    "FlextOracleObs",
    "FlextResult",
    "FlextTargetOracle",
    "FlextTargetOracleAuthenticationError",
    "FlextTargetOracleCliService",
    "FlextTargetOracleConfig",
    "FlextTargetOracleConnectionError",
    "FlextTargetOracleError",
    "FlextTargetOracleLoader",
    "FlextTargetOracleModels",
    "FlextTargetOracleProcessingError",
    "FlextTargetOracleProtocols",
    "FlextTargetOracleSchemaError",
    "FlextTargetOracleTypes",
    "FlextTargetOracleUtilities",
    "FlextTargetOracleVersion",
    "LoadMethod",
    "LoadMethodModel",
    "LoadStatisticsModel",
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
    "__version__",
    "__version_info__",
    "configure_oracle_observability",
]
