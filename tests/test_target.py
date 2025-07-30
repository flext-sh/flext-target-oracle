"""Unit tests for Oracle Target implementation."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from flext_core import FlextResult

from flext_target_oracle import FlextOracleTarget, FlextOracleTargetConfig, LoadMethod


class TestFlextOracleTarget:
    """Test Oracle Target implementation."""

    @pytest.mark.asyncio
    async def test_target_initialization(
        self, sample_config: FlextOracleTargetConfig
    ) -> None:
        """Test target initialization."""
        target = FlextOracleTarget(config=sample_config)

        if target.name != "flext-oracle-target":

            raise AssertionError(f"Expected {"flext-oracle-target"}, got {target.name}")
        assert isinstance(target.target_config, FlextOracleTargetConfig)
        if target.target_config.oracle_host != "localhost":
            raise AssertionError(f"Expected {"localhost"}, got {target.target_config.oracle_host}")
        assert target.target_config.oracle_port == 1521

    @pytest.mark.asyncio
    async def test_test_connection_success(
        self, sample_target: FlextOracleTarget
    ) -> None:
        """Test successful connection test."""
        # Mock the validation to return True
        with patch.object(
            sample_target.target_config, "validate_oracle_config", return_value=True
        ):
            result = sample_target._test_connection_impl()
            if not (result):
                raise AssertionError(f"Expected True, got {result}")

    @pytest.mark.asyncio
    async def test_test_connection_failure(
        self, sample_target: FlextOracleTarget
    ) -> None:
        """Test failed connection test."""
        # Mock the validation to return False
        with patch.object(
            sample_target.target_config, "validate_oracle_config", return_value=False
        ):
            result = sample_target._test_connection_impl()
            if result:
                raise AssertionError(f"Expected False, got {result}")
    @pytest.mark.asyncio
    async def test_write_records_success(
        self, sample_target: FlextOracleTarget, batch_records: list[dict[str, object]]
    ) -> None:
        """Test successful record writing."""
        # Mock the loader to return success
        with patch.object(
            sample_target._loader, "load_record", return_value=FlextResult.ok(None)
        ):
            result = await sample_target._write_records_impl(batch_records)
            assert result.is_success

    @pytest.mark.asyncio
    async def test_write_records_failure(
        self, sample_target: FlextOracleTarget, batch_records: list[dict[str, object]]
    ) -> None:
        """Test failed record writing."""
        # Mock the loader to return failure
        with patch.object(
            sample_target._loader,
            "load_record",
            return_value=FlextResult.fail("Load failed"),
        ):
            result = await sample_target._write_records_impl(batch_records)
            assert not result.is_success
            error_msg = result.error or ""
            if "Load failed" not in error_msg:
                raise AssertionError(f"Expected 'Load failed' in {error_msg}")

    @pytest.mark.asyncio
    async def test_write_records_invalid_format(
        self, sample_target: FlextOracleTarget
    ) -> None:
        """Test record writing with invalid format."""
        invalid_records: list[dict[str, object]] = [
            {"invalid": "format"},  # Missing stream and record
            {"stream": "users"},  # Missing record
            {"record": {"id": 1}},  # Missing stream
        ]

        result = await sample_target._write_records_impl(invalid_records)
        assert result.is_success  # Should continue processing other records

    @pytest.mark.asyncio
    async def test_process_singer_message_schema(
        self, sample_target: FlextOracleTarget, schema: dict[str, object]
    ) -> None:
        """Test processing SCHEMA message."""
        # Mock the loader to return success
        with patch.object(
            sample_target._loader,
            "ensure_table_exists",
            return_value=FlextResult.ok(None),
        ):
            result = await sample_target.process_singer_message(schema)
            assert result.is_success

    @pytest.mark.asyncio
    async def test_process_singer_message_record(
        self, sample_target: FlextOracleTarget, record: dict[str, object]
    ) -> None:
        """Test processing RECORD message."""
        # Mock the loader to return success
        with patch.object(
            sample_target._loader, "load_record", return_value=FlextResult.ok(None)
        ):
            result = await sample_target.process_singer_message(record)
            assert result.is_success

    @pytest.mark.asyncio
    async def test_process_singer_message_state(
        self, sample_target: FlextOracleTarget, state: dict[str, object]
    ) -> None:
        """Test processing STATE message."""
        result = await sample_target.process_singer_message(state)
        assert result.is_success

    @pytest.mark.asyncio
    async def test_process_singer_message_unknown_type(
        self, sample_target: FlextOracleTarget
    ) -> None:
        """Test processing unknown message type."""
        unknown_message = {"type": "UNKNOWN", "data": "test"}
        result = await sample_target.process_singer_message(unknown_message)
        assert not result.is_success
        error_msg = result.error or ""
        if "Unknown message type" not in error_msg:
            raise AssertionError(f"Expected 'Unknown message type' in {error_msg}")

    @pytest.mark.asyncio
    async def test_handle_schema_success(
        self, sample_target: FlextOracleTarget
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
            assert result.is_success

    @pytest.mark.asyncio
    async def test_handle_schema_missing_stream(
        self, sample_target: FlextOracleTarget
    ) -> None:
        """Test schema handling with missing stream."""
        schema_message = {
            "type": "SCHEMA",
            "schema": {"type": "object"},
            # Missing stream
        }

        result = await sample_target._handle_schema(schema_message)
        assert not result.is_success
        error_msg = result.error or ""
        if "missing stream name" not in error_msg:
            raise AssertionError(f"Expected 'missing stream name' in {error_msg}")

    @pytest.mark.asyncio
    async def test_handle_record_success(
        self, sample_target: FlextOracleTarget
    ) -> None:
        """Test successful record handling."""
        record_message = {
            "type": "RECORD",
            "stream": "users",
            "record": {"id": 1, "name": "John"},
        }

        # Mock the loader to return success
        with patch.object(
            sample_target._loader, "load_record", return_value=FlextResult.ok(None)
        ):
            result = await sample_target._handle_record(record_message)
            assert result.is_success

    @pytest.mark.asyncio
    async def test_handle_record_missing_data(
        self, sample_target: FlextOracleTarget
    ) -> None:
        """Test record handling with missing data."""
        record_message = {
            "type": "RECORD",
            "stream": "users",
            # Missing record
        }

        result = await sample_target._handle_record(record_message)
        assert not result.is_success
        error_msg = result.error or ""
        if "missing stream or data" not in error_msg:
            raise AssertionError(f"Expected 'missing stream or data' in {error_msg}")

    @pytest.mark.asyncio
    async def test_handle_state_success(self, sample_target: FlextOracleTarget) -> None:
        """Test successful state handling."""
        state_message = {
            "type": "STATE",
            "value": {"bookmarks": {"users": {"last_updated": "2025-01-01T00:00:00Z"}}},
        }

        result = await sample_target._handle_state(state_message)
        assert result.is_success

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
            assert result.is_success
            assert result.data is not None, "Result data should not be None"
            if result.data["total_records"] != 100:
                raise AssertionError(f"Expected {100}, got {result.data["total_records"]}")

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
            assert not result.is_success
            error_msg = result.error or ""
            if "Finalization failed" not in error_msg:
                raise AssertionError(f"Expected 'Finalization failed' in {error_msg}")

    def test_get_implementation_metrics(self, sample_target: FlextOracleTarget) -> None:
        """Test implementation metrics."""
        metrics = sample_target._get_implementation_metrics()

        if "oracle_host" not in metrics:

            raise AssertionError(f"Expected {"oracle_host"} in {metrics}")
        assert "oracle_port" in metrics
        if "default_schema" not in metrics:
            raise AssertionError(f"Expected {"default_schema"} in {metrics}")
        assert "load_method" in metrics
        if "use_bulk_operations" not in metrics:
            raise AssertionError(f"Expected {"use_bulk_operations"} in {metrics}")

        if metrics["oracle_host"] != "localhost":

            raise AssertionError(f"Expected {"localhost"}, got {metrics["oracle_host"]}")
        assert metrics["oracle_port"] == 1521
        # The default_schema comes from FlextBaseConfig, not FlextOracleTargetConfig
        assert (
            metrics["default_schema"] == "SINGER_DATA"
        )  # Default value from FlextBaseConfig
        if metrics["load_method"] != "append-only":
            raise AssertionError(f"Expected {"append-only"}, got {metrics["load_method"]}")
        if not (metrics["use_bulk_operations"]):
            raise AssertionError(f"Expected True, got {metrics["use_bulk_operations"]}")

    def test_target_config_class(self) -> None:
        """Test that target uses correct config class."""
        if FlextOracleTarget.config_class != FlextOracleTargetConfig:
            raise AssertionError(f"Expected {FlextOracleTargetConfig}, got {FlextOracleTarget.config_class}")

    def test_target_name(self) -> None:
        """Test target name."""
        if FlextOracleTarget.name != "flext-oracle-target":
            raise AssertionError(f"Expected {"flext-oracle-target"}, got {FlextOracleTarget.name}")

    @pytest.mark.asyncio
    async def test_exception_handling_in_write_records(
        self, sample_target: FlextOracleTarget
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
            assert not result.is_success
            error_msg = result.error or ""
            if "Database error" not in error_msg:
                raise AssertionError(f"Expected 'Database error' in {error_msg}")

    @pytest.mark.asyncio
    async def test_exception_handling_in_process_message(
        self, sample_target: FlextOracleTarget
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
            assert not result.is_success
            error_msg = result.error or ""
            if "Processing error" not in error_msg:
                raise AssertionError(f"Expected 'Processing error' in {error_msg}")
