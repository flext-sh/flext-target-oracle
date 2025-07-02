"""
Comprehensive bulk operations and performance optimization tests.

These tests validate high-volume data loading scenarios, parallel processing,
and performance optimizations with real Oracle database connections.
"""

from __future__ import annotations

import json
import random
import time
from datetime import datetime, timedelta
from io import StringIO
from typing import TYPE_CHECKING, Any

import pytest
from sqlalchemy import text

from flext_target_oracle.target import OracleTarget

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine


@pytest.mark.integration
@pytest.mark.performance
class TestBulkOperations:
    """Test bulk operations and performance optimizations."""

    def test_large_batch_insert_performance(
        self,
        oracle_config: dict[str, Any],
        oracle_engine: Engine,
        test_table_name: str,
        table_cleanup,
        performance_timer,
    ):
        """Test large batch insert performance with 10k+ records."""
        table_cleanup(test_table_name)

        # Generate large dataset
        record_count = 10000

        # Create target with optimized bulk configuration
        config = oracle_config.copy()
        config.update(
            {
                "load_method": "append-only",
                "batch_size": 5000,
                "use_bulk_operations": True,
                "use_append_values_hint": True,
                "parallel_degree": 4,
                "array_size": 1000,
                "prefetch_rows": 500,
                "use_insertmanyvalues": True,
                "insertmanyvalues_page_size": 1000,
                "skip_table_optimization": True,  # Skip advanced features for this test
            }
        )
        oracle_target = OracleTarget(config=config)

        # Create schema
        schema_message = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string", "maxLength": 100},
                    "description": {"type": "string", "maxLength": 500},
                    "score": {"type": "number"},
                    "active": {"type": "boolean"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "metadata": {"type": "object"},
                },
            },
            "key_properties": ["id"],
        }

        # Generate bulk records
        base_time = datetime.now()
        record_messages = []

        for i in range(record_count):
            record_time = base_time + timedelta(seconds=i)
            record = {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": i + 1,
                    "name": f"Bulk Test User {i + 1}",
                    "description": f"Test description for user {i + 1} "
                    * random.randint(1, 5),
                    "score": round(random.uniform(0, 100), 2),
                    "active": random.choice([True, False]),
                    "created_at": record_time.isoformat() + "Z",
                    "metadata": {
                        "batch": i // 1000,
                        "source": "bulk_test",
                        "priority": random.choice(["high", "medium", "low"]),
                    },
                },
                "time_extracted": record_time.isoformat() + "Z",
            }
            record_messages.append(record)

        # Create input stream
        messages = [schema_message] + record_messages
        input_lines = [json.dumps(msg) + "\n" for msg in messages]
        input_stream = StringIO("".join(input_lines))

        # Measure performance
        performance_timer.start()
        oracle_target.process_lines(input_stream)
        performance_timer.stop()

        # Verify all records were loaded
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            count = result.scalar()
            assert (
                count == record_count
            ), f"Expected {record_count} records, found {count}"

            # Verify data sampling
            result = conn.execute(
                text(f"""
                SELECT id, name, score, active
                FROM {test_table_name}
                WHERE id IN (1, 5000, 10000)
                ORDER BY id
            """)
            )
            rows = result.fetchall()
            assert len(rows) >= 2, "Sample records not found"

        # Performance validation
        throughput = record_count / performance_timer.duration
        print(f"Large batch performance: {throughput:.0f} records/second")
        print(f"Total time: {performance_timer.duration:.2f}s")

        # Should achieve reasonable throughput (adjust based on your Oracle setup)
        assert throughput > 100, f"Throughput too low: {throughput:.0f} records/second"
        assert (
            performance_timer.duration < 120
        ), f"Load took too long: {performance_timer.duration:.2f}s"

    def test_parallel_processing_performance(
        self,
        oracle_config: dict[str, Any],
        oracle_engine: Engine,
        test_table_name: str,
        table_cleanup,
        performance_timer,
    ):
        """Test parallel processing with multiple threads."""
        table_cleanup(test_table_name)

        # Create target with parallel processing
        config = oracle_config.copy()
        config.update(
            {
                "load_method": "append-only",
                "batch_size": 2000,
                "parallel_threads": 4,
                "chunk_size": 1000,
                "use_bulk_operations": True,
                "skip_table_optimization": True,
            }
        )
        oracle_target = OracleTarget(config=config)

        # Generate dataset for parallel processing
        record_count = 8000  # Will be split into 4 chunks of 2000 each

        schema_message = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "thread_id": {"type": "integer"},
                    "data": {"type": "string", "maxLength": 200},
                    "timestamp": {"type": "string", "format": "date-time"},
                },
            },
            "key_properties": ["id"],
        }

        record_messages = []
        for i in range(record_count):
            record = {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": i + 1,
                    "thread_id": (i % 4) + 1,  # Distribute across 4 threads
                    "data": f"Parallel data chunk {i + 1}",
                    "timestamp": datetime.now().isoformat() + "Z",
                },
                "time_extracted": datetime.now().isoformat() + "Z",
            }
            record_messages.append(record)

        # Process with parallel execution
        messages = [schema_message] + record_messages
        input_lines = [json.dumps(msg) + "\n" for msg in messages]
        input_stream = StringIO("".join(input_lines))

        performance_timer.start()
        oracle_target.process_lines(input_stream)
        performance_timer.stop()

        # Verify results
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            count = result.scalar()
            assert (
                count == record_count
            ), f"Expected {record_count} records, found {count}"

            # Verify data distribution across threads
            result = conn.execute(
                text(f"""
                SELECT thread_id, COUNT(*)
                FROM {test_table_name}
                GROUP BY thread_id
                ORDER BY thread_id
            """)
            )
            thread_counts = dict(result.fetchall())

            # Each thread should have processed approximately equal amounts
            expected_per_thread = record_count // 4
            for thread_id in range(1, 5):
                assert thread_id in thread_counts, f"Thread {thread_id} data not found"
                assert (
                    thread_counts[thread_id] == expected_per_thread
                ), f"Thread {thread_id}: expected {expected_per_thread}, got {thread_counts[thread_id]}"

        throughput = record_count / performance_timer.duration
        print(f"Parallel processing performance: {throughput:.0f} records/second")

    def test_upsert_performance_large_dataset(
        self,
        oracle_config: dict[str, Any],
        oracle_engine: Engine,
        test_table_name: str,
        table_cleanup,
        performance_timer,
    ):
        """Test MERGE (upsert) performance with large dataset."""
        table_cleanup(test_table_name)

        # Create target with upsert configuration
        config = oracle_config.copy()
        config.update(
            {
                "load_method": "upsert",
                "batch_size": 3000,
                "merge_batch_size": 1000,
                "use_merge_statements": True,
                "use_merge_hint": True,
                "skip_table_optimization": True,
            }
        )
        oracle_target = OracleTarget(config=config)

        # Schema with key for upsert
        schema_message = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer"},
                    "username": {"type": "string", "maxLength": 50},
                    "email": {"type": "string", "maxLength": 100},
                    "last_login": {"type": "string", "format": "date-time"},
                    "login_count": {"type": "integer"},
                },
            },
            "key_properties": ["user_id"],
        }

        # Initial load - 5000 records
        initial_count = 5000
        initial_messages = []

        for i in range(initial_count):
            record = {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "user_id": i + 1,
                    "username": f"user_{i + 1}",
                    "email": f"user_{i + 1}@example.com",
                    "last_login": datetime.now().isoformat() + "Z",
                    "login_count": 1,
                },
                "time_extracted": datetime.now().isoformat() + "Z",
            }
            initial_messages.append(record)

        # Process initial load
        messages = [schema_message] + initial_messages
        input_lines = [json.dumps(msg) + "\n" for msg in messages]
        input_stream = StringIO("".join(input_lines))
        oracle_target.process_lines(input_stream)

        # Verify initial load
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            count = result.scalar()
            assert (
                count == initial_count
            ), f"Initial load failed: expected {initial_count}, got {count}"

        # Upsert load - update existing + add new records
        update_messages = []

        # Update first 3000 records (increase login count)
        for i in range(3000):
            record = {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "user_id": i + 1,
                    "username": f"user_{i + 1}",
                    "email": f"user_{i + 1}@example.com",
                    "last_login": (datetime.now() + timedelta(hours=1)).isoformat()
                    + "Z",
                    "login_count": 2,  # Updated
                },
                "time_extracted": datetime.now().isoformat() + "Z",
            }
            update_messages.append(record)

        # Add 2000 new records
        for i in range(initial_count, initial_count + 2000):
            record = {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "user_id": i + 1,
                    "username": f"user_{i + 1}",
                    "email": f"user_{i + 1}@example.com",
                    "last_login": datetime.now().isoformat() + "Z",
                    "login_count": 1,
                },
                "time_extracted": datetime.now().isoformat() + "Z",
            }
            update_messages.append(record)

        # Process upsert
        input_lines = [json.dumps(msg) + "\n" for msg in update_messages]
        input_stream = StringIO("".join(input_lines))

        performance_timer.start()
        oracle_target.process_lines(input_stream)
        performance_timer.stop()

        # Verify upsert results
        with oracle_engine.connect() as conn:
            # Total count should be 7000 (5000 initial + 2000 new)
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            total_count = result.scalar()
            expected_total = initial_count + 2000
            assert (
                total_count == expected_total
            ), f"Expected {expected_total} total records, got {total_count}"

            # Check updated records
            result = conn.execute(
                text(f"""
                SELECT COUNT(*) FROM {test_table_name}
                WHERE user_id <= 3000 AND login_count = 2
            """)
            )
            updated_count = result.scalar()
            assert (
                updated_count == 3000
            ), f"Expected 3000 updated records, got {updated_count}"

            # Check new records
            result = conn.execute(
                text(f"""
                SELECT COUNT(*) FROM {test_table_name}
                WHERE user_id > {initial_count}
            """)
            )
            new_count = result.scalar()
            assert new_count == 2000, f"Expected 2000 new records, got {new_count}"

        throughput = (
            3000 + 2000
        ) / performance_timer.duration  # Total processed records
        print(f"Upsert performance: {throughput:.0f} records/second")

    def test_memory_efficient_streaming(
        self,
        oracle_config: dict[str, Any],
        oracle_engine: Engine,
        test_table_name: str,
        table_cleanup,
    ):
        """Test memory-efficient streaming for very large datasets."""
        table_cleanup(test_table_name)

        # Create target with streaming configuration
        config = oracle_config.copy()
        config.update(
            {
                "load_method": "append-only",
                "batch_size": 1000,  # Smaller batches for memory efficiency
                "stream_results": True,
                "max_memory_usage_mb": 512,
                "skip_table_optimization": True,
            }
        )
        oracle_target = OracleTarget(config=config)

        # Schema for streaming test
        schema_message = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "large_text": {"type": "string", "maxLength": 2000},
                    "json_data": {"type": "object"},
                },
            },
            "key_properties": ["id"],
        }

        # Generate records with larger data
        record_count = 5000
        record_messages = []

        for i in range(record_count):
            # Create large text data
            large_text = (
                f"Large text data for record {i + 1}. " * 50
            )  # ~1.5KB per record

            record = {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": i + 1,
                    "large_text": large_text,
                    "json_data": {
                        "record_id": i + 1,
                        "metadata": {"batch": i // 1000, "size": "large"},
                        "tags": [f"tag_{j}" for j in range(10)],
                        "description": f"JSON metadata for record {i + 1}",
                    },
                },
                "time_extracted": datetime.now().isoformat() + "Z",
            }
            record_messages.append(record)

        # Process in streaming fashion
        messages = [schema_message] + record_messages
        input_lines = [json.dumps(msg) + "\n" for msg in messages]
        input_stream = StringIO("".join(input_lines))

        oracle_target.process_lines(input_stream)

        # Verify streaming results
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            count = result.scalar()
            assert (
                count == record_count
            ), f"Expected {record_count} records, found {count}"

            # Verify large data was stored correctly
            result = conn.execute(
                text(f"""
                SELECT id, LENGTH(large_text), json_data
                FROM {test_table_name}
                WHERE id IN (1, 2500, 5000)
                ORDER BY id
            """)
            )
            rows = result.fetchall()
            assert len(rows) == 3, "Sample records not found"

            for row in rows:
                # Large text should be around 1500 characters
                assert row[1] > 1000, f"Large text too small: {row[1]} characters"

                # JSON data should be valid
                json_data = json.loads(row[2])
                assert "record_id" in json_data, "JSON data corrupted"
                assert json_data["record_id"] == row[0], "JSON data mismatch"

    def test_connection_pool_efficiency(
        self,
        oracle_config: dict[str, Any],
        oracle_engine: Engine,
        test_table_name: str,
        table_cleanup,
    ):
        """Test connection pool efficiency under load."""
        table_cleanup(test_table_name)

        # Create target with optimized pool settings
        config = oracle_config.copy()
        config.update(
            {
                "load_method": "append-only",
                "pool_size": 5,
                "max_overflow": 10,
                "pool_pre_ping": True,
                "pool_recycle": 3600,
                "batch_size": 2000,
                "skip_table_optimization": True,
            }
        )

        # Process multiple smaller loads to test pool efficiency
        schema_message = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "batch_num": {"type": "integer"},
                    "data": {"type": "string", "maxLength": 100},
                },
            },
            "key_properties": ["id"],
        }

        total_records = 0
        num_batches = 5
        records_per_batch = 1000

        for batch_num in range(num_batches):
            oracle_target = OracleTarget(config=config)

            record_messages = []
            for i in range(records_per_batch):
                record_id = batch_num * records_per_batch + i + 1
                record = {
                    "type": "RECORD",
                    "stream": test_table_name,
                    "record": {
                        "id": record_id,
                        "batch_num": batch_num + 1,
                        "data": f"Batch {batch_num + 1} Record {i + 1}",
                    },
                    "time_extracted": datetime.now().isoformat() + "Z",
                }
                record_messages.append(record)

            # Process batch
            if batch_num == 0:
                messages = [schema_message] + record_messages
            else:
                messages = record_messages

            input_lines = [json.dumps(msg) + "\n" for msg in messages]
            input_stream = StringIO("".join(input_lines))

            oracle_target.process_lines(input_stream)
            total_records += records_per_batch

            # Small delay between batches
            time.sleep(0.1)

        # Verify all batches were processed
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            count = result.scalar()
            assert (
                count == total_records
            ), f"Expected {total_records} records, found {count}"

            # Verify batch distribution
            result = conn.execute(
                text(f"""
                SELECT batch_num, COUNT(*)
                FROM {test_table_name}
                GROUP BY batch_num
                ORDER BY batch_num
            """)
            )
            batch_counts = dict(result.fetchall())

            for batch_num in range(1, num_batches + 1):
                assert batch_num in batch_counts, f"Batch {batch_num} not found"
                assert (
                    batch_counts[batch_num] == records_per_batch
                ), f"Batch {batch_num}: expected {records_per_batch}, got {batch_counts[batch_num]}"

    def test_error_recovery_bulk_operations(
        self,
        oracle_config: dict[str, Any],
        oracle_engine: Engine,
        test_table_name: str,
        table_cleanup,
    ):
        """Test error recovery during bulk operations."""
        table_cleanup(test_table_name)

        # Create target with error recovery settings
        config = oracle_config.copy()
        config.update(
            {
                "load_method": "append-only",
                "batch_size": 1000,
                "max_retries": 3,
                "retry_delay": 0.5,
                "retry_backoff": 1.5,
                "fail_fast": False,
                "skip_table_optimization": True,
            }
        )
        oracle_target = OracleTarget(config=config)

        schema_message = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string", "maxLength": 50},
                    "category": {"type": "string", "maxLength": 20},
                },
            },
            "key_properties": ["id"],
        }

        # Create mix of valid and potentially problematic records
        record_messages = []
        valid_record_count = 0

        for i in range(2000):
            if i % 500 == 0 and i > 0:
                # Every 500th record has potential issue (very long name)
                record = {
                    "type": "RECORD",
                    "stream": test_table_name,
                    "record": {
                        "id": i + 1,
                        "name": "A" * 100,  # Exceeds maxLength of 50
                        "category": "problematic",
                    },
                    "time_extracted": datetime.now().isoformat() + "Z",
                }
            else:
                # Normal valid record
                record = {
                    "type": "RECORD",
                    "stream": test_table_name,
                    "record": {
                        "id": i + 1,
                        "name": f"User {i + 1}",
                        "category": random.choice(["standard", "premium", "basic"]),
                    },
                    "time_extracted": datetime.now().isoformat() + "Z",
                }
                valid_record_count += 1

            record_messages.append(record)

        # Process with error recovery
        messages = [schema_message] + record_messages
        input_lines = [json.dumps(msg) + "\n" for msg in messages]
        input_stream = StringIO("".join(input_lines))

        try:
            oracle_target.process_lines(input_stream)
        except Exception as e:
            print(f"Processing completed with expected errors: {e}")

        # Verify that valid records were processed despite errors
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            count = result.scalar()

            # Should have most of the valid records
            assert (
                count >= valid_record_count * 0.8
            ), f"Too few records processed: {count}/{valid_record_count}"

            # Verify data quality
            result = conn.execute(
                text(f"""
                SELECT category, COUNT(*)
                FROM {test_table_name}
                GROUP BY category
            """)
            )
            categories = dict(result.fetchall())

            # Should have the valid categories
            expected_categories = ["standard", "premium", "basic"]
            for cat in expected_categories:
                assert cat in categories, f"Category {cat} not found"
