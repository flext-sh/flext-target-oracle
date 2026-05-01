"""Pytest Configuration and Test Fixtures - FLEXT Target Oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import os
from asyncio import AbstractEventLoop, get_event_loop_policy
from collections.abc import (
    Generator,
)
from contextlib import contextmanager
from pathlib import Path
from time import monotonic, sleep
from unittest.mock import MagicMock, Mock

import pytest
from flext_tests import tk

from flext_core import FlextSettings
from flext_db_oracle import (
    FlextDbOracleApi,
    FlextDbOracleSettings,
)
from flext_target_oracle import (
    FlextTargetOracle,
    FlextTargetOracleLoader,
    FlextTargetOracleSettings,
)
from tests import c, m, t, u

logger = u.fetch_logger(__name__)


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers."""
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "e2e: mark test as end-to-end test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "oracle: mark test as requiring Oracle database")


@pytest.fixture(autouse=True)
def isolate_target_oracle_env(
    monkeypatch: pytest.MonkeyPatch,
    request: pytest.FixtureRequest,
) -> None:
    """Keep unit tests deterministic regardless of host FLEXT_TARGET_ORACLE_* env."""
    _ = request
    for key in [key for key in os.environ if key.startswith("FLEXT_TARGET_ORACLE_")]:
        monkeypatch.delenv(key, raising=False)
    FlextSettings.reset_for_testing()


@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop]:
    """Create event loop for tests."""
    loop = get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def docker_control() -> tk:
    """Provide Docker control instance for tests."""
    return tk.shared(
        "flext-oracle-db-test",
        workspace_root=Path(__file__).resolve().parents[2],
    )


@pytest.fixture(scope="session")
def shared_oracle_container(docker_control: tk) -> str:
    """Managed Oracle container using tk with auto-start."""
    container_name = "flext-oracle-db-test"
    ensure_result = docker_control.execute()
    if ensure_result.failure:
        pytest.skip(
            ensure_result.error or f"Oracle container {container_name} is unavailable",
        )
    resolved_port = next(
        (
            int(host_port)
            for container_port, host_port in ensure_result.value.ports.items()
            if container_port.startswith("1521") and host_port.isdigit()
        ),
        1522,
    )
    os.environ["TEST_ORACLE_HOST"] = "localhost"
    os.environ["TEST_ORACLE_PORT"] = str(resolved_port)
    os.environ["TEST_ORACLE_SERVICE"] = "FLEXTDB"
    os.environ["TEST_ORACLE_USER"] = "flext_test"
    os.environ["TEST_ORACLE_PASSWORD"] = "flext_test_password"
    admin_settings = FlextDbOracleSettings.model_validate({
        "host": os.environ["TEST_ORACLE_HOST"],
        "port": int(os.environ["TEST_ORACLE_PORT"]),
        "service_name": os.environ["TEST_ORACLE_SERVICE"],
        "username": "system",
        "password": "flext_oracle_test",
    })
    oracle_settings = FlextDbOracleSettings.model_validate({
        "host": os.environ["TEST_ORACLE_HOST"],
        "port": int(os.environ["TEST_ORACLE_PORT"]),
        "service_name": os.environ["TEST_ORACLE_SERVICE"],
        "username": os.environ["TEST_ORACLE_USER"],
        "password": os.environ["TEST_ORACLE_PASSWORD"],
    })
    deadline = monotonic() + 180
    last_error = "Oracle application user is not ready yet"
    while monotonic() < deadline:
        admin_api = FlextDbOracleApi(admin_settings)
        admin_connect_result = admin_api.connect()
        if admin_connect_result.success:
            user_query_result = admin_api.oracle_services.execute_query(
                'SELECT COUNT(*) AS "count" FROM all_users WHERE username = :username',
                m.ConfigMap(root={"username": "FLEXT_TEST"}),
            )
            if user_query_result.success:
                raw_user_count = user_query_result.value[0].root["count"]
                user_count = (
                    raw_user_count
                    if isinstance(raw_user_count, int)
                    else int(str(raw_user_count))
                )
                user_exists = user_count > 0
                if not user_exists:
                    create_user_result = admin_api.execute_sql(
                        "CREATE USER flext_test IDENTIFIED BY flext_test_password"
                    )
                    if create_user_result.failure:
                        last_error = create_user_result.error or last_error
                alter_user_result = admin_api.execute_sql(
                    "ALTER USER flext_test IDENTIFIED BY flext_test_password ACCOUNT UNLOCK"
                )
                if alter_user_result.failure:
                    last_error = alter_user_result.error or last_error
                grant_result = admin_api.execute_sql(
                    "GRANT CONNECT, RESOURCE, CREATE VIEW, CREATE SEQUENCE, CREATE TABLE, CREATE PROCEDURE, CREATE TRIGGER, UNLIMITED TABLESPACE TO flext_test"
                )
                if grant_result.failure:
                    last_error = grant_result.error or last_error
            else:
                last_error = user_query_result.error or last_error
            admin_disconnect_result = admin_api.disconnect()
            _ = admin_disconnect_result
            api = FlextDbOracleApi(oracle_settings)
            connect_result = api.connect()
            if connect_result.success:
                health_result = api.oracle_services.execute_query(
                    'SELECT 1 AS "health" FROM DUAL'
                )
                disconnect_result = api.disconnect()
                _ = disconnect_result
                if health_result.success:
                    return container_name
                last_error = health_result.error or last_error
            else:
                last_error = connect_result.error or last_error
        else:
            last_error = admin_connect_result.error or last_error
        sleep(2)
    pytest.skip(last_error)
    return container_name


@pytest.fixture(scope="session")
def oracle_engine(shared_oracle_container: str) -> Generator[FlextDbOracleApi]:
    """Create Oracle database API fixture for integration verification.

    Skips tests if Oracle is not available.
    """
    _ = shared_oracle_container
    api = FlextDbOracleApi(
        FlextDbOracleSettings.model_validate({
            "host": os.getenv("TEST_ORACLE_HOST", c.TargetOracle.Tests.ORACLE_HOST),
            "port": int(
                os.getenv(
                    "TEST_ORACLE_PORT",
                    str(c.TargetOracle.Tests.ORACLE_PORT),
                )
            ),
            "service_name": os.getenv(
                "TEST_ORACLE_SERVICE",
                c.TargetOracle.Tests.ORACLE_SERVICE,
            ),
            "username": os.getenv(
                "TEST_ORACLE_USER",
                c.TargetOracle.Tests.TEST_SCHEMA,
            ),
            "password": os.getenv("TEST_ORACLE_PASSWORD", "test_password"),
        })
    )
    connect_result = api.connect()
    if connect_result.failure:
        pytest.skip(connect_result.error or "Oracle not available")
    health_result = api.oracle_services.execute_query('SELECT 1 AS "health" FROM DUAL')
    if health_result.failure:
        disconnect_result = api.disconnect()
        _ = disconnect_result
        pytest.skip(health_result.error or "Oracle health check failed")
    yield api
    disconnect_result = api.disconnect()
    _ = disconnect_result


@pytest.fixture
def clean_database(oracle_engine: FlextDbOracleApi) -> None:
    """Clean database before each test."""
    tables_result = oracle_engine.oracle_services.execute_query(
        'SELECT table_name AS "table_name" FROM all_tables WHERE owner = :schema',
        m.ConfigMap(root={"schema": c.TargetOracle.Tests.TEST_SCHEMA}),
    )
    assert tables_result.success, tables_result.error
    tables = [str(row.root["table_name"]) for row in tables_result.value]
    for table in tables:
        drop_result = oracle_engine.execute_statement(
            f"DROP TABLE {c.TargetOracle.Tests.TEST_SCHEMA}.{table} CASCADE CONSTRAINTS"
        )
        assert drop_result.success, drop_result.error


@pytest.fixture
def oracle_config(shared_oracle_container: str) -> FlextTargetOracleSettings:
    """Create Oracle target configuration for tests."""
    _ = shared_oracle_container
    return FlextTargetOracleSettings.model_validate({
        "oracle_host": os.getenv("TEST_ORACLE_HOST", c.TargetOracle.Tests.ORACLE_HOST),
        "oracle_port": int(
            os.getenv(
                "TEST_ORACLE_PORT",
                str(c.TargetOracle.Tests.ORACLE_PORT),
            )
        ),
        "oracle_service_name": os.getenv(
            "TEST_ORACLE_SERVICE",
            c.TargetOracle.Tests.ORACLE_SERVICE,
        ),
        "oracle_user": os.getenv(
            "TEST_ORACLE_USER",
            c.TargetOracle.Tests.TEST_SCHEMA,
        ),
        "oracle_password": os.getenv("TEST_ORACLE_PASSWORD", "test_password"),
        "default_target_schema": c.TargetOracle.Tests.TEST_SCHEMA,
        "batch_size": 1000,
        "use_bulk_operations": True,
        "parallel_degree": 1,
    })


@pytest.fixture
def oracle_target(oracle_config: FlextTargetOracleSettings) -> FlextTargetOracle:
    """Create FlextTargetOracle instance."""
    return FlextTargetOracle(settings=oracle_config)


@pytest.fixture
def sample_config() -> FlextTargetOracleSettings:
    """Sample configuration for unit testing (no Oracle connection required)."""
    return FlextTargetOracleSettings.model_validate({
        "oracle_host": c.TargetOracle.Tests.ORACLE_HOST,
        "oracle_port": c.TargetOracle.Tests.ORACLE_PORT,
        "oracle_service_name": c.TargetOracle.Tests.ORACLE_SERVICE,
        "oracle_user": "test_user",
        "oracle_password": "test_password",
        "default_target_schema": "TEST_SCHEMA",
        "batch_size": 1000,
        "use_bulk_operations": True,
    })


@pytest.fixture
def sample_target(sample_config: FlextTargetOracleSettings) -> FlextTargetOracle:
    """Create FlextTargetOracle instance for unit testing."""
    return FlextTargetOracle(settings=sample_config)


@pytest.fixture
def mock_oracle_api() -> Mock:
    """Create mocked FlextDbOracleApi for unit tests."""
    mock_api = Mock()
    mock_api.__enter__ = Mock(return_value=mock_api)
    mock_api.__exit__ = Mock(return_value=None)
    mock_api.connect.return_value = MagicMock(
        success=True,
        failure=False,
        value=None,
    )
    mock_api.disconnect.return_value = MagicMock(
        success=True,
        failure=False,
        value=None,
    )
    mock_api.get_tables.return_value = MagicMock(
        success=True,
        failure=False,
        value=[],
    )
    mock_api.create_table_ddl.return_value = MagicMock(
        success=True,
        failure=False,
        value="CREATE TABLE...",
    )
    mock_api.execute_ddl.return_value = MagicMock(
        success=True,
        failure=False,
        value=None,
    )
    mock_api.build_insert_statement.return_value = MagicMock(
        success=True,
        failure=False,
        value="INSERT INTO...",
    )
    mock_api.build_merge_statement.return_value = MagicMock(
        success=True,
        failure=False,
        value="MERGE INTO...",
    )
    mock_api.query.return_value = MagicMock(
        success=True,
        failure=False,
        value=None,
    )
    mock_api.execute_batch.return_value = MagicMock(
        success=True,
        failure=False,
        value=None,
    )
    mock_api.get_columns.return_value = MagicMock(
        success=True,
        failure=False,
        value=[],
    )
    mock_api.connection = MagicMock()
    return mock_api


@pytest.fixture
def schema() -> t.JsonMapping:
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
def record() -> t.JsonMapping:
    """Simple Singer record message for unit testing."""
    return {
        "type": "RECORD",
        "stream": "users",
        "record": {"id": 1, "name": "John Doe", "email": "john@example.com"},
    }


@pytest.fixture
def state() -> t.JsonMapping:
    """Simple Singer state message for unit testing."""
    return {
        "type": "STATE",
        "value": {"bookmarks": {"users": {"last_updated": "2025-01-01T00:00:00Z"}}},
    }


@pytest.fixture
def simple_schema() -> t.JsonMapping:
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
def nested_schema() -> t.JsonMapping:
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
def sample_record() -> t.JsonMapping:
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
def batch_records() -> t.SequenceOf[t.JsonMapping]:
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
        for i in range(1, 101)
    ]


@pytest.fixture
def state_message() -> t.JsonMapping:
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
    simple_schema: t.JsonMapping,
    sample_record: t.JsonMapping,
    state_message: t.JsonMapping,
) -> t.SequenceOf[t.JsonMapping]:
    """Complete Singer message stream for testing."""
    return [simple_schema, sample_record, sample_record, state_message]


@contextmanager
def temporary_env_vars(**kwargs: str | None) -> Generator[None]:
    """Temporarily set environment variables."""
    old_values: dict[str, str | None] = {}
    for key, value in kwargs.items():
        old_values[key] = os.environ.get(key)
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value
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
    config_data: t.JsonValue = {
        "oracle_host": c.TargetOracle.Tests.ORACLE_HOST,
        "oracle_port": c.TargetOracle.Tests.ORACLE_PORT,
        "oracle_service_name": c.TargetOracle.Tests.ORACLE_SERVICE,
        "oracle_user": c.TargetOracle.Tests.TEST_SCHEMA,
        "oracle_password": "test_password",
        "default_target_schema": c.TargetOracle.Tests.TEST_SCHEMA,
        "batch_size": 1000,
        "use_bulk_operations": True,
    }
    config_file = tmp_path / "settings.json"
    config_file.write_text(
        t.Tests.NORMALIZED_VALUE_ADAPTER.dump_json(config_data).decode("utf-8"),
    )
    return config_file


@pytest.fixture
def oracle_loader(
    oracle_config: FlextTargetOracleSettings,
    oracle_engine: FlextDbOracleApi,
) -> Generator[FlextTargetOracleLoader]:
    """Provide a connected FlextTargetOracleLoader instance."""
    _ = oracle_engine
    loader = FlextTargetOracleLoader(oracle_config)
    connect_result = loader.connect()
    if connect_result.failure:
        pytest.skip(connect_result.error or "Oracle loader could not connect")
    yield loader
    disconnect_result = loader.disconnect()
    _ = disconnect_result


@pytest.fixture
def large_dataset() -> t.SequenceOf[m.Dict]:
    """Generate large dataset for performance testing."""
    schema = t.Tests.DICT_ADAPTER.validate_python({
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
    })
    records = [
        t.Tests.DICT_ADAPTER.validate_python({
            "type": "RECORD",
            "stream": "performance_test",
            "record": {
                "id": i,
                "data": f"Performance test data {i}" * 10,
                "value": i * 1.5,
                "timestamp": f"2025-01-20T12:{i % 60:02d}:00Z",
            },
        })
        for i in range(10000)
    ]
    result: list[m.Dict] = []
    result.append(schema)
    result.extend(records)
    return result


def pytest_collection_modifyitems(items: t.SequenceOf[pytest.Item]) -> None:
    """Add markers to test items based on their location."""
    for item in items:
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
