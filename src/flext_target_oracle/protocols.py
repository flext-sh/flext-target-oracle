"""Target Oracle protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_core import FlextProtocols, FlextResult


class FlextTargetOracleProtocols(FlextProtocols):
    """Target Oracle protocols extending FlextProtocols with Oracle target-specific interfaces.

    This class provides protocol definitions for Singer target operations with Oracle database integration,
    data transformation, connection management, and enterprise Oracle authentication patterns.
    """

    @runtime_checkable
    class TargetProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for Oracle target operations."""

        def create_target(self, config: dict[str, object]) -> FlextResult[object]:
            """Create Oracle target instance.

            Args:
                config: Target configuration parameters

            Returns:
                FlextResult[object]: Target instance or error

            """
            ...

        def load_records(
            self,
            records: list[dict[str, object]],
            config: dict[str, object],
            *,
            stream_type: str = "data",
        ) -> FlextResult[int]:
            """Load records to Oracle database.

            Args:
                records: Records to load into Oracle
                config: Oracle target configuration
                stream_type: Type of stream being processed

            Returns:
                FlextResult[int]: Number of records loaded or error

            """
            ...

        def validate_target_config(
            self, config: dict[str, object]
        ) -> FlextResult[bool]:
            """Validate Oracle target configuration.

            Args:
                config: Configuration to validate

            Returns:
                FlextResult[bool]: Configuration validation status

            """
            ...

        def get_target_capabilities(self) -> FlextResult[dict[str, object]]:
            """Get Oracle target capabilities.

            Returns:
                FlextResult[dict[str, object]]: Target capabilities or error

            """
            ...

    @runtime_checkable
    class ConnectionProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for Oracle connection management operations."""

        def test_connection(self) -> FlextResult[None]:
            """Test Oracle database connection.

            Returns:
                FlextResult[None]: Connection test result or error

            """
            ...

        def get_connection_info(self) -> FlextResult[dict[str, object]]:
            """Get Oracle connection information.

            Returns:
                FlextResult[dict[str, object]]: Connection information or error

            """
            ...

        def establish_connection(
            self, config: dict[str, object]
        ) -> FlextResult[object]:
            """Establish Oracle connection.

            Args:
                config: Connection configuration

            Returns:
                FlextResult[object]: Connection instance or error

            """
            ...

        def close_connection(self, connection: object) -> FlextResult[bool]:
            """Close Oracle connection.

            Args:
                connection: Connection to close

            Returns:
                FlextResult[bool]: Close operation success status

            """
            ...

        def validate_credentials(self, config: dict[str, object]) -> FlextResult[bool]:
            """Validate Oracle credentials.

            Args:
                config: Configuration with credentials

            Returns:
                FlextResult[bool]: Credential validation status

            """
            ...

    @runtime_checkable
    class SchemaProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for Oracle schema management operations."""

        def ensure_table_exists(
            self,
            stream: dict[str, object],
            schema: dict[str, object],
            key_properties: list[str] | None = None,
        ) -> FlextResult[None]:
            """Ensure table exists for Singer stream.

            Args:
                stream: Singer stream definition
                schema: Table schema definition
                key_properties: Primary key properties

            Returns:
                FlextResult[None]: Success or error

            """
            ...

        def get_table_columns(
            self,
            table_name: str,
            schema_name: str,
        ) -> FlextResult[list[dict[str, object]]]:
            """Get table column definitions.

            Args:
                table_name: Name of the table
                schema_name: Name of the schema

            Returns:
                FlextResult[list[dict[str, object]]]: Column definitions or error

            """
            ...

        def validate_table_schema(
            self, table_name: str, schema: dict[str, object]
        ) -> FlextResult[bool]:
            """Validate table schema against Oracle constraints.

            Args:
                table_name: Name of the table
                schema: Schema to validate

            Returns:
                FlextResult[bool]: Schema validation status

            """
            ...

        def create_table_from_schema(
            self,
            table_name: str,
            schema: dict[str, object],
            primary_keys: list[str] | None = None,
        ) -> FlextResult[dict[str, object]]:
            """Create Oracle table from Singer schema.

            Args:
                table_name: Name of the table to create
                schema: Singer schema definition
                primary_keys: Primary key columns

            Returns:
                FlextResult[dict[str, object]]: Table creation result or error

            """
            ...

    @runtime_checkable
    class BatchProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for Oracle batch processing operations."""

        def add_record(
            self,
            stream_name: str,
            record: dict[str, object],
        ) -> FlextResult[None]:
            """Add record to batch processing queue.

            Args:
                stream_name: Name of the stream
                record: Record to add to batch

            Returns:
                FlextResult[None]: Success or error

            """
            ...

        def flush_batch(self, stream_name: str) -> FlextResult[None]:
            """Flush pending batch for stream.

            Args:
                stream_name: Name of the stream to flush

            Returns:
                FlextResult[None]: Flush operation result or error

            """
            ...

        def flush_all_batches(self) -> FlextResult[dict[str, object]]:
            """Flush all pending batches.

            Returns:
                FlextResult[dict[str, object]]: Load statistics or error

            """
            ...

        def get_batch_size(self, stream_name: str) -> FlextResult[int]:
            """Get current batch size for stream.

            Args:
                stream_name: Name of the stream

            Returns:
                FlextResult[int]: Current batch size or error

            """
            ...

        def optimize_batch_size(
            self, stream_name: str, performance_metrics: dict[str, object]
        ) -> FlextResult[int]:
            """Optimize batch size based on performance metrics.

            Args:
                stream_name: Name of the stream
                performance_metrics: Performance metrics for optimization

            Returns:
                FlextResult[int]: Optimal batch size or error

            """
            ...

    @runtime_checkable
    class RecordProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for Oracle record transformation operations."""

        def transform_record(
            self,
            record: dict[str, object],
            stream: dict[str, object],
        ) -> FlextResult[dict[str, object]]:
            """Transform Singer record for Oracle storage.

            Args:
                record: Singer record to transform
                stream: Stream definition

            Returns:
                FlextResult[dict[str, object]]: Transformed record or error

            """
            ...

        def validate_record(
            self,
            record: dict[str, object],
            schema: dict[str, object],
        ) -> FlextResult[None]:
            """Validate record against schema.

            Args:
                record: Record to validate
                schema: Schema definition

            Returns:
                FlextResult[None]: Validation result or error

            """
            ...

        def map_singer_to_oracle_types(
            self, record: dict[str, object], type_mapping: dict[str, str]
        ) -> FlextResult[dict[str, object]]:
            """Map Singer record types to Oracle types.

            Args:
                record: Singer record with source data
                type_mapping: Type mapping configuration

            Returns:
                FlextResult[dict[str, object]]: Oracle-typed record or error

            """
            ...

        def sanitize_record_for_oracle(
            self, record: dict[str, object]
        ) -> FlextResult[dict[str, object]]:
            """Sanitize record for Oracle database constraints.

            Args:
                record: Record to sanitize

            Returns:
                FlextResult[dict[str, object]]: Sanitized record or error

            """
            ...

    @runtime_checkable
    class SingerProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for Singer protocol operations."""

        def process_schema_message(
            self, message: dict[str, object]
        ) -> FlextResult[dict[str, object]]:
            """Process Singer SCHEMA message.

            Args:
                message: Singer SCHEMA message

            Returns:
                FlextResult[dict[str, object]]: Schema processing result or error

            """
            ...

        def process_record_message(
            self, message: dict[str, object]
        ) -> FlextResult[dict[str, object]]:
            """Process Singer RECORD message.

            Args:
                message: Singer RECORD message

            Returns:
                FlextResult[dict[str, object]]: Record processing result or error

            """
            ...

        def process_state_message(
            self, message: dict[str, object]
        ) -> FlextResult[dict[str, object]]:
            """Process Singer STATE message.

            Args:
                message: Singer STATE message

            Returns:
                FlextResult[dict[str, object]]: State processing result or error

            """
            ...

        def validate_singer_message(
            self, message: dict[str, object]
        ) -> FlextResult[bool]:
            """Validate Singer message format.

            Args:
                message: Singer message to validate

            Returns:
                FlextResult[bool]: Message validation status

            """
            ...

        def get_singer_capabilities(self) -> FlextResult[dict[str, object]]:
            """Get Singer target capabilities.

            Returns:
                FlextResult[dict[str, object]]: Singer capabilities or error

            """
            ...

    @runtime_checkable
    class PerformanceProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for Oracle performance optimization operations."""

        def optimize_connection_pool(
            self, pool_config: dict[str, object], usage_metrics: dict[str, object]
        ) -> FlextResult[dict[str, object]]:
            """Optimize Oracle connection pool for performance.

            Args:
                pool_config: Connection pool configuration
                usage_metrics: Pool usage metrics

            Returns:
                FlextResult[dict[str, object]]: Pool optimization result or error

            """
            ...

        def monitor_query_performance(
            self, query: str, execution_time: float
        ) -> FlextResult[dict[str, object]]:
            """Monitor Oracle query performance.

            Args:
                query: SQL query executed
                execution_time: Query execution time in seconds

            Returns:
                FlextResult[dict[str, object]]: Performance metrics or error

            """
            ...

        def optimize_insert_performance(
            self, table_name: str, record_count: int, current_metrics: dict[str, object]
        ) -> FlextResult[dict[str, object]]:
            """Optimize Oracle insert operations performance.

            Args:
                table_name: Target table name
                record_count: Number of records to insert
                current_metrics: Current performance metrics

            Returns:
                FlextResult[dict[str, object]]: Performance optimization result or error

            """
            ...

        def get_performance_metrics(self) -> FlextResult[dict[str, object]]:
            """Get Oracle target performance metrics.

            Returns:
                FlextResult[dict[str, object]]: Performance metrics or error

            """
            ...

    @runtime_checkable
    class SecurityProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for Oracle security operations."""

        def encrypt_credentials(
            self, credentials: dict[str, object]
        ) -> FlextResult[dict[str, object]]:
            """Encrypt Oracle credentials for secure storage.

            Args:
                credentials: Raw credentials to encrypt

            Returns:
                FlextResult[dict[str, object]]: Encrypted credentials or error

            """
            ...

        def validate_ssl_connection(
            self, config: dict[str, object]
        ) -> FlextResult[bool]:
            """Validate SSL/TLS connection configuration.

            Args:
                config: SSL connection configuration

            Returns:
                FlextResult[bool]: SSL validation status

            """
            ...

        def audit_database_operations(
            self, operation: str, details: dict[str, object]
        ) -> FlextResult[bool]:
            """Audit Oracle database operations for security compliance.

            Args:
                operation: Database operation being audited
                details: Operation details

            Returns:
                FlextResult[bool]: Audit logging success status

            """
            ...

        def validate_access_permissions(
            self, user: str, operation: str, resource: str
        ) -> FlextResult[bool]:
            """Validate user access permissions for Oracle operations.

            Args:
                user: User performing operation
                operation: Type of operation
                resource: Resource being accessed

            Returns:
                FlextResult[bool]: Permission validation status

            """
            ...

    @runtime_checkable
    class MonitoringProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for Oracle monitoring operations."""

        def track_operation_metrics(
            self, operation: str, duration: float, *, success: bool
        ) -> FlextResult[bool]:
            """Track Oracle operation metrics.

            Args:
                operation: Operation name
                duration: Operation duration in seconds
                success: Operation success status

            Returns:
                FlextResult[bool]: Metric tracking success status

            """
            ...

        def get_health_status(self) -> FlextResult[dict[str, object]]:
            """Get Oracle target health status.

            Returns:
                FlextResult[dict[str, object]]: Health status or error

            """
            ...

        def create_performance_report(
            self, time_range: str, *, include_details: bool = False
        ) -> FlextResult[dict[str, object]]:
            """Create Oracle performance report.

            Args:
                time_range: Time range for report
                include_details: Include detailed metrics

            Returns:
                FlextResult[dict[str, object]]: Performance report or error

            """
            ...

        def alert_on_threshold_breach(
            self, metric_name: str, threshold: float, current_value: float
        ) -> FlextResult[bool]:
            """Alert when performance thresholds are breached.

            Args:
                metric_name: Name of the metric
                threshold: Threshold value
                current_value: Current metric value

            Returns:
                FlextResult[bool]: Alert creation success status

            """
            ...


__all__ = [
    "FlextTargetOracleProtocols",
]
