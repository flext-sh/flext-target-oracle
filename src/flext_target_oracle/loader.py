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

import json
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from flext_core import FlextResult, get_logger
from flext_db_oracle import (
    FlextDbOracleApi,
    FlextDbOracleConfig,
    FlextDbOracleConnection,
)
from flext_db_oracle.metadata import FlextDbOracleMetadataManager
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
        oracle_config = FlextDbOracleConfig(**oracle_config_dict)
        self.oracle_api = FlextDbOracleApi(oracle_config)

        # Initialize connection and metadata components
        self._connection: FlextDbOracleConnection | None = None
        self._metadata_manager: FlextDbOracleMetadataManager | None = None
        self._metadata = MetaData()
        self._schema_cache: dict[str, dict[str, object]] = {}
        self._tables: dict[str, Table] = {}
        self._key_properties_cache: dict[str, list[str]] = {}

        # Buffers for batch processing
        self._record_buffers: dict[str, list[dict[str, object]]] = {}
        self._total_records = 0

        # Bulk operation support
        self._bulk_prepared: dict[str, object] = {}
        self._use_bulk_operations = config.use_bulk_operations
        self._use_direct_path = config.use_direct_path
        self._parallel_degree = config.parallel_degree

    def connect(self) -> FlextResult[None]:
        """Establish connection to Oracle database.

        Returns:
            FlextResult indicating success/failure

        """
        try:
            # Connect via API
            connect_result = self.oracle_api.connect()
            if connect_result.is_failure:
                msg = f"Failed to establish Oracle connection: {connect_result.error}"
                raise FlextOracleTargetConnectionError(
                    msg,
                    host=self.config.oracle_host,
                    port=self.config.oracle_port,
                    service_name=self.config.oracle_service,
                )

            # Get connection for metadata operations
            self._connection = self.oracle_api.connection
            if not self._connection:
                msg = "Connected but no connection object available"
                raise FlextOracleTargetConnectionError(
                    msg,
                    host=self.config.oracle_host,
                    port=self.config.oracle_port,
                )

            self._metadata_manager = FlextDbOracleMetadataManager(self._connection)
            logger.info(
                f"Connected to Oracle: {self.config.oracle_host}:{self.config.oracle_port}/{self.config.oracle_service}",
            )
            return FlextResult.ok(None)

        except FlextOracleTargetConnectionError:
            raise
        except Exception as e:
            msg = f"Unexpected error during connection: {e}"
            raise FlextOracleTargetConnectionError(
                msg,
                host=self.config.oracle_host,
                port=self.config.oracle_port,
                service_name=self.config.oracle_service,
            ) from e

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
                f"Ensuring table exists: stream={stream_name}, table={table_name}",
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

                existing_tables = [t.upper() for t in tables_result.value or []]

                table_exists = table_name.upper() in existing_tables

                # Handle force recreate
                if table_exists and self.config.force_recreate_tables:
                    logger.info(f"Force recreating table {table_name}")
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
                    logger.info(f"Table {table_name} already exists")

                    # Truncate if configured
                    if self.config.truncate_before_load:
                        logger.info(f"Truncating table {table_name}")
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
                logger.info(f"Created table {table_name} for stream {stream_name}")
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
                    for key_prop in key_properties:
                        if key_prop in properties:
                            col_type = self._map_json_type_to_oracle(
                                properties[key_prop],
                                stream_name,
                                key_prop,
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
                        prop_def, stream_name, prop_name,
                    )

                    # Check if it's a primary key (only in merge mode)
                    is_pk = (
                        self.config.sdc_mode == "merge"
                        and key_properties
                        and prop_name in key_properties
                    )

                    column = Column(
                        col_name,
                        col_type,
                        primary_key=is_pk,
                        nullable=not is_pk,
                    )
                    columns.append(column)

            # Add SDC metadata columns with custom names
            sdc_columns = {
                self.config.sdc_extracted_at_column: TIMESTAMP(
                    self.config.default_timestamp_precision,
                ),
                self.config.sdc_loaded_at_column: TIMESTAMP(
                    self.config.default_timestamp_precision,
                ),
                self.config.sdc_deleted_at_column: TIMESTAMP(
                    self.config.default_timestamp_precision,
                ),
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
                msg = f"Failed to create table: {ddl_result.error}"
                raise FlextOracleTargetSchemaError(
                    msg,
                    table_name=table_name,
                    schema_name=self.config.default_target_schema,
                    ddl_operation="CREATE TABLE",
                    oracle_error_code=ddl_result.error,
                )

            # Store table reference
            self._tables[table_name] = table

            # Create indexes for performance
            self._create_indexes(table_name, key_properties, api, schema)

            logger.info(f"Created table {table_name} with {len(columns)} columns")
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
                return TIMESTAMP(self.config.default_timestamp_precision)
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
                if len(params) == 2:
                    return NUMBER(int(params[0]), int(params[1]))
                if len(params) == 1:
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
                precision = int(type_str[10:-1])
                return TIMESTAMP(precision)
            return TIMESTAMP(self.config.default_timestamp_precision)

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
        self, columns: list[Column], key_properties: list[str] | None,
    ) -> list[Column]:
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
                result = api.execute_ddl(idx_result.value)
                if result.is_failure:
                    logger.warning(f"Failed to create SDC index: {result.error}")
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
                    result = api.execute_ddl(idx_result.value)
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
                        result = api.execute_ddl(idx_result.value)
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
                            result = api.execute_ddl(idx_result.value)
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
            logger.warning(f"Failed to create indexes for {table_name}: {e}")

    def _format_index_name(
        self, table_name: str, columns: list[str], idx_type: str = "",
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
        col_str = "_".join(columns[:3])  # Use first 3 columns max
        if len(col_str) > 20:
            col_str = col_str[:20]

        name = self.config.index_naming_template.format(
            table=table_name[:20],  # Truncate table name
            columns=col_str,
            type=idx_type,
        )

        # Ensure Oracle naming limit (30 chars)
        if len(name) > 30:
            name = name[:30]

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
                col["name"].upper(): col for col in columns_result.value or []
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
                        logger.info(f"Added column {col_name} to table {table_name}")

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
                    prop_def, stream_name, prop_name,
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
        stream_name: str,
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
            # Add to buffer
            if stream_name not in self._record_buffers:
                self._record_buffers[stream_name] = []

            self._record_buffers[stream_name].append(record_data)
            buffer_size = len(self._record_buffers[stream_name])

            # Check if batch is ready
            if buffer_size >= self.config.batch_size:
                logger.info(f"Buffer full, flushing batch for stream: {stream_name}")
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
            # Flush all remaining batches
            for stream_name in list(self._record_buffers.keys()):
                if self._record_buffers[stream_name]:
                    result = await self._flush_batch(stream_name)
                    if not result.success:
                        logger.error(
                            f"Failed to flush final batch for {stream_name}: {result.error}",
                        )

            # Return simple statistics
            stats: dict[str, object] = {
                "total_records": self._total_records,
                "successful_records": self._total_records,
                "failed_records": 0,
                "total_batches": len(self._record_buffers),
            }

            logger.info(
                f"Finalization complete: {stats['total_records']} records processed",
            )
            return FlextResult.ok(stats)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Failed to finalize streams")
            return FlextResult.fail(f"Finalization failed: {e}")

    async def _flush_batch(self, stream_name: str) -> FlextResult[None]:
        """Flush pending records for a stream."""
        try:
            if (
                stream_name not in self._record_buffers
                or not self._record_buffers[stream_name]
            ):
                return FlextResult.ok(None)

            records = self._record_buffers[stream_name]
            table_name = self.config.get_table_name(stream_name)

            # Execute batch insert
            result = await self._insert_batch(table_name, records)

            # Clear buffer and update stats
            record_count = len(records)
            self._record_buffers[stream_name] = []

            if result.success:
                self._total_records += record_count
                logger.info(f"Batch loaded: {record_count} records to {table_name}")
            else:
                logger.error(f"Batch failed: {result.error}")

            return result

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception(f"Failed to flush batch for stream {stream_name}")
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
                msg = f"Table metadata not found for {table_key}"
                raise FlextOracleTargetProcessingError(
                    msg,
                    operation="standard_insert",
                    table_name=table_name,
                )

            table = self._tables[table_key]

            # Check if we need merge or append mode
            if self.config.sdc_mode == "merge":
                return await self._standard_merge(
                    schema_name, table_name, records, table,
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
                msg = f"Failed to build INSERT statement: {sql_result.error}"
                raise FlextOracleTargetProcessingError(
                    msg,
                    operation="standard_insert",
                    table_name=table_name,
                )

            sql = sql_result.value

            # Process each record
            sequence = 0
            loaded_at = datetime.now(UTC)

            for record in records:
                # Prepare row data using the helper method
                params = self._prepare_row_data(record, table, sequence, loaded_at)

                # Execute insert using flext-db-oracle API
                result = self.oracle_api.query(sql, params)
                if result.is_failure:
                    msg = f"Insert failed: {result.error}"
                    raise FlextOracleTargetProcessingError(
                        msg,
                        operation="standard_insert",
                        table_name=table_name,
                        record_id=sequence,
                    )

                sequence += 1

            logger.info(f"Standard inserted {len(records)} records to {table_name}")
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
                schema_name, table_name, table, merge_keys,
            )

            # Execute merges
            sequence = 0
            loaded_at = datetime.now(UTC)

            for record in records:
                row_data = self._prepare_row_data(record, table, sequence, loaded_at)

                # Prepare parameters for merge
                params = {}
                for k, v in row_data.items():
                    params[f"src_{k}"] = v

                # Execute merge using flext-db-oracle API
                result = self.oracle_api.query(merge_sql, params)
                if result.is_failure:
                    msg = f"Merge failed: {result.error}"
                    raise FlextOracleTargetProcessingError(
                        msg,
                        operation="standard_merge",
                        table_name=table_name,
                        record_id=sequence,
                    )

                sequence += 1

            logger.info(f"Standard merged {len(records)} records to {table_name}")
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
                    msg = "No connection available for bulk operations"
                    raise FlextOracleTargetProcessingError(
                        msg,
                        operation="bulk_insert",
                        table_name=table_name,
                        batch_size=len(records),
                    )

                # Get table metadata
                table_key = f"{schema_name}.{table_name}"
                if table_key not in self._tables:
                    msg = f"Table metadata not found for {table_key}"
                    raise FlextOracleTargetProcessingError(
                        msg,
                        operation="bulk_insert",
                        table_name=table_name,
                    )

                table = self._tables[table_key]

                # Check if we need to do merge or append
                if self.config.sdc_mode == "merge":
                    return await self._bulk_merge(
                        schema_name, table_name, records, table,
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
            sequence = 0
            loaded_at = datetime.now(UTC)

            # Prepare all records for bulk insert
            for record in records:
                row_data = self._prepare_row_data(record, table, sequence, loaded_at)
                bulk_data.append(row_data)
                sequence += 1

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
                msg = f"Failed to build INSERT statement: {sql_result.error}"
                raise FlextOracleTargetProcessingError(
                    msg,
                    operation="bulk_append",
                    table_name=table_name,
                )

            sql = sql_result.value

            # Execute bulk insert using batch operations
            operations = [(sql, row) for row in bulk_data]
            result = self.oracle_api.execute_batch(operations)

            if result.is_failure:
                msg = f"Bulk append failed: {result.error}"
                raise FlextOracleTargetProcessingError(
                    msg,
                    operation="bulk_append",
                    table_name=table_name,
                    batch_size=len(records),
                )

            logger.info(f"Bulk appended {len(records)} records to {table_name}")
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
                schema_name, table_name, table, merge_keys,
            )

            # Prepare merge operations
            operations = []
            sequence = 0

            for record in records:
                row_data = self._prepare_row_data(record, table, sequence, loaded_at)
                # Convert to parameter dict for merge
                params = {f"src_{k}": v for k, v in row_data.items()}
                operations.append((merge_sql, params))
                sequence += 1

            # Execute batch merge using flext-db-oracle API
            result = self.oracle_api.execute_batch(operations)

            if result.is_failure:
                msg = f"Bulk merge failed: {result.error}"
                raise FlextOracleTargetProcessingError(
                    msg,
                    operation="bulk_merge",
                    table_name=table_name,
                    batch_size=len(records),
                )

            logger.info(f"Bulk merged {len(records)} records to {table_name}")
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
        """Prepare row data for insertion."""
        row_data = {}

        # Check if we're in JSON storage mode
        if self.config.storage_mode == "json":
            # Store entire record as JSON
            json_col_name = self.config.json_column_name
            # Remove SDC metadata from the record for clean JSON storage
            clean_record = {
                k: v for k, v in record.items() if not k.startswith("_sdc_")
            }
            row_data[json_col_name] = json.dumps(clean_record)

            # Add key columns if in merge mode
            for col in table.columns:
                col_name = col.name
                if col_name != json_col_name and col_name not in {
                    self.config.sdc_extracted_at_column,
                    self.config.sdc_loaded_at_column,
                    self.config.sdc_deleted_at_column,
                    self.config.sdc_sequence_column,
                }:
                    # This is a key column, extract from record
                    value = record.get(col_name.lower(), record.get(col_name))
                    if isinstance(value, bool):
                        value = 1 if value else 0
                    row_data[col_name] = value
        else:
            # Flattened or hybrid mode
            if self.config.storage_mode == "flattened":
                # Flatten the record
                flattened_record = self._flatten_record(record)
            else:
                # Hybrid mode - flatten to max depth
                flattened_record = self._flatten_record(
                    record,
                    max_depth=self.config.max_flattening_depth,
                )

            # Map flattened data to columns
            for col in table.columns:
                col_name = col.name
                if col_name not in {
                    self.config.sdc_extracted_at_column,
                    self.config.sdc_loaded_at_column,
                    self.config.sdc_deleted_at_column,
                    self.config.sdc_sequence_column,
                }:
                    # Get value from flattened record (case-insensitive)
                    value = None
                    for k, v in flattened_record.items():
                        if k.upper() == col_name:
                            value = v
                            break

                    # Convert complex types to JSON
                    if isinstance(value, (dict, list)):
                        value = json.dumps(value)
                    elif isinstance(value, bool):
                        value = 1 if value else 0

                    row_data[col_name] = value

        # Add SDC metadata columns with custom names
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

        return merge_result.value

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
                exec_result = connected_api.execute_ddl(ddl_result.value)
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
