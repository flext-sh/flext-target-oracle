"""FLEXT Target Oracle - Production-Grade Singer Target for Oracle Database.

This module provides a complete Singer specification-compliant target for Oracle
Database data loading, built using FLEXT ecosystem patterns and enterprise-grade
reliability standards.

The target implements Clean Architecture principles with Domain-Driven Design
patterns, leveraging the FLEXT ecosystem's foundational components for consistent
error handling, configuration management, and database operations.

Key Components:
    FlextTargetOracle: Main Singer target implementation with async processing
    FlextTargetOracleConfig: Type-safe configuration with domain validation
    LoadMethod: Enumeration of supported Oracle loading strategies
    Exception Hierarchy: Comprehensive error handling with context preservation

Architecture Integration:
    Built on flext-core foundations (FlextResult, FlextValueObject patterns)
    Integrates with flext-meltano for Singer SDK compliance
    Uses flext-db-oracle for production-grade Oracle connectivity
    Follows railway-oriented programming for error handling

Example:
    Basic target initialization and configuration:

    >>> from flext_target_oracle import FlextTargetOracle, FlextTargetOracleConfig
    >>> config = FlextTargetOracleConfig(
    ...     oracle_host="localhost",
    ...     oracle_service="XE",
    ...     oracle_user="target_user",
    ...     oracle_password="secure_password",
    ... )
    >>> target = FlextTargetOracle(config)
    >>> # Process Singer messages
    >>> result = await target.process_singer_message(schema_message)
    >>> if result.success:
    ...     print("Schema processed successfully")

Note:
    Version 0.9.0 is pre-production. See docs/TODO.md for known issues including
    SQL injection vulnerabilities and missing Singer SDK methods that must be
    addressed before production deployment.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

# Import FLEXT core patterns for ecosystem consistency
from flext_core import FlextResult

# === FLEXT-MELTANO COMPLETE INTEGRATION ===
# Re-export ALL flext-meltano facilities for full ecosystem integration
from flext_meltano import (
    BatchSink,
    FlextMeltanoBaseService,
    # Bridge integration
    FlextMeltanoBridge,
    # Configuration and validation
    FlextMeltanoConfig,
    FlextMeltanoEvent,
    # Enterprise services from flext-meltano.base
    FlextMeltanoTargetService,
    # Authentication patterns
    OAuthAuthenticator,
    # Typing definitions
    PropertiesList,
    Property,
    Sink,
    SQLSink,
    # Core Singer SDK classes (centralized from flext-meltano)
    Stream,
    Tap,
    Target,
    create_meltano_target_service,
    # Testing utilities
    get_tap_test_class,
    # Singer typing utilities (centralized)
    singer_typing,
)

# Import local implementations - CONSOLIDATED PEP8 STRUCTURE
from flext_target_oracle.target_config import FlextTargetOracleConfig, LoadMethod
from flext_target_oracle.target_exceptions import (
    FlextTargetOracleAuthenticationError,
    FlextTargetOracleConnectionError,
    FlextTargetOracleError,
    FlextTargetOracleProcessingError,
    FlextTargetOracleSchemaError,
)
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
"""Current version - pre-production with known critical issues."""

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
    "FlextTargetOraclePlugin",
    "create_target_oracle_plugin",
    "TargetOracle",  # Compatibility alias
    
    # === CONFIGURATION ===
    "FlextTargetOracleConfig",
    "LoadMethod",
    
    # === EXCEPTION HIERARCHY ===
    "FlextTargetOracleAuthenticationError",
    "FlextTargetOracleConnectionError",
    "FlextTargetOracleError",
    "FlextTargetOracleProcessingError",
    "FlextTargetOracleSchemaError",
    
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
]
