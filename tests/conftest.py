"""Pytest Configuration and Test Fixtures - FLEXT Target Oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import asyncio
import json
import os
import time
from collections.abc import AsyncGenerator, Generator
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
import pytest_asyncio
from flext_core import FlextLogger, FlextResult, FlextTypes
from flext_db_oracle import FlextDbOracleApi, FlextDbOracleConfig
from pydantic import SecretStr
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.pool import NullPool

from flext_target_oracle import (
    FlextTargetOracle,
    FlextTargetOracleConfig,
    FlextTargetOracleLoader,
    LoadMethod,
)

# Constants
logger = FlextLogger(__name__)
ORACLE_CONTAINER_NAME = "flext-oracle-test"
ORACLE_IMAGE = "gvenzl/oracle-xe:21-slim"
ORACLE_HOST = "localhost"
ORACLE_PORT = 1521
ORACLE_USER = "system"
ORACLE_PASSWORD = "Oracle123"
ORACLE_SERVICE = "XE"
TEST_SCHEMA = "FLEXT_TEST"
DOCKER_COMPOSE_PATH = (
    Path(__file__).parent.parent.parent
    / "flext-db-oracle"
    / "docker-compose.oracle.yml"
)


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers."""
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "e2e: mark test as end-to-end test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "oracle: mark test as requiring Oracle database")


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop]:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def oracle_container() -> Generator[None]:
    """Manage Oracle Docker container lifecycle for tests."""
    # Check if container is already running
    check_cmd = [
        "docker",
        "ps",
        "-a",
        "--filter",
        f"name={ORACLE_CONTAINER_NAME}",
        "--format",
        "{{.Status}}",
    ]
    try:

        async def _run(cmd: FlextTypes.Core.StringList) -> tuple[int, str, str]:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()
            # process.returncode could be None if not terminated, use 0 as default
            return process.returncode or 0, stdout.decode(), stderr.decode()

        rc, out, _err = asyncio.run(_run(check_cmd))
        container_status = out.strip() if rc == 0 else ""

        if "Up" in container_status:
            yield
            return
    except Exception:
        pass

    # Start Oracle container using docker-compose
    try:
        # Stop any existing containers
        asyncio.run(
            _run(
                [
                    "/usr/bin/docker-compose",
                    "-f",
                    str(DOCKER_COMPOSE_PATH),
                    "down",
                    "-v",
                ],
            ),
        )

        # Start new container
        rc, _out, err = asyncio.run(
            _run(
                [
                    "/usr/bin/docker-compose",
                    "-f",
                    str(DOCKER_COMPOSE_PATH),
                    "up",
                    "-d",
                    "oracle-xe",
                ],
            ),
        )
        if rc != 0:
            msg = f"Failed to start docker-compose: {err}"
            raise RuntimeError(msg)

        # Wait for Oracle to be ready
        max_attempts = 60  # 5 minutes max
        for attempt in range(max_attempts):
            try:
                engine = create_engine(
                    f"oracle+oracledb://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}",
                    poolclass=NullPool,
                )
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1 FROM DUAL"))
                break
            except Exception as e:
                if attempt == max_attempts - 1:
                    msg = "Oracle container failed to start within timeout"
                    raise RuntimeError(msg) from e
                time.sleep(5)

        # Create test schema
        with engine.connect() as conn:
            try:
                conn.execute(
                    text(f"CREATE USER {TEST_SCHEMA} IDENTIFIED BY test_password"),
                )
                conn.execute(text(f"GRANT ALL PRIVILEGES TO {TEST_SCHEMA}"))
                conn.commit()
            except Exception:
                # Schema might already exist - expected behavior for test setup
                logger.debug("Schema might already exist - expected behavior")

        yield

    finally:
        # Cleanup: stop container
        if os.environ.get("KEEP_TEST_DB") != "true":
            asyncio.run(
                _run(
                    [
                        "/usr/bin/docker-compose",
                        "-f",
                        str(DOCKER_COMPOSE_PATH),
                        "down",
                        "-v",
                    ],
                ),
            )


@pytest.fixture(scope="session")
def oracle_engine() -> Engine:
    """Create SQLAlchemy engine for direct database access."""
    return create_engine(
        f"oracle+oracledb://{TEST_SCHEMA}:test_password@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}",
        poolclass=NullPool,
    )


@pytest.fixture
def clean_database(oracle_engine: Engine) -> None:
    """Clean database before each test."""
    with oracle_engine.connect() as conn:
        # Drop all tables in test schema
        result = conn.execute(
            text(
                """

              SELECT table_name
              FROM all_tables
              WHERE owner = :schema
              """,
            ),
            {"schema": TEST_SCHEMA},
        )
        tables = [row[0] for row in result]

        for table in tables:
            conn.execute(text(f"DROP TABLE {TEST_SCHEMA}.{table} CASCADE CONSTRAINTS"))
        conn.commit()

    # Cleanup after test (optional)


@pytest.fixture
def oracle_config() -> FlextTargetOracleConfig:
    """Create Oracle target configuration for tests."""
    return FlextTargetOracleConfig(
        oracle_host=ORACLE_HOST,
        oracle_port=ORACLE_PORT,
        oracle_service=ORACLE_SERVICE,
        oracle_user=TEST_SCHEMA,
        oracle_password="test_password",
        default_target_schema=TEST_SCHEMA,
        batch_size=1000,
        load_method=LoadMethod.INSERT,
        # Enable all features for testing
        sdc_mode="merge",
        storage_mode="flattened",
        column_ordering="alphabetical",
        allow_alter_table=True,
        maintain_indexes=True,
        create_foreign_key_indexes=True,
    )


@pytest.fixture
def oracle_api(oracle_config: FlextTargetOracleConfig) -> FlextDbOracleApi:
    """Create mocked FlextDbOracleApi instance."""
    # Create real config for reference
    db_config = FlextDbOracleConfig(
        host=oracle_config.oracle_host,
        port=oracle_config.oracle_port,
        service_name=oracle_config.oracle_service,
        username=oracle_config.oracle_user,
        password=SecretStr(oracle_config.oracle_password),
        oracle_schema=oracle_config.default_target_schema,
    )

    # Create mock API with common method responses
    mock_api = MagicMock()
    mock_api.config = db_config
    mock_api.connect.return_value = FlextResult.ok("Connected successfully")
    mock_api.disconnect.return_value = FlextResult.ok("Disconnected successfully")
    mock_api.test_connection.return_value = FlextResult.ok(data=True)
    mock_api.is_connected = True

    return mock_api


@pytest_asyncio.fixture
async def oracle_loader(
    oracle_config: FlextTargetOracleConfig,
) -> AsyncGenerator[FlextTargetOracleLoader]:
    """Create FlextTargetOracleLoader instance with mocked connection."""
    with patch("flext_target_oracle.target_client.FlextDbOracleApi") as mock_api_class:
        # Mock the API instance
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api

        # Mock successful connection
        mock_api.connect.return_value = FlextResult.ok("Connected successfully")
        mock_api.disconnect.return_value = FlextResult.ok("Disconnected successfully")
        mock_api.is_connected = True

        # Create loader with mocked API
        loader = FlextTargetOracleLoader(oracle_config)

        # Mock the connect result to avoid real database connection
        FlextResult.ok("Mocked connection successful")

        yield loader


@pytest.fixture
def oracle_target(oracle_config: FlextTargetOracleConfig) -> FlextTargetOracle:
    """Create FlextTargetOracle instance."""
    return FlextTargetOracle(config=oracle_config)


@pytest.fixture
def sample_config() -> FlextTargetOracleConfig:
    """Sample configuration for unit testing (no Oracle connection required)."""
    return FlextTargetOracleConfig(
        oracle_host="localhost",
        oracle_port=1521,
        oracle_service="XE",
        oracle_user="test_user",
        oracle_password="test_password",
        default_target_schema="TEST_SCHEMA",
        batch_size=1000,
        load_method=LoadMethod.INSERT,
        use_bulk_operations=True,
    )


@pytest.fixture
def sample_target(sample_config: FlextTargetOracleConfig) -> FlextTargetOracle:
    """Create FlextTargetOracle instance for unit testing."""
    return FlextTargetOracle(config=sample_config)


@pytest.fixture
def mock_oracle_api() -> Mock:
    """Create mocked FlextDbOracleApi for unit tests."""
    mock_api = Mock(spec=FlextDbOracleApi)
    mock_api.__enter__ = Mock(return_value=mock_api)
    mock_api.__exit__ = Mock(return_value=None)

    # Setup common return values
    mock_api.connect.return_value = MagicMock(
        is_success=True,
        is_failure=False,
        value=None,
    )
    mock_api.disconnect.return_value = MagicMock(
        is_success=True,
        is_failure=False,
        value=None,
    )
    mock_api.get_tables.return_value = MagicMock(
        is_success=True,
        is_failure=False,
        value=[],
    )
    mock_api.create_table_ddl.return_value = MagicMock(
        is_success=True,
        is_failure=False,
        value="CREATE TABLE...",
    )
    mock_api.execute_ddl.return_value = MagicMock(
        is_success=True,
        is_failure=False,
        value=None,
    )
    mock_api.build_insert_statement.return_value = MagicMock(
        is_success=True,
        is_failure=False,
        value="INSERT INTO...",
    )
    mock_api.build_merge_statement.return_value = MagicMock(
        is_success=True,
        is_failure=False,
        value="MERGE INTO...",
    )
    mock_api.query.return_value = MagicMock(
        is_success=True,
        is_failure=False,
        value=None,
    )
    mock_api.execute_batch.return_value = MagicMock(
        is_success=True,
        is_failure=False,
        value=None,
    )
    mock_api.get_columns.return_value = MagicMock(
        is_success=True,
        is_failure=False,
        value=[],
    )

    # Mock connection property
    mock_api.connection = MagicMock()

    return mock_api


@pytest.fixture
def mock_loader() -> AsyncMock:
    """Create mocked FlextTargetOracleLoader for unit tests."""
    mock = AsyncMock(spec=FlextTargetOracleLoader)
    mock.connect.return_value = MagicMock(is_success=True, value=None)
    mock.disconnect.return_value = MagicMock(is_success=True, value=None)
    mock.ensure_table_exists.return_value = MagicMock(is_success=True, value=None)
    mock.insert_records.return_value = MagicMock(is_success=True, value=None)
    return mock


# Test Data Fixtures
@pytest.fixture
def schema() -> FlextTypes.Core.Dict:
    """Simple Singer schema message for unit testing."""
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
def record() -> FlextTypes.Core.Dict:
    """Simple Singer record message for unit testing."""
    return {
        "type": "RECORD",
        "stream": "users",
        "record": {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
        },
    }


@pytest.fixture
def state() -> FlextTypes.Core.Dict:
    """Simple Singer state message for unit testing."""
    return {
        "type": "STATE",
        "value": {"bookmarks": {"users": {"last_updated": "2025-01-01T00:00:00Z"}}},
    }


@pytest.fixture
def simple_schema() -> FlextTypes.Core.Dict:
    """Simple Singer schema for testing."""
    return {
        "type": "SCHEMA",
        "stream": "users",
        "schema": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string"},
                "created_at": {"type": "string", "format": "date-time"},
            },
        },
        "key_properties": ["id"],
    }


@pytest.fixture
def nested_schema() -> FlextTypes.Core.Dict:
    """Nested Singer schema for testing flattening."""
    return {
        "type": "SCHEMA",
        "stream": "orders",
        "schema": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "customer": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "address": {
                            "type": "object",
                            "properties": {
                                "street": {"type": "string"},
                                "city": {"type": "string"},
                                "zip": {"type": "string"},
                            },
                        },
                    },
                },
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "product_id": {"type": "integer"},
                            "quantity": {"type": "integer"},
                            "price": {"type": "number"},
                        },
                    },
                },
                "total": {"type": "number"},
                "created_at": {"type": "string", "format": "date-time"},
            },
        },
        "key_properties": ["id"],
    }


@pytest.fixture
def sample_record() -> FlextTypes.Core.Dict:
    """Sample Singer record message."""
    return {
        "type": "RECORD",
        "stream": "users",
        "record": {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "created_at": "2025-01-20T12:00:00Z",
        },
        "time_extracted": "2025-01-20T12:00:00Z",
        "version": 1,
    }


@pytest.fixture
def batch_records() -> list[FlextTypes.Core.Dict]:
    """Batch of records for testing bulk operations."""
    return [
        {
            "type": "RECORD",
            "stream": "users",
            "record": {
                "id": i,
                "name": f"User {i}",
                "email": f"user{i}@example.com",
                "created_at": f"2025-01-20T12:00:{i:02d}Z",
            },
            "time_extracted": "2025-01-20T12:00:00Z",
        }
        for i in range(1, 101)  # 100 records
    ]


@pytest.fixture
def state_message() -> FlextTypes.Core.Dict:
    """Sample Singer state message."""
    return {
        "type": "STATE",
        "value": {
            "bookmarks": {
                "users": {
                    "replication_key": "created_at",
                    "replication_key_value": "2025-01-20T12:00:00Z",
                    "version": 1,
                },
            },
        },
    }


@pytest.fixture
def singer_messages(
    simple_schema: FlextTypes.Core.Dict,
    sample_record: FlextTypes.Core.Dict,
    state_message: FlextTypes.Core.Dict,
) -> list[FlextTypes.Core.Dict]:
    """Complete Singer message stream for testing."""
    return [
        simple_schema,
        sample_record,
        sample_record,  # Duplicate for testing updates
        state_message,
    ]


# Utility Functions
@contextmanager
def temporary_env_vars(**kwargs: str | None) -> Generator[None]:
    """Temporarily set environment variables."""
    old_values = {}
    for key, value in kwargs.items():
        old_values[key] = os.environ.get(key)
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = str(value)

    try:
        yield
    finally:
        for key, value in old_values.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


@pytest.fixture
def temp_config_file(tmp_path: Path) -> Path:
    """Create temporary configuration file."""
    config_data = {
        "oracle_host": ORACLE_HOST,
        "oracle_port": ORACLE_PORT,
        "oracle_service": ORACLE_SERVICE,
        "oracle_user": TEST_SCHEMA,
        "oracle_password": "test_password",
        "default_target_schema": TEST_SCHEMA,
        "batch_size": 1000,
        "load_method": "insert",
    }

    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config_data))
    return config_file


# Async Fixtures
@pytest_asyncio.fixture
async def connected_loader(
    oracle_loader: FlextTargetOracleLoader,
) -> AsyncGenerator[FlextTargetOracleLoader]:
    """Provide a connected FlextTargetOracleLoader instance."""
    yield oracle_loader


# Performance Testing Fixtures
@pytest.fixture
def large_dataset() -> list[FlextTypes.Core.Dict]:
    """Generate large dataset for performance testing."""
    schema = {
        "type": "SCHEMA",
        "stream": "performance_test",
        "schema": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "data": {"type": "string"},
                "value": {"type": "number"},
                "timestamp": {"type": "string", "format": "date-time"},
            },
        },
        "key_properties": ["id"],
    }

    records = [
        {
            "type": "RECORD",
            "stream": "performance_test",
            "record": {
                "id": i,
                "data": f"Performance test data {i}" * 10,  # Make it larger
                "value": i * 1.5,
                "timestamp": f"2025-01-20T12:{i % 60:02d}:00Z",
            },
        }
        for i in range(10000)  # 10k records
    ]

    result: list[FlextTypes.Core.Dict] = [schema]
    result.extend(records)
    return result


# Markers for different test categories
def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Add markers to test items based on their location."""
    for item in items:
        # Add markers based on test file location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
            item.add_marker(pytest.mark.oracle)
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
            item.add_marker(pytest.mark.oracle)
            item.add_marker(pytest.mark.slow)
        elif "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)
            item.add_marker(pytest.mark.oracle)
            item.add_marker(pytest.mark.slow)
