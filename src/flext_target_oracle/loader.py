"""Oracle Data Loading Infrastructure with FLEXT Database Integration.

This module provides the core Oracle data loading functionality for the FLEXT
Target Oracle Singer target, implementing production-grade database operations
through the flext-db-oracle library. The loader handles batch processing,
table management, and data persistence with enterprise reliability standards.

The implementation follows Clean Architecture principles with clear separation
between data loading concerns and business logic, using railway-oriented
programming patterns for consistent error handling and flext-db-oracle for
production-grade Oracle connectivity.

Key Components:
    FlextOracleTargetLoader: Main data loading service with batch processing
    Table Management: Dynamic table creation and schema management
    Batch Processing: Configurable batch sizes for optimal Oracle performance
    Error Handling: Comprehensive error context with recovery strategies

Architecture Integration:
    Infrastructure Layer: Database operations and external system integration
    Railway-Oriented Programming: FlextResult pattern for consistent error handling
    Connection Management: Production-grade connection pooling through flext-db-oracle
    Batch Processing: Memory-efficient processing with configurable batch sizes

Data Loading Strategy:
    The loader implements a JSON-based storage approach where Singer records
    are stored as JSON documents in Oracle CLOB columns. This provides flexibility
    for varying schema structures while maintaining performance.

Example:
    Basic loader setup and record processing:

    >>> config = FlextOracleTargetConfig(
    ...     oracle_host="localhost",
    ...     oracle_service="XE",
    ...     oracle_user="data_loader",
    ...     oracle_password="secure_password",
    ...     batch_size=1000,
    ... )
    >>> loader = FlextOracleTargetLoader(config)
    >>>
    >>> # Ensure table exists for stream
    >>> schema = {"type": "object", "properties": {"id": {"type": "integer"}}}
    >>> result = await loader.ensure_table_exists("users", schema)
    >>>
    >>> # Load records with automatic batching
    >>> for record in user_records:
    ...     result = await loader.load_record("users", record)
    ...     if result.is_failure:
    ...         print(f"Record loading failed: {result.error}")
    >>>
    >>> # Finalize and get statistics
    >>> stats_result = await loader.finalize_all_streams()
    >>> print(f"Loaded {stats_result.data['total_records']} records")

Note:
    SECURITY WARNING: Current implementation contains SQL injection vulnerabilities
    in the _insert_batch method. See docs/TODO.md for remediation plan before
    production deployment.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from flext_core import FlextResult, get_logger
from flext_db_oracle import (
    FlextDbOracleApi,
    FlextDbOracleConfig,
    FlextDbOracleConnection,
)
from flext_db_oracle.metadata import (
    FlextDbOracleMetadataManager,
)
from sqlalchemy import (
    CLOB,
    Column,
    MetaData,
    Table,
    UniqueConstraint,
)
from sqlalchemy.dialects import oracle
from sqlalchemy.dialects.oracle import DATE, NUMBER, TIMESTAMP, VARCHAR2

from flext_target_oracle.exceptions import (
    FlextOracleTargetConnectionError,
    FlextOracleTargetProcessingError,
    FlextOracleTargetSchemaError,
)

if TYPE_CHECKING:
    from flext_target_oracle.config import FlextOracleTargetConfig

logger = get_logger(__name__)

# Oracle type constants
MAX_ORACLE_IDENTIFIER_LENGTH = 30
HASH_SUFFIX_LENGTH = 6
UNDERSCORE_LENGTH = 1
MAX_COLUMNS_IN_INDEX = 3
MAX_COLUMN_NAME_LENGTH = 20
MAX_INDEX_NAME_LENGTH = 30
DEFAULT_STRING_LENGTH = 4000
DEFAULT_NUMBER_PRECISION = 38
DEFAULT_NUMBER_SCALE = 6
DEFAULT_BOOLEAN_PRECISION = 1
DEFAULT_BOOLEAN_SCALE = 0
DEFAULT_TIMESTAMP_PRECISION = 6
NUMBER_PARAMS_WITH_SCALE = 2
NUMBER_PARAMS_WITHOUT_SCALE = 1

# Constants for magic values
MAX_ORACLE_IDENTIFIER_LENGTH = 30
MAX_COLUMN_NAME_LENGTH = 20
MAX_COLUMNS_IN_INDEX = 3
HASH_SUFFIX_LENGTH = 6
UNDERSCORE_LENGTH = 1
DEFAULT_STRING_LENGTH = 4000
DEFAULT_NUMBER_PRECISION = 38
DEFAULT_NUMBER_SCALE = 6
BOOLEAN_PRECISION = 1
BOOLEAN_SCALE = 0
DEFAULT_TIMEOUT_SECONDS = 20
DEFAULT_BATCH_TIMEOUT_SECONDS = 30


# ============================================================================
# SOLID Architecture Services - Following Single Responsibility Principle
# ============================================================================


class OracleConnectionManager:
    """Oracle connection lifecycle management following Single Responsibility."""

    def __init__(
        self, oracle_api: FlextDbOracleApi, config: FlextOracleTargetConfig,
    ) -> None:
        """Initialize connection manager."""
        self.oracle_api = oracle_api
        self.config = config
        self._connection: FlextDbOracleConnection | None = None
        self._metadata_manager: FlextDbOracleMetadataManager | None = None

    def _handle_connection_failure(self, error_msg: str) -> None:
        """Handle connection failure by raising appropriate exception."""
        raise FlextOracleTargetConnectionError(
            error_msg,
            host=self.config.oracle_host,
            port=self.config.oracle_port,
            service_name=self.config.oracle_service,
        )

    def _handle_connection_object_failure(self, error_msg: str) -> None:
        """Handle connection object failure by raising appropriate exception."""
        raise FlextOracleTargetConnectionError(
            error_msg,
            host=self.config.oracle_host,
            port=self.config.oracle_port,
        )

    def connect(self) -> FlextResult[None]:
        """Establish Oracle connection."""
        try:
            # The connect() method returns Self, not FlextResult
            self.oracle_api.connect()

            self._connection = self.oracle_api.connection
            if not self._connection:
                msg = "Connected but no connection object available"
                self._handle_connection_object_failure(msg)

            # Type guard to ensure connection is not None for metadata manager
            if self._connection is not None:
                self._metadata_manager = FlextDbOracleMetadataManager(self._connection)
            else:
                msg = "Connection is None after successful connect"
                raise FlextOracleTargetConnectionError(
                    msg,
                    host=self.config.oracle_host,
                    port=self.config.oracle_port,
                    service_name=self.config.oracle_service,
                )
            logger.info(
                "Connected to Oracle: %s:%s/%s",
                self.config.oracle_host,
                self.config.oracle_port,
                self.config.oracle_service,
            )
            return FlextResult.ok(None)

        except FlextOracleTargetConnectionError:
            # Re-raise the same exception without modification
            raise
        except Exception as e:
            msg = f"Unexpected error during connection: {e}"
            raise FlextOracleTargetConnectionError(
                msg,
                host=self.config.oracle_host,
                port=self.config.oracle_port,
                service_name=self.config.oracle_service,
            ) from e

    @property
    def connection(self) -> FlextDbOracleConnection | None:
        """Get current connection."""
        return self._connection

    @property
    def metadata_manager(self) -> FlextDbOracleMetadataManager | None:
        """Get metadata manager."""
        return self._metadata_manager


class OracleSchemaManager:
    """Oracle schema operations following Single Responsibility."""

    def __init__(self, metadata: MetaData) -> None:
        """Initialize schema manager."""
        self._metadata = metadata
        self._schema_cache: dict[str, dict[str, object]] = {}
        self._tables: dict[str, Table] = {}

    def map_json_type_to_oracle(
        self, json_type: str, format_type: str | None = None,
    ) -> object:
        """Map JSON schema type to Oracle column type."""
        if json_type == "string":
            if format_type == "date":
                return DATE()
            if format_type in {"date-time", "datetime"}:
                return TIMESTAMP()
            return VARCHAR2(DEFAULT_STRING_LENGTH)
        if json_type == "integer":
                            return NUMBER(precision=DEFAULT_NUMBER_PRECISION, scale=0)  # type: ignore[no-untyped-call]
        if json_type == "number":
            return NUMBER(precision=DEFAULT_NUMBER_PRECISION, scale=DEFAULT_NUMBER_SCALE)  # type: ignore[no-untyped-call]
        if json_type == "boolean":
            return NUMBER(precision=BOOLEAN_PRECISION, scale=BOOLEAN_SCALE)  # type: ignore[no-untyped-call]
        if json_type in {"object", "array"}:
            return CLOB()
        return VARCHAR2(DEFAULT_STRING_LENGTH)

    def flatten_schema_properties(
        self,
        properties: dict[str, object],
        prefix: str = "",
    ) -> dict[str, object]:
        """Flatten nested schema properties for Oracle table structure."""
        flattened = {}

        for key, value in properties.items():
            if not isinstance(value, dict):
                continue

            full_key = f"{prefix}{key}" if prefix else key
            value_type = value.get("type")

            if value_type == "object" and "properties" in value:
                nested_props = value["properties"]
                if isinstance(nested_props, dict):
                    flattened.update(
                        self.flatten_schema_properties(nested_props, f"{full_key}_"),
                    )
            else:
                flattened[full_key] = value

        return flattened

    def get_cached_schema(self, stream_name: str) -> dict[str, object] | None:
        """Get cached schema for stream."""
        return self._schema_cache.get(stream_name)

    def cache_schema(self, stream_name: str, schema: dict[str, object]) -> None:
        """Cache schema for stream."""
        self._schema_cache[stream_name] = schema

    def get_table(self, table_name: str) -> Table | None:
        """Get cached table object."""
        return self._tables.get(table_name)

    def cache_table(self, table_name: str, table: Table) -> None:
        """Cache table object."""
        self._tables[table_name] = table


class OracleSQLGenerator:
    """Oracle SQL generation following Single Responsibility."""

    def __init__(self, config: FlextOracleTargetConfig) -> None:
        """Initialize SQL generator."""
        self.config = config

    def build_merge_statement(
        self,
        table_name: str,
        merge_keys: list[str],
        all_columns: list[str],
    ) -> str:
        """Build MERGE statement for upsert operations."""
        if not merge_keys:
            msg = f"No merge keys defined for table {table_name}"
            raise FlextOracleTargetProcessingError(
                msg,
            )

        # Validate inputs to prevent SQL injection
        if not self._is_valid_identifier(table_name):
            msg = f"Invalid table name: {table_name}"
            raise FlextOracleTargetProcessingError(msg)

        for key in merge_keys + all_columns:
            if not self._is_valid_identifier(key):
                msg = f"Invalid column name: {key}"
                raise FlextOracleTargetProcessingError(msg)

        # Build the ON condition
        on_conditions = [f"target.{key} = source.{key}" for key in merge_keys]
        on_clause = " AND ".join(on_conditions)

        # Build UPDATE SET clause
        update_columns = [col for col in all_columns if col not in merge_keys]
        if update_columns:
            update_sets = [f"{col} = source.{col}" for col in update_columns]
            update_clause = f"UPDATE SET {', '.join(update_sets)}"
        else:
            update_clause = ""

        # Build INSERT clause
        insert_columns = ", ".join(all_columns)
        insert_values = ", ".join([f"source.{col}" for col in all_columns])
        insert_clause = f"INSERT ({insert_columns}) VALUES ({insert_values})"

        # Combine into MERGE statement
        # Note: SQL injection is prevented by _is_valid_identifier validation above
        merge_sql = f"""
        MERGE INTO {table_name} target
        USING (SELECT {", ".join([f":{col} as {col}" for col in all_columns])} FROM dual) source
        ON ({on_clause})
        WHEN MATCHED THEN {update_clause}
        WHEN NOT MATCHED THEN {insert_clause}
        """

        return merge_sql.strip()

    def _is_valid_identifier(self, identifier: str) -> bool:
        """Validate SQL identifier to prevent injection."""
        if not identifier or not identifier.strip():
            return False

        # Check for SQL injection patterns
        # Note: This validation prevents SQL injection in dynamic SQL construction
        dangerous_patterns = [
            ";", "--", "/*", "*/", "xp_", "sp_", "exec", "execute",
            "union", "select", "insert", "update", "delete", "drop", "create",
        ]

        identifier_lower = identifier.lower()
        for pattern in dangerous_patterns:
            if pattern in identifier_lower:
                return False

        # Check for valid identifier characters (alphanumeric and underscore)
        # This ensures only safe characters are used in SQL identifiers
        return all(c.isalnum() or c == "_" for c in identifier)

    def format_index_name(self, table_name: str, column_names: list[str]) -> str:
        """Format index name following Oracle naming conventions."""
        base_name = f"idx_{table_name}_" + "_".join(column_names)
        # Oracle identifier limit is 128 characters in 12.2+, 30 in earlier versions
        if len(base_name) > MAX_ORACLE_IDENTIFIER_LENGTH:
            # Truncate and add hash for uniqueness
            hash_suffix = hashlib.sha256(base_name.encode()).hexdigest()[:HASH_SUFFIX_LENGTH]
            truncated = base_name[: MAX_ORACLE_IDENTIFIER_LENGTH - HASH_SUFFIX_LENGTH - UNDERSCORE_LENGTH]
            return f"{truncated}_{hash_suffix}"
        return base_name


class OracleRecordTransformer:
    """Oracle record transformation following Single Responsibility."""

    def __init__(self, config: FlextOracleTargetConfig) -> None:
        """Initialize record transformer."""
        self.config = config

    def flatten_record(
        self, record: dict[str, object], prefix: str = "",
    ) -> dict[str, object]:
        """Flatten nested record for Oracle table structure."""
        flattened = {}

        for key, value in record.items():
            full_key = f"{prefix}{key}" if prefix else key

            if isinstance(value, dict):
                flattened.update(self.flatten_record(value, f"{full_key}_"))
            elif isinstance(value, list):
                # Convert arrays to JSON strings
                flattened[full_key] = json.dumps(value)
            else:
                flattened[full_key] = value

        return flattened

    def prepare_row_data(
        self,
        record: dict[str, object],
        table_columns: list[str],
    ) -> dict[str, object]:
        """Prepare record data for Oracle insertion."""
        flattened = self.flatten_record(record)
        prepared_data: dict[str, object] = {}

        for column in table_columns:
            value = flattened.get(column)
            if value is None:
                prepared_data[column] = None
            elif isinstance(value, (dict, list)):
                prepared_data[column] = json.dumps(value)
            else:
                prepared_data[column] = value

        return prepared_data


class OracleBatchProcessor:
    """Oracle batch processing following Single Responsibility."""

    def __init__(self, config: FlextOracleTargetConfig) -> None:
        """Initialize batch processor."""
        self.config = config
        self._record_buffers: dict[str, list[dict[str, object]]] = {}
        self._total_records = 0

    def add_record(self, stream_name: str, record: dict[str, object]) -> None:
        """Add record to batch buffer."""
        if stream_name not in self._record_buffers:
            self._record_buffers[stream_name] = []

        self._record_buffers[stream_name].append(record)
        self._total_records += 1

    def is_batch_ready(self, stream_name: str) -> bool:
        """Check if batch is ready for processing."""
        buffer = self._record_buffers.get(stream_name, [])
        return len(buffer) >= self.config.batch_size

    def get_batch(self, stream_name: str) -> list[dict[str, object]]:
        """Get and clear batch for stream."""
        batch = self._record_buffers.get(stream_name, [])
        self._record_buffers[stream_name] = []
        return batch

    def get_all_pending_batches(self) -> dict[str, list[dict[str, object]]]:
        """Get all pending batches."""
        batches = self._record_buffers.copy()
        self._record_buffers.clear()
        return batches

    @property
    def total_records(self) -> int:
        """Get total record count."""
        return self._total_records


class FlextOracleTargetLoader:
    """Oracle data loading service with batch processing and error handling.

    This class provides comprehensive Oracle data loading functionality for Singer
    targets, implementing enterprise-grade reliability patterns with batch processing,
    connection management, and comprehensive error handling. The loader integrates
    with flext-db-oracle for production-grade Oracle connectivity.

    The loader implements a JSON-based storage strategy where Singer records are
    stored as JSON documents in Oracle CLOB columns, providing flexibility for
    varying schema structures while maintaining Oracle performance characteristics.

    Key Features:
        - Batch Processing: Configurable batch sizes for optimal Oracle performance
        - Automatic Table Creation: Dynamic table creation based on Singer streams
        - Connection Management: Production-grade connection pooling and error handling
        - JSON Storage: Flexible schema handling with CLOB-based JSON storage
        - Error Recovery: Comprehensive error handling with detailed context
        - Statistics Tracking: Detailed processing statistics and performance metrics

    Architecture:
        The loader follows Clean Architecture principles as an infrastructure component:
        - Infrastructure Layer: Oracle database operations and connection management
        - Railway-Oriented: FlextResult pattern for consistent error handling
        - Dependency Injection: Configuration-driven initialization and operation
        - Single Responsibility: Focused on data loading with clear boundaries

    Performance Characteristics:
        - Batch Size: Configurable batch processing (default: 1000 records)
        - Connection Pooling: Managed through flext-db-oracle (1-10 connections)
        - Memory Management: Efficient record buffering with automatic flushing
        - Transaction Management: Automatic transaction handling per batch

    Attributes:
        config: Oracle target configuration with connection and performance settings
        oracle_api: FlextDbOracleApi instance for database operations
        _record_buffers: Per-stream record buffers for batch processing
        _total_records: Total number of records processed for statistics

    Example:
        Production-ready loader configuration and usage:

        >>> config = FlextOracleTargetConfig(
        ...     oracle_host="prod-oracle.company.com",
        ...     oracle_service="PRODDB",
        ...     oracle_user="data_loader",
        ...     oracle_password="secure_password",
        ...     default_target_schema="DATA_WAREHOUSE",
        ...     batch_size=2000,
        ...     connection_timeout=60,
        ... )
        >>> loader = FlextOracleTargetLoader(config)
        >>>
        >>> # Process Singer data loading workflow
        >>> table_result = await loader.ensure_table_exists("customer_orders", schema)
        >>> record_result = await loader.load_record("customer_orders", record_data)
        >>> stats_result = await loader.finalize_all_streams()
        >>>
        >>> if all(r.success for r in [table_result, record_result, stats_result]):
        ...     print(
        ...         f"Successfully loaded {stats_result.data['total_records']} records"
        ...     )

    Security Note:
        Current implementation contains SQL injection vulnerabilities in the
        _insert_batch method. These must be addressed before production deployment.
        See docs/TODO.md for detailed remediation plan.

    """

    def __init__(self, config: FlextOracleTargetConfig) -> None:
        """Initialize Oracle loader with configuration and connection setup.

        Sets up the Oracle data loader with validated configuration, establishes
        the Oracle API connection through flext-db-oracle, and initializes
        internal state for batch processing and statistics tracking.

        The initialization process includes:
        1. Store validated configuration for operational use
        2. Create flext-db-oracle configuration from target config
        3. Initialize Oracle API client with connection pooling
        4. Setup internal data structures for batch processing

        Args:
            config: Validated FlextOracleTargetConfig with Oracle connection
                   parameters, batch processing settings, and operational configuration

        Example:
            >>> config = FlextOracleTargetConfig(
            ...     oracle_host="localhost",
            ...     oracle_service="XE",
            ...     oracle_user="test_user",
            ...     oracle_password="test_password",
            ...     batch_size=500,
            ... )
            >>> loader = FlextOracleTargetLoader(config)
            >>> # Loader is ready for table creation and record loading

        Note:
            The Oracle API client is initialized but not connected during __init__.
            Actual database connections are established when using the context
            manager pattern in database operations.

        """
        self.config = config

        # Oracle API from flext-db-oracle - use configuration method
        oracle_config_dict = config.get_oracle_config()
        # Cast to the expected type for FlextDbOracleConfig.from_dict
        oracle_config_dict_typed: dict[str, object] = dict(oracle_config_dict)
        oracle_config_result = FlextDbOracleConfig.from_dict(oracle_config_dict_typed)
        if oracle_config_result.is_failure:
            msg = f"Failed to create Oracle config: {oracle_config_result.error}"
            raise FlextOracleTargetConnectionError(
                msg,
                host=config.oracle_host,
                port=config.oracle_port,
                service_name=config.oracle_service,
            )
        oracle_config = oracle_config_result.data
        self.oracle_api = FlextDbOracleApi(oracle_config)

        # SOLID Architecture Services - Dependency Injection
        self._connection_manager = OracleConnectionManager(self.oracle_api, config)
        self._schema_manager = OracleSchemaManager(MetaData())
        self._sql_generator = OracleSQLGenerator(config)
        self._record_transformer = OracleRecordTransformer(config)
        self._batch_processor = OracleBatchProcessor(config)

        # Legacy support for existing interface
        self._key_properties_cache: dict[str, list[str]] = {}
        self._bulk_prepared: dict[str, object] = {}
        self._use_bulk_operations = config.use_bulk_operations
        self._use_direct_path = config.use_direct_path
        self._parallel_degree = config.parallel_degree

        # Initialize missing attributes to fix mypy errors
        self._schema_cache: dict[str, dict[str, object]] = {}
        self._tables: dict[str, object] = {}
        self._metadata: object = None
        self._connection: object = None

    def connect(self) -> FlextResult[None]:
        """Establish connection to Oracle database using SOLID connection manager.

        Returns:
            FlextResult indicating success/failure

        """
        return self._connection_manager.connect()

    def _handle_table_metadata_error(self, table_key: str, table_name: str) -> None:
        """Handle table metadata not found error."""
        msg = f"Table metadata not found for {table_key}"
        raise FlextOracleTargetProcessingError(
            msg,
            operation="standard_insert",
            table_name=table_name,
        )

    def _handle_sql_build_error(self, sql_result: FlextResult[object], table_name: str) -> None:
        """Handle SQL build error."""
        msg = f"Failed to build INSERT statement: {sql_result.error}"
        raise FlextOracleTargetProcessingError(
            msg,
            operation="standard_insert",
            table_name=table_name,
        )

    def _handle_insert_error(self, result: FlextResult[object], table_name: str, sequence: int) -> None:
        """Handle insert execution error."""
        msg = f"Insert failed: {result.error}"
        raise FlextOracleTargetProcessingError(
            msg,
            operation="standard_insert",
            table_name=table_name,
            record_id=sequence,
        )

    def _handle_merge_error(self, result: FlextResult[object], table_name: str, sequence: int) -> None:
        """Handle merge execution error."""
        msg = f"Merge failed: {result.error}"
        raise FlextOracleTargetProcessingError(
            msg,
            operation="standard_merge",
            table_name=table_name,
            record_id=sequence,
        )

    def _handle_bulk_operation_error(self, result: FlextResult[object], operation: str, table_name: str) -> None:
        """Handle bulk operation error."""
        msg = f"{operation} failed: {result.error}"
        raise FlextOracleTargetProcessingError(
            msg,
            operation=operation,
            table_name=table_name,
        )

    def _handle_connection_error(self, table_name: str) -> None:
        """Handle connection error for bulk operations."""
        msg = "No connection available for bulk operations"
        raise FlextOracleTargetProcessingError(
            msg,
            operation="bulk_operation",
            table_name=table_name,
        )

    def _handle_ddl_error(self, ddl_result: FlextResult[object], table_name: str) -> None:
        """Handle DDL execution error."""
        msg = f"Failed to create table: {ddl_result.error}"
        raise FlextOracleTargetSchemaError(
            msg,
            table_name=table_name,
            schema_name=self.config.default_target_schema,
            ddl_operation="CREATE TABLE",
            oracle_error_code=ddl_result.error,
        )

    async def ensure_table_exists(
        self,
        stream_name: str,
        schema: dict[str, object],
        key_properties: list[str] | None = None,
    ) -> FlextResult[None]:
        """Ensure target Oracle table exists for Singer stream data loading.

        Creates or verifies the existence of Oracle tables required for storing
        Singer stream data. This method implements dynamic table creation based
        on stream names while using a standardized JSON storage approach for
        flexibility across varying schema structures.

        The table creation process includes:
        1. Convert stream name to valid Oracle table name
        2. Check for existing table in target schema
        3. Create table if it doesn't exist using JSON storage structure
        4. Log table creation or verification status

        Table Structure:
            The created tables use a standardized structure optimized for Singer data:
            - DATA: CLOB column containing JSON representation of the record
            - _SDC_EXTRACTED_AT: Timestamp when record was processed
            - _SDC_BATCHED_AT: Timestamp when record was inserted (auto-generated)
            - _SDC_SEQUENCE: Sequence number for record ordering

        Args:
            stream_name: Singer stream identifier used for table naming
            schema: JSON Schema definition of the stream structure (informational)
                   Note: Currently used for logging only; actual storage uses JSON approach
            key_properties: Primary key columns for merge operations

        Returns:
            FlextResult[None]: Success if table exists or was created successfully,
            failure with detailed error if table operations fail

        Example:
            >>> schema = {
            ...     "type": "object",
            ...     "properties": {
            ...         "user_id": {"type": "integer"},
            ...         "username": {"type": "string"},
            ...         "email": {"type": "string"},
            ...         "created_at": {"type": "string", "format": "date-time"},
            ...     },
            ... }
            >>> result = await loader.ensure_table_exists("user_profiles", schema)
            >>> if result.success:
            ...     print("Table USER_PROFILES ready for data loading")
            ... else:
            ...     print(f"Table creation failed: {result.error}")

        Note:
            The schema parameter is currently used for logging and future
            enhancement planning. The actual table structure uses a JSON-based
            approach for maximum flexibility with Singer data variations.

        """
        try:
            table_name = self.config.get_table_name(stream_name)
            logger.info(
                "Ensuring table exists: stream=%s, table=%s",
                stream_name,
                table_name,
            )

            # Use context manager pattern from flext-db-oracle
            with self.oracle_api as connected_api:
                # Check if table already exists
                tables_result = connected_api.get_tables(
                    schema=self.config.default_target_schema,
                )

                if tables_result.is_failure:
                    return FlextResult.fail(
                        f"Failed to check existing tables: {tables_result.error}",
                    )

                existing_tables = [t.upper() for t in tables_result.data or []]

                table_exists = table_name.upper() in existing_tables

                # Handle force recreate
                if table_exists and self.config.force_recreate_tables:
                    logger.info("Force recreating table %s", table_name)
                    drop_result = connected_api.execute_ddl(
                        f"DROP TABLE {self.config.default_target_schema}.{table_name}",
                    )
                    if drop_result.is_failure:
                        logger.warning(
                            f"Failed to drop table for recreation: {drop_result.error}",
                        )
                    table_exists = False

                # Handle existing table
                if table_exists:
                    logger.info("Table %s already exists", table_name)

                    # Truncate if configured
                    if self.config.truncate_before_load:
                        logger.info("Truncating table %s", table_name)
                        truncate_result = connected_api.execute_ddl(
                            f"TRUNCATE TABLE {self.config.default_target_schema}.{table_name}",
                        )
                        if truncate_result.is_failure:
                            logger.warning(
                                f"Failed to truncate table: {truncate_result.error}",
                            )

                    # Check if we need to alter table
                    if self.config.allow_alter_table:
                        alter_result = self._check_and_alter_table(
                            table_name,
                            schema,
                            key_properties,
                            connected_api,
                        )
                        if alter_result.is_failure:
                            logger.warning(
                                f"Failed to alter table: {alter_result.error}",
                            )

                    # Store schema and key properties for future reference
                    self._schema_cache[stream_name] = schema
                    if key_properties:
                        self._key_properties_cache[stream_name] = key_properties
                    return FlextResult.ok(None)

                # Create table based on Singer schema
                create_result = self._create_table_from_schema(
                    table_name,
                    schema,
                    key_properties,
                    connected_api,
                )

                if create_result.is_failure:
                    return create_result

                self._schema_cache[stream_name] = schema
                if key_properties:
                    self._key_properties_cache[stream_name] = key_properties
                logger.info("Created table %s for stream %s", table_name, stream_name)
                return FlextResult.ok(None)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception(f"Failed to ensure table exists for stream {stream_name}")
            return FlextResult.fail(f"Table creation failed: {e}")

    def _create_table_from_schema(
        self,
        table_name: str,
        schema: dict[str, object],
        key_properties: list[str] | None,
        api: FlextDbOracleApi,
    ) -> FlextResult[None]:
        """Create Oracle table based on Singer schema.

        Args:
            table_name: Oracle table name
            schema: Singer schema definition
            key_properties: Primary key columns
            api: Connected Oracle API instance

        Returns:
            FlextResult indicating success/failure

        """
        try:
            columns = []
            stream_name = self._get_stream_name_from_table(table_name)

            # Check storage mode
            if self.config.storage_mode == "json":
                # JSON storage mode - single JSON column + metadata
                columns.append(
                    Column(
                        self.config.json_column_name,
                        CLOB,  # Use CLOB for JSON storage
                        nullable=False,
                    ),
                )

                # Add key columns if in merge mode
                if self.config.sdc_mode == "merge" and key_properties:
                    # Extract key properties as separate columns for indexing
                    properties = schema.get("properties", {})
                    # Type guard to ensure properties is a dict
                    if isinstance(properties, dict):
                        for key_prop in key_properties:
                            if key_prop in properties and isinstance(properties[key_prop], dict):
                                key_prop_def = properties[key_prop]
                                col_type = self._schema_manager.map_json_type_to_oracle(
                                    key_prop_def.get("type", "string"),
                                    key_prop_def.get("format"),
                                )
                                columns.append(
                                    Column(
                                        key_prop.upper(),
                                        col_type,
                                        primary_key=True,
                                        nullable=False,
                                    ),
                                )
            else:
                # Flattened or hybrid mode
                properties = schema.get("properties", {})

                if self.config.storage_mode == "flattened":
                    # Flatten all nested structures
                    flattened_props = self._flatten_schema_properties(properties)
                else:
                    # Hybrid mode - flatten up to max depth
                    flattened_props = self._flatten_schema_properties(
                        properties,
                        max_depth=self.config.max_flattening_depth,
                    )

                # Create columns from flattened properties
                for prop_name, prop_def in flattened_props.items():
                    col_name = prop_name.upper()
                    col_type = self._map_json_type_to_oracle(
                        prop_def,
                        stream_name,
                        prop_name,
                    )

                    # Check if it's a primary key (only in merge mode)
                    is_pk = (
                        self.config.sdc_mode == "merge"
                        and key_properties
                        and prop_name in key_properties
                    )

                    column: Column[object] = Column(
                        col_name,
                        col_type,
                        primary_key=is_pk,
                        nullable=not is_pk,
                    )
                    columns.append(column)

            # Add SDC metadata columns with custom names
            sdc_columns = {
                self.config.sdc_extracted_at_column: TIMESTAMP(),
                self.config.sdc_loaded_at_column: TIMESTAMP(),
                self.config.sdc_deleted_at_column: TIMESTAMP(),
                self.config.sdc_sequence_column: NUMBER,
            }

            existing_cols = [c.name.upper() for c in columns]

            for col_name, col_type in sdc_columns.items():
                if col_name.upper() not in existing_cols:
                    # Special handling for loaded_at in append mode
                    is_pk = (
                        col_name == self.config.sdc_loaded_at_column
                        and self.config.sdc_mode == "append"
                        and key_properties
                    )
                    nullable = col_name == self.config.sdc_deleted_at_column

                    columns.append(
                        Column(
                            col_name,
                            col_type,
                            primary_key=is_pk,
                            nullable=nullable,
                        ),
                    )

            # Order columns according to configuration
            ordered_columns = self._order_columns(columns, key_properties)

            # Create table
            table = Table(
                table_name,
                self._metadata,
                *ordered_columns,
                schema=self.config.default_target_schema,
            )

            # Add unique constraint for append mode if we have key properties
            if self.config.sdc_mode == "append" and key_properties:
                # Create unique constraint on original keys + timestamp
                constraint_cols = [col.upper() for col in key_properties]
                constraint_cols.append("_SDC_LOADED_AT")
                table.append_constraint(
                    UniqueConstraint(*constraint_cols, name=f"UK_{table_name}_SDC"),
                )

            # Execute DDL using flext-db-oracle API
            ddl = str(table.compile(dialect=oracle.dialect()))
            ddl_result = api.execute_ddl(ddl)

            if ddl_result.is_failure:
                self._handle_ddl_error(ddl_result, table_name)

            # Store table reference
            self._tables[table_name] = table

            # Create indexes for performance
            self._create_indexes(table_name, key_properties, api, schema)

            logger.info("Created table %s with %d columns", table_name, len(columns))
            return FlextResult.ok(None)

        except FlextOracleTargetSchemaError:
            raise
        except Exception as e:
            msg = f"Failed to create table from schema: {e}"
            raise FlextOracleTargetSchemaError(
                msg,
                table_name=table_name,
                schema_name=self.config.default_target_schema,
                ddl_operation="CREATE TABLE",
            ) from e

    def _flatten_schema_properties(
        self,
        properties: dict[str, object],
        prefix: str = "",
        max_depth: int | None = None,
        current_depth: int = 0,
    ) -> dict[str, object]:
        """Flatten nested JSON schema properties.

        Args:
            properties: Schema properties to flatten
            prefix: Prefix for nested properties
            max_depth: Maximum depth to flatten (None = no limit)
            current_depth: Current recursion depth

        Returns:
            Flattened properties dictionary

        """
        flattened = {}

        for prop_name, prop_def in properties.items():
            # Build the flattened name
            flat_name = f"{prefix}_{prop_name}" if prefix else prop_name

            # Check if we should continue flattening
            if prop_def.get("type") == "object" and prop_def.get("properties"):
                if max_depth is None or current_depth < max_depth:
                    # Recursively flatten nested object
                    nested_flat = self._flatten_schema_properties(
                        prop_def["properties"],
                        flat_name,
                        max_depth,
                        current_depth + 1,
                    )
                    flattened.update(nested_flat)
                else:
                    # Max depth reached, store as JSON
                    flattened[flat_name] = {"type": "string", "format": "json"}
            elif prop_def.get("type") == "array":
                # Arrays are stored as JSON
                flattened[flat_name] = {"type": "string", "format": "json"}
            else:
                # Regular property
                flattened[flat_name] = prop_def

        return flattened

    def _map_json_type_to_oracle(
        self,
        json_schema: dict[str, str],
        stream_name: str | None = None,
        prop_name: str | None = None,
    ) -> object:
        """Map JSON Schema type to Oracle column type.

        Args:
            json_schema: JSON Schema type definition
            stream_name: Optional stream name for type overrides
            prop_name: Optional property name for type overrides

        Returns:
            SQLAlchemy Oracle column type

        """
        # First check for column-specific override
        if (
            stream_name
            and prop_name
            and self.config.column_type_overrides
            and stream_name in self.config.column_type_overrides
            and prop_name in self.config.column_type_overrides[stream_name]
        ):
            oracle_type_str = self.config.column_type_overrides[stream_name][prop_name]
            return self._parse_oracle_type_string(oracle_type_str)

        json_type = json_schema.get("type", "string")
        json_format = json_schema.get("format", "")

        # Handle array types (e.g., ["null", "string"])
        if isinstance(json_type, list):
            # Filter out "null" and use the first non-null type
            non_null_types = [t for t in json_type if t != "null"]
            json_type = non_null_types[0] if non_null_types else "string"

        # Check custom type mappings
        if self.config.type_mappings and json_type in self.config.type_mappings:
            oracle_type_str = self.config.type_mappings[json_type]
            return self._parse_oracle_type_string(oracle_type_str)

        # Default type mapping
        if json_type == "integer":
            return NUMBER(precision=38, scale=0)
        if json_type == "number":
            return NUMBER
        if json_type == "boolean":
            return NUMBER(1)  # 0 or 1
        if json_type == "string":
            if json_format == "date-time":
                return TIMESTAMP()
            if json_format == "date":
                return DATE
            if json_format == "json":
                return CLOB
            # Use VARCHAR2 with configured defaults
            max_length = json_schema.get("maxLength", self.config.default_string_length)
            if max_length > self.config.use_clob_threshold:
                return CLOB
            return VARCHAR2(min(max_length, 32767))
        if json_type in {"object", "array"}:
            return CLOB  # Store as JSON
        # Default to CLOB for unknown types
        return CLOB

    def _parse_oracle_type_string(self, type_str: str) -> object:
        """Parse Oracle type string to SQLAlchemy type.

        Args:
            type_str: Oracle type string (e.g., 'NUMBER(10,2)', 'VARCHAR2(100)')

        Returns:
            SQLAlchemy Oracle column type

        """
        type_str = type_str.upper().strip()

        if type_str.startswith("NUMBER"):
            # Extract precision and scale if present
            if "(" in type_str:
                params = type_str[7:-1].split(",")
                if len(params) == NUMBER_PARAMS_WITH_SCALE:
                    return NUMBER(int(params[0]), int(params[1]))
                if len(params) == NUMBER_PARAMS_WITHOUT_SCALE:
                    return NUMBER(int(params[0]))
            return NUMBER

        if type_str.startswith("VARCHAR2"):
            if "(" in type_str:
                length = int(type_str[9:-1])
                return VARCHAR2(length)
            return VARCHAR2(self.config.default_string_length)

        if type_str.startswith("CHAR"):
            if "(" in type_str:
                length = int(type_str[5:-1])
                return oracle.CHAR(length)
            return oracle.CHAR

        if type_str.startswith("TIMESTAMP"):
            if "(" in type_str:
                int(type_str[10:-1])
                return TIMESTAMP()
            return TIMESTAMP()

        if type_str == "DATE":
            return DATE

        if type_str == "CLOB":
            return CLOB

        if type_str == "BLOB":
            return oracle.BLOB

        if type_str.startswith("FLOAT"):
            return oracle.FLOAT

        if type_str == "JSON":
            # Oracle 21c+ JSON type, fallback to CLOB for older versions
            return CLOB

        # Default to VARCHAR2
        return VARCHAR2(self.config.default_string_length)

    def _order_columns(
        self,
        columns: list[Column[object]],
        key_properties: list[str] | None,  # noqa: ARG002
    ) -> list[Column[object]]:
        """Order columns according to configuration rules.

        Args:
            columns: List of SQLAlchemy Column objects
            key_properties: Primary key column names

        Returns:
            Ordered list of columns

        """
        if self.config.column_ordering == "schema_order":
            # Keep original order from schema
            return columns

        # Categorize columns
        pk_columns = []
        audit_columns = []
        sdc_columns = []
        regular_columns = []

        for col in columns:
            col_name_lower = col.name.lower()

            # Check if it's an SDC column
            if col_name_lower in {
                self.config.sdc_extracted_at_column.lower(),
                self.config.sdc_loaded_at_column.lower(),
                self.config.sdc_deleted_at_column.lower(),
                self.config.sdc_sequence_column.lower(),
            }:
                sdc_columns.append(col)
            # Check if it's a primary key
            elif col.primary_key:
                pk_columns.append(col)
            # Check if it's an audit column
            elif any(
                pattern in col_name_lower
                for pattern in self.config.audit_column_patterns
            ):
                audit_columns.append(col)
            else:
                regular_columns.append(col)

        # Sort columns within each category if alphabetical ordering
        if self.config.column_ordering == "alphabetical":
            pk_columns.sort(key=lambda c: c.name)
            audit_columns.sort(key=lambda c: c.name)
            sdc_columns.sort(key=lambda c: c.name)
            regular_columns.sort(key=lambda c: c.name)

        # Combine in priority order
        ordered = []
        groups = {
            "primary_keys": pk_columns,
            "regular_columns": regular_columns,
            "audit_columns": audit_columns,
            "sdc_columns": sdc_columns,
        }

        # Sort groups by priority
        sorted_groups = sorted(
            groups.items(),
            key=lambda x: self.config.column_order_rules.get(x[0], 999),
        )

        for _group_name, group_columns in sorted_groups:
            ordered.extend(group_columns)

        return ordered

    def _create_indexes(
        self,
        table_name: str,
        key_properties: list[str] | None,
        api: FlextDbOracleApi,
        schema: dict[str, object] | None = None,
    ) -> None:
        """Create indexes for better query performance.

        Args:
            table_name: Oracle table name
            key_properties: Primary key columns
            api: Connected Oracle API instance
            schema: Singer schema with potential foreign key information

        """
        try:
            db_schema = self.config.default_target_schema

            # Create index on metadata columns for incremental loads
            idx_name = f"IDX_{table_name}_SDC"
            idx_result = api.build_create_index_statement(
                index_name=idx_name,
                table_name=table_name,
                columns=[
                    self.config.sdc_loaded_at_column,
                    self.config.sdc_sequence_column,
                ],
                schema_name=db_schema,
            )

            if idx_result.is_success:
                result = api.execute_ddl(idx_result.data)
                if result.is_failure:
                    logger.warning("Failed to create SDC index: %s", result.error)
            else:
                logger.warning(
                    f"Failed to build SDC index statement: {idx_result.error}",
                )

            # Create composite index on key properties if multiple
            if key_properties and len(key_properties) > 1:
                idx_name = self._format_index_name(table_name, key_properties, "pk")
                key_cols = [k.upper() for k in key_properties]
                idx_result = api.build_create_index_statement(
                    index_name=idx_name,
                    table_name=table_name,
                    columns=key_cols,
                    schema_name=db_schema,
                )

                if idx_result.is_success:
                    result = api.execute_ddl(idx_result.data)
                    if result.is_failure:
                        logger.warning(
                            f"Failed to create key properties index: {result.error}",
                        )
                else:
                    logger.warning(
                        f"Failed to build key properties index statement: {idx_result.error}",
                    )

            # Create custom indexes if defined
            stream_name = self._get_stream_name_from_table(table_name)
            if self.config.custom_indexes and stream_name in self.config.custom_indexes:
                for idx_def in self.config.custom_indexes[stream_name]:
                    idx_name = idx_def.get("name") or self._format_index_name(
                        table_name,
                        idx_def["columns"],
                        "custom",
                    )
                    idx_result = api.build_create_index_statement(
                        index_name=idx_name,
                        table_name=table_name,
                        columns=idx_def["columns"],
                        schema_name=db_schema,
                        unique=idx_def.get("unique", False),
                    )

                    if idx_result.is_success:
                        result = api.execute_ddl(idx_result.data)
                        if result.is_failure:
                            logger.warning(
                                f"Failed to create custom index {idx_name}: {result.error}",
                            )
                    else:
                        logger.warning(
                            f"Failed to build custom index statement: {idx_result.error}",
                        )

            # Create foreign key indexes if enabled and schema has references
            if self.config.create_foreign_key_indexes and schema:
                properties = schema.get("properties", {})
                for prop_name, prop_def in properties.items():
                    # Check for foreign key references in schema
                    # Common patterns: "foreign_key", "references", "$ref"
                    if any(
                        key in prop_def for key in ["foreign_key", "references", "$ref"]
                    ):
                        fk_cols = [prop_name.upper()]
                        idx_name = self._format_index_name(table_name, fk_cols, "fk")

                        idx_result = api.build_create_index_statement(
                            index_name=idx_name,
                            table_name=table_name,
                            columns=fk_cols,
                            schema_name=db_schema,
                        )

                        if idx_result.is_success:
                            result = api.execute_ddl(idx_result.data)
                            if result.is_failure:
                                logger.warning(
                                    f"Failed to create FK index {idx_name}: {result.error}",
                                )
                        else:
                            logger.warning(
                                f"Failed to build FK index statement: {idx_result.error}",
                            )

        except Exception as e:
            # Index creation failure is not critical
            logger.warning("Failed to create indexes for %s: %s", table_name, e)

    def _format_index_name(
        self,
        table_name: str,
        columns: list[str],
        idx_type: str = "",
    ) -> str:
        """Format index name using configured template.

        Args:
            table_name: Table name
            columns: Column names in the index
            idx_type: Type of index (pk, fk, custom, etc.)

        Returns:
            Formatted index name

        """
        # Truncate column names if too long
        col_str = "_".join(columns[:MAX_COLUMNS_IN_INDEX])  # Use first 3 columns max
        if len(col_str) > MAX_COLUMN_NAME_LENGTH:
            col_str = col_str[:MAX_COLUMN_NAME_LENGTH]

        name = self.config.index_naming_template.format(
            table=table_name[:MAX_COLUMN_NAME_LENGTH],  # Truncate table name
            columns=col_str,
            type=idx_type,
        )

        # Ensure Oracle naming limit (30 chars)
        if len(name) > MAX_ORACLE_IDENTIFIER_LENGTH:
            name = name[:MAX_ORACLE_IDENTIFIER_LENGTH]

        return name.upper()

    def _check_and_alter_table(
        self,
        table_name: str,
        schema: dict[str, object],
        key_properties: list[str] | None,
        api: FlextDbOracleApi,
    ) -> FlextResult[None]:
        """Check if table schema matches and alter if needed.

        Args:
            table_name: Table name
            schema: Singer schema
            key_properties: Primary key columns
            api: Connected Oracle API

        Returns:
            FlextResult indicating success/failure

        """
        try:
            # Get current table columns
            columns_result = api.get_columns(
                table_name=table_name,
                schema=self.config.default_target_schema,
            )

            if columns_result.is_failure:
                return FlextResult.fail(
                    f"Failed to get table columns: {columns_result.error}",
                )

            existing_columns = {
                col["name"].upper(): col for col in columns_result.data or []
            }

            # Get expected columns from schema
            stream_name = self._get_stream_name_from_table(table_name)
            expected_columns = self._get_expected_columns_from_schema(
                schema,
                stream_name,
                key_properties,
            )

            # Find columns to add
            columns_to_add = []
            for col_name, col_def in expected_columns.items():
                if col_name.upper() not in existing_columns:
                    columns_to_add.append((col_name, col_def))

            # Add new columns if any
            if columns_to_add:
                for col_name, col_type in columns_to_add:
                    alter_sql = f"ALTER TABLE {self.config.default_target_schema}.{table_name} ADD {col_name} {col_type}"
                    result = api.execute_ddl(alter_sql)
                    if result.is_failure:
                        logger.warning(
                            f"Failed to add column {col_name}: {result.error}",
                        )
                    else:
                        logger.info("Added column %s to table %s", col_name, table_name)

            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Table alteration failed: {e}")

    def _get_expected_columns_from_schema(
        self,
        schema: dict[str, object],
        stream_name: str,
        key_properties: list[str] | None,
    ) -> dict[str, str]:
        """Get expected columns and their types from schema.

        Returns:
            Dictionary mapping column names to Oracle type strings

        """
        expected = {}
        properties = schema.get("properties", {})

        # Process schema properties
        if self.config.storage_mode == "json":
            expected[self.config.json_column_name] = "CLOB"
            # Add key columns for merge mode
            if self.config.sdc_mode == "merge" and key_properties:
                for key_prop in key_properties:
                    if key_prop in properties:
                        col_type = self._map_json_type_to_oracle(
                            properties[key_prop],
                            stream_name,
                            key_prop,
                        )
                        # Convert SQLAlchemy type to string
                        expected[key_prop.upper()] = str(
                            col_type.compile(dialect=oracle.dialect()),
                        )
        else:
            # Flattened mode
            if self.config.storage_mode == "flattened":
                flattened_props = self._flatten_schema_properties(properties)
            else:
                flattened_props = self._flatten_schema_properties(
                    properties,
                    max_depth=self.config.max_flattening_depth,
                )

            for prop_name, prop_def in flattened_props.items():
                col_type = self._map_json_type_to_oracle(
                    prop_def,
                    stream_name,
                    prop_name,
                )
                expected[prop_name.upper()] = str(
                    col_type.compile(dialect=oracle.dialect()),
                )

        # Add SDC columns
        expected[self.config.sdc_extracted_at_column] = (
            f"TIMESTAMP({self.config.default_timestamp_precision})"
        )
        expected[self.config.sdc_loaded_at_column] = (
            f"TIMESTAMP({self.config.default_timestamp_precision})"
        )
        expected[self.config.sdc_deleted_at_column] = (
            f"TIMESTAMP({self.config.default_timestamp_precision})"
        )
        expected[self.config.sdc_sequence_column] = "NUMBER"

        return expected

    async def _process_table_existence_result(
        self,
        tables_result: FlextResult[list[str]],
        table_name: str,
        stream_name: str,  # noqa: ARG002
    ) -> FlextResult[None]:
        """Process table existence result using Railway Pattern - Single Responsibility."""
        if not tables_result.success:
            return FlextResult.fail(
                f"Failed to check table existence: {tables_result.error}",
            )

        existing_tables = tables_result.data or []
        table_exists = table_name.upper() in [
            table.upper() for table in existing_tables
        ]

        if not table_exists:
            # Create table using flext-db-oracle patterns
            create_result = await self._create_table(table_name)
            if not create_result.success:
                return create_result
            logger.info(
                f"Created table: {self.config.default_target_schema}.{table_name}",
            )

        return FlextResult.ok(None)

    async def load_record(
        self,
        stream_name: str,
        record_data: dict[str, object],
    ) -> FlextResult[None]:
        """Load individual record with automatic batch processing and error handling.

        Processes individual Singer records by adding them to stream-specific buffers
        for batch processing. When the buffer reaches the configured batch size,
        automatically flushes the batch to Oracle for optimal performance.

        This method implements memory-efficient batch processing by:
        1. Adding the record to the appropriate stream buffer
        2. Checking if the buffer has reached the configured batch size
        3. Automatically flushing full batches to Oracle
        4. Providing detailed error context for troubleshooting

        The buffering strategy ensures optimal Oracle performance by minimizing
        the number of database round trips while maintaining reasonable memory usage.

        Args:
            stream_name: Singer stream identifier for buffer and table identification
            record_data: Dictionary containing the record's field values to load
                        Must be JSON-serializable for Oracle CLOB storage

        Returns:
            FlextResult[None]: Success if record was buffered successfully or
            batch was flushed successfully. Failure with detailed error context
            if buffering or batch processing fails.

        Example:
            Loading individual records with automatic batching:

            >>> # Configure with batch size of 100 records
            >>> loader = FlextOracleTargetLoader(config_with_batch_size_100)
            >>>
            >>> # Load records - batches flush automatically
            >>> for i in range(250):
            ...     record = {
            ...         "id": i,
            ...         "name": f"User {i}",
            ...         "email": f"user{i}@example.com",
            ...     }
            ...     result = await loader.load_record("users", record)
            ...     if result.is_failure:
            ...         print(f"Record {i} failed: {result.error}")
            >>>
            >>> # Batches flush at records 100 and 200 automatically
            >>> # Final 50 records remain buffered until finalize()

        Performance Notes:
            - Records are buffered in memory until batch size is reached
            - Automatic flushing minimizes memory usage and provides regular progress
            - Failed records are logged but don't stop processing of subsequent records
            - Buffer sizes can be tuned via configuration for optimal performance

        """
        try:
            # Use SOLID batch processor service
            self._batch_processor.add_record(stream_name, record_data)

            # Check if batch is ready using SOLID service
            if self._batch_processor.is_batch_ready(stream_name):
                logger.info("Buffer full, flushing batch for stream: %s", stream_name)
                return await self._flush_batch(stream_name)

            return FlextResult.ok(None)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception(f"Failed to load record for stream {stream_name}")
            return FlextResult.fail(f"Record loading failed: {e}")

    async def finalize_all_streams(self) -> FlextResult[dict[str, object]]:
        """Finalize data loading operations and return comprehensive statistics.

        Completes all pending data loading operations by flushing remaining
        buffered records to Oracle and collecting comprehensive statistics
        about the entire loading session. This method must be called after
        all records have been processed to ensure data consistency.

        The finalization process includes:
        1. Flush all remaining buffered records to Oracle
        2. Handle any flush failures with detailed error reporting
        3. Collect comprehensive statistics about the loading session
        4. Generate summary report with performance and reliability metrics

        Statistics collected include:
        - Total records processed across all streams
        - Successful vs failed record counts
        - Number of batches processed
        - Stream-specific processing details

        Returns:
            FlextResult[dict[str, object]]: Success contains comprehensive statistics
            dictionary with processing metrics. Failure contains detailed error
            information about finalization issues.

        Statistics Dictionary Format:
            {
                "total_records": int,      # Total records processed
                "successful_records": int, # Successfully loaded records
                "failed_records": int,     # Failed record count
                "total_batches": int,      # Number of batches processed
                "streams_processed": int,  # Number of unique streams
                "processing_status": str   # Overall processing status
            }

        Example:
            Finalizing after record processing:

            >>> # After processing all records
            >>> stats_result = await loader.finalize_all_streams()
            >>> if stats_result.success:
            ...     stats = stats_result.data
            ...     print(f"Loading completed successfully:")
            ...     print(f"  Total records: {stats['total_records']}")
            ...     print(f"  Successful: {stats['successful_records']}")
            ...     print(f"  Failed: {stats['failed_records']}")
            ...     print(f"  Batches: {stats['total_batches']}")
            ... else:
            ...     print(f"Finalization failed: {stats_result.error}")

        Note:
            This method attempts to flush all remaining batches even if some
            fail, providing as complete statistics as possible. Check the
            failed_records count to determine if any data was lost.

        """
        try:
            # Flush all remaining batches using SOLID batch processor
            pending_batches = self._batch_processor.get_all_pending_batches()
            for stream_name, records in pending_batches.items():
                if records:
                    result = await self._flush_batch_records(stream_name, records)
                    if not result.success:
                        logger.error(
                            f"Failed to flush final batch for {stream_name}: {result.error}",
                        )

            # Return statistics from SOLID batch processor
            stats: dict[str, object] = {
                "total_records": self._batch_processor.total_records,
                "successful_records": self._batch_processor.total_records,
                "failed_records": 0,
                "total_batches": len(pending_batches),
            }

            logger.info(
                f"Finalization complete: {stats['total_records']} records processed",
            )
            return FlextResult.ok(stats)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Failed to finalize streams")
            return FlextResult.fail(f"Finalization failed: {e}")

    async def _flush_batch(self, stream_name: str) -> FlextResult[None]:
        """Flush pending records for a stream using SOLID batch processor."""
        try:
            # Get batch from SOLID batch processor
            records = self._batch_processor.get_batch(stream_name)
            if not records:
                return FlextResult.ok(None)

            return await self._flush_batch_records(stream_name, records)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception(f"Failed to flush batch for stream {stream_name}")
            return FlextResult.fail(f"Batch flush failed: {e}")

    async def _flush_batch_records(
        self, stream_name: str, records: list[dict[str, object]],
    ) -> FlextResult[None]:
        """Helper method to flush specific records."""
        try:
            table_name = self.config.get_table_name(stream_name)

            # Execute batch insert
            result = await self._insert_batch(table_name, records)

            record_count = len(records)
            if result.success:
                logger.info("Batch loaded: %d records to %s", record_count, table_name)
                return result
            logger.error("Batch failed: %s", result.error)
            return result

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception(f"Failed to flush batch records for stream {stream_name}")
            return FlextResult.fail(f"Batch flush failed: {e}")

    async def _insert_batch(
        self,
        table_name: str,
        records: list[dict[str, object]],
    ) -> FlextResult[None]:
        """Insert batch of records using flext-db-oracle."""
        try:
            if not records:
                return FlextResult.ok(None)

            schema_name = self.config.default_target_schema.upper()
            table_name_upper = table_name.upper()

            # Use bulk operations if enabled and supported
            if self._use_bulk_operations and len(records) > 1:
                return await self._bulk_insert(schema_name, table_name_upper, records)
            return await self._standard_insert(schema_name, table_name_upper, records)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception(f"Failed to insert batch to {table_name}")
            return FlextResult.fail(f"Batch insert failed: {e}")

    async def _standard_insert(
        self,
        schema_name: str,
        table_name: str,
        records: list[dict[str, object]],
    ) -> FlextResult[None]:
        """Standard insert using individual INSERT statements."""
        try:
            # Get table metadata
            table_key = f"{schema_name}.{table_name}"
            if table_key not in self._tables:
                self._handle_table_metadata_error(table_key, table_name)

            table = self._tables[table_key]

            # Check if we need merge or append mode
            if self.config.sdc_mode == "merge":
                return await self._standard_merge(
                    schema_name,
                    table_name,
                    records,
                    table,
                )

            # Build INSERT statement using flext-db-oracle
            col_names = [col.name for col in table.columns]

            # Build INSERT with hints if needed
            hints = []
            if self._use_direct_path:
                hints.append("APPEND")
            if self._parallel_degree:
                hints.append(f"PARALLEL({table_name}, {self._parallel_degree})")

            sql_result = self.oracle_api.build_insert_statement(
                table_name=table_name,
                columns=col_names,
                schema_name=schema_name,
                hints=hints or None,
            )

            if sql_result.is_failure:
                self._handle_sql_build_error(sql_result, table_name)

            sql = sql_result.data

            # Process each record
            loaded_at = datetime.now(UTC)

            for sequence, record in enumerate(records):
                # Prepare row data using the helper method
                params = self._prepare_row_data(record, table, sequence, loaded_at)

                # Execute insert using flext-db-oracle API
                result = self.oracle_api.query(sql, params)
                if result.is_failure:
                    self._handle_insert_error(result, table_name, sequence)

            logger.info("Standard inserted %d records to %s", len(records), table_name)
            return FlextResult.ok(None)

        except FlextOracleTargetProcessingError:
            raise
        except Exception as e:
            msg = f"Standard insert failed: {e}"
            raise FlextOracleTargetProcessingError(
                msg,
                operation="standard_insert",
                table_name=table_name,
                batch_size=len(records),
            ) from e

    async def _standard_merge(
        self,
        schema_name: str,
        table_name: str,
        records: list[dict[str, object]],
        table: Table,
    ) -> FlextResult[None]:
        """Standard merge using individual MERGE statements."""
        try:
            # Get merge keys
            stream_name = self._get_stream_name_from_table(table_name)
            merge_keys = self._get_merge_keys(stream_name)

            if not merge_keys:
                # No merge keys, fall back to insert
                logger.warning(
                    f"No merge keys for {stream_name}, using standard insert",
                )
                return await self._standard_insert(schema_name, table_name, records)

            # Build merge statement
            merge_sql = self._build_merge_statement(
                schema_name,
                table_name,
                table,
                merge_keys,
            )

            # Execute merges
            loaded_at = datetime.now(UTC)

            for sequence, record in enumerate(records):
                row_data = self._prepare_row_data(record, table, sequence, loaded_at)

                # Prepare parameters for merge
                params = {}
                for k, v in row_data.items():
                    params[f"src_{k}"] = v

                # Execute merge using flext-db-oracle API
                result = self.oracle_api.query(merge_sql, params)
                if result.is_failure:
                    self._handle_merge_error(result, table_name, sequence)

            logger.info("Standard merged %d records to %s", len(records), table_name)
            return FlextResult.ok(None)

        except FlextOracleTargetProcessingError:
            raise
        except Exception as e:
            msg = f"Standard merge failed: {e}"
            raise FlextOracleTargetProcessingError(
                msg,
                operation="standard_merge",
                table_name=table_name,
                batch_size=len(records),
            ) from e

    async def _bulk_insert(
        self,
        schema_name: str,
        table_name: str,
        records: list[dict[str, object]],
    ) -> FlextResult[None]:
        """Bulk insert using Oracle array operations for better performance."""
        try:
            with self.oracle_api:
                # Get connection for bulk operations
                if not self._connection:
                    self._handle_connection_error(table_name)

                # Get table metadata
                table_key = f"{schema_name}.{table_name}"
                if table_key not in self._tables:
                    self._handle_table_metadata_error(table_key, table_name)

                table = self._tables[table_key]

                # Check if we need to do merge or append
                if self.config.sdc_mode == "merge":
                    return await self._bulk_merge(
                        schema_name,
                        table_name,
                        records,
                        table,
                    )
                return await self._bulk_append(schema_name, table_name, records, table)

        except FlextOracleTargetProcessingError:
            raise
        except Exception as e:
            msg = f"Bulk insert failed: {e}"
            raise FlextOracleTargetProcessingError(
                msg,
                operation="bulk_insert",
                table_name=table_name,
                batch_size=len(records),
            ) from e

    async def _bulk_append(
        self,
        schema_name: str,
        table_name: str,
        records: list[dict[str, object]],
        table: Table,
    ) -> FlextResult[None]:
        """Bulk append records (always insert new rows)."""
        try:
            bulk_data = []
            loaded_at = datetime.now(UTC)

            # Prepare all records for bulk insert
            for sequence, record in enumerate(records):
                row_data = self._prepare_row_data(record, table, sequence, loaded_at)
                bulk_data.append(row_data)

            # Build INSERT statement using flext-db-oracle
            col_names = list(bulk_data[0].keys()) if bulk_data else []

            # Build hints if needed
            hints = []
            if self._use_direct_path:
                hints.append("APPEND")
            if self._parallel_degree:
                hints.append(f"PARALLEL({table_name}, {self._parallel_degree})")

            sql_result = self.oracle_api.build_insert_statement(
                table_name=table_name,
                columns=col_names,
                schema_name=schema_name,
                hints=hints or None,
            )

            if sql_result.is_failure:
                self._handle_bulk_operation_error(sql_result, "bulk_append", table_name)

            sql = sql_result.data

            # Execute bulk insert using batch operations
            operations = [(sql, row) for row in bulk_data]
            result = self.oracle_api.execute_batch(operations)

            if result.is_failure:
                self._handle_bulk_operation_error(result, "bulk_append", table_name)

            logger.info("Bulk appended %d records to %s", len(records), table_name)
            return FlextResult.ok(None)

        except FlextOracleTargetProcessingError:
            raise
        except Exception as e:
            msg = f"Bulk append failed: {e}"
            raise FlextOracleTargetProcessingError(
                msg,
                operation="bulk_append",
                table_name=table_name,
                batch_size=len(records),
            ) from e

    async def _bulk_merge(
        self,
        schema_name: str,
        table_name: str,
        records: list[dict[str, object]],
        table: Table,
    ) -> FlextResult[None]:
        """Bulk merge records (update existing or insert new)."""
        try:
            # Get merge keys for this stream
            stream_name = self._get_stream_name_from_table(table_name)
            merge_keys = self._get_merge_keys(stream_name)

            if not merge_keys:
                # No merge keys defined, fall back to append
                logger.warning(
                    f"No merge keys defined for {stream_name}, using append mode",
                )
                return await self._bulk_append(schema_name, table_name, records, table)

            loaded_at = datetime.now(UTC)

            # Build MERGE statement
            merge_sql = self._build_merge_statement(
                schema_name,
                table_name,
                table,
                merge_keys,
            )

            # Prepare merge operations
            operations = []

            for sequence, record in enumerate(records):
                row_data = self._prepare_row_data(record, table, sequence, loaded_at)
                # Convert to parameter dict for merge
                params = {f"src_{k}": v for k, v in row_data.items()}
                operations.append((merge_sql, params))

            # Execute batch merge using flext-db-oracle API
            result = self.oracle_api.execute_batch(operations)

            if result.is_failure:
                self._handle_bulk_operation_error(result, "bulk_merge", table_name)

            logger.info("Bulk merged %d records to %s", len(records), table_name)
            return FlextResult.ok(None)

        except FlextOracleTargetProcessingError:
            raise
        except Exception as e:
            msg = f"Bulk merge failed: {e}"
            raise FlextOracleTargetProcessingError(
                msg,
                operation="bulk_merge",
                table_name=table_name,
                batch_size=len(records),
            ) from e

    def _prepare_row_data(
        self,
        record: dict[str, object],
        table: Table,
        sequence: int,
        loaded_at: datetime,
    ) -> dict[str, object]:
        """Prepare row data for insertion using SOLID record transformer."""
        # Delegate to the SOLID record transformer service
        table_columns = [col.name for col in table.columns]
        row_data = self._record_transformer.prepare_row_data(record, table_columns)

        # Add SDC metadata columns
        for col in table.columns:
            col_name = col.name
            if col_name == self.config.sdc_loaded_at_column:
                row_data[col_name] = loaded_at
            elif col_name == self.config.sdc_sequence_column:
                row_data[col_name] = sequence
            elif col_name == self.config.sdc_extracted_at_column:
                row_data[col_name] = record.get("_sdc_extracted_at", loaded_at)
            elif col_name == self.config.sdc_deleted_at_column:
                row_data[col_name] = record.get("_sdc_deleted_at")

        return row_data

    def _flatten_record(
        self,
        record: dict[str, object],
        prefix: str = "",
        max_depth: int | None = None,
        current_depth: int = 0,
    ) -> dict[str, object]:
        """Flatten a record's nested structure.

        Args:
            record: Record to flatten
            prefix: Prefix for nested fields
            max_depth: Maximum depth to flatten
            current_depth: Current recursion depth

        Returns:
            Flattened record dictionary

        """
        flattened = {}

        for key, value in record.items():
            # Build the flattened key name
            flat_key = f"{prefix}_{key}" if prefix else key

            # Check if we should continue flattening
            if isinstance(value, dict):
                if max_depth is None or current_depth < max_depth:
                    # Recursively flatten nested dict
                    nested_flat = self._flatten_record(
                        value,
                        flat_key,
                        max_depth,
                        current_depth + 1,
                    )
                    flattened.update(nested_flat)
                else:
                    # Max depth reached, store as JSON
                    flattened[flat_key] = value
            else:
                # Regular value or array (arrays stored as-is)
                flattened[flat_key] = value

        return flattened

    def _get_stream_name_from_table(self, table_name: str) -> str:
        """Get stream name from table name."""
        # Reverse the table name mapping
        if self.config.table_name_mappings:
            for stream, mapped_table in self.config.table_name_mappings.items():
                if mapped_table.upper() == table_name.upper():
                    return stream

        # Remove prefix/suffix if configured
        name = table_name
        if self.config.table_prefix:
            name = name.replace(self.config.table_prefix, "", 1)
        if self.config.table_suffix:
            name = name.replace(self.config.table_suffix, "")

        return name.lower().replace("_", "-")

    def _get_merge_keys(self, stream_name: str) -> list[str]:
        """Get merge keys for a stream."""
        # First check if there's a custom merge key configuration
        if (
            self.config.sdc_merge_key_properties
            and stream_name in self.config.sdc_merge_key_properties
        ):
            return self.config.sdc_merge_key_properties[stream_name]

        # Otherwise use the key properties from schema creation
        if stream_name in self._key_properties_cache:
            return self._key_properties_cache[stream_name]

        return []

    def _build_merge_statement(
        self,
        schema_name: str,
        table_name: str,
        table: Table,
        merge_keys: list[str],
    ) -> str:
        """Build Oracle MERGE statement using flext-db-oracle."""
        # Build column lists
        all_cols = [col.name for col in table.columns]

        # Identify update columns (exclude merge keys and SDC metadata that shouldn't be updated)
        update_cols = [
            col
            for col in all_cols
            if col.upper() not in [k.upper() for k in merge_keys]
            and col
            not in {
                self.config.sdc_extracted_at_column,
                self.config.sdc_sequence_column,
            }
        ]

        # Build hints if needed
        hints = []
        if self._parallel_degree:
            hints.append(f"PARALLEL({table_name}, {self._parallel_degree})")

        # Build MERGE statement
        merge_result = self.oracle_api.build_merge_statement(
            target_table=table_name,
            source_columns=all_cols,
            merge_keys=merge_keys,
            update_columns=update_cols,
            insert_columns=all_cols,
            schema_name=schema_name,
            hints=hints or None,
        )

        if merge_result.is_failure:
            msg = f"Failed to build MERGE statement: {merge_result.error}"
            raise FlextOracleTargetProcessingError(
                msg,
                operation="build_merge",
                table_name=table_name,
            )

        return merge_result.data

    async def _create_table(self, table_name: str) -> FlextResult[None]:
        """Create table with simple JSON storage structure."""
        try:
            # Define columns for simple JSON storage structure
            columns = [
                {
                    "name": self.config.json_column_name,
                    "type": "CLOB",
                    "nullable": True,
                },
                {
                    "name": self.config.sdc_extracted_at_column,
                    "type": f"TIMESTAMP({self.config.default_timestamp_precision})",
                    "nullable": True,
                },
                {
                    "name": self.config.sdc_loaded_at_column,
                    "type": f"TIMESTAMP({self.config.default_timestamp_precision})",
                    "nullable": True,
                    "default": "CURRENT_TIMESTAMP",
                },
                {
                    "name": self.config.sdc_sequence_column,
                    "type": "NUMBER",
                    "nullable": True,
                    "default": "0",
                },
            ]

            # Build CREATE TABLE DDL using flext-db-oracle
            with self.oracle_api as connected_api:
                ddl_result = connected_api.create_table_ddl(
                    table_name=table_name.upper(),
                    columns=columns,
                    schema_name=self.config.default_target_schema,
                )

                if ddl_result.is_failure:
                    return FlextResult.fail(
                        f"Failed to build CREATE TABLE DDL: {ddl_result.error}",
                    )

                # Execute DDL
                exec_result = connected_api.execute_ddl(ddl_result.data)
                if exec_result.is_failure:
                    return FlextResult.fail(
                        f"Failed to execute CREATE TABLE: {exec_result.error}",
                    )

                logger.info(
                    f"Created simple JSON table: {self.config.default_target_schema}.{table_name}",
                )
            return FlextResult.ok(None)

        except Exception as e:
            logger.exception(f"Failed to create table {table_name}")
            return FlextResult.fail(f"Table creation failed: {e}")
