# Copyright (c) 2025 FLEXT Team
# Licensed under the MIT License
# SPDX-License-Identifier: MIT

"""Test basic functionality of the Oracle Target.

These tests validate the target's core functionality using the real architecture.
"""

from typing import Any

import pytest

from flext_target_oracle import OracleTarget
from flext_target_oracle.connectors import OracleConnector
from flext_target_oracle.domain.models import TargetConfig
from flext_target_oracle.sinks import OracleSink

# Test constants to avoid hardcoded password warnings
TEST_HOST = "test-host"
TEST_USER = "test-user"
TEST_PASSWORD = "test-pass"  # noqa: S105


class TestTargetConfig:
    """Test TargetConfig functionality."""

    @staticmethod
    def test_minimal_config() -> None:
        """Test minimal target configuration."""
        config = TargetConfig(
            host=TEST_HOST,
            username=TEST_USER,
            password=TEST_PASSWORD,
        )

        assert config.host == "test-host"
        assert config.username == "test-user"
        assert config.port == 1521  # default
        assert config.service_name == "XEPDB1"  # default from validator
        assert config.load_method == "append-only"  # default

    @staticmethod
    def test_full_config() -> None:
        """Test full configuration."""
        config = TargetConfig(
            host="oracle.example.com",
            port=1522,
            service_name="TESTDB",
            username="testuser",
            password=TEST_PASSWORD,
            protocol="tcps",
            batch_size=5000,
            max_parallelism=8,
            use_bulk_operations=False,
            compression=True,
            parallel_degree=4,
        )

        assert config.host == "oracle.example.com"
        assert config.port == 1522
        assert config.service_name == "TESTDB"
        assert config.protocol == "tcps"
        assert config.batch_size == 5000
        assert config.max_parallelism == 8
        assert config.use_bulk_operations is False
        assert config.compression is True
        assert config.parallel_degree == 4

    @staticmethod
    def test_oracle_config_generation() -> None:
        """Test Oracle config generation."""
        config = TargetConfig(
            host=TEST_HOST,
            username=TEST_USER,
            password=TEST_PASSWORD,
        )

        oracle_config = config.oracle_config
        assert oracle_config["host"] == TEST_HOST
        assert oracle_config["username"] == TEST_USER
        assert oracle_config["password"] == TEST_PASSWORD
        assert oracle_config["pool_min_size"] == 1
        assert oracle_config["pool_max_size"] == 4


class TestOracleTarget:
    """Test OracleTarget functionality."""

    @staticmethod
    def test_target_initialization() -> None:
        """Test target initialization."""
        config = {
            "host": TEST_HOST,
            "username": TEST_USER,
            "password": TEST_PASSWORD,
        }

        target = OracleTarget(config=config)

        assert isinstance(target.config, TargetConfig)
        assert target.config.host == "test-host"
        assert target.config.username == "test-user"
        assert hasattr(target, "target_service")

    @staticmethod
    def test_empty_config() -> None:
        """Test target with empty config."""
        with pytest.raises((ValueError, TypeError), match="required"):  # Should fail validation
            OracleTarget(config={})


class TestOracleConnector:
    """Test OracleConnector functionality."""

    @staticmethod
    def test_tcp_url_generation() -> None:
        """Test TCP URL generation."""
        config = {
            "host": "oracle.example.com",
            "port": 1521,
            "service_name": "TESTDB",
            "username": "testuser",
            "password": "testpass",
            "protocol": "tcp",
        }

        connector = OracleConnector(config=config)
        url = connector.get_sqlalchemy_url(config)

        assert "oracle+oracledb://" in url
        assert "oracle.example.com" in url
        assert "1521" in url
        assert "TESTDB" in url

    @staticmethod
    def test_tcps_url_generation() -> None:
        """Test TCPS URL generation."""
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

        assert "TCPS" in url or "tcps" in url
        assert "(PORT=2484)" in url
        assert "secure.oracle.com" in url

    @staticmethod
    def test_missing_credentials() -> None:
        """Test connector with missing credentials."""
        config = {
            "host": "test-host",
            "service_name": "TESTDB",
        }

        connector = OracleConnector(config=config)

        with pytest.raises(ValueError, match="username and password are required"):
            connector.get_sqlalchemy_url(config)


class TestOracleSink:
    """Test OracleSink functionality."""

    @staticmethod
    def test_sink_initialization() -> None:
        """Test sink initialization."""
        config = {
            "host": TEST_HOST,
            "username": TEST_USER,
            "password": TEST_PASSWORD,
        }

        schema = {
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
            },
            "key_properties": ["id"],
        }

        sink = OracleSink(
            stream_name="test_stream",
            schema=schema,
            config=config,
        )

        assert sink.stream_name == "test_stream"
        assert sink.schema == schema
        assert sink.key_properties == ["id"]
        assert hasattr(sink, "_connector")

    @staticmethod
    def test_schema_from_target() -> None:
        """Test sink initialization with target."""
        config = {
            "host": TEST_HOST,
            "username": TEST_USER,
            "password": TEST_PASSWORD,
        }

        target = OracleTarget(config=config)

        schema = {
            "properties": {"id": {"type": "integer"}},
            "key_properties": ["id"],
        }

        sink = OracleSink(
            target=target,
            stream_name="test_stream",
            schema=schema,
        )

        assert sink.stream_name == "test_stream"
        assert sink.key_properties == ["id"]
