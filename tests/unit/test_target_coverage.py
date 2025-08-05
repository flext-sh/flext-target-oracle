"""Additional Coverage Tests for FlextOracleTarget.

This module provides targeted tests to improve coverage on specific methods
that are not adequately tested in the main test suite. Focus on edge cases,
error conditions, and integration scenarios.
"""

from unittest.mock import AsyncMock, patch

import pytest
from flext_core import FlextResult
from flext_target_oracle import FlextOracleTarget, FlextOracleTargetConfig


class TestFlextOracleTargetCoverage:
    """Coverage-focused tests for FlextOracleTarget methods."""

    def test_write_record_success(self) -> None:
        """Test _write_record method success path."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_service="xe",
            oracle_user="test",
            oracle_password="test",
        )
        target = FlextOracleTarget(config)

        # Mock the loader to return success
        mock_result = FlextResult.ok(None)
        target._loader.load_record = AsyncMock(return_value=mock_result)

        # Test successful record write
        target._write_record("test_stream", {"id": 1, "name": "test"})

        # Verify the loader was called
        target._loader.load_record.assert_called_once()

    def test_write_record_failure(self) -> None:
        """Test _write_record method failure path."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_service="xe",
            oracle_user="test",
            oracle_password="test",
        )
        target = FlextOracleTarget(config)

        # Mock the loader to return failure
        mock_result = FlextResult.fail("Database connection failed")
        target._loader.load_record = AsyncMock(return_value=mock_result)

        # Test record write failure
        with pytest.raises(RuntimeError, match="Failed to write record"):
            target._write_record("test_stream", {"id": 1, "name": "test"})

    def test_write_record_exception(self) -> None:
        """Test _write_record method exception handling."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_service="xe",
            oracle_user="test",
            oracle_password="test",
        )
        target = FlextOracleTarget(config)

        # Mock the loader to raise exception
        target._loader.load_record = AsyncMock(
            side_effect=Exception("Connection error"),
        )

        # Test exception handling
        with pytest.raises(RuntimeError, match="Singer SDK _write_record failed"):
            target._write_record("test_stream", {"id": 1, "name": "test"})

    def test_test_connection_impl_success(self) -> None:
        """Test _test_connection_impl method success path."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_service="xe",
            oracle_user="test",
            oracle_password="test",
        )
        target = FlextOracleTarget(config)

        # Mock successful validation using patch
        with patch.object(
            target.target_config,
            "validate_domain_rules",
        ) as mock_validate:
            mock_validate.return_value = FlextResult.ok(None)

            # Test successful connection
            result = target._test_connection_impl()
            assert result is True

    def test_test_connection_impl_basic(self) -> None:
        """Test _test_connection_impl basic functionality."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_service="xe",
            oracle_user="test",
            oracle_password="test",
        )
        target = FlextOracleTarget(config)

        # The current implementation always returns True if no exception occurs
        # This test validates the success path
        result = target._test_connection_impl()
        assert result is True

    def test_test_connection_impl_exception(self) -> None:
        """Test _test_connection_impl exception handling."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_service="xe",
            oracle_user="test",
            oracle_password="test",
        )
        target = FlextOracleTarget(config)

        # Test exception handling by patching the logger to simulate a failure condition
        with patch("flext_target_oracle.target.logger") as mock_logger:
            # Mock an exception during logging
            mock_logger.info.side_effect = RuntimeError("System error")

            # Test exception handling
            result = target._test_connection_impl()
            assert result is False

    def test_get_implementation_metrics(self) -> None:
        """Test _get_implementation_metrics method."""
        config = FlextOracleTargetConfig(
            oracle_host="prod-oracle.company.com",
            oracle_port=1521,
            oracle_service="PRODDB",
            oracle_user="data_loader",
            oracle_password="secure_password",
            default_target_schema="DATA_SCHEMA",
            use_bulk_operations=True,
        )
        target = FlextOracleTarget(config)

        metrics = target._get_implementation_metrics()

        # Verify all expected metrics are present
        expected_keys = {
            "oracle_host",
            "oracle_port",
            "default_schema",
            "load_method",
            "use_bulk_operations",
        }
        assert all(key in metrics for key in expected_keys)

        # Verify specific values
        assert metrics["oracle_host"] == "prod-oracle.company.com"
        assert metrics["oracle_port"] == 1521
        assert metrics["default_schema"] == "DATA_SCHEMA"
        assert metrics["use_bulk_operations"] is True

    @pytest.mark.asyncio
    async def test_write_records_impl_edge_cases(self) -> None:
        """Test _write_records_impl with edge cases."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_service="xe",
            oracle_user="test",
            oracle_password="test",
        )
        target = FlextOracleTarget(config)

        # Test with empty records list
        result = await target._write_records_impl([])
        assert result.success

        # Test with invalid record format
        invalid_records = [
            {"stream": "test", "record": {"id": 1}},  # Valid
            {"invalid": "format"},  # Invalid - missing stream/record
            {"stream": None, "record": {"id": 2}},  # Invalid - None stream
        ]

        # Mock loader to return success for valid records
        target._loader.load_record = AsyncMock(return_value=FlextResult.ok(None))

        result = await target._write_records_impl(invalid_records)
        assert result.success

        # Verify only valid record was processed
        target._loader.load_record.assert_called_once_with("test", {"id": 1})

    @pytest.mark.asyncio
    async def test_process_singer_message_unknown_type(self) -> None:
        """Test process_singer_message with unknown message type."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_service="xe",
            oracle_user="test",
            oracle_password="test",
        )
        target = FlextOracleTarget(config)

        # Test with unknown message type
        unknown_message = {"type": "UNKNOWN", "data": "test"}
        result = await target.process_singer_message(unknown_message)

        assert result.is_failure
        assert "Unknown message type" in str(result.error)

    @pytest.mark.asyncio
    async def test_handle_state_error_path(self) -> None:
        """Test _handle_state method error handling."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_service="xe",
            oracle_user="test",
            oracle_password="test",
        )
        target = FlextOracleTarget(config)

        # Mock to raise exception during state handling
        with patch("flext_target_oracle.target.logger") as mock_logger:
            mock_logger.debug.side_effect = RuntimeError("Logging error")

            state_message = {"type": "STATE", "value": {"test": "data"}}
            result = await target._handle_state(state_message)

            # Should handle exception gracefully
            assert result.is_failure
            assert "State handling failed" in str(result.error)

    def test_target_compatibility_aliases(self) -> None:
        """Test compatibility aliases work correctly."""
        from flext_target_oracle.target import FlextTargetOracle, TargetOracle

        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_service="xe",
            oracle_user="test",
            oracle_password="test",
        )

        # Test compatibility aliases
        target1 = FlextTargetOracle(config)
        target2 = TargetOracle(config)

        assert isinstance(target1, FlextOracleTarget)
        assert isinstance(target2, FlextOracleTarget)
        assert target1.name == "flext-oracle-target"
        assert target2.name == "flext-oracle-target"
