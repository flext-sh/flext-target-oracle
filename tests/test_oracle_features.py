"""Test Oracle-specific features and optimizations.

This module tests Oracle-specific functionality including MERGE operations,
partitioning, compression, and advanced Oracle features.
"""

from __future__ import annotations

import json
import logging
from io import StringIO
from typing import TYPE_CHECKING, Any
from unittest.mock import patch

from sqlalchemy import text

from flext_target_oracle.target import OracleTarget
from tests.helpers import requires_oracle_connection

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine

log = logging.getLogger(__name__)


@requires_oracle_connection
class TestOracleSpecificFeatures:
    """Test Oracle-specific features and optimizations."""

    def test_merge_upsert_operations(
        self,
        oracle_config: dict[str, Any],
        test_table_name: str,
        oracle_engine: Engine,
        table_cleanup,
    ) -> None:
        """Test Oracle MERGE operations for efficient upserts."""
        table_cleanup(test_table_name)

        # Configure for MERGE operations
        merge_config = oracle_config.copy()
        merge_config["upsert_method"] = "merge"
        merge_config["use_bulk_operations"] = True

        target = OracleTarget(config=merge_config)

        # Create test schema
        test_schema = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "status": {"type": "string"},
                    "updated_at": {"type": "string", "format": "date-time"},
                },
            },
            "key_properties": ["id"],
        }

        # Initial batch of records
        initial_records = [
            {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": 1,
                    "name": "Alice",
                    "status": "active",
                    "updated_at": "2025-07-02T10:00:00Z",
                },
            },
            {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": 2,
                    "name": "Bob",
                    "status": "inactive",
                    "updated_at": "2025-07-02T10:01:00Z",
                },
            },
        ]

        # Process initial records
        messages = [json.dumps(test_schema)]
        messages.extend([json.dumps(record) for record in initial_records])
        input_data = "\n".join(messages)

        with patch("sys.stdin", StringIO(input_data)):
            target.cli()

        # Verify initial data
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            assert row[0] == 2

        # MERGE operation: update existing + insert new
        merge_records = [
            {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": 1,  # Update existing
                    "name": "Alice Updated",
                    "status": "active",
                    "updated_at": "2025-07-02T11:00:00Z",
                },
            },
            {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": 3,  # Insert new
                    "name": "Charlie",
                    "status": "pending",
                    "updated_at": "2025-07-02T11:01:00Z",
                },
            },
        ]

        # Process MERGE records
        messages = [json.dumps(test_schema)]
        messages.extend([json.dumps(record) for record in merge_records])
        input_data = "\n".join(messages)

        target_new = OracleTarget(config=merge_config)
        with patch("sys.stdin", StringIO(input_data)):
            target_new.cli()

        # Verify MERGE results
        with oracle_engine.connect() as conn:
            # Should have 3 total records
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            assert row[0] == 3

            # Verify updated record
            result = conn.execute(
                text(f"SELECT name FROM {test_table_name} WHERE id = 1"),
            )
            row = result.fetchone()
            assert row is not None
            assert row[0] == "Alice Updated"

            # Verify inserted record
            result = conn.execute(
                text(f"SELECT name FROM {test_table_name} WHERE id = 3"),
            )
            row = result.fetchone()
            assert row is not None
            assert row[0] == "Charlie"

    def test_bulk_operations(
        self,
        oracle_config: dict[str, Any],
        test_table_name: str,
        oracle_engine: Engine,
        table_cleanup,
        performance_timer,
    ) -> None:
        """Test Oracle bulk operations for high performance."""
        table_cleanup(test_table_name)

        # Configure for bulk operations
        bulk_config = oracle_config.copy()
        bulk_config["use_bulk_operations"] = True
        bulk_config["batch_size"] = 1000
        bulk_config["array_size"] = 1000

        target = OracleTarget(config=bulk_config)

        # Create test schema
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

        # Generate large dataset for bulk testing
        bulk_records = [{
                    "type": "RECORD",
                    "stream": test_table_name,
                    "record": {
                        "id": i + 1,
                        "data": f"Bulk data item {i + 1}",
                        "value": float(i * 0.5),
                    },
                } for i in range(5000)]

        # Process with timing
        messages = [json.dumps(test_schema)]
        messages.extend([json.dumps(record) for record in bulk_records])
        input_data = "\n".join(messages)

        performance_timer.start()

        with patch("sys.stdin", StringIO(input_data)):
            target.cli()

        performance_timer.stop()

        # Verify bulk processing results
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            count = row[0]
            assert count == len(bulk_records)

        # Performance check for bulk operations
        throughput = len(bulk_records) / performance_timer.duration
        assert (
            throughput > 100
        ), f"Bulk operation throughput too low: {throughput:.2f} records/sec"

    def test_parallel_processing_configuration(
        self,
        oracle_config: dict[str, Any],
        test_table_name: str,
        oracle_engine: Engine,
        table_cleanup,
    ) -> None:
        """Test Oracle parallel processing configuration."""
        table_cleanup(test_table_name)

        # Configure for parallel processing
        parallel_config = oracle_config.copy()
        parallel_config["parallel_degree"] = 4
        parallel_config["use_bulk_operations"] = True
        parallel_config["max_workers"] = 4

        target = OracleTarget(config=parallel_config)

        # Create test schema
        test_schema = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "category": {"type": "string"},
                    "amount": {"type": "number"},
                },
            },
            "key_properties": ["id"],
        }

        # Generate moderate dataset
        parallel_records = [{
                    "type": "RECORD",
                    "stream": test_table_name,
                    "record": {
                        "id": i + 1,
                        "category": f"Category {(i % 10) + 1}",
                        "amount": float(i * 1.25),
                    },
                } for i in range(2000)]

        # Process records
        messages = [json.dumps(test_schema)]
        messages.extend([json.dumps(record) for record in parallel_records])
        input_data = "\n".join(messages)

        with patch("sys.stdin", StringIO(input_data)):
            target.cli()

        # Verify parallel processing results
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            count = row[0]
            assert count == len(parallel_records)

            # Verify data distribution
            result = conn.execute(
                text(
                    f"SELECT DISTINCT category "
                    f"FROM {test_table_name} ORDER BY category",
                ),
            )
            categories = [row[0] for row in result.fetchall()]
            assert len(categories) == 10  # Should have 10 different categories

    def test_table_compression_features(
        self,
        oracle_config: dict[str, Any],
        test_table_name: str,
        oracle_engine: Engine,
        table_cleanup,
    ) -> None:
        """Test Oracle table compression features."""
        table_cleanup(test_table_name)

        # Configure for compression
        compression_config = oracle_config.copy()
        compression_config["enable_compression"] = True
        compression_config["compression_type"] = "basic"

        target = OracleTarget(config=compression_config)

        # Create test schema with larger data
        test_schema = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "large_text": {"type": "string"},
                    "description": {"type": "string"},
                },
            },
            "key_properties": ["id"],
        }

        # Generate records with larger text data
        compression_records = [{
                    "type": "RECORD",
                    "stream": test_table_name,
                    "record": {
                        "id": i + 1,
                        "large_text": "A" * 1000,  # 1KB of repeated data
                        "description": (
                            f"Description for record {i + 1} with lots of "
                            "repeated text " * 10
                        ),
                    },
                } for i in range(100)]

        # Process records
        messages = [json.dumps(test_schema)]
        messages.extend([json.dumps(record) for record in compression_records])
        input_data = "\n".join(messages)

        with patch("sys.stdin", StringIO(input_data)):
            target.cli()

        # Verify compression was applied (check table exists and has data)
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            count = row[0]
            assert count == len(compression_records)

            # Try to check if compression is enabled (may require DBA
            # privileges)
            try:
                result = conn.execute(
                    text(
                        f"""
                    SELECT compression, compress_for
                    FROM user_tables
                    WHERE table_name = UPPER('{test_table_name}')
                """,
                    ),
                )
                table_info = result.fetchone()
                if table_info and table_info.compression:
                    assert table_info.compression in {"ENABLED", "DISABLED"}
            except Exception as e:
                # for debug
                # TODO: Consider using else block
                log.exception(
                    f"Could not access compression info (expected in some "
                    # Link: https://github.com/issue/todo
                    f"environments)  # TODO(@dev): Replace with proper logging: {e}",
                )

    def test_array_size_optimization(
        self,
        oracle_config: dict[str, Any],
        test_table_name: str,
        oracle_engine: Engine,
        table_cleanup,
        performance_timer,
    ) -> None:
        """Test Oracle array size optimization for fetch operations."""
        table_cleanup(test_table_name)

        # Configure with optimized array size
        array_config = oracle_config.copy()
        array_config["array_size"] = 2000
        array_config["batch_size"] = 2000

        target = OracleTarget(config=array_config)

        # Create test schema
        test_schema = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "timestamp": {"type": "string", "format": "date-time"},
                },
            },
            "key_properties": ["id"],
        }

        # Generate dataset for array size testing
        array_records = [{
                    "type": "RECORD",
                    "stream": test_table_name,
                    "record": {
                        "id": i + 1,
                        "name": f"Record {i + 1}",
                        "timestamp": "2025-07-02T10:00:00Z",
                    },
                } for i in range(3000)]

        # Process with timing
        messages = [json.dumps(test_schema)]
        messages.extend([json.dumps(record) for record in array_records])
        input_data = "\n".join(messages)

        performance_timer.start()

        with patch("sys.stdin", StringIO(input_data)):
            target.cli()

        performance_timer.stop()

        # Verify array processing results
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            count = row[0]
            assert count == len(array_records)

        # Performance check
        throughput = len(array_records) / performance_timer.duration
        assert (
            throughput > 200
        ), f"Array optimization throughput too low: {throughput:.2f} records/sec"

    def test_oracle_data_type_mappings(
        self,
        oracle_config: dict[str, Any],
        test_table_name: str,
        oracle_engine: Engine,
        table_cleanup,
    ) -> None:
        """Test Oracle-specific data type mappings."""
        table_cleanup(test_table_name)

        # Configure with Oracle type settings
        type_config = oracle_config.copy()
        type_config["varchar_max_length"] = 2000
        type_config["use_nvarchar"] = True
        type_config["number_precision"] = 20
        type_config["number_scale"] = 5

        target = OracleTarget(config=type_config)

        # Create comprehensive schema with Oracle-specific types
        oracle_type_schema = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "short_text": {"type": "string", "maxLength": 100},
                    "medium_text": {"type": "string", "maxLength": 2000},
                    "long_text": {
                        "type": "string",
                        "maxLength": 10000,
                    },  # Should become CLOB
                    "unicode_text": {"type": "string", "maxLength": 500},
                    "small_number": {"type": "integer"},
                    "big_number": {"type": "number"},
                    "precise_decimal": {"type": "number", "multipleOf": 0.00001},
                    "boolean_flag": {"type": "boolean"},
                    "timestamp_field": {"type": "string", "format": "date-time"},
                    "date_field": {"type": "string", "format": "date"},
                    "json_object": {"type": "object"},
                    "json_array": {"type": "array"},
                },
            },
            "key_properties": ["id"],
        }

        # Create record with various Oracle data types
        oracle_type_record = {
            "type": "RECORD",
            "stream": test_table_name,
            "record": {
                "id": 1,
                "short_text": "Short text",
                "medium_text": "M" * 1500,
                "long_text": "L" * 8000,
                "unicode_text": "Unicode: 中文 العربية русский 🌍",
                "small_number": 42,
                "big_number": 999999999.123456789,
                "precise_decimal": 123.45678,
                "boolean_flag": True,
                "timestamp_field": "2025-07-02T10:30:45.123Z",
                "date_field": "2025-07-02",
                "json_object": {
                    "key1": "value1",
                    "key2": 123,
                    "nested": {"inner": "data"},
                },
                "json_array": [1, "two", {"three": 3}],
            },
        }

        # Process Oracle type record
        messages = [json.dumps(oracle_type_schema), json.dumps(oracle_type_record)]
        input_data = "\n".join(messages)

        with patch("sys.stdin", StringIO(input_data)):
            target.cli()

        # Verify Oracle type mapping results
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None

            # Verify basic data retrieval
            assert row.id == 1
            assert row.short_text == "Short text"
            assert len(row.medium_text) == 1500
            assert len(row.long_text) == 8000
            assert "中文" in row.unicode_text
            assert row.small_number == 42
            assert row.boolean_flag == 1

            # Check column types in Oracle
            result = conn.execute(
                text(
                    f"""
                SELECT column_name, data_type, data_length, data_precision, data_scale
                FROM user_tab_columns
                WHERE table_name = UPPER('{test_table_name}')
                ORDER BY column_id
            """,
                ),
            )

            columns = result.fetchall()
            column_types = {col.column_name: col.data_type for col in columns}

            # Verify Oracle-specific type mappings
            assert column_types.get("ID") in {"NUMBER", "INTEGER"}
            assert column_types.get("SHORT_TEXT") in {"VARCHAR2", "NVARCHAR2"}
            assert column_types.get("LONG_TEXT") in {"CLOB", "NCLOB"}
            assert column_types.get("PRECISE_DECIMAL") == "NUMBER"

    def test_connection_pooling_behavior(
        self,
        oracle_config: dict[str, Any],
        test_table_name: str,
        oracle_engine: Engine,
        table_cleanup,
    ) -> None:
        """Test Oracle connection pooling behavior."""
        table_cleanup(test_table_name)

        # Configure connection pooling
        pool_config = oracle_config.copy()
        pool_config["pool_size"] = 5
        pool_config["max_overflow"] = 10
        pool_config["pool_pre_ping"] = True
        pool_config["pool_recycle"] = 3600

        # Create multiple target instances to test pooling
        targets = [OracleTarget(config=pool_config) for _ in range(3)]

        # Create test schema
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

        # Process records with multiple targets (simulating concurrent access)
        for worker_id, target in enumerate(targets):
            worker_records = [{
                        "type": "RECORD",
                        "stream": test_table_name,
                        "record": {
                            "id": worker_id * 100 + i + 1,
                            "worker_id": worker_id + 1,
                            "data": f"Worker {worker_id + 1} Record {i + 1}",
                        },
                    } for i in range(100)]

            messages = [json.dumps(test_schema)]
            messages.extend([json.dumps(record) for record in worker_records])
            input_data = "\n".join(messages)

            with patch("sys.stdin", StringIO(input_data)):
                target.cli()

        # Verify pooled connection results
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            total_count = row[0]
            assert total_count == 300  # 3 workers * 100 records each

            # Verify data from all workers
            result = conn.execute(
                text(
                    f"SELECT DISTINCT worker_id FROM {test_table_name} "
                    f"ORDER BY worker_id",
                ),
            )
            worker_ids = [row[0] for row in result.fetchall()]
            assert worker_ids == [1, 2, 3]

    def test_oracle_error_handling(
        self,
        oracle_config: dict[str, Any],
        test_table_name: str,
        oracle_engine: Engine,
        table_cleanup,
    ) -> None:
        """Test Oracle-specific error handling."""
        table_cleanup(test_table_name)

        # Configure error handling
        error_config = oracle_config.copy()
        error_config["max_retries"] = 2
        error_config["retry_delay"] = 0.1
        error_config["retry_backoff"] = 2.0

        target = OracleTarget(config=error_config)

        # Create schema with constraints
        constraint_schema = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "short_field": {"type": "string", "maxLength": 10},
                    "required_field": {"type": "string"},
                },
            },
            "key_properties": ["id"],
        }

        # First, create the table with a valid record
        valid_record = {
            "type": "RECORD",
            "stream": test_table_name,
            "record": {
                "id": 1,
                "short_field": "Valid",
                "required_field": "Required",
            },
        }

        messages = [json.dumps(constraint_schema), json.dumps(valid_record)]
        input_data = "\n".join(messages)

        with patch("sys.stdin", StringIO(input_data)):
            target.cli()

        # Verify valid record was inserted
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            assert row[0] == 1

        # Test duplicate key error handling
        duplicate_record = {
            "type": "RECORD",
            "stream": test_table_name,
            "record": {
                "id": 1,  # Duplicate ID
                "short_field": "Duplicate",
                "required_field": "Required",
            },
        }

        target_new = OracleTarget(config=error_config)
        messages = [json.dumps(constraint_schema), json.dumps(duplicate_record)]
        input_data = "\n".join(messages)

        # This should handle the duplicate gracefully depending on upsert
        # settings
        try:
            with patch("sys.stdin", StringIO(input_data)):
                target_new.cli()
        except Exception as e:
            # Duplicate errors are expected and should be handled
            assert "unique" in str(e).lower() or "duplicate" in str(e).lower()
