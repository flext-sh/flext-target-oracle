# Copyright (c) 2025 FLEXT Team
# Licensed under the MIT License
# SPDX-License-Identifier: MIT

"""Test data type mapping and conversion."""

from __future__ import annotations

import json
from typing import Any

import pytest

from flext_target_oracle import OracleSink, OracleTarget
from tests.helpers import requires_oracle_connection


@requires_oracle_connection
class TestTypeMapping:
    """Test Singer to Oracle type mapping."""

    @staticmethod
    @pytest.fixture
    def target_config() -> Any:
        return {
            "host": "localhost",
            "username": "test",
            "password": "test",
            "service_name": "XE",
        }

    @staticmethod
    @pytest.fixture
    def oracle_target(target_config: dict[str, Any]) -> OracleTarget:
        return OracleTarget(config=target_config)

    @staticmethod
    def test_string_type_mapping(oracle_target: OracleTarget) -> None:
        schema = {
            "type": "object",
            "properties": {
                "short_string": {"type": "string", "maxLength": 100},
                "medium_string": {"type": "string", "maxLength": 2000},
                "long_string": {"type": "string", "maxLength": 5000},
                "unlimited_string": {"type": "string"},
            },
        }

        sink = OracleSink(
            target=oracle_target,
            stream_name="test_strings",
            schema=schema,
            key_properties=["short_string"],
        )

        # Test type mapping (this would normally check the actual SQL types)
        # For now, we verify the sink is created properly
        assert sink.stream_name == "test_strings"
        assert "short_string" in sink.schema["properties"]

    @staticmethod
    def test_numeric_type_mapping(oracle_target: OracleTarget) -> None:
        schema = {
            "type": "object",
            "properties": {
                "integer_field": {"type": "integer"},
                "number_field": {"type": "number"},
                "decimal_field": {"type": "number", "multipleOf": 0.01},
                "big_integer": {"type": "integer", "maximum": 999999999999},
            },
        }

        sink = OracleSink(
            target=oracle_target,
            stream_name="test_numbers",
            schema=schema,
        )

        assert "integer_field" in sink.schema["properties"]
        assert "number_field" in sink.schema["properties"]

    @staticmethod
    def test_boolean_type_mapping(oracle_target: OracleTarget) -> None:
        schema = {
            "type": "object",
            "properties": {
                "is_active": {"type": "boolean"},
                "is_verified": {"type": "boolean"},
            },
        }

        # Test with default boolean values
        sink = OracleSink(
            target=oracle_target,
            stream_name="test_booleans",
            schema=schema,
        )

        # Test boolean conversion
        record = {"is_active": True, "is_verified": False}
        conformed = sink._conform_record(record)  # type: ignore[attr-defined]

        # Should convert to configured values (default 1/0)
        assert conformed["is_active"] == 1
        assert conformed["is_verified"] == 0

    @staticmethod
    def test_datetime_type_mapping(oracle_target: OracleTarget) -> None:
        schema = {
            "type": "object",
            "properties": {
                "date_field": {"type": "string", "format": "date"},
                "datetime_field": {"type": "string", "format": "date-time"},
                "time_field": {"type": "string", "format": "time"},
            },
        }

        sink = OracleSink(target=oracle_target, stream_name="test_dates", schema=schema)

        assert "date_field" in sink.schema["properties"]
        assert "datetime_field" in sink.schema["properties"]

    @staticmethod
    def test_json_type_mapping(oracle_target: OracleTarget) -> None:
        schema = {
            "type": "object",
            "properties": {
                "metadata": {"type": "object"},
                "tags": {"type": "array"},
                "config": {
                    "type": "object",
                    "properties": {
                        "key": {"type": "string"},
                        "value": {"type": "number"},
                    },
                },
            },
        }

        sink = OracleSink(target=oracle_target, stream_name="test_json", schema=schema)

        # Test JSON serialization
        record = {
            "metadata": {"source": "api", "version": "1.0"},
            "tags": ["tag1", "tag2", "tag3"],
            "config": {"key": "test", "value": 123},
        }

        conformed = sink._conform_record(record)  # type: ignore[attr-defined]

        # JSON fields should be serialized
        assert isinstance(conformed["metadata"], str)
        assert isinstance(conformed["tags"], str)
        assert isinstance(conformed["config"], str)

        # Verify JSON is valid
        assert json.loads(conformed["metadata"]) == record["metadata"]
        assert json.loads(conformed["tags"]) == record["tags"]

    @staticmethod
    def test_nullable_types(oracle_target: OracleTarget) -> None:
        schema = {
            "type": "object",
            "properties": {
                "nullable_string": {"type": ["string", "null"]},
                "nullable_number": {"type": ["number", "null"]},
                "nullable_object": {"type": ["object", "null"]},
            },
        }

        sink = OracleSink(
            target=oracle_target,
            stream_name="test_nullable",
            schema=schema,
        )

        # Test with null values
        record = {
            "nullable_string": None,
            "nullable_number": None,
            "nullable_object": None,
        }

        conformed = sink._conform_record(record)  # type: ignore[attr-defined]

        assert conformed["nullable_string"] is None
        assert conformed["nullable_number"] is None
        assert conformed["nullable_object"] is None

    @staticmethod
    def test_custom_type_configuration() -> None:
        config = {
            "host": "localhost",
            "username": "test",
            "password": "test",
            "service_name": "XE",
            # Custom type settings
            "varchar_max_length": 2000,
            "use_nvarchar": True,
            "number_precision": 20,
            "number_scale": 5,
            "json_column_type": "JSON",
            "boolean_true_value": "Y",
            "boolean_false_value": "N",
        }

        target = OracleTarget(config=config)

        schema = {
            "type": "object",
            "properties": {"text": {"type": "string"}, "flag": {"type": "boolean"}},
        }

        sink = OracleSink(target=target, stream_name="test_custom", schema=schema)

        # Test custom boolean values
        record = {"text": "test", "flag": True}
        conformed = sink._conform_record(record)  # type: ignore[attr-defined]

        # Should use custom boolean values
        assert conformed["flag"] == "Y"

    @staticmethod
    def test_complex_nested_types(oracle_target: OracleTarget) -> None:
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "user": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "email": {"type": "string"},
                        "preferences": {
                            "type": "object",
                            "properties": {
                                "notifications": {"type": "boolean"},
                                "theme": {"type": "string"},
                            },
                        },
                    },
                },
                "history": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "action": {"type": "string"},
                            "timestamp": {"type": "string", "format": "date-time"},
                        },
                    },
                },
            },
        }

        sink = OracleSink(
            target=oracle_target,
            stream_name="test_nested",
            schema=schema,
            key_properties=["id"],
        )

        # Test complex record
        record = {
            "id": 1,
            "user": {
                "name": "John Doe",
                "email": "john@example.com",
                "preferences": {"notifications": True, "theme": "dark"},
            },
            "history": [
                {"action": "login", "timestamp": "2025-01-01T10:00:00Z"},
                {"action": "update", "timestamp": "2025-01-01T11:00:00Z"},
            ],
        }

        conformed = sink._conform_record(record)  # type: ignore[attr-defined]

        # Complex objects should be JSON serialized
        assert isinstance(conformed["user"], str)
        assert isinstance(conformed["history"], str)

        # Verify structure is preserved
        user_data = json.loads(conformed["user"])
        assert user_data["name"] == "John Doe"
        assert user_data["preferences"]["theme"] == "dark"
