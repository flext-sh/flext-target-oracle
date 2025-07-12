# Copyright (c) 2025 FLEXT Team
# Licensed under the MIT License
# SPDX-License-Identifier: MIT

"""Modern test configuration using pytest patterns.

Clean, minimal test setup following enterprise standards.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pytest

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flext_db_oracle import OracleConfig


@pytest.fixture
def mock_oracle_config() -> dict[str, Any]:
    return {
        "connection": {
            "host": "localhost",
            "port": 1521,
            "service_name": "XEPDB1",
            "username": "test_user",
            "password": "test_password",
            "oracle_schema": "TEST_SCHEMA",
        },
        "performance": {
            "batch_size": 1000,
            "pool_size": 5,
        },
        "table": {
            "load_method": "append-only",
            "create_indexes": True,
        },
        "log_level": "DEBUG",
    }


@pytest.fixture
def oracle_config(mock_oracle_config: dict[str, Any]) -> OracleConfig:
    return OracleConfig(**mock_oracle_config)


@pytest.fixture
def flat_oracle_config() -> dict[str, Any]:
    return {
        # Singer SDK expects flat configuration
        "host": "localhost",
        "port": 1521,
        "service_name": "XEPDB1",
        "username": "test_user",
        "password": "test_password",
        "schema": "TEST_SCHEMA",
        "batch_size": 1000,
        "pool_size": 5,
        "load_method": "append-only",
        "log_level": "DEBUG",
    }


@pytest.fixture
def sample_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string", "maxLength": 100},
            "email": {"type": "string", "maxLength": 255},
            "created_at": {"type": "string", "format": "date-time"},
            "active": {"type": "boolean"},
        },
        "required": ["id", "name"],
    }


@pytest.fixture
def sample_records() -> list[dict[str, Any]]:
    return [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "created_at": "2024-01-01T00:00:00Z",
            "active": True,
        },
        {
            "id": 2,
            "name": "Jane Smith",
            "email": "jane@example.com",
            "created_at": "2024-01-02T00:00:00Z",
            "active": False,
        },
    ]
