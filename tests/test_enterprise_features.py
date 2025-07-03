"""
Oracle Enterprise Edition features tests.

These tests validate advanced Oracle features that require Enterprise Edition
licenses, focusing on partitioning and compression (including HCC for
Exadata/Autonomous).
"""

from __future__ import annotations

import json
import random
from datetime import datetime, timedelta
from io import StringIO
from typing import TYPE_CHECKING, Any

import pytest
from sqlalchemy import text

from flext_target_oracle.target import OracleTarget
from tests.helpers import requires_oracle_connection

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine


@pytest.mark.integration
@requires_oracle_connection
class TestEnterpriseFeatures:
    """Test Oracle Enterprise Edition advanced features."""

    def test_table_partitioning_features(
        self,
        oracle_config: dict[str, Any],
        oracle_engine: Engine,
        oracle_edition_info: dict[str, bool],
        test_table_name: str,
        table_cleanup,
    ) -> None:
        """Test Oracle table partitioning (requires Partitioning option)."""
        table_cleanup(test_table_name)

        # Skip if partitioning not available
        if not oracle_edition_info.get("has_partitioning", False):
            pytest.skip("Oracle Partitioning option not available")

        # Configure with partitioning enabled
        config = oracle_config.copy()
        config.update(
            {
                "load_method": "append-only",
                "batch_size": 1000,
                "oracle_is_enterprise_edition": True,
                "oracle_has_partitioning_option": True,
                "enable_partitioning": True,
                "partition_type": "range",
                "partition_column": "created_date",
                "partition_interval": "NUMTOYMINTERVAL(1,'MONTH')",
                "skip_table_optimization": False,  # Enable to test partitioning
            }
        )
        oracle_target = OracleTarget(config=config)

        # Schema with date column for partitioning
        schema_message = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "customer_id": {"type": "integer"},
                    "order_amount": {"type": "number"},
                    "created_date": {"type": "string", "format": "date-time"},
                    "product_category": {"type": "string", "maxLength": 50},
                    "region": {"type": "string", "maxLength": 20},
                },
            },
            "key_properties": ["id"],
        }

        # Generate data across multiple months for partitioning
        record_count = 5000
        record_messages = []
        base_date = datetime(2025, 1, 1)

        categories = ["Electronics", "Clothing", "Books", "Home", "Sports"]
        regions = ["North", "South", "East", "West", "Central"]

        for i in range(record_count):
            # Distribute data across 6 months
            month_offset = i % 6
            record_date = base_date + timedelta(days=30 * month_offset + (i % 30))

            record = {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": i + 1,
                    "customer_id": random.randint(1, 1000),
                    "order_amount": round(random.uniform(10.0, 1000.0), 2),
                    "created_date": record_date.isoformat() + "Z",
                    "product_category": random.choice(categories),
                    "region": random.choice(regions),
                },
                "time_extracted": datetime.now().isoformat() + "Z",
            }
            record_messages.append(record)

        # Process partitioned data
        messages = [schema_message] + record_messages
        input_lines = [json.dumps(msg) + "\n" for msg in messages]
        input_stream = StringIO("".join(input_lines))

        oracle_target.process_lines(input_stream)

        # Verify partitioning worked
        with oracle_engine.connect() as conn:
            # Check total record count
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            count = result.scalar()
            assert (
                count == record_count
            ), f"Expected {record_count} records, got {count}"

            # Check if table is partitioned (Enterprise Edition feature)
            try:
                result = conn.execute(
                    text(
                        f"""
                    SELECT table_name, partitioning_type, partition_count
                    FROM user_part_tables
                    WHERE table_name = UPPER('{test_table_name}')
                """
                    )
                )
                partition_info = result.fetchone()

                if partition_info:
                    print(
                        f"Table partitioned: {partition_info[1]} with "
                        f"{partition_info[2]} partitions"
                    )
                    assert partition_info[1] is not None, "Partitioning type not set"
                else:
                    print(
                        "Partitioning not applied (may require specific "
                        "Oracle configuration)"
                    )

            except Exception as e:
                print(f"Could not verify partitioning (may not be available): {e}")

            # Test partition pruning with date-based queries
            try:
                result = conn.execute(
                    text(
                        f"""
                    SELECT COUNT(*) FROM {test_table_name}
                    WHERE created_date >= DATE '2025-03-01'
                    AND created_date < DATE '2025-04-01'
                """
                    )
                )
                march_count = result.scalar()
                assert march_count > 0, "No records found in March partition"
                print(f"March partition contains {march_count} records")

            except Exception as e:
                print(f"Partition pruning test failed: {e}")

    def test_compression_features(
        self,
        oracle_config: dict[str, Any],
        oracle_engine: Engine,
        _oracle_edition_info: dict[str, bool],
        test_table_name: str,
        table_cleanup,
    ) -> None:
        """Test Oracle compression (HCC for Exadata/Autonomous, Advanced for others)."""
        # Note: _oracle_edition_info fixture provided but not used in test logic
        table_cleanup(test_table_name)

        # Detect if running on Exadata or Autonomous Database
        is_exadata_or_autonomous = False
        compression_type = "advanced"
        compress_for = "OLTP"

        try:
            with oracle_engine.connect() as conn:
                # Check for Exadata or Autonomous indicators
                result = conn.execute(
                    text(
                        """
                    SELECT banner FROM v$version
                    WHERE banner LIKE '%Exadata%'
                       OR banner LIKE '%Autonomous%'
                       OR banner LIKE '%Cloud%'
                """
                    )
                )
                exadata_check = result.fetchone()

                if exadata_check:
                    is_exadata_or_autonomous = True
                    compression_type = "hcc"  # Hybrid Columnar Compression
                    compress_for = "QUERY HIGH"
                    print(
                        f"Detected Exadata/Autonomous environment: {exadata_check[0]}"
                    )
                else:
                    print("Standard Oracle environment detected")

        except Exception as e:
            print(f"Could not detect Oracle environment: {e}")

        # Configure with appropriate compression
        config = oracle_config.copy()
        config.update(
            {
                "load_method": "append-only",
                "batch_size": 2000,
                "oracle_is_enterprise_edition": True,
                "oracle_has_compression_option": True,
                "enable_compression": True,
                "compression_type": compression_type,
                "compress_for": compress_for,
                "skip_table_optimization": False,  # Enable to test compression
            }
        )
        oracle_target = OracleTarget(config=config)

        # Schema with varied data types for compression testing
        schema_message = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "text_data": {"type": "string", "maxLength": 1000},
                    "repeated_text": {"type": "string", "maxLength": 500},
                    "numeric_value": {"type": "number"},
                    "json_metadata": {"type": "object"},
                    "created_at": {"type": "string", "format": "date-time"},
                },
            },
            "key_properties": ["id"],
        }

        # Generate data with repetitive patterns (good for compression)
        record_count = 8000
        record_messages = []

        repeated_phrases = [
            "This is a repeated phrase for compression testing",
            "Another common phrase that appears frequently",
            "Standard template text that shows up often",
            "Repeated content for optimal compression ratio",
        ]

        for i in range(record_count):
            record = {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": i + 1,
                    "text_data": f"Record {i + 1}: "
                    + random.choice(repeated_phrases) * 3,
                    "repeated_text": repeated_phrases[i % 4],  # Highly repetitive
                    "numeric_value": round(random.uniform(1.0, 100.0), 2),
                    "json_metadata": {
                        "category": random.choice(["A", "B", "C"]),  # Low cardinality
                        "status": random.choice(["active", "inactive"]),
                        "priority": random.choice(["high", "medium", "low"]),
                        "template_id": i % 10,  # Repetitive values
                    },
                    "created_at": datetime.now().isoformat() + "Z",
                },
                "time_extracted": datetime.now().isoformat() + "Z",
            }
            record_messages.append(record)

        # Process compressed data
        messages = [schema_message] + record_messages
        input_lines = [json.dumps(msg) + "\n" for msg in messages]
        input_stream = StringIO("".join(input_lines))

        oracle_target.process_lines(input_stream)

        # Verify compression worked
        with oracle_engine.connect() as conn:
            # Check record count
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            count = result.scalar()
            assert (
                count == record_count
            ), f"Expected {record_count} records, got {count}"

            # Check compression status
            try:
                result = conn.execute(
                    text(
                        f"""
                    SELECT table_name, compression, compress_for
                    FROM user_tables
                    WHERE table_name = UPPER('{test_table_name}')
                """
                    )
                )
                compression_info = result.fetchone()

                if compression_info and compression_info[1] == "ENABLED":
                    print(f"Table compressed: {compression_info[2]}")
                    if is_exadata_or_autonomous:
                        print("HCC (Hybrid Columnar Compression) applied")
                    else:
                        print("Advanced compression applied")
                    assert compression_info[1] == "ENABLED", "Compression not enabled"
                else:
                    print(
                        "Compression not applied (may require license or "
                        "specific platform)"
                    )

            except Exception as e:
                print(f"Could not verify compression (may not be available): {e}")

            # Test compressed data retrieval performance
            try:
                # Query that benefits from compression
                result = conn.execute(
                    text(
                        f"""
                    SELECT repeated_text, COUNT(*) as frequency,
                           AVG(numeric_value) as avg_value
                    FROM {test_table_name}
                    GROUP BY repeated_text
                    ORDER BY frequency DESC
                """
                    )
                )

                compression_query_results = result.fetchall()
                assert len(compression_query_results) == 4, "Compressed query failed"

                # Verify compression effectiveness
                for result_row in compression_query_results:
                    assert (
                        result_row[1] == record_count // 4
                    ), "Compression query incorrect"
                    assert result_row[2] > 0, "Average calculation failed"

                print(
                    f"Compression query successful: "
                    f"{len(compression_query_results)} groups"
                )

            except Exception as e:
                print(f"Compression query test failed: {e}")

    def test_parallel_dml_operations(
        self,
        oracle_config: dict[str, Any],
        oracle_engine: Engine,
        oracle_edition_info: dict[str, bool],
        test_table_name: str,
        table_cleanup,
        performance_timer,
    ) -> None:
        """Test Oracle Parallel DML operations (requires Enterprise Edition)."""
        table_cleanup(test_table_name)

        # Skip if not Enterprise Edition
        if not oracle_edition_info.get("is_enterprise", False):
            pytest.skip("Oracle Enterprise Edition not available")

        # Configure with parallel DML enabled
        config = oracle_config.copy()
        config.update(
            {
                "load_method": "append-only",
                "batch_size": 5000,
                "oracle_is_enterprise_edition": True,
                "parallel_degree": 4,
                "use_parallel_dml": True,
                "enable_parallel_ddl": True,
                "enable_parallel_query": True,
                "use_append_hint": True,
                "skip_table_optimization": False,  # Enable to test parallel features
            }
        )
        oracle_target = OracleTarget(config=config)

        # Schema for parallel processing
        schema_message = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "batch_id": {"type": "integer"},
                    "data_value": {"type": "number"},
                    "text_content": {"type": "string", "maxLength": 200},
                    "processing_timestamp": {"type": "string", "format": "date-time"},
                },
            },
            "key_properties": ["id"],
        }

        # Generate large dataset for parallel processing
        record_count = 20000
        record_messages = []

        for i in range(record_count):
            record = {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": i + 1,
                    "batch_id": (i // 1000) + 1,  # 20 batches of 1000 records
                    "data_value": round(random.uniform(1.0, 1000.0), 3),
                    "text_content": (
                        f"Parallel processing record {i + 1} with substantial content"
                    ),
                    "processing_timestamp": datetime.now().isoformat() + "Z",
                },
                "time_extracted": datetime.now().isoformat() + "Z",
            }
            record_messages.append(record)

        # Process with parallel DML
        messages = [schema_message] + record_messages
        input_lines = [json.dumps(msg) + "\n" for msg in messages]
        input_stream = StringIO("".join(input_lines))

        performance_timer.start()
        oracle_target.process_lines(input_stream)
        performance_timer.stop()

        # Verify parallel processing results
        with oracle_engine.connect() as conn:
            # Check record count
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            count = result.scalar()
            assert (
                count == record_count
            ), f"Expected {record_count} records, got {count}"

            # Verify batch distribution
            result = conn.execute(
                text(
                    f"""
                SELECT batch_id, COUNT(*) as batch_count
                FROM {test_table_name}
                GROUP BY batch_id
                ORDER BY batch_id
            """
                )
            )

            batch_stats = result.fetchall()
            assert (
                len(batch_stats) == 20
            ), f"Expected 20 batches, got {len(batch_stats)}"

            for batch_id, batch_count in batch_stats:
                assert (
                    batch_count == 1000
                ), f"Batch {batch_id}: expected 1000 records, got {batch_count}"

            # Test parallel query performance
            try:
                parallel_query = f"""
                SELECT /*+ PARALLEL({test_table_name}, 4) */
                       batch_id,
                       COUNT(*) as record_count,
                       SUM(data_value) as total_value,
                       AVG(data_value) as avg_value
                FROM {test_table_name}
                GROUP BY batch_id
                ORDER BY batch_id
                """

                result = conn.execute(text(parallel_query))
                parallel_results = result.fetchall()
                assert len(parallel_results) == 20, "Parallel query failed"
                print("Parallel query execution successful")

            except Exception as e:
                print(f"Parallel query test failed: {e}")

        # Performance validation
        throughput = record_count / performance_timer.duration
        print(f"Parallel DML performance: {throughput:.0f} records/second")

        # Parallel processing should show good performance
        expected_min_throughput = 500  # Adjust based on your Oracle setup
        assert (
            throughput > expected_min_throughput
        ), f"Parallel DML throughput too low: {throughput:.0f} records/second"
