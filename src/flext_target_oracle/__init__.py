"""Copyright (c) 2025 FLEXT Team. All rights reserved.

SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from flext_core import FlextTypes

"""Production-Grade Singer Target for Oracle Database data loading.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""


# Import FLEXT core patterns for ecosystem consistency
from flext_core import FlextResult

# === FLEXT-MELTANO COMPLETE INTEGRATION ===
# Re-export ALL flext-meltano facilities for full ecosystem integration
from flext_meltano import (
    # Bridge integration
    FlextMeltanoBridge,
    # Configuration and validation
    FlextMeltanoConfig,
    # Core Singer SDK classes (available from flext-meltano)
    FlextTarget as Target,
)

# Import local implementations - CONSOLIDATED PEP8 STRUCTURE
from flext_target_oracle.target_config import FlextTargetOracleConfig, LoadMethod

FlextOracleTargetConfig = FlextTargetOracleConfig
from flext_target_oracle.target_exceptions import (
    FlextTargetOracleAuthenticationError,
    FlextTargetOracleConnectionError,
    FlextTargetOracleError,
    FlextTargetOracleProcessingError,
    FlextTargetOracleSchemaError,
)

# Backward compatibility aliases for tests
FlextOracleTargetError = FlextTargetOracleError
FlextOracleTargetAuthenticationError = FlextTargetOracleAuthenticationError
FlextOracleTargetConnectionError = FlextTargetOracleConnectionError
FlextOracleTargetProcessingError = FlextTargetOracleProcessingError
FlextOracleTargetSchemaError = FlextTargetOracleSchemaError
from flext_target_oracle.target_client import (
    FlextTargetOracle,
    TargetOracle,
)
from flext_target_oracle.target_loader import (
    FlextTargetOracleLoader,
)
from flext_target_oracle.target_observability import (
    FlextOracleError,
    FlextOracleObs,
    configure_oracle_observability,
)

# Compatibility aliases
FlextOracleTargetLoader = FlextTargetOracleLoader
FlextTargetOraclePlugin = None  # Removed in SOLID refactoring
create_target_oracle_plugin = None  # Removed in SOLID refactoring
from flext_target_oracle.target_models import (
    BatchProcessingModel,
    LoadMethodModel,
    LoadStatisticsModel,
    OracleConnectionModel,
    OracleTableMetadataModel,
    SingerStreamModel,
    StorageModeModel,
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

__version__ = "0.9.0"
__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

__all__: FlextTypes.Core.StringList = [
    "BatchProcessingModel",
    "BatchServiceProtocol",
    # === FLEXT-MELTANO COMPLETE RE-EXPORTS ===
    "BatchSink",
    # === SERVICES ===
    "ConnectionServiceProtocol",
    "FlextMeltanoBaseService",
    # Bridge integration
    "FlextMeltanoBridge",
    # Configuration patterns
    "FlextMeltanoConfig",
    "FlextMeltanoEvent",
    # Enterprise services
    "FlextMeltanoTargetService",
    # === OBSERVABILITY ===
    "FlextOracleError",
    "FlextOracleObs",
    "FlextOracleTargetAuthenticationError",
    "FlextOracleTargetConfig",
    "FlextOracleTargetConnectionError",
    # Backward compatibility aliases
    "FlextOracleTargetError",
    "FlextOracleTargetLoader",
    "FlextOracleTargetProcessingError",
    "FlextOracleTargetSchemaError",
    # === FLEXT-CORE RE-EXPORTS ===
    "FlextResult",
    # === PRIMARY TARGET CLASSES ===
    "FlextTargetOracle",
    # === EXCEPTION HIERARCHY ===
    "FlextTargetOracleAuthenticationError",
    # === CONFIGURATION ===
    "FlextTargetOracleConfig",
    "FlextTargetOracleConnectionError",
    "FlextTargetOracleError",
    "FlextTargetOracleLoader",
    "FlextTargetOraclePlugin",
    "FlextTargetOracleProcessingError",
    "FlextTargetOracleSchemaError",
    "LoadMethod",
    # === DATA MODELS ===
    "LoadMethodModel",
    "LoadStatisticsModel",
    # Authentication
    "OAuthAuthenticator",
    "OracleBatchService",
    "OracleConnectionModel",
    "OracleConnectionService",
    "OracleRecordService",
    "OracleSchemaService",
    "OracleTableMetadataModel",
    "OracleTargetServiceFactory",
    "PropertiesList",
    "Property",
    "RecordServiceProtocol",
    "SQLSink",
    "SchemaServiceProtocol",
    "SingerStreamModel",
    "Sink",
    "StorageModeModel",
    # Singer SDK core classes
    "Stream",
    "Tap",
    "Target",
    "TargetOracle",  # Compatibility alias
    # === METADATA ===
    "__version__",
    "__version_info__",
    "configure_oracle_observability",
    "create_meltano_target_service",
    "create_target_oracle_plugin",
    # Testing
    "get_tap_test_class",
    # Singer typing
    "singer_typing",
]
