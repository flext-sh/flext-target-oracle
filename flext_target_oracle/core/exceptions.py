"""Custom exceptions for flext-target-oracle.

These exceptions provide clear error hierarchies and make
error handling more precise and maintainable.
"""

from __future__ import annotations

from typing import Any


class OracleTargetError(Exception):
    """Base exception for all Oracle target errors."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        """Initialize with message and optional details."""
        super().__init__(message)
        self.details = details or {}


class ConfigurationError(OracleTargetError):
    """Configuration-related errors."""


class ConnectionError(OracleTargetError):
    """Database connection errors."""


class SchemaError(OracleTargetError):
    """Schema-related errors."""


class TypeMappingError(OracleTargetError):
    """Type mapping errors."""


class BatchProcessingError(OracleTargetError):
    """Batch processing errors."""


class ValidationError(OracleTargetError):
    """Data validation errors."""


class LicenseComplianceError(ConfigurationError):
    """Oracle license compliance errors."""


class PoolExhaustedError(ConnectionError):
    """Connection pool exhausted."""


class UnsupportedTypeError(TypeMappingError):
    """Unsupported data type."""


class RecoverableError(OracleTargetError):
    """Base class for recoverable errors."""


class NonRecoverableError(OracleTargetError):
    """Base class for non-recoverable errors."""
