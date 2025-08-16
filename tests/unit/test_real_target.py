"""Real Oracle Target Tests - Using Docker Oracle Container.

Tests target functionality against a real Oracle container for maximum coverage.
"""

import json
from datetime import UTC, datetime
from typing import Any

import pytest
from sqlalchemy import text

from flext_target_oracle import FlextOracleTarget, FlextOracleTargetConfig, LoadMethod
from flext_target_oracle.exceptions import (
    FlextOracleTargetProcessingError,
    FlextOracleTargetSchemaError,
)


@pytest.mark.oracle
class TestRealOracleTarget:
    """Test Oracle target with real database connection."""

    @pytest.fixture
    def real_target(self, oracle_config: object) -> object:
        """Create real target instance."""
        return FlextOracleTarget(config=oracle_config)

    def test_real_initialize(self, real_target: object) -> None:
        """Test real target initialization."""
        result = real_target.initialize()
        assert result.is_success

        # Should set start time
        assert real_target._start_time is not None

        # Should initialize loader
        assert real_target._loader is not None

    def test_real_discover_catalog(self, real_target) -> None:
        """Test catalog discovery."""
        real_target.initialize()

        result = real_target.discover_catalog()
        assert result.is_success

        catalog = result.value
        assert catalog["type"] == "CATALOG"
        assert "streams" in catalog
        assert len(catalog["streams"]) == 0  # No streams initially

    def test_real_validate_configuration(self, real_target) -> None:
        """Test configuration validation."""
        result = real_target.validate_configuration()
        assert result.is_success

        validation = result.value
        assert validation["valid"] is True
        assert "connection" in validation["components"]
        assert "schema" in validation["components"]

    def test_real_process_schema_message(self, real_target, simple_schema) -> None:
        """Test processing schema message."""
        real_target.initialize()

        schema_msg = {
            "type": "SCHEMA",
            "stream": "test_stream",
            "schema": simple_schema["schema"],
            "key_properties": simple_schema["key_properties"],
        }

        result = real_target.execute(json.dumps(schema_msg))
        assert result.is_success

        # Schema should be stored
        assert "test_stream" in real_target._stream_schemas
        assert (
            real_target._stream_schemas["test_stream"]["schema"]
            == simple_schema["schema"]
        )

    @pytest.mark.asyncio
    async def test_real_process_record_message(
        self,
        real_target,
        simple_schema,
        oracle_engine,
    ) -> None:
        """Test processing record message with real database."""
        real_target.initialize()

        # First send schema
        schema_msg = {
            "type": "SCHEMA",
            "stream": "users",
            "schema": simple_schema["schema"],
            "key_properties": simple_schema["key_properties"],
        }
        result = real_target.execute(json.dumps(schema_msg))
        assert result.is_success

        # Then send record
        record_msg = {
            "type": "RECORD",
            "stream": "users",
            "record": {
                "id": 1,
                "name": "Test User",
                "email": "test@example.com",
            },
            "time_extracted": datetime.now(UTC).isoformat(),
        }
        result = real_target.execute(json.dumps(record_msg))
        assert result.is_success

        # Send state to flush
        state_msg = {
            "type": "STATE",
            "value": {"bookmarks": {"users": {"version": 1}}},
        }
        result = real_target.execute(json.dumps(state_msg))
        assert result.is_success

        # Verify in database
        with oracle_engine.connect() as conn:
            count = conn.execute(text("SELECT COUNT(*) FROM users")).scalar()
            assert count == 1

    def test_real_process_state_message(self, real_target) -> None:
        """Test processing state message."""
        real_target.initialize()

        state_msg = {
            "type": "STATE",
            "value": {
                "bookmarks": {
                    "stream1": {"replication_key_value": "2023-01-01", "version": 1},
                    "stream2": {"version": 2},
                },
            },
        }

        result = real_target.execute(json.dumps(state_msg))
        assert result.is_success

        # State should be emitted (check via logs or return value)

    def test_real_process_activate_version_message(self, real_target) -> None:
        """Test processing ACTIVATE_VERSION message."""
        real_target.initialize()

        activate_msg = {
            "type": "ACTIVATE_VERSION",
            "stream": "test_stream",
            "version": 2,
        }

        result = real_target.execute(json.dumps(activate_msg))
        assert result.is_success

    def test_real_batch_processing(
        self,
        real_target,
        simple_schema,
        oracle_engine,
    ) -> None:
        """Test batch processing with real database."""
        real_target.initialize()

        # Send schema
        schema_msg = {
            "type": "SCHEMA",
            "stream": "batch_test",
            "schema": simple_schema["schema"],
            "key_properties": simple_schema["key_properties"],
        }
        real_target.execute(json.dumps(schema_msg))

        # Send multiple records
        for i in range(10):
            record_msg = {
                "type": "RECORD",
                "stream": "batch_test",
                "record": {
                    "id": i + 1,
                    "name": f"User {i + 1}",
                    "email": f"user{i + 1}@example.com",
                },
                "time_extracted": datetime.now(UTC).isoformat(),
            }
            result = real_target.execute(json.dumps(record_msg))
            assert result.is_success

        # Flush with state
        state_msg = {"type": "STATE", "value": {}}
        real_target.execute(json.dumps(state_msg))

        # Verify all records
        with oracle_engine.connect() as conn:
            count = conn.execute(text("SELECT COUNT(*) FROM batch_test")).scalar()
            assert count == 10

    def test_real_column_mapping(
        self,
        real_target,
        simple_schema,
        oracle_engine,
    ) -> None:
        """Test column mapping with real database."""
        # Configure column mappings
        real_target.config.column_mappings = {
            "mapping_test": {
                "name": "full_name",
                "email": "email_address",
            },
        }

        real_target.initialize()

        # Send schema
        schema_msg = {
            "type": "SCHEMA",
            "stream": "mapping_test",
            "schema": simple_schema["schema"],
            "key_properties": simple_schema["key_properties"],
        }
        real_target.execute(json.dumps(schema_msg))

        # Send record
        record_msg = {
            "type": "RECORD",
            "stream": "mapping_test",
            "record": {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
            },
        }
        real_target.execute(json.dumps(record_msg))

        # Flush
        real_target.execute(json.dumps({"type": "STATE", "value": {}}))

        # Verify mapped columns
        with oracle_engine.connect() as conn:
            result = conn.execute(
                text(
                    """
                    SELECT column_name
                    FROM user_tab_columns
                    WHERE table_name = 'MAPPING_TEST'
                    """,
                ),
            )
            columns = [row[0] for row in result]

            assert "FULL_NAME" in columns  # Mapped from 'name'
            assert "EMAIL_ADDRESS" in columns  # Mapped from 'email'
            assert "NAME" not in columns  # Original name not present
            assert "EMAIL" not in columns  # Original email not present

    def test_real_ignored_columns(self, real_target, oracle_engine) -> None:
        """Test ignored columns with real database."""
        # Configure ignored columns
        real_target.config.ignored_columns = ["password", "internal_id"]

        real_target.initialize()

        # Send schema with ignored columns
        schema_msg = {
            "type": "SCHEMA",
            "stream": "ignore_test",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "username": {"type": "string"},
                    "password": {"type": "string"},  # Should be ignored
                    "internal_id": {"type": "string"},  # Should be ignored
                },
            },
            "key_properties": ["id"],
        }
        real_target.execute(json.dumps(schema_msg))

        # Send record
        record_msg = {
            "type": "RECORD",
            "stream": "ignore_test",
            "record": {
                "id": 1,
                "username": "testuser",
                "password": "secret123",
                "internal_id": "INT-001",
            },
        }
        real_target.execute(json.dumps(record_msg))

        # Flush
        real_target.execute(json.dumps({"type": "STATE", "value": {}}))

        # Verify ignored columns not in table
        with oracle_engine.connect() as conn:
            result = conn.execute(
                text(
                    """
                    SELECT column_name
                    FROM user_tab_columns
                    WHERE table_name = 'IGNORE_TEST'
                    """,
                ),
            )
            columns = [row[0] for row in result]

            assert "PASSWORD" not in columns
            assert "INTERNAL_ID" not in columns
            assert "USERNAME" in columns

    def test_real_nested_json_handling(
        self,
        real_target,
        nested_schema,
        oracle_engine,
    ) -> None:
        """Test nested JSON handling with real database."""
        real_target.initialize()

        # Send schema
        schema_msg = {
            "type": "SCHEMA",
            "stream": "nested_test",
            "schema": nested_schema["schema"],
            "key_properties": nested_schema["key_properties"],
        }
        real_target.execute(json.dumps(schema_msg))

        # Send nested record
        record_msg = {
            "type": "RECORD",
            "stream": "nested_test",
            "record": {
                "order_id": "ORD-001",
                "customer": {
                    "id": 123,
                    "name": "John Doe",
                    "address": {
                        "street": "123 Main St",
                        "city": "Anytown",
                    },
                },
                "items": [
                    {"sku": "ITEM-1", "quantity": 2},
                ],
                "total": 99.99,
            },
        }
        real_target.execute(json.dumps(record_msg))

        # Flush
        real_target.execute(json.dumps({"type": "STATE", "value": {}}))

        # Verify flattened structure
        with oracle_engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM nested_test WHERE order_id = 'ORD-001'"),
            )
            row = result.fetchone()
            assert row is not None

            # Check flattened columns exist
            result = conn.execute(
                text(
                    """
                    SELECT column_name
                    FROM user_tab_columns
                    WHERE table_name = 'NESTED_TEST'
                    AND column_name LIKE 'CUSTOMER__%'
                    """,
                ),
            )
            customer_cols = [row[0] for row in result]
            assert len(customer_cols) > 0

    def test_real_error_handling_invalid_json(self, real_target) -> None:
        """Test error handling with invalid JSON."""
        real_target.initialize()

        # Send invalid JSON
        result = real_target.execute("{ invalid json }")
        assert result.is_failure
        assert isinstance(result.error, FlextOracleTargetProcessingError)

    def test_real_error_handling_missing_stream(self, real_target) -> None:
        """Test error handling with missing stream in record."""
        real_target.initialize()

        # Send record without schema
        record_msg = {
            "type": "RECORD",
            "stream": "unknown_stream",
            "record": {"id": 1},
        }

        result = real_target.execute(json.dumps(record_msg))
        assert result.is_failure
        assert isinstance(result.error, FlextOracleTargetSchemaError)

    def test_real_metrics_collection(
        self,
        real_target,
        simple_schema,
        oracle_engine,
    ) -> None:
        """Test metrics collection with real processing."""
        real_target.initialize()

        # Process some data
        schema_msg = {
            "type": "SCHEMA",
            "stream": "metrics_test",
            "schema": simple_schema["schema"],
            "key_properties": simple_schema["key_properties"],
        }
        real_target.execute(json.dumps(schema_msg))

        # Send records
        for i in range(5):
            record_msg = {
                "type": "RECORD",
                "stream": "metrics_test",
                "record": {
                    "id": i + 1,
                    "name": f"User {i + 1}",
                    "email": f"user{i + 1}@example.com",
                },
            }
            real_target.execute(json.dumps(record_msg))

        # Get metrics
        result = real_target.get_implementation_metrics()
        assert result.is_success

        metrics = result.value
        assert metrics["records_processed"] >= 5
        assert metrics["streams_processed"] >= 1
        assert "elapsed_time" in metrics
        assert metrics["status"] == "running"

    def test_real_connection_pooling(self, oracle_engine) -> None:
        """Test connection pooling configuration."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service="XE",
            oracle_user="FLEXT_TEST",
            oracle_password="test_password",
            default_target_schema="FLEXT_TEST",
            enable_connection_pool=True,
            pool_size=5,
            pool_max_overflow=10,
        )

        target = FlextOracleTarget(config=config)
        result = target.initialize()
        assert result.is_success

    def test_real_ssl_configuration(self) -> None:
        """Test SSL/TLS configuration."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service="XE",
            oracle_user="FLEXT_TEST",
            oracle_password="test_password",
            default_target_schema="FLEXT_TEST",
            use_ssl=True,
            ssl_verify_cert=False,
        )

        target = FlextOracleTarget(config=config)
        # SSL connection would fail with test container, but config is valid
        assert target.config.use_ssl is True

    def test_real_type_mapping_customization(self, real_target, oracle_engine) -> None:
        """Test custom type mapping with real database."""
        # Configure custom type mappings
        real_target.config.type_mapping = {
            "string": "VARCHAR2(4000)",  # Larger strings
            "number": "NUMBER(38,10)",  # More precision
            "boolean": "CHAR(1)",  # Use CHAR instead of NUMBER
        }

        real_target.initialize()

        # Send schema
        schema_msg = {
            "type": "SCHEMA",
            "stream": "type_mapping_test",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "description": {"type": "string"},
                    "amount": {"type": "number"},
                    "is_active": {"type": "boolean"},
                },
            },
            "key_properties": ["id"],
        }
        real_target.execute(json.dumps(schema_msg))

        # Verify column types
        with oracle_engine.connect() as conn:
            result = conn.execute(
                text(
                    """
                    SELECT column_name, data_type, data_length, data_precision, data_scale
                    FROM user_tab_columns
                    WHERE table_name = 'TYPE_MAPPING_TEST'
                    """,
                ),
            )
            columns = {row[0]: row for row in result}

            # Check custom mappings applied
            assert columns["DESCRIPTION"][1] == "VARCHAR2"
            assert columns["DESCRIPTION"][2] == 4000  # Custom length

            assert columns["AMOUNT"][1] == "NUMBER"
            assert columns["AMOUNT"][3] == 38  # Custom precision
            assert columns["AMOUNT"][4] == 10  # Custom scale

            assert columns["IS_ACTIVE"][1] == "CHAR"
            assert columns["IS_ACTIVE"][2] == 1

    def test_real_write_state_messages(self, real_target: Any, capfd: Any) -> None:
        """Test write_state behavior."""
        real_target.initialize()

        # Write state should emit to stdout
        state = {"bookmarks": {"test": {"version": 1}}}
        real_target.write_state(state)

        captured = capfd.readouterr()
        assert '{"type": "STATE"' in captured.out
        assert '"bookmarks"' in captured.out

    def test_real_compatibility_methods(self, real_target) -> None:
        """Test Singer compatibility methods."""
        real_target.initialize()

        # Test write_record
        record = {"id": 1, "name": "test"}
        result = real_target.write_record(record, "test_stream", None)
        assert result.is_failure  # No schema

        # Test write_records
        records = [{"id": 1}, {"id": 2}]
        result = real_target.write_records("test_stream", records)
        assert result.is_failure  # No schema

        # Test test_connection
        result = real_target.test_connection()
        assert result.is_success

    def test_real_large_batch_processing(
        self,
        real_target,
        simple_schema,
        oracle_engine,
    ) -> None:
        """Test processing large batches with real database."""
        # Configure for large batches
        real_target.config.batch_size = 1000
        real_target.config.load_method = LoadMethod.BULK_INSERT

        real_target.initialize()

        # Send schema
        schema_msg = {
            "type": "SCHEMA",
            "stream": "large_batch",
            "schema": simple_schema["schema"],
            "key_properties": simple_schema["key_properties"],
        }
        real_target.execute(json.dumps(schema_msg))

        # Send many records
        for i in range(2500):  # More than 2 batches
            record_msg = {
                "type": "RECORD",
                "stream": "large_batch",
                "record": {
                    "id": i + 1,
                    "name": f"User {i + 1}",
                    "email": f"user{i + 1}@example.com",
                },
            }
            real_target.execute(json.dumps(record_msg))

        # Flush
        real_target.execute(json.dumps({"type": "STATE", "value": {}}))

        # Verify all records
        with oracle_engine.connect() as conn:
            count = conn.execute(text("SELECT COUNT(*) FROM large_batch")).scalar()
            assert count == 2500

    def test_real_schema_evolution(self, real_target, oracle_engine) -> None:
        """Test schema evolution with real database."""
        # Enable schema evolution
        real_target.config.allow_alter_table = True

        real_target.initialize()

        # Initial schema
        schema_v1 = {
            "type": "SCHEMA",
            "stream": "evolving_table",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                },
            },
            "key_properties": ["id"],
        }
        real_target.execute(json.dumps(schema_v1))

        # Insert initial data
        record_v1 = {
            "type": "RECORD",
            "stream": "evolving_table",
            "record": {"id": 1, "name": "Initial"},
        }
        real_target.execute(json.dumps(record_v1))
        real_target.execute(json.dumps({"type": "STATE", "value": {}}))

        # Evolved schema with new column
        schema_v2 = {
            "type": "SCHEMA",
            "stream": "evolving_table",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "email": {"type": "string"},  # New column
                },
            },
            "key_properties": ["id"],
        }
        real_target.execute(json.dumps(schema_v2))

        # Insert data with new column
        record_v2 = {
            "type": "RECORD",
            "stream": "evolving_table",
            "record": {"id": 2, "name": "Evolved", "email": "evolved@example.com"},
        }
        real_target.execute(json.dumps(record_v2))
        real_target.execute(json.dumps({"type": "STATE", "value": {}}))

        # Verify schema evolution
        with oracle_engine.connect() as conn:
            # Check new column exists
            result = conn.execute(
                text(
                    """
                    SELECT COUNT(*)
                    FROM user_tab_columns
                    WHERE table_name = 'EVOLVING_TABLE'
                    AND column_name = 'EMAIL'
                    """,
                ),
            )
            assert result.scalar() == 1

            # Check both records exist
            count = conn.execute(text("SELECT COUNT(*) FROM evolving_table")).scalar()
            assert count == 2
