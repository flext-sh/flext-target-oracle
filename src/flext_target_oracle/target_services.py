"""Target Services for FLEXT Target Oracle.

This module provides specialized services following Single Responsibility Principle
to support Oracle Singer target operations. Each service has a focused responsibility
and uses dependency injection via FlextContainer

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import asyncio
from datetime import UTC, datetime
from typing import Protocol

from pydantic import Field

from flext_core import FlextResult, FlextService, FlextTypes
from flext_db_oracle import FlextDbOracleApi
from flext_target_oracle.target_config import FlextTargetOracleConfig
from flext_target_oracle.target_models import (
    LoadMethodModel,
    LoadStatisticsModel,
    OracleConnectionModel,
    SingerStreamModel,
)


class ConnectionServiceProtocol(Protocol):
    """Protocol for Oracle connection management services."""

    def test_connection(self) -> FlextResult[None]:
        """Test Oracle database connection."""
        ...

    def get_connection_info(self) -> FlextResult[OracleConnectionModel]:
        """Get connection information."""
        ...


class SchemaServiceProtocol(Protocol):
    """Protocol for Oracle schema management services."""

    async def ensure_table_exists(
        self,
        stream: SingerStreamModel,
        schema: FlextTypes.Core.Dict,
        key_properties: FlextTypes.Core.StringList | None = None,
    ) -> FlextResult[None]:
        """Ensure table exists for Singer stream."""
        ...

    async def get_table_columns(
        self,
        table_name: str,
        schema_name: str,
    ) -> FlextResult[list[FlextTypes.Core.Dict]]:
        """Get table column definitions."""
        ...


class BatchServiceProtocol(Protocol):
    """Protocol for batch processing services."""

    async def add_record(
        self,
        stream_name: str,
        _record: FlextTypes.Core.Dict,
    ) -> FlextResult[None]:
        """Add record to batch processing queue."""
        ...

    async def flush_batch(self, stream_name: str) -> FlextResult[None]:
        """Flush pending batch for stream."""
        ...

    async def flush_all_batches(self) -> FlextResult[LoadStatisticsModel]:
        """Flush all pending batches."""
        ...


class RecordServiceProtocol(Protocol):
    """Protocol for record transformation services."""

    def transform_record(
        self,
        record: FlextTypes.Core.Dict,
        stream: SingerStreamModel,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Transform Singer record for Oracle storage."""
        ...

    def validate_record(
        self,
        record: FlextTypes.Core.Dict,
        schema: FlextTypes.Core.Dict,
    ) -> FlextResult[None]:
        """Validate record against schema."""
        ...


class OracleConnectionService(FlextService[None]):
    """Oracle database connection lifecycle management using flext-core domain patterns.

    Handles Oracle database connections, connection pooling,
    and connection health monitoring following Single Responsibility Principle.
    Uses FlextService foundation to eliminate duplication and ensure SOLID principles.

    Pydantic-based field definitions following flext-core SOURCE OF TRUTH patterns.
    """

    # Pydantic fields - seguindo FlextModels.Config padrão da SOURCE OF TRUTH
    config: FlextTargetOracleConfig = Field(
        ...,
        description="Oracle target configuration",
    )
    oracle_api: FlextDbOracleApi = Field(
        ...,
        description="Oracle database API instance",
    )

    # Connection model is computed property, not field
    @property
    def connection_model(self) -> OracleConnectionModel:
        """Get connection model using domain service configuration."""
        return OracleConnectionModel(
            host=self.config.oracle_host,
            port=self.config.oracle_port,
            service_name=self.config.oracle_service,
            username=self.config.oracle_user,
            schema=self.config.default_target_schema,
            use_ssl=self.config.use_ssl,
            connection_timeout=self.config.connection_timeout,
        )

    def test_connection(self) -> FlextResult[None]:
        """Test Oracle database connection using zero-fallback error handling.

        Returns:
            FlextResult indicating connection success/failure

        """
        # Use direct API access with explicit FlextResult error handling - NO fallbacks
        with self.oracle_api as connected_api:
            tables_result = connected_api.get_tables(
                schema=self.config.default_target_schema,
            )

            if tables_result.is_failure:
                return FlextResult[None].fail(
                    f"Connection test failed: {tables_result.error}",
                )

            # Use FlextService built-in logging instead of module logger
            self.log_info("Oracle connection test successful")
            return FlextResult[None].ok(None)

    def execute(self) -> FlextResult[None]:
        """Execute domain service - implements FlextService abstract method.

        Executes the primary domain operation: testing Oracle connection.

        Returns:
            FlextResult[None] indicating connection test success/failure

        """
        return self.test_connection()

    def get_connection_info(self) -> FlextResult[OracleConnectionModel]:
        """Get connection information.

        Returns:
            FlextResult containing connection model

        """
        return FlextResult[OracleConnectionModel].ok(self.connection_model)


class OracleSchemaService(FlextService[None]):
    """Oracle schema and table management using flext-core domain patterns.

    Handles Oracle table creation, schema evolution, and metadata
    management following Single Responsibility Principle and
    FlextService patterns.
    """

    # Pydantic fields - seguindo FlextModels.Config padrão da SOURCE OF TRUTH
    config: FlextTargetOracleConfig = Field(
        ...,
        description="Oracle target configuration",
    )
    oracle_api: FlextDbOracleApi = Field(
        ...,
        description="Oracle database API instance",
    )

    def execute(self) -> FlextResult[None]:
        """Execute domain service - implements FlextService abstract method.

        For schema service, execute validates Oracle schema access.

        Returns:
            FlextResult[None] indicating schema access validation

        """
        return self.validate_schema_access()

    def validate_schema_access(self) -> FlextResult[None]:
        """Validate Oracle schema access and permissions."""
        try:
            with self.oracle_api as connected_api:
                # Test schema access by attempting to list tables
                tables_result = connected_api.get_tables(
                    schema=self.config.default_target_schema,
                )

                if tables_result.is_failure:
                    return FlextResult[None].fail(
                        f"Schema access validation failed: {tables_result.error}",
                    )

                self.log_info(
                    f"Schema access validated for {self.config.default_target_schema}",
                )
                return FlextResult[None].ok(None)

        except Exception as e:
            self.log_error(f"Schema access validation failed: {e}")
            return FlextResult[None].fail(f"Schema validation failed: {e}")

    async def ensure_table_exists(
        self,
        stream: SingerStreamModel,
        schema: FlextTypes.Core.Dict,
        key_properties: FlextTypes.Core.StringList | None = None,
    ) -> FlextResult[None]:
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
            columns_result = await self.get_table_columns(
                stream.table_name,
                self.config.default_target_schema,
            )

            if columns_result.is_failure:
                # Table doesn't exist, create it
                self.log_info(f"Creating table {stream.table_name}")
                return await self._create_table(stream, schema, key_properties)
            # Table exists, optionally evolve schema
            self.log_info(f"Table {stream.table_name} already exists")
            return FlextResult[None].ok(None)

        except Exception as e:
            self.log_error(f"Failed to ensure table exists: {e}")
            return FlextResult[None].fail(f"Table existence check failed: {e}")

    async def get_table_columns(
        self,
        table_name: str,
        schema_name: str | None = None,
    ) -> FlextResult[list[FlextTypes.Core.Dict]]:
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
                    return FlextResult[list[FlextTypes.Core.Dict]].fail(
                        f"Failed to get columns: {columns_result.error}",
                    )

                return FlextResult[list[FlextTypes.Core.Dict]].ok(
                    columns_result.data or [],
                )

        except Exception as e:
            self.log_error(f"Failed to get table columns: {e}")
            return FlextResult[list[FlextTypes.Core.Dict]].fail(
                f"Column retrieval failed: {e}",
            )

    async def _create_table(
        self,
        stream: SingerStreamModel,
        _schema: FlextTypes.Core.Dict,
        _key_properties: FlextTypes.Core.StringList | None = None,
    ) -> FlextResult[None]:
        """Create Oracle table based on stream configuration.

        Args:
            stream: Singer stream configuration
            _schema: JSON schema (not used in current simple implementation)
            _key_properties: Primary key columns (not used in current implementation)

        Returns:
            FlextResult indicating success/failure

        """
        try:
            with self.oracle_api as connected_api:
                # For now, create simple JSON table
                # Future enhancement: Create flattened tables based on schema
                columns = [
                    {
                        "name": "DATA",
                        "type": "CLOB",
                        "nullable": True,
                    },
                    {
                        "name": "_SDC_EXTRACTED_AT",
                        "type": "TIMESTAMP",
                        "nullable": True,
                    },
                    {
                        "name": "_SDC_LOADED_AT",
                        "type": "TIMESTAMP",
                        "nullable": True,
                        "default": "CURRENT_TIMESTAMP",
                    },
                ]

                # Add sequence column for unique identification
                if self.config.add_metadata_columns:
                    columns.append(
                        {
                            "name": "_SDC_SEQUENCE",
                            "type": "NUMBER",
                            "nullable": False,
                        },
                    )

                # Generate DDL SQL
                table_name = stream.table_name
                ddl_sql = f"CREATE TABLE {table_name} ("
                column_definitions = []
                for col in columns:
                    col_def = f"{col['name']} {col['type']}"
                    if not col.get("nullable", True):
                        col_def += " NOT NULL"
                    if "default" in col:
                        col_def += f" DEFAULT {col['default']}"
                    column_definitions.append(col_def)

                ddl_sql += ", ".join(column_definitions) + ")"

                exec_result = connected_api.execute_sql(ddl_sql)
                if exec_result.is_failure:
                    return FlextResult[None].fail(
                        f"Failed to create table: {exec_result.error}",
                    )

                self.log_info(f"Created table {stream.table_name}")
                return FlextResult[None].ok(None)

        except Exception as e:
            self.log_error(f"Failed to create table: {e}")
            return FlextResult[None].fail(f"Table creation failed: {e}")


class OracleBatchService(FlextService[LoadStatisticsModel]):
    """Oracle batch processing using flext-core domain patterns.

    Handles batching of records for efficient Oracle loading
    following Single Responsibility Principle and FlextService patterns.
    """

    # Pydantic fields - seguindo FlextModels.Config padrão da SOURCE OF TRUTH
    config: FlextTargetOracleConfig = Field(
        ...,
        description="Oracle target configuration",
    )
    oracle_api: FlextDbOracleApi = Field(
        ...,
        description="Oracle database API instance",
    )
    batches: dict[str, object] = Field(
        default_factory=dict,
        description="Batch storage",
    )
    statistics: dict[str, object] = Field(
        default_factory=dict,
        description="Processing statistics",
    )

    def execute(self) -> FlextResult[LoadStatisticsModel]:
        """Execute domain service - implements FlextService abstract method.

        For batch service, execute finalizes all pending batches.

        Returns:
            FlextResult[LoadStatisticsModel] with aggregated statistics

        """
        return asyncio.run(self.finalize_all())

    async def finalize_all(self) -> FlextResult[LoadStatisticsModel]:
        """Flush all pending batches and return aggregated statistics.

        Returns:
            FlextResult[LoadStatisticsModel]: Aggregated statistics from all batches

        """
        try:
            # Flush all pending batches
            for stream_name in list(self.batches.keys()):
                # Placeholder: In real implementation, check batch status
                result = await self.flush_batch(stream_name)
                if result.is_failure:
                    self.log_error(f"Failed to flush {stream_name}: {result.error}")

            # Aggregate statistics - placeholder implementation
            total_records = 0
            total_successful = 0
            total_failed = 0
            total_batches = 0
            all_errors: FlextTypes.Core.StringList = []

            # For now, return empty statistics - to be implemented with real batch processing
            # In real implementation: for stats in self.statistics.values(): ...

            # Create aggregated statistics
            aggregated_stats = LoadStatisticsModel(
                stream_name="ALL_STREAMS",
                total_records_processed=total_records,
                successful_records=total_successful,
                failed_records=total_failed,
                batches_processed=total_batches,
                load_method_used=LoadMethodModel(self.config.load_method.value),
                error_details=all_errors,
            ).finalize()

            return FlextResult[LoadStatisticsModel].ok(aggregated_stats)

        except Exception as e:
            self.log_error(f"Failed to flush all batches: {e}")
            return FlextResult[LoadStatisticsModel].fail(f"Batch flush all failed: {e}")

    async def add_record(
        self,
        stream_name: str,
        _record: FlextTypes.Core.Dict,
    ) -> FlextResult[None]:
        """Add record to batch processing queue.

        Args:
            stream_name: Name of the stream
            record: Record to add to batch

        Returns:
            FlextResult indicating success/failure

        """
        # Implementation placeholder for proper async batch management
        self.log_info(f"Adding record to batch for stream {stream_name}")
        return FlextResult[None].ok(None)

    async def flush_batch(self, stream_name: str) -> FlextResult[None]:
        """Flush pending batch for stream.

        Args:
            stream_name: Name of the stream to flush

        Returns:
            FlextResult indicating success/failure

        """
        # Implementation placeholder for proper batch flushing
        self.log_info(f"Flushing batch for stream {stream_name}")
        return FlextResult[None].ok(None)


class OracleRecordService(FlextService[None]):
    """Oracle record transformation using flext-core domain patterns.

    Handles Singer record transformation, validation, and mapping
    for Oracle storage following Single Responsibility Principle and
    FlextService patterns.
    """

    # Pydantic fields - seguindo FlextModels.Config padrão da SOURCE OF TRUTH
    config: FlextTargetOracleConfig = Field(
        ...,
        description="Oracle target configuration",
    )

    def execute(self) -> FlextResult[None]:
        """Execute domain service - implements FlextService abstract method.

        For record service, execute validates transformation capabilities.

        Returns:
            FlextResult[None] indicating service readiness

        """
        self.log_info("Record transformation service is ready")
        return FlextResult[None].ok(None)

    def transform_record(
        self,
        record: FlextTypes.Core.Dict,
        stream: SingerStreamModel,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Transform Singer record for Oracle storage.

        Args:
            record: Original Singer record
            stream: Singer stream model

        Returns:
            FlextResult containing transformed record

        """
        try:
            transformed_record = {}

            # Apply column mappings and transformations
            for col_name, original_value in record.items():
                # Skip ignored columns
                if col_name in stream.ignored_columns:
                    continue

                # Apply column name mapping
                mapped_name = stream.column_mappings.get(col_name, col_name)

                # Apply any value transformations here
                final_value = original_value

                transformed_record[mapped_name] = final_value

            # Add metadata columns if enabled
            if self.config.add_metadata_columns:
                now = datetime.now(UTC)
                transformed_record["_sdc_loaded_at"] = now

                # Preserve extracted time if available
                if "_sdc_extracted_at" not in transformed_record:
                    transformed_record["_sdc_extracted_at"] = now

            return FlextResult[FlextTypes.Core.Dict].ok(transformed_record)

        except Exception as e:
            self.log_error(f"Failed to transform record: {e}")
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Record transformation failed: {e}",
            )

    def validate_record(
        self,
        record: FlextTypes.Core.Dict,
        schema: FlextTypes.Core.Dict,
    ) -> FlextResult[None]:
        """Validate record against schema."""
        try:
            properties = schema.get("properties", {})
            required_fields = schema.get("required", [])

            # Validate required fields
            required_validation = self._validate_required_fields(
                record,
                required_fields if isinstance(required_fields, list) else [],
            )
            if required_validation.is_failure:
                return required_validation

            # Validate field types
            type_validation = self._validate_field_types(
                record,
                properties if isinstance(properties, dict) else {},
            )
            if type_validation.is_failure:
                return type_validation

            return FlextResult[None].ok(None)

        except Exception as e:
            self.log_error(f"Failed to validate record: {e}")
            return FlextResult[None].fail(f"Record validation failed: {e}")

    def _validate_required_fields(
        self,
        record: FlextTypes.Core.Dict,
        required_fields: FlextTypes.Core.StringList,
    ) -> FlextResult[None]:
        """Validate required fields are present."""
        for field in required_fields:
            if field not in record:
                return FlextResult[None].fail(f"Missing required field: {field}")
        return FlextResult[None].ok(None)

    def _validate_field_types(
        self,
        record: FlextTypes.Core.Dict,
        properties: FlextTypes.Core.Dict,
    ) -> FlextResult[None]:
        """Validate field types match schema."""
        type_validators: dict[str, FlextTypes.Validation.Validator] = {
            "string": lambda v: isinstance(v, str),
            "integer": lambda v: isinstance(v, int),
            "number": lambda v: isinstance(v, (int, float)),
            "boolean": lambda v: isinstance(v, bool),
        }

        for field_name, field_value in record.items():
            if field_name in properties and field_value is not None:
                field_schema = properties[field_name]
                if isinstance(field_schema, dict):
                    expected_type = field_schema.get("type")

                    if expected_type in type_validators:
                        validator_func = type_validators[expected_type]
                        if not validator_func(field_value):
                            return FlextResult[None].fail(
                                f"Field {field_name} should be {expected_type}, got {type(field_value)}",
                            )

        return FlextResult[None].ok(None)


class OracleTargetServiceFactory:
    """Factory for creating Oracle target services with dependency injection."""

    def __init__(
        self,
        config: FlextTargetOracleConfig,
        oracle_api: FlextDbOracleApi,
    ) -> None:
        """Initialize service factory.

        Args:
            config: Oracle target configuration
            oracle_api: Oracle database API instance

        """
        self._config = config
        self._oracle_api = oracle_api

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
