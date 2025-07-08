"""Performance benchmark tests for Oracle target.

This module provides comprehensive performance testing including
throughput benchmarks, scalability tests, and resource utilization monitoring.
"""

from __future__ import annotations

import json
import logging
from io import StringIO
from typing import TYPE_CHECKING, Any
from unittest.mock import patch

import pytest
from sqlalchemy import text

from flext_target_oracle.target import OracleTarget
from tests.helpers import requires_oracle_connection

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine

log = logging.getLogger(__name__)


@requires_oracle_connection
class TestPerformanceBenchmarks:
    """Performance benchmark tests for Oracle target."""

    @pytest.mark.performance
    def test_high_throughput_ingestion(
        self,
        oracle_config: dict[str, Any],
        test_table_name: str,
        oracle_engine: Engine,
        table_cleanup: Any,
        performance_timer: Any,
    ) -> None:
        """Test high-throughput data ingestion performance."""
        table_cleanup(test_table_name)

        # Configure for maximum throughput
        perf_config = oracle_config.copy()
        perf_config["batch_size"] = 10000
        perf_config["max_workers"] = 8
        perf_config["use_bulk_operations"] = True
        perf_config["parallel_degree"] = 4
        perf_config["array_size"] = 2000

        target = OracleTarget(config=perf_config)

        # Create performance test schema
        perf_schema = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "timestamp": {"type": "string", "format": "date-time"},
                    "value": {"type": "number"},
                    "status": {"type": "string"},
                },
            },
            "key_properties": ["id"],
        }

        # Generate large dataset for throughput testing
        record_count = 50000
        perf_records = []

        for i in range(record_count):
            perf_records.append(
                {
                    "type": "RECORD",
                    "stream": test_table_name,
                    "record": {
                        "id": i + 1,
                        "name": f"User {i + 1}",
                        "email": f"user{i + 1}@example.com",
                        "timestamp": "2025-07-02T10:00:00Z",
                        "value": float(i * 1.5),
                        "status": "active" if i % 2 == 0 else "inactive",
                    },
                },
            )

        # Measure ingestion performance
        messages = [json.dumps(perf_schema)]
        messages.extend([json.dumps(record) for record in perf_records])
        input_data = "\n".join(messages)

        performance_timer.start()

        with patch("sys.stdin", StringIO(input_data)):
            target.cli()

        performance_timer.stop()

        # Verify all records were processed
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            count = row[0]
            assert count == record_count

        # Performance metrics
        duration = performance_timer.duration
        throughput = record_count / duration

        # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        log.error("\nPerformance Results:")
        log.error(
            f"Records processed: {record_count:,}",
        )  # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        log.error(
            f"Duration: {duration:.2f} seconds",
        )  # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        log.error(
            f"Throughput: {throughput:.2f} records/second",
        )  # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        log.error(
            f"Throughput: {throughput * 60:.2f} records/minute",
        )  # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo

        # Performance assertions
        assert (
            throughput > 1000
        ), f"Throughput too low: {
            throughput:.2f} records/sec"
        assert (
            duration < 120
        ), f"Processing took too long: {
            duration:.2f} seconds"

    @pytest.mark.performance
    def test_bulk_vs_individual_performance(
        self,
        oracle_config: dict[str, Any],
        test_table_name: str,
        oracle_engine: Engine,
        table_cleanup: Any,
        performance_timer: Any,
    ) -> None:
        """Compare bulk operations vs individual insert performance."""
        record_count = 10000

        # Test schema
        test_schema = {
            "type": "SCHEMA",
            "stream": test_table_name,
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

        # Generate test data
        test_records = []
        for i in range(record_count):
            test_records.append(
                {
                    "type": "RECORD",
                    "stream": test_table_name,
                    "record": {
                        "id": i + 1,
                        "data": f"Data item {i + 1}",
                        "value": float(i * 0.5),
                    },
                },
            )

        messages = [json.dumps(test_schema)]
        messages.extend([json.dumps(record) for record in test_records])
        "\n".join(messages)

        # Test 1: Bulk operations enabled
        table_cleanup(f"{test_table_name}_bulk")
        bulk_config = oracle_config.copy()
        bulk_config["use_bulk_operations"] = True
        bulk_config["batch_size"] = 5000

        bulk_schema = test_schema.copy()
        bulk_schema["stream"] = f"{test_table_name}_bulk"
        bulk_records = []
        for record in test_records:
            bulk_record = record.copy()
            bulk_record["stream"] = f"{test_table_name}_bulk"
            bulk_records.append(bulk_record)

        bulk_messages = [json.dumps(bulk_schema)]
        bulk_messages.extend([json.dumps(record) for record in bulk_records])
        bulk_input = "\n".join(bulk_messages)

        target_bulk = OracleTarget(config=bulk_config)

        performance_timer.start()
        with patch("sys.stdin", StringIO(bulk_input)):
            target_bulk.cli()
        performance_timer.stop()

        bulk_duration = performance_timer.duration
        bulk_throughput = record_count / bulk_duration

        # Test 2: Individual operations
        table_cleanup(f"{test_table_name}_individual")
        individual_config = oracle_config.copy()
        individual_config["use_bulk_operations"] = False
        individual_config["batch_size"] = 1

        individual_schema = test_schema.copy()
        individual_schema["stream"] = f"{test_table_name}_individual"
        individual_records = []
        for record in test_records:
            individual_record = record.copy()
            individual_record["stream"] = f"{test_table_name}_individual"
            individual_records.append(individual_record)

        individual_messages = [json.dumps(individual_schema)]
        individual_messages.extend(
            [json.dumps(record) for record in individual_records],
        )
        individual_input = "\n".join(individual_messages)

        target_individual = OracleTarget(config=individual_config)

        performance_timer.start()
        with patch("sys.stdin", StringIO(individual_input)):
            target_individual.cli()
        performance_timer.stop()

        individual_duration = performance_timer.duration
        individual_throughput = record_count / individual_duration

        # Verify both processed correctly
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}_bulk"))
            row = result.fetchone()
            assert row is not None
            assert row[0] == record_count

            result = conn.execute(
                text(f"SELECT COUNT(*) FROM {test_table_name}_individual"),
            )
            row = result.fetchone()
            assert row is not None
            assert row[0] == record_count

        # Performance comparison
        performance_ratio = bulk_throughput / individual_throughput

        log.error(
            "\nBulk vs Individual Performance:",
        )  # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        log.error(
            f"Bulk operations: {bulk_throughput:.2f} records/sec ({bulk_duration:.2f}s)"
            # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        )
        log.error(
            f"Individual operations: {individual_throughput:.2f} records/sec "
            f"({individual_duration:.2f}s)"
            # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        )
        log.error(
            f"Bulk is {performance_ratio:.1f}x faster",
        )  # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo

        # Bulk should be significantly faster
        assert (
            performance_ratio > 2.0
        ), f"Bulk operations not sufficiently faster: {performance_ratio:.2f}x"

        # Cleanup
        table_cleanup(f"{test_table_name}_bulk")
        table_cleanup(f"{test_table_name}_individual")

    @pytest.mark.performance
    def test_parallel_degree_scaling(
        self,
        oracle_config: dict[str, Any],
        test_table_name: str,
        oracle_engine: Engine,
        table_cleanup: Any,
        performance_timer: Any,
    ) -> None:
        """Test performance scaling with different parallel degrees."""
        record_count = 20000

        # Test schema
        test_schema = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "category": {"type": "string"},
                    "amount": {"type": "number"},
                    "description": {"type": "string"},
                },
            },
            "key_properties": ["id"],
        }

        # Generate test data
        test_records = []
        for i in range(record_count):
            test_records.append(
                {
                    "type": "RECORD",
                    "stream": test_table_name,
                    "record": {
                        "id": i + 1,
                        "category": f"Category {(i % 5) + 1}",
                        "amount": float(i * 2.5),
                        "description": (
                            f"Description for record {
                                i + 1} with some text data"
                        ),
                    },
                },
            )

        # Test different parallel degrees
        parallel_degrees = [1, 2, 4]
        results = {}

        for degree in parallel_degrees:
            table_name = f"{test_table_name}_parallel_{degree}"
            table_cleanup(table_name)

            # Configure for this parallel degree
            parallel_config = oracle_config.copy()
            parallel_config["parallel_degree"] = degree
            parallel_config["max_workers"] = degree * 2
            parallel_config["use_bulk_operations"] = True
            parallel_config["batch_size"] = 2000

            target = OracleTarget(config=parallel_config)

            # Prepare messages for this test
            parallel_schema = test_schema.copy()
            parallel_schema["stream"] = table_name

            parallel_records = []
            for record in test_records:
                parallel_record = record.copy()
                parallel_record["stream"] = table_name
                parallel_records.append(parallel_record)

            messages = [json.dumps(parallel_schema)]
            messages.extend([json.dumps(record) for record in parallel_records])
            input_data = "\n".join(messages)

            # Measure performance
            performance_timer.start()

            with patch("sys.stdin", StringIO(input_data)):
                target.cli()

            performance_timer.stop()

            duration = performance_timer.duration
            throughput = record_count / duration
            results[degree] = {"duration": duration, "throughput": throughput}

            # Verify processing
            with oracle_engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                row = result.fetchone()
            assert row is not None
            assert row[0] == record_count

            log.error(
                f"Parallel degree {degree}: {throughput:.2f} records/sec "
                # Link: https://github.com/issue/todo
                f"({duration:.2f}s)  # TODO(@dev): Replace with proper logging",
            )

            # Cleanup
            table_cleanup(table_name)

        # Analyze scaling
        log.error(
            "\nParallel Degree Scaling Results:",
        )  # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        baseline_throughput = results[1]["throughput"]

        for degree in parallel_degrees:
            scaling_factor = results[degree]["throughput"] / baseline_throughput
            log.error(
                f"Degree {degree}: {
                    scaling_factor:.2f}x baseline performance",
            )  # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo

        # Higher parallel degrees should generally perform better
        assert (
            results[2]["throughput"] >= results[1]["throughput"] * 0.8
        ), "Degree 2 performance regression"
        assert (
            results[4]["throughput"] >= results[1]["throughput"] * 0.6
        ), "Degree 4 significant regression"

    @pytest.mark.performance
    def test_memory_usage_scaling(
        self,
        oracle_config: dict[str, Any],
        test_table_name: str,
        oracle_engine: Engine,
        table_cleanup: Any,
        performance_timer: Any,
    ) -> None:
        """Test memory usage with different batch sizes."""
        # Test different batch sizes
        batch_sizes = [1000, 5000, 10000]
        record_count = 30000

        # Test schema with moderate data size
        test_schema = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "text_data": {"type": "string"},
                    "numeric_data": {"type": "number"},
                },
            },
            "key_properties": ["id"],
        }

        # Generate test data
        test_records = []
        for i in range(record_count):
            test_records.append(
                {
                    "type": "RECORD",
                    "stream": test_table_name,
                    "record": {
                        "id": i + 1,
                        "name": f"User {i + 1}",
                        "text_data": "Sample text data " * 10,  # ~200 bytes
                        "numeric_data": float(i * 1.234),
                    },
                },
            )

        batch_results = {}

        for batch_size in batch_sizes:
            table_name = f"{test_table_name}_batch_{batch_size}"
            table_cleanup(table_name)

            # Configure for this batch size
            batch_config = oracle_config.copy()
            batch_config["batch_size"] = batch_size
            batch_config["use_bulk_operations"] = True

            target = OracleTarget(config=batch_config)

            # Prepare messages
            batch_schema = test_schema.copy()
            batch_schema["stream"] = table_name

            batch_records = []
            for record in test_records:
                batch_record = record.copy()
                batch_record["stream"] = table_name
                batch_records.append(batch_record)

            messages = [json.dumps(batch_schema)]
            messages.extend([json.dumps(record) for record in batch_records])
            input_data = "\n".join(messages)

            # Measure performance
            performance_timer.start()

            with patch("sys.stdin", StringIO(input_data)):
                target.cli()

            performance_timer.stop()

            duration = performance_timer.duration
            throughput = record_count / duration
            batch_results[batch_size] = {"duration": duration, "throughput": throughput}

            # Verify processing
            with oracle_engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                row = result.fetchone()
            assert row is not None
            assert row[0] == record_count

            log.error(
                f"Batch size {batch_size}: {throughput:.2f} records/sec "
                # Link: https://github.com/issue/todo
                f"({duration:.2f}s)  # TODO(@dev): Replace with proper logging",
            )

            # Cleanup
            table_cleanup(table_name)

        # Analyze batch size scaling
        # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        log.error("\nBatch Size Scaling Results:")
        for batch_size in batch_sizes:
            batch_result = batch_results[batch_size]
            efficiency = (
                batch_result["throughput"] / batch_size
            )  # Records per second per batch item
            log.error(
                f"Batch {batch_size}: {batch_result['throughput']:.2f} records/sec "
                # Link: https://github.com/issue/todo
                f"(efficiency: {efficiency:.4f})  "
                "# TODO(@dev): Replace with proper logging",
            )

        # Larger batch sizes should generally be more efficient
        assert (
            batch_results[5000]["throughput"] >= batch_results[1000]["throughput"] * 0.8
        )
        assert (
            batch_results[10000]["throughput"]
            >= batch_results[1000]["throughput"] * 0.6
        )

    @pytest.mark.performance
    def test_connection_pool_performance(
        self,
        oracle_config: dict[str, Any],
        test_table_name: str,
        oracle_engine: Engine,
        table_cleanup: Any,
        performance_timer: Any,
    ) -> None:
        """Test performance impact of connection pool settings."""
        record_count = 15000

        # Test schema
        test_schema = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "worker_id": {"type": "integer"},
                    "data": {"type": "string"},
                },
            },
            "key_properties": ["id"],
        }

        # Test different pool configurations
        pool_configs = [
            {"pool_size": 5, "max_overflow": 5, "max_workers": 2},
            {"pool_size": 10, "max_overflow": 10, "max_workers": 4},
            {"pool_size": 15, "max_overflow": 15, "max_workers": 6},
        ]

        pool_results = {}

        for i, pool_config in enumerate(pool_configs):
            table_name = f"{test_table_name}_pool_{i + 1}"
            table_cleanup(table_name)

            # Configure for this pool setup
            config = oracle_config.copy()
            config.update(pool_config)
            config["batch_size"] = 2000
            config["use_bulk_operations"] = True

            target = OracleTarget(config=config)

            # Generate test data
            test_records = []
            for j in range(record_count):
                test_records.append(
                    {
                        "type": "RECORD",
                        "stream": table_name,
                        "record": {
                            "id": j + 1,
                            "worker_id": (j % pool_config["max_workers"]) + 1,
                            "data": (
                                f"Data item {j + 1} for worker "
                                f"{(j % pool_config['max_workers']) + 1}"
                            ),
                        },
                    },
                )

            # Prepare messages
            pool_schema = test_schema.copy()
            pool_schema["stream"] = table_name

            messages = [json.dumps(pool_schema)]
            messages.extend([json.dumps(record) for record in test_records])
            input_data = "\n".join(messages)

            # Measure performance
            performance_timer.start()

            with patch("sys.stdin", StringIO(input_data)):
                target.cli()

            performance_timer.stop()

            duration = performance_timer.duration
            throughput = record_count / duration
            pool_results[i] = {
                "config": pool_config,
                "duration": duration,
                "throughput": throughput,
            }

            # Verify processing
            with oracle_engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                row = result.fetchone()
            assert row is not None
            assert row[0] == record_count

            config_desc = f"Pool:{
                    pool_config['pool_size']}, Workers:{
                    pool_config['max_workers']}"
            log.error(
                f"{config_desc}: {
    throughput:.2f} records/sec ({
        duration:.2f}s)  # TODO(@dev): Replace with proper logging",
          # Link: https://github.com/issue/todo
            )

            # Cleanup
            table_cleanup(table_name)

        # Analyze pool scaling
        log.error(
            "\nConnection Pool Performance Results:",
        )  # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        for _i, pool_result in pool_results.items():
            config = pool_result["config"]
            log.error(
                f"Pool {config['pool_size']}/Workers {config['max_workers']}: "
                f"{pool_result['throughput']:.2f} records/sec",
            )  # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo

        # Verify reasonable performance scaling
        baseline = pool_results[0]["throughput"]
        for i in range(1, len(pool_results)):
            scaling = pool_results[i]["throughput"] / baseline
            assert scaling >= 0.5, (
                f"Pool config {_i} shows significant performance regression: "
                f"{scaling:.2f}x"
            )

    @pytest.mark.performance
    def test_large_record_handling(
        self,
        oracle_config: dict[str, Any],
        test_table_name: str,
        oracle_engine: Engine,
        table_cleanup: Any,
        performance_timer: Any,
    ) -> None:
        """Test performance with large individual records."""
        table_cleanup(test_table_name)

        # Configure for large records
        large_config = oracle_config.copy()
        large_config["batch_size"] = 500  # Smaller batches for large records
        large_config["use_bulk_operations"] = True

        target = OracleTarget(config=large_config)

        # Create schema for large records
        large_schema = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "large_text": {"type": "string"},
                    "metadata": {"type": "object"},
                    "description": {"type": "string"},
                },
            },
            "key_properties": ["id"],
        }

        # Generate large records (each ~10KB)
        record_count = 2000
        large_records = []

        for i in range(record_count):
            large_text = "Large text content " * 500  # ~10KB
            metadata = {
                "tags": ["tag" + str(j) for j in range(100)],
                "attributes": {f"attr_{j}": f"value_{j}" for j in range(50)},
                "history": [
                    {"event": f"event_{j}", "timestamp": "2025-07-02T10:00:00Z"}
                    for j in range(20)
                ],
            }

            large_records.append(
                {
                    "type": "RECORD",
                    "stream": test_table_name,
                    "record": {
                        "id": i + 1,
                        "large_text": large_text,
                        "metadata": metadata,
                        "description": (
                            f"Large record {i + 1} with extensive content "
                            f"for performance testing"
                        ),
                    },
                },
            )

        # Process large records
        messages = [json.dumps(large_schema)]
        messages.extend([json.dumps(record) for record in large_records])
        input_data = "\n".join(messages)

        performance_timer.start()

        with patch("sys.stdin", StringIO(input_data)):
            target.cli()

        performance_timer.stop()

        # Verify processing
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            count = row[0]
            assert count == record_count

        # Performance metrics for large records
        duration = performance_timer.duration
        throughput = record_count / duration
        # Approximate data size in MB
        data_size_mb = (record_count * 10) / 1024
        mb_per_second = data_size_mb / duration

        # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        log.error("\nLarge Record Performance:")
        log.error(
            f"Records: {record_count:,} (~10KB each)"
            # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        )
        log.error(
            f"Total data: ~{data_size_mb:.1f} MB",
        )  # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        log.error(
            f"Duration: {duration:.2f} seconds",
        )  # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        log.error(
            f"Throughput: {throughput:.2f} records/second",
        )  # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        log.error(
            f"Data rate: {mb_per_second:.2f} MB/second",
        )  # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo

        # Performance assertions for large records
        assert (
            throughput > 50
        ), f"Large record throughput too low: {throughput:.2f} records/sec"
        assert (
            mb_per_second > 2
        ), f"Data rate too low: {
            mb_per_second:.2f} MB/sec"
