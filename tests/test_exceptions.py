"""Unit tests for Oracle Target Exceptions."""

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
            raise AssertionError(f"Expected {"Test error"} in {str(error)}")
        assert isinstance(error, FlextOracleTargetError)

    def test_flext_oracle_target_connection_error(self) -> None:
        """Test Oracle connection error."""
        error = FlextOracleTargetConnectionError("Connection failed")
        if "Connection failed" not in str(error):
            raise AssertionError(f"Expected {"Connection failed"} in {str(error)}")
        assert isinstance(error, FlextOracleTargetError)
        assert isinstance(error, FlextOracleTargetConnectionError)

    def test_flext_oracle_target_authentication_error(self) -> None:
        """Test Oracle authentication error."""
        error = FlextOracleTargetAuthenticationError("Authentication failed")
        if "Authentication failed" not in str(error):
            raise AssertionError(f"Expected {"Authentication failed"} in {str(error)}")
        assert isinstance(error, FlextOracleTargetError)
        assert isinstance(error, FlextOracleTargetAuthenticationError)

    def test_flext_oracle_target_processing_error(self) -> None:
        """Test Oracle processing error."""
        error = FlextOracleTargetProcessingError("Processing failed")
        if "Processing failed" not in str(error):
            raise AssertionError(f"Expected {"Processing failed"} in {str(error)}")
        assert isinstance(error, FlextOracleTargetError)
        assert isinstance(error, FlextOracleTargetProcessingError)

    def test_flext_oracle_target_schema_error(self) -> None:
        """Test Oracle schema error."""
        error = FlextOracleTargetSchemaError("Schema validation failed")
        if "Schema validation failed" not in str(error):
            raise AssertionError(f"Expected {"Schema validation failed"} in {str(error)}")
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
            raise AssertionError(f"Expected {"Connection failed"} in {str(connection_error)}")
        assert "Auth failed" in str(auth_error)
        if "Processing failed" not in str(processing_error):
            raise AssertionError(f"Expected {"Processing failed"} in {str(processing_error)}")
        assert "Schema failed" in str(schema_error)

    def test_exception_raising_and_catching(self) -> None:
        """Test raising and catching exceptions."""
        # Test raising FlextOracleTargetError
        with pytest.raises(FlextOracleTargetError) as exc_info:
            raise FlextOracleTargetError("Test error")
        if "Test error" not in str(exc_info.value):
            raise AssertionError(f"Expected {"Test error"} in {str(exc_info.value)}")

        # Test raising FlextOracleTargetConnectionError
        with pytest.raises(FlextOracleTargetConnectionError) as exc_info:
            raise FlextOracleTargetConnectionError("Connection error")
        if "Connection error" not in str(exc_info.value):
            raise AssertionError(f"Expected {"Connection error"} in {str(exc_info.value)}")

        # Test catching specific exception
        try:
            raise FlextOracleTargetAuthenticationError("Auth error")
        except FlextOracleTargetAuthenticationError as e:
            if "Auth error" not in str(e):
                raise AssertionError(f"Expected {"Auth error"} in {str(e)}")
        except FlextOracleTargetError:
            pytest.fail("Should have caught FlextOracleTargetAuthenticationError")

        # Test catching base exception
        try:
            raise FlextOracleTargetSchemaError("Schema error")
        except FlextOracleTargetError as e:
            if "Schema error" not in str(e):
                raise AssertionError(f"Expected {"Schema error"} in {str(e)}")
        except (RuntimeError, ValueError, TypeError):
            pytest.fail("Should have caught FlextOracleTargetError")

    def test_exception_in_error_handling_pattern(self) -> None:
        """Test exceptions in typical error handling patterns."""

        def function_that_might_fail(should_fail: bool) -> None:
            if should_fail:
                raise FlextOracleTargetConnectionError("Simulated connection failure")

        # Test successful execution
        try:
            function_that_might_fail(False)
        except FlextOracleTargetError:
            pytest.fail("Should not have raised exception")

        # Test failed execution
        with pytest.raises(FlextOracleTargetConnectionError) as exc_info:
            function_that_might_fail(True)
        if "Simulated connection failure" not in str(exc_info.value):
            raise AssertionError(f"Expected {"Simulated connection failure"} in {str(exc_info.value)}")

    def test_exception_with_context_management(self) -> None:
        """Test exceptions in context management scenarios."""

        class MockOracleConnection:
            def __enter__(self) -> None:
                raise FlextOracleTargetConnectionError("Connection failed")

            def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
                pass

        # Test that connection errors are properly raised
        with pytest.raises(FlextOracleTargetConnectionError) as exc_info:
            with MockOracleConnection():
                pass
        if "Connection failed" not in str(exc_info.value):
            raise AssertionError(f"Expected {"Connection failed"} in {str(exc_info.value)}")

    def test_exception_serialization(self) -> None:
        """Test that exceptions can be serialized properly."""
        error = FlextOracleTargetProcessingError("Processing failed")

        # Test string representation
        error_str = str(error)
        if "Processing failed" not in error_str:
            raise AssertionError(f"Expected {"Processing failed"} in {error_str}")

        # Test repr representation
        error_repr = repr(error)
        if "FlextOracleTargetProcessingError" not in error_repr:
            raise AssertionError(f"Expected {"FlextOracleTargetProcessingError"} in {error_repr}")
        assert "Processing failed" in error_repr

    def test_exception_comparison(self) -> None:
        """Test exception comparison."""
        error1 = FlextOracleTargetError("Same message")
        error2 = FlextOracleTargetError("Same message")
        error3 = FlextOracleTargetError("Different message")

        # Test that exceptions with same message are equal
        if str(error1) != str(error2):
            raise AssertionError(f"Expected {str(error2)}, got {str(error1)}")
        assert str(error1) != str(error3)

    def test_exception_in_logging_context(self) -> None:
        """Test exceptions in logging context."""


        # Create a logger
        logger = logging.getLogger("test_oracle_target")

        # Test that exceptions can be logged
        try:
            raise FlextOracleTargetSchemaError("Schema validation failed")
        except FlextOracleTargetSchemaError as e:
            # This should not raise an exception
            logger.error(f"Oracle schema error: {e}")
            if "Schema validation failed" not in str(e):
                raise AssertionError(f"Expected {"Schema validation failed"} in {str(e)}")
