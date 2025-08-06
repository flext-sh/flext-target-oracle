"""Oracle Target Exception Hierarchy with FLEXT Error Handling Integration.

This module provides a comprehensive exception hierarchy for Oracle Singer target
operations, built on FLEXT ecosystem error handling patterns. The exceptions
provide detailed context for troubleshooting Oracle-specific issues while
maintaining consistency with FLEXT error handling standards.

The exception hierarchy follows Domain-Driven Design principles with specific
exception types for different failure categories: connection issues, authentication
problems, schema errors, and data processing failures. All exceptions include
detailed context for operational troubleshooting and monitoring.

Key Components:
    FlextOracleTargetError: Base exception with context preservation
    FlextOracleTargetConnectionError: Network and connectivity failures
    FlextOracleTargetAuthenticationError: Authentication and authorization issues
    FlextOracleTargetSchemaError: Table and schema management failures
    FlextOracleTargetProcessingError: Data processing and loading failures

Architecture Integration:
    FLEXT Error Patterns: Built on FlextTargetError for ecosystem consistency
    Context Preservation: Rich error context with stream names and operation details
    Monitoring Integration: Structured error information for observability systems
    Domain-Driven Design: Exception types aligned with business operation boundaries

Example:
    Raising and handling Oracle-specific exceptions:

    >>> try:
    ...     # Oracle operation that might fail
    ...     result = await oracle_api.connect()
    ... except Exception as e:
    ...     raise FlextOracleTargetConnectionError(
    ...         "Failed to connect to Oracle database",
    ...         host="prod-oracle.company.com",
    ...         port=1521,
    ...         service_name="PRODDB",
    ...         error_code="ORA-12541",
    ...     ) from e

    >>> try:
    ...     # Process Singer record
    ...     await loader.load_record("users", record_data)
    ... except FlextOracleTargetProcessingError as e:
    ...     logger.error("Record processing failed: %s", e, extra=e.context)

Note:
    This module resolves the exception duplication issue identified in docs/TODO.md
    by providing a single source of truth for Oracle target exceptions, eliminating
    the duplication between __init__.py and exceptions.py.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from flext_core import FlextTargetError


class FlextOracleTargetError(FlextTargetError):
    """Base exception for Oracle Singer target operations with context preservation.

    This is the root exception class for all Oracle target-specific errors,
    providing consistent error handling patterns across the FLEXT ecosystem.
    The exception includes detailed context information for troubleshooting
    and monitoring Oracle-specific operational issues.

    The exception follows FLEXT error handling patterns by extending FlextTargetError
    and providing Oracle-specific context while maintaining compatibility with
    ecosystem-wide error handling and observability systems.

    Key Features:
        - Context Preservation: Rich error context with Oracle-specific details
        - Stream Awareness: Includes Singer stream information when available
        - Monitoring Integration: Structured context for observability systems
        - Error Classification: Consistent categorization for error handling
        - Troubleshooting Support: Detailed information for operational diagnosis

    Attributes:
        message: Human-readable error description
        stream_name: Singer stream name if error is stream-specific
        context: Additional context information for troubleshooting
        component_type: Always "target" for target operations
        destination_system: Always "oracle" for Oracle operations

    Example:
        Raising base Oracle target errors:

        >>> raise FlextOracleTargetError(
        ...     "Oracle target operation failed",
        ...     stream_name="customer_orders",
        ...     operation="record_loading",
        ...     table_name="CUSTOMER_ORDERS",
        ...     batch_size=1000,
        ...     oracle_error_code="ORA-00001",
        ... )

        Catching and logging Oracle errors:

        >>> try:
        ...     # Oracle target operation
        ...     await target.process_singer_message(message)
        ... except FlextOracleTargetError as e:
        ...     logger.error(
        ...         f"Oracle target error: {e}",
        ...         extra={
        ...             "stream_name": e.stream_name,
        ...             "component_type": e.component_type,
        ...             "context": getattr(e, "context", {}),
        ...         },
        ...     )

    Note:
        This base class should not be raised directly in most cases. Use the
        specific exception subclasses (ConnectionError, AuthenticationError,
        etc.) for better error classification and handling.

    """

    def __init__(
        self,
        message: str,
        stream_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Oracle target error with context and classification.

        Creates an Oracle target error with detailed context information for
        troubleshooting and monitoring. The error includes Oracle-specific
        classification and integrates with FLEXT ecosystem error patterns.

        Args:
            message: Human-readable error description explaining what went wrong
            stream_name: Optional Singer stream name if error is stream-specific
            **kwargs: Additional context information including:
                     - operation: The operation that failed (e.g., "record_loading")
                     - table_name: Oracle table name if applicable
                     - oracle_error_code: Oracle error code if available
                     - batch_size: Batch size if error occurred during batch processing
                     - Any other relevant context for troubleshooting

        Example:
            >>> error = FlextOracleTargetError(
            ...     "Failed to process batch",
            ...     stream_name="users",
            ...     operation="batch_insert",
            ...     table_name="USERS",
            ...     batch_size=500,
            ...     oracle_error_code="ORA-00001",
            ... )

        """
        super().__init__(
            message,
            component_type="target",
            stream_name=stream_name,
            destination_system="oracle",
            **kwargs,
        )


class FlextOracleTargetConnectionError(FlextOracleTargetError):
    """Oracle database connection and network-related errors.

    Raised when Oracle database connection establishment, authentication, or
    network communication fails. This exception provides detailed context
    about connection parameters and failure conditions for troubleshooting
    connectivity issues.

    Common scenarios include:
        - Network connectivity issues to Oracle host/port
        - Oracle listener not running or misconfigured
        - Firewall blocking database connections
        - DNS resolution failures for Oracle hostname
        - Connection timeout or connection refused errors

    Example:
        >>> raise FlextOracleTargetConnectionError(
        ...     "Unable to connect to Oracle database",
        ...     host="prod-oracle.company.com",
        ...     port=1521,
        ...     service_name="PRODDB",
        ...     timeout=30,
        ...     oracle_error_code="ORA-12541",
        ... )

    """

    def __init__(self, message: str, **kwargs: object) -> None:
        """Initialize Oracle connection error with detailed context.

        Args:
            message: Descriptive error message about the connection failure
            **kwargs: Connection context including host, port, service_name,
                     oracle_error_code, timeout, and other relevant details

        """
        super().__init__(f"Connection error: {message}", context=kwargs)


class FlextOracleTargetAuthenticationError(FlextOracleTargetError):
    """Oracle authentication and authorization failures.

    Raised when Oracle database authentication fails due to invalid credentials
    or when the authenticated user lacks required permissions for target operations.
    This exception helps distinguish between connectivity issues and credential problems.

    Common scenarios include:
        - Invalid username or password
        - User account locked or expired
        - Insufficient privileges for table creation or data insertion
        - Schema access denied
        - Required roles not granted to user

    Example:
        >>> raise FlextOracleTargetAuthenticationError(
        ...     "Authentication failed for Oracle user",
        ...     username="data_loader",
        ...     schema="DATA_WAREHOUSE",
        ...     required_privileges=["CREATE TABLE", "INSERT"],
        ...     oracle_error_code="ORA-00942",
        ... )

    """

    def __init__(self, message: str, **kwargs: object) -> None:
        """Initialize Oracle authentication error with context.

        Args:
            message: Descriptive error message about the authentication failure
            **kwargs: Authentication context including username, schema,
                     required_privileges, oracle_error_code, and other details

        """
        super().__init__(f"Authentication error: {message}", context=kwargs)


class FlextOracleTargetProcessingError(FlextOracleTargetError):
    """Oracle data processing and DML operation failures.

    Raised when Singer record processing, batch operations, or data transformation
    operations fail during execution. This exception covers all data manipulation
    failures that occur after successful connection and authentication.

    Common scenarios include:
        - Data type conversion failures during record processing
        - Constraint violations during data insertion
        - Batch processing failures or transaction rollbacks
        - JSON serialization errors for CLOB storage
        - Bulk operation timeouts or memory issues
        - Data validation failures

    Example:
        >>> raise FlextOracleTargetProcessingError(
        ...     "Batch insert failed due to constraint violation",
        ...     stream_name="customer_orders",
        ...     operation="batch_insert",
        ...     table_name="CUSTOMER_ORDERS",
        ...     batch_size=1000,
        ...     failed_record_count=15,
        ...     oracle_error_code="ORA-00001",
        ...     constraint_name="PK_CUSTOMER_ORDERS",
        ... )

    """

    def __init__(self, message: str, **kwargs: object) -> None:
        """Initialize Oracle processing error with operational context.

        Args:
            message: Descriptive error message about the processing failure
            **kwargs: Processing context including stream_name, operation,
                     table_name, batch_size, oracle_error_code, and other
                     relevant operational details

        """
        super().__init__(f"Processing error: {message}", context=kwargs)


class FlextOracleTargetSchemaError(FlextOracleTargetError):
    """Oracle schema and DDL operation failures.

    Raised when table creation, schema validation, or DDL operations fail due to
    database constraints, permission issues, or schema conflicts. This exception
    covers all schema-related operations that fail during target setup or evolution.

    Common scenarios include:
        - Table creation failures due to insufficient privileges
        - Schema name conflicts or invalid identifiers
        - DDL operation timeouts or resource constraints
        - Invalid table or column name characters
        - Schema does not exist or is not accessible
        - Object name length exceeds Oracle limits

    Example:
        >>> raise FlextOracleTargetSchemaError(
        ...     "Failed to create target table",
        ...     stream_name="customer_orders",
        ...     table_name="CUSTOMER_ORDERS",
        ...     schema_name="DATA_WAREHOUSE",
        ...     ddl_operation="CREATE TABLE",
        ...     oracle_error_code="ORA-00955",
        ...     conflicting_object="Existing table with same name",
        ... )

    """

    def __init__(self, message: str, **kwargs: object) -> None:
        """Initialize Oracle schema error with DDL context.

        Args:
            message: Descriptive error message about the schema operation failure
            **kwargs: Schema context including table_name, schema_name,
                     ddl_operation, oracle_error_code, and other DDL-related details

        """
        super().__init__(f"Schema error: {message}", context=kwargs)


__all__: list[str] = [
    "FlextOracleTargetAuthenticationError",
    "FlextOracleTargetConnectionError",
    "FlextOracleTargetError",
    "FlextOracleTargetProcessingError",
    "FlextOracleTargetSchemaError",
]
