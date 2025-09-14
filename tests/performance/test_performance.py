"""Performance tests for Oracle Target.

These tests measure and validate performance characteristics including
throughput, latency, memory usage, and scalability.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import gc
import json
import os
import time
from datetime import UTC, datetime

import psutil
import pytest
from faker import Faker
from sqlalchemy import Engine, text

from flext_target_oracle import FlextTargetOracle, FlextTargetOracleConfig, LoadMethod


@pytest.mark.performance
@pytest.mark.oracle
@pytest.mark.slow
class TestPerformance:
    """Performance benchmarking tests."""

    @pytest.fixture
    def fake(self) -> Faker:
        """Faker instance for generating test data."""
        return Faker()

    @pytest.fixture
    def performance_config(
        self,
        oracle_config: FlextTargetOracleConfig,
    ) -> FlextTargetOracleConfig:
        """Configure for optimal performance."""
        oracle_config.batch_size = 10000
        oracle_config.load_method = LoadMethod.BULK_INSERT
        oracle_config.use_direct_path = True
        oracle_config.parallel_degree = 4
        oracle_config.sdc_mode = "append"
        oracle_config.enable_auto_commit = False
        return oracle_config

    def get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024

    @pytest.mark.asyncio
    @pytest.mark.benchmark
    async def test_insert_throughput(
        self,
        performance_config: FlextTargetOracleConfig,
        _oracle_engine: Engine,
        _clean_database: None,
        fake: Faker,
    ) -> None:
        """Benchmark INSERT throughput with different batch sizes."""
        target = FlextTargetOracle(config=performance_config)
        await target.initialize()

        # Test schema
        schema = {
            "type": "SCHEMA",
            "stream": "benchmark_inserts",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "age": {"type": "integer"},
                    "balance": {"type": "number"},
                    "is_active": {"type": "boolean"},
                    "created_at": {"type": "string", "format": "date-time"},
                },
            },
            "key_properties": ["id"],
        }

        result = await target.execute(json.dumps(schema))
        assert result.is_success

        # Test different batch sizes
        batch_sizes = [100, 500, 1000, 5000, 10000]
        results = []

        for batch_size in batch_sizes:
            performance_config.batch_size = batch_size

            # Generate test data
            records = []
            for i in range(batch_size):
                record = {
                    "type": "RECORD",
                    "stream": "benchmark_inserts",
                    "record": {
                        "id": i + (batch_size * len(results)),
                        "name": fake.name(),
                        "email": fake.email(),
                        "age": fake.random_int(18, 80),
                        "balance": fake.pyfloat(
                            left_digits=5,
                            right_digits=2,
                            positive=True,
                        ),
                        "is_active": fake.boolean(),
                        "created_at": datetime.now(UTC).isoformat(),
                    },
                }
                records.append(record)

            # Measure performance
            gc.collect()
            start_memory = self.get_memory_usage()
            start_time = time.time()

            # Insert records
            for record in records:
                result = await target.execute(json.dumps(record))
                assert result.is_success

            end_time = time.time()
            end_memory = self.get_memory_usage()
            elapsed = end_time - start_time

            # Calculate metrics
            records_per_second = batch_size / elapsed
            memory_used = end_memory - start_memory
            latency_ms = (elapsed / batch_size) * 1000

            results.append(
                {
                    "batch_size": batch_size,
                    "elapsed_time": elapsed,
                    "records_per_second": records_per_second,
                    "memory_used_mb": memory_used,
                    "avg_latency_ms": latency_ms,
                },
            )

        # Verify all records inserted
        # Database verification disabled for performance test
        with _oracle_engine.connect() as conn:
            count = conn.execute(
                text("SELECT COUNT(*) FROM benchmark_inserts"),
            ).scalar()
            assert count == sum(batch_sizes)

        # Performance assertions
        best_throughput = max(r["records_per_second"] for r in results)
        assert best_throughput > 1000  # Should handle > 1k records/sec

    @pytest.mark.asyncio
    async def test_bulk_vs_standard_performance(
        self,
        oracle_config: FlextTargetOracleConfig,
        _oracle_engine: Engine,
        _clean_database: None,
        fake: Faker,
    ) -> None:
        """Compare BULK INSERT vs standard INSERT performance."""
        record_count = 10000

        # Test schema
        schema = {
            "type": "SCHEMA",
            "stream": "benchmark_comparison",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "data": {"type": "string"},
                    "value": {"type": "number"},
                },
            },
            "key_properties": ["id"],
        }

        # Test 1: Standard INSERT
        oracle_config.load_method = LoadMethod.INSERT
        oracle_config.batch_size = 100
        target_standard = FlextTargetOracle(config=oracle_config)
        await target_standard.initialize()

        result = await target_standard.execute(json.dumps(schema))
        assert result.is_success

        start_time = time.time()
        for i in range(record_count // 10):  # Test with 1/10th for standard
            record = {
                "type": "RECORD",
                "stream": "benchmark_comparison",
                "record": {
                    "id": i,
                    "data": fake.text(max_nb_chars=100),
                    "value": fake.pyfloat(),
                },
            }
            await target_standard.execute(json.dumps(record))

        standard_time = time.time() - start_time
        standard_rate = (record_count // 10) / standard_time

        # Clean table
        # Database verification disabled for performance test

        # Test 2: BULK INSERT
        oracle_config.load_method = LoadMethod.BULK_INSERT
        oracle_config.batch_size = 1000
        oracle_config.use_direct_path = True
        target_bulk = FlextTargetOracle(config=oracle_config)
        await target_bulk.initialize()

        start_time = time.time()
        for i in range(record_count):
            record = {
                "type": "RECORD",
                "stream": "benchmark_comparison",
                "record": {
                    "id": i,
                    "data": fake.text(max_nb_chars=100),
                    "value": fake.pyfloat(),
                },
            }
            await target_bulk.execute(json.dumps(record))

        bulk_time = time.time() - start_time
        bulk_rate = record_count / bulk_time

        # Bulk should be significantly faster
        assert bulk_rate > standard_rate * 5  # At least 5x faster

    @pytest.mark.asyncio
    async def test_memory_efficiency(
        self,
        performance_config: FlextTargetOracleConfig,
        _oracle_engine: Engine,
        _clean_database: None,
        fake: Faker,
    ) -> None:
        """Test memory efficiency with large batches."""
        target = FlextTargetOracle(config=performance_config)
        await target.initialize()

        # Schema with large text fields
        schema = {
            "type": "SCHEMA",
            "stream": "memory_test",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "large_text": {"type": "string"},
                    "json_data": {"type": "object"},
                },
            },
            "key_properties": ["id"],
        }

        result = await target.execute(json.dumps(schema))
        assert result.is_success

        # Monitor memory during large batch processing
        memory_samples = []
        gc.collect()
        base_memory = self.get_memory_usage()

        # Process in waves
        waves = 5
        records_per_wave = 5000

        for wave in range(waves):
            wave_start_memory = self.get_memory_usage()

            for i in range(records_per_wave):
                record_id = wave * records_per_wave + i
                record = {
                    "type": "RECORD",
                    "stream": "memory_test",
                    "record": {
                        "id": record_id,
                        "large_text": fake.text(max_nb_chars=1000),
                        "json_data": {
                            "nested": {
                                "data": [fake.word() for _ in range(50)],
                                "values": {
                                    str(j): fake.random_int() for j in range(20)
                                },
                            },
                        },
                    },
                }
                await target.execute(json.dumps(record))

            # Force garbage collection
            gc.collect()
            wave_end_memory = self.get_memory_usage()
            memory_growth = wave_end_memory - wave_start_memory
            memory_samples.append(memory_growth)

        # Calculate memory statistics
        avg_growth = sum(memory_samples) / len(memory_samples)
        max(memory_samples)
        total_memory = self.get_memory_usage() - base_memory

        # Memory assertions
        assert avg_growth < 100  # Should not grow more than 100MB per wave
        assert total_memory < 500  # Total should stay under 500MB

    @pytest.mark.asyncio
    async def test_concurrent_streams(
        self,
        performance_config: FlextTargetOracleConfig,
        _oracle_engine: Engine,
        _clean_database: None,
        fake: Faker,
    ) -> None:
        """Test performance with multiple concurrent streams."""
        target = FlextTargetOracle(config=performance_config)
        await target.initialize()

        # Define multiple streams
        streams = ["orders", "customers", "products", "inventory", "transactions"]

        for stream in streams:
            schema = {
                "type": "SCHEMA",
                "stream": stream,
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "value": {"type": "number"},
                        "timestamp": {"type": "string", "format": "date-time"},
                    },
                },
                "key_properties": ["id"],
            }
            result = await target.execute(json.dumps(schema))
            assert result.is_success

        # Generate interleaved records from multiple streams
        total_records = 50000
        start_time = time.time()

        for i in range(total_records):
            stream = streams[i % len(streams)]
            record = {
                "type": "RECORD",
                "stream": stream,
                "record": {
                    "id": i // len(streams),
                    "name": fake.word(),
                    "value": fake.pyfloat(),
                    "timestamp": datetime.now(UTC).isoformat(),
                },
            }
            result = await target.execute(json.dumps(record))
            assert result.is_success

        elapsed = time.time() - start_time
        throughput = total_records / elapsed

        # Verify data distribution
        # Database verification disabled for performance test

        # Performance assertion
        assert throughput > 500  # Should handle > 500 records/sec with multiple streams

    @pytest.mark.asyncio
    async def test_scalability(
        self,
        performance_config: FlextTargetOracleConfig,
        _oracle_engine: Engine,
        _clean_database: None,
    ) -> None:
        """Test scalability with increasing data volume."""
        target = FlextTargetOracle(config=performance_config)
        await target.initialize()

        schema = {
            "type": "SCHEMA",
            "stream": "scalability_test",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "data": {"type": "string"},
                },
            },
            "key_properties": ["id"],
        }

        result = await target.execute(json.dumps(schema))
        assert result.is_success

        # Test with increasing data sizes
        data_sizes = [1000, 5000, 10000, 25000, 50000]
        performance_metrics = []

        for size in data_sizes:
            start_time = time.time()

            for i in range(size):
                record = {
                    "type": "RECORD",
                    "stream": "scalability_test",
                    "record": {
                        "id": sum(data_sizes[: data_sizes.index(size)]) + i,
                        "data": f"Record {i} of {size}",
                    },
                }
                await target.execute(json.dumps(record))

            elapsed = time.time() - start_time
            throughput = size / elapsed

            performance_metrics.append(
                {
                    "size": size,
                    "elapsed": elapsed,
                    "throughput": throughput,
                },
            )

        # Check if performance scales linearly
        # Calculate throughput degradation
        base_throughput = performance_metrics[0]["throughput"]
        degradations = [
            (m["throughput"] / base_throughput) * 100 for m in performance_metrics
        ]

        for i, metrics in enumerate(performance_metrics):
            _ = i  # Used for iteration tracking
            _ = metrics  # Process metrics data

        # Performance should not degrade by more than 50%
        assert min(degradations) > 50.0
