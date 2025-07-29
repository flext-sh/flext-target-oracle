"""Pytest configuration for flext-target-oracle tests."""

from unittest.mock import AsyncMock

import pytest

from flext_target_oracle import FlextOracleTarget, FlextOracleTargetConfig, LoadMethod


@pytest.fixture
def sample_config() -> FlextOracleTargetConfig:
    """Sample configuration for testing."""
    return FlextOracleTargetConfig(
        host="localhost",
        port=1521,
        service_name="XE",
        username="test_user",
        password="test_pass",
        default_target_schema="TEST_SCHEMA",
        batch_size=1000,
        load_method=LoadMethod.APPEND_ONLY,
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
