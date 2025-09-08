"""Target Services for FLEXT Target Oracle.

This module provides specialized services following Single Responsibility Principle
to support Oracle Singer target operations. Each service has a focused responsibility
and uses dependency injection via FlextContainer following SOLID principles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from datetime import UTC, datetime
from typing import Protocol

from flext_core import FlextLogger, FlextResult, FlextTypes
from flext_db_oracle import FlextDbOracleApi

from flext_target_oracle.target_config import FlextTargetOracleConfig
from flext_target_oracle.target_models import (
    LoadMethodModel,
    LoadStatisticsModel,
    OracleConnectionModel,
    SingerStreamModel,
)

logger = FlextLogger(__name__)
# =============================================================================
# SERVICE PROTOCOLS (INTERFACES)
# =============================================================================


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
        record: FlextTypes.Core.Dict,
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


# =============================================================================
# ORACLE CONNECTION SERVICE
# =============================================================================


class OracleConnectionService:
    """Oracle database connection lifecycle management.

    Handles Oracle database connections, connection pooling,
    and connection health monitoring following Single Responsibility Principle.
    """

    def __init__(
        self,
        config: FlextTargetOracleConfig,
        oracle_api: FlextDbOracleApi,
    ) -> None:
        """Initialize connection service.

        Args:
            config: Oracle target configuration
            oracle_api: Oracle database API instance

        """
        self._config = config
        self._oracle_api = oracle_api
        self._connection_model: OracleConnectionModel | None = None

        # Initialize connection model
        self._connection_model = OracleConnectionModel(
            host=config.oracle_host,
            port=config.oracle_port,
            service_name=config.oracle_service,
            username=config.oracle_user,
            schema=config.default_target_schema,
            use_ssl=config.use_ssl,
            connection_timeout=config.connection_timeout,
        )

    def test_connection(self) -> FlextResult[None]:
        """Test Oracle database connection.

        Returns:
            FlextResult indicating connection success/failure

        """
        try:
            with self._oracle_api as connected_api:
                # Simple connection test by querying system tables
                tables_result = connected_api.get_tables(
                    schema=self._config.default_target_schema,
                )

                if tables_result.is_failure:
                    return FlextResult[None].fail(
                        f"Connection test failed: {tables_result.error}",
                    )

                logger.info("Oracle connection test successful")
                return FlextResult[None].ok(None)

        except Exception as e:
            logger.exception("Oracle connection test failed")
            return FlextResult[None].fail(f"Connection test failed: {e}")

    def get_connection_info(self) -> FlextResult[OracleConnectionModel]:
        """Get connection information.

        Returns:
            FlextResult containing connection model

        """
        if self._connection_model is None:
            return FlextResult[OracleConnectionModel].fail(
                "Connection model not initialized"
            )

        return FlextResult[OracleConnectionModel].ok(self._connection_model)


# =============================================================================
# ORACLE SCHEMA SERVICE
# =============================================================================


class OracleSchemaService:
    """Oracle schema and table management service.

    Handles Oracle table creation, schema evolution, and metadata
    management following Single Responsibility Principle.
    """

    def __init__(
        self,
        config: FlextTargetOracleConfig,
        oracle_api: FlextDbOracleApi,
    ) -> None:
        """Initialize schema service.

        Args:
            config: Oracle target configuration
            oracle_api: Oracle database API instance

        Returns:
            FlextResult indicating success/failure

        Returns:
            FlextResult indicating success/failure

        Returns:
            FlextResult indicating success/failure

        Returns:
            FlextResult indicating success/failure

        Returns:
            FlextResult indicating success/failure

        Returns:
            FlextResult indicating success/failure

        Returns:
            FlextResult indicating success/failure

        Returns:
            FlextResult indicating success/failure

        Returns:
            FlextResult indicating success/failure

        Returns:
            FlextResult indicating success/failure

        Returns:
            FlextResult indicating success/failure

        Returns:
            FlextResult indicating success/failure

        Returns:
            FlextResult indicating success/failure

        Returns:
            FlextResult indicating success/failure

        Returns:
            FlextResult indicating success/failure

            key_properties: Primary key columns

        Returns:
            FlextResult indicating success/failure

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

        Returns:
            FlextResult containing column definitions

            schema_name: Oracle schema name

        Returns:
            FlextResult containing column definitions

        """
        try:
            with self._oracle_api as connected_api:
                # Get column information using Oracle API
                # API signature is get_columns(table_name: str, schema: str | None)
                columns_result = connected_api.get_columns(
                    table_name=table_name,
                    schema=schema_name,
                )

                if columns_result.is_failure:
                    return FlextResult[list[FlextTypes.Core.Dict]].fail(
                        f"Failed to get columns: {columns_result.error}",
                    )

                return FlextResult[list[FlextTypes.Core.Dict]].ok(
                    columns_result.data or []
                )

        except Exception as e:
            logger.exception("Failed to get table columns")
            return FlextResult[list[FlextTypes.Core.Dict]].fail(
                f"Column retrieval failed: {e}"
            )

    async def _create_table(
        self,
        stream: SingerStreamModel,
        _schema: FlextTypes.Core.Dict,
        _key_properties: FlextTypes.Core.StringList | None = None,
    ) -> FlextResult[None]:
        """Create Oracle table based on stream configuration."""
        try:
            with self._oracle_api as connected_api:
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
                if self._config.add_metadata_columns:
                    columns.append(
                        {
                            "name": "_SDC_SEQUENCE",
                            "type": "NUMBER",
                            "nullable": True,
                        },
                    )

                # Create table DDL
                ddl_result = connected_api.create_table_ddl(
                    table_name=stream.table_name,
                    columns=columns,
                    schema=stream.schema_name,
                )

                if ddl_result.is_failure:
                    return FlextResult[None].fail(
                        f"Failed to create DDL: {ddl_result.error}"
                    )

                # Execute DDL
                ddl_sql = ddl_result.data
                if ddl_sql is None:
                    return FlextResult[None].fail("DDL creation returned None")

                exec_result = connected_api.execute_ddl(ddl_sql)
                if exec_result.is_failure:
                    return FlextResult[None].fail(
                        f"Failed to create table: {exec_result.error}",
                    )

                logger.info(f"Created table {stream.table_name}")
                return FlextResult[None].ok(None)

        except Exception as e:
            logger.exception("Failed to create table")
            return FlextResult[None].fail(f"Table creation failed: {e}")


# =============================================================================
# ORACLE BATCH PROCESSING SERVICE
# =============================================================================


class OracleBatchService:
    """Oracle batch processing service.

    Handles batching of records for efficient Oracle loading
    following Single Responsibility Principle.
    """

    def __init__(
        self,
        config: FlextTargetOracleConfig,
        oracle_api: FlextDbOracleApi,
    ) -> None:
        """Initialize batch service.

        Args:
            config: Oracle target configuration
            oracle_api: Oracle database API instance

        """
        try:
            # Flush all pending batches
            for stream_name in list(self._batches.keys()):
                if self._batches[stream_name].has_pending_records:
                    result = await self.flush_batch(stream_name)
                    if result.is_failure:
                        logger.error(f"Failed to flush {stream_name}: {result.error}")

            # Aggregate statistics
            total_records = 0
            total_successful = 0
            total_failed = 0
            total_batches = 0
            all_errors: FlextTypes.Core.StringList = []

            for stats in self._statistics.values():
                final_stats = stats.finalize()
                total_records += final_stats.total_records_processed
                total_successful += final_stats.successful_records
                total_failed += final_stats.failed_records
                total_batches += final_stats.batches_processed
                all_errors.extend(final_stats.error_details)

            # Create aggregated statistics
            aggregated_stats = LoadStatisticsModel(
                stream_name="ALL_STREAMS",
                total_records_processed=total_records,
                successful_records=total_successful,
                failed_records=total_failed,
                batches_processed=total_batches,
                load_method_used=LoadMethodModel(self._config.load_method.value),
                error_details=all_errors,
            ).finalize()

            return FlextResult[LoadStatisticsModel].ok(aggregated_stats)

        except Exception as e:
            logger.exception("Failed to flush all batches")
            return FlextResult[LoadStatisticsModel].fail(f"Batch flush all failed: {e}")


# =============================================================================
# ORACLE RECORD TRANSFORMATION SERVICE
# =============================================================================


class OracleRecordService:
    """Oracle record transformation and validation service.

    Handles Singer record transformation, validation, and mapping
    for Oracle storage following Single Responsibility Principle.
    """

    def __init__(self, config: FlextTargetOracleConfig) -> None:
        """Initialize record service.

        Args:
            config: Oracle target configuration

        Returns:
            object: Description of return value.

        """
        self._config = config

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
            if self._config.add_metadata_columns:
                now = datetime.now(UTC)
                transformed_record["_sdc_loaded_at"] = now

                # Preserve extracted time if available
                if "_sdc_extracted_at" not in transformed_record:
                    transformed_record["_sdc_extracted_at"] = now

            return FlextResult[FlextTypes.Core.Dict].ok(transformed_record)

        except Exception as e:
            logger.exception("Failed to transform record")
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Record transformation failed: {e}"
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
            logger.exception("Failed to validate record")
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


# =============================================================================
# SERVICE FACTORY
# =============================================================================


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
        return OracleConnectionService(self._config, self._oracle_api)

    def create_schema_service(self) -> OracleSchemaService:
        """Create Oracle schema service."""
        return OracleSchemaService(self._config, self._oracle_api)

    def create_batch_service(self) -> OracleBatchService:
        """Create Oracle batch processing service."""
        return OracleBatchService(self._config, self._oracle_api)

    def create_record_service(self) -> OracleRecordService:
        """Create Oracle record transformation service."""
        return OracleRecordService(self._config)


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
