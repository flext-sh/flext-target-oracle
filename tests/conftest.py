"""Pytest Configuration and Test Fixtures - FLEXT Target Oracle.

This module provides pytest configuration, fixtures, and test utilities for
the Oracle target test suite. Includes configuration fixtures, mock objects,
and test data generators for comprehensive testing.

Key Fixtures:
    - sample_config: Basic Oracle target configuration
    - mock_oracle_api: Mocked flext-db-oracle API
    - test_data_generators: Sample Singer messages and data

Configuration:
    - Test markers for different test categories
    - Environment variable handling for Oracle connections
    - Mock setup for external dependencies
"""

import os
from unittest.mock import AsyncMock

import pytest

from flext_target_oracle import FlextOracleTarget, FlextOracleTargetConfig, LoadMethod


@pytest.fixture(scope="session", autouse=True)
def oracle_test_environment() -> None:
    """Setup Oracle test environment variables for shared container."""
    # Set Oracle environment variables for shared container (pytest-oracle-xe on port 10521)
    os.environ.update(
        {
            "FLEXT_TARGET_ORACLE_HOST": "localhost",
            "FLEXT_TARGET_ORACLE_PORT": "10521",
            "FLEXT_TARGET_ORACLE_USERNAME": "system",
            "FLEXT_TARGET_ORACLE_PASSWORD": "oracle",
            "FLEXT_TARGET_ORACLE_SERVICE_NAME": "XE",
            "FLEXT_TARGET_ORACLE_DEFAULT_TARGET_SCHEMA": "FLEXT_TEST",
        },
    )
    # Cleanup is optional since these are test variables


@pytest.fixture
def sample_config() -> FlextOracleTargetConfig:
    """Sample configuration for testing."""
    return FlextOracleTargetConfig(
        oracle_host="localhost",
        oracle_port=1521,
        oracle_service="XE",
        oracle_user="test_user",
        oracle_password="test_pass",
        default_target_schema="TEST_SCHEMA",
        batch_size=1000,
        load_method=LoadMethod.INSERT,
    )


@pytest.fixture
def sample_target(sample_config: FlextOracleTargetConfig) -> FlextOracleTarget:
    """Sample target instance for testing."""
    return FlextOracleTarget(config=sample_config)


@pytest.fixture
def mock_loader() -> AsyncMock:
    """Mock loader for testing."""
    return AsyncMock()


@pytest.fixture
def schema() -> dict[str, object]:
    """Sample Singer schema message."""
    return {
        "type": "SCHEMA",
        "stream": "users",
        "schema": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string"},
            },
        },
        "key_properties": ["id"],
    }


@pytest.fixture
def record() -> dict[str, object]:
    """Sample Singer record message."""
    return {
        "type": "RECORD",
        "stream": "users",
        "record": {"id": 1, "name": "John Doe", "email": "john@example.com"},
    }


@pytest.fixture
def state() -> dict[str, object]:
    """Sample Singer state message."""
    return {
        "type": "STATE",
        "value": {"bookmarks": {"users": {"last_updated": "2025-01-01T00:00:00Z"}}},
    }


@pytest.fixture
def batch_records() -> list[dict[str, object]]:
    """Sample batch of records for testing."""
    return [
        {
            "stream": "users",
            "record": {"id": 1, "name": "John", "email": "john@example.com"},
        },
        {
            "stream": "users",
            "record": {"id": 2, "name": "Jane", "email": "jane@example.com"},
        },
        {
            "stream": "products",
            "record": {"id": 1, "name": "Product A", "price": 100.0},
        },
    ]
