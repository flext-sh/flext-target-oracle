"""Production-Grade Singer Target for Oracle Database data loading."""

from __future__ import annotations

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

FlextOracleTargetConfig = FlextTargetOracleConfig  # Alias for backward compatibility
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
from flext_target_oracle.target_observability import (
    FlextOracleError,
    FlextOracleObs,
    configure_oracle_observability,
)
from flext_target_oracle.target_client import (
    FlextTargetOracle,
    FlextTargetOracleLoader,
    FlextTargetOraclePlugin,
    create_target_oracle_plugin,
    TargetOracle,
)

FlextOracleTargetLoader = FlextTargetOracleLoader  # Alias for backward compatibility
from flext_target_oracle.target_models import (
    LoadMethodModel,
    StorageModeModel,
    OracleConnectionModel,
    SingerStreamModel,
    BatchProcessingModel,
    LoadStatisticsModel,
    OracleTableMetadataModel,
)
from flext_target_oracle.target_services import (
    ConnectionServiceProtocol,
    SchemaServiceProtocol,
    BatchServiceProtocol,
    RecordServiceProtocol,
    OracleConnectionService,
    OracleSchemaService,
    OracleBatchService,
    OracleRecordService,
    OracleTargetServiceFactory,
)

__version__ = "0.9.0"
__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

__all__: list[str] = [
    # === FLEXT-MELTANO COMPLETE RE-EXPORTS ===
    "BatchSink",
    "FlextMeltanoBaseService",
    # Bridge integration
    "FlextMeltanoBridge",
    # Configuration patterns
    "FlextMeltanoConfig",
    "FlextMeltanoEvent",
    # Enterprise services
    "FlextMeltanoTargetService",
    # Authentication
    "OAuthAuthenticator",
    "PropertiesList",
    "Property",
    "SQLSink",
    "Sink",
    # Singer SDK core classes
    "Stream",
    "Tap",
    "Target",
    "create_meltano_target_service",
    # Testing
    "get_tap_test_class",
    # Singer typing
    "singer_typing",
    # === FLEXT-CORE RE-EXPORTS ===
    "FlextResult",
    # === PRIMARY TARGET CLASSES ===
    "FlextTargetOracle",
    "FlextTargetOracleLoader",
    "FlextOracleTargetLoader",  # Alias for backward compatibility
    "FlextTargetOraclePlugin",
    "create_target_oracle_plugin",
    "TargetOracle",  # Compatibility alias
    # === CONFIGURATION ===
    "FlextTargetOracleConfig",
    "FlextOracleTargetConfig",  # Alias for backward compatibility
    "LoadMethod",
    # === EXCEPTION HIERARCHY ===
    "FlextTargetOracleAuthenticationError",
    "FlextTargetOracleConnectionError",
    "FlextTargetOracleError",
    "FlextTargetOracleProcessingError",
    "FlextTargetOracleSchemaError",
    # Backward compatibility aliases
    "FlextOracleTargetError",
    "FlextOracleTargetAuthenticationError",
    "FlextOracleTargetConnectionError",
    "FlextOracleTargetProcessingError",
    "FlextOracleTargetSchemaError",
    # === OBSERVABILITY ===
    "FlextOracleError",
    "FlextOracleObs",
    "configure_oracle_observability",
    # === DATA MODELS ===
    "LoadMethodModel",
    "StorageModeModel",
    "OracleConnectionModel",
    "SingerStreamModel",
    "BatchProcessingModel",
    "LoadStatisticsModel",
    "OracleTableMetadataModel",
    # === SERVICES ===
    "ConnectionServiceProtocol",
    "SchemaServiceProtocol",
    "BatchServiceProtocol",
    "RecordServiceProtocol",
    "OracleConnectionService",
    "OracleSchemaService",
    "OracleBatchService",
    "OracleRecordService",
    "OracleTargetServiceFactory",
    # === METADATA ===
    "__version__",
    "__version_info__",
]
