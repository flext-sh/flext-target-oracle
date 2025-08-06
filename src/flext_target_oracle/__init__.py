"""FLEXT Target Oracle - Production-Grade Singer Target for Oracle Database.

This module provides a complete Singer specification-compliant target for Oracle
Database data loading, built using FLEXT ecosystem patterns and enterprise-grade
reliability standards.

The target implements Clean Architecture principles with Domain-Driven Design
patterns, leveraging the FLEXT ecosystem's foundational components for consistent
error handling, configuration management, and database operations.

Key Components:
    FlextOracleTarget: Main Singer target implementation with async processing
    FlextOracleTargetConfig: Type-safe configuration with domain validation
    LoadMethod: Enumeration of supported Oracle loading strategies
    Exception Hierarchy: Comprehensive error handling with context preservation

Architecture Integration:
    Built on flext-core foundations (FlextResult, FlextValueObject patterns)
    Integrates with flext-meltano for Singer SDK compliance
    Uses flext-db-oracle for production-grade Oracle connectivity
    Follows railway-oriented programming for error handling

Example:
    Basic target initialization and configuration:

    >>> from flext_target_oracle import FlextOracleTarget, FlextOracleTargetConfig
    >>> config = FlextOracleTargetConfig(
    ...     oracle_host="localhost",
    ...     oracle_service="XE",
    ...     oracle_user="target_user",
    ...     oracle_password="secure_password",
    ... )
    >>> target = FlextOracleTarget(config)
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

# === FLEXT-MELTANO COMPLETE INTEGRATION ===
# Re-export ALL flext-meltano facilities for full ecosystem integration
from flext_meltano import (
    # Core Singer SDK classes (centralized from flext-meltano)
    Stream,
    Tap,
    Target,
    Sink,
    BatchSink,
    SQLSink,
    
    # Enterprise services from flext-meltano.base
    FlextMeltanoTargetService,
    FlextMeltanoBaseService,
    create_meltano_target_service,
    
    # Configuration and validation
    FlextMeltanoConfig,
    FlextMeltanoEvent,
    
    # Singer typing utilities (centralized)
    singer_typing,
    
    # Bridge integration
    FlextMeltanoBridge,
    
    # Testing utilities
    get_tap_test_class,
    
    # Authentication patterns
    OAuthAuthenticator,
    
    # Typing definitions
    PropertiesList,
    Property,
)

# Import FLEXT core patterns for ecosystem consistency
from flext_core import FlextResult

# Import local implementations
from flext_target_oracle.config import FlextOracleTargetConfig, LoadMethod
from flext_target_oracle.exceptions import (
    FlextOracleTargetAuthenticationError,
    FlextOracleTargetConnectionError,
    FlextOracleTargetError,
    FlextOracleTargetProcessingError,
    FlextOracleTargetSchemaError,
)
from flext_target_oracle.observability import (
    FlextOracleError,
    FlextOracleObs,
    configure_oracle_observability,
)
from flext_target_oracle.target import FlextOracleTarget

__version__ = "0.9.0"
"""Current version - pre-production with known critical issues."""

__all__: list[str] = [
    # === PRIMARY TARGET CLASSES ===
    "FlextOracleTarget",
    "FlextOracleTargetConfig",
    "LoadMethod",
    
    # === FLEXT-MELTANO COMPLETE RE-EXPORTS ===
    # Singer SDK core classes
    "Stream",
    "Tap",
    "Target", 
    "Sink",
    "BatchSink",
    "SQLSink",
    
    # Enterprise services
    "FlextMeltanoTargetService",
    "FlextMeltanoBaseService",
    "create_meltano_target_service",
    
    # Configuration patterns
    "FlextMeltanoConfig",
    "FlextMeltanoEvent",
    
    # Singer typing
    "singer_typing",
    "PropertiesList",
    "Property",
    
    # Bridge integration
    "FlextMeltanoBridge",
    
    # Testing
    "get_tap_test_class",
    
    # Authentication
    "OAuthAuthenticator",
    
    # === OBSERVABILITY ===
    "FlextOracleError",
    "FlextOracleObs", 
    "configure_oracle_observability",
    
    # === EXCEPTION HIERARCHY ===
    "FlextOracleTargetAuthenticationError",
    "FlextOracleTargetConnectionError",
    "FlextOracleTargetError",
    "FlextOracleTargetProcessingError",
    "FlextOracleTargetSchemaError",
    
    # === FLEXT-CORE RE-EXPORTS ===
    "FlextResult",
    
    # === METADATA ===
    "__version__",
]
