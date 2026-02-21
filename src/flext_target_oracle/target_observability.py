"""Observability helpers for Oracle target runtime."""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager

from flext_core import FlextLogger

from .target_exceptions import (
    FlextTargetOracleAuthenticationError,
    FlextTargetOracleConnectionError,
    FlextTargetOracleProcessingError,
    FlextTargetOracleSchemaError,
)

logger = FlextLogger(__name__)


class FlextOracleError:
    """Domain-specific exception factories."""

    class Connection:
        """Connection error factories."""

        @staticmethod
        def database_unavailable(
            *,
            connection_string: str,
            error_code: str | None = None,
            recovery_strategy: str = "retry_with_backoff",
        ) -> FlextTargetOracleConnectionError:
            """Build a connection error for unavailable Oracle endpoints."""
            logger.error(
                "Oracle database unavailable",
                extra={
                    "connection_string": connection_string,
                    "error_code": error_code,
                    "recovery_strategy": recovery_strategy,
                },
            )
            return FlextTargetOracleConnectionError(
                f"Oracle database unavailable: {connection_string}",
            )

        @staticmethod
        def authentication_failed(
            *, username: str, oracle_service: str, error_code: str | None = None
        ) -> FlextTargetOracleAuthenticationError:
            """Build an authentication failure error with service context."""
            logger.error(
                "Oracle authentication failure",
                extra={
                    "username": username,
                    "oracle_service": oracle_service,
                    "error_code": error_code,
                },
            )
            return FlextTargetOracleAuthenticationError(
                f"Oracle authentication failed for {username} on {oracle_service}",
            )

    class Singer:
        """Singer protocol error factories."""

        @staticmethod
        def schema_validation_failed(
            *,
            stream_name: str,
            schema_errors: list[str],
            singer_specification: str = "1.5.0",
        ) -> FlextTargetOracleSchemaError:
            """Build a Singer schema validation failure."""
            logger.error(
                "Singer schema validation failed",
                extra={
                    "stream_name": stream_name,
                    "schema_errors": schema_errors,
                    "singer_specification": singer_specification,
                },
            )
            return FlextTargetOracleSchemaError(
                f"Schema validation failed for {stream_name}: {'; '.join(schema_errors)}",
            )

        @staticmethod
        def record_processing_failed(
            *, stream_name: str, record_count: int, failed_records: int
        ) -> FlextTargetOracleProcessingError:
            """Build a Singer record processing failure."""
            logger.error(
                "Singer record processing failed",
                extra={
                    "stream_name": stream_name,
                    "record_count": record_count,
                    "failed_records": failed_records,
                },
            )
            return FlextTargetOracleProcessingError(
                f"Record processing failed for {stream_name}: {failed_records}/{record_count}",
            )


class FlextOracleObs:
    """Runtime monitoring helpers."""

    class Monitor:
        """Monitoring utility namespace."""

        @staticmethod
        @contextmanager
        def query_performance(
            table_name: str, operation: str = "SELECT"
        ) -> Generator[dict[str, str]]:
            """Yield a mutable context while timing a query operation."""
            logger.debug("Starting query performance monitor")
            context = {"table_name": table_name, "operation": operation}
            try:
                yield context
            finally:
                logger.debug("Finished query performance monitor")

        @staticmethod
        def connection_health(
            connection_pool_size: int, active_connections: int, **context: object
        ) -> None:
            """Log Oracle connection pool health snapshots."""
            context_keys = list(context.keys())
            logger.info(
                "Oracle connection pool health",
                extra={
                    "connection_pool_size": connection_pool_size,
                    "active_connections": active_connections,
                    "context_keys": context_keys,
                },
            )


def configure_oracle_observability(
    *,
    oracle_host: str,
    oracle_service: str,
    enable_performance_monitoring: bool = True,
    enable_connection_monitoring: bool = True,
) -> None:
    """Configure runtime observability logging context."""
    logger.info(
        "Oracle observability configured",
        extra={
            "oracle_host": oracle_host,
            "oracle_service": oracle_service,
            "enable_performance_monitoring": enable_performance_monitoring,
            "enable_connection_monitoring": enable_connection_monitoring,
        },
    )


__all__ = ["FlextOracleError", "FlextOracleObs", "configure_oracle_observability"]
