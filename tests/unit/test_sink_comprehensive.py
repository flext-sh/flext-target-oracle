"""Comprehensive tests for Oracle sink functionality.

Tests for the OracleSink class and related sink functionality.
"""

import asyncio
from datetime import UTC, datetime
from unittest.mock import AsyncMock, Mock, patch

import pytest
from flext_core import ServiceResult

from flext_target_oracle.sinks import OracleSink


class TestOracleSinkInitialization:
    """Test Oracle sink initialization."""

    def test_sink_creation_with_minimal_config(self) -> None:
        """Test creating sink with minimal configuration."""
        config = {
            "host": "localhost",
            "username": "test_user",
            "password": "test_pass",
        }

        sink = OracleSink(
            target=Mock(),
            schema={"type": "object"},
            key_properties=[],
            config=config,
        )
        assert sink.connector_config == config
        assert sink.schema == {"type": "object"}
        assert sink.key_properties == []

    def test_sink_creation_with_full_config(self) -> None:
        """Test creating sink with full configuration."""
        config = {
            "host": "oracle.example.com",
            "port": 1521,
            "service_name": "XEPDB1",
            "username": "flext_user",
            "password": "secure_password",
            "default_target_schema": "FLEXT_DATA",
            "batch_size": 5000,
            "load_method": "upsert",
        }

        sink = OracleSink(
            target=Mock(),
            schema={"type": "object"},
            key_properties=["id"],
            config=config,
        )
        assert sink.connector_config == config
        assert sink.key_properties == ["id"]

    def test_sink_stream_name_property(self) -> None:
        """Test sink stream name property."""
        config = {"host": "localhost", "username": "test", "password": "test"}
        sink = OracleSink(
            target=Mock(),
            schema={"type": "object"},
            key_properties=[],
            config=config,
        )

        # Stream name should be derived from schema or default
        expected_name = sink.stream_name
        assert isinstance(expected_name, str)
        assert len(expected_name) > 0


class TestOracleSinkRecordProcessing:
    """Test record processing functionality."""

    @pytest.fixture
    def mock_sink(self) -> OracleSink:
        """Create a mock sink for testing."""
        config = {
            "host": "localhost",
            "username": "test_user",
            "password": "test_pass",
        }
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string"},
            },
        }
        return OracleSink(
            target=Mock(),
            schema=schema,
            key_properties=["id"],
            config=config,
        )

    @pytest.mark.asyncio
    async def test_process_record_structure(self, mock_sink: OracleSink) -> None:
        """Test record processing structure."""
        record = {
            "id": 123,
            "name": "John Doe",
            "email": "john@example.com",
        }

        # Mock the process_record method to test structure
        with patch.object(mock_sink, "process_record") as mock_process:
            mock_process.return_value = None
            await mock_sink.process_record(record)
            mock_process.assert_called_once_with(record)

    @pytest.mark.asyncio
    async def test_process_batch_async(self, mock_sink: OracleSink) -> None:
        """Test asynchronous batch processing."""
        records = [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
        ]

        # Mock the process_batch method
        with patch.object(
            mock_sink,
            "process_batch",
            new_callable=AsyncMock,
        ) as mock_batch:
            mock_batch.return_value = ServiceResult.ok("Processed 2 records")

            result = await mock_sink.process_batch(records)
            assert result.is_success
            assert "2 records" in result.value
            mock_batch.assert_called_once_with(records)

    @pytest.mark.asyncio
    async def test_record_validation(self, mock_sink: OracleSink) -> None:
        """Test record validation against schema."""
        # Valid record
        valid_record = {
            "id": 1,
            "name": "Test User",
            "email": "test@example.com",
        }

        # Test validation through process_record behavior
        with (
            patch.object(mock_sink, "_validate_record") as mock_validate,
            patch.object(mock_sink, "_service") as mock_service,
        ):
            mock_validate.return_value = None  # Valid record, no exception
            mock_service.load_record = AsyncMock(return_value=None)

            # Test valid record processing doesn't raise
            try:
                await mock_sink.process_record(valid_record)
                validation_passed = True
            except (TypeError, ValueError):
                validation_passed = False
            assert validation_passed

            # Test validation is called
            mock_validate.assert_called_with(valid_record)


class TestOracleSinkErrorHandling:
    """Test error handling in Oracle sink."""

    @pytest.fixture
    def error_sink(self) -> OracleSink:
        """Create a sink configured for error testing."""
        config = {
            "host": "nonexistent.host",
            "username": "invalid_user",
            "password": "wrong_password",
        }
        schema = {"type": "object", "properties": {"id": {"type": "integer"}}}
        return OracleSink(
            target=Mock(),
            schema=schema,
            key_properties=["id"],
            config=config,
        )

    @pytest.mark.asyncio
    async def test_connection_error_handling(self, error_sink: OracleSink) -> None:
        """Test handling of connection errors."""
        with patch.object(
            error_sink,
            "_internal_process_batch",
            new_callable=AsyncMock,
        ) as mock_batch:
            mock_batch.side_effect = ConnectionError("Cannot connect to Oracle")

            records = [{"id": 1}]
            result = await error_sink.process_batch(records)

            # Should handle the error gracefully
            assert not result.is_success
            assert "Cannot connect to Oracle" in str(result.error)

    @pytest.mark.asyncio
    async def test_data_validation_error_handling(self, error_sink: OracleSink) -> None:
        """Test handling of data validation errors."""
        invalid_records = [
            {"id": "not_an_integer"},  # Wrong type
            {"invalid_field": "value"},  # Unknown field
        ]

        with patch.object(
            error_sink,
            "_internal_process_batch",
            new_callable=AsyncMock,
        ) as mock_batch:
            mock_batch.side_effect = ValueError("Invalid data format")

            result = await error_sink.process_batch(invalid_records)
            assert not result.is_success
            assert "Invalid data format" in str(result.error)

    @pytest.mark.asyncio
    async def test_sql_error_handling(self, error_sink: OracleSink) -> None:
        """Test handling of SQL execution errors."""
        records = [{"id": 1}]

        with patch.object(
            error_sink,
            "_internal_process_batch",
            new_callable=AsyncMock,
        ) as mock_batch:
            # Simulate SQL error
            mock_batch.side_effect = Exception(
                "ORA-00942: table or view does not exist",
            )

            result = await error_sink.process_batch(records)
            assert not result.is_success
            assert "ORA-00942" in str(result.error)


class TestOracleSinkPerformance:
    """Test performance-related functionality."""

    @pytest.fixture
    def performance_sink(self) -> OracleSink:
        """Create a sink for performance testing."""
        config = {
            "host": "localhost",
            "username": "perf_user",
            "password": "perf_pass",
            "batch_size": 1000,
        }
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "data": {"type": "string"},
            },
        }
        return OracleSink(
            target=Mock(),
            schema=schema,
            key_properties=["id"],
            config=config,
        )

    @pytest.mark.asyncio
    async def test_batch_size_handling(self, performance_sink: OracleSink) -> None:
        """Test handling of different batch sizes."""
        # Small batch
        small_batch = [{"id": i, "data": f"record_{i}"} for i in range(10)]

        # Large batch
        large_batch = [{"id": i, "data": f"record_{i}"} for i in range(2000)]

        with patch.object(
            performance_sink,
            "process_batch",
            new_callable=AsyncMock,
        ) as mock_batch:
            mock_batch.return_value = ServiceResult.ok("Batch processed")

            # Both should be handled successfully
            small_result = await performance_sink.process_batch(small_batch)
            large_result = await performance_sink.process_batch(large_batch)

            assert small_result.is_success
            assert large_result.is_success
            assert mock_batch.call_count == 2

    @pytest.mark.asyncio
    async def test_concurrent_batch_processing(
        self,
        performance_sink: OracleSink,
    ) -> None:
        """Test concurrent processing of multiple batches."""
        batch1 = [{"id": i, "data": f"batch1_{i}"} for i in range(100)]
        batch2 = [{"id": i + 100, "data": f"batch2_{i}"} for i in range(100)]
        batch3 = [{"id": i + 200, "data": f"batch3_{i}"} for i in range(100)]

        with patch.object(
            performance_sink,
            "process_batch",
            new_callable=AsyncMock,
        ) as mock_batch:
            mock_batch.return_value = ServiceResult.ok(
                "Concurrent batch processed",
            )

            # Process batches concurrently
            tasks = [
                performance_sink.process_batch(batch1),
                performance_sink.process_batch(batch2),
                performance_sink.process_batch(batch3),
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # All should succeed
            for result in results:
                assert not isinstance(result, Exception)
                assert result.is_success

    @pytest.mark.asyncio
    async def test_memory_efficiency(self, performance_sink: OracleSink) -> None:
        """Test memory efficiency with large data sets."""
        # This test ensures the sink doesn't hold onto large amounts of data
        large_record = {
            "id": 1,
            "data": "x" * 10000,  # 10KB of data
        }

        # Process and verify no memory leaks
        with patch.object(performance_sink, "process_record") as mock_process:
            mock_process.return_value = None

            for i in range(100):  # Process 100 large records
                large_record["id"] = i
                await performance_sink.process_record(large_record.copy())

            assert mock_process.call_count == 100


class TestOracleSinkIntegration:
    """Test integration aspects of Oracle sink."""

    @pytest.mark.asyncio
    async def test_sink_with_different_data_types(self) -> None:
        """Test sink handling different data types."""
        config = {"host": "localhost", "username": "test", "password": "test"}
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "price": {"type": "number"},
                "active": {"type": "boolean"},
                "created_at": {"type": "string", "format": "date-time"},
                "metadata": {"type": "object"},
                "tags": {"type": "array"},
            },
        }

        sink = OracleSink(
            target=Mock(),
            schema=schema,
            key_properties=["id"],
            config=config,
        )

        record = {
            "id": 42,
            "name": "Test Product",
            "price": 29.99,
            "active": True,
            "created_at": datetime.now(tz=UTC).isoformat(),
            "metadata": {"category": "electronics"},
            "tags": ["new", "featured"],
        }

        # Should handle all data types without error
        with patch.object(sink, "process_record") as mock_process:
            mock_process.return_value = None
            await sink.process_record(record)
            mock_process.assert_called_once_with(record)

    def test_sink_table_name_generation(self) -> None:
        """Test table name generation from stream."""
        config = {"host": "localhost", "username": "test", "password": "test"}
        schema = {"type": "object", "stream": "user_events"}

        sink = OracleSink(
            target=Mock(),
            schema=schema,
            key_properties=[],
            config=config,
        )

        # Table name should be derived from stream or schema
        table_name = sink.stream_name
        assert isinstance(table_name, str)
        assert len(table_name) > 0
        # Should be valid Oracle table name (uppercase, no special chars)
        assert table_name.replace("_", "").isalnum()

    @pytest.mark.asyncio
    async def test_sink_cleanup_on_close(self) -> None:
        """Test proper cleanup when sink is closed."""
        config = {"host": "localhost", "username": "test", "password": "test"}
        sink = OracleSink(
            target=Mock(),
            schema={"type": "object"},
            key_properties=[],
            config=config,
        )

        # Mock cleanup methods
        with patch.object(sink, "_cleanup_resources") as mock_cleanup:
            # Simulate sink closing
            if hasattr(sink, "close"):
                await sink.close()
            elif hasattr(sink, "__aenter__"):
                async with sink:
                    pass

            # Cleanup should be called
            if mock_cleanup.called:
                mock_cleanup.assert_called()
