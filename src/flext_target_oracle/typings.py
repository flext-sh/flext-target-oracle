"""FLEXT Target Oracle Types - Domain-specific Singer Oracle target type definitions.

This module provides Singer Oracle target-specific type definitions extending t.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends t properly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Literal

from flext_core import FlextTypes

# =============================================================================
# TARGET ORACLE-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for Singer Oracle target operations
# =============================================================================


# Singer Oracle target domain TypeVars
class FlextTargetOracleTypes(FlextTypes):
    """Singer Oracle target-specific type definitions extending t.

    Domain-specific type system for Singer Oracle target operations.
    Contains ONLY complex Oracle target-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    # =========================================================================
    # SINGER TARGET TYPES - Complex Singer target protocol types
    # =========================================================================

    class SingerTarget:
        """Singer target protocol complex types."""

        type TargetConfiguration = dict[
            str, str | int | bool | dict[str, FlextTypes.GeneralValueType]
        ]
        type StreamConfiguration = dict[
            str,
            str | bool | dict[str, FlextTypes.JsonValue],
        ]
        type MessageProcessing = dict[str, str | list[dict[str, FlextTypes.JsonValue]]]
        type RecordHandling = dict[str, str | dict[str, FlextTypes.JsonValue] | bool]
        type StateManagement = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type BatchProcessing = dict[str, str | int | dict[str, FlextTypes.JsonValue]]

    # =========================================================================
    # ORACLE DATABASE TYPES - Complex Oracle database operation types
    # =========================================================================

    class OracleDatabase:
        """Oracle database operation complex types."""

        type DatabaseConfiguration = dict[
            str, str | int | bool | dict[str, FlextTypes.GeneralValueType]
        ]
        type ConnectionManagement = dict[
            str,
            str | int | dict[str, FlextTypes.JsonValue],
        ]
        type SessionSettings = dict[
            str, str | bool | dict[str, FlextTypes.GeneralValueType]
        ]
        type TransactionControl = dict[
            str, str | bool | dict[str, FlextTypes.GeneralValueType]
        ]
        type DatabaseMetadata = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type PerformanceSettings = dict[
            str, int | float | dict[str, FlextTypes.GeneralValueType]
        ]

    # =========================================================================
    # ORACLE TABLE TYPES - Complex Oracle table and schema types
    # =========================================================================

    class OracleTable:
        """Oracle table and schema complex types."""

        type TableConfiguration = dict[
            str, str | bool | dict[str, FlextTypes.GeneralValueType]
        ]
        type SchemaDefinition = dict[
            str,
            str | list[str] | dict[str, FlextTypes.JsonValue],
        ]
        type ColumnMapping = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type IndexConfiguration = dict[
            str, str | list[str] | dict[str, FlextTypes.GeneralValueType]
        ]
        type ConstraintDefinition = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type TablespaceSettings = dict[
            str, str | int | dict[str, FlextTypes.GeneralValueType]
        ]

    # =========================================================================
    # ORACLE SQL TYPES - Complex Oracle SQL operation types
    # =========================================================================

    class OracleSql:
        """Oracle SQL operation complex types."""

        type SqlConfiguration = dict[
            str, str | bool | int | dict[str, FlextTypes.GeneralValueType]
        ]
        type QueryExecution = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type BulkOperations = dict[
            str, str | int | list[str] | dict[str, FlextTypes.GeneralValueType]
        ]
        type PreparedStatements = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type SqlOptimization = dict[
            str, bool | str | dict[str, FlextTypes.GeneralValueType]
        ]
        type ResultSetHandling = dict[
            str, str | int | dict[str, FlextTypes.GeneralValueType]
        ]

    # =========================================================================
    # ORACLE PERFORMANCE TYPES - Complex Oracle performance optimization types
    # =========================================================================

    class OraclePerformance:
        """Oracle performance optimization complex types."""

        type PerformanceConfiguration = dict[
            str, str | int | dict[str, FlextTypes.GeneralValueType]
        ]
        type ConnectionPooling = dict[str, int | bool | dict[str, FlextTypes.JsonValue]]
        type BulkLoadOptimization = dict[
            str, str | int | dict[str, FlextTypes.GeneralValueType]
        ]
        type QueryOptimization = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type CachingStrategy = dict[
            str, bool | str | dict[str, FlextTypes.GeneralValueType]
        ]
        type ParallelProcessing = dict[
            str, int | str | dict[str, FlextTypes.GeneralValueType]
        ]

    # =========================================================================
    # DATA TRANSFORMATION TYPES - Complex data transformation types
    # =========================================================================

    class DataTransformation:
        """Data transformation complex types."""

        type TransformationConfiguration = dict[
            str, str | bool | dict[str, FlextTypes.GeneralValueType]
        ]
        type FieldMapping = dict[
            str, str | list[str] | dict[str, FlextTypes.GeneralValueType]
        ]
        type DataValidation = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type TypeConversion = dict[
            str, bool | str | dict[str, FlextTypes.GeneralValueType]
        ]
        type FilteringRules = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type TransformationResult = dict[str, dict[str, FlextTypes.JsonValue]]

    # =========================================================================
    # STREAM PROCESSING TYPES - Complex stream handling types
    # =========================================================================

    class StreamProcessing:
        """Stream processing complex types."""

        type StreamConfiguration = dict[
            str, str | bool | int | dict[str, FlextTypes.GeneralValueType]
        ]
        type StreamMetadata = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type StreamRecord = dict[
            str, FlextTypes.JsonValue | dict[str, FlextTypes.GeneralValueType]
        ]
        type StreamState = dict[str, str | int | dict[str, FlextTypes.JsonValue]]
        type StreamBookmark = dict[
            str, str | int | dict[str, FlextTypes.GeneralValueType]
        ]
        type StreamSchema = dict[str, str | dict[str, FlextTypes.JsonValue] | bool]

    class SingerMessage:
        """Singer protocol message complex types."""

        type SchemaMessage = dict[
            str,
            str | list[str] | dict[str, FlextTypes.JsonValue],
        ]
        type RecordMessage = dict[
            str,
            str | dict[str, FlextTypes.JsonValue],
        ]
        type StateMessage = dict[
            str,
            str | dict[str, FlextTypes.JsonValue],
        ]
        type ActivateVersionMessage = dict[str, str | int]

    # =========================================================================
    # ERROR HANDLING TYPES - Complex error management types
    # =========================================================================

    class ErrorHandling:
        """Error handling complex types."""

        type ErrorConfiguration = dict[
            str, bool | str | int | dict[str, FlextTypes.GeneralValueType]
        ]
        type ErrorRecovery = dict[
            str, str | bool | dict[str, FlextTypes.GeneralValueType]
        ]
        type ErrorReporting = dict[str, str | int | dict[str, FlextTypes.JsonValue]]
        type ErrorClassification = dict[
            str, str | int | dict[str, FlextTypes.GeneralValueType]
        ]
        type ErrorMetrics = dict[str, int | float | dict[str, FlextTypes.JsonValue]]
        type ErrorTracking = list[
            dict[str, str | int | dict[str, FlextTypes.JsonValue]]
        ]

    # =========================================================================
    # CORE COMMONLY USED TYPES - Convenience aliases for common patterns
    # =========================================================================

    class Core:
        """Core convenience type aliases for common patterns.

        Provides commonly used type aliases for consistency across the codebase.
        These are simple aliases but are used extensively, so provided for convenience.
        Access parent core types via inheritance from FlextTargetOracleTypes.
        """

        # Common dictionary types
        type Dict = dict[str, FlextTypes.GeneralValueType]
        """Type alias for generic dictionary (attribute name to value mapping)."""

    # =========================================================================
    # SINGER TARGET ORACLE PROJECT TYPES - Domain-specific project types extending t
    # =========================================================================

    class Project:
        """Singer Target Oracle-specific project types extending t.

        Adds Singer target Oracle-specific project types while inheriting
        generic types from t. Follows domain separation principle:
        Singer target Oracle domain owns Oracle loading and Singer protocol-specific types.
        """

        # Singer target Oracle-specific project types extending the generic ones
        type ProjectType = Literal[
            # Generic types inherited from t
            "library",
            "application",
            "service",
            # Singer target Oracle-specific types
            "singer-target",
            "oracle-loader",
            "database-loader",
            "singer-target-oracle",
            "target-oracle",
            "oracle-connector",
            "database-connector",
            "singer-protocol",
            "oracle-integration",
            "database-service",
            "oracle-target",
            "singer-stream",
            "etl-target",
            "data-pipeline",
            "oracle-sink",
            "singer-integration",
        ]

        # Singer target Oracle-specific project configurations
        type SingerTargetOracleProjectConfig = dict[str, FlextTypes.GeneralValueType]
        type OracleLoaderConfig = dict[str, str | int | bool | list[str]]
        type SingerProtocolConfig = dict[
            str, bool | str | dict[str, FlextTypes.GeneralValueType]
        ]
        type TargetOraclePipelineConfig = dict[str, FlextTypes.GeneralValueType]

    class TargetOracle:
        """Target Oracle types namespace for cross-project access.

        Provides organized access to all Target Oracle types for other FLEXT projects.
        Usage: Other projects can reference `t.TargetOracle.SingerTarget.*`, `t.TargetOracle.Project.*`, etc.
        This enables consistent namespace patterns for cross-project type access.

        Examples:
            from flext_target_oracle.typings import t
            config: t.TargetOracle.Project.SingerTargetOracleProjectConfig = ...
            message: t.TargetOracle.SingerTarget.TargetConfiguration = ...

        Note: Namespace composition via inheritance - no aliases needed.
        Access parent namespaces directly through inheritance.

        """


# Alias for simplified usage
t = FlextTargetOracleTypes

# Namespace composition via class inheritance
# TargetOracle namespace provides access to nested classes through inheritance
# Access patterns:
# - t.TargetOracle.* for Target Oracle-specific types
# - t.Project.* for project types
# - t.Core.* for core types (inherited from parent)

# =============================================================================
# PUBLIC API EXPORTS - Singer Oracle target TypeVars and types
# =============================================================================

__all__ = [
    "FlextTargetOracleTypes",
    "t",
]
