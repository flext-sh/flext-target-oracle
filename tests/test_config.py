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

from flext_target_oracle.config import (
    ConnectionConfig,
    OracleConfig,
    PerformanceConfig,
)


class TestConnectionConfig:
    """Test Oracle connection configuration."""

    def test_valid_service_name_config(self) -> None:
        """Test valid configuration with service name."""
        config = ConnectionConfig(
            host="localhost",
            port=1521,
            service_name="XEPDB1",
            username="user",
            password="pass",
        )
        assert config.host == "localhost"
        assert config.service_name == "XEPDB1"

    def test_valid_database_config(self) -> None:
        """Test valid configuration with database SID."""
        config = ConnectionConfig(
            host="localhost",
            database="XE",
            username="user",
            password="pass",
        )
        assert config.database == "XE"
        assert config.service_name is None

    def test_missing_service_and_database(self) -> None:
        """Test validation error when both service_name and database are missing."""
        with pytest.raises(ValidationError, match="Either service_name or database"):
            ConnectionConfig(
                host="localhost",
                username="user",
                password="pass",
            )

    def test_invalid_port(self) -> None:
        """Test validation error for invalid port."""
        with pytest.raises(ValidationError):
            ConnectionConfig(
                host="localhost",
                port=70000,  # Invalid port
                service_name="test",
                username="user",
                password="pass",
            )


class TestPerformanceConfig:
    """Test performance configuration validation."""

    def test_default_values(self) -> None:
        """Test default performance configuration."""
        config = PerformanceConfig()
        assert config.batch_size == 10000
        assert config.pool_size == 10
        assert config.use_bulk_operations is True

    def test_batch_size_validation(self) -> None:
        """Test batch size validation."""
        with pytest.raises(ValidationError):
            PerformanceConfig(batch_size=50)  # Too small

        with pytest.raises(ValidationError):
            PerformanceConfig(batch_size=200000)  # Too large


class TestOracleConfig:
    """Test complete Oracle configuration."""

    def test_from_dict(self, mock_oracle_config: dict[str, Any]) -> None:
        """Test config creation from dictionary."""
        config = OracleConfig.from_dict(mock_oracle_config)
        assert config.connection.host == "localhost"
        assert config.performance.batch_size == 1000

    def test_sqlalchemy_url_generation(self, oracle_config: OracleConfig) -> None:
        """Test SQLAlchemy URL generation."""
        url = oracle_config.to_sqlalchemy_url()
        assert "oracle+oracledb://" in url
        assert "localhost:1521" in url
        assert "XEPDB1" in url

    def test_engine_options(self, oracle_config: OracleConfig) -> None:
        """Test SQLAlchemy engine options."""
        options = oracle_config.get_engine_options()
        assert "pool_size" in options
        assert "max_overflow" in options
        assert options["pool_pre_ping"] is True

