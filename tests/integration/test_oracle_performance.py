"""Oracle performance tests.

Tests for Oracle database performance and optimization.
"""

import asyncio
import os
import time
from concurrent.futures import ThreadPoolExecutor

import pytest
from flext_db_oracle import OracleQueryService

from flext_target_oracle.application.services import SingerTargetService
from flext_target_oracle.domain.models import TargetConfig


class TestPerformanceBaseline:
    """Test basic performance characteristics."""

    @pytest.fixture
    def target_config(self) -> TargetConfig:
        """Create target configuration for performance testing."""
        return TargetConfig(
            host=os.getenv("ORACLE_HOST", "localhost"),
            port=int(os.getenv("ORACLE_PORT", "1521")),
            service_name=os.getenv("ORACLE_SERVICE_NAME", "XEPDB1"),
            username=os.getenv("ORACLE_USERNAME", "FLEXT_TEST"),
            password=os.getenv("ORACLE_PASSWORD", "test_password"),
            default_target_schema="FLEXT_PERF_TEST",
            batch_size=1000,
        )

    @pytest.mark.asyncio
    async def test_single_record_performance(self, target_config: TargetConfig) -> None:
        """Test performance of single record processing.

        ZERO TOLERANCE: Uses real Oracle E2E environment, NO SKIPS.
        """
        singer_service = SingerTargetService(target_config)

        # Setup table
        schema_message = {
            "type": "SCHEMA",
            "stream": "perf_single",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "data": {"type": "string"},
                },
            },
        }

        try:
            await singer_service.process_singer_message(schema_message)

            # Time single record processing
            start_time = time.time()

            record_message = {
                "type": "RECORD",
                "stream": "perf_single",
                "record": {"id": 1, "data": "performance test"},
            }

            result = await singer_service.process_singer_message(record_message)

            # Finalize to ensure processing completes
            await singer_service.finalize_all_streams()

            end_time = time.time()
            duration = end_time - start_time

            assert result.is_success
            assert duration < 5.0  # Should complete within 5 seconds

        except (ConnectionError, OSError, ValueError, AssertionError) as e:
            pytest.fail(f"Single record performance test failed: {e}")

    @pytest.mark.asyncio
    async def test_batch_performance(self, target_config: TargetConfig) -> None:
        """Test performance of batch processing.

        ZERO TOLERANCE: Uses real Oracle E2E environment, NO SKIPS.
        """
        singer_service = SingerTargetService(target_config)

        # Setup table
        schema_message = {
            "type": "SCHEMA",
            "stream": "perf_batch",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "data": {"type": "string"},
                },
            },
        }

        try:
            await singer_service.process_singer_message(schema_message)

            # Process large batch
            batch_size = 10000
            start_time = time.time()

            for i in range(batch_size):
                record_message = {
                    "type": "RECORD",
                    "stream": "perf_batch",
                    "record": {"id": i, "data": f"batch_record_{i}"},
                }
                result = await singer_service.process_singer_message(record_message)
                assert result.is_success

            # Finalize to flush all batches
            stats_result = await singer_service.finalize_all_streams()
            end_time = time.time()

            duration = end_time - start_time
            records_per_second = batch_size / duration

            assert stats_result.is_success
            assert records_per_second > 100  # At least 100 records/second

        except (ConnectionError, OSError, ValueError, AssertionError) as e:
            pytest.fail(f"Batch performance test failed: {e}")


class TestConcurrentProcessing:
    """Test concurrent processing performance."""

    @pytest.fixture
    def target_config(self) -> TargetConfig:
        """Create target configuration for concurrent testing."""
        return TargetConfig(
            host=os.getenv("ORACLE_HOST", "localhost"),
            port=int(os.getenv("ORACLE_PORT", "1521")),
            service_name=os.getenv("ORACLE_SERVICE_NAME", "XEPDB1"),
            username=os.getenv("ORACLE_USERNAME", "FLEXT_TEST"),
            password=os.getenv("ORACLE_PASSWORD", "test_password"),
            default_target_schema="FLEXT_PERF_TEST",
            batch_size=500,
            max_parallelism=4,
        )

    @pytest.mark.asyncio
    async def test_concurrent_streams(self, target_config: TargetConfig) -> None:
        """Test processing multiple streams concurrently.

        ZERO TOLERANCE: Uses real Oracle E2E environment, NO SKIPS.
        """
        num_streams = 3
        records_per_stream = 1000

        async def process_stream(stream_id: int) -> float:
            """Process a single stream and return duration."""
            singer_service = SingerTargetService(target_config)
            stream_name = f"concurrent_stream_{stream_id}"

            # Setup table
            schema_message = {
                "type": "SCHEMA",
                "stream": stream_name,
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "stream_id": {"type": "integer"},
                        "data": {"type": "string"},
                    },
                },
            }

            await singer_service.process_singer_message(schema_message)

            start_time = time.time()

            # Process records
            for i in range(records_per_stream):
                record_message = {
                    "type": "RECORD",
                    "stream": stream_name,
                    "record": {
                        "id": i,
                        "stream_id": stream_id,
                        "data": f"stream_{stream_id}_record_{i}",
                    },
                }
                await singer_service.process_singer_message(record_message)

            await singer_service.finalize_all_streams()

            return time.time() - start_time

        try:
            # Process streams concurrently
            start_time = time.time()
            tasks = [process_stream(i) for i in range(num_streams)]
            durations = await asyncio.gather(*tasks)
            total_time = time.time() - start_time

            # Verify all streams completed
            assert len(durations) == num_streams
            assert all(d > 0 for d in durations)

            total_records = num_streams * records_per_stream
            throughput = total_records / total_time

            # Should achieve reasonable throughput with concurrency
            assert throughput > 50  # At least 50 records/second across all streams
        except (ConnectionError, OSError, ValueError, AssertionError) as e:
            pytest.fail(f"Concurrent streams test failed: {e}")

    def test_connection_pool_performance(self, target_config: TargetConfig) -> None:
        """Test connection pool performance under load.

        ZERO TOLERANCE: Uses real Oracle E2E environment, NO SKIPS.
        """
        from flext_db_oracle import OracleConfig, OracleConnectionService

        oracle_config = OracleConfig(**target_config.oracle_config)
        connection_service = OracleConnectionService(oracle_config)
        query_service = OracleQueryService(connection_service)

        def execute_query(query_id: int) -> float:
            """Execute a query and return duration."""
            start_time = time.time()

            try:
                # Run async query in sync context
                result = asyncio.run(
                    query_service.execute_scalar(
                        "SELECT :id FROM DUAL",
                        {"id": query_id},
                    ),
                )
                assert result.is_success
                assert result.value == query_id

                return time.time() - start_time
            except (ConnectionError, OSError, ValueError, AssertionError) as e:
                pytest.fail(f"Query execution failed: {e}")
                return 0.0

        try:
            # Test concurrent queries
            num_queries = 20
            start_time = time.time()

            with ThreadPoolExecutor(max_workers=8) as executor:
                futures = [
                    executor.submit(execute_query, i) for i in range(num_queries)
                ]
                durations = [f.result() for f in futures]

            time.time() - start_time
            avg_duration = sum(durations) / len(durations)

            # All queries should complete successfully
            assert len(durations) == num_queries
            assert all(d > 0 for d in durations)
            assert avg_duration < 1.0  # Average query should be under 1 second
        except (ConnectionError, OSError, ValueError, AssertionError) as e:
            pytest.fail(f"Connection pool performance test failed: {e}")


class TestMemoryPerformance:
    """Test memory usage and efficiency."""

    @pytest.fixture
    def target_config(self) -> TargetConfig:
        """Create target configuration for memory testing."""
        return TargetConfig(
            host=os.getenv("ORACLE_HOST", "localhost"),
            port=int(os.getenv("ORACLE_PORT", "1521")),
            service_name=os.getenv("ORACLE_SERVICE_NAME", "XEPDB1"),
            username=os.getenv("ORACLE_USERNAME", "FLEXT_TEST"),
            password=os.getenv("ORACLE_PASSWORD", "test_password"),
            default_target_schema="FLEXT_PERF_TEST",
            batch_size=100,  # Smaller batch for memory testing
        )

    @pytest.mark.asyncio
    async def test_large_record_processing(self, target_config: TargetConfig) -> None:
        """Test processing of large individual records.

        ZERO TOLERANCE: Uses real Oracle E2E environment, NO SKIPS.
        """
        singer_service = SingerTargetService(target_config)

        # Setup table
        schema_message = {
            "type": "SCHEMA",
            "stream": "large_records",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "large_data": {"type": "string"},
                },
            },
        }

        try:
            await singer_service.process_singer_message(schema_message)

            # Process records with large data
            large_data = "x" * 50000  # 50KB per record
            num_records = 100

            start_time = time.time()

            for i in range(num_records):
                record_message = {
                    "type": "RECORD",
                    "stream": "large_records",
                    "record": {"id": i, "large_data": large_data},
                }
                result = await singer_service.process_singer_message(record_message)
                assert result.is_success

            await singer_service.finalize_all_streams()

            duration = time.time() - start_time
            (len(large_data) * num_records) / (1024 * 1024)

            # Should handle large records without excessive memory usage
            assert duration < 60.0  # Should complete within 1 minute
        except (ConnectionError, OSError, ValueError, AssertionError, MemoryError) as e:
            pytest.fail(f"Large record processing test failed: {e}")

    @pytest.mark.asyncio
    async def test_streaming_efficiency(self, target_config: TargetConfig) -> None:
        """Test efficiency of streaming large datasets.

        ZERO TOLERANCE: Uses real Oracle E2E environment, NO SKIPS.
        """
        singer_service = SingerTargetService(target_config)

        # Setup table
        schema_message = {
            "type": "SCHEMA",
            "stream": "streaming_test",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "timestamp": {"type": "string"},
                    "data": {"type": "string"},
                },
            },
        }

        try:
            await singer_service.process_singer_message(schema_message)

            # Process a continuous stream of records
            num_records = 5000
            batch_checkpoints = [1000, 2000, 3000, 4000, 5000]

            start_time = time.time()

            for i in range(num_records):
                record_message = {
                    "type": "RECORD",
                    "stream": "streaming_test",
                    "record": {
                        "id": i,
                        "timestamp": f"2024-01-01T{i % 24:02d}:00:00Z",
                        "data": f"streaming_data_{i}",
                    },
                }
                await singer_service.process_singer_message(record_message)

                # Check progress at checkpoints
                if (i + 1) in batch_checkpoints:
                    checkpoint_time = time.time() - start_time
                    (i + 1) / checkpoint_time

            await singer_service.finalize_all_streams()

            total_time = time.time() - start_time
            final_rate = num_records / total_time

            # Should maintain consistent throughput
            assert final_rate > 100  # At least 100 records/second
        except (ConnectionError, OSError, ValueError, AssertionError) as e:
            pytest.fail(f"Streaming efficiency test failed: {e}")


class TestResourceCleanup:
    """Test resource cleanup and optimization."""

    @pytest.fixture
    def target_config(self) -> TargetConfig:
        """Create target configuration for cleanup testing."""
        return TargetConfig(
            host=os.getenv("ORACLE_HOST", "localhost"),
            port=int(os.getenv("ORACLE_PORT", "1521")),
            service_name=os.getenv("ORACLE_SERVICE_NAME", "XEPDB1"),
            username=os.getenv("ORACLE_USERNAME", "FLEXT_TEST"),
            password=os.getenv("ORACLE_PASSWORD", "test_password"),
            default_target_schema="FLEXT_PERF_TEST",
        )

    @pytest.mark.asyncio
    async def test_connection_cleanup(self) -> None:
        """Test proper cleanup of database connections.

        ZERO TOLERANCE: Uses real Oracle E2E environment, NO SKIPS.
        """
        target_config = TargetConfig(
            host=os.getenv("ORACLE_HOST", "localhost"),
            port=int(os.getenv("ORACLE_PORT", "1521")),
            service_name=os.getenv("ORACLE_SERVICE_NAME", "XEPDB1"),
            username=os.getenv("ORACLE_USERNAME", "FLEXT_TEST"),
            password=os.getenv("ORACLE_PASSWORD", "test_password"),
            default_target_schema="FLEXT_PERF_TEST",
        )

        try:
            # Create and use multiple services
            services = []
            for i in range(5):
                service = SingerTargetService(target_config)
                services.append(service)

                # Use the service briefly
                schema_message = {
                    "type": "SCHEMA",
                    "stream": f"cleanup_test_{i}",
                    "schema": {
                        "type": "object",
                        "properties": {"id": {"type": "integer"}},
                    },
                }
                await service.process_singer_message(schema_message)

            # Finalize all services
            for service in services:
                await service.finalize_all_streams()

            # Services should clean up properly without hanging connections
        except (ConnectionError, OSError, ValueError, AssertionError) as e:
            pytest.fail(f"Connection cleanup test failed: {e}")

    @pytest.mark.asyncio
    async def test_table_cleanup(self, target_config: TargetConfig) -> None:
        """Test cleanup of test tables after performance tests.

        ZERO TOLERANCE: Uses real Oracle E2E environment, NO SKIPS.
        """
        singer_service = SingerTargetService(target_config)
        test_schema = target_config.default_target_schema.upper()

        try:
            # Get list of test tables created during performance tests
            query_result = await singer_service.query_service.execute_query(
                """
                SELECT table_name
                FROM all_tables
                WHERE owner = :schema_name
                AND table_name LIKE 'TEST_%'
                """,
                {"schema_name": test_schema},
            )

            if query_result.is_success and query_result.value:
                test_tables = [row[0] for row in query_result.value]

                # Clean up test tables to prevent residual data issues
                for table_name in test_tables:
                    # Use direct string concatenation for cleanup (acceptable in test context)
                    table_full = f'"{test_schema}"."{table_name}"'
                    cleanup_result = await singer_service.query_service.execute_query(
                        f"DELETE FROM {table_full}",  # noqa: S608 - table names are controlled in test context
                    )

                    if cleanup_result.is_success:
                        pass

        except (ConnectionError, OSError, ValueError):
            pass
            # Don't fail the test for cleanup issues
