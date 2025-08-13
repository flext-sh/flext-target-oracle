"""Target Services for FLEXT Target Oracle.

This module provides specialized services following Single Responsibility Principle
to support Oracle Singer target operations. Each service has a focused responsibility
and uses dependency injection via FlextContainer following SOLID principles.

The services implement Clean Architecture patterns with proper separation of concerns:
- Application Services: High-level business logic coordination
- Domain Services: Core business rule implementations
- Infrastructure Services: External system integrations

Key Services:
    OracleConnectionService: Connection lifecycle management
    OracleSchemaService: Table creation and schema operations
    OracleBatchService: Batch processing logic
    OracleSQLService: SQL generation for different operations
    OracleRecordService: Record transformation and validation

Architecture Patterns:
    - FlextResult for all operations (railway-oriented programming)
    - FlextEntity/FlextValueObject where appropriate
    - Constructor injection via dependencies
    - Interface segregation with protocols
    - Single Responsibility Principle

Following docs/patterns/foundation.md:
    - Consistent error handling with FlextResult
    - Immutable value objects for data transfer
    - Domain-driven design with clear boundaries
    - Testable services with dependency injection

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Protocol
from flext_target_oracle.typings import FlextTypes

from flext_core import FlextResult, get_logger

from flext_target_oracle.target_models import (
    BatchProcessingModel,
    LoadMethodModel,
    LoadStatisticsModel,
    OracleConnectionModel,
    SingerStreamModel,
)

if TYPE_CHECKING:
    from collections.abc import Callable as _Callable

    from flext_db_oracle import FlextDbOracleApi

    from flext_target_oracle.target_config import FlextTargetOracleConfig

logger = get_logger(__name__)


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
        schema: dict[str, object],
        key_properties: list[str] | None = None,
    ) -> FlextResult[None]:
        """Ensure table exists for Singer stream."""
        ...

    async def get_table_columns(
        self,
        table_name: str,
        schema_name: str,
    ) -> FlextResult[list[dict[str, object]]]:
        """Get table column definitions."""
        ...


class BatchServiceProtocol(Protocol):
    """Protocol for batch processing services."""

    async def add_record(
        self,
        stream_name: str,
        record: dict[str, object],
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
        record: dict[str, object],
        stream: SingerStreamModel,
    ) -> FlextResult[dict[str, object]]:
        """Transform Singer record for Oracle storage."""
        ...

    def validate_record(
        self,
        record: dict[str, object],
        schema: dict[str, object],
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
                    return FlextResult.fail(
                        f"Connection test failed: {tables_result.error}",
                    )

                logger.info("Oracle connection test successful")
                return FlextResult.ok(None)

        except Exception as e:
            logger.exception("Oracle connection test failed")
            return FlextResult.fail(f"Connection test failed: {e}")

    def get_connection_info(self) -> FlextResult[OracleConnectionModel]:
        """Get connection information.

        Returns:
            FlextResult containing connection model

        """
        if self._connection_model is None:
            return FlextResult.fail("Connection model not initialized")

        return FlextResult.ok(self._connection_model)


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

        """
        self._config = config
        self._oracle_api = oracle_api

    async def ensure_table_exists(
        self,
        stream: SingerStreamModel,
        schema: dict[str, object],
        key_properties: list[str] | None = None,
    ) -> FlextResult[None]:
        """Ensure table exists for Singer stream.

        Args:
            stream: Singer stream model
            schema: JSON schema definition
            key_properties: Primary key columns

        Returns:
            FlextResult indicating success/failure

        """
        try:
            with self._oracle_api as connected_api:
                # Check if table exists
                tables_result = connected_api.get_tables(
                    schema=stream.schema_name,
                )

                if tables_result.is_failure:
                    return FlextResult.fail(
                        f"Failed to check tables: {tables_result.error}",
                    )

                existing_tables = [t.upper() for t in tables_result.data or []]
                table_exists = stream.table_name.upper() in existing_tables

                if table_exists:
                    logger.info(f"Table {stream.table_name} already exists")
                    return FlextResult.ok(None)

                # Create table based on storage mode
                return await self._create_table(stream, schema, key_properties)

        except Exception as e:
            logger.exception("Failed to ensure table exists")
            return FlextResult.fail(f"Table creation failed: {e}")

    async def get_table_columns(
        self,
        table_name: str,
        schema_name: str,
    ) -> FlextResult[list[dict[str, object]]]:
        """Get table column definitions.

        Args:
            table_name: Oracle table name
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
                    return FlextResult.fail(
                        f"Failed to get columns: {columns_result.error}",
                    )

                return FlextResult.ok(columns_result.data or [])

        except Exception as e:
            logger.exception("Failed to get table columns")
            return FlextResult.fail(f"Column retrieval failed: {e}")

    async def _create_table(
        self,
        stream: SingerStreamModel,
        _schema: dict[str, object],
        _key_properties: list[str] | None = None,
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
                    return FlextResult.fail(f"Failed to create DDL: {ddl_result.error}")

                # Execute DDL
                ddl_sql = ddl_result.data
                if ddl_sql is None:
                    return FlextResult.fail("DDL creation returned None")

                exec_result = connected_api.execute_ddl(ddl_sql)
                if exec_result.is_failure:
                    return FlextResult.fail(
                        f"Failed to create table: {exec_result.error}",
                    )

                logger.info(f"Created table {stream.table_name}")
                return FlextResult.ok(None)

        except Exception as e:
            logger.exception("Failed to create table")
            return FlextResult.fail(f"Table creation failed: {e}")


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
        self._config = config
        self._oracle_api = oracle_api
        self._batches: dict[str, BatchProcessingModel] = {}
        self._statistics: dict[str, LoadStatisticsModel] = {}

    async def add_record(
        self,
        stream_name: str,
        record: dict[str, object],
    ) -> FlextResult[None]:
        """Add record to batch processing queue.

        Args:
            stream_name: Singer stream name
            record: Record data to add

        Returns:
            FlextResult indicating success/failure

        """
        try:
            # Initialize batch if not exists
            if stream_name not in self._batches:
                self._batches[stream_name] = BatchProcessingModel(
                    stream_name=stream_name,
                    batch_size=self._config.batch_size,
                )
                self._statistics[stream_name] = LoadStatisticsModel(
                    stream_name=stream_name,
                    load_method_used=LoadMethodModel(self._config.load_method.value),
                )

            # Add record to batch
            current_batch = self._batches[stream_name]
            new_batch = current_batch.add_record(record)
            self._batches[stream_name] = new_batch

            # Auto-flush if batch is full
            if new_batch.is_batch_full:
                return await self.flush_batch(stream_name)

            return FlextResult.ok(None)

        except Exception as e:
            logger.exception("Failed to add record to batch")
            return FlextResult.fail(f"Batch add failed: {e}")

    async def flush_batch(self, stream_name: str) -> FlextResult[None]:
        """Flush pending batch for stream.

        Args:
            stream_name: Singer stream name

        Returns:
            FlextResult indicating success/failure

        """
        try:
            batch = self._batches.get(stream_name)
            if not batch or not batch.has_pending_records:
                return FlextResult.ok(None)

            table_name = self._config.get_table_name(stream_name)
            loaded_at = datetime.now(UTC)

            # Execute batch insert
            with self._oracle_api as connected_api:
                # Build INSERT statement
                sql_result = connected_api.build_insert_statement(
                    table_name=table_name,
                    columns=["DATA", "_SDC_EXTRACTED_AT", "_SDC_LOADED_AT"],
                    schema_name=self._config.default_target_schema,
                )

                if sql_result.is_failure:
                    return FlextResult.fail(
                        f"Failed to build INSERT: {sql_result.error}",
                    )

                sql_str = sql_result.data
                if sql_str is None:
                    return FlextResult.fail("INSERT statement creation returned None")

                # Prepare batch operations
                batch_operations: list[tuple[str, dict[str, object] | None]] = []
                for record in batch.current_batch:
                    params: dict[str, object] = {
                        "DATA": json.dumps(record),
                        "_SDC_EXTRACTED_AT": record.get("_sdc_extracted_at", loaded_at),
                        "_SDC_LOADED_AT": loaded_at,
                    }
                    batch_operations.append((sql_str, params))

                # Execute batch
                result = connected_api.execute_batch(batch_operations)
                if result.is_failure:
                    # Update statistics with error
                    stats = self._statistics[stream_name]
                    self._statistics[stream_name] = stats.add_error(
                        f"Batch insert failed: {result.error}",
                    )
                    return FlextResult.fail(f"Batch insert failed: {result.error}")

                # Update batch and statistics
                records_processed = len(batch.current_batch)
                self._batches[stream_name] = batch.clear_batch()

                # Update statistics
                stats = self._statistics[stream_name]
                self._statistics[stream_name] = stats.model_copy(
                    update={
                        "successful_records": stats.successful_records
                        + records_processed,
                        "total_records_processed": stats.total_records_processed
                        + records_processed,
                        "batches_processed": stats.batches_processed + 1,
                    },
                )

                logger.info(f"Flushed {records_processed} records to {table_name}")
                return FlextResult.ok(None)

        except Exception as e:
            logger.exception("Failed to flush batch")
            return FlextResult.fail(f"Batch flush failed: {e}")

    async def flush_all_batches(self) -> FlextResult[LoadStatisticsModel]:
        """Flush all pending batches.

        Returns:
            FlextResult containing aggregated load statistics

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
            all_errors: list[str] = []

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

            return FlextResult.ok(aggregated_stats)

        except Exception as e:
            logger.exception("Failed to flush all batches")
            return FlextResult.fail(f"Batch flush all failed: {e}")


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

        """
        self._config = config

    def transform_record(
        self,
        record: dict[str, object],
        stream: SingerStreamModel,
    ) -> FlextResult[dict[str, object]]:
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

            return FlextResult.ok(transformed_record)

        except Exception as e:
            logger.exception("Failed to transform record")
            return FlextResult.fail(f"Record transformation failed: {e}")

    def validate_record(
        self,
        record: dict[str, object],
        schema: dict[str, object],
    ) -> FlextResult[None]:
        """Validate record against schema."""
        try:
            properties = schema.get("properties", {})
            required_fields = schema.get("required", [])

            # Validate required fields
            required_validation = self._validate_required_fields(
                record, required_fields if isinstance(required_fields, list) else [],
            )
            if required_validation.is_failure:
                return required_validation

            # Validate field types
            type_validation = self._validate_field_types(
                record, properties if isinstance(properties, dict) else {},
            )
            if type_validation.is_failure:
                return type_validation

            return FlextResult.ok(None)

        except Exception as e:
            logger.exception("Failed to validate record")
            return FlextResult.fail(f"Record validation failed: {e}")

    def _validate_required_fields(
        self,
        record: dict[str, object],
        required_fields: list[str],
    ) -> FlextResult[None]:
        """Validate required fields are present."""
        for field in required_fields:
            if field not in record:
                return FlextResult.fail(f"Missing required field: {field}")
        return FlextResult.ok(None)

    def _validate_field_types(
        self,
        record: dict[str, object],
        properties: dict[str, object],
    ) -> FlextResult[None]:
        """Validate field types match schema."""
        type_validators: dict[str, _Callable[[object], bool]] = {
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
                            return FlextResult.fail(
                                f"Field {field_name} should be {expected_type}, got {type(field_value)}",
                            )

        return FlextResult.ok(None)


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
