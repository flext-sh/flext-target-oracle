"""Target Services for FLEXT Target Oracle.

This module provides specialized services following Single Responsibility Principle
to support Oracle Singer target operations. Each service has a focused responsibility
and uses dependency injection via FlextContainer

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, override

from flext_core import FlextService, FlextTypes as t, r
from flext_db_oracle import FlextDbOracleApi
from pydantic import Field

from flext_target_oracle.settings import FlextTargetOracleSettings
from flext_target_oracle.target_models import (
    LoadMethodModel,
    LoadStatisticsModel,
    OracleConnectionModel,
    SingerStreamModel,
)
from flext_target_oracle.utilities import FlextTargetOracleUtilities

# Constants
ALL_STREAMS = "__ALL_STREAMS__"


class ConnectionServiceProtocol(Protocol):
    """Protocol for Oracle connection management services."""

    def test_connection(self) -> r[None]:
        """Test Oracle database connection."""

    def get_connection_info(self) -> r[OracleConnectionModel]:
        """Get connection information."""


class SchemaServiceProtocol(Protocol):
    """Protocol for Oracle schema management services."""

    def ensure_table_exists(
        self,
        stream: SingerStreamModel,
        schema: dict[str, t.GeneralValueType],
        key_properties: list[str] | None = None,
    ) -> r[None]:
        """Ensure table exists for Singer stream."""

    def get_table_columns(
        self,
        table_name: str,
        schema_name: str,
    ) -> r[list[dict[str, t.GeneralValueType]]]:
        """Get table column definitions."""


class BatchServiceProtocol(Protocol):
    """Protocol for batch processing services."""

    def add_record(
        self,
        stream_name: str,
        _record: dict[str, t.GeneralValueType],
    ) -> r[None]:
        """Add record to batch processing queue."""

    def flush_batch(self, stream_name: str) -> r[None]:
        """Flush pending batch for stream."""

    def flush_all_batches(self) -> r[LoadStatisticsModel]:
        """Flush all pending batches."""


class RecordServiceProtocol(Protocol):
    """Protocol for record transformation services."""

    def transform_record(
        self,
        record: dict[str, t.GeneralValueType],
        stream: SingerStreamModel,
    ) -> r[dict[str, t.GeneralValueType]]:
        """Transform Singer record for Oracle storage."""

    def validate_record(
        self,
        record: dict[str, t.GeneralValueType],
        schema: dict[str, t.GeneralValueType],
    ) -> r[None]:
        """Validate record against schema."""


class OracleConnectionService(FlextService[None]):
    """Oracle database connection lifecycle management using flext-core domain patterns.

    Handles Oracle database connections, connection pooling,
    and connection health monitoring following Single Responsibility Principle.
    Uses FlextService foundation to eliminate duplication and ensure SOLID principles.

    Pydantic-based field definitions following flext-core SOURCE OF TRUTH patterns.
    """

    # Pydantic fields - following FlextModels.Config pattern from SOURCE OF TRUTH
    config: FlextTargetOracleSettings = Field(
        ...,
        description="Oracle target configuration",
    )
    oracle_api: FlextDbOracleApi = Field(
        ...,
        description="Oracle database API instance",
    )

    def __init__(self, **data: object) -> None:
        """Initialize Oracle connection service."""
        super().__init__(**data)
        # Zero Tolerance FIX: Use FlextTargetOracleUtilities for ALL business logic
        self._utilities = FlextTargetOracleUtilities()

    # Connection model is computed property, not field
    @property
    def connection_model(self) -> OracleConnectionModel:
        """Get connection model using domain service configuration."""
        return OracleConnectionModel(
            host=self._config.oracle_host,
            port=self._config.oracle_port,
            service_name=self._config.oracle_service,
            username=self._config.oracle_user,
            schema=self._config.default_target_schema,
            use_ssl=self._config.use_ssl,
            connection_timeout=self._config.connection_timeout,
        )

    def test_connection(self) -> r[None]:
        """Test Oracle database connection using zero-fallback error handling.

        Returns:
        FlextResult indicating connection success/failure

        """
        # Zero Tolerance FIX: Use utilities for connection validation
        validation_result = (
            self._utilities.ConfigValidation.validate_oracle_connection_config({
                "oracle_host": self._config.oracle_host,
                "oracle_port": self._config.oracle_port,
                "oracle_service": self._config.oracle_service,
                "oracle_user": self._config.oracle_user,
                "default_target_schema": self._config.default_target_schema,
                "use_ssl": self._config.use_ssl,
                "connection_timeout": self._config.connection_timeout,
            })
        )
        if validation_result.is_failure:
            return r[None].fail(
                f"Connection configuration validation failed: {validation_result.error}",
            )

        # Use direct API access with explicit FlextResult error handling - NO fallbacks
        with self.oracle_api as connected_api:
            tables_result = connected_api.get_tables(
                schema=self._config.default_target_schema,
            )

            if tables_result.is_failure:
                return r[None].fail(
                    f"Connection test failed: {tables_result.error}",
                )

            # Zero Tolerance FIX: Use utilities for connection diagnostics
            diagnostics_result = (
                self._utilities.ConnectionManagement.generate_connection_diagnostics(
                    host=self._config.oracle_host,
                    port=self._config.oracle_port,
                    service_name=self._config.oracle_service,
                    schema=self._config.default_target_schema,
                    table_count=len(tables_result.value)
                    if isinstance(tables_result.value, list)
                    else 0,
                )
            )

            if diagnostics_result.is_success:
                self.log_info(
                    f"Oracle connection test successful: {diagnostics_result.value}",
                )
            else:
                self.log_warning(
                    f"Diagnostics generation failed: {diagnostics_result.error}",
                )

            # Use FlextService built-in logging instead of module logger
            self.log_info("Oracle connection test successful")
            return r[None].ok(None)

    @override
    def execute(self) -> r[None]:
        """Execute domain service - implements FlextService abstract method.

        Executes the primary domain operation: testing Oracle connection.

        Returns:
        r[None] indicating connection test success/failure

        """
        return self.test_connection()

    def get_connection_info(self) -> r[OracleConnectionModel]:
        """Get connection information.

        Returns:
        FlextResult containing connection model

        """
        return r[OracleConnectionModel].ok(self.connection_model)


class OracleSchemaService(FlextService[None]):
    """Oracle schema and table management using flext-core domain patterns.

    Handles Oracle table creation, schema evolution, and metadata
    management following Single Responsibility Principle and
    FlextService patterns.
    """

    # Pydantic fields - following FlextModels.Config pattern from SOURCE OF TRUTH
    config: FlextTargetOracleSettings = Field(
        ...,
        description="Oracle target configuration",
    )
    oracle_api: FlextDbOracleApi = Field(
        ...,
        description="Oracle database API instance",
    )

    def __init__(self, **data: object) -> None:
        """Initialize Oracle schema service."""
        super().__init__(**data)
        # Zero Tolerance FIX: Use FlextTargetOracleUtilities for ALL business logic
        self._utilities = FlextTargetOracleUtilities()

    @override
    def execute(self) -> r[None]:
        """Execute domain service - implements FlextService abstract method.

        For schema service, execute validates Oracle schema access.

        Returns:
        r[None] indicating schema access validation

        """
        return self.validate_schema_access()

    def validate_schema_access(self) -> r[None]:
        """Validate Oracle schema access and permissions."""
        try:
            # Zero Tolerance FIX: Use utilities for schema validation
            schema_validation = (
                self._utilities.SchemaValidation.validate_oracle_schema_access(
                    schema_name=self._config.default_target_schema,
                    required_permissions=["CREATE", "INSERT", "UPDATE", "SELECT"],
                )
            )

            if schema_validation.is_failure:
                return r[None].fail(
                    f"Schema validation failed: {schema_validation.error}",
                )

            with self.oracle_api as connected_api:
                # Test schema access by attempting to list tables
                tables_result = connected_api.get_tables(
                    schema=self._config.default_target_schema,
                )

                if tables_result.is_failure:
                    return r[None].fail(
                        f"Schema access validation failed: {tables_result.error}",
                    )

                self.log_info(
                    f"Schema access validated for {self._config.default_target_schema}",
                )
                return r[None].ok(None)

        except Exception as e:
            self.log_error(f"Schema access validation failed: {e}")
            return r[None].fail(f"Schema validation failed: {e}")

    def ensure_table_exists(
        self,
        stream: SingerStreamModel,
        schema: dict[str, t.GeneralValueType],
        key_properties: list[str] | None = None,
    ) -> r[None]:
        """Ensure Oracle table exists for stream data.

        Args:
        stream: Singer stream configuration
        schema: JSON schema for the stream
        key_properties: Primary key columns

        Returns:
        FlextResult indicating success/failure

        """
        try:
            # Check if table exists
            columns_result = self.get_table_columns(
                stream.table_name,
                self._config.default_target_schema,
            )

            if columns_result.is_failure:
                # Table doesn't exist, create it
                self.log_info(f"Creating table {stream.table_name}")
                return self._create_table(stream, schema, key_properties)
            # Table exists, optionally evolve schema
            self.log_info(f"Table {stream.table_name} already exists")
            return r[None].ok(None)

        except Exception as e:
            self.log_error(f"Failed to ensure table exists: {e}")
            return r[None].fail(f"Table existence check failed: {e}")

    def get_table_columns(
        self,
        table_name: str,
        schema_name: str | None = None,
    ) -> r[list[dict[str, t.GeneralValueType]]]:
        """Get column information for Oracle table.

        Args:
        table_name: Name of the table
        schema_name: Oracle schema name

        Returns:
        FlextResult containing column definitions

        """
        try:
            with self.oracle_api as connected_api:
                # Get column information using Oracle API
                columns_result = connected_api.get_columns(
                    table_name,
                    schema_name,
                )

                if columns_result.is_failure:
                    return r[list[dict[str, t.GeneralValueType]]].fail(
                        f"Failed to get columns: {columns_result.error}",
                    )

                return r[list[dict[str, t.GeneralValueType]]].ok(
                    columns_result.value or [],
                )

        except Exception as e:
            self.log_error(f"Failed to get table columns: {e}")
            return r[list[dict[str, t.GeneralValueType]]].fail(
                f"Column retrieval failed: {e}",
            )

    def _create_table(
        self,
        stream: SingerStreamModel,
        schema: dict[str, t.GeneralValueType],
        key_properties: list[str] | None = None,
    ) -> r[None]:
        """Create Oracle table based on stream configuration.

        Args:
        stream: Singer stream configuration
        schema: JSON schema
        key_properties: Primary key columns

        Returns:
        FlextResult indicating success/failure

        """
        try:
            # Zero Tolerance FIX: Use utilities for DDL generation
            ddl_result = self._utilities.TableManagement.generate_create_table_ddl(
                table_name=stream.table_name,
                schema=schema,
                key_properties=key_properties or [],
                add_metadata_columns=self._config.add_metadata_columns,
            )

            if ddl_result.is_failure:
                return r[None].fail(
                    f"DDL generation failed: {ddl_result.error}",
                )

            with self.oracle_api as connected_api:
                # Zero Tolerance FIX: Use utilities for DDL validation before execution
                ddl_sql = ddl_result.value
                validation_result = self._utilities.TableManagement.validate_ddl_syntax(
                    ddl_sql,
                )

                if validation_result.is_failure:
                    return r[None].fail(
                        f"DDL validation failed: {validation_result.error}",
                    )

                exec_result: r[object] = connected_api.execute_sql(ddl_sql)
                if exec_result.is_failure:
                    return r[None].fail(
                        f"Failed to create table: {exec_result.error}",
                    )

                # Zero Tolerance FIX: Use utilities for post-creation validation
                verification_result = (
                    self._utilities.TableManagement.verify_table_creation(
                        table_name=stream.table_name,
                        expected_columns=[],  # Would be populated based on schema
                        oracle_api=connected_api,
                    )
                )

                if verification_result.is_failure:
                    self.log_warning(
                        f"Table creation verification failed: {verification_result.error}",
                    )

                self.log_info(f"Created table {stream.table_name}")
                return r[None].ok(None)

        except Exception as e:
            self.log_error(f"Failed to create table: {e}")
            return r[None].fail(f"Table creation failed: {e}")


class OracleBatchService(FlextService[LoadStatisticsModel]):
    """Oracle batch processing using flext-core domain patterns.

    Handles batching of records for efficient Oracle loading
    following Single Responsibility Principle and FlextService patterns.
    """

    # Pydantic fields - following FlextModels.Config pattern from SOURCE OF TRUTH
    config: FlextTargetOracleSettings = Field(
        ...,
        description="Oracle target configuration",
    )
    oracle_api: FlextDbOracleApi = Field(
        ...,
        description="Oracle database API instance",
    )
    batches: dict[str, t.GeneralValueType] = Field(
        default_factory=dict,
        description="Batch storage",
    )
    statistics: dict[str, t.GeneralValueType] = Field(
        default_factory=dict,
        description="Processing statistics",
    )

    @override
    def execute(self) -> r[LoadStatisticsModel]:
        """Execute domain service - implements FlextService abstract method.

        For batch service, execute finalizes all pending batches.

        Returns:
        r[LoadStatisticsModel] with aggregated statistics

        """
        return self.finalize_all()

    def finalize_all(self) -> r[LoadStatisticsModel]:
        """Flush all pending batches and return aggregated statistics.

        Returns:
        r[LoadStatisticsModel]: Aggregated statistics from all batches

        """
        try:
            # Flush all pending batches
            for stream_name in list(self.batches.keys()):
                # Placeholder: In real implementation, check batch status
                result: r[object] = self.flush_batch(stream_name)
                if result.is_failure:
                    self.log_error(f"Failed to flush {stream_name}: {result.error}")

            # Aggregate statistics - placeholder implementation
            total_records = 0
            total_successful = 0
            total_failed = 0
            total_batches = 0
            all_errors: list[str] = []

            # For now, return empty statistics - to be implemented with real batch processing
            # In real implementation: for stats in self.statistics.values(): ...

            # Create aggregated statistics
            aggregated_stats = LoadStatisticsModel(
                stream_name=ALL_STREAMS,
                total_records_processed=total_records,
                successful_records=total_successful,
                failed_records=total_failed,
                batches_processed=total_batches,
                load_method_used=LoadMethodModel(self._config.load_method.value),
                error_details=all_errors,
            ).finalize()

            return r[LoadStatisticsModel].ok(aggregated_stats)

        except Exception as e:
            self.log_error(f"Failed to flush all batches: {e}")
            return r[LoadStatisticsModel].fail(f"Batch flush all failed: {e}")

    def add_record(
        self,
        stream_name: str,
        _record: dict[str, t.GeneralValueType],
    ) -> r[None]:
        """Add record to batch processing queue.

        Args:
        stream_name: Name of the stream
        _record: Record to add to batch

        Returns:
        FlextResult indicating success/failure

        """
        # Implementation placeholder for proper batch management
        self.log_info(f"Adding record to batch for stream {stream_name}")
        return r[None].ok(None)

    def flush_batch(self, stream_name: str) -> r[None]:
        """Flush pending batch for stream.

        Args:
        stream_name: Name of the stream to flush

        Returns:
        FlextResult indicating success/failure

        """
        # Implementation placeholder for proper batch flushing
        self.log_info(f"Flushing batch for stream {stream_name}")
        return r[None].ok(None)


class OracleRecordService(FlextService[None]):
    """Oracle record transformation using flext-core domain patterns.

    Handles Singer record transformation, validation, and mapping
    for Oracle storage following Single Responsibility Principle and
    FlextService patterns.
    """

    # Pydantic fields - following FlextModels.Config pattern from SOURCE OF TRUTH
    config: FlextTargetOracleSettings = Field(
        ...,
        description="Oracle target configuration",
    )

    def __init__(self, **data: object) -> None:
        """Initialize Oracle record service."""
        super().__init__(**data)
        # Zero Tolerance FIX: Use FlextTargetOracleUtilities for ALL business logic
        self._utilities = FlextTargetOracleUtilities()

    @override
    def execute(self) -> r[None]:
        """Execute domain service - implements FlextService abstract method.

        For record service, execute validates transformation capabilities.

        Returns:
        r[None] indicating service readiness

        """
        self.log_info("Record transformation service is ready")
        return r[None].ok(None)

    def transform_record(
        self,
        record: dict[str, t.GeneralValueType],
        stream: SingerStreamModel,
    ) -> r[dict[str, t.GeneralValueType]]:
        """Transform Singer record for Oracle storage.

        Args:
        record: Original Singer record
        stream: Singer stream model

        Returns:
        FlextResult containing transformed record

        """
        try:
            # Zero Tolerance FIX: Use utilities for Singer message parsing and validation
            # First validate the record structure
            validation_result = (
                self._utilities.SingerUtilities.validate_record_structure(record)
            )
            if validation_result.is_failure:
                return r[dict[str, t.GeneralValueType]].fail(
                    f"Record validation failed: {validation_result.error}",
                )

            transformed_record = {}

            # Apply column mappings and transformations
            for col_name, original_value in record.items():
                # Skip ignored columns
                if col_name in stream.ignored_columns:
                    continue

                # Apply column name mapping
                mapped_name = stream.column_mappings.get(col_name, col_name)

                # Zero Tolerance FIX: Use utilities for data type conversion
                conversion_result = self._utilities.DataTransformation.convert_singer_value_to_oracle(
                    value=original_value,
                    target_type="VARCHAR2",  # Default, should be determined from stream schema
                )

                if conversion_result.is_success:
                    final_value = conversion_result.value
                else:
                    self.log_warning(
                        f"Value conversion failed for {col_name}: {conversion_result.error}",
                    )
                    final_value = original_value

                # Zero Tolerance FIX: Use utilities for value sanitization
                if isinstance(final_value, str):
                    final_value = (
                        self._utilities.DataTransformation.sanitize_oracle_value(
                            final_value,
                        )
                    )

                transformed_record[mapped_name] = final_value

            # Zero Tolerance FIX: Use utilities for metadata column handling
            if self._config.add_metadata_columns:
                metadata_result = (
                    self._utilities.MetadataProcessing.add_singer_metadata_columns(
                        record=transformed_record,
                        source_timestamp=record.get("_sdc_extracted_at"),
                    )
                )

                if metadata_result.is_success:
                    transformed_record = metadata_result.value
                else:
                    self.log_warning(
                        f"Metadata addition failed: {metadata_result.error}",
                    )

            return r[dict[str, t.GeneralValueType]].ok(transformed_record)

        except Exception as e:
            self.log_error(f"Failed to transform record: {e}")
            return r[dict[str, t.GeneralValueType]].fail(
                f"Record transformation failed: {e}",
            )

    def validate_record(
        self,
        record: dict[str, t.GeneralValueType],
        schema: dict[str, t.GeneralValueType],
    ) -> r[None]:
        """Validate record against schema."""
        try:
            # Zero Tolerance FIX: Use utilities for complete record validation
            validation_result = (
                self._utilities.SchemaValidation.validate_record_against_schema(
                    record=record,
                    schema=schema,
                )
            )

            if validation_result.is_failure:
                return r[None].fail(validation_result.error)

            # Zero Tolerance FIX: Use utilities for Oracle-specific validations
            oracle_validation = (
                self._utilities.SchemaValidation.validate_oracle_constraints(
                    record=record,
                    schema=schema,
                )
            )

            if oracle_validation.is_failure:
                return r[None].fail(oracle_validation.error)

            return r[None].ok(None)

        except Exception as e:
            self.log_error(f"Failed to validate record: {e}")
            return r[None].fail(f"Record validation failed: {e}")


class OracleTargetServiceFactory:
    """Factory for creating Oracle target services with dependency injection."""

    @override
    def __init__(
        self,
        config: FlextTargetOracleSettings,
        oracle_api: FlextDbOracleApi,
    ) -> None:
        """Initialize service factory.

        Args:
        config: Oracle target configuration
        oracle_api: Oracle database API instance

        """
        self._config: FlextTargetOracleSettings = config
        self._oracle_api = oracle_api

    @property
    def config(self) -> FlextTargetOracleSettings:
        """Get configuration object."""
        return self._config

    def create_connection_service(self) -> OracleConnectionService:
        """Create Oracle connection service."""
        return OracleConnectionService(config=self._config, oracle_api=self._oracle_api)

    def create_schema_service(self) -> OracleSchemaService:
        """Create Oracle schema service."""
        return OracleSchemaService(config=self._config, oracle_api=self._oracle_api)

    def create_batch_service(self) -> OracleBatchService:
        """Create Oracle batch processing service."""
        return OracleBatchService(config=self._config, oracle_api=self._oracle_api)

    def create_record_service(self) -> OracleRecordService:
        """Create Oracle record transformation service."""
        return OracleRecordService(config=self._config)


__all__ = [
    "BatchServiceProtocol",
    # Service Protocols
    "ConnectionServiceProtocol",
    "OracleBatchService",
    # Service Implementations
    "OracleConnectionService",
    "OracleRecordService",
    "OracleSchemaService",
    # Factory
    "OracleTargetServiceFactory",
    "RecordServiceProtocol",
    "SchemaServiceProtocol",
]
