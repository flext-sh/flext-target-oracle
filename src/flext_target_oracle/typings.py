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

from flext_db_oracle.typings import FlextDbOracleTypes
from flext_meltano import FlextMeltanoTypes


class FlextTargetOracleTypes(FlextMeltanoTypes, FlextDbOracleTypes):
    """Singer Oracle target-specific type definitions extending t.

    Domain-specific type system for Singer Oracle target operations.
    Contains ONLY complex Oracle target-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    class TargetOracle:
        """Singer target protocol complex types."""

        type TargetConfiguration = dict[
            str, str | int | bool | dict[str, t.ContainerValue]
        ]
        type StreamConfiguration = dict[str, str | bool | dict[str, t.ContainerValue]]
        type MessageProcessing = dict[str, str | list[dict[str, t.ContainerValue]]]
        type RecordHandling = dict[str, str | dict[str, t.ContainerValue] | bool]
        type StateManagement = dict[str, str | dict[str, t.ContainerValue]]
        type BatchProcessing = dict[str, str | int | dict[str, t.ContainerValue]]

    class OracleDatabase:
        """Oracle database operation complex types."""

        type DatabaseConfiguration = dict[
            str, str | int | bool | dict[str, t.ContainerValue]
        ]
        type ConnectionManagement = dict[str, str | int | dict[str, t.ContainerValue]]
        type SessionSettings = dict[str, str | bool | dict[str, t.ContainerValue]]
        type TransactionControl = dict[str, str | bool | dict[str, t.ContainerValue]]
        type DatabaseMetadata = dict[str, str | dict[str, t.ContainerValue]]
        type PerformanceSettings = dict[str, int | float | dict[str, t.ContainerValue]]

    class OracleTable:
        """Oracle table and schema complex types."""

        type TableConfiguration = dict[str, str | bool | dict[str, t.ContainerValue]]
        type SchemaDefinition = dict[str, str | list[str] | dict[str, t.ContainerValue]]
        type ColumnMapping = dict[str, str | dict[str, t.ContainerValue]]
        type IndexConfiguration = dict[
            str, str | list[str] | dict[str, t.ContainerValue]
        ]
        type ConstraintDefinition = dict[str, str | dict[str, t.ContainerValue]]
        type TablespaceSettings = dict[str, str | int | dict[str, t.ContainerValue]]

    class OracleSql:
        """Oracle SQL operation complex types."""

        type SqlConfiguration = dict[
            str, str | bool | int | dict[str, t.ContainerValue]
        ]
        type QueryExecution = dict[str, str | dict[str, t.ContainerValue]]
        type BulkOperations = dict[
            str, str | int | list[str] | dict[str, t.ContainerValue]
        ]
        type PreparedStatements = dict[str, str | dict[str, t.ContainerValue]]
        type SqlOptimization = dict[str, bool | str | dict[str, t.ContainerValue]]
        type ResultSetHandling = dict[str, str | int | dict[str, t.ContainerValue]]

    class OraclePerformance:
        """Oracle performance optimization complex types."""

        type PerformanceConfiguration = dict[
            str, str | int | dict[str, t.ContainerValue]
        ]
        type ConnectionPooling = dict[str, int | bool | dict[str, t.ContainerValue]]
        type BulkLoadOptimization = dict[str, str | int | dict[str, t.ContainerValue]]
        type QueryOptimization = dict[str, str | dict[str, t.ContainerValue]]
        type CachingStrategy = dict[str, bool | str | dict[str, t.ContainerValue]]
        type ParallelProcessing = dict[str, int | str | dict[str, t.ContainerValue]]

    class DataTransformation:
        """Data transformation complex types."""

        type TransformationConfiguration = dict[
            str, str | bool | dict[str, t.ContainerValue]
        ]
        type FieldMapping = dict[str, str | list[str] | dict[str, t.ContainerValue]]
        type DataValidation = dict[str, str | dict[str, t.ContainerValue]]
        type TypeConversion = dict[str, bool | str | dict[str, t.ContainerValue]]
        type FilteringRules = dict[str, str | dict[str, t.ContainerValue]]
        type TransformationResult = dict[str, dict[str, t.ContainerValue]]

    class StreamProcessing:
        """Stream processing complex types."""

        type StreamConfiguration = dict[
            str, str | bool | int | dict[str, t.ContainerValue]
        ]
        type StreamMetadata = dict[str, str | dict[str, t.ContainerValue]]
        type StreamRecord = dict[str, t.ContainerValue]
        type StreamState = dict[str, str | int | dict[str, t.ContainerValue]]
        type StreamBookmark = dict[str, str | int | dict[str, t.ContainerValue]]
        type StreamSchema = dict[str, str | dict[str, t.ContainerValue] | bool]

    class SingerMessage:
        """Singer protocol message complex types."""

        type SchemaMessage = dict[str, str | list[str] | dict[str, t.ContainerValue]]
        type RecordMessage = dict[str, str | dict[str, t.ContainerValue]]
        type StateMessage = dict[str, str | dict[str, t.ContainerValue]]
        type ActivateVersionMessage = dict[str, str | int]

    class ErrorHandling:
        """Error handling complex types."""

        type ErrorConfiguration = dict[
            str, bool | str | int | dict[str, t.ContainerValue]
        ]
        type ErrorRecovery = dict[str, str | bool | dict[str, t.ContainerValue]]
        type ErrorReporting = dict[str, str | int | dict[str, t.ContainerValue]]
        type ErrorClassification = dict[str, str | int | dict[str, t.ContainerValue]]
        type ErrorMetrics = dict[str, int | float | dict[str, t.ContainerValue]]
        type ErrorTracking = list[dict[str, str | int | dict[str, t.ContainerValue]]]

    class Core:
        """Core convenience type aliases for common patterns.

        Provides commonly used type aliases for consistency across the codebase.
        These are simple aliases but are used extensively, so provided for convenience.
        Access parent core types via inheritance from FlextTargetOracleTypes.
        """

        type Dict = dict[str, t.ContainerValue]
        "Type alias for generic dictionary (attribute name to value mapping)."


t = FlextTargetOracleTypes
__all__ = ["FlextTargetOracleTypes", "t"]
