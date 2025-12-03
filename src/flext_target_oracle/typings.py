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

from flext_core import t

# =============================================================================
# TARGET ORACLE-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for Singer Oracle target operations
# =============================================================================


# Singer Oracle target domain TypeVars
class FlextTargetOracleTypes(t):
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

        type TargetConfiguration = dict[str, str | int | bool | dict[str, object]]
        type StreamConfiguration = dict[str, str | bool | dict[str, t.JsonValue]]
        type MessageProcessing = dict[str, str | list[dict[str, t.JsonValue]]]
        type RecordHandling = dict[str, str | dict[str, t.JsonValue] | bool]
        type StateManagement = dict[str, str | dict[str, t.JsonValue]]
        type BatchProcessing = dict[str, str | int | dict[str, t.JsonValue]]

    # =========================================================================
    # ORACLE DATABASE TYPES - Complex Oracle database operation types
    # =========================================================================

    class OracleDatabase:
        """Oracle database operation complex types."""

        type DatabaseConfiguration = dict[str, str | int | bool | dict[str, object]]
        type ConnectionManagement = dict[str, str | int | dict[str, t.JsonValue]]
        type SessionSettings = dict[str, str | bool | dict[str, object]]
        type TransactionControl = dict[str, str | bool | dict[str, object]]
        type DatabaseMetadata = dict[str, str | dict[str, t.JsonValue]]
        type PerformanceSettings = dict[str, int | float | dict[str, object]]

    # =========================================================================
    # ORACLE TABLE TYPES - Complex Oracle table and schema types
    # =========================================================================

    class OracleTable:
        """Oracle table and schema complex types."""

        type TableConfiguration = dict[str, str | bool | dict[str, object]]
        type SchemaDefinition = dict[str, str | list[str] | dict[str, t.JsonValue]]
        type ColumnMapping = dict[str, str | dict[str, t.JsonValue]]
        type IndexConfiguration = dict[str, str | list[str] | dict[str, object]]
        type ConstraintDefinition = dict[str, str | dict[str, t.JsonValue]]
        type TablespaceSettings = dict[str, str | int | dict[str, object]]

    # =========================================================================
    # ORACLE SQL TYPES - Complex Oracle SQL operation types
    # =========================================================================

    class OracleSql:
        """Oracle SQL operation complex types."""

        type SqlConfiguration = dict[str, str | bool | int | dict[str, object]]
        type QueryExecution = dict[str, str | dict[str, t.JsonValue]]
        type BulkOperations = dict[str, str | int | list[str] | dict[str, object]]
        type PreparedStatements = dict[str, str | dict[str, t.JsonValue]]
        type SqlOptimization = dict[str, bool | str | dict[str, object]]
        type ResultSetHandling = dict[str, str | int | dict[str, object]]

    # =========================================================================
    # ORACLE PERFORMANCE TYPES - Complex Oracle performance optimization types
    # =========================================================================

    class OraclePerformance:
        """Oracle performance optimization complex types."""

        type PerformanceConfiguration = dict[str, str | int | dict[str, object]]
        type ConnectionPooling = dict[str, int | bool | dict[str, t.JsonValue]]
        type BulkLoadOptimization = dict[str, str | int | dict[str, object]]
        type QueryOptimization = dict[str, str | dict[str, t.JsonValue]]
        type CachingStrategy = dict[str, bool | str | dict[str, object]]
        type ParallelProcessing = dict[str, int | str | dict[str, object]]

    # =========================================================================
    # DATA TRANSFORMATION TYPES - Complex data transformation types
    # =========================================================================

    class DataTransformation:
        """Data transformation complex types."""

        type TransformationConfiguration = dict[str, str | bool | dict[str, object]]
        type FieldMapping = dict[str, str | list[str] | dict[str, object]]
        type DataValidation = dict[str, str | dict[str, t.JsonValue]]
        type TypeConversion = dict[str, bool | str | dict[str, object]]
        type FilteringRules = dict[str, str | dict[str, t.JsonValue]]
        type TransformationResult = dict[str, dict[str, t.JsonValue]]

    # =========================================================================
    # STREAM PROCESSING TYPES - Complex stream handling types
    # =========================================================================

    class StreamProcessing:
        """Stream processing complex types."""

        type StreamConfiguration = dict[str, str | bool | int | dict[str, object]]
        type StreamMetadata = dict[str, str | dict[str, t.JsonValue]]
        type StreamRecord = dict[str, t.JsonValue | dict[str, object]]
        type StreamState = dict[str, str | int | dict[str, t.JsonValue]]
        type StreamBookmark = dict[str, str | int | dict[str, object]]
        type StreamSchema = dict[str, str | dict[str, t.JsonValue] | bool]

    # =========================================================================
    # ERROR HANDLING TYPES - Complex error management types
    # =========================================================================

    class ErrorHandling:
        """Error handling complex types."""

        type ErrorConfiguration = dict[str, bool | str | int | dict[str, object]]
        type ErrorRecovery = dict[str, str | bool | dict[str, object]]
        type ErrorReporting = dict[str, str | int | dict[str, t.JsonValue]]
        type ErrorClassification = dict[str, str | int | dict[str, object]]
        type ErrorMetrics = dict[str, int | float | dict[str, t.JsonValue]]
        type ErrorTracking = list[dict[str, str | int | dict[str, t.JsonValue]]]

    # =========================================================================
    # SINGER TARGET ORACLE PROJECT TYPES - Domain-specific project types extending t
    # =========================================================================

    class Project(t):
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
        type SingerTargetOracleProjectConfig = dict[str, object]
        type OracleLoaderConfig = dict[str, str | int | bool | list[str]]
        type SingerProtocolConfig = dict[str, bool | str | dict[str, object]]
        type TargetOraclePipelineConfig = dict[str, object]


# =============================================================================
# PUBLIC API EXPORTS - Singer Oracle target TypeVars and types
# =============================================================================

__all__: list[str] = [
    "FlextTargetOracleTypes",
]
