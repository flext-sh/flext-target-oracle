"""
End-to-end test using Oracle Autonomous Database with TCPS connection.

This test validates the complete Oracle target functionality using a real
Oracle Autonomous Database connection from the .env file.
"""

import json
from datetime import datetime, timezone
from io import StringIO

import pytest

from flext_target_oracle import OracleTarget
from flext_target_oracle.connectors import OracleConnector

from .helpers import get_test_config, requires_oracle_connection


class TestOracleAutonomousE2E:
    """End-to-end tests using Oracle Autonomous Database."""

    @pytest.fixture
    def oracle_config(self):
        """Get Oracle configuration from environment."""
        return get_test_config(include_licensed_features=False)

    @pytest.fixture
    def sample_schema(self):
        """Sample Singer schema for testing."""
        return {
            "type": "SCHEMA",
            "stream": "test_orders",
            "schema": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "integer"},
                    "customer_id": {"type": "integer"},
                    "order_date": {"type": "string", "format": "date"},
                    "order_status": {"type": "string"},
                    "total_amount": {"type": "number"},
                    "is_priority": {"type": "boolean"},
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "product_id": {"type": "integer"},
                                "quantity": {"type": "integer"},
                                "price": {"type": "number"},
                            },
                        },
                    },
                    "shipping_address": {
                        "type": "object",
                        "properties": {
                            "street": {"type": "string"},
                            "city": {"type": "string"},
                            "state": {"type": "string"},
                            "zip": {"type": "string"},
                        },
                    },
                    "notes": {"type": ["string", "null"]},
                },
            },
            "key_properties": ["order_id"],
        }

    @pytest.fixture
    def sample_records(self):
        """Sample records for testing."""
        return [
            {
                "type": "RECORD",
                "stream": "test_orders",
                "record": {
                    "order_id": 1001,
                    "customer_id": 201,
                    "order_date": "2025-01-01",
                    "order_status": "completed",
                    "total_amount": 1250.50,
                    "is_priority": True,
                    "items": [
                        {"product_id": 101, "quantity": 2, "price": 500.00},
                        {"product_id": 102, "quantity": 1, "price": 250.50},
                    ],
                    "shipping_address": {
                        "street": "123 Main St",
                        "city": "Austin",
                        "state": "TX",
                        "zip": "78701",
                    },
                    "notes": "Rush delivery requested",
                },
            },
            {
                "type": "RECORD",
                "stream": "test_orders",
                "record": {
                    "order_id": 1002,
                    "customer_id": 202,
                    "order_date": "2025-01-02",
                    "order_status": "pending",
                    "total_amount": 750.00,
                    "is_priority": False,
                    "items": [{"product_id": 103, "quantity": 3, "price": 250.00}],
                    "shipping_address": {
                        "street": "456 Oak Ave",
                        "city": "Dallas",
                        "state": "TX",
                        "zip": "75201",
                    },
                    "notes": None,
                },
            },
        ]

    @requires_oracle_connection
    def test_connection_verification(self, oracle_config):
        """Test basic connection to Oracle Autonomous Database."""
        target = OracleTarget(config=oracle_config)

        # Test that we can create a sink (which creates connector)
        sink = target.get_sink("test_connection")
        assert sink is not None

        # Test connector
        connector = sink.connector
        assert isinstance(connector, OracleConnector)

        # Test actual connection
        with connector._conn.begin() as conn:
            result = conn.execute("SELECT 1 FROM DUAL").scalar()
            assert result == 1

    @requires_oracle_connection
    def test_complete_data_pipeline(self, oracle_config, sample_schema, sample_records):
        """Test complete data pipeline from Singer messages to Oracle."""
        target = OracleTarget(config=oracle_config)

        # Prepare input messages
        messages = [sample_schema] + sample_records

        # Add a STATE message
        messages.append(
            {
                "type": "STATE",
                "value": {
                    "bookmarks": {
                        "test_orders": {
                            "replication_key": "order_date",
                            "replication_key_value": "2025-01-02",
                        }
                    }
                },
            }
        )

        input_data = "\n".join(json.dumps(msg) for msg in messages)

        # Process messages
        with StringIO():
            target.listen(file_input=StringIO(input_data))

        # Verify data was loaded
        sink = target.get_sink("test_orders")
        with sink.connector._conn.begin() as conn:
            # Check record count
            count_result = conn.execute(
                f"SELECT COUNT(*) FROM {sink.full_table_name}"
            ).scalar()
            assert count_result == 2

            # Check specific record
            order_result = conn.execute(
                f"""
                SELECT order_id, customer_id, order_status, total_amount, is_priority
                FROM {sink.full_table_name}
                WHERE order_id = 1001
                """
            ).fetchone()

            assert order_result is not None
            assert order_result[0] == 1001  # order_id
            assert order_result[1] == 201  # customer_id
            assert order_result[2] == "completed"
            assert float(order_result[3]) == 1250.50
            assert order_result[4] == 1  # boolean as 1/0

            # Check metadata columns if enabled
            if oracle_config.get("add_record_metadata", True):
                metadata_result = conn.execute(
                    f"""
                    SELECT _SDC_EXTRACTED_AT, _SDC_BATCHED_AT, _SDC_RECEIVED_AT
                    FROM {sink.full_table_name}
                    WHERE order_id = 1001
                    """
                ).fetchone()

                assert metadata_result is not None
                assert all(col is not None for col in metadata_result)

    @requires_oracle_connection
    def test_upsert_functionality(self, oracle_config, sample_schema):
        """Test UPSERT (MERGE) functionality."""
        # Enable upsert mode
        oracle_config["load_method"] = "upsert"
        target = OracleTarget(config=oracle_config)

        # Initial records
        initial_records = [
            {
                "type": "RECORD",
                "stream": "test_orders",
                "record": {
                    "order_id": 2001,
                    "customer_id": 301,
                    "order_date": "2025-01-01",
                    "order_status": "pending",
                    "total_amount": 500.00,
                    "is_priority": False,
                    "items": [],
                    "shipping_address": {
                        "street": "789 Elm",
                        "city": "Houston",
                        "state": "TX",
                        "zip": "77001",
                    },
                    "notes": "Initial order",
                },
            }
        ]

        # Process initial load
        messages = [sample_schema] + initial_records
        input_data = "\n".join(json.dumps(msg) for msg in messages)
        target.listen(file_input=StringIO(input_data))

        # Update record
        updated_records = [
            {
                "type": "RECORD",
                "stream": "test_orders",
                "record": {
                    "order_id": 2001,  # Same ID
                    "customer_id": 301,
                    "order_date": "2025-01-01",
                    "order_status": "completed",  # Updated
                    "total_amount": 600.00,  # Updated
                    "is_priority": True,  # Updated
                    "items": [{"product_id": 201, "quantity": 2, "price": 300.00}],
                    "shipping_address": {
                        "street": "789 Elm",
                        "city": "Houston",
                        "state": "TX",
                        "zip": "77001",
                    },
                    "notes": "Updated order",  # Updated
                },
            }
        ]

        # Process update
        messages = [sample_schema] + updated_records
        input_data = "\n".join(json.dumps(msg) for msg in messages)
        target.listen(file_input=StringIO(input_data))

        # Verify update
        sink = target.get_sink("test_orders")
        with sink.connector._conn.begin() as conn:
            # Should still have only 1 record
            count_result = conn.execute(
                f"SELECT COUNT(*) FROM {sink.full_table_name}"
            ).scalar()
            assert count_result == 1

            # Check updated values
            result = conn.execute(
                f"""
                SELECT order_status, total_amount, is_priority, notes
                FROM {sink.full_table_name}
                WHERE order_id = 2001
                """
            ).fetchone()

            assert result[0] == "completed"
            assert float(result[1]) == 600.00
            assert result[2] == 1  # True as 1
            assert result[3] == "Updated order"

    @requires_oracle_connection
    def test_data_type_handling(self, oracle_config):
        """Test various data type conversions."""
        target = OracleTarget(config=oracle_config)

        # Schema with various data types
        schema = {
            "type": "SCHEMA",
            "stream": "test_types",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "text_short": {"type": "string", "maxLength": 100},
                    "text_long": {"type": "string", "maxLength": 5000},
                    "number_int": {"type": "integer"},
                    "number_float": {"type": "number"},
                    "date_field": {"type": "string", "format": "date"},
                    "datetime_field": {"type": "string", "format": "date-time"},
                    "boolean_field": {"type": "boolean"},
                    "json_field": {"type": "object"},
                    "array_field": {"type": "array"},
                    "nullable_field": {"type": ["string", "null"]},
                },
            },
            "key_properties": ["id"],
        }

        # Test records
        records = [
            {
                "type": "RECORD",
                "stream": "test_types",
                "record": {
                    "id": 1,
                    "text_short": "Short text",
                    "text_long": "A" * 4500,  # Long text
                    "number_int": 42,
                    "number_float": 3.14159,
                    "date_field": "2025-01-01",
                    "datetime_field": "2025-01-01T12:30:45Z",
                    "boolean_field": True,
                    "json_field": {"key": "value", "nested": {"data": 123}},
                    "array_field": ["item1", "item2", "item3"],
                    "nullable_field": "not null",
                },
            },
            {
                "type": "RECORD",
                "stream": "test_types",
                "record": {
                    "id": 2,
                    "text_short": "Another",
                    "text_long": "Short",
                    "number_int": -100,
                    "number_float": -99.99,
                    "date_field": "2025-01-02",
                    "datetime_field": "2025-01-02T00:00:00Z",
                    "boolean_field": False,
                    "json_field": {},
                    "array_field": [],
                    "nullable_field": None,  # Test null
                },
            },
        ]

        # Process
        messages = [schema] + records
        input_data = "\n".join(json.dumps(msg) for msg in messages)
        target.listen(file_input=StringIO(input_data))

        # Verify
        sink = target.get_sink("test_types")
        with sink.connector._conn.begin() as conn:
            results = conn.execute(
                f"""
                SELECT id, text_short, LENGTH(text_long), number_int, number_float,
                       boolean_field, json_field, array_field, nullable_field
                FROM {sink.full_table_name}
                ORDER BY id
                """
            ).fetchall()

            assert len(results) == 2

            # Check first record
            assert results[0][0] == 1
            assert results[0][1] == "Short text"
            assert results[0][2] == 4500  # Length of long text
            assert results[0][3] == 42
            assert float(results[0][4]) == pytest.approx(3.14159, rel=1e-5)
            assert results[0][5] == 1  # True as 1
            assert json.loads(results[0][6]) == {
                "key": "value",
                "nested": {"data": 123},
            }
            assert json.loads(results[0][7]) == ["item1", "item2", "item3"]
            assert results[0][8] == "not null"

            # Check second record (with null)
            assert results[1][0] == 2
            assert results[1][5] == 0  # False as 0
            assert results[1][8] is None  # Null value

    @requires_oracle_connection
    def test_batch_performance(self, oracle_config):
        """Test batch processing performance."""
        # Configure for larger batches
        oracle_config["batch_config"]["batch_size"] = 1000
        oracle_config["use_bulk_operations"] = True
        oracle_config["array_size"] = 1000

        target = OracleTarget(config=oracle_config)

        # Schema
        schema = {
            "type": "SCHEMA",
            "stream": "test_batch_perf",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "value": {"type": "number"},
                    "category": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"},
                },
            },
            "key_properties": ["id"],
        }

        # Generate many records
        messages = [schema]
        for i in range(1000):
            messages.append(
                {
                    "type": "RECORD",
                    "stream": "test_batch_perf",
                    "record": {
                        "id": i + 1,
                        "value": float(i * 10.5),
                        "category": f"CAT_{i % 10}",
                        "created_at": datetime.now(timezone.utc).isoformat(),
                    },
                }
            )

        # Time the processing
        import time

        start_time = time.time()

        input_data = "\n".join(json.dumps(msg) for msg in messages)
        target.listen(file_input=StringIO(input_data))

        elapsed_time = time.time() - start_time

        # Verify all records loaded
        sink = target.get_sink("test_batch_perf")
        with sink.connector._conn.begin() as conn:
            count = conn.execute(
                f"SELECT COUNT(*) FROM {sink.full_table_name}"
            ).scalar()
            assert count == 1000

        # Performance assertion (should process 1000 records in reasonable time)
        assert elapsed_time < 30.0  # Should complete in less than 30 seconds
        print(f"Processed 1000 records in {elapsed_time:.2f} seconds")

    @requires_oracle_connection
    def test_error_handling(self, oracle_config):
        """Test error handling and recovery."""
        target = OracleTarget(config=oracle_config)

        # Schema with constraints
        schema = {
            "type": "SCHEMA",
            "stream": "test_errors",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "required_field": {"type": "string"},
                    "positive_number": {"type": "number"},
                },
            },
            "key_properties": ["id"],
        }

        # Valid record first
        valid_record = {
            "type": "RECORD",
            "stream": "test_errors",
            "record": {"id": 1, "required_field": "valid", "positive_number": 10.0},
        }

        # Process valid record
        messages = [schema, valid_record]
        input_data = "\n".join(json.dumps(msg) for msg in messages)
        target.listen(file_input=StringIO(input_data))

        # Invalid records (various error conditions)
        # Note: Singer SDK validates schema, so we test database-level errors

        # Duplicate key (if we try to insert same ID)
        duplicate_record = {
            "type": "RECORD",
            "stream": "test_errors",
            "record": {
                "id": 1,  # Duplicate
                "required_field": "duplicate",
                "positive_number": 20.0,
            },
        }

        # In append-only mode, duplicates should fail or be handled
        # depending on configuration
        messages = [schema, duplicate_record]
        input_data = "\n".join(json.dumps(msg) for msg in messages)

        # This might raise an error or handle it gracefully
        # depending on error handling configuration
        try:
            target.listen(file_input=StringIO(input_data))
        except Exception:
            # Expected for duplicate key in append-only mode
            pass

        # Verify original record is still there
        sink = target.get_sink("test_errors")
        with sink.connector._conn.begin() as conn:
            count = conn.execute(
                f"SELECT COUNT(*) FROM {sink.full_table_name}"
            ).scalar()
            assert count >= 1  # At least the valid record

    @requires_oracle_connection
    def test_cleanup(self, oracle_config):
        """Clean up test tables after tests."""
        target = OracleTarget(config=oracle_config)

        test_tables = [
            "test_orders",
            "test_types",
            "test_batch_perf",
            "test_errors",
            "test_connection",
        ]

        for table_name in test_tables:
            try:
                sink = target.get_sink(table_name)
                with sink.connector._conn.begin() as conn:
                    # Use proper schema prefix if configured
                    full_table = sink.full_table_name
                    conn.execute(f"DROP TABLE {full_table}")
                    print(f"Dropped table: {full_table}")
            except Exception as e:
                # Table might not exist, which is fine
                print(f"Could not drop table {table_name}: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
