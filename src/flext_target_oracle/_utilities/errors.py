"""Oracle Target Exception Hierarchy - Using flext-core SOURCE OF TRUTH.

Direct usage of flext-core exception classes without duplication or factories.
Oracle-specific exceptions inherit directly from flext-core bases.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Annotated, override

from flext_core import FlextConstants, FlextExceptionsBase, FlextModels, FlextTypes, u
from flext_target_oracle import e, t

if TYPE_CHECKING:
    from flext_target_oracle import t
else:
    t = FlextTypes

c = FlextConstants
m = FlextModels


class FlextTargetOracleErrorMetadata(m.FlexibleInternalModel):
    """Structured metadata attached to Oracle target error responses."""

    code: Annotated[str, u.Field(description="Canonical error code")]
    context: Annotated[
        t.MappingKV[str, t.JsonValue] | None,
        u.Field(
            description="Structured error context",
        ),
    ] = None
    correlation_id: Annotated[
        str | None,
        u.Field(
            description="Cross-service correlation identifier",
        ),
    ] = None


class FlextTargetOracleExceptions(e):
    """Oracle Target exceptions using flext-core SOURCE OF TRUTH."""

    @staticmethod
    def _build_context(
        *,
        default_code: str,
        metadata: FlextTargetOracleErrorMetadata | None,
        kwargs: dict[str, t.JsonPayload],
    ) -> tuple[FlextTargetOracleErrorMetadata, dict[str, t.JsonValue]]:
        """Resolve metadata and build merged oracle context from kwargs."""
        resolved = metadata or FlextTargetOracleErrorMetadata(code=default_code)
        ctx: dict[str, t.JsonValue] = dict(resolved.context) if resolved.context else {}
        ctx.update({
            k: (
                v.isoformat()
                if isinstance(v, datetime)
                else v
                if isinstance(v, (str, int, float, bool))
                else ""
                if v is None
                else str(v)
            )
            for k, v in kwargs.items()
        })
        return resolved, ctx

    class Error(FlextExceptionsBase.BaseError):
        """Oracle Target main error - inherits from base error."""

    class ConfigurationError(e.ConfigurationError):
        """Oracle configuration error using flext-core foundation."""

    class OracleConnectionError(e.ConnectionError):
        """Oracle connection error with Oracle-specific context."""

        @override
        def __init__(
            self,
            message: str,
            *,
            metadata: FlextTargetOracleErrorMetadata | None = None,
            **kwargs: t.JsonPayload,
        ) -> None:
            """Initialize connection error with Oracle-specific context."""
            _, ctx = FlextTargetOracleExceptions._build_context(
                default_code=c.ErrorCode.CONNECTION_ERROR,
                metadata=metadata,
                kwargs=kwargs,
            )
            super().__init__(message=message)
            self.service_name = ctx.get("service_name")
            self.user = ctx.get("user")
            self.dsn = ctx.get("dsn")

    class ValidationError(e.ValidationError):
        """Oracle validation error using flext-core foundation."""

    class AuthenticationError(e.AuthenticationError):
        """Oracle authentication error with Oracle-specific context."""

        @override
        def __init__(
            self,
            message: str,
            *,
            metadata: FlextTargetOracleErrorMetadata | None = None,
            **kwargs: t.JsonPayload,
        ) -> None:
            """Initialize authentication error with Oracle-specific context."""
            resolved, ctx = FlextTargetOracleExceptions._build_context(
                default_code=c.ErrorCode.AUTHENTICATION_ERROR,
                metadata=metadata,
                kwargs=kwargs,
            )
            super().__init__(
                message=message,
                error_code=resolved.code,
                context=ctx or None,
                correlation_id=resolved.correlation_id,
            )
            self.user = ctx.get("user")
            auth_method_val = ctx.get("auth_method")
            self.auth_method = (
                str(auth_method_val) if auth_method_val is not None else None
            )
            self.wallet_location = ctx.get("wallet_location")

    class ProcessingError(Error):
        """Oracle processing error with Oracle-specific context."""

        @override
        def __init__(
            self,
            message: str,
            *,
            metadata: FlextTargetOracleErrorMetadata | None = None,
            **kwargs: t.JsonPayload,
        ) -> None:
            """Initialize processing error with Oracle-specific context."""
            _, ctx = FlextTargetOracleExceptions._build_context(
                default_code=c.ErrorCode.PROCESSING_ERROR,
                metadata=metadata,
                kwargs=kwargs,
            )
            super().__init__(message=message)
            self.stream_name = ctx.get("stream_name")
            self.record_count = ctx.get("record_count")
            self.error_records = ctx.get("error_records")
            operation_val = ctx.get("operation")
            self.operation = str(operation_val) if operation_val is not None else None

    class OracleTimeoutError(e.TimeoutError):
        """Oracle timeout error using flext-core foundation."""

    class SchemaError(ValidationError):
        """Oracle schema-specific validation errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            metadata: FlextTargetOracleErrorMetadata | None = None,
            **kwargs: t.JsonPayload,
        ) -> None:
            """Initialize schema error with Oracle-specific context."""
            resolved, ctx = FlextTargetOracleExceptions._build_context(
                default_code=c.ErrorCode.VALIDATION_ERROR,
                metadata=metadata,
                kwargs=kwargs,
            )
            super().__init__(
                message=message,
                error_code=resolved.code,
                context=ctx or None,
                correlation_id=resolved.correlation_id,
            )
            self.stream_name = ctx.get("stream_name")
            self.table_name = ctx.get("table_name")
            self.schema_hash = ctx.get("schema_hash")
            validation_errors_val = ctx.get("validation_errors")
            self.validation_errors = (
                tuple(str(validation_errors_val).split(", "))
                if validation_errors_val is not None
                else None
            )

    class LoadError(ProcessingError):
        """Oracle data loading errors."""

    class SQLError(ProcessingError):
        """Oracle SQL execution errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            metadata: FlextTargetOracleErrorMetadata | None = None,
            **kwargs: t.JsonPayload,
        ) -> None:
            """Initialize SQL error with Oracle-specific context."""
            resolved, ctx = FlextTargetOracleExceptions._build_context(
                default_code=c.ErrorCode.OPERATION_ERROR,
                metadata=metadata,
                kwargs=kwargs,
            )
            super().__init__(
                message=message,
                metadata=resolved.model_copy(update={"context": ctx or None}),
            )
            self.sql_statement = ctx.get("sql_statement")
            self.table_name = ctx.get("table_name")

    class RecordError(ProcessingError):
        """Oracle record processing errors."""


__all__: t.StrSequence = [
    "FlextTargetOracleErrorMetadata",
    "FlextTargetOracleExceptions",
]
