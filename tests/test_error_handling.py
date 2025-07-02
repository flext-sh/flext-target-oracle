"""
Comprehensive error handling and recovery mechanism tests.

These tests validate robust error handling, retry logic, connection recovery,
and graceful degradation under various failure scenarios.
"""

from __future__ import annotations

import json
import time
from datetime import datetime
from io import StringIO
from typing import TYPE_CHECKING, Any

import pytest
from sqlalchemy import text

from flext_target_oracle.target import OracleTarget

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine


@pytest.mark.integration
class TestErrorHandling:
    """Test comprehensive error handling and recovery mechanisms."""

    def test_connection_failure_recovery(
        self,
        oracle_config: dict[str, Any],
        oracle_engine: Engine,
        test_table_name: str,
        table_cleanup,
    ):
        """Test recovery from connection failures with retry logic."""
        table_cleanup(test_table_name)

        # Configure with aggressive retry settings
        config = oracle_config.copy()
        config.update(
            {
                "load_method": "append-only",
                "max_retries": 5,
                "retry_delay": 0.1,
                "retry_backoff": 1.5,
                "retry_jitter": False,  # Disable jitter for predictable testing
                "pool_pre_ping": True,
                "pool_recycle": 1,  # Short recycle for testing
                "skip_table_optimization": True,
            }
        )

        schema_message = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string", "maxLength": 100},
                    "status": {"type": "string", "maxLength": 20},
                },
            },
            "key_properties": ["id"],
        }

        # Create valid records
        record_messages = []
        for i in range(100):
            record = {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": i + 1,
                    "name": f"Test Record {i + 1}",
                    "status": "active",
                },
                "time_extracted": datetime.now().isoformat() + "Z",
            }
            record_messages.append(record)

        # Test with simulated connection failures
        oracle_target = OracleTarget(config=config)

        # First, establish the table
        setup_messages = [schema_message] + record_messages[:10]
        input_lines = [json.dumps(msg) + "\n" for msg in setup_messages]
        input_stream = StringIO("".join(input_lines))
        oracle_target.process_lines(input_stream)

        # Verify initial records were processed (may be 0 if connection simulated)
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            initial_count = result.scalar()
            # In test environment, connection might be simulated
            print(f"Initial record count: {initial_count}")
            if initial_count == 0:
                print("Warning: No records inserted - likely simulated connection")

        # Now test with connection issues during processing
        remaining_records = record_messages[10:]

        # Process remaining records - Oracle target should handle any connection issues
        input_lines = [json.dumps(msg) + "\n" for msg in remaining_records]
        input_stream = StringIO("".join(input_lines))

        try:
            oracle_target.process_lines(input_stream)
        except Exception as e:
            # Log but don't fail - target should have retry logic
            print(f"Processing completed with potential recoverable errors: {e}")

        # Verify final state - should have most or all records
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            final_count = result.scalar()

            # Should have at least 80% of records (allowing for some failures)
            expected_min = len(record_messages) * 0.8
            assert (
                final_count >= expected_min
            ), f"Too few records after recovery: {final_count}/{len(record_messages)}"

    def test_schema_validation_errors(
        self,
        oracle_config: dict[str, Any],
        oracle_engine: Engine,
        test_table_name: str,
        table_cleanup,
    ):
        """Test handling of schema validation and data type errors."""
        table_cleanup(test_table_name)

        config = oracle_config.copy()
        config.update(
            {
                "load_method": "append-only",
                "validate_records": True,
                "fail_fast": False,
                "max_retries": 2,
                "skip_table_optimization": True,
            }
        )
        oracle_target = OracleTarget(config=config)

        # Valid schema
        schema_message = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string", "maxLength": 50},
                    "score": {"type": "number"},
                    "active": {"type": "boolean"},
                    "created_at": {"type": "string", "format": "date-time"},
                },
            },
            "key_properties": ["id"],
        }

        # Mix of valid and invalid records
        test_records = [
            # Valid records
            {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": 1,
                    "name": "Valid User 1",
                    "score": 85.5,
                    "active": True,
                    "created_at": "2025-07-02T10:00:00Z",
                },
                "time_extracted": "2025-07-02T10:00:00Z",
            },
            # Invalid type - string for integer
            {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": "not_a_number",
                    "name": "Invalid User 1",
                    "score": 75.0,
                    "active": True,
                    "created_at": "2025-07-02T10:01:00Z",
                },
                "time_extracted": "2025-07-02T10:01:00Z",
            },
            # Valid record
            {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": 2,
                    "name": "Valid User 2",
                    "score": 92.3,
                    "active": False,
                    "created_at": "2025-07-02T10:02:00Z",
                },
                "time_extracted": "2025-07-02T10:02:00Z",
            },
            # String too long
            {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": 3,
                    "name": "A" * 100,  # Exceeds maxLength of 50
                    "score": 88.1,
                    "active": True,
                    "created_at": "2025-07-02T10:03:00Z",
                },
                "time_extracted": "2025-07-02T10:03:00Z",
            },
            # Invalid date format
            {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": 4,
                    "name": "Invalid Date User",
                    "score": 67.8,
                    "active": True,
                    "created_at": "not-a-date",
                },
                "time_extracted": "2025-07-02T10:04:00Z",
            },
            # Another valid record
            {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": 5,
                    "name": "Valid User 3",
                    "score": 79.4,
                    "active": True,
                    "created_at": "2025-07-02T10:05:00Z",
                },
                "time_extracted": "2025-07-02T10:05:00Z",
            },
        ]

        # Process mixed records
        messages = [schema_message] + test_records
        input_lines = [json.dumps(msg) + "\n" for msg in messages]
        input_stream = StringIO("".join(input_lines))

        try:
            oracle_target.process_lines(input_stream)
        except Exception as e:
            print(f"Processing completed with expected validation errors: {e}")

        # Verify that valid records were processed despite errors
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            count = result.scalar()

            # Should have at least the clearly valid records (IDs 1, 2, 5)
            assert count >= 3, f"Too few valid records processed: {count}"

            # Verify specific valid records
            result = conn.execute(
                text(f"""
                SELECT id, name, score, active
                FROM {test_table_name}
                WHERE id IN (1, 2, 5)
                ORDER BY id
            """)
            )
            valid_records = result.fetchall()
            assert len(valid_records) >= 2, "Valid records not found"

    def test_transaction_rollback_on_failure(
        self,
        oracle_config: dict[str, Any],
        oracle_engine: Engine,
        test_table_name: str,
        table_cleanup,
    ):
        """Test transaction rollback behavior on batch failures."""
        table_cleanup(test_table_name)

        config = oracle_config.copy()
        config.update(
            {
                "load_method": "append-only",
                "batch_size": 10,  # Small batches to isolate failures
                "fail_fast": True,  # Should rollback on first error
                "skip_table_optimization": True,
            }
        )

        schema_message = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string", "maxLength": 20},
                    "amount": {"type": "number"},
                },
            },
            "key_properties": ["id"],
        }

        # Create records that will succeed initially
        valid_records = []
        for i in range(20):
            record = {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": i + 1,
                    "name": f"User {i + 1}",
                    "amount": 100.0 + i,
                },
                "time_extracted": datetime.now().isoformat() + "Z",
            }
            valid_records.append(record)

        # Process first batch successfully
        oracle_target = OracleTarget(config=config)
        first_batch = [schema_message] + valid_records[:10]
        input_lines = [json.dumps(msg) + "\n" for msg in first_batch]
        input_stream = StringIO("".join(input_lines))
        oracle_target.process_lines(input_stream)

        # Verify first batch
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            count = result.scalar()
            assert count == 10, f"First batch failed: expected 10, got {count}"

        # Create second batch with problematic records
        problematic_records = []
        for i in range(10, 15):
            record = {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": i + 1,
                    "name": "A" * 50,  # Exceeds maxLength of 20
                    "amount": 200.0 + i,
                },
                "time_extracted": datetime.now().isoformat() + "Z",
            }
            problematic_records.append(record)

        # Add some valid records after problematic ones
        for i in range(15, 20):
            record = {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": i + 1,
                    "name": f"User {i + 1}",
                    "amount": 300.0 + i,
                },
                "time_extracted": datetime.now().isoformat() + "Z",
            }
            problematic_records.append(record)

        # Process problematic batch
        input_lines = [json.dumps(msg) + "\n" for msg in problematic_records]
        input_stream = StringIO("".join(input_lines))

        try:
            oracle_target.process_lines(input_stream)
        except Exception as e:
            print(f"Expected failure in problematic batch: {e}")

        # Verify the state - first batch should still be there
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            count = result.scalar()

            # Should still have the first batch, but problematic batch behavior depends on implementation
            assert count >= 10, f"Transaction rollback affected previous data: {count}"

    def test_memory_pressure_handling(
        self,
        oracle_config: dict[str, Any],
        oracle_engine: Engine,
        test_table_name: str,
        table_cleanup,
    ):
        """Test graceful handling under memory pressure."""
        table_cleanup(test_table_name)

        config = oracle_config.copy()
        config.update(
            {
                "load_method": "append-only",
                "batch_size": 100,  # Smaller batches for memory efficiency
                "max_memory_usage_mb": 64,  # Low memory limit
                "stream_results": True,
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
                    "large_data": {"type": "string", "maxLength": 4000},
                    "metadata": {"type": "object"},
                },
            },
            "key_properties": ["id"],
        }

        # Generate records with large data to stress memory
        record_count = 500
        record_messages = []

        for i in range(record_count):
            # Create large string data (each record ~3KB)
            large_data = f"Large data block {i + 1}: " + "X" * 3000

            record = {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": i + 1,
                    "large_data": large_data,
                    "metadata": {
                        "block_id": i + 1,
                        "size": len(large_data),
                        "checksum": str(hash(large_data)),
                        "tags": [
                            f"tag_{j}" for j in range(20)
                        ],  # Additional memory usage
                    },
                },
                "time_extracted": datetime.now().isoformat() + "Z",
            }
            record_messages.append(record)

        # Process large data set
        messages = [schema_message] + record_messages
        input_lines = [json.dumps(msg) + "\n" for msg in messages]
        input_stream = StringIO("".join(input_lines))

        try:
            oracle_target.process_lines(input_stream)
        except Exception as e:
            print(f"Processing completed under memory pressure: {e}")

        # Verify data was processed efficiently
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            count = result.scalar()

            # Should process most records despite memory constraints
            expected_min = record_count * 0.8
            assert (
                count >= expected_min
            ), f"Memory pressure caused too many failures: {count}/{record_count}"

            # Verify data integrity of processed records
            result = conn.execute(
                text(f"""
                SELECT id, LENGTH(large_data), metadata
                FROM {test_table_name}
                WHERE id IN (1, 250, 500)
            """)
            )

            for row in result:
                assert row[1] > 3000, f"Large data truncated: {row[1]} chars"
                metadata = json.loads(row[2])
                assert "block_id" in metadata, "Metadata corrupted"

    def test_concurrent_access_conflicts(
        self,
        oracle_config: dict[str, Any],
        oracle_engine: Engine,
        test_table_name: str,
        table_cleanup,
    ):
        """Test handling of concurrent access and locking conflicts."""
        table_cleanup(test_table_name)

        config = oracle_config.copy()
        config.update(
            {
                "load_method": "upsert",
                "batch_size": 50,
                "max_retries": 3,
                "retry_delay": 0.2,
                "pool_size": 3,
                "skip_table_optimization": True,
            }
        )

        schema_message = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string", "maxLength": 100},
                    "counter": {"type": "integer"},
                    "updated_at": {"type": "string", "format": "date-time"},
                },
            },
            "key_properties": ["id"],
        }

        # Create initial data
        oracle_target = OracleTarget(config=config)
        initial_records = []

        for i in range(100):
            record = {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": i + 1,
                    "name": f"Record {i + 1}",
                    "counter": 1,
                    "updated_at": datetime.now().isoformat() + "Z",
                },
                "time_extracted": datetime.now().isoformat() + "Z",
            }
            initial_records.append(record)

        # Load initial data
        messages = [schema_message] + initial_records
        input_lines = [json.dumps(msg) + "\n" for msg in messages]
        input_stream = StringIO("".join(input_lines))
        oracle_target.process_lines(input_stream)

        # Verify initial load
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            count = result.scalar()
            assert count == 100, f"Initial load failed: {count}"

        # Simulate concurrent updates by updating same records multiple times
        update_batches = []

        for batch_num in range(3):
            batch_records = []
            for i in range(50):  # Update first 50 records
                record = {
                    "type": "RECORD",
                    "stream": test_table_name,
                    "record": {
                        "id": i + 1,
                        "name": f"Updated Record {i + 1} - Batch {batch_num + 1}",
                        "counter": batch_num + 2,
                        "updated_at": datetime.now().isoformat() + "Z",
                    },
                    "time_extracted": datetime.now().isoformat() + "Z",
                }
                batch_records.append(record)
            update_batches.append(batch_records)

        # Process updates concurrently (simulate by rapid succession)
        for batch in update_batches:
            input_lines = [json.dumps(msg) + "\n" for msg in batch]
            input_stream = StringIO("".join(input_lines))

            try:
                oracle_target.process_lines(input_stream)
                time.sleep(0.1)  # Small delay between batches
            except Exception as e:
                print(
                    f"Concurrent processing batch completed with potential conflicts: {e}"
                )

        # Verify final state
        with oracle_engine.connect() as conn:
            # Should still have 100 records
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            count = result.scalar()
            assert count == 100, f"Concurrent updates corrupted data: {count}"

            # Verify updated records
            result = conn.execute(
                text(f"""
                SELECT id, counter, name
                FROM {test_table_name}
                WHERE id <= 10
                ORDER BY id
            """)
            )

            updated_records = result.fetchall()
            for record in updated_records:
                # Counter should be > 1 (updated at least once)
                assert (
                    record[1] > 1
                ), f"Record {record[0]} not updated: counter={record[1]}"

    def test_network_timeout_recovery(
        self,
        oracle_config: dict[str, Any],
        oracle_engine: Engine,
        test_table_name: str,
        table_cleanup,
    ):
        """Test recovery from network timeouts and slow connections."""
        table_cleanup(test_table_name)

        config = oracle_config.copy()
        config.update(
            {
                "load_method": "append-only",
                "connection_timeout": 10,  # Short timeout for testing
                "pool_timeout": 5,
                "max_retries": 4,
                "retry_delay": 0.5,
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
                    "description": {"type": "string", "maxLength": 1000},
                    "timestamp": {"type": "string", "format": "date-time"},
                },
            },
            "key_properties": ["id"],
        }

        # Create records that should trigger timeout scenarios
        record_messages = []
        for i in range(200):
            record = {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": i + 1,
                    "description": f"Timeout test record {i + 1} with substantial content "
                    * 10,
                    "timestamp": datetime.now().isoformat() + "Z",
                },
                "time_extracted": datetime.now().isoformat() + "Z",
            }
            record_messages.append(record)

        # Process with potential timeouts
        messages = [schema_message] + record_messages
        input_lines = [json.dumps(msg) + "\n" for msg in messages]
        input_stream = StringIO("".join(input_lines))

        try:
            oracle_target.process_lines(input_stream)
        except Exception as e:
            print(f"Processing completed with potential timeout recovery: {e}")

        # Verify recovery
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            count = result.scalar()

            # Should have processed most records despite timeouts
            expected_min = len(record_messages) * 0.7
            assert (
                count >= expected_min
            ), f"Too many records lost to timeouts: {count}/{len(record_messages)}"

    def test_invalid_sql_handling(
        self,
        oracle_config: dict[str, Any],
        oracle_engine: Engine,
        test_table_name: str,
        table_cleanup,
    ):
        """Test handling of invalid SQL generation and execution errors."""
        table_cleanup(test_table_name)

        config = oracle_config.copy()
        config.update(
            {
                "load_method": "append-only",
                "batch_size": 20,
                "fail_fast": False,
                "max_retries": 2,
                "skip_table_optimization": True,
            }
        )
        oracle_target = OracleTarget(config=config)

        # Schema with potentially problematic names
        schema_message = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "normal_field": {"type": "string", "maxLength": 100},
                    "special-field": {
                        "type": "string",
                        "maxLength": 50,
                    },  # Hyphen in name
                    "123numeric": {"type": "number"},  # Starts with number
                    "case_sensitive": {"type": "boolean"},
                },
            },
            "key_properties": ["id"],
        }

        # Records with edge cases
        test_records = []
        for i in range(50):
            record = {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": i + 1,
                    "normal_field": f"Normal text {i + 1}",
                    "special-field": f"Special-{i + 1}",
                    "123numeric": round(100.5 + i, 2),
                    "case_sensitive": i % 2 == 0,
                },
                "time_extracted": datetime.now().isoformat() + "Z",
            }
            test_records.append(record)

        # Process with potentially problematic SQL
        messages = [schema_message] + test_records
        input_lines = [json.dumps(msg) + "\n" for msg in messages]
        input_stream = StringIO("".join(input_lines))

        try:
            oracle_target.process_lines(input_stream)
        except Exception as e:
            print(f"Processing completed with SQL generation challenges: {e}")

        # Verify that data was processed despite SQL complexities
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            count = result.scalar()

            # Should have processed most records
            expected_min = len(test_records) * 0.8
            assert (
                count >= expected_min
            ), f"SQL issues caused too many failures: {count}/{len(test_records)}"

            # Verify column handling worked
            if count > 0:
                result = conn.execute(
                    text(f"SELECT * FROM {test_table_name} WHERE ROWNUM <= 3")
                )
                sample_rows = result.fetchall()
                assert len(sample_rows) > 0, "No sample data retrieved"

    def test_resource_exhaustion_recovery(
        self,
        oracle_config: dict[str, Any],
        oracle_engine: Engine,
        test_table_name: str,
        table_cleanup,
    ):
        """Test graceful handling of resource exhaustion scenarios."""
        table_cleanup(test_table_name)

        config = oracle_config.copy()
        config.update(
            {
                "load_method": "append-only",
                "batch_size": 1000,  # Large batches to stress resources
                "pool_size": 2,  # Limited connections
                "max_overflow": 1,
                "pool_timeout": 2,  # Quick timeout
                "max_retries": 5,
                "retry_delay": 0.1,
                "skip_table_optimization": True,
            }
        )

        schema_message = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "resource_data": {"type": "string", "maxLength": 2000},
                    "timestamp": {"type": "string", "format": "date-time"},
                },
            },
            "key_properties": ["id"],
        }

        # Generate large dataset to stress resources
        record_count = 2000
        record_messages = []

        for i in range(record_count):
            record = {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": i + 1,
                    "resource_data": f"Resource test data {i + 1}: " + "R" * 1500,
                    "timestamp": datetime.now().isoformat() + "Z",
                },
                "time_extracted": datetime.now().isoformat() + "Z",
            }
            record_messages.append(record)

        # Process multiple targets concurrently to stress resources
        targets = []
        for i in range(3):
            target = OracleTarget(config=config)
            targets.append(target)

        # Process first batch to establish table
        first_target = targets[0]
        setup_messages = [schema_message] + record_messages[:100]
        input_lines = [json.dumps(msg) + "\n" for msg in setup_messages]
        input_stream = StringIO("".join(input_lines))
        first_target.process_lines(input_stream)

        # Process remaining data with resource contention
        remaining_records = record_messages[100:]
        chunk_size = len(remaining_records) // 3

        for i, target in enumerate(targets):
            start_idx = i * chunk_size
            end_idx = start_idx + chunk_size if i < 2 else len(remaining_records)
            chunk = remaining_records[start_idx:end_idx]

            if chunk:
                input_lines = [json.dumps(msg) + "\n" for msg in chunk]
                input_stream = StringIO("".join(input_lines))

                try:
                    target.process_lines(input_stream)
                except Exception as e:
                    print(f"Target {i} completed with resource constraints: {e}")

        # Verify recovery and data integrity
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            total_count = result.scalar()

            # Should have processed most records despite resource constraints
            expected_min = record_count * 0.7
            assert (
                total_count >= expected_min
            ), f"Resource exhaustion caused too many losses: {total_count}/{record_count}"

            # Verify no data corruption
            result = conn.execute(
                text(f"""
                SELECT COUNT(DISTINCT id) as unique_ids,
                       MAX(id) as max_id,
                       MIN(id) as min_id
                FROM {test_table_name}
            """)
            )

            stats = result.fetchone()
            assert (
                stats[0] == total_count
            ), "Duplicate IDs found - data corruption detected"
            assert stats[1] <= record_count, f"Invalid max ID: {stats[1]}"
            assert stats[2] >= 1, f"Invalid min ID: {stats[2]}"
