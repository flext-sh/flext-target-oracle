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

        type TargetConfiguration = dict[str, str | int | bool | dict[str, object]]
        type StreamConfiguration = dict[str, str | bool | dict[str, object]]
        type MessageProcessing = dict[str, str | list[dict[str, object]]]
        type RecordHandling = dict[str, str | dict[str, object] | bool]
        type StateManagement = dict[str, str | dict[str, object]]
        type BatchProcessing = dict[str, str | int | dict[str, object]]

    class OracleDatabase:
        """Oracle database operation complex types."""

        type DatabaseConfiguration = dict[str, str | int | bool | dict[str, object]]
        type ConnectionManagement = dict[str, str | int | dict[str, object]]
        type SessionSettings = dict[str, str | bool | dict[str, object]]
        type TransactionControl = dict[str, str | bool | dict[str, object]]
        type DatabaseMetadata = dict[str, str | dict[str, object]]
        type PerformanceSettings = dict[str, int | float | dict[str, object]]

    class OracleTable:
        """Oracle table and schema complex types."""

        type TableConfiguration = dict[str, str | bool | dict[str, object]]
        type SchemaDefinition = dict[str, str | list[str] | dict[str, object]]
        type ColumnMapping = dict[str, str | dict[str, object]]
        type IndexConfiguration = dict[str, str | list[str] | dict[str, object]]
        type ConstraintDefinition = dict[str, str | dict[str, object]]
        type TablespaceSettings = dict[str, str | int | dict[str, object]]

    class OracleSql:
        """Oracle SQL operation complex types."""

        type SqlConfiguration = dict[str, str | bool | int | dict[str, object]]
        type QueryExecution = dict[str, str | dict[str, object]]
        type BulkOperations = dict[str, str | int | list[str] | dict[str, object]]
        type PreparedStatements = dict[str, str | dict[str, object]]
        type SqlOptimization = dict[str, bool | str | dict[str, object]]
        type ResultSetHandling = dict[str, str | int | dict[str, object]]

    class OraclePerformance:
        """Oracle performance optimization complex types."""

        type PerformanceConfiguration = dict[str, str | int | dict[str, object]]
        type ConnectionPooling = dict[str, int | bool | dict[str, object]]
        type BulkLoadOptimization = dict[str, str | int | dict[str, object]]
        type QueryOptimization = dict[str, str | dict[str, object]]
        type CachingStrategy = dict[str, bool | str | dict[str, object]]
        type ParallelProcessing = dict[str, int | str | dict[str, object]]

    class DataTransformation:
        """Data transformation complex types."""

        type TransformationConfiguration = dict[str, str | bool | dict[str, object]]
        type FieldMapping = dict[str, str | list[str] | dict[str, object]]
        type DataValidation = dict[str, str | dict[str, object]]
        type TypeConversion = dict[str, bool | str | dict[str, object]]
        type FilteringRules = dict[str, str | dict[str, object]]
        type TransformationResult = dict[str, dict[str, object]]

    class StreamProcessing:
        """Stream processing complex types."""

        type StreamConfiguration = dict[str, str | bool | int | dict[str, object]]
        type StreamMetadata = dict[str, str | dict[str, object]]
        type StreamRecord = dict[str, object | dict[str, object]]
        type StreamState = dict[str, str | int | dict[str, object]]
        type StreamBookmark = dict[str, str | int | dict[str, object]]
        type StreamSchema = dict[str, str | dict[str, object] | bool]

    class SingerMessage:
        """Singer protocol message complex types."""

        type SchemaMessage = dict[str, str | list[str] | dict[str, object]]
        type RecordMessage = dict[str, str | dict[str, object]]
        type StateMessage = dict[str, str | dict[str, object]]
        type ActivateVersionMessage = dict[str, str | int]

    class ErrorHandling:
        """Error handling complex types."""

        type ErrorConfiguration = dict[str, bool | str | int | dict[str, object]]
        type ErrorRecovery = dict[str, str | bool | dict[str, object]]
        type ErrorReporting = dict[str, str | int | dict[str, object]]
        type ErrorClassification = dict[str, str | int | dict[str, object]]
        type ErrorMetrics = dict[str, int | float | dict[str, object]]
        type ErrorTracking = list[dict[str, str | int | dict[str, object]]]

    class Core:
        """Core convenience type aliases for common patterns.

        Provides commonly used type aliases for consistency across the codebase.
        These are simple aliases but are used extensively, so provided for convenience.
        Access parent core types via inheritance from FlextTargetOracleTypes.
        """

        type Dict = dict[str, object]
        "Type alias for generic dictionary (attribute name to value mapping)."


t = FlextTargetOracleTypes
__all__ = ["FlextTargetOracleTypes", "t"]
