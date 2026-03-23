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
            str | int | bool | Mapping[str, t.ContainerValue],
        ]
        type StreamConfiguration = Mapping[
            str, str | bool | Mapping[str, t.ContainerValue]
        ]
        type MessageProcessing = Mapping[
            str, str | Sequence[Mapping[str, t.ContainerValue]]
        ]
        type RecordHandling = Mapping[str, str | Mapping[str, t.ContainerValue] | bool]
        type StateManagement = Mapping[str, str | Mapping[str, t.ContainerValue]]
        type BatchProcessing = Mapping[str, str | int | Mapping[str, t.ContainerValue]]

    class OracleDatabase:
        """Oracle database operation complex types."""

        type DatabaseConfiguration = Mapping[
            str,
            str | int | bool | Mapping[str, t.ContainerValue],
        ]
        type ConnectionManagement = Mapping[
            str, str | int | Mapping[str, t.ContainerValue]
        ]
        type SessionSettings = Mapping[str, str | bool | Mapping[str, t.ContainerValue]]
        type TransactionControl = Mapping[
            str, str | bool | Mapping[str, t.ContainerValue]
        ]
        type DatabaseMetadata = Mapping[str, str | Mapping[str, t.ContainerValue]]
        type PerformanceSettings = Mapping[
            str, int | float | Mapping[str, t.ContainerValue]
        ]

    class OracleTable:
        """Oracle table and schema complex types."""

        type TableConfiguration = Mapping[
            str, str | bool | Mapping[str, t.ContainerValue]
        ]
        type SchemaDefinition = Mapping[
            str, str | Sequence[str] | Mapping[str, t.ContainerValue]
        ]
        type ColumnMapping = Mapping[str, str | Mapping[str, t.ContainerValue]]
        type IndexConfiguration = Mapping[
            str,
            str | Sequence[str] | Mapping[str, t.ContainerValue],
        ]
        type ConstraintDefinition = Mapping[str, str | Mapping[str, t.ContainerValue]]
        type TablespaceSettings = Mapping[
            str, str | int | Mapping[str, t.ContainerValue]
        ]

    class OracleSql:
        """Oracle SQL operation complex types."""

        type SqlConfiguration = Mapping[
            str,
            str | bool | int | Mapping[str, t.ContainerValue],
        ]
        type QueryExecution = Mapping[str, str | Mapping[str, t.ContainerValue]]
        type BulkOperations = Mapping[
            str,
            str | int | Sequence[str] | Mapping[str, t.ContainerValue],
        ]
        type PreparedStatements = Mapping[str, str | Mapping[str, t.ContainerValue]]
        type SqlOptimization = Mapping[str, bool | str | Mapping[str, t.ContainerValue]]
        type ResultSetHandling = Mapping[
            str, str | int | Mapping[str, t.ContainerValue]
        ]

    class OraclePerformance:
        """Oracle performance optimization complex types."""

        type PerformanceConfiguration = Mapping[
            str,
            str | int | Mapping[str, t.ContainerValue],
        ]
        type ConnectionPooling = Mapping[
            str, int | bool | Mapping[str, t.ContainerValue]
        ]
        type BulkLoadOptimization = Mapping[
            str, str | int | Mapping[str, t.ContainerValue]
        ]
        type QueryOptimization = Mapping[str, str | Mapping[str, t.ContainerValue]]
        type CachingStrategy = Mapping[str, bool | str | Mapping[str, t.ContainerValue]]
        type ParallelProcessing = Mapping[
            str, int | str | Mapping[str, t.ContainerValue]
        ]

    class DataTransformation:
        """Data transformation complex types."""

        type TransformationConfiguration = Mapping[
            str,
            str | bool | Mapping[str, t.ContainerValue],
        ]
        type FieldMapping = Mapping[
            str, str | Sequence[str] | Mapping[str, t.ContainerValue]
        ]
        type DataValidation = Mapping[str, str | Mapping[str, t.ContainerValue]]
        type TypeConversion = Mapping[str, bool | str | Mapping[str, t.ContainerValue]]
        type FilteringRules = Mapping[str, str | Mapping[str, t.ContainerValue]]
        type TransformationResult = Mapping[str, Mapping[str, t.ContainerValue]]

    class StreamProcessing:
        """Stream processing complex types."""

        type StreamConfiguration = Mapping[
            str,
            str | bool | int | Mapping[str, t.ContainerValue],
        ]
        type StreamMetadata = Mapping[str, str | Mapping[str, t.ContainerValue]]
        type StreamRecord = Mapping[str, t.ContainerValue]
        type StreamState = Mapping[str, str | int | Mapping[str, t.ContainerValue]]
        type StreamBookmark = Mapping[str, str | int | Mapping[str, t.ContainerValue]]
        type StreamSchema = Mapping[str, str | Mapping[str, t.ContainerValue] | bool]

    class SingerMessage:
        """Singer protocol message complex types."""

        type SchemaMessage = Mapping[
            str, str | Sequence[str] | Mapping[str, t.ContainerValue]
        ]
        type RecordMessage = Mapping[str, str | Mapping[str, t.ContainerValue]]
        type StateMessage = Mapping[str, str | Mapping[str, t.ContainerValue]]
        type ActivateVersionMessage = Mapping[str, str | int]

    class ErrorHandling:
        """Error handling complex types."""

        type ErrorConfiguration = Mapping[
            str,
            bool | str | int | Mapping[str, t.ContainerValue],
        ]
        type ErrorRecovery = Mapping[str, str | bool | Mapping[str, t.ContainerValue]]
        type ErrorReporting = Mapping[str, str | int | Mapping[str, t.ContainerValue]]
        type ErrorClassification = Mapping[
            str, str | int | Mapping[str, t.ContainerValue]
        ]
        type ErrorMetrics = Mapping[str, int | float | Mapping[str, t.ContainerValue]]
        type ErrorTracking = Sequence[
            Mapping[str, str | int | Mapping[str, t.ContainerValue]]
        ]

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
