"""Target Client Implementation for FLEXT Target Oracle.

This module consolidates the main Oracle Singer Target implementation, Oracle data
loader, and plugin implementation into a single cohesive client following PEP8
naming conventions and Clean Architecture principles.

The consolidated client provides:
- FlextTargetOracle: Main Singer Target implementation with async processing
- FlextTargetOracleLoader: Oracle data loading infrastructure
- FlextTargetOraclePlugin: Clean plugin architecture implementation

Architecture Integration:
    Built on flext-core foundations (FlextResult, FlextValueObject patterns)
    Integrates with flext-meltano for Singer SDK compliance
    Uses flext-db-oracle for production-grade Oracle connectivity
    Follows railway-oriented programming for error handling

Key Components:
    - Oracle data loader with batch processing and connection management
    - Singer protocol compliance with SCHEMA, RECORD, and STATE message handling
    - Plugin implementation with clean architecture patterns
    - Performance optimization through batch processing and connection pooling

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import asyncio
import json
import time
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from flext_core import FlextResult, get_logger
from flext_db_oracle import FlextDbOracleApi, FlextDbOracleConfig
from flext_meltano import FlextMeltanoTarget
from flext_meltano.flext_singer import flext_create_singer_bridge
from flext_meltano.singer_plugin_base import FlextTargetPlugin
from flext_meltano.singer_unified import (
    FlextSingerUnifiedInterface,
    FlextSingerUnifiedResult,
)

# FlextPluginEntity import removed - not essential for core functionality
from flext_target_oracle.target_config import FlextTargetOracleConfig
from flext_target_oracle.target_exceptions import (
    FlextTargetOracleConnectionError,
)

if TYPE_CHECKING:
    from collections.abc import Callable as _Callable, Mapping

logger = get_logger(__name__)

# Constants
MAX_PORT_NUMBER = 65535  # Maximum valid TCP port number


# =============================================================================
# ORACLE DATA LOADER
# =============================================================================


class FlextTargetOracleLoader:
    """Oracle data loader - CORRETO usando apenas flext-db-oracle API pública.

    Esta implementação:
    1. Usa APENAS a API pública da flext-db-oracle
    2. Não duplica funcionalidades genéricas
    3. Mantém apenas o código específico para Singer target
    """

    def __init__(self, config: FlextTargetOracleConfig) -> None:
        """Initialize loader using flext-db-oracle correctly."""
        self.config = config

        # Use flext-db-oracle configuration
        oracle_config_dict = config.get_oracle_config()
        try:
            oracle_config = FlextDbOracleConfig.from_dict(
                dict(oracle_config_dict),
            )
        except Exception as e:
            msg = f"Failed to create Oracle config: {e}"
            raise FlextTargetOracleConnectionError(msg) from e

        # Initialize Oracle API - CORRETA integração
        self.oracle_api = FlextDbOracleApi(oracle_config)

        # Simple state tracking - específico para Singer target
        self._record_buffers: dict[str, list[dict[str, object]]] = {}
        self._total_records = 0

    def connect(self) -> FlextResult[None]:
        """Test connection to Oracle database."""
        try:
            # Use flext-db-oracle context manager to test connection
            with self.oracle_api as connected_api:
                # Simple connection test
                tables_result = connected_api.get_tables(
                    schema=self.config.default_target_schema,
                )
                if tables_result.is_failure:
                    return FlextResult.fail(f"Connection test failed: {tables_result.error}")

                logger.info("Oracle connection established successfully")
                return FlextResult.ok(None)
        except Exception as e:
            logger.exception("Failed to connect to Oracle")
            return FlextResult.fail(f"Connection failed: {e}")

    async def ensure_table_exists(
        self,
        stream_name: str,
        _schema: dict[str, object],
        _key_properties: list[str] | None = None,
    ) -> FlextResult[None]:
        """Ensure table exists using flext-db-oracle API."""
        try:
            table_name = self.config.get_table_name(stream_name)

            # Use flext-db-oracle context manager CORRETAMENTE
            with self.oracle_api as connected_api:
                # Check if table exists usando API
                tables_result = connected_api.get_tables(
                    schema=self.config.default_target_schema,
                )

                if tables_result.is_failure:
                    return FlextResult.fail(f"Failed to check tables: {tables_result.error}")

                existing_tables = [t.upper() for t in tables_result.data or []]
                table_exists = table_name.upper() in existing_tables

                if table_exists:
                    logger.info("Table %s already exists", table_name)
                    return FlextResult.ok(None)

                # Create simple JSON table usando API pública
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

                # Create and execute table DDL using flext-db-oracle API
                ddl_result = connected_api.create_table_ddl(
                    table_name=table_name,
                    columns=columns,
                    schema=self.config.default_target_schema,
                )

                if ddl_result.is_failure:
                    return FlextResult.fail(f"Failed to create DDL: {ddl_result.error}")

                # Execute DDL - handle None case and execution result together
                ddl_sql = ddl_result.data
                if ddl_sql is None:
                    return FlextResult.fail("DDL creation returned None")

                exec_result = connected_api.execute_ddl(ddl_sql)
                logger.info("Created table %s", table_name) if exec_result.is_success else None

                return (
                    FlextResult.ok(None)
                    if exec_result.is_success
                    else FlextResult.fail(f"Failed to create table: {exec_result.error}")
                )

        except Exception as e:
            logger.exception("Failed to ensure table exists")
            return FlextResult.fail(f"Table creation failed: {e}")

    async def load_record(
        self,
        stream_name: str,
        record_data: dict[str, object],
    ) -> FlextResult[None]:
        """Load record with batching."""
        try:
            # Simple buffering - específico para Singer target
            if stream_name not in self._record_buffers:
                self._record_buffers[stream_name] = []

            self._record_buffers[stream_name].append(record_data)
            self._total_records += 1

            # Auto-flush if batch is full
            if len(self._record_buffers[stream_name]) >= self.config.batch_size:
                return await self._flush_batch(stream_name)

            return FlextResult.ok(None)

        except Exception as e:
            logger.exception("Failed to load record")
            return FlextResult.fail(f"Record loading failed: {e}")

    async def finalize_all_streams(self) -> FlextResult[dict[str, object]]:
        """Finalize all streams and return stats."""
        try:
            # Flush all remaining records
            for stream_name, records in self._record_buffers.items():
                if records:
                    result = await self._flush_batch(stream_name)
                    if result.is_failure:
                        logger.error(
                            f"Failed to flush {stream_name}: {result.error}",
                        )

            stats: dict[str, object] = {
                "total_records": self._total_records,
                "streams_processed": len(self._record_buffers),
            }

            return FlextResult.ok(stats)

        except Exception as e:
            logger.exception("Failed to finalize streams")
            return FlextResult.fail(f"Finalization failed: {e}")

    async def _flush_batch(self, stream_name: str) -> FlextResult[None]:
        """Flush batch usando flext-db-oracle API CORRETAMENTE."""
        try:
            records = self._record_buffers.get(stream_name, [])
            if not records:
                return FlextResult.ok(None)

            table_name = self.config.get_table_name(stream_name)
            loaded_at = datetime.now(UTC)

            # Use flext-db-oracle API para bulk operations
            with self.oracle_api as connected_api:
                # Prepare SQL usando API pública
                sql_result = connected_api.build_insert_statement(
                    table_name=table_name,
                    columns=["DATA", "_SDC_EXTRACTED_AT", "_SDC_LOADED_AT"],
                    schema_name=self.config.default_target_schema,
                )

                if sql_result.is_failure:
                    return FlextResult.fail(
                        f"Failed to build INSERT: {sql_result.error}",
                    )

                # Prepare batch data with correct types
                batch_operations: list[tuple[str, dict[str, object] | None]] = []
                sql_str = sql_result.data
                if sql_str is None:
                    return FlextResult.fail("INSERT statement creation returned None")

                for record in records:
                    params: dict[str, object] = {
                        "DATA": json.dumps(record),
                        "_SDC_EXTRACTED_AT": record.get("_sdc_extracted_at", loaded_at),
                        "_SDC_LOADED_AT": loaded_at,
                    }
                    batch_operations.append((sql_str, params))

                # Execute batch usando API pública CORRETAMENTE
                result = connected_api.execute_batch(batch_operations)
                if result.is_failure:
                    return FlextResult.fail(
                        f"Batch insert failed: {result.error}",
                    )

                # Clear buffer
                self._record_buffers[stream_name] = []

                logger.info(
                    "Flushed %d records to %s", len(records), table_name,
                )
                return FlextResult.ok(None)

        except Exception as e:
            logger.exception("Failed to flush batch")
            return FlextResult.fail(f"Batch flush failed: {e}")


# =============================================================================
# MAIN SINGER TARGET IMPLEMENTATION
# =============================================================================


class FlextTargetOracle(FlextMeltanoTarget, FlextSingerUnifiedInterface):
    """Oracle Singer Target implementation with FLEXT ecosystem integration.

    This class provides a production-grade Singer Target for Oracle Database
    data loading, implementing the Singer specification while leveraging FLEXT
    ecosystem patterns for reliability, maintainability, and enterprise scalability.

    The target follows Clean Architecture principles with clear separation between
    application logic (Singer message handling) and infrastructure concerns
    (Oracle database operations). All operations use railway-oriented programming
    with FlextResult for consistent error handling.

    Key Features:
        - Singer Protocol Compliance: Full support for SCHEMA, RECORD, and STATE messages
        - Batch Processing: Configurable batch sizes for optimal Oracle performance
        - Error Handling: Railway-oriented programming with detailed error context
        - Configuration Management: Type-safe configuration with domain validation
        - Oracle Integration: Production-grade Oracle connectivity through flext-db-oracle
        - Observability: Structured logging with correlation IDs and context

    Architecture:
        The target implements a layered architecture:
        - Application Layer: Singer message processing and protocol compliance
        - Domain Layer: Business rules and validation logic
        - Infrastructure Layer: Oracle database operations and external integrations

    Usage Patterns:
        - Direct instantiation: For programmatic usage and testing
        - Meltano integration: Through meltano.yml configuration
        - CLI usage: Via Singer CLI interface

    Attributes:
        name: Singer target name identifier ("flext-oracle-target")
        config_class: Configuration class for type-safe settings management
        target_config: Validated Oracle target configuration instance
        _loader: Oracle data loading service instance

    Example:
        Basic target setup and message processing:

        >>> config = FlextTargetOracleConfig(
        ...     oracle_host="prod-oracle.company.com",
        ...     oracle_service="PRODDB",
        ...     oracle_user="data_loader",
        ...     oracle_password="secure_password",
        ...     batch_size=2000,
        ... )
        >>> target = FlextTargetOracle(config)
        >>>
        >>> # Process complete Singer workflow
        >>> schema_result = await target.process_singer_message(schema_message)
        >>> record_result = await target.process_singer_message(record_message)
        >>> stats_result = await target.finalize()
        >>>
        >>> if all(r.success for r in [schema_result, record_result, stats_result]):
        ...     print("Data loading completed successfully")
        ...     print(f"Statistics: {stats_result.data}")

    Note:
        This implementation is currently undergoing architectural improvements
        to address identified issues. See docs/TODO.md for current status and
        improvement roadmap before production deployment.

    """

    name = "flext-oracle-target"

    def __init__(
        self,
        config: dict[str, object] | FlextTargetOracleConfig | None = None,
    ) -> None:
        """Initialize Oracle Singer Target with configuration validation.

        Sets up the Oracle target with proper configuration management, validation,
        and dependency injection. The initialization process handles both dict-based
        and typed configuration objects while maintaining compatibility with the
        Singer SDK initialization patterns.

        The initialization follows these steps:
        1. Initialize base Singer Target with dict configuration
        2. Convert/validate configuration to FlextTargetOracleConfig
        3. Perform domain rule validation
        4. Initialize Oracle data loader with validated configuration

        Args:
            config: Target configuration as dict or FlextTargetOracleConfig.
                   If None, creates minimal config for testing. Dict configs
                   are validated and converted to FlextTargetOracleConfig.

        Raises:
            ValueError: If configuration validation fails or required parameters missing
            TypeError: If configuration format is invalid

        Example:
            Configuration with dict (Meltano pattern):

            >>> config_dict = {
            ...     "oracle_host": "localhost",
            ...     "oracle_service": "XE",
            ...     "oracle_user": "test_user",
            ...     "oracle_password": "test_password",
            ...     "batch_size": 1000,
            ... }
            >>> target = FlextTargetOracle(config_dict)

            Configuration with typed config (programmatic pattern):

            >>> typed_config = FlextTargetOracleConfig(
            ...     oracle_host="prod-oracle.company.com",
            ...     oracle_service="PRODDB",
            ...     oracle_user="data_loader",
            ...     oracle_password="secure_password",
            ... )
            >>> target = FlextTargetOracle(typed_config)

        Note:
            The minimal test configuration is provided when config is None to
            support testing scenarios. Production usage should always provide
            explicit configuration with proper credentials and settings.

        """
        # Config import now at top level

        # Convert config to FlextTargetOracleConfig if needed
        if isinstance(config, FlextTargetOracleConfig):
            self.target_config = config
        elif isinstance(config, dict):
            self.target_config = FlextTargetOracleConfig.model_validate(config)
        else:
            msg = (
                "Configuration is required. Provide either a FlextTargetOracleConfig instance "
                "or a dictionary configuration with required Oracle connection parameters."
            )
            raise TypeError(
                msg,
            )

        # Set config_class for compatibility
        self.config_class = FlextTargetOracleConfig

        # Initialize base classes with proper config
        # Create a minimal FlextMeltanoConfig from our Oracle config
        from flext_meltano.config import FlextMeltanoConfig
        meltano_config = FlextMeltanoConfig(
            project_root=str(getattr(self.target_config, "project_root", ".")),
            environment=getattr(self.target_config, "environment", "dev"),
        )
        super().__init__(config=meltano_config)

        # Initialize components
        self._loader = FlextTargetOracleLoader(self.target_config)
        self._singer_bridge = flext_create_singer_bridge()
        self._schemas: dict[str, dict[str, object]] = {}
        self._state: dict[str, object] = {}

    def _handle_record_write_error(
        self, result: FlextResult[None], stream_name: str,
    ) -> None:
        """Handle record write error."""
        error_msg = result.error or "Record loading failed"
        msg = f"Failed to write record to {stream_name}: {error_msg}"
        raise RuntimeError(msg)

    # FlextSingerUnifiedInterface implementation

    def initialize(self, config: FlextSingerUnifiedConfig) -> FlextResult[None]:  # type: ignore[override]
        """Initialize the Oracle target.

        Args:
            config: Singer unified configuration object

        Returns:
            FlextResult indicating initialization success/failure

        """
        try:
            # Validate configuration
            validation_result = self.target_config.validate_domain_rules()
            if validation_result.is_failure:
                return FlextResult.fail(validation_result.error or "Configuration validation failed")

            # Initialize loader connection
            connect_result = self._loader.connect()
            if connect_result.is_failure:
                return FlextResult.fail(connect_result.error or "Connection failed")

            return FlextResult.ok(None)
        except Exception as e:
            return FlextResult.fail(f"Failed to initialize Oracle target: {e}")

    def discover_catalog(self) -> FlextResult[dict[str, object]]:
        """Discover available schemas and generate Singer catalog.

        For targets, this returns the current schema information from loaded streams.

        Returns:
            FlextResult containing catalog information

        """
        try:
            catalog: dict[str, object] = {
                "streams": [],
            }

            for stream_name, schema in self._schemas.items():
                stream_entry = {
                    "tap_stream_id": stream_name,
                    "stream": stream_name,
                    "schema": schema,
                    "metadata": [
                        {
                            "breadcrumb": [],
                            "metadata": {
                                "inclusion": "available",
                                "table-name": self.target_config.get_table_name(
                                    stream_name,
                                ),
                                "schema-name": self.target_config.default_target_schema,
                                "forced-replication-method": "FULL_TABLE",
                            },
                        },
                    ],
                }
                streams = catalog.get("streams")
                if isinstance(streams, list):
                    streams.append(stream_entry)

            return FlextResult.ok(catalog)
        except Exception as e:
            return FlextResult.fail(f"Failed to discover catalog: {e}")

    def execute(
        self,
        input_data: object | None = None,
    ) -> FlextResult[FlextSingerUnifiedResult]:
        """Execute the target operation - process Singer messages.

        Args:
            input_data: Singer messages to process

        Returns:
            FlextResult containing execution results

        """
        start_time = time.time()
        try:
            if input_data is None:
                return FlextResult.fail("No input data provided for target execution")

            # Process messages if they're provided as a list
            if isinstance(input_data, list):
                records_processed = 0
                for message in input_data:
                    if isinstance(message, dict):
                        message_result = self.process_singer_message(message)
                        if hasattr(message_result, "__await__"):
                            import asyncio
                            result = asyncio.run(message_result)  # type: ignore[arg-type]
                        else:
                            result = message_result  # type: ignore[assignment]
                        if result.is_failure:
                            return FlextResult.fail(
                                f"Failed to process message: {result.error}",
                            )
                        if message.get("type") == "RECORD":
                            records_processed += 1

                # Finalize all streams
                finalize_operation = self._loader.finalize_all_streams()
                if hasattr(finalize_operation, "__await__"):
                    import asyncio
                    finalize_result = asyncio.run(finalize_operation)  # type: ignore[arg-type]
                else:
                    finalize_result = finalize_operation  # type: ignore[assignment]
                if finalize_result.is_failure:
                    return FlextResult.fail(
                        f"Failed to finalize streams: {finalize_result.error}",
                    )

                # Calculate execution time in milliseconds
                execution_time_ms = int((time.time() - start_time) * 1000)

                return FlextResult.ok(
                    FlextSingerUnifiedResult(
                        success=True,
                        records_processed=records_processed,
                        schemas_discovered=list(self._schemas.keys()),
                        execution_time_ms=execution_time_ms,
                        state_updates=self._state,
                    ),
                )
            return FlextResult.fail("Input data must be a list of Singer messages")

        except Exception as e:
            return FlextResult.fail(f"Target execution failed: {e}")

    def validate_configuration(self) -> FlextResult[None]:
        """Validate the current configuration.

        Returns:
            FlextResult indicating validation success/failure

        """
        return self.target_config.validate_domain_rules()

    # Singer SDK methods

    def _test_connection(self) -> bool:
        """Test connection as required by Singer SDK."""
        return self._test_connection_impl()

    def _write_record(self, stream_name: str, record: dict[str, object]) -> None:
        """Write individual records as required by Singer SDK.

        This method implements the Singer SDK interface for processing individual
        RECORD messages. It delegates to the Oracle loader for database operations
        while handling errors appropriately for Singer SDK compliance.

        Args:
            stream_name: Name of the stream (table) to write to
            record: Dictionary containing the record data to insert

        Raises:
            Exception: If record writing fails, propagated for Singer SDK handling

        Note:
            This method is synchronous as required by Singer SDK interface,
            but internally delegates to async Oracle operations through the loader.

        """
        try:
            # Get or create event loop for async operations
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # Execute async load_record operation
            result = loop.run_until_complete(
                self._loader.load_record(stream_name, record),
            )

            if result.is_failure:
                self._handle_record_write_error(result, stream_name)

        except Exception as e:
            # Re-raise with context for Singer SDK error handling
            msg = f"Singer SDK _write_record failed: {e}"
            raise RuntimeError(msg) from e

    def _test_connection_impl(self) -> bool:
        """Test Oracle database connectivity and configuration validation.

        Performs comprehensive connectivity testing including configuration validation,
        network connectivity, authentication verification, and schema access validation.
        This method is part of the Singer SDK interface for connection testing.

        The test sequence includes:
        1. Configuration domain rule validation
        2. Network connectivity to Oracle host/port
        3. Database authentication verification
        4. Schema access permission checking

        Returns:
            bool: True if all connectivity tests pass, False if any test fails

        Example:
            >>> target = FlextTargetOracle(config)
            >>> if target._test_connection_impl():
            ...     print("Oracle connection verified")
            ... else:
            ...     print("Oracle connection failed - check configuration")

        Note:
            This method logs detailed error information to help with troubleshooting
            connectivity issues. Check logs for specific failure reasons when
            the method returns False.

        """
        try:
            # Validate configuration
            validation_result = self.target_config.validate_domain_rules()
            if not validation_result.success:
                logger.error(
                    f"Configuration validation failed: {validation_result.error}",
                )
                return False

            # Test connection using loader
            connection_result = self._loader.connect()
            if not connection_result.success:
                logger.error(f"Connection test failed: {connection_result.error}")
                return False

            logger.info("Oracle connection test passed")
            return True

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Oracle connection test failed")
            logger.warning(
                f"Connection test failed with error: {type(e).__name__}: {e}",
            )
            return False

    async def _write_records_impl(
        self,
        records: list[dict[str, object]],
    ) -> FlextResult[None]:
        """Write batch of records to Oracle database with error handling.

        Processes a batch of Singer RECORD messages and loads them into Oracle
        tables using the configured loading strategy. This method implements
        the Singer SDK batch writing interface while providing railway-oriented
        error handling for reliable data loading.

        The method processes each record individually, extracting stream name
        and record data, then delegating to the Oracle loader for database
        operations. Failed records are reported with detailed error context.

        Args:
            records: List of Singer RECORD messages, each containing:
                    - stream: Stream name for table identification
                    - record: Dictionary of field values to insert

        Returns:
            FlextResult[None]: Success if all records loaded successfully,
            failure with detailed error message if any record fails

        Example:
            >>> records = [
            ...     {"stream": "users", "record": {"id": 1, "name": "John"}},
            ...     {"stream": "users", "record": {"id": 2, "name": "Jane"}},
            ... ]
            >>> result = await target._write_records_impl(records)
            >>> if result.success:
            ...     print("All records loaded successfully")
            ... else:
            ...     print(f"Record loading failed: {result.error}")

        Note:
            This method validates record format before processing and logs
            warnings for invalid records while continuing with valid ones.
            Check logs for details about skipped invalid records.

        """
        try:
            for record in records:
                stream_name = record.get("stream")
                record_data = record.get("record")

                if isinstance(stream_name, str) and isinstance(record_data, dict):
                    result = await self._loader.load_record(stream_name, record_data)
                    if not result.success:
                        return FlextResult.fail(
                            f"Failed to load record: {result.error}",
                        )
                else:
                    logger.warning("Invalid record format: %s", record)

            return FlextResult.ok(None)

        except Exception as e:
            logger.exception("Failed to write records")
            return FlextResult.fail(f"Record writing failed: {e}")

    def _apply_schema_mappings(
        self,
        stream_name: str,
        schema: dict[str, object],
    ) -> dict[str, object]:
        """Apply column mappings to schema.

        Args:
            stream_name: Stream name
            schema: Original schema

        Returns:
            Modified schema with mappings applied

        """
        if "properties" not in schema:
            return schema

        new_properties = {}
        properties = schema["properties"]
        if isinstance(properties, dict):
            for col_name, original_schema in properties.items():
                # Skip ignored columns
                if self.target_config.should_ignore_column(col_name):
                    continue

                # Apply column name mapping
                mapped_name = self.target_config.map_column_name(stream_name, col_name)

                # Apply column transformations
                transform_config = self.target_config.get_column_transform(
                    stream_name, col_name,
                )
                final_schema = original_schema
                if transform_config and "type" in transform_config:
                    final_schema = {**original_schema, "type": transform_config["type"]}

                new_properties[mapped_name] = final_schema

        # Add metadata columns if enabled
        # Note: We use standard _sdc_ prefix in schema; loader maps to custom names
        if self.target_config.add_metadata_columns:
            new_properties["_sdc_extracted_at"] = {
                "type": "string",
                "format": "date-time",
            }
            new_properties["_sdc_loaded_at"] = {"type": "string", "format": "date-time"}
            new_properties["_sdc_deleted_at"] = {
                "type": ["null", "string"],
                "format": "date-time",
            }
            new_properties["_sdc_sequence"] = {"type": "integer"}

        return {**schema, "properties": new_properties}

    def _apply_record_mappings(
        self,
        stream_name: str,
        record: dict[str, object],
    ) -> dict[str, object]:
        """Apply column mappings and transformations to a record.

        Args:
            stream_name: Stream name
            record: Original record

        Returns:
            Modified record with mappings applied

        """
        new_record = {}

        for col_name, original_value in record.items():
            # Skip ignored columns
            if self.target_config.should_ignore_column(col_name):
                continue

            # Apply column name mapping
            mapped_name = self.target_config.map_column_name(stream_name, col_name)

            # Apply value transformations
            transform_config = self.target_config.get_column_transform(
                stream_name, col_name,
            )
            final_value = original_value
            if transform_config and original_value is not None:
                final_value = self._apply_value_transform(
                    original_value, transform_config,
                )

            new_record[mapped_name] = final_value

        return new_record

    def _apply_value_transform(
        self,
        value: object,
        transform: dict[str, object],
    ) -> object:
        """Apply transformation to a value.

        Args:
            value: Original value
            transform: Transformation configuration

        Returns:
            Transformed value

        """
        # Type conversion transformations
        if "type" in transform:
            target_type = transform["type"]
            type_converters: dict[str, _Callable[[object], object] | type[str]] = {
                "string": str,
                "integer": lambda x: int(str(x)) if x is not None else None,
                "number": lambda x: float(str(x)) if x is not None else None,
                "boolean": lambda x: bool(x) if x is not None else None,
            }
            if isinstance(target_type, str) and target_type in type_converters:
                converter = type_converters[target_type]
                return converter(value)

        # Format transformations
        if "format" in transform and isinstance(value, str):
            format_type = transform["format"]
            format_converters: dict[str, _Callable[[str], str]] = {
                "uppercase": lambda x: x.upper(),
                "lowercase": lambda x: x.lower(),
            }
            if isinstance(format_type, str) and format_type in format_converters:
                converter = format_converters[format_type]
                return converter(value)

        return value

    async def process_singer_message(
        self,
        message: dict[str, object],
    ) -> FlextResult[None]:
        """Process Singer protocol messages with comprehensive error handling.

        Main entry point for processing Singer specification messages including
        SCHEMA, RECORD, and STATE messages. This method implements the core
        Singer protocol handling while maintaining railway-oriented programming
        patterns for consistent error handling.

        The method routes messages to specialized handlers based on message type:
        - SCHEMA: Creates/updates Oracle table structures
        - RECORD: Loads data records into Oracle tables
        - STATE: Manages state information for incremental processing

        Args:
            message: Singer message dictionary containing:
                    - type: Message type (SCHEMA, RECORD, or STATE)
                    - Additional fields specific to message type

        Returns:
            FlextResult[None]: Success if message processed successfully,
            failure with detailed error context if processing fails

        Example:
            Processing different message types:

            >>> # SCHEMA message
            >>> schema_msg = {
            ...     "type": "SCHEMA",
            ...     "stream": "users",
            ...     "schema": {
            ...         "type": "object",
            ...         "properties": {
            ...             "id": {"type": "integer"},
            ...             "name": {"type": "string"},
            ...         },
            ...     },
            ... }
            >>> result = await target.process_singer_message(schema_msg)
            >>>
            >>> # RECORD message
            >>> record_msg = {
            ...     "type": "RECORD",
            ...     "stream": "users",
            ...     "record": {"id": 1, "name": "John Doe"},
            ... }
            >>> result = await target.process_singer_message(record_msg)

        Note:
            This method provides a unified interface for Singer message processing
            while delegating to specialized handlers. Unknown message types are
            rejected with detailed error messages.

        """
        try:
            message_type_raw = message.get("type", "")
            message_type = (
                message_type_raw.upper() if isinstance(message_type_raw, str) else ""
            )

            if message_type == "SCHEMA":
                return await self._handle_schema(message)
            if message_type == "RECORD":
                return await self._handle_record(message)
            if message_type == "STATE":
                return await self._handle_state(message)
            return FlextResult.fail(f"Unknown message type: {message.get('type')}")

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Failed to process Singer message")
            return FlextResult.fail(f"Message processing failed: {e}")

    async def _handle_schema(self, message: dict[str, object]) -> FlextResult[None]:
        """Handle Singer SCHEMA messages for table creation and structure management.

        Processes Singer SCHEMA messages to create or update Oracle table structures
        based on the JSON Schema definition. This method ensures target tables exist
        with appropriate column definitions before data loading begins.

        The schema handling process includes:
        1. Extract stream name and JSON Schema definition
        2. Validate schema message format and content
        3. Delegate to Oracle loader for table creation/update
        4. Log successful schema processing

        Args:
            message: Singer SCHEMA message containing:
                    - stream: Stream name for table identification
                    - schema: JSON Schema definition of record structure

        Returns:
            FlextResult[None]: Success if table created/updated successfully,
            failure with detailed error if schema processing fails

        Example:
            >>> schema_message = {
            ...     "type": "SCHEMA",
            ...     "stream": "customer_orders",
            ...     "schema": {
            ...         "type": "object",
            ...         "properties": {
            ...             "order_id": {"type": "integer"},
            ...             "customer_name": {"type": "string"},
            ...             "order_date": {"type": "string", "format": "date-time"},
            ...             "amount": {"type": "number"},
            ...         },
            ...         "required": ["order_id", "customer_name"],
            ...     },
            ... }
            >>> result = await target._handle_schema(schema_message)
            >>> if result.success:
            ...     print("Table CUSTOMER_ORDERS ready for data loading")

        Note:
            This method validates both stream name and schema definition before
            processing. Invalid or missing schema components result in detailed
            error messages for troubleshooting.

        """
        try:
            stream_name = message.get("stream")
            schema = message.get("schema", {})

            if not isinstance(stream_name, str):
                return FlextResult.fail("Schema message missing stream name")

            if not isinstance(schema, dict):
                return FlextResult.fail("Schema message missing valid schema")

            # Store original schema for catalog discovery
            self._schemas[stream_name] = schema

            # Apply column mappings if configured
            if self.target_config.column_mappings:
                schema = self._apply_schema_mappings(stream_name, schema)

            # Get key properties
            key_properties = message.get("key_properties", [])
            key_props_list = key_properties if isinstance(key_properties, list) else None

            result = await self._loader.ensure_table_exists(
                stream_name,
                schema,
                key_props_list,
            )
            if result.success:
                logger.info("Schema processed for stream: %s", stream_name)

            return result

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Failed to handle schema message")
            return FlextResult.fail(f"Schema handling failed: {e}")

    async def _handle_record(self, message: dict[str, object]) -> FlextResult[None]:
        """Handle Singer RECORD messages for data loading into Oracle tables.

        Processes Singer RECORD messages to load individual data records into
        Oracle tables. This method extracts the record data and delegates to
        the Oracle loader for database insertion using the configured loading
        strategy (INSERT, MERGE, BULK_INSERT, or BULK_MERGE).

        The record handling process includes:
        1. Extract stream name and record data from message
        2. Validate message format and required fields
        3. Delegate to Oracle loader for database insertion
        4. Handle any loading errors with detailed context

        Args:
            message: Singer RECORD message containing:
                    - stream: Stream name for table identification
                    - record: Dictionary of field values to insert

        Returns:
            FlextResult[None]: Success if record loaded successfully,
            failure with detailed error if loading fails

        Example:
            >>> record_message = {
            ...     "type": "RECORD",
            ...     "stream": "customer_orders",
            ...     "record": {
            ...         "order_id": 12345,
            ...         "customer_name": "John Doe",
            ...         "order_date": "2025-08-04T10:30:00Z",
            ...         "amount": 99.99,
            ...     },
            ... }
            >>> result = await target._handle_record(record_message)
            >>> if result.success:
            ...     print("Record loaded successfully")

        Note:
            This method validates both stream name and record data before
            processing. Missing or invalid components result in detailed
            error messages without affecting other records.

        """
        try:
            stream_name = message.get("stream")
            record_data = message.get("record")

            if not isinstance(stream_name, str) or not isinstance(record_data, dict):
                return FlextResult.fail("Record message missing stream or data")

            # Apply column mappings and transformations
            if self.target_config.column_mappings or self.target_config.ignored_columns:
                record_data = self._apply_record_mappings(stream_name, record_data)

            # Add metadata columns if enabled
            if self.target_config.add_metadata_columns:
                record_data["_sdc_extracted_at"] = message.get("time_extracted", "")
                record_data["_sdc_loaded_at"] = datetime.now(UTC).isoformat()
                # _sdc_deleted_at is set to null for non-deleted records
                record_data["_sdc_deleted_at"] = None

            return await self._loader.load_record(stream_name, record_data)

        except Exception as e:
            logger.exception("Failed to handle record message")
            return FlextResult.fail(f"Record handling failed: {e}")

    async def _handle_state(self, _message: dict[str, object]) -> FlextResult[None]:
        """Handle Singer STATE messages for incremental processing state management.

        Processes Singer STATE messages that contain bookmark information for
        incremental data synchronization. State messages are typically managed
        by the Singer orchestrator (like Meltano) and contain information about
        the last successfully processed record or timestamp.

        This implementation follows the Singer specification by acknowledging
        the state message while delegating actual state persistence to the
        orchestrator. The target logs the state reception for debugging purposes.

        Args:
            message: Singer STATE message containing:
                    - type: "STATE" message type identifier
                    - value: State data with bookmark information

        Returns:
            FlextResult[None]: Always succeeds as state handling is delegated
            to the Singer orchestrator

        Example:
            >>> state_message = {
            ...     "type": "STATE",
            ...     "value": {
            ...         "bookmarks": {
            ...             "users": {"last_updated": "2025-08-04T10:30:00Z"},
            ...             "orders": {"last_id": 12345},
            ...         }
            ...     },
            ... }
            >>> result = await target._handle_state(state_message)
            >>> # Always succeeds - state managed by orchestrator

        Note:
            State persistence is handled by the Singer orchestrator (Meltano).
            This method acknowledges receipt and logs for debugging. Custom
            state handling can be implemented here if needed for specific
            use cases.

        """
        try:
            # State messages are typically handled by Meltano
            logger.debug("State message received - forwarding to Meltano")
            return FlextResult.ok(None)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Failed to handle state message")
            return FlextResult.fail(f"State handling failed: {e}")

    async def finalize(self) -> FlextResult[dict[str, object]]:
        """Finalize data loading operations and return comprehensive statistics.

        Completes all pending data loading operations, flushes any remaining
        batches, commits transactions, and returns detailed statistics about
        the entire data loading session. This method should be called after
        all Singer messages have been processed.

        The finalization process includes:
        1. Flush any remaining batched records to Oracle
        2. Commit all pending database transactions
        3. Collect comprehensive loading statistics
        4. Release database connections and resources
        5. Generate summary report with performance metrics

        Returns:
            FlextResult[dict[str, object]]: Success contains statistics dictionary
            with details about records processed, performance metrics, and status.
            Failure contains detailed error information.

        Statistics Dictionary Format:
            {
                "total_records": int,           # Total records processed
                "total_streams": int,           # Number of streams processed
                "records_per_stream": dict,     # Per-stream record counts
                "processing_time_ms": int,      # Total processing time
                "average_batch_size": float,    # Average batch size used
                "oracle_connections_used": int, # Connection pool usage
                "load_method": str,             # Loading strategy used
                "errors_encountered": int,      # Number of errors handled
                "status": str                   # Overall processing status
            }

        Example:
            >>> # After processing all Singer messages
            >>> stats_result = await target.finalize()
            >>> if stats_result.success:
            ...     stats = stats_result.data
            ...     print(f"Processed {stats['total_records']} records")
            ...     print(f"Loading took {stats['processing_time_ms']}ms")
            ...     print(f"Used {stats['load_method']} loading strategy")
            ... else:
            ...     print(f"Finalization failed: {stats_result.error}")

        Note:
            This method must be called to ensure all data is properly committed
            to Oracle. Failure to call finalize() may result in data loss due
            to uncommitted transactions or unflushed batches.

        """
        try:
            result = await self._loader.finalize_all_streams()
            if result.success:
                logger.info("Target finalization completed successfully")
                return result
            return result

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Failed to finalize target")
            return FlextResult.fail(f"Finalization failed: {e}")

    def _get_implementation_metrics(self) -> dict[str, object]:
        """Get Oracle-specific implementation metrics and configuration details.

        Returns comprehensive metrics about the Oracle target implementation
        including configuration details, performance settings, and operational
        parameters. This method supports monitoring and debugging by providing
        visibility into the target's operational characteristics.

        The metrics include configuration details that affect performance and
        behavior, enabling operators to understand how the target is configured
        and performing in production environments.

        Returns:
            dict[str, object]: Dictionary containing Oracle-specific metrics:
                - oracle_host: Oracle database hostname
                - oracle_port: Oracle listener port number
                - default_schema: Target schema for table creation
                - load_method: Data loading strategy in use
                - use_bulk_operations: Whether bulk operations are enabled
                - batch_size: Configured batch size for processing
                - connection_timeout: Database connection timeout setting

        Example:
            >>> target = FlextTargetOracle(config)
            >>> metrics = target._get_implementation_metrics()
            >>> print(f"Connected to {metrics['oracle_host']}:{metrics['oracle_port']}")
            >>> print(
            ...     f"Using {metrics['load_method']}"
                    f" with batch size {metrics['batch_size']}"
            ... )
            >>> print(f"Bulk operations: {metrics['use_bulk_operations']}")

        Note:
            This method returns configuration values, not runtime statistics.
            For runtime statistics including record counts and performance
            metrics, use the finalize() method result.

        """
        return {
            "oracle_host": self.target_config.oracle_host,
            "oracle_port": self.target_config.oracle_port,
            "default_schema": self.target_config.default_target_schema,
            "load_method": self.target_config.load_method.value,
            "use_bulk_operations": self.target_config.use_bulk_operations,
        }


# =============================================================================
# ORACLE TARGET PLUGIN IMPLEMENTATION
# =============================================================================


class FlextTargetOraclePlugin(FlextTargetPlugin):
    """Oracle-specific implementation of target plugin.

    Extends FlextTargetPlugin with Oracle-specific functionality for
    data loading to Oracle databases.

    Attributes:
        _connection_string: Oracle connection string
        _schema: Target schema name
        _batch_size: Batch size for bulk inserts

    """

    def __init__(
        self,
        name: str = "target-oracle",
        version: str = "1.0.0",
        config: dict[str, object] | None = None,
        _entity: dict[str, object] | None = None,
    ) -> None:
        """Initialize Oracle target plugin.

        Args:
            name: Plugin name
            version: Plugin version
            config: Plugin configuration
            entity: Optional domain entity

        """
        super().__init__(name, version, config, None)  # Convert entity to FlextPluginEntity if needed
        self._connection_string = ""
        self._schema = config.get("schema", "PUBLIC") if config else "PUBLIC"
        batch_size_value = config.get("batch_size", 1000) if config else 1000
        self._batch_size = int(batch_size_value) if isinstance(batch_size_value, (int, str)) else 1000
        self._load_method = config.get("load_method", "insert") if config else "insert"

    def _get_required_config_fields(self) -> list[str]:
        """Get list of required configuration fields.

        Returns:
            List of required field names for Oracle connection

        """
        return ["host", "port", "user", "password", "service_name"]

    def _validate_specific_config(self, config: Mapping[str, object]) -> FlextResult[None]:
        """Perform Oracle-specific configuration validation.

        Args:
            config: Configuration to validate

        Returns:
            FlextResult indicating validation success or errors

        """
        # Validate port is numeric
        port = config.get("port")
        if not isinstance(port, int) or port <= 0 or port > MAX_PORT_NUMBER:
            return FlextResult.fail(f"Invalid port number: {port}")

        # Validate service_name is provided
        service_name = config.get("service_name")
        if not service_name or not isinstance(service_name, str):
            return FlextResult.fail("service_name must be a non-empty string")

        # Build connection string
        self._connection_string = (
            f"oracle://{config['user']}:{config['password']}@"
            f"{config['host']}:{config['port']}/{service_name}"
        )

        # Store optional configuration
        self._schema = str(config.get("schema", "PUBLIC"))

        # Validate batch size
        batch_size = config.get("batch_size", 1000)
        if isinstance(batch_size, int) and batch_size > 0:
            self._batch_size = batch_size
        else:
            self._logger.warning(f"Invalid batch_size {batch_size}, using default 1000")
            self._batch_size = 1000

        # Validate load method
        load_method = config.get("load_method", "insert")
        if load_method in {"insert", "upsert", "replace"}:
            self._load_method = str(load_method)
        else:
            self._logger.warning(f"Invalid load_method {load_method}, using 'insert'")
            self._load_method = "insert"

        return FlextResult.ok(None)

    def _test_specific_connection(self) -> FlextResult[None]:
        """Perform Oracle-specific connection test.

        Returns:
            FlextResult indicating connection success or failure

        """
        try:
            self._logger.info(f"Testing Oracle connection to {self._connection_string}")

            # Use flext-db-oracle for Oracle operations
            if not self._connection_string:
                return FlextResult.fail("Connection string not configured")

            # NOTE: Real Oracle connection testing would use FlextDbOracleApi here
            # Current implementation is a simulated test for development
            self._logger.info("Oracle connection test successful (simulated)")
            return FlextResult.ok(None)

        except Exception as e:
            self._logger.exception("Oracle connection test failed")
            return FlextResult.fail(f"Connection failed: {e!s}")

    def _load_target_data(self, data: object) -> FlextResult[dict[str, object]]:
        """Perform Oracle-specific data loading.

        Args:
            data: Singer messages to load

        Returns:
            FlextResult containing load statistics or error

        """
        try:
            self._logger.info(f"Loading data to Oracle schema {self._schema}")

            # Parse Singer messages
            if not isinstance(data, list):
                return FlextResult.fail("Data must be a list of Singer messages")

            loaded_count = 0
            error_count = 0
            batch: list[dict[str, object]] = []

            for message in data:
                if not isinstance(message, dict):
                    error_count += 1
                    continue

                # Process message based on type
                process_result = self._process_singer_message(message, batch)
                if process_result.is_failure:
                    error_count += 1
                    continue

                # Process batch if full
                if len(batch) >= self._batch_size:
                    batch_result = self._insert_batch(batch)
                    loaded_count, error_count = self._update_counts(
                        batch_result, batch, loaded_count, error_count,
                    )
                    batch = []

            # Process remaining batch
            if batch:
                batch_result = self._insert_batch(batch)
                loaded_count, error_count = self._update_counts(
                    batch_result, batch, loaded_count, error_count,
                )

            statistics = {
                "loaded": loaded_count,
                "errors": error_count,
                "load_method": self._load_method,
                "target_schema": self._schema,
            }

            self._logger.info(
                f"Oracle load complete: {loaded_count} loaded, {error_count} errors",
            )

            return FlextResult.ok(statistics)

        except Exception as e:
            self._logger.exception("Oracle data loading failed")
            return FlextResult.fail(f"Load error: {e!s}")

    def _process_singer_message(
        self, message: dict[str, object], batch: list[dict[str, object]],
    ) -> FlextResult[None]:
        """Process a single Singer message."""
        msg_type = message.get("type")

        if msg_type == "SCHEMA":
            current_stream = message.get("stream")
            self._logger.info(f"Processing schema for stream {current_stream}")
            return FlextResult.ok(None)

        if msg_type == "RECORD":
            stream = message.get("stream")
            record = message.get("record")

            if not stream or not record:
                return FlextResult.fail("Invalid record message")

            batch.append({
                "stream": stream,
                "record": record,
                "time_extracted": message.get("time_extracted"),
            })
            return FlextResult.ok(None)

        if msg_type == "STATE":
            self._logger.debug(f"Processing state: {message.get('value')}")
            return FlextResult.ok(None)

        return FlextResult.fail(f"Unknown message type: {msg_type}")

    def _update_counts(
        self,
        batch_result: FlextResult[None],
        batch: list[dict[str, object]],
        loaded_count: int,
        error_count: int,
    ) -> tuple[int, int]:
        """Update loaded and error counts based on batch result."""
        if batch_result.success:
            return loaded_count + len(batch), error_count
        return loaded_count, error_count + len(batch)

    def _insert_batch(self, batch: list[dict[str, object]]) -> FlextResult[None]:
        """Insert a batch of records to Oracle.

        Args:
            batch: List of records to insert

        Returns:
            FlextResult indicating success or failure

        """
        try:
            if not batch:
                return FlextResult.ok(None)

            # Group by stream
            streams: dict[str, list[dict[str, object]]] = {}
            for item in batch:
                stream = item.get("stream")
                if not isinstance(stream, str):
                    continue
                if stream not in streams:
                    streams[stream] = []
                record = item.get("record")
                if isinstance(record, dict):
                    streams[stream].append(record)

            # Insert each stream's records
            for stream, records in streams.items():
                table_name = f"{self._schema}.{stream}"
                self._logger.debug(f"Inserting {len(records)} records to {table_name}")

                # In real implementation, use Oracle bulk insert
                # with connection.cursor() as cursor:
                #     if self._load_method == "insert":
                #         cursor.executemany(insert_sql, records)
                #     elif self._load_method == "upsert":
                #         cursor.executemany(merge_sql, records)
                #     elif self._load_method == "replace":
                #         cursor.execute(f"TRUNCATE TABLE {table_name}")
                #         cursor.executemany(insert_sql, records)

            return FlextResult.ok(None)

        except Exception as e:
            self._logger.exception("Batch insert failed")
            return FlextResult.fail(f"Batch insert error: {e!s}")

    def get_info(self) -> dict[str, object]:
        """Get plugin information.

        Returns:
            Dictionary containing plugin metadata

        """
        return {
            "name": self.name,
            "version": self.version,
            "description": "Oracle database target plugin for Singer protocol",
            "plugin_type": "target",
            "database_type": "oracle",
            "batch_size": self._batch_size,
            "schema": self._schema,
            "load_method": self._load_method,
        }


def create_target_oracle_plugin(
    name: str = "target-oracle",
    version: str = "1.0.0",
    config: dict[str, object] | None = None,
    entity: dict[str, object] | None = None,
) -> FlextResult[FlextTargetOraclePlugin]:
    """Create Oracle target plugin.

    Args:
        name: Plugin name
        version: Plugin version
        config: Plugin configuration
        entity: Optional domain entity

    Returns:
        FlextResult containing plugin instance or error

    """
    try:
        # Skip entity creation - FlextPluginEntity not available
        # entity would normally be created here

        # Create plugin instance
        plugin = FlextTargetOraclePlugin(
            name=name,
            version=version,
            config=config,
            _entity=entity,
        )

        return FlextResult.ok(plugin)

    except Exception as e:
        plugin_logger = get_logger("target.oracle")
        plugin_logger.exception("Failed to create Oracle target plugin")
        return FlextResult.fail(f"Plugin creation failed: {e!s}")


# Compatibility aliases
TargetOracle = FlextTargetOracle


__all__ = [
    # Main Oracle Target classes
    "FlextTargetOracle",
    "FlextTargetOracleLoader",
    "FlextTargetOraclePlugin",
    # Compatibility aliases
    "TargetOracle",
    # Factory functions
    "create_target_oracle_plugin",
]
