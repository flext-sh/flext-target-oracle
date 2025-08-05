"""Unit Tests for FlextOracleTarget - Singer Target Implementation.

This module tests the main Singer Target implementation including message processing,
FLEXT ecosystem integration, and error handling patterns. Tests validate Singer
protocol compliance and Oracle data loading operations.

Test Categories:
    - Target initialization and configuration
    - Singer message processing (SCHEMA, RECORD, STATE)
    - FlextResult error handling patterns
    - Oracle loader integration

Note:
    Integration tests with actual Oracle database are in tests/integration/.
    Performance tests are in tests/performance/.

"""

from unittest.mock import patch

import pytest
from flext_core import FlextResult
from flext_target_oracle import FlextOracleTarget, FlextOracleTargetConfig


class TestFlextOracleTarget:
    """Test Oracle Target implementation."""

    @pytest.mark.asyncio
    async def test_target_initialization(
        self,
        sample_config: FlextOracleTargetConfig,
    ) -> None:
        """Test target initialization."""
        target = FlextOracleTarget(config=sample_config)

        if target.name != "flext-oracle-target":
            msg: str = f"Expected {'flext-oracle-target'}, got {target.name}"
            raise AssertionError(msg)
        assert isinstance(target.target_config, FlextOracleTargetConfig)
        if target.target_config.oracle_host != "localhost":
            msg: str = f"Expected {'localhost'}, got {target.target_config.oracle_host}"
            raise AssertionError(msg)
        assert target.target_config.oracle_port == 1521

    @pytest.mark.asyncio
    async def test_test_connection_success(
        self,
        sample_target: FlextOracleTarget,
    ) -> None:
        """Test successful connection test."""
        # Mock the domain validation to return success
        with patch(
            "flext_target_oracle.config.FlextOracleTargetConfig.validate_domain_rules",
            return_value=FlextResult.ok(None),
        ):
            result = sample_target._test_connection_impl()
            if not (result):
                msg: str = f"Expected True, got {result}"
                raise AssertionError(msg)

    @pytest.mark.asyncio
    async def test_test_connection_failure(
        self,
        sample_target: FlextOracleTarget,
    ) -> None:
        """Test failed connection test."""
        # Mock the domain validation to return failure
        with patch(
            "flext_target_oracle.config.FlextOracleTargetConfig.validate_domain_rules",
            return_value=FlextResult.fail("Validation failed"),
        ):
            result = sample_target._test_connection_impl()
            if result:
                msg: str = f"Expected False, got {result}"
                raise AssertionError(msg)

    @pytest.mark.asyncio
    async def test_write_records_success(
        self,
        sample_target: FlextOracleTarget,
        batch_records: list[dict[str, object]],
    ) -> None:
        """Test successful record writing."""
        # Mock the loader to return success
        with patch.object(
            sample_target._loader,
            "load_record",
            return_value=FlextResult.ok(None),
        ):
            result = await sample_target._write_records_impl(batch_records)
            assert result.success

    @pytest.mark.asyncio
    async def test_write_records_failure(
        self,
        sample_target: FlextOracleTarget,
        batch_records: list[dict[str, object]],
    ) -> None:
        """Test failed record writing."""
        # Mock the loader to return failure
        with patch.object(
            sample_target._loader,
            "load_record",
            return_value=FlextResult.fail("Load failed"),
        ):
            result = await sample_target._write_records_impl(batch_records)
            assert not result.success
            error_msg = result.error or ""
            if "Load failed" not in error_msg:
                msg: str = f"Expected 'Load failed' in {error_msg}"
                raise AssertionError(msg)

    @pytest.mark.asyncio
    async def test_write_records_invalid_format(
        self,
        sample_target: FlextOracleTarget,
    ) -> None:
        """Test record writing with invalid format."""
        invalid_records: list[dict[str, object]] = [
            {"invalid": "format"},  # Missing stream and record
            {"stream": "users"},  # Missing record
            {"record": {"id": 1}},  # Missing stream
        ]

        result = await sample_target._write_records_impl(invalid_records)
        assert result.success  # Should continue processing other records

    @pytest.mark.asyncio
    async def test_process_singer_message_schema(
        self,
        sample_target: FlextOracleTarget,
        schema: dict[str, object],
    ) -> None:
        """Test processing SCHEMA message."""
        # Mock the loader to return success
        with patch.object(
            sample_target._loader,
            "ensure_table_exists",
            return_value=FlextResult.ok(None),
        ):
            result = await sample_target.process_singer_message(schema)
            assert result.success

    @pytest.mark.asyncio
    async def test_process_singer_message_record(
        self,
        sample_target: FlextOracleTarget,
        record: dict[str, object],
    ) -> None:
        """Test processing RECORD message."""
        # Mock the loader to return success
        with patch.object(
            sample_target._loader,
            "load_record",
            return_value=FlextResult.ok(None),
        ):
            result = await sample_target.process_singer_message(record)
            assert result.success

    @pytest.mark.asyncio
    async def test_process_singer_message_state(
        self,
        sample_target: FlextOracleTarget,
        state: dict[str, object],
    ) -> None:
        """Test processing STATE message."""
        result = await sample_target.process_singer_message(state)
        assert result.success

    @pytest.mark.asyncio
    async def test_process_singer_message_unknown_type(
        self,
        sample_target: FlextOracleTarget,
    ) -> None:
        """Test processing unknown message type."""
        unknown_message = {"type": "UNKNOWN", "data": "test"}
        result = await sample_target.process_singer_message(unknown_message)
        assert not result.success
        error_msg = result.error or ""
        if "Unknown message type" not in error_msg:
            msg: str = f"Expected 'Unknown message type' in {error_msg}"
            raise AssertionError(msg)

    @pytest.mark.asyncio
    async def test_handle_schema_success(
        self,
        sample_target: FlextOracleTarget,
    ) -> None:
        """Test successful schema handling."""
        schema_message = {
            "type": "SCHEMA",
            "stream": "users",
            "schema": {"type": "object", "properties": {"id": {"type": "integer"}}},
        }

        # Mock the loader to return success
        with patch.object(
            sample_target._loader,
            "ensure_table_exists",
            return_value=FlextResult.ok(None),
        ):
            result = await sample_target._handle_schema(schema_message)
            assert result.success

    @pytest.mark.asyncio
    async def test_handle_schema_missing_stream(
        self,
        sample_target: FlextOracleTarget,
    ) -> None:
        """Test schema handling with missing stream."""
        schema_message = {
            "type": "SCHEMA",
            "schema": {"type": "object"},
            # Missing stream
        }

        result = await sample_target._handle_schema(schema_message)
        assert not result.success
        error_msg = result.error or ""
        if "missing stream name" not in error_msg:
            msg: str = f"Expected 'missing stream name' in {error_msg}"
            raise AssertionError(msg)

    @pytest.mark.asyncio
    async def test_handle_record_success(
        self,
        sample_target: FlextOracleTarget,
    ) -> None:
        """Test successful record handling."""
        record_message = {
            "type": "RECORD",
            "stream": "users",
            "record": {"id": 1, "name": "John"},
        }

        # Mock the loader to return success
        with patch.object(
            sample_target._loader,
            "load_record",
            return_value=FlextResult.ok(None),
        ):
            result = await sample_target._handle_record(record_message)
            assert result.success

    @pytest.mark.asyncio
    async def test_handle_record_missing_data(
        self,
        sample_target: FlextOracleTarget,
    ) -> None:
        """Test record handling with missing data."""
        record_message = {
            "type": "RECORD",
            "stream": "users",
            # Missing record
        }

        result = await sample_target._handle_record(record_message)
        assert not result.success
        error_msg = result.error or ""
        if "missing stream or data" not in error_msg:
            msg: str = f"Expected 'missing stream or data' in {error_msg}"
            raise AssertionError(msg)

    @pytest.mark.asyncio
    async def test_handle_state_success(self, sample_target: FlextOracleTarget) -> None:
        """Test successful state handling."""
        state_message = {
            "type": "STATE",
            "value": {"bookmarks": {"users": {"last_updated": "2025-01-01T00:00:00Z"}}},
        }

        result = await sample_target._handle_state(state_message)
        assert result.success

    @pytest.mark.asyncio
    async def test_finalize_success(self, sample_target: FlextOracleTarget) -> None:
        """Test successful finalization."""
        # Mock the loader to return success with stats
        mock_stats = {
            "total_records": 100,
            "successful_records": 100,
            "failed_records": 0,
            "total_batches": 5,
        }

        with patch.object(
            sample_target._loader,
            "finalize_all_streams",
            return_value=FlextResult.ok(mock_stats),
        ):
            result = await sample_target.finalize()
            assert result.success
            assert result.data is not None, "Result data should not be None"
            if result.data["total_records"] != 100:
                msg: str = f"Expected {100}, got {result.data['total_records']}"
                raise AssertionError(msg)

    @pytest.mark.asyncio
    async def test_finalize_failure(self, sample_target: FlextOracleTarget) -> None:
        """Test failed finalization."""
        # Mock the loader to return failure
        with patch.object(
            sample_target._loader,
            "finalize_all_streams",
            return_value=FlextResult.fail("Finalization failed"),
        ):
            result = await sample_target.finalize()
            assert not result.success
            error_msg = result.error or ""
            if "Finalization failed" not in error_msg:
                msg: str = f"Expected 'Finalization failed' in {error_msg}"
                raise AssertionError(msg)

    def test_get_implementation_metrics(self, sample_target: FlextOracleTarget) -> None:
        """Test implementation metrics."""
        metrics = sample_target._get_implementation_metrics()

        if "oracle_host" not in metrics:
            msg: str = f"Expected {'oracle_host'} in {metrics}"
            raise AssertionError(msg)
        assert "oracle_port" in metrics
        if "default_schema" not in metrics:
            msg: str = f"Expected {'default_schema'} in {metrics}"
            raise AssertionError(msg)
        assert "load_method" in metrics
        if "use_bulk_operations" not in metrics:
            msg: str = f"Expected {'use_bulk_operations'} in {metrics}"
            raise AssertionError(msg)

        if metrics["oracle_host"] != "localhost":
            msg: str = f"Expected {'localhost'}, got {metrics['oracle_host']}"
            raise AssertionError(msg)
        assert metrics["oracle_port"] == 1521
        # The default_schema comes from the test fixture configuration
        assert (
            metrics["default_schema"] == "TEST_SCHEMA"
        )  # Value from sample_config fixture
        if metrics["load_method"] != "insert":
            msg: str = f"Expected {'insert'}, got {metrics['load_method']}"
            raise AssertionError(msg)
        if not (metrics["use_bulk_operations"]):
            msg: str = f"Expected True, got {metrics['use_bulk_operations']}"
            raise AssertionError(msg)

    def test_target_config_class(self) -> None:
        """Test that target uses correct config class."""
        if FlextOracleTarget.config_class != FlextOracleTargetConfig:
            msg: str = f"Expected {FlextOracleTargetConfig}, got {FlextOracleTarget.config_class}"
            raise AssertionError(msg)

    def test_target_name(self) -> None:
        """Test target name."""
        if FlextOracleTarget.name != "flext-oracle-target":
            msg: str = f"Expected {'flext-oracle-target'}, got {FlextOracleTarget.name}"
            raise AssertionError(msg)

    @pytest.mark.asyncio
    async def test_exception_handling_in_write_records(
        self,
        sample_target: FlextOracleTarget,
    ) -> None:
        """Test exception handling in record writing."""
        batch_records = [{"stream": "users", "record": {"id": 1}}]

        # Mock the loader to raise an exception
        with patch.object(
            sample_target._loader,
            "load_record",
            side_effect=Exception("Database error"),
        ):
            result = await sample_target._write_records_impl(batch_records)
            assert not result.success
            error_msg = result.error or ""
            if "Database error" not in error_msg:
                msg: str = f"Expected 'Database error' in {error_msg}"
                raise AssertionError(msg)

    @pytest.mark.asyncio
    async def test_exception_handling_in_process_message(
        self,
        sample_target: FlextOracleTarget,
    ) -> None:
        """Test exception handling in message processing."""
        record_message = {"type": "RECORD", "stream": "users", "record": {"id": 1}}

        # Mock the loader to raise an exception
        with patch.object(
            sample_target._loader,
            "load_record",
            side_effect=Exception("Processing error"),
        ):
            result = await sample_target.process_singer_message(record_message)
            assert not result.success
            error_msg = result.error or ""
            if "Processing error" not in error_msg:
                msg: str = f"Expected 'Processing error' in {error_msg}"
                raise AssertionError(msg)
