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

from collections.abc import Mapping, Sequence

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

        type TargetConfiguration = Mapping[
            str,
            t.Scalar | t.ContainerValueMapping,
        ]
        type StreamConfiguration = Mapping[str, str | bool | t.ContainerValueMapping]
        type MessageProcessing = Mapping[str, str | Sequence[t.ContainerValueMapping]]
        type RecordHandling = Mapping[str, str | t.ContainerValueMapping | bool]
        type StateManagement = Mapping[str, str | t.ContainerValueMapping]
        type BatchProcessing = Mapping[str, str | int | t.ContainerValueMapping]

    class OracleDatabase:
        """Oracle database operation complex types."""

        type DatabaseConfiguration = Mapping[
            str,
            t.Scalar | t.ContainerValueMapping,
        ]
        type ConnectionManagement = Mapping[str, str | int | t.ContainerValueMapping]
        type SessionSettings = Mapping[str, str | bool | t.ContainerValueMapping]
        type TransactionControl = Mapping[str, str | bool | t.ContainerValueMapping]
        type DatabaseMetadata = Mapping[str, str | t.ContainerValueMapping]
        type PerformanceSettings = Mapping[str, int | float | t.ContainerValueMapping]

    class OracleTable:
        """Oracle table and schema complex types."""

        type TableConfiguration = Mapping[str, str | bool | t.ContainerValueMapping]
        type SchemaDefinition = Mapping[
            str, str | Sequence[str] | t.ContainerValueMapping
        ]
        type ColumnMapping = Mapping[str, str | t.ContainerValueMapping]
        type IndexConfiguration = Mapping[
            str,
            str | Sequence[str] | t.ContainerValueMapping,
        ]
        type ConstraintDefinition = Mapping[str, str | t.ContainerValueMapping]
        type TablespaceSettings = Mapping[str, str | int | t.ContainerValueMapping]

    class OracleSql:
        """Oracle SQL operation complex types."""

        type SqlConfiguration = Mapping[
            str,
            str | bool | int | t.ContainerValueMapping,
        ]
        type QueryExecution = Mapping[str, str | t.ContainerValueMapping]
        type BulkOperations = Mapping[
            str,
            str | int | Sequence[str] | t.ContainerValueMapping,
        ]
        type PreparedStatements = Mapping[str, str | t.ContainerValueMapping]
        type SqlOptimization = Mapping[str, bool | str | t.ContainerValueMapping]
        type ResultSetHandling = Mapping[str, str | int | t.ContainerValueMapping]

    class OraclePerformance:
        """Oracle performance optimization complex types."""

        type PerformanceConfiguration = Mapping[
            str,
            str | int | t.ContainerValueMapping,
        ]
        type ConnectionPooling = Mapping[str, int | bool | t.ContainerValueMapping]
        type BulkLoadOptimization = Mapping[str, str | int | t.ContainerValueMapping]
        type QueryOptimization = Mapping[str, str | t.ContainerValueMapping]
        type CachingStrategy = Mapping[str, bool | str | t.ContainerValueMapping]
        type ParallelProcessing = Mapping[str, int | str | t.ContainerValueMapping]

    class DataTransformation:
        """Data transformation complex types."""

        type TransformationConfiguration = Mapping[
            str,
            str | bool | t.ContainerValueMapping,
        ]
        type FieldMapping = Mapping[str, str | Sequence[str] | t.ContainerValueMapping]
        type DataValidation = Mapping[str, str | t.ContainerValueMapping]
        type TypeConversion = Mapping[str, bool | str | t.ContainerValueMapping]
        type FilteringRules = Mapping[str, str | t.ContainerValueMapping]
        type TransformationResult = Mapping[str, Mapping[str, t.ContainerValue]]

    class StreamProcessing:
        """Stream processing complex types."""

        type StreamConfiguration = Mapping[
            str,
            str | bool | int | t.ContainerValueMapping,
        ]
        type StreamMetadata = Mapping[str, str | t.ContainerValueMapping]
        type StreamRecord = Mapping[str, t.ContainerValue]
        type StreamState = Mapping[str, str | int | t.ContainerValueMapping]
        type StreamBookmark = Mapping[str, str | int | t.ContainerValueMapping]
        type StreamSchema = Mapping[str, str | t.ContainerValueMapping | bool]

    class SingerMessage:
        """Singer protocol message complex types."""

        type SchemaMessage = Mapping[str, str | Sequence[str] | t.ContainerValueMapping]
        type RecordMessage = Mapping[str, str | t.ContainerValueMapping]
        type StateMessage = Mapping[str, str | t.ContainerValueMapping]
        type ActivateVersionMessage = Mapping[str, str | int]

    class ErrorHandling:
        """Error handling complex types."""

        type ErrorConfiguration = Mapping[
            str,
            bool | str | int | t.ContainerValueMapping,
        ]
        type ErrorRecovery = Mapping[str, str | bool | t.ContainerValueMapping]
        type ErrorReporting = Mapping[str, str | int | t.ContainerValueMapping]
        type ErrorClassification = Mapping[str, str | int | t.ContainerValueMapping]
        type ErrorMetrics = Mapping[str, int | float | t.ContainerValueMapping]
        type ErrorTracking = Sequence[Mapping[str, str | int | t.ContainerValueMapping]]

    class Core:
        """Core convenience type aliases for common patterns.

        Provides commonly used type aliases for consistency across the codebase.
        These are simple aliases but are used extensively, so provided for convenience.
        Access parent core types via inheritance from FlextTargetOracleTypes.
        """

        type Dict = Mapping[str, t.ContainerValue]
        "Type alias for generic dictionary (attribute name to value mapping)."


t = FlextTargetOracleTypes
__all__ = ["FlextTargetOracleTypes", "t"]
