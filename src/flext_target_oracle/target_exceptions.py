"""Oracle Target Exception Hierarchy - Using flext-core SOURCE OF TRUTH.

Direct usage of flext-core exception classes without duplication or factories.
Oracle-specific exceptions inherit directly from flext-core bases.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import override

from flext_core import FlextConstants, FlextExceptions


class FlextTargetOracleExceptions(FlextExceptions):
    """Oracle Target exceptions using flext-core SOURCE OF TRUTH."""

    # Main Oracle error - inherits from base error
    class Error(FlextExceptions.BaseError):
        """Oracle Target main error - inherits from base error."""

    class ConfigurationError(FlextExceptions.ConfigurationError):
        """Oracle configuration error using flext-core foundation."""

    class OracleConnectionError(FlextExceptions.ConnectionError):
        """Oracle connection error with Oracle-specific context."""

        @override
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
                error_code=code or FlextConstants.Errors.CONNECTION_ERROR,
                context=oracle_context,
                _correlation_id=correlation_id,
            )
            # Oracle-specific attributes beyond parent's host/port/timeout
            self.service_name = oracle_context.get("service_name")
            self.user = oracle_context.get("user")
            self.dsn = oracle_context.get("dsn")

    class ValidationError(FlextExceptions.ValidationError):
        """Oracle validation error using flext-core foundation."""

    class AuthenticationError(FlextExceptions.AuthenticationError):
        """Oracle authentication error with Oracle-specific context."""

        @override
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
                error_code=code or FlextConstants.Errors.AUTHENTICATION_ERROR,
                context=oracle_context,
                _correlation_id=correlation_id,
            )
            # Oracle-specific attributes
            self.user = oracle_context.get("user")
            self.auth_method = oracle_context.get("auth_method")
            self.wallet_location = oracle_context.get("wallet_location")

    class ProcessingError(FlextExceptions.OperationError):
        """Oracle processing error with Oracle-specific context."""

        @override
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
                error_code=code or FlextConstants.Errors.PROCESSING_ERROR,
                context=oracle_context,
                _correlation_id=correlation_id,
            )
            # Oracle-specific attributes
            self.stream_name = oracle_context.get("stream_name")
            self.record_count = oracle_context.get("record_count")
            self.error_records = oracle_context.get("error_records")
            self.operation = oracle_context.get("operation")

    class OracleTimeoutError(FlextExceptions.TimeoutError):
        """Oracle timeout error using flext-core foundation."""

    # Domain-specific Oracle exceptions extending flext-core patterns
    class SchemaError(ValidationError):
        """Oracle schema-specific validation errors."""

        @override
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
                error_code=code or FlextConstants.Errors.VALIDATION_ERROR,
                context=oracle_context,
                _correlation_id=correlation_id,
            )
            # Oracle-specific attributes
            self.stream_name = oracle_context.get("stream_name")
            self.table_name = oracle_context.get("table_name")
            self.schema_hash = oracle_context.get("schema_hash")
            self.validation_errors = oracle_context.get("validation_errors")

    class LoadError(ProcessingError):
        """Oracle data loading errors."""

    class SQLError(ProcessingError):
        """Oracle SQL execution errors."""

        @override
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
            # Oracle-specific attributes
            self.sql_statement = oracle_context.get("sql_statement")
            self.table_name = oracle_context.get("table_name")

    class RecordError(ProcessingError):
        """Oracle record processing errors."""


# Module-level classes with real inheritance for backward compatibility
class FlextTargetOracleError(FlextTargetOracleExceptions.Error):
    """FlextTargetOracleError - real inheritance from Error."""


class FlextTargetOracleSettingsurationError(
    FlextTargetOracleExceptions.ConfigurationError,
):
    """FlextTargetOracleSettingsurationError - real inheritance from ConfigurationError."""


class FlextTargetOracleConnectionError(
    FlextTargetOracleExceptions.OracleConnectionError,
):
    """FlextTargetOracleConnectionError - real inheritance from OracleConnectionError."""


class FlextTargetOracleValidationError(FlextTargetOracleExceptions.ValidationError):
    """FlextTargetOracleValidationError - real inheritance from ValidationError."""


class FlextTargetOracleAuthenticationError(
    FlextTargetOracleExceptions.AuthenticationError,
):
    """FlextTargetOracleAuthenticationError - real inheritance from AuthenticationError."""


class FlextTargetOracleProcessingError(FlextTargetOracleExceptions.ProcessingError):
    """FlextTargetOracleProcessingError - real inheritance from ProcessingError."""


class FlextTargetOracleTimeoutError(FlextTargetOracleExceptions.OracleTimeoutError):
    """FlextTargetOracleTimeoutError - real inheritance from OracleTimeoutError."""


class FlextTargetOracleSchemaError(FlextTargetOracleExceptions.SchemaError):
    """FlextTargetOracleSchemaError - real inheritance from SchemaError."""


class FlextTargetOracleLoadError(FlextTargetOracleExceptions.LoadError):
    """FlextTargetOracleLoadError - real inheritance from LoadError."""


class FlextTargetOracleSQLError(FlextTargetOracleExceptions.SQLError):
    """FlextTargetOracleSQLError - real inheritance from SQLError."""


class FlextTargetOracleRecordError(FlextTargetOracleExceptions.RecordError):
    """FlextTargetOracleRecordError - real inheritance from RecordError."""


__all__: list[str] = [
    "FlextTargetOracleAuthenticationError",
    "FlextTargetOracleConnectionError",
    "FlextTargetOracleError",
    "FlextTargetOracleExceptions",
    "FlextTargetOracleLoadError",
    "FlextTargetOracleProcessingError",
    "FlextTargetOracleRecordError",
    "FlextTargetOracleSQLError",
    "FlextTargetOracleSchemaError",
    "FlextTargetOracleSettingsurationError",
    "FlextTargetOracleTimeoutError",
    "FlextTargetOracleValidationError",
]
