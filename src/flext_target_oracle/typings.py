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
            FlextMeltanoTypes.Scalar | FlextMeltanoTypes.ContainerValueMapping,
        ]
        type StreamConfiguration = Mapping[
            str, str | bool | FlextMeltanoTypes.ContainerValueMapping
        ]
        type MessageProcessing = Mapping[
            str, str | Sequence[FlextMeltanoTypes.ContainerValueMapping]
        ]
        type RecordHandling = Mapping[
            str, str | FlextMeltanoTypes.ContainerValueMapping | bool
        ]
        type StateManagement = Mapping[
            str, str | FlextMeltanoTypes.ContainerValueMapping
        ]
        type BatchProcessing = Mapping[
            str, str | int | FlextMeltanoTypes.ContainerValueMapping
        ]

    class OracleDatabase:
        """Oracle database operation complex types."""

        type DatabaseConfiguration = Mapping[
            str,
            FlextMeltanoTypes.Scalar | FlextMeltanoTypes.ContainerValueMapping,
        ]
        type ConnectionManagement = Mapping[
            str, str | int | FlextMeltanoTypes.ContainerValueMapping
        ]
        type SessionSettings = Mapping[
            str, str | bool | FlextMeltanoTypes.ContainerValueMapping
        ]
        type TransactionControl = Mapping[
            str, str | bool | FlextMeltanoTypes.ContainerValueMapping
        ]
        type DatabaseMetadata = Mapping[
            str, str | FlextMeltanoTypes.ContainerValueMapping
        ]
        type PerformanceSettings = Mapping[
            str, int | float | FlextMeltanoTypes.ContainerValueMapping
        ]

    class OracleTable:
        """Oracle table and schema complex types."""

        type TableConfiguration = Mapping[
            str, str | bool | FlextMeltanoTypes.ContainerValueMapping
        ]
        type SchemaDefinition = Mapping[
            str,
            str
            | FlextMeltanoTypes.StrSequence
            | FlextMeltanoTypes.ContainerValueMapping,
        ]
        type ColumnMapping = Mapping[str, str | FlextMeltanoTypes.ContainerValueMapping]
        type IndexConfiguration = Mapping[
            str,
            str
            | FlextMeltanoTypes.StrSequence
            | FlextMeltanoTypes.ContainerValueMapping,
        ]
        type ConstraintDefinition = Mapping[
            str, str | FlextMeltanoTypes.ContainerValueMapping
        ]
        type TablespaceSettings = Mapping[
            str, str | int | FlextMeltanoTypes.ContainerValueMapping
        ]

    class OracleSql:
        """Oracle SQL operation complex types."""

        type SqlConfiguration = Mapping[
            str,
            str | bool | int | FlextMeltanoTypes.ContainerValueMapping,
        ]
        type QueryExecution = Mapping[
            str, str | FlextMeltanoTypes.ContainerValueMapping
        ]
        type BulkOperations = Mapping[
            str,
            str
            | int
            | FlextMeltanoTypes.StrSequence
            | FlextMeltanoTypes.ContainerValueMapping,
        ]
        type PreparedStatements = Mapping[
            str, str | FlextMeltanoTypes.ContainerValueMapping
        ]
        type SqlOptimization = Mapping[
            str, bool | str | FlextMeltanoTypes.ContainerValueMapping
        ]
        type ResultSetHandling = Mapping[
            str, str | int | FlextMeltanoTypes.ContainerValueMapping
        ]

    class OraclePerformance:
        """Oracle performance optimization complex types."""

        type PerformanceConfiguration = Mapping[
            str,
            str | int | FlextMeltanoTypes.ContainerValueMapping,
        ]
        type ConnectionPooling = Mapping[
            str, int | bool | FlextMeltanoTypes.ContainerValueMapping
        ]
        type BulkLoadOptimization = Mapping[
            str, str | int | FlextMeltanoTypes.ContainerValueMapping
        ]
        type QueryOptimization = Mapping[
            str, str | FlextMeltanoTypes.ContainerValueMapping
        ]
        type CachingStrategy = Mapping[
            str, bool | str | FlextMeltanoTypes.ContainerValueMapping
        ]
        type ParallelProcessing = Mapping[
            str, int | str | FlextMeltanoTypes.ContainerValueMapping
        ]

    class DataTransformation:
        """Data transformation complex types."""

        type TransformationConfiguration = Mapping[
            str,
            str | bool | FlextMeltanoTypes.ContainerValueMapping,
        ]
        type FieldMapping = Mapping[
            str,
            str
            | FlextMeltanoTypes.StrSequence
            | FlextMeltanoTypes.ContainerValueMapping,
        ]
        type DataValidation = Mapping[
            str, str | FlextMeltanoTypes.ContainerValueMapping
        ]
        type TypeConversion = Mapping[
            str, bool | str | FlextMeltanoTypes.ContainerValueMapping
        ]
        type FilteringRules = Mapping[
            str, str | FlextMeltanoTypes.ContainerValueMapping
        ]
        type TransformationResult = Mapping[
            str, Mapping[str, FlextMeltanoTypes.ContainerValue]
        ]

    class StreamProcessing:
        """Stream processing complex types."""

        type StreamConfiguration = Mapping[
            str,
            str | bool | int | FlextMeltanoTypes.ContainerValueMapping,
        ]
        type StreamMetadata = Mapping[
            str, str | FlextMeltanoTypes.ContainerValueMapping
        ]
        type StreamRecord = Mapping[str, FlextMeltanoTypes.ContainerValue]
        type StreamState = Mapping[
            str, str | int | FlextMeltanoTypes.ContainerValueMapping
        ]
        type StreamBookmark = Mapping[
            str, str | int | FlextMeltanoTypes.ContainerValueMapping
        ]
        type StreamSchema = Mapping[
            str, str | FlextMeltanoTypes.ContainerValueMapping | bool
        ]

    class SingerMessage:
        """Singer protocol message complex types."""

        type SchemaMessage = Mapping[
            str,
            str
            | FlextMeltanoTypes.StrSequence
            | FlextMeltanoTypes.ContainerValueMapping,
        ]
        type RecordMessage = Mapping[str, str | FlextMeltanoTypes.ContainerValueMapping]
        type StateMessage = Mapping[str, str | FlextMeltanoTypes.ContainerValueMapping]
        type ActivateVersionMessage = Mapping[str, str | int]

    class ErrorHandling:
        """Error handling complex types."""

        type ErrorConfiguration = Mapping[
            str,
            bool | str | int | FlextMeltanoTypes.ContainerValueMapping,
        ]
        type ErrorRecovery = Mapping[
            str, str | bool | FlextMeltanoTypes.ContainerValueMapping
        ]
        type ErrorReporting = Mapping[
            str, str | int | FlextMeltanoTypes.ContainerValueMapping
        ]
        type ErrorClassification = Mapping[
            str, str | int | FlextMeltanoTypes.ContainerValueMapping
        ]
        type ErrorMetrics = Mapping[
            str, int | float | FlextMeltanoTypes.ContainerValueMapping
        ]
        type ErrorTracking = Sequence[
            Mapping[str, str | int | FlextMeltanoTypes.ContainerValueMapping]
        ]

    class Core:
        """Core convenience type aliases for common patterns.

        Provides commonly used type aliases for consistency across the codebase.
        These are simple aliases but are used extensively, so provided for convenience.
        Access parent core types via inheritance from FlextTargetOracleTypes.
        """

        type Dict = Mapping[str, FlextMeltanoTypes.ContainerValue]
        "Type alias for generic dictionary (attribute name to value mapping)."


t = FlextTargetOracleTypes
__all__ = ["FlextTargetOracleTypes", "t"]
