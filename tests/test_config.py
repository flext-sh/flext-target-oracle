# Copyright (c) 2025 FLEXT Team
# Licensed under the MIT License
# SPDX-License-Identifier: MIT

"""Test modern configuration system.

Unit tests for Pydantic configuration validation.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flext_target_oracle.config import ConnectionConfig, OracleConfig, PerformanceConfig


class TestConnectionConfig:  """Test Oracle connection configuration."""

    @staticmethod
    def test_valid_service_name_config() -> None: config = ConnectionConfig(
            host="localhost",
            port=1521,
            service_name="XEPDB1",
            username="user",
            password="pass",
        )
        assert config.host == "localhost"
        assert config.service_name == "XEPDB1"

    @staticmethod
    def test_valid_database_config() -> None: config = ConnectionConfig(
            host="localhost",
            database="XE",
            username="user",
            password="pass",
        )
        assert config.database == "XE"
        assert config.service_name is None

    @staticmethod
    def test_missing_service_and_database() -> None: with pytest.raises(ValidationError, match="Either service_name or database"): ConnectionConfig(
                host="localhost",
                username="user",
                password="pass",
            )

    @staticmethod
    def test_invalid_port() -> None: with pytest.raises(ValidationError):
    ConnectionConfig(
                host="localhost",
                port=70000,  # Invalid port
                service_name="test",
                username="user",
                password="pass",
            )


class TestPerformanceConfig:  """Test performance configuration validation.

    @staticmethod
    def test_default_values() -> None: config = PerformanceConfig()
        assert config.batch_size == 10000
        assert config.pool_size == 10
        assert config.use_bulk_operations is True

    @staticmethod
    def test_batch_size_validation() -> None:
        with pytest.raises(ValidationError):
    PerformanceConfig(batch_size=50)  # Too small

        with pytest.raises(ValidationError):


            PerformanceConfig(batch_size=200000)  # Too large


class TestOracleConfig:
    """Test complete Oracle configuration."""

    @staticmethod
    def test_from_dict(mock_oracle_config: dict[str, Any]) -> None: config = OracleConfig.from_dict(mock_oracle_config)
        assert config.connection.host == "localhost"
        assert config.performance.batch_size == 1000

    @staticmethod
    def test_sqlalchemy_url_generation(oracle_config: OracleConfig) -> None:
            url = oracle_config.to_sqlalchemy_url()
        assert "oracle+oracledb://" in url
        assert "localhost:1521" in url
        assert "XEPDB1" in url

    @staticmethod
    def test_engine_options(oracle_config: OracleConfig) -> None:
            options = oracle_config.get_engine_options()
        assert "pool_size" in options
        assert "max_overflow" in options
        assert options["pool_pre_ping"] is True
