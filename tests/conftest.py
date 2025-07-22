# Copyright (c) 2025 FLEXT Team
# Licensed under the MIT License
# SPDX-License-Identifier: MIT

"""Modern test configuration using pytest patterns.

Clean, minimal test setup following enterprise standards.
ZERO TOLERANCE: NO SKIPS - All tests must run with real Oracle infrastructure.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flext_db_oracle import OracleConfig


@pytest.fixture(scope="session")
def oracle_e2e_environment() -> dict[str, str]:
    """Ensure Oracle E2E environment is available.

    ZERO TOLERANCE: This fixture MUST provide working Oracle configuration.
    NO SKIPS allowed - tests will use real Oracle infrastructure.
    """
    # Check if Oracle E2E is already running
    try:
        result = subprocess.run(
            [
                "docker",
                "ps",
                "--filter",
                "name=flext-oracle-db-e2e",
                "--format",
                "{{.Names}}",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        if "flext-oracle-db-e2e" in result.stdout:
            # Oracle already running - use it
            return {
                "ORACLE_HOST": "localhost",
                "ORACLE_PORT": "1521",
                "ORACLE_SERVICE_NAME": "FLEXT_PDB",
                "ORACLE_USERNAME": "FLEXT_USER",
                "ORACLE_PASSWORD": "FlextTest123!",
                "ORACLE_SCHEMA": "FLEXT_TEST",
            }
    except subprocess.CalledProcessError:
        pass

    # Start Oracle E2E infrastructure
    docker_dir = Path(__file__).parent.parent.parent / "docker"
    compose_file = docker_dir / "docker-compose.oracle-e2e.yml"

    if not compose_file.exists():
        pytest.fail(f"Oracle E2E infrastructure not found: {compose_file}")

    try:
        # Start Oracle database
        subprocess.run(
            [
                "docker",
                "compose",
                "-f",
                str(compose_file),
                "up",
                "-d",
                "oracle-db",
            ],
            check=True,
            cwd=docker_dir,
        )

        # Wait for Oracle to be healthy
        subprocess.run(
            [
                "docker",
                "compose",
                "-f",
                str(compose_file),
                "exec",
                "-T",
                "oracle-db",
                "bash",
                "-c",
                "until sqlplus -s sys/Oracle123!@localhost:1521/FLEXT_PDB as sysdba <<< 'SELECT 1 FROM DUAL;' | grep -q '1'; do sleep 5; done",
            ],
            check=True,
            cwd=docker_dir,
            timeout=300,
        )

        return {
            "ORACLE_HOST": "localhost",
            "ORACLE_PORT": "1521",
            "ORACLE_SERVICE_NAME": "FLEXT_PDB",
            "ORACLE_USERNAME": "FLEXT_USER",
            "ORACLE_PASSWORD": "FlextTest123!",
            "ORACLE_SCHEMA": "FLEXT_TEST",
        }

    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        pytest.fail(f"Failed to start Oracle E2E infrastructure: {e}")


@pytest.fixture
def oracle_env_vars(oracle_e2e_environment: dict[str, str]) -> None:
    """Configure Oracle environment variables for integration tests.

    Use this fixture explicitly for tests that need real Oracle connection.
    """
    for key, value in oracle_e2e_environment.items():
        os.environ[key] = value


@pytest.fixture
def mock_oracle_config() -> dict[str, Any]:
    """Provide mock Oracle configuration for unit tests that don't need real Oracle."""
    return {
        "connection": {
            "host": "mock-oracle",
            "port": 1521,
            "service_name": "MOCK_PDB",
            "username": "MOCK_USER",
            "password": "mock_password",
            "oracle_schema": "MOCK_SCHEMA",
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
def oracle_config() -> dict[str, Any]:
    """Provide REAL Oracle configuration for testing.

    ZERO TOLERANCE: Uses actual Oracle E2E environment, no mocks.
    """
    return {
        "connection": {
            "host": os.getenv("ORACLE_HOST", "localhost"),
            "port": int(os.getenv("ORACLE_PORT", "1521")),
            "service_name": os.getenv("ORACLE_SERVICE_NAME", "FLEXT_PDB"),
            "username": os.getenv("ORACLE_USERNAME", "FLEXT_USER"),
            "password": os.getenv("ORACLE_PASSWORD", "FlextTest123!"),
            "oracle_schema": os.getenv("ORACLE_SCHEMA", "FLEXT_TEST"),
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
def oracle_config_instance(oracle_config: dict[str, Any]) -> OracleConfig:
    """Create OracleConfig instance from REAL Oracle configuration."""
    # Extract flat configuration from nested structure
    connection = oracle_config["connection"]
    return OracleConfig(
        host=connection.get("host", "localhost"),
        port=connection.get("port", 1521),
        service_name=connection.get("service_name", "XEPDB1"),
        username=connection["username"],
        password=connection["password"],
    )


@pytest.fixture
def flat_oracle_config() -> dict[str, Any]:
    """Provide flat Oracle configuration for Singer SDK compatibility.

    ZERO TOLERANCE: Uses REAL Oracle environment variables.
    """
    return {
        # Singer SDK expects flat configuration
        "host": os.getenv("ORACLE_HOST", "localhost"),
        "port": int(os.getenv("ORACLE_PORT", "1521")),
        "service_name": os.getenv("ORACLE_SERVICE_NAME", "FLEXT_PDB"),
        "username": os.getenv("ORACLE_USERNAME", "FLEXT_USER"),
        "password": os.getenv("ORACLE_PASSWORD", "FlextTest123!"),
        "schema": os.getenv("ORACLE_SCHEMA", "FLEXT_TEST"),
        "batch_size": 1000,
        "pool_size": 5,
        "load_method": "append-only",
        "log_level": "DEBUG",
    }


@pytest.fixture
def sample_schema() -> dict[str, Any]:
    """Provide sample Singer schema for testing."""
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
    """Provide sample Singer records for testing."""
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
