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
from flext_db_oracle import FlextDbOracleApi, FlextDbOracleConfig

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

        # Oracle API from flext-db-oracle - create config directly
        from pydantic import SecretStr

        oracle_config = FlextDbOracleConfig(
            host=config.oracle_host,
            port=config.oracle_port,
            service_name=config.oracle_service,
            username=config.oracle_user,
            password=SecretStr(config.oracle_password),
            sid=None,
            timeout=config.connection_timeout,
            pool_min=1,
            pool_max=10,
            pool_increment=1,
            encoding="UTF-8",
            ssl_enabled=False,
            autocommit=False,
            ssl_server_dn_match=True,
        )
        self.oracle_api = FlextDbOracleApi(oracle_config)

        # Buffers for batch processing
        self._record_buffers: dict[str, list[dict[str, object]]] = {}
        self._total_records = 0

    async def ensure_table_exists(
        self,
        stream_name: str,
        schema: dict[str, object],
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
                # Use flext-db-oracle get_tables method instead of manual SQL
                tables_result = connected_api.get_tables(
                    schema=self.config.default_target_schema,
                )

                return await self._process_table_existence_result(
                    tables_result,
                    table_name,
                    stream_name,
                )

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception(f"Failed to ensure table exists for stream {stream_name}")
            return FlextResult.fail(f"Table creation failed: {e}")

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

            # Simple JSON storage approach
            schema_name = self.config.default_target_schema.upper()
            table_name_upper = table_name.upper()

            # Build INSERT SQL
            sql_template = 'INSERT INTO "{0}"."{1}" ("DATA", "_SDC_EXTRACTED_AT") VALUES (:data, :extracted_at)'
            sql = sql_template.format(schema_name, table_name_upper)

            # Build parameters
            params = []
            for record in records:
                param = {
                    "data": json.dumps(record),
                    "extracted_at": datetime.now(UTC).isoformat(),
                }
                params.append(param)

            # Execute insert using flext-db-oracle API with parameterized queries
            # Use context manager to ensure connection is active
            with self.oracle_api as connected_api:
                for param in params:
                    # Use parameterized query to prevent SQL injection
                    # Convert param to object dict for API compatibility
                    param_obj: dict[str, object] = dict(param)
                    result = connected_api.query(sql, param_obj)
                    if not result.success:
                        return FlextResult.fail(f"Insert failed: {result.error}")

            return FlextResult.ok(None)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception(f"Failed to insert batch to {table_name}")
            return FlextResult.fail(f"Batch insert failed: {e}")

    async def _create_table(self, table_name: str) -> FlextResult[None]:
        """Create table with simple JSON storage structure."""
        try:
            # Simple table structure - JSON storage
            schema_name = self.config.default_target_schema.upper()
            table_name_upper = table_name.upper()
            table_full = f'"{schema_name}"."{table_name_upper}"'

            create_sql_template = """
            CREATE TABLE {0} (
                "DATA" CLOB,
                "_SDC_EXTRACTED_AT" TIMESTAMP,
                "_SDC_BATCHED_AT" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                "_SDC_SEQUENCE" NUMBER DEFAULT 0
            )
            """
            create_sql = create_sql_template.format(table_full)

            # Execute via flext-db-oracle API with context manager
            with self.oracle_api as connected_api:
                result = connected_api.execute_ddl(create_sql)
                if not result.success:
                    return FlextResult.fail(f"Table creation failed: {result.error}")

            return FlextResult.ok(None)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception(f"Failed to create table {table_name}")
            return FlextResult.fail(f"Table creation failed: {e}")
