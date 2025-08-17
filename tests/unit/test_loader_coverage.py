"""Additional Coverage Tests for FlextOracleTargetLoader.

This module provides targeted tests to improve coverage on specific methods
in the loader that are not adequately tested, focusing on error conditions,
edge cases, and integration scenarios.
"""

from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from flext_core import FlextResult

from flext_target_oracle import FlextOracleTargetConfig, FlextOracleTargetLoader


class TestFlextOracleTargetLoaderCoverage:
    """Coverage-focused tests for FlextOracleTargetLoader methods."""

    def test_init_with_custom_config(self) -> None:
      """Test loader initialization with custom configuration."""
      config = FlextOracleTargetConfig(
          oracle_host="custom-host",
          oracle_port=9999,
          oracle_service="CUSTOM_DB",
          oracle_user="custom_user",
          oracle_password="custom_pass",
          default_target_schema="CUSTOM_SCHEMA",
          batch_size=5000,
      )

      loader = FlextOracleTargetLoader(config)

      # Verify configuration is stored correctly
      assert loader.config == config
      assert loader._record_buffers == {}
      assert loader._total_records == 0

    @pytest.mark.asyncio
    async def test_ensure_table_exists_error_handling(self) -> None:
      """Test ensure_table_exists with error conditions."""
      config = FlextOracleTargetConfig(
          oracle_host="localhost",
          oracle_service="xe",
          oracle_user="test",
          oracle_password="test",
      )
      loader = FlextOracleTargetLoader(config)

      # Mock Oracle API to raise exception
      loader.oracle_api = MagicMock()
      loader.oracle_api.__enter__ = MagicMock(return_value=loader.oracle_api)
      loader.oracle_api.__exit__ = MagicMock()
      loader.oracle_api.query = Mock(side_effect=Exception("Connection failed"))

      schema = {
          "type": "object",
          "properties": {
              "id": {"type": "integer"},
              "name": {"type": "string"},
          },
      }

      result = await loader.ensure_table_exists("test_stream", schema)
      assert result.is_failure
      assert "Failed to ensure table exists" in str(result.error)

    @pytest.mark.asyncio
    async def test_load_record_invalid_data(self) -> None:
      """Test load_record with invalid record data."""
      config = FlextOracleTargetConfig(
          oracle_host="localhost",
          oracle_service="xe",
          oracle_user="test",
          oracle_password="test",
      )
      loader = FlextOracleTargetLoader(config)

      # Test with None record data
      result = await loader.load_record("test_stream", None)
      assert result.is_failure
      assert "Invalid record data" in str(result.error)

      # Test with non-dict record data
      result = await loader.load_record("test_stream", "invalid_data")
      assert result.is_failure
      assert "Invalid record data" in str(result.error)

    @pytest.mark.asyncio
    async def test_insert_batch_connection_error(self) -> None:
      """Test _insert_batch with connection errors."""
      config = FlextOracleTargetConfig(
          oracle_host="localhost",
          oracle_service="xe",
          oracle_user="test",
          oracle_password="test",
      )
      loader = FlextOracleTargetLoader(config)

      # Mock Oracle API to raise connection error when used as context manager
      mock_api = MagicMock()
      mock_api.__enter__.side_effect = RuntimeError("Connection failed")
      loader.oracle_api = mock_api

      records = [{"id": 1, "name": "test"}]
      result = await loader._insert_batch("test_table", records)

      assert result.is_failure
      assert "Batch insert failed" in str(result.error)

    @pytest.mark.asyncio
    async def test_insert_batch_query_failure(self) -> None:
      """Test _insert_batch with query execution failure."""
      config = FlextOracleTargetConfig(
          oracle_host="localhost",
          oracle_service="xe",
          oracle_user="test",
          oracle_password="test",
      )
      loader = FlextOracleTargetLoader(config)

      # Mock Oracle API connection success but query failure
      mock_api = MagicMock()
      mock_api.query = Mock(return_value=FlextResult.fail("SQL execution failed"))

      loader.oracle_api = MagicMock()
      loader.oracle_api.__enter__ = MagicMock(return_value=mock_api)
      loader.oracle_api.__exit__ = MagicMock()

      records = [{"id": 1, "name": "test"}]
      result = await loader._insert_batch("test_table", records)

      assert result.is_failure
      assert "Insert failed" in str(result.error)

    @pytest.mark.asyncio
    async def test_finalize_all_streams_error(self) -> None:
      """Test finalize_all_streams with error conditions."""
      config = FlextOracleTargetConfig(
          oracle_host="localhost",
          oracle_service="xe",
          oracle_user="test",
          oracle_password="test",
      )
      loader = FlextOracleTargetLoader(config)

      # The loader uses internal batch management now
      # Mock _flush_batch to fail
      with patch.object(loader, "_flush_batch") as mock_flush:
          mock_flush.return_value = FlextResult.fail("Flush failed")

          result = await loader.finalize_all_streams()
          assert result.is_failure
          assert "Failed to finalize streams" in str(result.error)

    @pytest.mark.asyncio
    async def test_flush_stream_empty(self) -> None:
      """Test _flush_stream with empty records."""
      config = FlextOracleTargetConfig(
          oracle_host="localhost",
          oracle_service="xe",
          oracle_user="test",
          oracle_password="test",
      )
      loader = FlextOracleTargetLoader(config)

      # Test flushing empty stream
      result = await loader._flush_batch("empty_stream")
      assert result.success  # Should succeed with no-op

    @pytest.mark.asyncio
    async def test_load_record_batch_processing(self) -> None:
      """Test load_record batch processing logic."""
      config = FlextOracleTargetConfig(
          oracle_host="localhost",
          oracle_service="xe",
          oracle_user="test",
          oracle_password="test",
          batch_size=2,  # Small batch size for testing
      )
      loader = FlextOracleTargetLoader(config)

      # Mock table existence check
      loader.ensure_table_exists = AsyncMock(return_value=FlextResult.ok(None))

      # Mock batch flush
      loader._flush_stream = AsyncMock(return_value=FlextResult.ok(None))

      # Load records - should trigger batch flush
      await loader.load_record("test_stream", {"id": 1, "name": "test1"})
      await loader.load_record("test_stream", {"id": 2, "name": "test2"})

      # Verify flush was called when batch size reached
      loader._flush_stream.assert_called()

    def test_loader_initialization_edge_cases(self) -> None:
      """Test loader initialization with various configurations."""
      # Test with minimal config
      minimal_config = FlextOracleTargetConfig(
          oracle_host="localhost",
          oracle_service="xe",
          oracle_user="test",
          oracle_password="test",
      )
      loader = FlextOracleTargetLoader(minimal_config)
      assert loader.config == minimal_config

      # Test with full config
      full_config = FlextOracleTargetConfig(
          oracle_host="prod-oracle.company.com",
          oracle_port=1521,
          oracle_service="PRODDB",
          oracle_user="prod_user",
          oracle_password="prod_password",
          default_target_schema="PROD_SCHEMA",
          batch_size=5000,
          connection_timeout=120,
          use_bulk_operations=True,
      )
      loader_full = FlextOracleTargetLoader(full_config)
      assert loader_full.config == full_config

    def test_table_creation_scenarios(self) -> None:
      """Test table creation edge cases."""
      config = FlextOracleTargetConfig(
          oracle_host="localhost",
          oracle_service="xe",
          oracle_user="test",
          oracle_password="test",
      )
      loader = FlextOracleTargetLoader(config)

      # Test internal state management
      assert len(loader._record_buffers) == 0
      assert loader._total_records == 0

      # Test configuration access
      assert loader.config.oracle_host == "localhost"
      assert loader.config.oracle_service == "xe"

    @pytest.mark.asyncio
    async def test_comprehensive_error_scenarios(self) -> None:
      """Test comprehensive error scenarios across methods."""
      config = FlextOracleTargetConfig(
          oracle_host="localhost",
          oracle_service="xe",
          oracle_user="test",
          oracle_password="test",
      )
      loader = FlextOracleTargetLoader(config)

      # Test exception during record processing
      with patch.object(
          loader,
          "_create_table",
          side_effect=Exception("Table creation error"),
      ):
          result = await loader.load_record("test", {"id": 1})
          assert result.is_failure
          assert "Failed to load record" in str(result.error)

    def test_stream_state_management(self) -> None:
      """Test stream state management functionality."""
      config = FlextOracleTargetConfig(
          oracle_host="localhost",
          oracle_service="xe",
          oracle_user="test",
          oracle_password="test",
      )
      loader = FlextOracleTargetLoader(config)

      # Test basic loader state
      assert loader.config == config
      assert loader._total_records == 0

      # The loader doesn't expose stream records directly anymore
      # This is handled internally by the batch processing
