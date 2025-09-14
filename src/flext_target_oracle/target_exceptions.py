"""Oracle Target Exception Hierarchy - Using flext-core SOURCE OF TRUTH.

Direct usage of flext-core exception classes without duplication or factories.
Oracle-specific exceptions inherit directly from flext-core bases.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextConstants, FlextExceptions, FlextTypes

# Direct access to the internal exception classes for proper inheritance
BaseError = FlextExceptions.BaseError
ConfigurationError = FlextExceptions._ConfigurationError
FlextConnectionError = (
    FlextExceptions._ConnectionError
)  # Avoid Python builtin shadowing
ValidationError = FlextExceptions._ValidationError
AuthenticationError = FlextExceptions._AuthenticationError
ProcessingError = FlextExceptions._ProcessingError
FlextTimeoutError = FlextExceptions._TimeoutError  # Avoid Python builtin shadowing


# Oracle-specific exception classes using flext-core SOURCE OF TRUTH
class FlextTargetOracleBaseError(BaseError):
    """Oracle Target base error using flext-core foundation."""


# Main Oracle error - inherits from base error
class FlextTargetOracleError(FlextTargetOracleBaseError):
    """Oracle Target main error - inherits from base error."""


class FlextTargetOracleConfigurationError(ConfigurationError):
    """Oracle configuration error using flext-core foundation."""


class FlextTargetOracleConnectionError(FlextConnectionError):
    """Oracle connection error with Oracle-specific context."""

    def __init__(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        service_name: str | None = None,
        user: str | None = None,
        dsn: str | None = None,
        code: str | None = None,
        context: dict[str, object] | None = None,
        correlation_id: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize connection error with Oracle-specific context."""
        oracle_context = context or {}
        if host is not None:
            oracle_context["host"] = host
        if port is not None:
            oracle_context["port"] = port
        if service_name is not None:
            oracle_context["service_name"] = service_name
        if user is not None:
            oracle_context["user"] = user
        if dsn is not None:
            oracle_context["dsn"] = dsn

        oracle_context.update(kwargs)

        super().__init__(
            message=message,
            code=code or FlextConstants.Errors.CONNECTION_ERROR,
            context=oracle_context,
            correlation_id=correlation_id,
        )

    @property
    def host(self) -> str | None:
        """Get connection host."""
        ctx = getattr(self, "context", None)
        if isinstance(ctx, dict):
            value = ctx.get("host")
            return value if isinstance(value, str) else None
        return None

    @property
    def port(self) -> int | None:
        """Get connection port."""
        ctx = getattr(self, "context", None)
        if isinstance(ctx, dict):
            value = ctx.get("port")
            return value if isinstance(value, int) else None
        return None

    @property
    def service_name(self) -> str | None:
        """Get Oracle service name."""
        ctx = getattr(self, "context", None)
        if isinstance(ctx, dict):
            value = ctx.get("service_name")
            return value if isinstance(value, str) else None
        return None

    @property
    def user(self) -> str | None:
        """Get connection user."""
        ctx = getattr(self, "context", None)
        if isinstance(ctx, dict):
            value = ctx.get("user")
            return value if isinstance(value, str) else None
        return None

    @property
    def dsn(self) -> str | None:
        """Get Oracle DSN."""
        ctx = getattr(self, "context", None)
        if isinstance(ctx, dict):
            value = ctx.get("dsn")
            return value if isinstance(value, str) else None
        return None


class FlextTargetOracleValidationError(ValidationError):
    """Oracle validation error using flext-core foundation."""


class FlextTargetOracleAuthenticationError(AuthenticationError):
    """Oracle authentication error with Oracle-specific context."""

    def __init__(
        self,
        message: str,
        *,
        user: str | None = None,
        auth_method: str | None = None,
        wallet_location: str | None = None,
        code: str | None = None,
        context: dict[str, object] | None = None,
        correlation_id: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize authentication error with Oracle-specific context."""
        oracle_context = context or {}
        if user is not None:
            oracle_context["user"] = user
        if auth_method is not None:
            oracle_context["auth_method"] = auth_method
        if wallet_location is not None:
            oracle_context["wallet_location"] = wallet_location

        oracle_context.update(kwargs)

        super().__init__(
            message=message,
            code=code or FlextConstants.Errors.AUTHENTICATION_ERROR,
            context=oracle_context,
            correlation_id=correlation_id,
        )

    @property
    def user(self) -> str | None:
        """Get authentication user."""
        ctx = getattr(self, "context", None)
        if isinstance(ctx, dict):
            value = ctx.get("user")
            return value if isinstance(value, str) else None
        return None

    @property
    def wallet_location(self) -> str | None:
        """Get wallet location."""
        ctx = getattr(self, "context", None)
        if isinstance(ctx, dict):
            value = ctx.get("wallet_location")
            return value if isinstance(value, str) else None
        return None


class FlextTargetOracleProcessingError(ProcessingError):
    """Oracle processing error with Oracle-specific context."""

    def __init__(
        self,
        message: str,
        *,
        stream_name: str | None = None,
        record_count: int | None = None,
        error_records: list[dict[str, object]] | None = None,
        operation: str | None = None,
        code: str | None = None,
        context: dict[str, object] | None = None,
        correlation_id: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize processing error with Oracle-specific context."""
        oracle_context = context or {}
        if stream_name is not None:
            oracle_context["stream_name"] = stream_name
        if record_count is not None:
            oracle_context["record_count"] = record_count
        if error_records is not None:
            oracle_context["error_records"] = error_records
        if operation is not None:
            oracle_context["operation"] = operation

        oracle_context.update(kwargs)

        super().__init__(
            message=message,
            code=code or FlextConstants.Errors.PROCESSING_ERROR,
            context=oracle_context,
            correlation_id=correlation_id,
        )

    @property
    def stream_name(self) -> str | None:
        """Get stream name."""
        ctx = getattr(self, "context", None)
        if isinstance(ctx, dict):
            value = ctx.get("stream_name")
            return value if isinstance(value, str) else None
        return None

    @property
    def record_count(self) -> int | None:
        """Get record count."""
        ctx = getattr(self, "context", None)
        if isinstance(ctx, dict):
            value = ctx.get("record_count")
            return value if isinstance(value, int) else None
        return None

    @property
    def error_records(self) -> list[dict[str, object]] | None:
        """Get error records."""
        ctx = getattr(self, "context", None)
        if isinstance(ctx, dict):
            value = ctx.get("error_records")
            if isinstance(value, list) and all(isinstance(i, dict) for i in value):
                # Rebuild to ensure precise element typing
                normalized: list[dict[str, object]] = [
                    {**item}
                    for item in value  # shallow copy as dict[str, object]
                ]
                return normalized
        return None


class FlextTargetOracleTimeoutError(FlextTimeoutError):
    """Oracle timeout error using flext-core foundation."""


# Domain-specific Oracle exceptions extending flext-core patterns
class FlextTargetOracleSchemaError(FlextTargetOracleValidationError):
    """Oracle schema-specific validation errors."""

    def __init__(
        self,
        message: str,
        *,
        stream_name: str | None = None,
        table_name: str | None = None,
        schema_hash: str | None = None,
        validation_errors: list[str] | None = None,
        code: str | None = None,
        context: dict[str, object] | None = None,
        correlation_id: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize schema error with Oracle-specific context."""
        oracle_context = context or {}
        if stream_name is not None:
            oracle_context["stream_name"] = stream_name
        if table_name is not None:
            oracle_context["table_name"] = table_name
        if schema_hash is not None:
            oracle_context["schema_hash"] = schema_hash
        if validation_errors is not None:
            oracle_context["validation_errors"] = validation_errors

        oracle_context.update(kwargs)

        super().__init__(
            message=message,
            code=code or FlextConstants.Errors.VALIDATION_ERROR,
            context=oracle_context,
            correlation_id=correlation_id,
        )

    @property
    def stream_name(self) -> str | None:
        """Get stream name."""
        ctx = getattr(self, "context", None)
        if isinstance(ctx, dict):
            value = ctx.get("stream_name")
            return value if isinstance(value, str) else None
        return None

    @property
    def table_name(self) -> str | None:
        """Get table name."""
        ctx = getattr(self, "context", None)
        if isinstance(ctx, dict):
            value = ctx.get("table_name")
            return value if isinstance(value, str) else None
        return None

    @property
    def schema_hash(self) -> str | None:
        """Get schema hash."""
        ctx = getattr(self, "context", None)
        if isinstance(ctx, dict):
            value = ctx.get("schema_hash")
            return value if isinstance(value, str) else None
        return None

    @property
    def validation_errors(self) -> list[str] | None:
        """Get validation errors."""
        ctx = getattr(self, "context", None)
        if isinstance(ctx, dict):
            value = ctx.get("validation_errors")
            if isinstance(value, list) and all(isinstance(s, str) for s in value):
                return value
        return None


class FlextTargetOracleLoadError(FlextTargetOracleProcessingError):
    """Oracle data loading errors."""


class FlextTargetOracleSQLError(FlextTargetOracleProcessingError):
    """Oracle SQL execution errors."""

    def __init__(
        self,
        message: str,
        *,
        sql_statement: str | None = None,
        table_name: str | None = None,
        operation: str | None = None,
        code: str | None = None,
        context: dict[str, object] | None = None,
        correlation_id: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize SQL error with Oracle-specific context."""
        oracle_context = context or {}
        if sql_statement is not None:
            oracle_context["sql_statement"] = sql_statement
        if table_name is not None:
            oracle_context["table_name"] = table_name
        if operation is not None:
            oracle_context["operation"] = operation

        oracle_context.update(kwargs)

        super().__init__(
            message=message,
            code=code or FlextConstants.Errors.OPERATION_ERROR,
            context=oracle_context,
            correlation_id=correlation_id,
        )

    @property
    def sql_statement(self) -> str | None:
        """Get SQL statement."""
        ctx = getattr(self, "context", None)
        if isinstance(ctx, dict):
            value = ctx.get("sql_statement")
            return value if isinstance(value, str) else None
        return None


class FlextTargetOracleRecordError(FlextTargetOracleProcessingError):
    """Oracle record processing errors."""


__all__: FlextTypes.Core.StringList = [
    "FlextTargetOracleAuthenticationError",
    "FlextTargetOracleBaseError",
    "FlextTargetOracleConfigurationError",
    "FlextTargetOracleConnectionError",
    "FlextTargetOracleError",
    "FlextTargetOracleLoadError",
    "FlextTargetOracleProcessingError",
    "FlextTargetOracleRecordError",
    "FlextTargetOracleSQLError",
    "FlextTargetOracleSchemaError",
    "FlextTargetOracleTimeoutError",
    "FlextTargetOracleValidationError",
]
