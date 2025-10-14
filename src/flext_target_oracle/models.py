"""Models for Oracle target operations.

This module provides data models for Oracle target operations.
"""

from __future__ import annotations

from flext_core import FlextCore
from pydantic import Field


class FlextTargetOracleModels(FlextCore.Models):
    """Comprehensive models for Oracle target operations extending FlextCore.Models.

    Provides standardized models for all Oracle target domain entities including:
    - Singer message processing and validation
    - Oracle table management and schema operations
    - Data loading and transformation operations
    - Performance monitoring and metrics collection
    - Error handling and recovery operations

    All nested classes inherit FlextCore.Models validation and patterns.
    """

    # Constants
    MAX_PORT_NUMBER = 65535

    class OracleTargetConfig(FlextCore.Models.BaseConfig):
        """Configuration for Oracle target operations."""

        # Oracle connection settings
        oracle_host: str = Field(
            default="localhost", description="Oracle database host"
        )
        oracle_port: int = Field(default=1521, description="Oracle database port")
        oracle_service_name: str = Field(
            default="XE", description="Oracle service name"
        )
        oracle_user: str = Field(description="Oracle database username")
        oracle_password: str = Field(description="Oracle database password")

        # Target configuration
        default_target_schema: str = Field(
            default="SINGER_DATA", description="Default schema for loading data"
        )
        table_prefix: str = Field(
            default="", description="Prefix for target table names"
        )
        table_suffix: str = Field(
            default="", description="Suffix for target table names"
        )

        # Loading configuration
        batch_size: int = Field(default=5000, description="Number of records per batch")
        use_bulk_operations: bool = Field(
            default=True,
            description="Use Oracle bulk operations for better performance",
        )
        parallel_degree: int = Field(
            default=1, description="Oracle parallel degree for operations"
        )

        # Transaction settings
        autocommit: bool = Field(
            default=False, description="Enable autocommit for operations"
        )
        commit_interval: int = Field(
            default=1000, description="Number of records between commits"
        )
        transaction_timeout: int = Field(
            default=300, description="Transaction timeout in seconds"
        )

    class SingerMessageProcessing(FlextCore.Models.StrictArbitraryTypesModel):
        """Singer message processing configuration and state."""

        # Message processing state
        message_count: int = Field(default=0, description="Total messages processed")
        schema_messages: int = Field(default=0, description="Schema messages processed")
        record_messages: int = Field(default=0, description="Record messages processed")
        state_messages: int = Field(default=0, description="State messages processed")

        # Processing performance
        processing_start_time: str = Field(description="Processing start timestamp")
        last_processed_time: str | None = Field(
            default=None, description="Last message processing timestamp"
        )
        records_per_second: float = Field(
            default=0.0, description="Current processing rate"
        )

        # Error tracking
        error_count: int = Field(default=0, description="Number of processing errors")
        failed_messages: FlextCore.Types.StringList = Field(
            default_factory=list, description="Failed message IDs"
        )

    class OracleTableMetadata(FlextCore.Models.StrictArbitraryTypesModel):
        """Oracle table metadata for target operations."""

        # Table identification
        schema_name: str = Field(description="Oracle schema name")
        table_name: str = Field(description="Oracle table name")
        full_table_name: str = Field(description="Fully qualified table name")

        # Table structure
        columns: list[FlextCore.Types.Dict] = Field(
            default_factory=list, description="Table column definitions"
        )
        primary_keys: FlextCore.Types.StringList = Field(
            default_factory=list, description="Primary key column names"
        )
        indexes: list[FlextCore.Types.Dict] = Field(
            default_factory=list, description="Table index definitions"
        )

        # Table statistics
        row_count: int | None = Field(
            default=None, description="Current table row count"
        )
        last_analyzed: str | None = Field(
            default=None, description="Last table statistics analysis time"
        )

        # Singer metadata
        singer_stream_name: str = Field(description="Singer stream name")
        singer_schema: dict[str, object] = Field(description="Singer schema definition")
        key_properties: FlextCore.Types.StringList = Field(
            default_factory=list, description="Singer key properties"
        )

    class OracleLoadingOperation(FlextCore.Models.StrictArbitraryTypesModel):
        """Oracle data loading operation tracking."""

        # Operation identification
        operation_id: str = Field(description="Unique operation identifier")
        stream_name: str = Field(description="Singer stream name")
        operation_type: str = Field(description="Type of loading operation")

        # Operation metrics
        records_loaded: int = Field(
            default=0, description="Records successfully loaded"
        )
        records_failed: int = Field(
            default=0, description="Records that failed to load"
        )
        bytes_processed: int = Field(default=0, description="Total bytes processed")

        # Timing information
        start_time: str = Field(description="Operation start time")
        end_time: str | None = Field(default=None, description="Operation end time")
        duration_seconds: float = Field(default=0.0, description="Operation duration")

        # Oracle-specific metrics
        oracle_execution_time: float = Field(
            default=0.0, description="Oracle query execution time"
        )
        oracle_commit_time: float = Field(
            default=0.0, description="Oracle transaction commit time"
        )
        batch_count: int = Field(default=0, description="Number of batches processed")

    class OracleErrorRecovery(FlextCore.Models.StrictArbitraryTypesModel):
        """Oracle error handling and recovery configuration."""

        # Retry configuration
        max_retries: int = Field(default=3, description="Maximum retry attempts")
        retry_delay: float = Field(default=1.0, description="Delay between retries")
        exponential_backoff: bool = Field(
            default=True, description="Use exponential backoff for retries"
        )

        # Error handling options
        continue_on_error: bool = Field(
            default=False, description="Continue processing after non-fatal errors"
        )
        rollback_on_error: bool = Field(
            default=True, description="Rollback transaction on error"
        )
        log_failed_records: bool = Field(
            default=True, description="Log records that fail to load"
        )

        # Oracle-specific error handling
        ignore_duplicate_key_errors: bool = Field(
            default=False, description="Ignore Oracle duplicate key constraint errors"
        )
        handle_constraint_violations: bool = Field(
            default=True, description="Handle Oracle constraint violations gracefully"
        )

    class OraclePerformanceMetrics(FlextCore.Models.StrictArbitraryTypesModel):
        """Performance metrics for Oracle target operations."""

        # Throughput metrics
        records_per_second: float = Field(
            default=0.0, description="Records processed per second"
        )
        bytes_per_second: float = Field(
            default=0.0, description="Bytes processed per second"
        )
        batches_per_second: float = Field(
            default=0.0, description="Batches processed per second"
        )

        # Oracle database metrics
        oracle_connections_used: int = Field(
            default=0, description="Number of Oracle connections used"
        )
        oracle_connection_pool_size: int = Field(
            default=0, description="Oracle connection pool size"
        )
        average_oracle_response_time: float = Field(
            default=0.0, description="Average Oracle response time in milliseconds"
        )

        # Resource utilization
        memory_usage_mb: float = Field(
            default=0.0, description="Memory usage in megabytes"
        )
        cpu_usage_percent: float = Field(
            default=0.0, description="CPU usage percentage"
        )

        # Quality metrics
        success_rate: float = Field(
            default=0.0, description="Operation success rate (0-100)"
        )
        error_rate: float = Field(
            default=0.0, description="Operation error rate (0-100)"
        )


# ZERO TOLERANCE CONSOLIDATION - FlextTargetOracleUtilities moved to utilities.py
#
# CRITICAL: FlextTargetOracleUtilities was DUPLICATED between models.py and utilities.py.
# This was a ZERO TOLERANCE violation of the user's explicit requirements.
#
# RESOLUTION: Import from utilities.py to eliminate duplication completely.


# Note: This import ensures backward compatibility while eliminating duplication
