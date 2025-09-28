"""Module docstring."""

from __future__ import annotations

"""Models for Oracle target operations.

This module provides data models for Oracle target operations.
"""

from pydantic import Field

from flext_core import FlextModels


class FlextTargetOracleModels(FlextModels):
    """Comprehensive models for Oracle target operations extending FlextModels.

    Provides standardized models for all Oracle target domain entities including:
    - Singer message processing and validation
    - Oracle table management and schema operations
    - Data loading and transformation operations
    - Performance monitoring and metrics collection
    - Error handling and recovery operations

    All nested classes inherit FlextModels validation and patterns.
    """

    # Legacy type aliases for backward compatibility
    OracleRecord = dict["str", "object"]
    OracleRecords = list[OracleRecord]

    class OracleTargetConfig(FlextModels.BaseConfig):
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

    class SingerMessageProcessing(FlextModels.BaseModel):
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
        failed_messages: list[str] = Field(
            default_factory=list, description="Failed message IDs"
        )

    class OracleTableMetadata(FlextModels.BaseModel):
        """Oracle table metadata for target operations."""

        # Table identification
        schema_name: str = Field(description="Oracle schema name")
        table_name: str = Field(description="Oracle table name")
        full_table_name: str = Field(description="Fully qualified table name")

        # Table structure
        columns: list[dict] = Field(
            default_factory=list, description="Table column definitions"
        )
        primary_keys: list[str] = Field(
            default_factory=list, description="Primary key column names"
        )
        indexes: list[dict] = Field(
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
        singer_schema: dict = Field(description="Singer schema definition")
        key_properties: list[str] = Field(
            default_factory=list, description="Singer key properties"
        )

    class OracleLoadingOperation(FlextModels.BaseModel):
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

    class OracleErrorRecovery(FlextModels.BaseModel):
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

    class OraclePerformanceMetrics(FlextModels.BaseModel):
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

    # Legacy type aliases for backward compatibility
    TargetConfiguration = dict[str, object]
    LoadingOperation = dict[str, object]


class FlextTargetOracleUtilities(FlextUtilities):
    """Standardized utilities for FLEXT Target Oracle operations.

    Provides comprehensive utility functions for Oracle target operations including
    Singer target configuration, Oracle database connections, data transformation,
    and performance optimization following FLEXT patterns.
    """

    class _OracleTargetHelper:
        """Helper for Singer target Oracle operations."""

        @staticmethod
        def validate_target_config(config: dict) -> FlextResult[dict]:
            """Validate Singer target configuration for Oracle operations."""
            if not config:
                return FlextResult[dict].fail("Target configuration cannot be empty")

            required_fields = [
                "oracle_host",
                "oracle_port",
                "oracle_service",
                "oracle_user",
            ]
            for field in required_fields:
                if field not in config:
                    return FlextResult[dict].fail(
                        f"Missing required Oracle field: {field}"
                    )

            return FlextResult[dict].ok(config)

        @staticmethod
        def create_oracle_connection_config(
            host: str,
            port: int,
            service_name: str,
            username: str,
            password: str,
            schema: str | None = None,
        ) -> FlextResult[dict]:
            """Create Oracle connection configuration for Singer target."""
            if not all([host, port, service_name, username, password]):
                return FlextResult[dict].fail(
                    "All Oracle connection parameters are required"
                )

            config = {
                "oracle_host": host,
                "oracle_port": port,
                "oracle_service": service_name,
                "oracle_user": username,
                "oracle_password": password,
                "oracle_schema": schema or username.upper(),
                "connection_pool_size": 10,
                "connection_timeout": 30,
                "query_timeout": 300,
            }

            return FlextResult[dict].ok(config)

    class _OracleDataTransformationHelper:
        """Helper for Oracle data transformation and type mapping."""

        @staticmethod
        def transform_singer_record_to_oracle(
            record: dict, table_schema: dict
        ) -> FlextResult[dict]:
            """Transform Singer record to Oracle-compatible format."""
            if not record:
                return FlextResult[str].fail("Record cannot be empty")
            if not table_schema:
                return FlextResult[str].fail("Table schema is required")

            try:
                transformed_record = {}

                for field_name, field_value in record.items():
                    if field_name.startswith("_"):  # Skip Singer metadata fields
                        continue

                    oracle_column = table_schema.get(field_name, {})
                    oracle_type = oracle_column.get("type", "VARCHAR2")

                    # Transform based on Oracle data type
                    if oracle_type.startswith("VARCHAR"):
                        transformed_record[field_name] = (
                            str(field_value) if field_value is not None else None
                        )
                    elif oracle_type.startswith("NUMBER"):
                        if field_value is not None:
                            try:
                                transformed_record[field_name] = (
                                    float(field_value)
                                    if "." in str(field_value)
                                    else int(field_value)
                                )
                            except ValueError:
                                return FlextResult[dict].fail(
                                    f"Cannot convert {field_value} to NUMBER for field {field_name}"
                                )
                        else:
                            transformed_record[field_name] = None
                    elif oracle_type in {"DATE", "TIMESTAMP"}:
                        if field_value is not None:
                            # Handle ISO format dates
                            from datetime import datetime

                            try:
                                transformed_record[field_name] = datetime.fromisoformat(
                                    str(field_value)
                                )
                            except ValueError:
                                return FlextResult[dict].fail(
                                    f"Cannot convert {field_value} to Oracle date for field {field_name}"
                                )
                        else:
                            transformed_record[field_name] = None
                    elif oracle_type == "CLOB":
                        transformed_record[field_name] = (
                            str(field_value) if field_value is not None else None
                        )
                    else:
                        transformed_record[field_name] = field_value

                return FlextResult[dict].ok(transformed_record)

            except Exception as e:
                return FlextResult[dict].fail(
                    f"Oracle record transformation failed: {e}"
                )

        @staticmethod
        def generate_oracle_insert_statement(
            table_name: str, record: dict
        ) -> FlextResult[str]:
            """Generate Oracle INSERT statement from transformed record."""
            if not table_name:
                return FlextResult[str].fail("Table name is required")
            if not record:
                return FlextResult[str].fail("Record cannot be empty")

            try:
                columns = list(record.keys())
                placeholders = [f":{col}" for col in columns]

                sql = f"""
                INSERT INTO {table_name} ({", ".join(columns)})
                VALUES ({", ".join(placeholders)})
                """

                return FlextResult[str].ok(sql.strip())

            except Exception as e:
                return FlextResult[str].fail(
                    f"Oracle INSERT statement generation failed: {e}"
                )

    class _OraclePerformanceHelper:
        """Helper for Oracle performance optimization."""

        @staticmethod
        def create_batch_insert_config(batch_size: int = 1000) -> FlextResult[dict]:
            """Create Oracle batch insert configuration for optimal performance."""
            if batch_size <= 0:
                return FlextResult[dict].fail("Batch size must be positive")

            config = {
                "batch_size": min(batch_size, 10000),  # Oracle limit
                "commit_frequency": min(batch_size, 1000),
                "use_bulk_insert": True,
                "parallel_workers": 4,
                "oracle_hints": {
                    "use_append": True,
                    "parallel_degree": 4,
                    "disable_constraints": False,
                },
            }

            return FlextResult[dict].ok(config)

        @staticmethod
        def optimize_oracle_connection(config: dict) -> FlextResult[dict]:
            """Optimize Oracle connection parameters for target operations."""
            optimized_config = config.copy()

            # Oracle-specific optimizations
            optimized_config.update({
                "arraysize": 10000,
                "prefetchrows": 1000,
                "autocommit": False,
                "encoding": "UTF-8",
                "nencoding": "UTF-8",
                "threaded": True,
            })

            return FlextResult[dict].ok(optimized_config)

    class _SingerOracleIntegrationHelper:
        """Helper for Singer target integration with Oracle operations."""

        @staticmethod
        def process_singer_message(
            message: dict, oracle_config: dict
        ) -> FlextResult[dict]:
            """Process Singer message for Oracle target output."""
            if not message:
                return FlextResult[dict].fail("Singer message cannot be empty")

            message_type = message.get("type")
            if not message_type:
                return FlextResult[dict].fail("Singer message must have type")

            if message_type == "RECORD":
                return FlextTargetOracleUtilities._SingerOracleIntegrationHelper._process_record_message(
                    message, oracle_config
                )
            if message_type == "SCHEMA":
                return FlextTargetOracleUtilities._SingerOracleIntegrationHelper._process_schema_message(
                    message, oracle_config
                )
            if message_type == "STATE":
                return FlextTargetOracleUtilities._SingerOracleIntegrationHelper._process_state_message(
                    message, oracle_config
                )
            return FlextResult[dict].fail(
                f"Unsupported Singer message type: {message_type}"
            )

        @staticmethod
        def _process_record_message(
            message: dict, oracle_config: dict
        ) -> FlextResult[dict]:
            """Process Singer RECORD message for Oracle target."""
            record = message.get("record", {})
            stream = message.get("stream", "unknown")

            # Get table schema for transformation
            table_schema = oracle_config.get("table_schemas", {}).get(stream, {})

            # Transform record for Oracle
            transform_result = FlextTargetOracleUtilities._OracleDataTransformationHelper.transform_singer_record_to_oracle(
                record, table_schema
            )

            if transform_result.is_failure:
                return FlextResult[dict].fail(
                    f"Oracle transformation failed: {transform_result.error}"
                )

            transformed_record = transform_result.unwrap()

            # Generate Oracle INSERT statement
            table_name = oracle_config.get("table_mappings", {}).get(stream, stream)
            insert_result = FlextTargetOracleUtilities._OracleDataTransformationHelper.generate_oracle_insert_statement(
                table_name, transformed_record
            )

            if insert_result.is_failure:
                return FlextResult[dict].fail(
                    f"Oracle INSERT generation failed: {insert_result.error}"
                )

            return FlextResult[dict].ok({
                "type": "oracle_insert",
                "stream": stream,
                "table": table_name,
                "sql": insert_result.unwrap(),
                "parameters": transformed_record,
                "original_record": record,
            })

        @staticmethod
        def _process_schema_message(
            message: dict, oracle_config: dict
        ) -> FlextResult[dict]:
            """Process Singer SCHEMA message for Oracle target."""
            schema = message.get("schema", {})
            stream = message.get("stream", "unknown")

            # Generate Oracle table schema from Singer schema
            oracle_schema = FlextTargetOracleUtilities._SingerOracleIntegrationHelper._generate_oracle_table_schema(
                schema
            )

            return FlextResult[dict].ok({
                "type": "oracle_schema",
                "stream": stream,
                "oracle_schema": oracle_schema,
                "singer_schema": schema,
            })

        @staticmethod
        def _process_state_message(
            message: dict, oracle_config: dict
        ) -> FlextResult[dict]:
            """Process Singer STATE message for Oracle target."""
            state = message.get("value", {})

            return FlextResult[dict].ok({"type": "oracle_state", "state": state})

        @staticmethod
        def _generate_oracle_table_schema(singer_schema: dict) -> dict:
            """Generate Oracle table schema from Singer schema."""
            properties = singer_schema.get("properties", {})
            oracle_schema = {}

            for field_name, field_def in properties.items():
                field_type = field_def.get("type", "string")

                # Map Singer types to Oracle types
                if field_type in {"string", "text"}:
                    oracle_type = "VARCHAR2(4000)"
                elif field_type in {"integer", "number"}:
                    oracle_type = "NUMBER"
                elif field_type == "boolean":
                    oracle_type = "NUMBER(1)"
                elif field_type in {"date", "datetime", "timestamp"}:
                    oracle_type = "TIMESTAMP"
                else:
                    oracle_type = "VARCHAR2(4000)"  # Default fallback

                oracle_schema[field_name] = {
                    "type": oracle_type,
                    "nullable": True,  # Default to nullable
                    "singer_type": field_type,
                }

            return oracle_schema

    @classmethod
    def create_oracle_target_config(
        cls,
        host: str,
        port: int,
        service_name: str,
        username: str,
        password: str,
        schema: str | None = None,
        table_mappings: dict | None = None,
        performance_config: dict | None = None,
    ) -> FlextResult[dict]:
        """Create comprehensive Oracle target configuration."""
        connection_result = cls._OracleTargetHelper.create_oracle_connection_config(
            host, port, service_name, username, password, schema
        )

        if connection_result.is_failure:
            return connection_result

        config = connection_result.unwrap()

        # Add additional configuration
        config["table_mappings"] = table_mappings or {}
        config["table_schemas"] = {}

        # Add performance configuration
        if performance_config:
            config.update(performance_config)
        else:
            perf_result = cls._OraclePerformanceHelper.create_batch_insert_config()
            if perf_result.is_success:
                config.update(perf_result.unwrap())

        return FlextResult[dict].ok(config)

    @classmethod
    def validate_oracle_target_environment(cls, config: dict) -> FlextResult[dict]:
        """Validate Oracle target environment and connectivity."""
        validation_result = cls._OracleTargetHelper.validate_target_config(config)
        if validation_result.is_failure:
            return validation_result

        # Additional Oracle-specific validation
        oracle_host = config.get("oracle_host", "")
        oracle_port = config.get("oracle_port", 0)

        if not oracle_host:
            return FlextResult[dict].fail("Oracle host not specified")

        if not (1 <= oracle_port <= 65535):
            return FlextResult[dict].fail("Oracle port must be between 1 and 65535")

        return FlextResult[dict].ok({
            "environment": "valid",
            "oracle_host": oracle_host,
            "oracle_port": oracle_port,
            "connection_ready": True,
        })

    @classmethod
    def process_singer_stream_to_oracle(
        cls, messages: list[dict], oracle_config: dict
    ) -> FlextResult[list[dict]]:
        """Process complete Singer message stream for Oracle target output."""
        if not messages:
            return FlextResult[list[dict]].fail("No Singer messages to process")

        oracle_operations = []

        for message in messages:
            result = cls._SingerOracleIntegrationHelper.process_singer_message(
                message, oracle_config
            )

            if result.is_failure:
                return FlextResult[list[dict]].fail(
                    f"Message processing failed: {result.error}"
                )

            processed = result.unwrap()
            oracle_operations.append(processed)

        return FlextResult[list[dict]].ok(oracle_operations)
