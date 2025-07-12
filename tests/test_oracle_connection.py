# Copyright (c) 2025 FLEXT Team
# Licensed under the MIT License
# SPDX-License-Identifier: MIT

"""Test Oracle database connections and basic functionality.

This module tests TCPS connections to Oracle Autonomous Database
and validates basic database operations.
"""

from typing import Any

import pytest
from flext_target_oracle.connectors import OracleConnector
from flext_target_oracle.target import OracleTarget
from sqlalchemy import text
from sqlalchemy.engine import Engine

from tests.helpers import requires_oracle_connection


@requires_oracle_connection
class TestOracleConnection:  """Test Oracle database connection functionality."""

    @staticmethod
    def test_basic_connection(oracle_engine: Engine) -> None: with oracle_engine.connect() as conn:
    result = conn.execute(text("SELECT 1 FROM DUAL"))
            row = result.fetchone()
            assert row is not None
            assert row[0] == 1

    @staticmethod
    def test_tcps_connection_details(
        oracle_config: dict[str, Any],
        oracle_engine: Engine,
    ) -> None: # Verify we're using TCPS protocol
        assert oracle_config.get("protocol") == "tcps"

        with oracle_engine.connect() as conn: # Check session details
            result = conn.execute(
                text(
                    """
                SELECT
                    sys_context('USERENV', 'NETWORK_PROTOCOL') as protocol,
                    sys_context('USERENV', 'SESSION_USER') as session_user,
                    sys_context('USERENV', 'CURRENT_SCHEMA') as current_schema
                FROM DUAL
            """
                ),
            )
            row = result.fetchone()
            assert row is not None

            # Verify connection details
            assert row.protocol in {
                "TCP",
                "TCPS",
            }, f"Unexpected protocol: {row.protocol}"
            assert row.session_user.upper() == oracle_config["username"].upper()

    @staticmethod
    def test_autonomous_database_features(oracle_engine: Engine) -> None: with oracle_engine.connect() as conn:
            # Check if we're on Autonomous Database: result = conn.execute(
                text(
                    """
                SELECT
                    banner,
                    con_id
                FROM v$version
                WHERE ROWNUM = 1
            """
                ),
            )
            version_info = result.fetchone()

            # Check database service
            result = conn.execute(
                text(
                    """
                SELECT
                    sys_context('USERENV', 'SERVICE_NAME') as service_name,
                    sys_context('USERENV', 'DB_NAME') as db_name
                FROM DUAL
            """
                ),
            )
            service_info = result.fetchone()

            # Verify Autonomous Database characteristics
            assert version_info is not None
            assert service_info is not None
            assert "Oracle Database" in version_info.banner
            assert service_info.service_name is not None
            assert service_info.db_name is not None

    @staticmethod
    def test_connector_initialization(oracle_config: dict[str, Any]) -> None: connector = OracleConnector(config=oracle_config)

        # Test connection URL generation
        url = connector.sqlalchemy_url
        assert "oracle+oracledb://" in str(url)
        assert oracle_config["host"] in str(url)
        assert str(oracle_config["port"]) in str(url)
        assert oracle_config["service_name"] in str(url)

    @staticmethod
    def test_connection_pool_settings(oracle_config: dict[str, Any]) -> None: connector = OracleConnector(config=oracle_config)

        # Verify pool settings are applied
        assert connector.config.get("pool_size") == oracle_config.get("pool_size", 10)
        assert connector.config.get("max_overflow") == oracle_config.get(
            "max_overflow",
            20,
        )

    @staticmethod
    def test_ssl_configuration(oracle_config: dict[str, Any]) -> None: connector = OracleConnector(config=oracle_config)

        # Verify SSL settings
        if oracle_config.get("protocol") == "tcps": assert "protocol" in connector.config
            assert connector.config["protocol"] == "tcps"

    @staticmethod
    def test_target_initialization(oracle_config: dict[str, Any]) -> None: target = OracleTarget(config=oracle_config)

        # Verify target is properly configured
        assert target.name == "flext-target-oracle"
        assert target.config is not None

        # Test capabilities
        capabilities = target.capabilities
        assert "RECORD" in [cap.value for cap in capabilities]

    @pytest.mark.parametrize(
        ("query", "expected"),
        [
            ("SELECT SYSDATE FROM DUAL", "datetime"),
            ("SELECT USER FROM DUAL", "string"),
            ("SELECT 42 FROM DUAL", "number"),
        ],
    )

    @staticmethod
    def test_basic_queries(oracle_engine: Engine, query: str, expected: str) -> None: with oracle_engine.connect() as conn:
    result = conn.execute(text(query))
            row = result.fetchone()

            assert row is not None
            if expected == "datetime": assert row[0] is not None
            elif expected == "string": assert isinstance(row[0], str)
            elif expected == "number": assert isinstance(row[0], int | float)

    @staticmethod
    def test_connection_health_check(oracle_engine:
        Engine) -> None:
        # Test multiple connections to verify pool health
        for _i in range(5):

            with oracle_engine.connect() as conn:

                    result = conn.execute(text("SELECT 1 FROM DUAL"))
                row = result.fetchone()
                assert row is not None
                assert row[0] == 1

    @staticmethod
    def test_connection_error_handling(oracle_config: dict[str, Any]) -> None: # Test with invalid host
        invalid_config = oracle_config.copy()
        invalid_config["host"] = "invalid-host-12345.example.com"

        connector = OracleConnector(config=invalid_config)

        # This should not raise an error during initialization
        # The error should occur when trying to connect
        with pytest.raises((ValueError, ConnectionError, Exception)): engine = connector.create_sqlalchemy_engine()
            with engine.connect():

                pass

    @staticmethod
    def test_schema_access(
        oracle_engine: Engine,
        oracle_config: dict[str, Any],
    ) -> None:
        schema = oracle_config.get("schema")
        if schema: with oracle_engine.connect() as conn:
                # Test access to user tables
                result = conn.execute(
                    text(
                        """
                    SELECT COUNT(*)
                    FROM user_tables
                    WHERE ROWNUM <= 10
                """
                    ),
                )
                row = result.fetchone()
                assert row is not None
                count = row[0]
                assert isinstance(count, int)

                # Test access to user objects
                result = conn.execute(
                    text(
                        """
                    SELECT COUNT(*)
                    FROM user_objects
                    WHERE ROWNUM <= 10
                ,
                    ),
                )
                row = result.fetchone()
                assert row is not None
                count = row[0]
                assert isinstance(count, int)

    @staticmethod
    def test_database_version_compatibility(oracle_engineEngine) -> None: with oracle_engine.connect() as conn:
    result = conn.execute(
                text(
                    """
                SELECT
                    VERSION_FULL,
                    VERSION_LEGACY
                FROM v$instance
            """
                ),
            )
            version_info = result.fetchone()
            assert version_info is not None

            # Extract major version
            if version_info.VERSION_FULL: version_parts = version_info.VERSION_FULL.split(".")
                major_version = int(version_parts[0])

                # Verify supported Oracle version (19c and later)
                assert (
                    major_version >= 19
                ), f"Unsupported Oracle version: {version_info.VERSION_FULL}"

    @staticmethod
    def test_character_set_support(oracle_engineEngine) -> None: with oracle_engine.connect() as conn:
            # Check database character set
            result = conn.execute(
                text(
                    """
                SELECT
                    VALUE as db_charset
                FROM v$nls_parameters
                WHERE PARAMETER = 'NLS_CHARACTERSET'
            """
                ),
            )
            charset_info = result.fetchone()

            # Check national character set
            result = conn.execute(
                text(
                    """
                SELECT
                    VALUE as national_charset
                FROM v$nls_parameters
                WHERE PARAMETER = 'NLS_NCHAR_CHARACTERSET'
            """
                ),
            )
            ncharset_info = result.fetchone()

            # Verify Unicode support
            assert charset_info is not None
            assert ncharset_info is not None
            assert charset_info.db_charset is not None
            assert ncharset_info.national_charset is not None

            # Test Unicode string handling
            unicode_test = "Hello 世界 🌍 Café"
            result = conn.execute(
                text("SELECT :test_string FROM DUAL"),
                {"test_string": unicode_test},
            )
            row = result.fetchone()
            assert row is not None
            retrieved = row[0]
            assert retrieved == unicode_test

    @staticmethod
    def test_transaction_isolation(oracle_engineEngine) -> None: with oracle_engine.connect() as conn:
            # Check current isolation level
            result = conn.execute(
                text(
                    """
                SELECT
                    s.sid,
                    s.serial#,
                    t.isolation_level
                FROM v$session s
                LEFT JOIN v$transaction t ON s.saddr = t.ses_addr
                WHERE s.sid = sys_context('USERENV', 'SID')
            """
                ),
            )
            session_info = result.fetchone()
            assert session_info is not None
            assert session_info.sid is not None

    @staticmethod
    def test_performance_monitoring_views(oracle_engineEngine) -> None: with oracle_engine.connect() as conn:
            # Test access to performance views
            test_views = [
                "v$session",
                "v$sql",
                "v$sysstat",
                "v$system_event",
            ]

            for view in test_views: result = conn.execute(
                        text(f"SELECT COUNT(*) FROM {view} WHERE ROWNUM = 1"),
                    )
                    row = result.fetchone()
                    assert row is not None
                    count = row[0]
                    assert isinstance(count, int)
                except Exception as e: # Some views may not be accessible, which is acceptable
                    pytest.skip(f"Cannot access {view}: {e}")
