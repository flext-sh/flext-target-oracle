"""Oracle Target Exceptions - Simple and clean.

Uses flext-core patterns for exception handling.
"""

from flext_core.exceptions import FlextError


class FlextOracleTargetError(FlextError):
    """Base exception for Oracle target operations."""

    def __init__(self, message: str, **kwargs: object) -> None:
        """Initialize Oracle target error."""
        super().__init__(message, context=kwargs)


class FlextOracleTargetConnectionError(FlextOracleTargetError):
    """Oracle connection error."""

    def __init__(self, message: str, **kwargs: object) -> None:
        """Initialize connection error."""
        super().__init__(f"Connection error: {message}", context=kwargs)


class FlextOracleTargetAuthenticationError(FlextOracleTargetError):
    """Oracle authentication error."""

    def __init__(self, message: str, **kwargs: object) -> None:
        """Initialize authentication error."""
        super().__init__(f"Authentication error: {message}", context=kwargs)


class FlextOracleTargetProcessingError(FlextOracleTargetError):
    """Oracle processing error."""

    def __init__(self, message: str, **kwargs: object) -> None:
        """Initialize processing error."""
        super().__init__(f"Processing error: {message}", context=kwargs)


class FlextOracleTargetSchemaError(FlextOracleTargetError):
    """Oracle schema error."""

    def __init__(self, message: str, **kwargs: object) -> None:
        """Initialize schema error."""
        super().__init__(f"Schema error: {message}", context=kwargs)


__all__ = [
    "FlextOracleTargetAuthenticationError",
    "FlextOracleTargetConnectionError",
    "FlextOracleTargetError",
    "FlextOracleTargetProcessingError",
    "FlextOracleTargetSchemaError",
]
