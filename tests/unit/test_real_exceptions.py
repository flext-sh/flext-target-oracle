"""Real Oracle Exceptions Tests - Comprehensive Coverage.

Tests exception functionality with real scenarios for maximum coverage.
"""

import logging
from datetime import UTC, datetime
from typing import Never

import pytest

from flext_target_oracle.exceptions import (
    FlextOracleTargetAuthenticationError,
    FlextOracleTargetConnectionError,
    FlextOracleTargetError,
    FlextOracleTargetProcessingError,
    FlextOracleTargetSchemaError,
)


class TestRealOracleExceptions:
    """Test Oracle exceptions with real scenarios."""

    def _log_exception(self) -> None:
        """Helper method for logging exceptions."""
        from flext_core import get_logger
        logger = get_logger(__name__)
        logger.error("Error occurred")

    def _raise_processing_error(self, original_error: ValueError) -> Never:
        """Helper method to raise processing error."""
        msg = "Failed to process due to invalid value"
        raise FlextOracleTargetProcessingError(
            msg,
            stream_name="test",
        ) from original_error

    def _verify_exception_chain(self, exc: FlextOracleTargetProcessingError) -> None:
        """Helper method to verify exception chain."""
        assert exc.__cause__ is not None
        assert isinstance(exc.__cause__, ValueError)
        assert str(exc.__cause__) == "Invalid value"

    def _raise_processing_error_for_logging(self) -> None:
        """Helper method to raise processing error for logging test."""
        msg = "Processing failed"
        raise FlextOracleTargetProcessingError(
            msg,
            stream_name="test_stream",
            record_count=100,
        )

    def _raise_value_error_for_chaining(self) -> None:
        """Helper method to raise ValueError for exception chaining test."""
        msg = "Invalid value"
        raise ValueError(msg)

    def test_base_exception_creation(self) -> None:
        """Test creating base exception."""
        exc = FlextOracleTargetError("Base error occurred")

        assert str(exc) == "[SINGER_ERROR] Base error occurred"
        assert exc.message == "Base error occurred"
        assert exc.error_code == "SINGER_ERROR"
        assert exc.timestamp is not None
        assert exc.context == {}

    def test_base_exception_with_context(self) -> None:
        """Test base exception with context."""
        context = {
            "stream": "users",
            "record_id": 123,
            "operation": "insert",
        }
        exc = FlextOracleTargetError("Error with context", context=context)

        assert exc.context == context
        assert exc.context["stream"] == "users"
        assert exc.context["record_id"] == 123

    def test_connection_error_full(self) -> None:
        """Test connection error with all parameters."""
        exc = FlextOracleTargetConnectionError(
            "Failed to connect to Oracle",
            host="prod-oracle.company.com",
            port=1522,
            service_name="PRODDB",
            user="test_user",
            dsn="(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=prod-oracle.company.com)(PORT=1522))(CONNECT_DATA=(SERVICE_NAME=PRODDB)))",
        )

        assert "Failed to connect to Oracle" in str(exc)
        assert exc.host == "prod-oracle.company.com"
        assert exc.port == 1522
        assert exc.service_name == "PRODDB"
        assert exc.user == "test_user"
        assert exc.dsn is not None

        # Check formatted message
        full_message = str(exc)
        assert "prod-oracle.company.com:1522" in full_message

    def test_connection_error_minimal(self) -> None:
        """Test connection error with minimal parameters."""
        exc = FlextOracleTargetConnectionError("Connection refused")

        assert str(exc) == "[CONNECTION_ERROR] Connection refused"
        assert exc.host is None
        assert exc.port is None
        assert exc.service_name is None

    def test_authentication_error(self) -> None:
        """Test authentication error."""
        exc = FlextOracleTargetAuthenticationError(
            "Invalid credentials",
            user="test_user",
            auth_method="password",
        )

        assert "Invalid credentials" in str(exc)
        assert exc.user == "test_user"
        assert exc.auth_method == "password"
        assert exc.error_code == "AUTHENTICATION_ERROR"

    def test_authentication_error_wallet(self) -> None:
        """Test authentication error with wallet."""
        exc = FlextOracleTargetAuthenticationError(
            "Wallet authentication failed",
            user="wallet_user",
            auth_method="wallet",
            wallet_location="/opt/oracle/wallet",
        )

        assert exc.auth_method == "wallet"
        assert exc.wallet_location == "/opt/oracle/wallet"

    def test_schema_error_with_details(self) -> None:
        """Test schema error with full details."""
        exc = FlextOracleTargetSchemaError(
            "Invalid schema structure",
            stream_name="users",
            schema_hash="abc123def456",
            validation_errors=[
                "Missing required property: type",
                "Invalid format for date field",
            ],
        )

        assert "Invalid schema structure" in str(exc)
        assert exc.stream_name == "users"
        assert exc.schema_hash == "abc123def456"
        assert len(exc.validation_errors) == 2
        assert exc.error_code == "SCHEMA_ERROR"

    def test_schema_error_minimal(self) -> None:
        """Test schema error with minimal info."""
        exc = FlextOracleTargetSchemaError("Schema not found")

        assert exc.stream_name is None
        assert exc.schema_hash is None
        assert exc.validation_errors is None

    def test_processing_error_comprehensive(self) -> None:
        """Test processing error with all details."""
        exc = FlextOracleTargetProcessingError(
            "Failed to process record",
            stream_name="orders",
            record_count=1500,
            error_records=[
                {"id": 100, "error": "Invalid date format"},
                {"id": 250, "error": "Duplicate key"},
            ],
            operation="bulk_insert",
        )

        assert "Failed to process record" in str(exc)
        assert exc.stream_name == "orders"
        assert exc.record_count == 1500
        assert len(exc.error_records) == 2
        assert exc.operation == "bulk_insert"
        assert exc.error_code == "PROCESSING_ERROR"

    def test_processing_error_single_record(self) -> None:
        """Test processing error for single record."""
        exc = FlextOracleTargetProcessingError(
            "Record validation failed",
            stream_name="users",
            record_count=1,
            operation="validate",
        )

        assert exc.record_count == 1
        assert exc.error_records is None

    def test_exception_inheritance(self) -> None:
        """Test exception inheritance hierarchy."""
        # All should inherit from base
        conn_err = FlextOracleTargetConnectionError("test")
        auth_err = FlextOracleTargetAuthenticationError("test")
        schema_err = FlextOracleTargetSchemaError("test")
        proc_err = FlextOracleTargetProcessingError("test")

        assert isinstance(conn_err, FlextOracleTargetError)
        assert isinstance(auth_err, FlextOracleTargetError)
        assert isinstance(schema_err, FlextOracleTargetError)
        assert isinstance(proc_err, FlextOracleTargetError)

        # All should be Exception
        assert isinstance(conn_err, Exception)
        assert isinstance(auth_err, Exception)
        assert isinstance(schema_err, Exception)
        assert isinstance(proc_err, Exception)

    def test_exception_catching(self) -> None:
        """Test catching exceptions in hierarchy."""

        def raise_connection_error() -> Never:
            msg = "Connection failed"
            raise FlextOracleTargetConnectionError(msg)

        # Can catch as specific type
        with pytest.raises(FlextOracleTargetConnectionError):
            raise_connection_error()

        # Can catch as base type
        with pytest.raises(FlextOracleTargetError):
            raise_connection_error()

        # Can catch as Exception
        with pytest.raises(Exception):
            raise_connection_error()

    def test_exception_context_manager(self) -> Never:
        """Test using exceptions in context managers."""

        class MockResource:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                if exc_type is FlextOracleTargetConnectionError:
                    # Handle connection errors
                    return False  # Propagate
                return False

        def _raise_connection_error():
            msg = "Connection lost"
            raise FlextOracleTargetConnectionError(msg)

        with pytest.raises(FlextOracleTargetConnectionError), MockResource():
            _raise_connection_error()

    def test_exception_logging(self, caplog) -> None:
        """Test exception logging behavior."""
        with caplog.at_level(logging.ERROR):
            try:
                self._raise_processing_error_for_logging()
            except FlextOracleTargetProcessingError:
                self._log_exception()

        assert "Processing failed" in caplog.text
        assert "PROCESSING_ERROR" in caplog.text

    def test_exception_serialization(self) -> None:
        """Test exception can be serialized."""
        exc = FlextOracleTargetSchemaError(
            "Schema validation failed",
            stream_name="users",
            validation_errors=["Error 1", "Error 2"],
        )

        # Get exception details
        exc_dict = {
            "type": type(exc).__name__,
            "message": exc.message,
            "error_code": exc.error_code,
            "timestamp": exc.timestamp.isoformat() if exc.timestamp else None,
            "context": exc.context,
            "stream_name": getattr(exc, "stream_name", None),
            "validation_errors": getattr(exc, "validation_errors", None),
        }

        assert exc_dict["type"] == "FlextOracleTargetSchemaError"
        assert exc_dict["message"] == "Schema validation failed"
        assert exc_dict["error_code"] == "SCHEMA_ERROR"
        assert exc_dict["stream_name"] == "users"
        assert len(exc_dict["validation_errors"]) == 2

    def test_exception_chaining(self) -> None:
        """Test exception chaining."""
        try:
            try:
                # Original error
                self._raise_value_error_for_chaining()
            except ValueError as e:
                # Chain with our exception
                self._raise_processing_error(e)
        except FlextOracleTargetProcessingError as e:
            self._verify_exception_chain(e)

    def test_exception_comparison(self) -> None:
        """Test exception comparison."""
        exc1 = FlextOracleTargetError("Error 1")
        exc2 = FlextOracleTargetError("Error 1")
        exc3 = FlextOracleTargetError("Error 2")

        # Same message but different instances
        assert exc1 != exc2  # Different objects
        assert str(exc1) == str(exc2)  # Same string representation
        assert str(exc1) != str(exc3)  # Different messages

    def test_exception_timestamp(self) -> None:
        """Test exception timestamp is set."""
        before = datetime.now(UTC)
        exc = FlextOracleTargetError("Test error")
        after = datetime.now(UTC)

        assert exc.timestamp is not None
        assert before <= exc.timestamp <= after

    def test_complex_error_scenario(self) -> None:
        """Test complex error scenario with nested context."""
        # Simulate a complex processing error
        error_context = {
            "batch_id": "batch-001",
            "total_records": 1000,
            "failed_records": 15,
            "streams": ["users", "orders", "products"],
            "start_time": datetime.now(UTC).isoformat(),
            "error_summary": {
                "validation_errors": 10,
                "database_errors": 5,
            },
        }

        exc = FlextOracleTargetProcessingError(
            "Batch processing failed with multiple errors",
            stream_name="multi_stream_batch",
            record_count=1000,
            error_records=[
                {"stream": "users", "id": 100, "error": "Invalid email"},
                {"stream": "orders", "id": 200, "error": "FK constraint"},
                {"stream": "products", "id": 300, "error": "Duplicate SKU"},
            ],
            operation="batch_process",
            context=error_context,
        )

        assert exc.record_count == 1000
        assert len(exc.error_records) == 3
        assert exc.context["batch_id"] == "batch-001"
        assert exc.context["error_summary"]["validation_errors"] == 10

    def test_authentication_error_methods(self) -> None:
        """Test different authentication methods in errors."""
        # Password auth
        exc1 = FlextOracleTargetAuthenticationError(
            "Invalid password",
            user="user1",
            auth_method="password",
        )
        assert exc1.auth_method == "password"

        # Wallet auth
        exc2 = FlextOracleTargetAuthenticationError(
            "Wallet not found",
            user="user2",
            auth_method="wallet",
            wallet_location="/path/to/wallet",
        )
        assert exc2.auth_method == "wallet"
        assert exc2.wallet_location == "/path/to/wallet"

        # Kerberos auth
        exc3 = FlextOracleTargetAuthenticationError(
            "Kerberos ticket expired",
            user="user3",
            auth_method="kerberos",
        )
        assert exc3.auth_method == "kerberos"

    def test_connection_error_retry_info(self) -> None:
        """Test connection error with retry information."""
        exc = FlextOracleTargetConnectionError(
            "Connection failed after retries",
            host="localhost",
            port=1521,
            service_name="XE",
            context={
                "retry_count": 3,
                "max_retries": 3,
                "retry_delay": 5,
                "last_error": "ORA-12541: TNS:no listener",
            },
        )

        assert exc.context["retry_count"] == 3
        assert exc.context["last_error"] == "ORA-12541: TNS:no listener"

    def test_schema_error_diff(self) -> None:
        """Test schema error with schema differences."""
        exc = FlextOracleTargetSchemaError(
            "Schema mismatch detected",
            stream_name="users",
            schema_hash="old_hash_123",
            validation_errors=[
                "Property 'email' changed from 'string' to 'object'",
                "New required property: 'user_id'",
                "Removed property: 'username'",
            ],
            context={
                "old_version": 1,
                "new_version": 2,
                "breaking_changes": True,
            },
        )

        assert len(exc.validation_errors) == 3
        assert exc.context["breaking_changes"] is True

    def test_processing_error_bulk_details(self) -> None:
        """Test processing error with bulk operation details."""
        exc = FlextOracleTargetProcessingError(
            "Bulk insert partially failed",
            stream_name="large_dataset",
            record_count=10000,
            error_records=[{"batch": i, "count": 10} for i in range(5)],
            operation="bulk_insert",
            context={
                "successful_records": 9950,
                "failed_records": 50,
                "batch_size": 1000,
                "total_batches": 10,
                "failed_batches": 5,
                "performance": {
                    "records_per_second": 5000,
                    "total_time_seconds": 2.0,
                },
            },
        )

        assert exc.record_count == 10000
        assert len(exc.error_records) == 5
        assert exc.context["successful_records"] == 9950
        assert exc.context["performance"]["records_per_second"] == 5000
