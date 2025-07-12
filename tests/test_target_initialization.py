# Copyright (c) 2025 FLEXT Team
# Licensed under the MIT License
# SPDX-License-Identifier: MIT

"""Test target initialization and message processing."""

from unittest.mock import Mock, patch

import pytest

from flext_target_oracle.sink import OracleSink
from flext_target_oracle.target import OracleTarget


class TestTargetInitialization:
    """Test target initialization and message processing."""

    @staticmethod
    def test_target_init_no_network_calls() -> None:
        config = {
            "host": "localhost",
            "port": 1521,
            "database": "test",
            "username": "test",
            "password": "test",
        }

        # Mock database connection to ensure it's not made during init
        with patch(
            "sqlalchemy.create_engine",
        ) as mock_engine:  # Initialize target - should not trigger database connections
            target = OracleTarget(config=config)

            # Verify no database engine was created during init
            mock_engine.assert_not_called()

            # Verify target is properly initialized
            assert target.config["host"] == "localhost"
            assert target.config["database"] == "test"

    @staticmethod
    def test_schema_message_processing() -> None:
        config = {
            "host": "localhost",
            "port": 1521,
            "database": "test",
            "username": "test",
            "password": "test",
        }

        target = OracleTarget(config=config)

        # Valid schema message
        schema_message = {
            "type": "SCHEMA",
            "stream": "test_stream",
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

        # Mock sink creation - use correct method name
        with patch.object(target, "get_sink") as mock_get_sink:
            mock_sink = Mock()
            mock_get_sink.return_value = mock_sink

            # Process schema message
            target._process_schema_message(schema_message)

            # Verify sink was created
            mock_get_sink.assert_called_once()

    @staticmethod
    def test_schema_message_validation_errors() -> None:
        config = {
            "host": "localhost",
            "port": 1521,
            "database": "test",
            "username": "test",
            "password": "test",
        }

        target = OracleTarget(config=config)

        # Missing stream field
        invalid_message = {
            "type": "SCHEMA",
            "schema": {"type": "object"},
            "key_properties": [],
        }

        with pytest.raises(
            ValueError,
            match="Schema message must contain 'stream' field",
        ):
            target._process_schema_message(invalid_message)

        # Missing schema field
        invalid_message = {
            "type": "SCHEMA",
            "stream": "test_stream",
            "key_properties": [],
        }

        with pytest.raises(
            ValueError,
            match="Schema message must contain 'schema' field",
        ):
            target._process_schema_message(invalid_message)

    @staticmethod
    def test_empty_schema_handling() -> None:
        config = {
            "host": "localhost",
            "port": 1521,
            "database": "test",
            "username": "test",
            "password": "test",
        }

        target = OracleTarget(config=config)

        # Empty schema message
        schema_message = {
            "type": "SCHEMA",
            "stream": "empty_stream",
            "schema": {},
            "key_properties": [],
        }

        # Mock sink creation - use correct method name
        with patch.object(target, "get_sink") as mock_get_sink:
            mock_sink = Mock()
            mock_get_sink.return_value = mock_sink

            # Should handle empty schema gracefully
            target._process_schema_message(schema_message)

            # Verify sink was still created
            mock_get_sink.assert_called_once()


class TestOracleSinkTypeConversion:
    """Test Oracle sink type conversion functionality."""

    @staticmethod
    def test_type_conversion_string_to_number() -> None:
        # Mock sink with complete config
        mock_target = Mock()
        mock_target.config = {
            "host": "localhost",
            "port": 1521,
            "database": "test",
            "username": "test",
            "password": "test",
        }

        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "amount": {"type": "number"},
                "name": {"type": "string"},
            },
        }

        # Mock the connector to avoid database connection
        with patch("flext_target_oracle.sink.OracleConnector"):
            sink = OracleSink(
                target=mock_target,
                stream_name="test_stream",
                schema=schema,
                key_properties=["id"],
            )

            # Test record with string numbers
            record = {"id": "123", "amount": "540.50", "name": "Test Record"}

            # Convert record types
            converted = sink._convert_record_types(record)

            # Verify conversions
            assert isinstance(converted["id"], int)
            assert converted["id"] == 123
            assert isinstance(converted["amount"], float)
            assert converted["amount"] == 540.50
            assert isinstance(converted["name"], str)
            assert converted["name"] == "Test Record"

    @staticmethod
    def test_type_conversion_edge_cases() -> None:
        mock_target = Mock()
        mock_target.config = {
            "host": "localhost",
            "port": 1521,
            "database": "test",
            "username": "test",
            "password": "test",
        }

        schema = {
            "type": "object",
            "properties": {
                "nullable_number": {"type": "number"},
                "boolean_field": {"type": "boolean"},
                "invalid_number": {"type": "number"},
            },
        }

        # Mock the connector to avoid database connection
        with patch("flext_target_oracle.sink.OracleConnector"):
            sink = OracleSink(
                target=mock_target,
                stream_name="test_stream",
                schema=schema,
                key_properties=[],
            )

            # Test edge cases
            record = {
                "nullable_number": None,
                "boolean_field": "true",
                "invalid_number": "not_a_number",
            }

            converted = sink._convert_record_types(record)

            # Verify edge case handling
            assert converted["nullable_number"] is None
            assert converted["boolean_field"] is True
            assert (
                converted["invalid_number"] is None
            )  # Invalid conversion returns None

    @staticmethod
    def test_minimal_table_creation() -> None:
        mock_target = Mock()
        mock_target.config = {
            "host": "localhost",
            "port": 1521,
            "database": "test",
            "username": "test",
            "password": "test",
        }

        # Empty schema
        schema: dict[str, str] = {}

        # Mock the connector to avoid database connection
        with patch("flext_target_oracle.sink.OracleConnector"):
            sink = OracleSink(
                target=mock_target,
                stream_name="minimal_stream",
                schema=schema,
                key_properties=[],
            )

            # Mock database components
            with patch("sqlalchemy.Table") as mock_table:
                with patch("sqlalchemy.MetaData"):
                    # Should handle empty schema gracefully
                    sink._create_table()

                    # Verify table creation was attempted
                    mock_table.assert_called()

    @staticmethod
    def test_boolean_conversion_variants() -> None:
        mock_target = Mock()
        mock_target.config = {
            "host": "localhost",
            "port": 1521,
            "database": "test",
            "username": "test",
            "password": "test",
        }

        # Mock the connector to avoid database connection
        with patch("flext_target_oracle.sink.OracleConnector"):
            sink = OracleSink(
                target=mock_target,
                stream_name="test_stream",
                schema={},
                key_properties=[],
            )

            # Test various boolean representations
            test_cases = [
                ("true", True),
                ("false", False),
                ("1", True),
                ("0", False),
                ("yes", True),
                ("no", False),
                ("Y", True),
                ("N", False),
                (1, True),
                (0, False),
                (True, True),
                (False, False),
            ]

            for input_val, expected in test_cases:
                result = sink._convert_field_value(
                    "test_field",
                    input_val,
                    {"type": "boolean"},
                )
                assert result == expected, f"Failed for input: {input_val}"
