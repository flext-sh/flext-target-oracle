"""FLEXT Target Oracle Types - Domain-specific Singer Oracle target type definitions.

This module provides Singer Oracle target-specific type definitions extending FlextCore.Types.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends FlextCore.Types properly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Literal

from flext_core import FlextCore

# =============================================================================
# TARGET ORACLE-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for Singer Oracle target operations
# =============================================================================


# Singer Oracle target domain TypeVars
class FlextTargetOracleTypes(FlextCore.Types):
    """Singer Oracle target-specific type definitions extending FlextCore.Types.

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
            str, str | int | bool | dict[str, FlextCore.Types.ConfigValue]
        ]
        type StreamConfiguration = dict[
            str, str | bool | dict[str, FlextCore.Types.JsonValue]
        ]
        type MessageProcessing = dict[
            str, str | list[dict[str, FlextCore.Types.JsonValue]]
        ]
        type RecordHandling = dict[
            str, str | dict[str, FlextCore.Types.JsonValue] | bool
        ]
        type StateManagement = dict[str, str | dict[str, FlextCore.Types.JsonValue]]
        type BatchProcessing = dict[
            str, str | int | dict[str, FlextCore.Types.JsonValue]
        ]

    # =========================================================================
    # ORACLE DATABASE TYPES - Complex Oracle database operation types
    # =========================================================================

    class OracleDatabase:
        """Oracle database operation complex types."""

        type DatabaseConfiguration = dict[
            str, str | int | bool | dict[str, FlextCore.Types.ConfigValue]
        ]
        type ConnectionManagement = dict[
            str, str | int | dict[str, FlextCore.Types.JsonValue]
        ]
        type SessionSettings = dict[
            str, str | bool | dict[str, FlextCore.Types.ConfigValue]
        ]
        type TransactionControl = dict[str, str | bool | FlextCore.Types.Dict]
        type DatabaseMetadata = dict[str, str | dict[str, FlextCore.Types.JsonValue]]
        type PerformanceSettings = dict[str, int | float | FlextCore.Types.Dict]

    # =========================================================================
    # ORACLE TABLE TYPES - Complex Oracle table and schema types
    # =========================================================================

    class OracleTable:
        """Oracle table and schema complex types."""

        type TableConfiguration = dict[
            str, str | bool | dict[str, FlextCore.Types.ConfigValue]
        ]
        type SchemaDefinition = dict[
            str, str | FlextCore.Types.StringList | dict[str, FlextCore.Types.JsonValue]
        ]
        type ColumnMapping = dict[str, str | dict[str, FlextCore.Types.JsonValue]]
        type IndexConfiguration = dict[
            str, str | FlextCore.Types.StringList | FlextCore.Types.Dict
        ]
        type ConstraintDefinition = dict[
            str, str | dict[str, FlextCore.Types.JsonValue]
        ]
        type TablespaceSettings = dict[str, str | int | FlextCore.Types.Dict]

    # =========================================================================
    # ORACLE SQL TYPES - Complex Oracle SQL operation types
    # =========================================================================

    class OracleSql:
        """Oracle SQL operation complex types."""

        type SqlConfiguration = dict[
            str, str | bool | int | dict[str, FlextCore.Types.ConfigValue]
        ]
        type QueryExecution = dict[str, str | dict[str, FlextCore.Types.JsonValue]]
        type BulkOperations = dict[
            str, str | int | FlextCore.Types.StringList | FlextCore.Types.Dict
        ]
        type PreparedStatements = dict[str, str | dict[str, FlextCore.Types.JsonValue]]
        type SqlOptimization = dict[
            str, bool | str | dict[str, FlextCore.Types.ConfigValue]
        ]
        type ResultSetHandling = dict[str, str | int | FlextCore.Types.Dict]

    # =========================================================================
    # ORACLE PERFORMANCE TYPES - Complex Oracle performance optimization types
    # =========================================================================

    class OraclePerformance:
        """Oracle performance optimization complex types."""

        type PerformanceConfiguration = dict[
            str, str | int | dict[str, FlextCore.Types.ConfigValue]
        ]
        type ConnectionPooling = dict[
            str, int | bool | dict[str, FlextCore.Types.JsonValue]
        ]
        type BulkLoadOptimization = dict[str, str | int | FlextCore.Types.Dict]
        type QueryOptimization = dict[str, str | dict[str, FlextCore.Types.JsonValue]]
        type CachingStrategy = dict[
            str, bool | str | dict[str, FlextCore.Types.ConfigValue]
        ]
        type ParallelProcessing = dict[str, int | str | FlextCore.Types.Dict]

    # =========================================================================
    # DATA TRANSFORMATION TYPES - Complex data transformation types
    # =========================================================================

    class DataTransformation:
        """Data transformation complex types."""

        type TransformationConfiguration = dict[
            str, str | bool | dict[str, FlextCore.Types.ConfigValue]
        ]
        type FieldMapping = dict[
            str, str | FlextCore.Types.StringList | FlextCore.Types.Dict
        ]
        type DataValidation = dict[str, str | dict[str, FlextCore.Types.JsonValue]]
        type TypeConversion = dict[str, bool | str | FlextCore.Types.Dict]
        type FilteringRules = dict[str, str | dict[str, FlextCore.Types.JsonValue]]
        type TransformationResult = dict[str, dict[str, FlextCore.Types.JsonValue]]

    # =========================================================================
    # STREAM PROCESSING TYPES - Complex stream handling types
    # =========================================================================

    class StreamProcessing:
        """Stream processing complex types."""

        type StreamConfiguration = dict[
            str, str | bool | int | dict[str, FlextCore.Types.ConfigValue]
        ]
        type StreamMetadata = dict[str, str | dict[str, FlextCore.Types.JsonValue]]
        type StreamRecord = dict[str, FlextCore.Types.JsonValue | FlextCore.Types.Dict]
        type StreamState = dict[str, str | int | dict[str, FlextCore.Types.JsonValue]]
        type StreamBookmark = dict[str, str | int | FlextCore.Types.Dict]
        type StreamSchema = dict[str, str | dict[str, FlextCore.Types.JsonValue] | bool]

    # =========================================================================
    # ERROR HANDLING TYPES - Complex error management types
    # =========================================================================

    class ErrorHandling:
        """Error handling complex types."""

        type ErrorConfiguration = dict[
            str, bool | str | int | dict[str, FlextCore.Types.ConfigValue]
        ]
        type ErrorRecovery = dict[str, str | bool | FlextCore.Types.Dict]
        type ErrorReporting = dict[
            str, str | int | dict[str, FlextCore.Types.JsonValue]
        ]
        type ErrorClassification = dict[str, str | int | FlextCore.Types.Dict]
        type ErrorMetrics = dict[
            str, int | float | dict[str, FlextCore.Types.JsonValue]
        ]
        type ErrorTracking = list[
            dict[str, str | int | dict[str, FlextCore.Types.JsonValue]]
        ]

    # =========================================================================
    # SINGER TARGET ORACLE PROJECT TYPES - Domain-specific project types extending FlextCore.Types
    # =========================================================================

    class Project(FlextCore.Types.Project):
        """Singer Target Oracle-specific project types extending FlextCore.Types.Project.

        Adds Singer target Oracle-specific project types while inheriting
        generic types from FlextCore.Types. Follows domain separation principle:
        Singer target Oracle domain owns Oracle loading and Singer protocol-specific types.
        """

        # Singer target Oracle-specific project types extending the generic ones
        type ProjectType = Literal[
            # Generic types inherited from FlextCore.Types.Project
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
        type SingerTargetOracleProjectConfig = dict[
            str, FlextCore.Types.ConfigValue | object
        ]
        type OracleLoaderConfig = dict[
            str, str | int | bool | FlextCore.Types.StringList
        ]
        type SingerProtocolConfig = dict[str, bool | str | FlextCore.Types.Dict]
        type TargetOraclePipelineConfig = dict[
            str, FlextCore.Types.ConfigValue | object
        ]


# =============================================================================
# PUBLIC API EXPORTS - Singer Oracle target TypeVars and types
# =============================================================================

__all__: FlextCore.Types.StringList = [
    "FlextTargetOracleTypes",
]
