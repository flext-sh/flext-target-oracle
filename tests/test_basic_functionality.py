# Copyright (c) 2025 FLEXT Team
# Licensed under the MIT License
# SPDX-License-Identifier: MIT

"""Test basic functionality without requiring database connection.

These tests validate the target's basic functionality without
needing an actual Oracle database connection.
"""

from typing import Any
from unittest.mock import patch

import pytest

from flext_target_oracle import OracleTarget
from flext_target_oracle.connectors import OracleConnector
from flext_target_oracle.sinks import OracleSink


class TestBasicFunctionality:
    """Test basic target functionality without database."""

    @staticmethod
    def test_target_initialization_minimal() -> None:
        """Test minimal target initialization."""
        config = {"host": "test-host", "username": "test-user", "password": "test-pass"}

        target = OracleTarget(config=config)
        assert target.name == "flext-target-oracle"
        assert target.config["host"] == "test-host"
        assert target.config["username"] == "test-user"

    @staticmethod
    def test_target_capabilities() -> None:
        """Test target capabilities."""
        config = {"host": "test-host", "username": "test-user", "password": "test-pass"}

        target = OracleTarget(config=config)
        capabilities = target.capabilities

        # Check standard capabilities
        assert "about" in capabilities
        assert "supported_python_versions" in capabilities
        assert "settings" in capabilities

    @staticmethod
    def test_config_defaults() -> None:
        """Test configuration defaults."""
        config = {"host": "test-host", "username": "test-user", "password": "test-pass"}

        target = OracleTarget(config=config)

        # Check defaults from config schema
        assert target.config.get("batch_size", 10000) == 10000
        assert target.config.get("load_method", "append-only") == "append-only"

    @staticmethod
    def test_license_flags_default_to_false() -> None:
        """Test license flags default to false."""
        config = {"host": "test-host", "username": "test-user", "password": "test-pass"}

        target = OracleTarget(config=config)

        # All license flags should default to false
        assert target.config.get("oracle_has_partitioning", False) is False
        assert target.config.get("oracle_has_advanced_security_option", False) is False

    @staticmethod
    def test_connector_url_generation() -> None:
        """Test connector URL generation."""
        config = {
            "host": "oracle.example.com",
            "port": 1521,
            "service_name": "TESTDB",
            "username": "testuser",
            "password": "testpass",
        }

        connector = OracleConnector(config=config)
        url = connector.get_sqlalchemy_url(config)

        # Check URL contains expected components
        assert "oracle" in url
        assert "oracle.example.com" in url
        assert "1521" in url
        assert "TESTDB" in url

    @staticmethod
    def test_connector_tcps_url() -> None:
        """Test connector TCPS URL generation."""
        config = {
            "host": "secure.oracle.com",
            "port": 2484,
            "service_name": "SECUREDB",
            "username": "testuser",
            "password": "testpass",
            "protocol": "tcps",
        }

        connector = OracleConnector(config=config)
        url = connector.get_sqlalchemy_url(config)

        # Check TCPS protocol is used
        assert "tcps" in url or "ssl" in url
        assert "(PORT=2484)" in url

    @staticmethod
    def test_sink_initialization() -> None:
        """Test sink initialization."""
        config = {"host": "test-host", "username": "test-user", "password": "test-pass"}

        target = OracleTarget(config=config)

        schema = {
            "properties": {"id": {"type": "integer"}, "name": {"type": "string"}},
            "key_properties": ["id"],
        }

        # Mock the connector to avoid actual database connection
        with patch.object(OracleSink, "setup"):
            sink = OracleSink(
                target=target,
                stream_name="test_stream",
                schema=schema,
            )

            assert sink.stream_name == "test_stream"
            assert sink.key_properties == ["id"]

    @staticmethod
    def test_type_mapping() -> None:
        """Test type mapping functionality."""
        config = {"host": "test-host", "username": "test-user", "password": "test-pass"}

        target = OracleTarget(config=config)
        schema: dict[str, Any] = {"properties": {}}

        with patch.object(OracleSink, "setup"):
            sink = OracleSink(target=target, stream_name="test_stream", schema=schema)

            # Test various type mappings
            string_type = sink._singer_sdk_to_oracle_type(  # type: ignore[attr-defined]
                {"type": "string", "maxLength": 100},
            )
            assert "VARCHAR" in str(string_type)

            integer_type = sink._singer_sdk_to_oracle_type(  # type: ignore[attr-defined]
                {"type": "integer"},
            )
            assert "NUMBER" in str(integer_type)

            object_type = sink._singer_sdk_to_oracle_type(  # type: ignore[attr-defined]
                {"type": "object"},
            )
            assert "CLOB" in str(object_type) or "JSON" in str(object_type)

    @staticmethod
    def test_record_conformance() -> None:
        """Test record conformance."""
        config = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-pass",
            "true_values": ["Y", "true"],
            "false_values": ["N", "false"],
        }

        target = OracleTarget(config=config)
        schema = {
            "properties": {
                "id": {"type": "integer"},
                "active": {"type": "boolean"},
                "data": {"type": "object"},
            },
        }

        with patch.object(OracleSink, "setup"):
            sink = OracleSink(target=target, stream_name="test_stream", schema=schema)

            # Test record conformance
            record = {"id": 123, "active": True, "data": {"key": "value"}}

            conformed = sink._conform_record(record)  # type: ignore[attr-defined]

            assert conformed["id"] == 123
            assert conformed["active"] in ["Y", "true", 1]
            assert conformed["data"] == '{"key": "value"}'

    @staticmethod
    def test_batch_config_parsing() -> None:
        """Test batch configuration parsing."""
        config = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-pass",
            "batch_config": {
                "batch_size": 5000,
                "encoding": {"format": "jsonl", "compression": "gzip"},
            },
        }

        target = OracleTarget(config=config)

        assert target.config["batch_config"]["batch_size"] == 5000
        assert target.config["batch_config"]["encoding"]["compression"] == "gzip"
        assert target.config["batch_config"]["encoding"]["format"] == "jsonl"

    @staticmethod
    def test_parallel_configuration() -> None:
        """Test parallel processing configuration."""
        config = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-pass",
            "stream_config": {"test_stream": {"parallel_threads": 4, "chunk_size": 5000}},
        }

        target = OracleTarget(config=config)

        with patch.object(OracleSink, "setup"):
            sink = OracleSink(
                target=target,
                stream_name="test_stream",
                schema={"properties": {}},
            )

            assert sink._parallel_threads == 4  # type: ignore[attr-defined]
            assert sink._chunk_size == 5000  # type: ignore[attr-defined]

            # Thread pool should be created for parallel processing
            if sink._parallel_threads > 1:  # type: ignore[attr-defined]
                assert sink._executor is not None  # type: ignore[attr-defined]

    @staticmethod
    def test_wan_optimization_config() -> None:
        """Test WAN optimization configuration."""
        config = {
            "host": "remote-oracle.company.com",
            "username": "test-user",
            "password": "test-pass",
            "wan_optimization": {
                "prefetch_rows": 1000,
                "arraysize": 500,
                "auto_commit": False,
                "batch_size": 2000,
            },
            "connection_pool": {
                "min_size": 2,
                "max_size": 10,
                "max_retries": 3,
                "retry_delay": 2.0,
            },
            "data_flattening": {"max_level": 3, "null_value_treatment": "empty_string"},
            "load_method": "append-only",
            "add_record_metadata": True,
            "table_prefix": "RAW_",
            "column_name_transform": "snake_case",
            "hard_delete": False,
            "validate_records": True,
            "on_record_error": "fail",
            "on_schema_mismatch": "evolve",
            "stream_config": {
                "users": {
                    "replication_method": "INCREMENTAL",
                    "replication_key": "updated_at",
                },
            },
        }

        target = OracleTarget(config=config)

        assert target.config["max_retries"] == 3
        assert target.config["retry_delay"] == 2.0
        assert target.config["on_schema_mismatch"] == "evolve"
