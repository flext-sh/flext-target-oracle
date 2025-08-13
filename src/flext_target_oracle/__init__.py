"""FLEXT Target Oracle - Production-Grade Singer Target for Oracle Database in FLEXT ecosystem.

This module provides a comprehensive Singer specification-compliant target for Oracle
Database data loading, implementing enterprise-grade reliability, performance, and
error handling standards within the FLEXT data integration ecosystem.

The target follows Clean Architecture principles with Domain-Driven Design patterns,
leveraging FLEXT ecosystem's foundational components for consistent configuration
management, database operations, and comprehensive error handling with observability.

Architecture (Clean Architecture + Singer Patterns):
    - Target Layer: Singer target implementation with stream processing and loading
    - Application Layer: Data loading services and transformation logic
    - Domain Layer: Oracle-specific data models and business rules
    - Infrastructure Layer: Database connectivity and batch processing via flext-db-oracle

Key Features:
    - Singer Specification Compliance: Full adherence to Singer target standards
    - High-Performance Loading: Optimized bulk loading with Oracle-specific features
    - Transaction Management: ACID-compliant transactions with rollback capabilities
    - Schema Evolution: Automatic schema creation and evolution support
    - Data Validation: Comprehensive validation with detailed error reporting
    - Upsert Operations: Merge/upsert support for incremental data loading
    - Batch Processing: Configurable batch sizes for optimal performance
    - Error Recovery: Robust error handling with retry mechanisms
    - Monitoring: Built-in metrics and observability for loading operations

Oracle-Specific Optimizations:
    - Direct Path Loading: Oracle SQL*Loader integration for maximum performance
    - Partition-Aware Loading: Intelligent partition key handling
    - Advanced Data Types: Full support for Oracle-specific types (CLOB, BLOB, etc.)
    - Constraint Handling: Smart constraint validation and deferred checking
    - Parallel Processing: Multi-threaded loading with Oracle parallel DML

Key Components:
    - FlextTargetOracle: Main Singer target implementation with async processing
    - FlextTargetOracleConfig: Type-safe configuration with domain validation
    - FlextOracleLoadMethod: Enumeration of supported Oracle loading strategies
    - FlextTargetOracleException: Comprehensive error handling with context preservation

FLEXT Ecosystem Integration:
    - Built on flext-core foundations (FlextResult, FlextValueObject patterns)
    - Integrates with flext-meltano for Singer SDK compliance and orchestration
    - Uses flext-db-oracle for production-grade Oracle database connectivity
    - Follows railway-oriented programming patterns for error handling
    - Leverages flext-auth for secure credential management

Example:
    Basic target configuration and usage:

    >>> from flext_target_oracle import FlextTargetOracle, FlextTargetOracleConfig
    >>> from flext_core import FlextResult
    >>>
    >>> # Configure target with connection details
    >>> config = FlextTargetOracleConfig(
    ...     oracle_host="oracle.example.com",
    ...     oracle_port=1521,
    ...     oracle_service="PROD",
    ...     oracle_user="target_user",
    ...     oracle_password="secure_password",
    ...     batch_size=10000,
    ...     load_method="BULK_INSERT",
    ... )
    >>>
    >>> # Initialize and process data
    >>> target = FlextTargetOracle(config)
    >>> result = target.process_stream("users", user_records)
    >>> if result.is_success:
    ...     print(f"Loaded {result.data.records_processed} records")

    Advanced loading with upsert operations:

    >>> # Configure for incremental loading with merge operations
    >>> config.load_method = "UPSERT"
    >>> config.primary_keys = ["user_id"]
    >>> target = FlextTargetOracle(config)
    >>>
    >>> # Process incremental data with automatic schema evolution
    >>> result = target.process_incremental_stream("user_updates", updates)
    >>> if result.is_success:
    ...     stats = result.data
    ...     print(f"Inserted: {stats.inserted}, Updated: {stats.updated}")

Note:
    Version 0.9.0 is pre-production. See docs/TODO.md for known issues including
    SQL injection vulnerabilities and missing Singer SDK methods that must be
    addressed before production deployment.

Copyright (c) 2025 FLEXT Contributors
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
from flext_target_oracle.models import (
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
    "__version_info__",
]
