"""FLEXT Target Oracle Observability - Semantic Error Handling Extensions.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import time
import uuid

from flext_core import FlextLogger, FlextTypes

from flext_target_oracle.constants import FlextTargetOracleConstants
from flext_target_oracle.target_exceptions import (
    FlextTargetOracleAuthenticationError,
    FlextTargetOracleConnectionError,
    FlextTargetOracleProcessingError,
    FlextTargetOracleSchemaError,
)

logger = FlextLogger(__name__)

# Security audit constants - moved to FlextTargetOracleConstants.Observability
# Performance monitoring thresholds - moved to FlextTargetOracleConstants.Observability


class FlextOracleError:
    """Oracle domain error namespace with semantic categorization."""

    class Connection:
        """Oracle database connection and network errors."""

        @staticmethod
        def database_unavailable(
            *,
            connection_string: str,
            error_code: str | None = None,
            recovery_strategy: str = "retry_with_backoff",
        ) -> FlextTargetOracleConnectionError:
            """Oracle database server unavailable or unreachable."""
            error = FlextTargetOracleConnectionError(
                f"Oracle database unavailable: {connection_string}",
            )
            # Log with observability integration
            logger.error(
                "Oracle database unavailable: %s (error_code=%s, recovery=%s)",
                connection_string,
                error_code,
                recovery_strategy,
                extra={"exception": "error"},
            )
            return error

        @staticmethod
        def authentication_failed(
            *,
            username: str,
            oracle_service: str,
            error_code: str | None = None,
        ) -> FlextTargetOracleAuthenticationError:
            """Oracle authentication failure with user context."""
            error = FlextTargetOracleAuthenticationError(
                f"Oracle authentication failed for user {username} on service {oracle_service}",
            )
            # Security audit logging
            logger.info(
                "Oracle authentication failure",
                user_id=username,
                action=FlextTargetOracleConstants.Observability.DATABASE_LOGIN,
                resource=oracle_service,
                outcome=FlextTargetOracleConstants.Observability.FAILURE,
                error_code=error_code,
            )
            # Metrics placeholder - removed FlextObs dependency
            return error

        @staticmethod
        def connection_timeout(
            *,
            timeout_seconds: int,
            operation: str,
        ) -> FlextTargetOracleConnectionError:
            """Oracle connection timeout during operation."""
            error = FlextTargetOracleConnectionError(
                f"Oracle connection timeout after {timeout_seconds}s during {operation}",
            )
            logger.error(
                "Oracle connection timeout",
                timeout_seconds=timeout_seconds,
                operation=operation,
                exception=error,
            )
            # Metrics placeholder - removed FlextObs dependency
            return error

    class Singer:
        """Singer protocol violations and compliance errors."""

        @staticmethod
        def schema_validation_failed(
            *,
            stream_name: str,
            schema_errors: FlextTypes.StringList,
            singer_specification: str = "1.5.0",
        ) -> FlextTargetOracleSchemaError:
            """Singer schema validation failure with detailed errors."""
            error = FlextTargetOracleSchemaError(
                f"Singer schema validation failed for stream {stream_name}: {'; '.join(schema_errors)}",
            )
            logger.error(
                "Singer schema validation failed",
                stream_name=stream_name,
                schema_errors=schema_errors,
                singer_specification=singer_specification,
                exception=error,
            )
            # Metrics placeholder - removed FlextObs dependency
            return error

        @staticmethod
        def record_processing_failed(
            *,
            stream_name: str,
            record_count: int,
            failed_records: int,
        ) -> FlextTargetOracleProcessingError:
            """Singer record processing failure with batch context."""
            error = FlextTargetOracleProcessingError(
                f"Singer record processing failed for stream {stream_name}: {failed_records}/{record_count} records failed",
            )
            logger.error(
                "Singer record processing failed",
                stream_name=stream_name,
                record_count=record_count,
                failed_records=failed_records,
                success_rate=(record_count - failed_records) / record_count,
                exception=error,
            )
            # Metrics placeholder - removed FlextObs dependency
            return error

    class Data:
        """Oracle data operations and transformation errors."""

        @staticmethod
        def sql_execution_failed(
            *,
            sql_operation: str,
            table_name: str,
            oracle_error_code: str,
            affected_rows: int = 0,
        ) -> FlextTargetOracleProcessingError:
            """Oracle SQL execution failure with operation context."""
            error = FlextTargetOracleProcessingError(
                f"Oracle SQL execution failed: {sql_operation} on {table_name} (Oracle: {oracle_error_code})",
            )
            logger.error(
                "Oracle SQL execution failed",
                sql_operation=sql_operation,
                table_name=table_name,
                oracle_error_code=oracle_error_code,
                affected_rows=affected_rows,
                exception=error,
            )
            # Metrics placeholder - removed FlextObs dependency
            return error

        @staticmethod
        def bulk_load_failed(
            *,
            table_name: str,
            batch_size: int,
            processed_records: int,
            load_method: str,
        ) -> FlextTargetOracleProcessingError:
            """Oracle bulk load operation failure."""
            error = FlextTargetOracleProcessingError(
                f"Oracle bulk load failed: {processed_records}/{batch_size} records loaded to {table_name} using {load_method}",
            )
            logger.error(
                "Oracle bulk load failed",
                table_name=table_name,
                batch_size=batch_size,
                processed_records=processed_records,
                load_method=load_method,
                success_rate=processed_records / batch_size,
                exception=error,
            )
            # Metrics placeholder - removed FlextObs dependency
            return error


class FlextOracleObs:
    """Oracle-specific observability extensions with database monitoring."""

    class Monitor:
        """Oracle database performance monitoring and health checks."""

        @classmethod
        def query_performance(
            cls,
            table_name: str,
            operation: str = "SELECT",
        ) -> object:
            """Monitor Oracle query performance with execution context."""
            correlation_id = str(uuid.uuid4())

            def _performance_context() -> object:
                # Start timing
                start_time = time.time()
                timing = {
                    "table_name": "table_name",
                    "operation": "operation",
                    "correlation_id": "correlation_id",
                }

                try:
                    yield timing
                finally:
                    # Calculate duration
                    duration = time.time() - start_time

                    # Log performance metrics
                    logger.info(
                        f"Oracle {operation} performance",
                        table_name=table_name,
                        operation=operation,
                        duration_seconds=duration,
                        correlation_id=correlation_id,
                    )

                    # Metrics and alerting placeholder - removed FlextObs dependency
                    if (
                        duration
                        > FlextTargetOracleConstants.Observability.SLOW_QUERY_THRESHOLD_SECONDS
                    ):
                        logger.warning(
                            f"Slow Oracle {operation} detected",
                            extra={
                                "table_name": "table_name",
                                "duration_seconds": "duration",
                                "threshold_seconds": FlextTargetOracleConstants.Observability.SLOW_QUERY_THRESHOLD_SECONDS,
                            },
                        )

            return _performance_context()

        @classmethod
        def connection_health(
            cls,
            connection_pool_size: int,
            active_connections: int,
            **context: object,
        ) -> None:
            """Monitor Oracle connection pool health and utilization."""
            utilization = active_connections / connection_pool_size

            logger.info(
                "Oracle connection pool health",
                pool_size=connection_pool_size,
                active_connections=active_connections,
                utilization_percent=utilization * 100,
                **context,
            )

            # Metrics and alerting placeholder - removed FlextObs dependency
            if (
                utilization
                > FlextTargetOracleConstants.Observability.HIGH_UTILIZATION_THRESHOLD
            ):
                logger.warning(
                    "High Oracle connection pool utilization",
                    extra={
                        "pool_size": "connection_pool_size",
                        "active_connections": "active_connections",
                        "utilization_percent": utilization * 100,
                    },
                )

        @classmethod
        def batch_processing_metrics(
            cls,
            *,
            stream_name: str,
            batch_size: int,
            processing_time: float,
            success_count: int,
            error_count: int,
        ) -> None:
            """Track Singer batch processing performance metrics."""
            success_rate = (
                success_count / (success_count + error_count)
                if (success_count + error_count) > 0
                else 0
            )
            throughput = success_count / processing_time if processing_time > 0 else 0

            logger.info(
                "Oracle batch processing metrics",
                stream_name=stream_name,
                batch_size=batch_size,
                processing_time=processing_time,
                success_count=success_count,
                error_count=error_count,
                success_rate=success_rate,
                throughput_records_per_second=throughput,
            )

            # Metrics placeholder - removed FlextObs dependency


def configure_oracle_observability(
    *,
    oracle_host: str,
    oracle_service: str,
    enable_performance_monitoring: bool = True,
    enable_connection_monitoring: bool = True,
) -> None:
    """Configure Oracle-specific observability with database context."""
    # Configure base observability
    # configure_observability placeholder - removed for simplicity

    # Set Oracle-specific context in FlextObs
    # Note: Without FlextContext, we log the configuration directly

    logger.info(
        "Oracle observability configured",
        oracle_host=oracle_host,
        oracle_service=oracle_service,
        performance_monitoring=enable_performance_monitoring,
        connection_monitoring=enable_connection_monitoring,
    )


__all__ = [
    "FlextOracleError",
    "FlextOracleObs",
    "configure_oracle_observability",
]
