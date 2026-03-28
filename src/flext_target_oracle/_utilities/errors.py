"""Oracle Target Exception Hierarchy - Using flext-core SOURCE OF TRUTH.

Direct usage of flext-core exception classes without duplication or factories.
Oracle-specific exceptions inherit directly from flext-core bases.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from datetime import datetime
from typing import Annotated, ClassVar, override

from flext_core import FlextExceptions, r
from pydantic import ConfigDict, Field

from flext_target_oracle import c, m, t


def _to_metadata_value(value: t.RuntimeData | None) -> t.MetadataValue:
    if isinstance(value, (str, int, float, bool, datetime)):
        return value
    if value is None:
        return ""
    return str(value)


class FlextTargetOracleErrorMetadata(m.Value):
    """Structured metadata attached to Oracle target error responses."""

    model_config: ClassVar[ConfigDict] = ConfigDict(extra="allow")

    code: Annotated[str, Field(description="Canonical error code")]
    context: Annotated[
        Mapping[str, t.MetadataValue] | None,
        Field(
            default=None,
            description="Structured error context",
        ),
    ]
    correlation_id: Annotated[
        str | None,
        Field(
            default=None,
            description="Cross-service correlation identifier",
        ),
    ]


def _extract_legacy_metadata_kwargs(
    kwargs: MutableMapping[str, t.RuntimeData],
) -> tuple[str | None, Mapping[str, t.MetadataValue] | None, str | None]:
    code_value = kwargs.pop("code", None)
    context_value = kwargs.pop("context", None)
    correlation_value = kwargs.pop("correlation_id", None)

    legacy_code = code_value if isinstance(code_value, str) else None
    legacy_correlation_id = (
        correlation_value if isinstance(correlation_value, str) else None
    )

    legacy_context: Mapping[str, t.MetadataValue] | None = None
    if isinstance(context_value, Mapping):
        legacy_context = {
            str(key): _to_metadata_value(value) for key, value in context_value.items()
        }

    return legacy_code, legacy_context, legacy_correlation_id


def _resolve_metadata(
    *,
    default_code: str,
    metadata: FlextTargetOracleErrorMetadata | None,
    legacy_code: str | None,
    legacy_context: Mapping[str, t.MetadataValue] | None,
    legacy_correlation_id: str | None,
) -> r[FlextTargetOracleErrorMetadata]:
    resolved_code = legacy_code or (metadata.code if metadata is not None else None)
    resolved_context = (
        legacy_context
        if legacy_context is not None
        else (metadata.context if metadata is not None else None)
    )
    resolved_correlation_id = (
        legacy_correlation_id
        if legacy_correlation_id is not None
        else (metadata.correlation_id if metadata is not None else None)
    )
    return r[FlextTargetOracleErrorMetadata].ok(
        value=FlextTargetOracleErrorMetadata(
            code=resolved_code or default_code,
            context=resolved_context,
            correlation_id=resolved_correlation_id,
        ),
    )


class FlextTargetOracleExceptions(FlextExceptions):
    """Oracle Target exceptions using flext-core SOURCE OF TRUTH."""

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
            metadata: FlextTargetOracleErrorMetadata | None = None,
            **kwargs: t.RuntimeData,
        ) -> None:
            """Initialize connection error with Oracle-specific context."""
            legacy_code, legacy_context, legacy_correlation_id = (
                _extract_legacy_metadata_kwargs(kwargs)
            )
            metadata_result = _resolve_metadata(
                default_code=c.CONNECTION_ERROR,
                metadata=metadata,
                legacy_code=legacy_code,
                legacy_context=legacy_context,
                legacy_correlation_id=legacy_correlation_id,
            )
            resolved_metadata = metadata_result.value
            oracle_context: MutableMapping[str, t.MetadataValue] = (
                dict(resolved_metadata.context) if resolved_metadata.context else {}
            )
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
            for key, value in kwargs.items():
                oracle_context[key] = _to_metadata_value(value)
            if resolved_metadata.correlation_id is None:
                super().__init__(
                    message=message,
                    error_code=resolved_metadata.code,
                    context=oracle_context or None,
                )
            else:
                super().__init__(
                    message=message,
                    error_code=resolved_metadata.code,
                    context=oracle_context or None,
                    _correlation_id=resolved_metadata.correlation_id,
                )
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
            metadata: FlextTargetOracleErrorMetadata | None = None,
            **kwargs: t.RuntimeData,
        ) -> None:
            """Initialize authentication error with Oracle-specific context."""
            legacy_code, legacy_context, legacy_correlation_id = (
                _extract_legacy_metadata_kwargs(kwargs)
            )
            metadata_result = _resolve_metadata(
                default_code=c.AUTHENTICATION_ERROR,
                metadata=metadata,
                legacy_code=legacy_code,
                legacy_context=legacy_context,
                legacy_correlation_id=legacy_correlation_id,
            )
            resolved_metadata = metadata_result.value
            oracle_context: MutableMapping[str, t.MetadataValue] = (
                dict(resolved_metadata.context) if resolved_metadata.context else {}
            )
            if user is not None:
                oracle_context["user"] = user
            if auth_method is not None:
                oracle_context["auth_method"] = auth_method
            if wallet_location is not None:
                oracle_context["wallet_location"] = wallet_location
            for key, value in kwargs.items():
                oracle_context[key] = _to_metadata_value(value)
            if resolved_metadata.correlation_id is None:
                super().__init__(
                    message=message,
                    error_code=resolved_metadata.code,
                    context=oracle_context or None,
                )
            else:
                super().__init__(
                    message=message,
                    error_code=resolved_metadata.code,
                    context=oracle_context or None,
                    _correlation_id=resolved_metadata.correlation_id,
                )
            self.user = oracle_context.get("user")
            auth_method_val = oracle_context.get("auth_method")
            self.auth_method = (
                str(auth_method_val) if auth_method_val is not None else None
            )
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
            error_records: Sequence[Mapping[str, t.ContainerValue]] | None = None,
            operation: str | None = None,
            metadata: FlextTargetOracleErrorMetadata | None = None,
            **kwargs: t.RuntimeData,
        ) -> None:
            """Initialize processing error with Oracle-specific context."""
            legacy_code, legacy_context, legacy_correlation_id = (
                _extract_legacy_metadata_kwargs(kwargs)
            )
            metadata_result = _resolve_metadata(
                default_code=c.PROCESSING_ERROR,
                metadata=metadata,
                legacy_code=legacy_code,
                legacy_context=legacy_context,
                legacy_correlation_id=legacy_correlation_id,
            )
            resolved_metadata = metadata_result.value
            oracle_context: MutableMapping[str, t.MetadataValue] = (
                dict(resolved_metadata.context) if resolved_metadata.context else {}
            )
            if stream_name is not None:
                oracle_context["stream_name"] = stream_name
            if record_count is not None:
                oracle_context["record_count"] = record_count
            if error_records is not None:
                oracle_context["error_records"] = str(error_records)
            if operation is not None:
                oracle_context["operation"] = operation
            for key, value in kwargs.items():
                oracle_context[key] = _to_metadata_value(value)
            if resolved_metadata.correlation_id is None:
                super().__init__(
                    message=message,
                    error_code=resolved_metadata.code,
                    context=oracle_context or None,
                )
            else:
                super().__init__(
                    message=message,
                    error_code=resolved_metadata.code,
                    context=oracle_context or None,
                    _correlation_id=resolved_metadata.correlation_id,
                )
            self.stream_name = oracle_context.get("stream_name")
            self.record_count = oracle_context.get("record_count")
            self.error_records = error_records
            operation_val = oracle_context.get("operation")
            self.operation = str(operation_val) if operation_val is not None else None

    class OracleTimeoutError(FlextExceptions.TimeoutError):
        """Oracle timeout error using flext-core foundation."""

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
            validation_errors: t.StrSequence | None = None,
            metadata: FlextTargetOracleErrorMetadata | None = None,
            **kwargs: t.RuntimeData,
        ) -> None:
            """Initialize schema error with Oracle-specific context."""
            legacy_code, legacy_context, legacy_correlation_id = (
                _extract_legacy_metadata_kwargs(kwargs)
            )
            metadata_result = _resolve_metadata(
                default_code=c.VALIDATION_ERROR,
                metadata=metadata,
                legacy_code=legacy_code,
                legacy_context=legacy_context,
                legacy_correlation_id=legacy_correlation_id,
            )
            resolved_metadata = metadata_result.value
            oracle_context: MutableMapping[str, t.MetadataValue] = (
                dict(resolved_metadata.context) if resolved_metadata.context else {}
            )
            if stream_name is not None:
                oracle_context["stream_name"] = stream_name
            if table_name is not None:
                oracle_context["table_name"] = table_name
            if schema_hash is not None:
                oracle_context["schema_hash"] = schema_hash
            if validation_errors is not None:
                oracle_context["validation_errors"] = ", ".join(validation_errors)
            for key, value in kwargs.items():
                oracle_context[key] = _to_metadata_value(value)
            super().__init__(
                message=message,
                error_code=resolved_metadata.code,
                context=oracle_context or None,
                _correlation_id=resolved_metadata.correlation_id,
            )
            self.stream_name = oracle_context.get("stream_name")
            self.table_name = oracle_context.get("table_name")
            self.schema_hash = oracle_context.get("schema_hash")
            self.validation_errors = validation_errors

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
            metadata: FlextTargetOracleErrorMetadata | None = None,
            **kwargs: t.RuntimeData,
        ) -> None:
            """Initialize SQL error with Oracle-specific context."""
            legacy_code, legacy_context, legacy_correlation_id = (
                _extract_legacy_metadata_kwargs(kwargs)
            )
            metadata_result = _resolve_metadata(
                default_code=c.OPERATION_ERROR,
                metadata=metadata,
                legacy_code=legacy_code,
                legacy_context=legacy_context,
                legacy_correlation_id=legacy_correlation_id,
            )
            resolved_metadata = metadata_result.value
            oracle_context: MutableMapping[str, t.MetadataValue] = (
                dict(resolved_metadata.context) if resolved_metadata.context else {}
            )
            if sql_statement is not None:
                oracle_context["sql_statement"] = sql_statement
            if table_name is not None:
                oracle_context["table_name"] = table_name
            if operation is not None:
                oracle_context["operation"] = operation
            for key, value in kwargs.items():
                oracle_context[key] = _to_metadata_value(value)
            super().__init__(
                message=message,
                metadata=FlextTargetOracleErrorMetadata(
                    code=resolved_metadata.code,
                    context=oracle_context or None,
                    correlation_id=resolved_metadata.correlation_id,
                ),
            )
            self.sql_statement = oracle_context.get("sql_statement")
            self.table_name = oracle_context.get("table_name")

    class RecordError(ProcessingError):
        """Oracle record processing errors."""


__all__: t.StrSequence = [
    "FlextTargetOracleErrorMetadata",
    "FlextTargetOracleExceptions",
]
