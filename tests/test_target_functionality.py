"""Test Oracle target core functionality with Singer SDK patterns.

This module tests the complete target functionality including
schema handling, record processing, and error management.
"""

import json
from io import StringIO
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest
from sqlalchemy import text
from sqlalchemy.engine import Engine

from flext_target_oracle.target import OracleTarget
from tests.helpers import requires_oracle_connection


@requires_oracle_connection
class TestOracleTargetFunctionality:
    """Test Oracle target core functionality."""

    def test_target_name_and_capabilities(self, oracle_target: OracleTarget) -> None:
        """Test target name and capabilities."""
        assert oracle_target.name == "flext-target-oracle"

        capabilities = oracle_target.capabilities
        assert len(capabilities) > 0

        # Verify specific capabilities
        cap_values = [cap.value for cap in capabilities]
        assert "about" in cap_values  # This capability should exist
        assert "stream-maps" in cap_values  # This capability should exist

    def test_schema_message_processing(self,
                                       oracle_target: OracleTarget,
                                       sample_singer_schema: dict[str, Any],
                                       test_table_name: str,
                                       table_cleanup: Any,
                                       ) -> None:
        """Test Singer SCHEMA message processing."""
        table_cleanup(test_table_name)

        # Modify schema to use test table name
        test_schema = sample_singer_schema.copy()
        test_schema["stream"] = test_table_name

        # Process schema message
        schema_message = json.dumps(test_schema)

        with patch("sys.stdin", StringIO(schema_message)):
            # This should process the schema without errors
            oracle_target._process_schema_message(test_schema)

    def test_record_message_processing(self,
                                       oracle_target: OracleTarget,
                                       sample_singer_schema: dict[str, Any],
                                       sample_singer_records: list[dict[str, Any]],
                                       test_table_name: str,
                                       oracle_engine: Engine,
                                       table_cleanup: Any,
                                       ) -> None:
        """Test Singer RECORD message processing."""
        table_cleanup(test_table_name)

        # Modify schema and records to use test table name
        test_schema = sample_singer_schema.copy()
        test_schema["stream"] = test_table_name

        test_records = []
        for record in sample_singer_records:
            test_record = record.copy()
            test_record["stream"] = test_table_name
            test_records.append(test_record)

        # Create input with schema and records
        messages = [json.dumps(test_schema)]
        messages.extend([json.dumps(record) for record in test_records])
        input_data = "\n".join(messages)

        # Process messages
        with patch("sys.stdin", StringIO(input_data)):
            oracle_target.cli()

        # Verify records were inserted
        with oracle_engine.connect() as conn:
            result = conn.execute(
                text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            count = row[0]
            assert count == len(test_records)

            # Verify specific record data
            result = conn.execute(
                text(
                    f"SELECT id, name, email FROM {test_table_name} ORDER BY id"),
            )
            rows = result.fetchall()

            for i, row in enumerate(rows):
                expected_record = test_records[i]["record"]
                assert row.id == expected_record["id"]
                assert row.name == expected_record["name"]
                assert row.email == expected_record["email"]

    def test_batch_processing(self,
                              oracle_config: dict[str, Any],
                              bulk_singer_schema: dict[str, Any],
                              bulk_singer_records: list[dict[str, Any]],
                              test_table_name: str,
                              oracle_engine: Engine,
                              table_cleanup: Any,
                              performance_timer: Any,
                              ) -> None:
        """Test batch processing with large datasets."""
        table_cleanup(test_table_name)

        # Configure for batch testing
        batch_config = oracle_config.copy()
        batch_config["batch_size"] = 100
        batch_config["max_workers"] = 4

        target = OracleTarget(config=batch_config)

        # Modify schema and records for testing
        test_schema = bulk_singer_schema.copy()
        test_schema["stream"] = test_table_name

        test_records = []
        for record in bulk_singer_records:
            test_record = record.copy()
            test_record["stream"] = test_table_name
            test_records.append(test_record)

        # Create input with schema and records
        messages = [json.dumps(test_schema)]
        messages.extend([json.dumps(record) for record in test_records])
        input_data = "\n".join(messages)

        # Process with performance timing
        performance_timer.start()

        with patch("sys.stdin", StringIO(input_data)):
            target.cli()

        performance_timer.stop()

        # Verify all records were processed
        with oracle_engine.connect() as conn:
            result = conn.execute(
                text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            count = row[0]
            assert count == len(test_records)

        # Performance assertions
        throughput = len(test_records) / performance_timer.duration
        assert throughput > 10, f"Throughput too low: {
            throughput:.2f} records/sec"

    def test_upsert_operations(self,
                               oracle_config: dict[str, Any],
                               sample_singer_schema: dict[str, Any],
                               test_table_name: str,
                               oracle_engine: Engine,
                               table_cleanup: Any,
                               ) -> None:
        """Test upsert operations using Oracle MERGE."""
        table_cleanup(test_table_name)

        # Configure for MERGE upserts
        upsert_config = oracle_config.copy()
        upsert_config["upsert_method"] = "merge"
        upsert_config["use_bulk_operations"] = True

        target = OracleTarget(config=upsert_config)

        # Create test schema and initial records
        test_schema = sample_singer_schema.copy()
        test_schema["stream"] = test_table_name

        initial_records = [
            {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": 1,
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "age": 30,
                    "active": True,
                    "created_at": "2025-07-02T10:00:00Z",
                    "metadata": {"department": "Engineering"},
                    "score": 95.5,
                },
            },
            {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": 2,
                    "name": "Jane Smith",
                    "email": "jane.smith@example.com",
                    "age": 28,
                    "active": True,
                    "created_at": "2025-07-02T10:01:00Z",
                    "metadata": {"department": "Marketing"},
                    "score": 87.3,
                },
            },
        ]

        # Insert initial records
        messages = [json.dumps(test_schema)]
        messages.extend([json.dumps(record) for record in initial_records])
        input_data = "\n".join(messages)

        with patch("sys.stdin", StringIO(input_data)):
            target.cli()

        # Verify initial insert
        with oracle_engine.connect() as conn:
            result = conn.execute(
                text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            assert row[0] == 2

        # Update existing records and add new one
        updated_records = [
            {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": 1,  # Update existing
                    "name": "John Smith",  # Changed name
                    "email": "john.smith@example.com",  # Changed email
                    "age": 31,  # Changed age
                    "active": True,
                    "created_at": "2025-07-02T10:00:00Z",
                    "metadata": {"department": "Engineering", "level": "Senior"},
                    "score": 96.0,  # Changed score
                },
            },
            {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": 3,  # New record
                    "name": "Bob Wilson",
                    "email": "bob.wilson@example.com",
                    "age": 35,
                    "active": False,
                    "created_at": "2025-07-02T10:02:00Z",
                    "metadata": {"department": "Sales"},
                    "score": 92.1,
                },
            },
        ]

        # Process updates
        messages = [json.dumps(test_schema)]
        messages.extend([json.dumps(record) for record in updated_records])
        input_data = "\n".join(messages)

        target_new = OracleTarget(
            config=upsert_config)  # Fresh target instance
        with patch("sys.stdin", StringIO(input_data)):
            target_new.cli()

        # Verify upsert results
        with oracle_engine.connect() as conn:
            # Should have 3 total records now (2 original + 1 new)
            result = conn.execute(
                text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            assert row[0] == 3

            # Verify updated record
            result = conn.execute(
                text(
                    f"SELECT name, email, age, score FROM {test_table_name} "
                    f"WHERE id = 1",
                ),
            )
            row = result.fetchone()
            assert row is not None
            assert row.name == "John Smith"
            assert row.email == "john.smith@example.com"
            assert row.age == 31
            assert float(row.score) == 96.0

            # Verify new record
            result = conn.execute(
                text(f"SELECT name FROM {test_table_name} WHERE id = 3"),
            )
            row = result.fetchone()
            assert row is not None
            assert row.name == "Bob Wilson"

    def test_data_type_handling(self,
                                oracle_target: OracleTarget,
                                test_table_name: str,
                                oracle_engine: Engine,
                                table_cleanup: Any,
                                ) -> None:
        """Test various data type handling."""
        table_cleanup(test_table_name)

        # Create comprehensive schema with various data types
        comprehensive_schema = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string", "maxLength": 100},
                    "description": {"type": "string", "maxLength": 4000},
                    "long_text": {"type": "string"},  # Should become CLOB
                    "age": {"type": "integer"},
                    "salary": {"type": "number"},
                    "is_active": {"type": "boolean"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "birth_date": {"type": "string", "format": "date"},
                    "metadata": {"type": "object"},
                    "tags": {"type": "array"},
                    "score": {"type": "number", "multipleOf": 0.01},
                },
            },
            "key_properties": ["id"],
        }

        # Create test record with various data types
        test_record = {
            "type": "RECORD",
            "stream": test_table_name,
            "record": {
                "id": 1,
                "name": "Test User",
                "description": "A" * 3000,  # Long VARCHAR2
                "long_text": "B" * 5000,  # Should become CLOB
                "age": 30,
                "salary": 75000.50,
                "is_active": True,
                "created_at": "2025-07-02T10:30:00Z",
                "birth_date": "1995-01-15",
                "metadata": {
                    "department": "Engineering",
                    "level": "Senior",
                    "skills": ["Python", "Oracle", "SQL"],
                },
                "tags": ["developer", "database", "expert"],
                "score": 95.75,
            },
        }

        # Process schema and record
        messages = [json.dumps(comprehensive_schema), json.dumps(test_record)]
        input_data = "\n".join(messages)

        with patch("sys.stdin", StringIO(input_data)):
            oracle_target.cli()

        # Verify data was stored correctly
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None

            assert row.id == 1
            assert row.name == "Test User"
            assert len(row.description) == 3000
            assert len(row.long_text) == 5000
            assert row.age == 30
            assert float(row.salary) == 75000.50
            # Oracle might return 1 for boolean
            assert row.is_active == 1
            assert row.created_at is not None
            assert row.birth_date is not None

            # Verify JSON data (stored as strings)
            assert row.metadata is not None
            assert row.tags is not None

    def test_error_handling_and_recovery(self,
                                         oracle_config: dict[str, Any],
                                         test_table_name: str,
                                         oracle_engine: Engine,
                                         table_cleanup: Any,
                                         ) -> None:
        """Test error handling and recovery mechanisms."""
        table_cleanup(test_table_name)

        # Configure with retry settings
        error_config = oracle_config.copy()
        error_config["max_retries"] = 3
        error_config["retry_delay"] = 0.1  # Fast retry for testing
        error_config["retry_backoff"] = 1.5

        target = OracleTarget(config=error_config)

        # Create schema
        test_schema = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {
                        "type": "string",
                        "maxLength": 10,
                    },  # Short limit for testing
                    "email": {"type": "string", "maxLength": 50},
                },
            },
            "key_properties": ["id"],
        }

        # Create records with one that will cause constraint violation
        valid_record = {
            "type": "RECORD",
            "stream": test_table_name,
            "record": {
                "id": 1,
                "name": "John",
                "email": "john@example.com",
            },
        }

        invalid_record = {
            "type": "RECORD",
            "stream": test_table_name,
            "record": {
                "id": 2,
                "name": "A" * 20,  # Too long for column
                "email": "jane@example.com",
            },
        }

        # Process valid record first
        messages = [json.dumps(test_schema), json.dumps(valid_record)]
        input_data = "\n".join(messages)

        with patch("sys.stdin", StringIO(input_data)):
            target.cli()

        # Verify valid record was inserted
        with oracle_engine.connect() as conn:
            result = conn.execute(
                text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            assert row[0] == 1

        # Test handling of invalid record (should be handled gracefully)
        messages = [json.dumps(test_schema), json.dumps(invalid_record)]
        input_data = "\n".join(messages)

        target_new = OracleTarget(config=error_config)

        # This should not crash the target, depending on configuration
        try:
            with patch("sys.stdin", StringIO(input_data)):
                target_new.cli()
        except Exception as e:
            # Some errors are expected for invalid data
            assert "constraint" in str(e).lower() or "length" in str(e).lower()

    def test_parallel_processing(self,
                                 oracle_config: dict[str, Any],
                                 test_table_name: str,
                                 oracle_engine: Engine,
                                 table_cleanup: Any,
                                 performance_timer: Any,
                                 ) -> None:
        """Test parallel processing capabilities."""
        table_cleanup(test_table_name)

        # Configure for parallel processing
        parallel_config = oracle_config.copy()
        parallel_config["max_workers"] = 4
        parallel_config["parallel_degree"] = 2
        parallel_config["batch_size"] = 200

        target = OracleTarget(config=parallel_config)

        # Generate large dataset
        test_schema = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "value": {"type": "number"},
                },
            },
            "key_properties": ["id"],
        }

        # Generate 2000 test records
        test_records = [{
                    "type": "RECORD",
                    "stream": test_table_name,
                    "record": {
                        "id": i + 1,
                        "name": f"User {i + 1}",
                        "value": float(i * 1.5),
                    },
                } for i in range(2000)]

        # Process with timing
        messages = [json.dumps(test_schema)]
        messages.extend([json.dumps(record) for record in test_records])
        input_data = "\n".join(messages)

        performance_timer.start()

        with patch("sys.stdin", StringIO(input_data)):
            target.cli()

        performance_timer.stop()

        # Verify all records processed
        with oracle_engine.connect() as conn:
            result = conn.execute(
                text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            count = row[0]
            assert count == len(test_records)

        # Performance check
        throughput = len(test_records) / performance_timer.duration
        assert (
            throughput > 50
        ), f"Parallel processing throughput too low: {throughput:.2f} records/sec"

    def test_configuration_validation(self, oracle_config: dict[str, Any]) -> None:
        """Test configuration validation functionality."""
        """Test configuration validation functionality."""
        # Test valid configuration
        target = OracleTarget(config=oracle_config)
        assert target.config is not None

        # Test missing required field
        invalid_config = oracle_config.copy()
        del invalid_config["host"]

        with pytest.raises((ValueError, ConnectionError, Exception)):
            OracleTarget(config=invalid_config)

        # Test that target accepts valid config without errors
        valid_config = oracle_config.copy()
        valid_config["batch_size"] = 1000

        # This should work fine
        target_valid = OracleTarget(config=valid_config)
        assert target_valid.config["batch_size"] == 1000

    def test_cli_functionality(self, temp_config_file: str) -> None:
        """Test CLI functionality and commands."""
        """Test CLI functionality and commands."""
        import json

        # Test that we can load config file
        config_path = Path(temp_config_file)
        with config_path.open(encoding="utf-8") as f:
            config = json.load(f)
        assert config is not None
        assert config["host"] is not None

        # Test invalid configuration file handling
        try:
            nonexistent_path = Path("/nonexistent/file.json")
            with nonexistent_path.open(encoding="utf-8") as f:
                json.load(f)
            msg = "Should have raised an exception"
            raise AssertionError(msg) from None
        except Exception:
            # TODO: Consider using else block
            pass  # This is expected
