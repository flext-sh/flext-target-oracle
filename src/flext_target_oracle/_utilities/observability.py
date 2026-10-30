"""Observability helpers for Oracle target runtime.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from contextlib import contextmanager
from typing import TYPE_CHECKING, ClassVar

from flext_meltano import u

from flext_target_oracle import c, m, p
from flext_target_oracle._utilities import FlextTargetOracleUtilitiesErrors

if TYPE_CHECKING:
    from collections.abc import Generator


class FlextTargetOracleUtilitiesObservability:
    """Runtime observability and error factory utilities."""

    logger: ClassVar[p.Logger] = u.fetch_logger(__name__)

    @staticmethod
    def target_oracle_connection_authentication_failed(
        *,
        username: str,
        oracle_service: str,
        error_code: str | None = None,
    ) -> FlextTargetOracleUtilitiesErrors.Exceptions.AuthenticationError:
        """Build an authentication failure error with service context.

        Args:
            username: User name that failed authentication.
            oracle_service: Oracle service the authentication targeted.
            error_code: Optional error code overriding the default.

        Returns:
            The authentication failure exception with error metadata.

        """
        FlextTargetOracleUtilitiesObservability.logger.error(
            "Oracle authentication failure",
            username=username,
            oracle_service=oracle_service,
            error_code=error_code or "",
        )
        return FlextTargetOracleUtilitiesErrors.Exceptions.AuthenticationError(
            f"Oracle authentication failed for {username} on {oracle_service}",
            metadata=m.TargetOracle.ErrorMetadata(
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
    ) -> FlextTargetOracleUtilitiesErrors.Exceptions.OracleConnectionError:
        """Build a connection error for unavailable Oracle endpoints.

        Args:
            connection_string: Connection string that could not be reached.
            error_code: Optional error code overriding the default.
            recovery_strategy: Recovery strategy recorded in the metadata.

        Returns:
            The connection failure exception with error metadata.

        """
        FlextTargetOracleUtilitiesObservability.logger.error(
            "Oracle database unavailable",
            connection_string=connection_string,
            error_code=error_code or "",
            recovery_strategy=recovery_strategy,
        )
        return FlextTargetOracleUtilitiesErrors.Exceptions.OracleConnectionError(
            f"Oracle database unavailable: {connection_string}",
            metadata=m.TargetOracle.ErrorMetadata(
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
    ) -> FlextTargetOracleUtilitiesErrors.Exceptions.ProcessingError:
        """Build a Singer record processing failure.

        Args:
            stream_name: Name of the Singer stream being processed.
            record_count: Total records in the failed batch.
            failed_records: Number of records that failed processing.

        Returns:
            The processing failure exception with error metadata.

        """
        FlextTargetOracleUtilitiesObservability.logger.error(
            "Singer record processing failed",
            stream_name=stream_name,
            record_count=record_count,
            failed_records=failed_records,
        )
        return FlextTargetOracleUtilitiesErrors.Exceptions.ProcessingError(
            "Record processing failed for %s: %s/%s",
            stream_name,
            failed_records,
            record_count,
            metadata=m.TargetOracle.ErrorMetadata(
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
        schema_errors: Sequence[str],
        singer_specification: str = "1.5.0",
    ) -> FlextTargetOracleUtilitiesErrors.Exceptions.SchemaError:
        """Build a Singer schema validation failure.

        Args:
            stream_name: Name of the Singer stream whose schema failed.
            schema_errors: Human-readable schema validation errors.
            singer_specification: Singer specification version assumed.

        Returns:
            The schema failure exception with error metadata.

        """
        FlextTargetOracleUtilitiesObservability.logger.error(
            "Singer schema validation failed",
            stream_name=stream_name,
            schema_errors="; ".join(schema_errors),
            singer_specification=singer_specification,
        )

        return FlextTargetOracleUtilitiesErrors.Exceptions.SchemaError(
            f"Schema validation failed for {stream_name}: {'; '.join(schema_errors)}",
            metadata=m.TargetOracle.ErrorMetadata(
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
        """Log Oracle connection pool health snapshots.

        Args:
            connection_pool_size: Configured pool size.
            active_connections: Currently open connections.
            **context: Optional extra context keys logged by name.

        """
        context_keys = list(context.keys())
        FlextTargetOracleUtilitiesObservability.logger.info(
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
    ) -> Generator[Mapping[str, str]]:
        """Yield a mutable context while timing a query operation.

        Args:
            table_name: Table the operation targets.
            operation: Operation label recorded in the context.

        Yields:
            The mutable context mapping updated by the timed operation.

        """
        FlextTargetOracleUtilitiesObservability.logger.debug(
            "Starting query performance monitor",
        )
        context_data = {"table_name": table_name, c.ContextScope.OPERATION: operation}
        try:
            yield context_data
        finally:
            FlextTargetOracleUtilitiesObservability.logger.debug(
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
        """Configure runtime observability logging context.

        Args:
            oracle_host: Oracle host recorded in the log context.
            oracle_service: Oracle service recorded in the log context.
            enable_performance_monitoring: Whether to log performance
                monitoring activation.
            enable_connection_monitoring: Whether to log connection
                monitoring activation.

        """
        FlextTargetOracleUtilitiesObservability.logger.info(
            "Oracle observability configured",
            oracle_host=oracle_host,
            oracle_service=oracle_service,
            enable_performance_monitoring=enable_performance_monitoring,
            enable_connection_monitoring=enable_connection_monitoring,
        )


__all__: list[str] = ["FlextTargetOracleUtilitiesObservability"]
