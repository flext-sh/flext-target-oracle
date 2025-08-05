"""Unit Tests for Oracle Target Exception Hierarchy.

This module tests the Oracle-specific exception classes and error handling patterns.
Tests validate exception hierarchy, error context preservation, and integration
with FLEXT error handling patterns.

Test Categories:
    - Exception creation and hierarchy
    - Error context preservation
    - FLEXT error pattern integration
    - Exception handling in various scenarios

Note:
    Tests validate the exception classes defined in exceptions.py.
    Integration with actual error scenarios tested in integration tests.

"""

import logging

import pytest
from flext_target_oracle.exceptions import (
    FlextOracleTargetAuthenticationError,
    FlextOracleTargetConnectionError,
    FlextOracleTargetError,
    FlextOracleTargetProcessingError,
    FlextOracleTargetSchemaError,
)


class TestFlextOracleTargetExceptions:
    """Test Oracle Target exception hierarchy."""

    def test_flext_oracle_target_error_base(self) -> None:
        """Test base Oracle target error."""
        error = FlextOracleTargetError("Test error")
        if "Test error" not in str(error):
            msg: str = f"Expected {'Test error'} in {error!s}"
            raise AssertionError(msg)
        assert isinstance(error, FlextOracleTargetError)

    def test_flext_oracle_target_connection_error(self) -> None:
        """Test Oracle connection error."""
        error = FlextOracleTargetConnectionError("Connection failed")
        if "Connection failed" not in str(error):
            msg: str = f"Expected {'Connection failed'} in {error!s}"
            raise AssertionError(msg)
        assert isinstance(error, FlextOracleTargetError)
        assert isinstance(error, FlextOracleTargetConnectionError)

    def test_flext_oracle_target_authentication_error(self) -> None:
        """Test Oracle authentication error."""
        error = FlextOracleTargetAuthenticationError("Authentication failed")
        if "Authentication failed" not in str(error):
            msg: str = f"Expected {'Authentication failed'} in {error!s}"
            raise AssertionError(msg)
        assert isinstance(error, FlextOracleTargetError)
        assert isinstance(error, FlextOracleTargetAuthenticationError)

    def test_flext_oracle_target_processing_error(self) -> None:
        """Test Oracle processing error."""
        error = FlextOracleTargetProcessingError("Processing failed")
        if "Processing failed" not in str(error):
            msg: str = f"Expected {'Processing failed'} in {error!s}"
            raise AssertionError(msg)
        assert isinstance(error, FlextOracleTargetError)
        assert isinstance(error, FlextOracleTargetProcessingError)

    def test_flext_oracle_target_schema_error(self) -> None:
        """Test Oracle schema error."""
        error = FlextOracleTargetSchemaError("Schema validation failed")
        if "Schema validation failed" not in str(error):
            msg: str = f"Expected {'Schema validation failed'} in {error!s}"
            raise AssertionError(msg)
        assert isinstance(error, FlextOracleTargetError)
        assert isinstance(error, FlextOracleTargetSchemaError)

    def test_exception_inheritance_hierarchy(self) -> None:
        """Test exception inheritance hierarchy."""
        # Test that all exceptions inherit from FlextOracleTargetError
        connection_error = FlextOracleTargetConnectionError("test")
        auth_error = FlextOracleTargetAuthenticationError("test")
        processing_error = FlextOracleTargetProcessingError("test")
        schema_error = FlextOracleTargetSchemaError("test")

        assert isinstance(connection_error, FlextOracleTargetError)
        assert isinstance(auth_error, FlextOracleTargetError)
        assert isinstance(processing_error, FlextOracleTargetError)
        assert isinstance(schema_error, FlextOracleTargetError)

    def test_exception_with_details(self) -> None:
        """Test exceptions with additional details."""
        # Test that exceptions can be created with additional context
        connection_error = FlextOracleTargetConnectionError("Connection failed")
        auth_error = FlextOracleTargetAuthenticationError("Auth failed")
        processing_error = FlextOracleTargetProcessingError("Processing failed")
        schema_error = FlextOracleTargetSchemaError("Schema failed")

        # All should be valid exceptions
        if "Connection failed" not in str(connection_error):
            msg: str = f"Expected {'Connection failed'} in {connection_error!s}"
            raise AssertionError(msg)
        assert "Auth failed" in str(auth_error)
        if "Processing failed" not in str(processing_error):
            msg: str = f"Expected {'Processing failed'} in {processing_error!s}"
            raise AssertionError(msg)
        assert "Schema failed" in str(schema_error)

    def test_exception_raising_and_catching(self) -> None:
        """Test raising and catching exceptions."""
        # Test raising FlextOracleTargetError
        msg = "Test error"
        with pytest.raises(FlextOracleTargetError) as exc_info:
            raise FlextOracleTargetError(msg)
        if "Test error" not in str(exc_info.value):
            msg: str = f"Expected {'Test error'} in {exc_info.value!s}"
            raise AssertionError(msg)

        # Test raising FlextOracleTargetConnectionError
        msg = "Connection error"
        with pytest.raises(FlextOracleTargetConnectionError) as exc_info:
            raise FlextOracleTargetConnectionError(msg)
        if "Connection error" not in str(exc_info.value):
            msg: str = f"Expected {'Connection error'} in {exc_info.value!s}"
            raise AssertionError(msg)

        # Test catching specific exception
        try:
            msg = "Auth error"
            raise FlextOracleTargetAuthenticationError(msg)
        except FlextOracleTargetAuthenticationError as e:
            if "Auth error" not in str(e):
                msg: str = f"Expected {'Auth error'} in {e!s}"
                raise AssertionError(msg) from None
        except FlextOracleTargetError:
            pytest.fail("Should have caught FlextOracleTargetAuthenticationError")

        # Test catching base exception
        try:
            msg = "Schema error"
            raise FlextOracleTargetSchemaError(msg)
        except FlextOracleTargetError as e:
            if "Schema error" not in str(e):
                msg: str = f"Expected {'Schema error'} in {e!s}"
                raise AssertionError(msg) from None
        except (RuntimeError, ValueError, TypeError):
            pytest.fail("Should have caught FlextOracleTargetError")

    def test_exception_in_error_handling_pattern(self) -> None:
        """Test exceptions in typical error handling patterns."""

        def function_that_might_fail(should_fail: bool) -> None:
            if should_fail:
                msg = "Simulated connection failure"
                raise FlextOracleTargetConnectionError(msg)

        # Test successful execution
        try:
            function_that_might_fail(False)
        except FlextOracleTargetError:
            pytest.fail("Should not have raised exception")

        # Test failed execution
        with pytest.raises(FlextOracleTargetConnectionError) as exc_info:
            function_that_might_fail(True)
        if "Simulated connection failure" not in str(exc_info.value):
            msg: str = (
                f"Expected {'Simulated connection failure'} in {exc_info.value!s}"
            )
            raise AssertionError(msg)

    def test_exception_with_context_management(self) -> None:
        """Test exceptions in context management scenarios."""

        class MockOracleConnection:
            def __enter__(self) -> None:
                msg = "Connection failed"
                raise FlextOracleTargetConnectionError(msg)

            def __exit__(
                self,
                exc_type: object,
                exc_val: object,
                exc_tb: object,
            ) -> None:
                pass

        # Test that connection errors are properly raised
        with (
            pytest.raises(FlextOracleTargetConnectionError) as exc_info,
            MockOracleConnection(),
        ):
            pass
        if "Connection failed" not in str(exc_info.value):
            msg: str = f"Expected {'Connection failed'} in {exc_info.value!s}"
            raise AssertionError(msg)

    def test_exception_serialization(self) -> None:
        """Test that exceptions can be serialized properly."""
        error = FlextOracleTargetProcessingError("Processing failed")

        # Test string representation
        error_str = str(error)
        if "Processing failed" not in error_str:
            msg: str = f"Expected {'Processing failed'} in {error_str}"
            raise AssertionError(msg)

        # Test repr representation
        error_repr = repr(error)
        if "FlextOracleTargetProcessingError" not in error_repr:
            msg: str = f"Expected {'FlextOracleTargetProcessingError'} in {error_repr}"
            raise AssertionError(msg)
        assert "Processing failed" in error_repr

    def test_exception_comparison(self) -> None:
        """Test exception comparison."""
        error1 = FlextOracleTargetError("Same message")
        error2 = FlextOracleTargetError("Same message")
        error3 = FlextOracleTargetError("Different message")

        # Test that exceptions with same message are equal
        if str(error1) != str(error2):
            msg: str = f"Expected {error2!s}, got {error1!s}"
            raise AssertionError(msg)
        assert str(error1) != str(error3)

    def test_exception_in_logging_context(self) -> None:
        """Test exceptions in logging context."""
        # Create a logger
        logger = logging.getLogger("test_oracle_target")

        # Test that exceptions can be logged
        try:
            msg = "Schema validation failed"
            raise FlextOracleTargetSchemaError(msg)
        except FlextOracleTargetSchemaError as e:
            # This should not raise an exception
            logger.exception("Oracle schema error")
            if "Schema validation failed" not in str(e):
                msg: str = f"Expected {'Schema validation failed'} in {e!s}"
                raise AssertionError(msg) from None
