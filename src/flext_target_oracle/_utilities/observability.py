"""Observability helpers for Oracle target runtime."""

from __future__ import annotations

import typing as _t
from collections.abc import Generator
from contextlib import contextmanager
from typing import ClassVar

from flext_meltano import p, u
from flext_target_oracle import (
    FlextTargetOracleErrorMetadata,
    FlextTargetOracleExceptions as e,
    c,
)


class FlextTargetOracleUtilitiesObservability:
    """Runtime observability and error factory utilities."""

    _logger: ClassVar[p.Logger] = u.fetch_logger(__name__)

    @staticmethod
    def target_oracle_connection_authentication_failed(
        *,
        username: str,
        oracle_service: str,
        error_code: str | None = None,
    ) -> e.AuthenticationError:
        """Build an authentication failure error with service context."""
        FlextTargetOracleUtilitiesObservability._logger.error(
            "Oracle authentication failure",
            username=username,
            oracle_service=oracle_service,
            error_code=error_code or "",
        )
        return e.AuthenticationError(
            f"Oracle authentication failed for {username} on {oracle_service}",
            metadata=FlextTargetOracleErrorMetadata(
                code=error_code or c.ErrorCode.AUTHENTICATION_ERROR,
                context={
                    "user": username,
                    "oracle_service": oracle_service,
                },
                correlation_id=None,
            ),
        )

    @staticmethod
    def target_oracle_connection_database_unavailable(
        *,
        connection_string: str,
        error_code: str | None = None,
        recovery_strategy: str = "retry_with_backoff",
    ) -> e.OracleConnectionError:
        """Build a connection error for unavailable Oracle endpoints."""
        FlextTargetOracleUtilitiesObservability._logger.error(
            "Oracle database unavailable",
            connection_string=connection_string,
            error_code=error_code or "",
            recovery_strategy=recovery_strategy,
        )
        return e.OracleConnectionError(
            f"Oracle database unavailable: {connection_string}",
            metadata=FlextTargetOracleErrorMetadata(
                code=error_code or c.ErrorCode.CONNECTION_ERROR,
                context={
                    "connection_string": connection_string,
                    "recovery_strategy": recovery_strategy,
                },
                correlation_id=None,
            ),
        )

    @staticmethod
    def target_oracle_singer_record_processing_failed(
        *,
        stream_name: str,
        record_count: int,
        failed_records: int,
    ) -> e.ProcessingError:
        """Build a Singer record processing failure."""
        FlextTargetOracleUtilitiesObservability._logger.error(
            "Singer record processing failed",
            stream_name=stream_name,
            record_count=record_count,
            failed_records=failed_records,
        )
        return e.ProcessingError(
            f"Record processing failed for {stream_name}: {failed_records}/{record_count}",
            metadata=FlextTargetOracleErrorMetadata(
                code=c.ErrorCode.PROCESSING_ERROR,
                context={
                    "stream_name": stream_name,
                    "record_count": record_count,
                    "failed_records": failed_records,
                },
                correlation_id=None,
            ),
        )

    @staticmethod
    def target_oracle_singer_schema_validation_failed(
        *,
        stream_name: str,
        schema_errors: _t.t.StrSequence,
        singer_specification: str = "1.5.0",
    ) -> e.SchemaError:
        """Build a Singer schema validation failure."""
        FlextTargetOracleUtilitiesObservability._logger.error(
            "Singer schema validation failed",
            stream_name=stream_name,
            schema_errors="; ".join(schema_errors),
            singer_specification=singer_specification,
        )

        return e.SchemaError(
            f"Schema validation failed for {stream_name}: {'; '.join(schema_errors)}",
            metadata=FlextTargetOracleErrorMetadata(
                code=c.ErrorCode.VALIDATION_ERROR,
                context={
                    "stream_name": stream_name,
                    "schema_errors": "; ".join(schema_errors),
                    "singer_specification": singer_specification,
                },
                correlation_id=None,
            ),
        )

    @staticmethod
    def target_oracle_monitor_connection_health(
        connection_pool_size: int,
        active_connections: int,
        **context: str | float | bool | None,
    ) -> None:
        """Log Oracle connection pool health snapshots."""
        context_keys = list(context.keys())
        FlextTargetOracleUtilitiesObservability._logger.info(
            "Oracle connection pool health",
            connection_pool_size=connection_pool_size,
            active_connections=active_connections,
            context_keys=",".join(context_keys),
        )

    @staticmethod
    @contextmanager
    def target_oracle_monitor_query_performance(
        table_name: str,
        operation: str = "SELECT",
    ) -> Generator[_t.t.StrMapping]:
        """Yield a mutable context while timing a query operation."""
        FlextTargetOracleUtilitiesObservability._logger.debug(
            "Starting query performance monitor",
        )
        context_data = {"table_name": table_name, "operation": operation}
        try:
            yield context_data
        finally:
            FlextTargetOracleUtilitiesObservability._logger.debug(
                "Finished query performance monitor",
            )

    @staticmethod
    def configure_oracle_observability(
        *,
        oracle_host: str,
        oracle_service: str,
        enable_performance_monitoring: bool = True,
        enable_connection_monitoring: bool = True,
    ) -> None:
        """Configure runtime observability logging context."""
        FlextTargetOracleUtilitiesObservability._logger.info(
            "Oracle observability configured",
            oracle_host=oracle_host,
            oracle_service=oracle_service,
            enable_performance_monitoring=enable_performance_monitoring,
            enable_connection_monitoring=enable_connection_monitoring,
        )


__all__: list[str] = ["FlextTargetOracleUtilitiesObservability"]
