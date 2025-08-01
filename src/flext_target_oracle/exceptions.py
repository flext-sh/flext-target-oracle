"""Oracle Target Exceptions - Simple and clean.

Uses flext-core Singer base patterns for exception handling.
Eliminates duplication by using centralized Singer exception patterns.
"""

# 🚨 ARCHITECTURAL COMPLIANCE: Use Singer base exceptions to eliminate duplication
from flext_core import FlextTargetError


class FlextOracleTargetError(FlextTargetError):
    """Base exception for Oracle target operations."""

    def __init__(
        self,
        message: str,
        stream_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Oracle target error."""
        super().__init__(
            message,
            component_type="target",
            stream_name=stream_name,
            destination_system="oracle",
            **kwargs,
        )


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
