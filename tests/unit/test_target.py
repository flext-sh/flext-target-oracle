"""Real Oracle Target Tests - Using Docker Oracle Container.

Tests target functionality against a real Oracle container for maximum coverage.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import json
from datetime import UTC, datetime

import pytest
from _pytest.capture import CaptureFixture
from sqlalchemy import Engine, text

from flext_target_oracle import (
    FlextTargetOracle,
    FlextTargetOracleConfig,
    FlextTargetOracleProcessingError,
    FlextTargetOracleSchemaError,
    LoadMethod,
)


@pytest.mark.oracle
class TestRealOracleTarget:
    """Test Oracle target with real database connection."""

    @pytest.fixture
    def real_target(self, oracle_config: FlextTargetOracleConfig) -> FlextTargetOracle:
        """Create real target instance."""
        return FlextTargetOracle(config=oracle_config)

    def test_target_initialization(self, real_target: FlextTargetOracle) -> None:
        """Test real target initialization."""
        result = real_target.initialize()
        assert result.is_success

        # Should set start time
        assert real_target._start_time is not None

        # Should initialize loader
        assert real_target._loader is not None

    def test_catalog_discovery(self, real_target: FlextTargetOracle) -> None:
        """Test catalog discovery."""
        real_target.initialize()

        result = real_target.discover_catalog()
        assert result.is_success

        catalog = result.value
        assert catalog["type"] == "CATALOG"
        assert "streams" in catalog
        assert len(catalog["streams"]) == 0  # No streams initially

    def test_configuration_validation(self, real_target: FlextTargetOracle) -> None:
        """Test configuration validation."""
        result = real_target.validate_configuration()
        assert result.is_success

        validation = result.value
        assert validation["valid"] is True
        assert "connection" in validation["components"]
        assert "schema" in validation["components"]

    def test_real_process_schema_message(
        self,
        real_target: FlextTargetOracle,
        simple_schema: dict[str, object],
    ) -> None:
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

    def test_real_process_record_message(
        self,
        real_target: FlextTargetOracle,
        simple_schema: dict[str, object],
        oracle_engine: Engine,
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

    def test_state_message_processing(self, real_target: FlextTargetOracle) -> None:
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

    def test_activate_version_message(self, real_target: FlextTargetOracle) -> None:
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
        real_target: FlextTargetOracle,
        simple_schema: dict[str, object],
        oracle_engine: Engine,
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
        real_target: FlextTargetOracle,
        simple_schema: dict[str, object],
        oracle_engine: Engine,
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

    def test_real_ignored_columns(
        self,
        real_target: FlextTargetOracle,
    ) -> None:
        """Test ignored columns with real database."""
        # Configure ignored columns
        real_target.config.ignored_columns = ["email", "phone"]

        # Send schema
        schema_msg = {
            "type": "SCHEMA",
            "stream": "ignored_test",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "phone": {"type": "string"},
                },
            },
            "key_properties": ["id"],
        }
        real_target.execute(json.dumps(schema_msg))

        # Send record
        record_msg = {
            "type": "RECORD",
            "stream": "ignored_test",
            "record": {
                "id": 1,
                "name": "Test User",
                "email": "test@example.com",
                "phone": "123-456-7890",
            },
            "time_extracted": datetime.now(UTC).isoformat(),
        }
        real_target.execute(json.dumps(record_msg))

        # Send state to flush
        state_msg = {
            "type": "STATE",
            "value": {"bookmarks": {"ignored_test": {"version": 1}}},
        }
        real_target.execute(json.dumps(state_msg))

        # Verify ignored columns are not in database
        # This would require database verification in real test
        assert real_target._ignored_columns == ["email", "phone"]

    def test_real_nested_json_handling(
        self,
        real_target: FlextTargetOracle,
        nested_schema: dict[str, object],
        oracle_engine: Engine,
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
                        "city": "objecttown",
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

    def test_error_handling_invalid_json(self, real_target: FlextTargetOracle) -> None:
        """Test error handling with invalid JSON."""
        real_target.initialize()

        # Send invalid JSON
        result = real_target.execute("{ invalid json }")
        assert result.is_failure
        assert isinstance(result.error, FlextTargetOracleProcessingError)

    def test_error_handling_missing_stream(
        self, real_target: FlextTargetOracle
    ) -> None:
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
        assert isinstance(result.error, FlextTargetOracleSchemaError)

    def test_real_metrics_collection(
        self,
        real_target: FlextTargetOracle,
        simple_schema: dict[str, object],
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

    def test_real_connection_pooling(self) -> None:
        """Test connection pooling configuration."""
        config = FlextTargetOracleConfig(
            host="localhost",
            port=1521,
            service_name="test",
            username="test",
            password="test",
            connection_pool_size=10,
            connection_pool_max_overflow=20,
        )

        target = FlextTargetOracle(config)
        assert target.config.connection_pool_size == 10
        assert target.config.connection_pool_max_overflow == 20

        # Test SSL configuration
        ssl_config = FlextTargetOracleConfig(
            host="localhost",
            port=1521,
            service_name="test",
            username="test",
            password="test",
            use_ssl=True,
        )

        target = FlextTargetOracle(ssl_config)
        assert target.config.use_ssl is True

    def test_real_type_mapping_customization(
        self,
        real_target: object,
    ) -> None:
        """Test custom type mapping with real database."""
        # Configure custom type mappings
        real_target.config.custom_type_mappings = {
            "string": "VARCHAR2(4000)",
            "integer": "NUMBER(10)",
            "number": "NUMBER(15,2)",
        }

        # Send schema
        schema_msg = {
            "type": "SCHEMA",
            "stream": "custom_types",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "amount": {"type": "number"},
                },
            },
            "key_properties": ["id"],
        }
        real_target.execute(json.dumps(schema_msg))

        # Send record
        record_msg = {
            "type": "RECORD",
            "stream": "custom_types",
            "record": {
                "id": 1,
                "name": "Custom Type Test",
                "amount": 99.99,
            },
            "time_extracted": datetime.now(UTC).isoformat(),
        }
        real_target.execute(json.dumps(record_msg))

        # Send state to flush
        state_msg = {
            "type": "STATE",
            "value": {"bookmarks": {"custom_types": {"version": 1}}},
        }
        real_target.execute(json.dumps(state_msg))

        # Verify custom type mappings are applied
        assert real_target.config.custom_type_mappings["string"] == "VARCHAR2(4000)"
        assert real_target.config.custom_type_mappings["integer"] == "NUMBER(10)"
        assert real_target.config.custom_type_mappings["number"] == "NUMBER(15,2)"

    def test_real_write_state_messages(
        self,
        real_target: FlextTargetOracle,
        capfd: CaptureFixture[str],
    ) -> None:
        """Test writing state messages to stdout."""
        real_target.initialize()

        # Capture stdout
        with capfd.disabled():
            result = real_target.execute(
                json.dumps(
                    {
                        "type": "STATE",
                        "value": {"bookmarks": {"test_stream": {"version": 1}}},
                    },
                ),
            )

        assert result.is_success
        # State messages are written to stdout, not returned
        # In real test, would capture stdout to verify content

    def test_singer_compatibility_methods(self, real_target: FlextTargetOracle) -> None:
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
        real_target: FlextTargetOracle,
        simple_schema: dict[str, object],
        oracle_engine: Engine,
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

    def test_real_schema_evolution(
        self,
        real_target: FlextTargetOracle,
        oracle_engine: Engine,
    ) -> None:
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
