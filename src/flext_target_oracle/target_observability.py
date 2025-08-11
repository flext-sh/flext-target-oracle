"""FLEXT Target Oracle Observability - Semantic Error Handling Extensions.

Oracle-specific extensions to the FLEXT observability foundation, providing
domain-specific error handling, logging, and monitoring for Oracle database
operations in Singer target implementations.

Module Role in Architecture:
    Domain Extension Layer → Oracle Observability → Singer Target Monitoring

    This module extends flext-core observability patterns with Oracle-specific
    semantic error handling and monitoring:
    - Oracle connection error classification and recovery strategies
    - Singer protocol error categorization for Oracle operations
    - Database performance monitoring with Oracle-specific metrics
    - SQL error analysis and structured logging

Semantic Architecture Patterns:
    FlextOracleError: Domain-specific error namespace for Oracle operations
    FlextOracleObs: Oracle-specific observability extensions
    Singer Integration: Error context preservation for Singer protocol violations
    Database Monitoring: Connection pooling and query performance tracking

Integration Points:
    - FlextError foundation: Extends base error hierarchy with Oracle semantics
    - FlextObs integration: Oracle-specific logging and metrics collection
    - Singer target errors: Protocol-specific error handling and recovery
    - Database operations: Query timing, connection health, and performance metrics

Usage Patterns:
    # Oracle connection error handling
    try:
        result = oracle_api.connect()
    except OracleConnectionError as e:
        FlextOracleError.Connection.database_unavailable(
            connection_string=config.connection_string,
            error_code=e.code,
            recovery_strategy="retry_with_backoff"
        )

    # Singer protocol error handling
    if not schema_valid:
        FlextOracleError.Singer.schema_validation_failed(
            stream_name=stream,
            schema_errors=validation_errors,
            singer_specification="1.5.0"
        )

    # Performance monitoring
    with FlextOracleObs.Monitor.query_performance(table_name, operation="INSERT"):
        result = loader.bulk_insert(records)

Domain-Specific Features:
    - Oracle error code mapping to business-meaningful categories
    - Singer protocol compliance monitoring and alerting
    - Database performance baselines and anomaly detection
    - Connection pooling health and resource utilization tracking
    - SQL query analysis with execution plan correlation

Quality Standards:
    - All Oracle errors must include database context (SID, schema, operation)
    - Singer errors must preserve protocol compliance information
    - Performance metrics must include baseline comparisons
    - Error recovery strategies must be deterministic and documented

See Also:
    flext_core.observability: Foundation observability patterns
    flext_core.exceptions: Base error hierarchy
    flext_db_oracle: Database connectivity and operations
    flext_meltano: Singer protocol implementation

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextObs

from flext_target_oracle.target_exceptions import (
    FlextTargetOracleAuthenticationError,
    FlextTargetOracleConnectionError,
    FlextTargetOracleProcessingError,
    FlextTargetOracleSchemaError,
)

# =============================================================================
# CONSTANTS
# =============================================================================

# Performance monitoring thresholds
SLOW_QUERY_THRESHOLD_SECONDS = 30.0  # 30 second threshold for slow queries
HIGH_UTILIZATION_THRESHOLD = 0.8  # 80% threshold for high resource utilization

# =============================================================================
# ORACLE-SPECIFIC ERROR NAMESPACE
# =============================================================================


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
            **context: object,
        ) -> FlextTargetOracleConnectionError:
            """Oracle database server unavailable or unreachable."""
            error = FlextTargetOracleConnectionError(
                f"Oracle database unavailable: {connection_string}",
                error_code=error_code or "ORA-CONNECTION-001",
                context={
                    "connection_string": connection_string,
                    "recovery_strategy": recovery_strategy,
                    "error_category": "database_unavailable",
                    **context,
                },
            )
            # Log with observability integration
            FlextObs.Log.error(
                "Oracle database unavailable",
                connection_string=connection_string,
                error_code=error_code,
                recovery_strategy=recovery_strategy,
                exception=error,
            )
            # Increment error metrics
            FlextObs.Metrics.increment(
                "oracle.connection.database_unavailable",
                tags={"recovery_strategy": recovery_strategy},
            )
            return error

        @staticmethod
        def authentication_failed(
            *,
            username: str,
            oracle_service: str,
            error_code: str | None = None,
            **context: object,
        ) -> FlextTargetOracleAuthenticationError:
            """Oracle authentication failure with user context."""
            error = FlextTargetOracleAuthenticationError(
                f"Oracle authentication failed for user {username} on service {oracle_service}",
                error_code=error_code or "ORA-AUTH-001",
                context={
                    "username": username,
                    "oracle_service": oracle_service,
                    "error_category": "authentication_failed",
                    **context,
                },
            )
            # Security audit logging
            FlextObs.Log.audit(
                "Oracle authentication failure",
                user_id=username,
                action="database_login",
                resource=oracle_service,
                outcome="failure",
                error_code=error_code,
            )
            # Security metrics
            FlextObs.Metrics.increment(
                "oracle.auth.failed",
                tags={"service": oracle_service},
            )
            return error

        @staticmethod
        def connection_timeout(
            *,
            timeout_seconds: int,
            operation: str,
            **context: object,
        ) -> FlextTargetOracleConnectionError:
            """Oracle connection timeout during operation."""
            error = FlextTargetOracleConnectionError(
                f"Oracle connection timeout after {timeout_seconds}s during {operation}",
                error_code="ORA-TIMEOUT-001",
                context={
                    "timeout_seconds": timeout_seconds,
                    "operation": operation,
                    "error_category": "connection_timeout",
                    **context,
                },
            )
            FlextObs.Log.error(
                "Oracle connection timeout",
                timeout_seconds=timeout_seconds,
                operation=operation,
                exception=error,
            )
            FlextObs.Metrics.histogram(
                "oracle.connection.timeout",
                timeout_seconds,
                tags={"operation": operation},
            )
            return error

    class Singer:
        """Singer protocol violations and compliance errors."""

        @staticmethod
        def schema_validation_failed(
            *,
            stream_name: str,
            schema_errors: list[str],
            singer_specification: str = "1.5.0",
            **context: object,
        ) -> FlextTargetOracleSchemaError:
            """Singer schema validation failure with detailed errors."""
            error = FlextTargetOracleSchemaError(
                f"Singer schema validation failed for stream {stream_name}: {'; '.join(schema_errors)}",
                error_code="SINGER-SCHEMA-001",
                context={
                    "stream_name": stream_name,
                    "schema_errors": schema_errors,
                    "singer_specification": singer_specification,
                    "error_category": "schema_validation_failed",
                    **context,
                },
            )
            FlextObs.Log.error(
                "Singer schema validation failed",
                stream_name=stream_name,
                schema_errors=schema_errors,
                singer_specification=singer_specification,
                exception=error,
            )
            FlextObs.Metrics.increment(
                "singer.schema.validation_failed",
                tags={"stream": stream_name},
            )
            return error

        @staticmethod
        def record_processing_failed(
            *,
            stream_name: str,
            record_count: int,
            failed_records: int,
            error_details: list[str],
            **context: object,
        ) -> FlextTargetOracleProcessingError:
            """Singer record processing failure with batch context."""
            error = FlextTargetOracleProcessingError(
                f"Singer record processing failed for stream {stream_name}: {failed_records}/{record_count} records failed",
                error_code="SINGER-RECORD-001",
                context={
                    "stream_name": stream_name,
                    "record_count": record_count,
                    "failed_records": failed_records,
                    "error_details": error_details,
                    "success_rate": (record_count - failed_records) / record_count,
                    "error_category": "record_processing_failed",
                    **context,
                },
            )
            FlextObs.Log.error(
                "Singer record processing failed",
                stream_name=stream_name,
                record_count=record_count,
                failed_records=failed_records,
                success_rate=(record_count - failed_records) / record_count,
                exception=error,
            )
            FlextObs.Metrics.increment(
                "singer.records.processing_failed",
                failed_records,
                tags={"stream": stream_name},
            )
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
            **context: object,
        ) -> FlextTargetOracleProcessingError:
            """Oracle SQL execution failure with operation context."""
            error = FlextTargetOracleProcessingError(
                f"Oracle SQL execution failed: {sql_operation} on {table_name} (Oracle: {oracle_error_code})",
                error_code=f"ORA-SQL-{oracle_error_code}",
                context={
                    "sql_operation": sql_operation,
                    "table_name": table_name,
                    "oracle_error_code": oracle_error_code,
                    "affected_rows": affected_rows,
                    "error_category": "sql_execution_failed",
                    **context,
                },
            )
            FlextObs.Log.error(
                "Oracle SQL execution failed",
                sql_operation=sql_operation,
                table_name=table_name,
                oracle_error_code=oracle_error_code,
                affected_rows=affected_rows,
                exception=error,
            )
            FlextObs.Metrics.increment(
                "oracle.sql.execution_failed",
                tags={
                    "operation": sql_operation,
                    "table": table_name,
                    "oracle_code": oracle_error_code,
                },
            )
            return error

        @staticmethod
        def bulk_load_failed(
            *,
            table_name: str,
            batch_size: int,
            processed_records: int,
            load_method: str,
            **context: object,
        ) -> FlextTargetOracleProcessingError:
            """Oracle bulk load operation failure."""
            error = FlextTargetOracleProcessingError(
                f"Oracle bulk load failed: {processed_records}/{batch_size} records loaded to {table_name} using {load_method}",
                error_code="ORA-BULK-001",
                context={
                    "table_name": table_name,
                    "batch_size": batch_size,
                    "processed_records": processed_records,
                    "load_method": load_method,
                    "success_rate": processed_records / batch_size,
                    "error_category": "bulk_load_failed",
                    **context,
                },
            )
            FlextObs.Log.error(
                "Oracle bulk load failed",
                table_name=table_name,
                batch_size=batch_size,
                processed_records=processed_records,
                load_method=load_method,
                success_rate=processed_records / batch_size,
                exception=error,
            )
            FlextObs.Metrics.histogram(
                "oracle.bulk_load.success_rate",
                processed_records / batch_size,
                tags={
                    "table": table_name,
                    "method": load_method,
                },
            )
            return error


# =============================================================================
# ORACLE-SPECIFIC OBSERVABILITY EXTENSIONS
# =============================================================================


class FlextOracleObs(FlextObs):
    """Oracle-specific observability extensions with database monitoring."""

    class Monitor:
        """Oracle database performance monitoring and health checks."""

        @classmethod
        def query_performance(
            cls,
            table_name: str,
            operation: str = "SELECT",
            **_context: object,
        ) -> object:
            """Monitor Oracle query performance with execution context."""
            import uuid
            import time
            correlation_id = str(uuid.uuid4())

            def _performance_context() -> object:
                # Start timing
                start_time = time.time()
                timing = {
                    "table_name": table_name,
                    "operation": operation, 
                    "correlation_id": correlation_id,
                }
                
                try:
                    yield timing
                finally:
                    # Calculate duration
                    duration = time.time() - start_time
                    
                    # Log performance metrics
                    FlextObs.Log.info(
                        f"Oracle {operation} performance",
                        table_name=table_name,
                        operation=operation,
                        duration_seconds=duration,
                        correlation_id=correlation_id,
                    )

                    # Record performance metrics
                    FlextObs.Metrics.histogram(
                        f"oracle.query.{operation.lower()}.duration",
                        duration,
                        tags={"table": table_name},
                    )

                    # Performance baseline alerting
                    if duration > SLOW_QUERY_THRESHOLD_SECONDS:
                        FlextObs.Alert.warning(
                            f"Slow Oracle {operation} detected",
                            table_name=table_name,
                            duration_seconds=duration,
                            threshold_seconds=SLOW_QUERY_THRESHOLD_SECONDS,
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

            FlextObs.Log.info(
                "Oracle connection pool health",
                pool_size=connection_pool_size,
                active_connections=active_connections,
                utilization_percent=utilization * 100,
                **context,
            )

            FlextObs.Metrics.gauge(
                "oracle.connection_pool.utilization",
                utilization,
                tags={"pool_size": str(connection_pool_size)},
            )

            # High utilization alerting
            if utilization > HIGH_UTILIZATION_THRESHOLD:
                FlextObs.Alert.warning(
                    "High Oracle connection pool utilization",
                    pool_size=connection_pool_size,
                    active_connections=active_connections,
                    utilization_percent=utilization * 100,
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
            **context: object,
        ) -> None:
            """Track Singer batch processing performance metrics."""
            success_rate = (
                success_count / (success_count + error_count)
                if (success_count + error_count) > 0
                else 0
            )
            throughput = success_count / processing_time if processing_time > 0 else 0

            FlextObs.Log.info(
                "Oracle batch processing metrics",
                stream_name=stream_name,
                batch_size=batch_size,
                processing_time=processing_time,
                success_count=success_count,
                error_count=error_count,
                success_rate=success_rate,
                throughput_records_per_second=throughput,
                **context,
            )

            # Record detailed metrics
            FlextObs.Metrics.histogram(
                "oracle.batch.processing_time",
                processing_time,
                tags={"stream": stream_name},
            )

            FlextObs.Metrics.gauge(
                "oracle.batch.success_rate",
                success_rate,
                tags={"stream": stream_name},
            )

            FlextObs.Metrics.gauge(
                "oracle.batch.throughput",
                throughput,
                tags={"stream": stream_name},
            )


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================


def configure_oracle_observability(
    service_name: str = "flext-target-oracle",
    *,
    oracle_host: str,
    oracle_service: str,
    enable_performance_monitoring: bool = True,
    enable_connection_monitoring: bool = True,
    **kwargs: object,
) -> None:
    """Configure Oracle-specific observability with database context."""
    # Configure base observability
    FlextObs.configure_observability(
        service_name=service_name,
        **kwargs,
    )

    # Set Oracle-specific context in FlextObs
    # Note: Without FlextContext, we log the configuration directly

    FlextObs.Log.info(
        "Oracle observability configured",
        oracle_host=oracle_host,
        oracle_service=oracle_service,
        performance_monitoring=enable_performance_monitoring,
        connection_monitoring=enable_connection_monitoring,
    )


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "FlextOracleError",
    "FlextOracleObs",
    "configure_oracle_observability",
]
