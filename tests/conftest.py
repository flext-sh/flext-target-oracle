"""Pytest Configuration and Test Fixtures - FLEXT Target Oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import os
from collections.abc import Generator
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
    FlextTargetOracleLoader,
    FlextTargetOracleSettings,
)
from tests import c, m, t


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
    """Create Oracle database API fixture for integration verification."""
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
def mock_oracle_api() -> Mock:
    """Create mocked FlextDbOracleApi for unit tests."""
    mock_api = Mock()
    mock_api.__enter__ = Mock(return_value=mock_api)
    mock_api.__exit__ = Mock(return_value=None)
    mock_api.connect.return_value = MagicMock(success=True, failure=False, value=None)
    mock_api.disconnect.return_value = MagicMock(
        success=True, failure=False, value=None,
    )
    mock_api.get_tables.return_value = MagicMock(success=True, failure=False, value=[])
    mock_api.create_table_ddl.return_value = MagicMock(
        success=True, failure=False, value="CREATE TABLE...",
    )
    mock_api.execute_ddl.return_value = MagicMock(
        success=True, failure=False, value=None,
    )
    mock_api.execute_dml.return_value = MagicMock(
        success=True, failure=False, value=None,
    )
    mock_api.execute_query.return_value = MagicMock(success=True, failure=False, value=[])
    mock_api.execute_statement.return_value = MagicMock(
        success=True, failure=False, value=None,
    )
    mock_api.execute_many.return_value = MagicMock(
        success=True, failure=False, value=None,
    )
    mock_api.fetch_tables.return_value = MagicMock(success=True, failure=False, value=[])
    mock_api.execute_sql.return_value = MagicMock(success=True, failure=False, value=True)
    mock_api.connection = MagicMock()
    return mock_api


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
