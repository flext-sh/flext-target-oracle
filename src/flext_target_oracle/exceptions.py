"""Oracle Target exceptions - CONSOLIDATED to eliminate duplication.

Uses flext-meltano common exception patterns. Eliminates exception hierarchy
duplication with other target projects.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Any

# Import consolidated target exceptions from flext-meltano common
# MIGRATED: Singer SDK imports centralized via flext-meltano
from flext_meltano.common import (
    FlextMeltanoTargetAuthenticationError,
    FlextMeltanoTargetError,
    FlextMeltanoTargetProcessingError,
    FlextMeltanoTargetTransformationError,
)

# Use consolidated base target exception
FlextOracleTargetError = FlextMeltanoTargetError
FlextOracleTargetAuthenticationError = FlextMeltanoTargetAuthenticationError
FlextOracleTargetProcessingError = FlextMeltanoTargetProcessingError
FlextOracleTargetTransformationError = FlextMeltanoTargetTransformationError

# Oracle-specific exceptions that need custom behavior
class FlextOracleTargetValidationError(FlextMeltanoTargetError):
    """Oracle-specific validation errors."""

    def __init__(
        self,
        message: str,
        field: str | None = None,
        value: Any = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, field, value, details)


class FlextOracleTargetSingerRecordError(FlextOracleTargetValidationError):
    """Exception for invalid Singer record data."""

    def __init__(
        self,
        record_type: str,
        message: str,
        record_data: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            f"Invalid Singer record of type '{record_type}': {message}",
            field="record_type",
            value=record_type,
            details={"record_data": record_data},
        )
        self.record_type = record_type
        self.record_data = record_data


class FlextOracleTargetSchemaError(FlextOracleTargetValidationError):
    """Exception for invalid schema definitions."""

    def __init__(
        self,
        schema_name: str,
        message: str,
        schema_data: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            f"Invalid schema '{schema_name}': {message}",
            field="schema",
            value=schema_name,
            details={"schema_data": schema_data},
        )
        self.schema_name = schema_name
        self.schema_data = schema_data


class FlextOracleTargetStreamProcessingError(FlextOracleTargetProcessingError):
    """Exception for stream processing errors."""

    def __init__(
        self,
        stream_name: str,
        message: str,
        operation: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            f"Stream processing error for '{stream_name}': {message}",
            entry_dn=stream_name,
            operation=operation,
            details=details,
        )
        self.stream_name = stream_name


class FlextOracleTargetBatchProcessingError(FlextOracleTargetProcessingError):
    """Exception for batch processing errors."""

    def __init__(
        self,
        batch_id: str,
        record_count: int,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            f"Batch processing error for batch '{batch_id}' ({record_count} records): {message}",
            entry_dn=batch_id,
            operation="batch_processing",
            details={"record_count": record_count, **(details or {})},
        )
        self.batch_id = batch_id
        self.record_count = record_count


# Oracle Target Connection Exceptions
class FlextOracleTargetConnectionError(FlextMeltanoTargetError):
    """Connection errors specific to Oracle Target."""

    def __init__(
        self,
        message: str,
        host: str | None = None,
        port: int | None = None,
        service: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, host, port, service, details)


__all__ = [
    "FlextOracleTargetBatchProcessingError",
    "FlextOracleTargetConnectionError",
    "FlextOracleTargetProcessingError",
    "FlextOracleTargetSchemaError",
    "FlextOracleTargetSingerRecordError",
    "FlextOracleTargetStreamProcessingError",
    "FlextOracleTargetValidationError",
]
