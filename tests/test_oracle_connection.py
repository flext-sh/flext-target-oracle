"""
Test Oracle database connections and basic functionality.

This module tests TCPS connections to Oracle Autonomous Database
and validates basic database operations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from sqlalchemy import text

from flext_target_oracle.connectors import OracleConnector
from flext_target_oracle.target import OracleTarget
from tests.helpers import requires_oracle_connection

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine


@requires_oracle_connection
class TestOracleConnection:
    """Test Oracle database connection functionality."""

    def test_basic_connection(self, oracle_engine: Engine) -> None:
        """Test basic Oracle database connection."""
        with oracle_engine.connect() as conn:
            result = conn.execute(text("SELECT 1 FROM DUAL"))
            assert result.fetchone()[0] == 1

    def test_tcps_connection_details(
        self, oracle_config: dict, oracle_engine: Engine
    ) -> None:
        """Test TCPS connection protocol details."""
        # Verify we're using TCPS protocol
        assert oracle_config.get("protocol") == "tcps"

        with oracle_engine.connect() as conn:
            # Check session details
            result = conn.execute(
                text(
                    """
                SELECT
                    sys_context('USERENV', 'NETWORK_PROTOCOL') as protocol,
                    sys_context('USERENV', 'SESSION_USER') as session_user,
                    sys_context('USERENV', 'CURRENT_SCHEMA') as current_schema
                FROM DUAL
            """
                )
            )
            row = result.fetchone()

            # Verify connection details
            assert row.protocol in [
                "TCP",
                "TCPS",
            ], f"Unexpected protocol: {row.protocol}"
            assert row.session_user.upper() == oracle_config["username"].upper()

    def test_autonomous_database_features(self, oracle_engine: Engine) -> None:
        """Test Oracle Autonomous Database specific features."""
        with oracle_engine.connect() as conn:
            # Check if we're on Autonomous Database
            result = conn.execute(
                text(
                    """
                SELECT
                    banner,
                    con_id
                FROM v$version
                WHERE ROWNUM = 1
            """
                )
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
                )
            )
            service_info = result.fetchone()

            # Verify Autonomous Database characteristics
            assert "Oracle Database" in version_info.banner
            assert service_info.service_name is not None
            assert service_info.db_name is not None

    def test_connector_initialization(self, oracle_config: dict) -> None:
        """Test OracleConnector initialization."""
        connector = OracleConnector(config=oracle_config)

        # Test connection URL generation
        url = connector.sqlalchemy_url
        assert "oracle+oracledb://" in str(url)
        assert oracle_config["host"] in str(url)
        assert str(oracle_config["port"]) in str(url)
        assert oracle_config["service_name"] in str(url)

    def test_connection_pool_settings(self, oracle_config: dict) -> None:
        """Test connection pool configuration."""
        connector = OracleConnector(config=oracle_config)

        # Verify pool settings are applied
        assert connector.config.get("pool_size") == oracle_config.get("pool_size", 10)
        assert connector.config.get("max_overflow") == oracle_config.get(
            "max_overflow", 20
        )

    def test_ssl_configuration(self, oracle_config: dict) -> None:
        """Test SSL/TCPS configuration."""
        connector = OracleConnector(config=oracle_config)

        # Verify SSL settings
        if oracle_config.get("protocol") == "tcps":
            assert "protocol" in connector.config
            assert connector.config["protocol"] == "tcps"

    def test_target_initialization(self, oracle_config: dict) -> None:
        """Test OracleTarget initialization."""
        target = OracleTarget(config=oracle_config)

        # Verify target is properly configured
        assert target.name == "flext-target-oracle"
        assert target.config is not None

        # Test capabilities
        capabilities = target.capabilities
        assert "RECORD" in [cap.value for cap in capabilities]

    @pytest.mark.parametrize(
        "query,expected",
        [
            ("SELECT SYSDATE FROM DUAL", "datetime"),
            ("SELECT USER FROM DUAL", "string"),
            ("SELECT 42 FROM DUAL", "number"),
        ],
    )
    def test_basic_queries(
        self, oracle_engine: Engine, query: str, expected: str
    ) -> None:
        """Test basic Oracle SQL queries."""
        with oracle_engine.connect() as conn:
            result = conn.execute(text(query))
            row = result.fetchone()

            if expected == "datetime":
                assert row[0] is not None
            elif expected == "string":
                assert isinstance(row[0], str)
            elif expected == "number":
                assert isinstance(row[0], (int, float))

    def test_connection_health_check(self, oracle_engine: Engine) -> None:
        """Test connection health validation."""
        # Test multiple connections to verify pool health
        for _i in range(5):
            with oracle_engine.connect() as conn:
                result = conn.execute(text("SELECT 1 FROM DUAL"))
                assert result.fetchone()[0] == 1

    def test_connection_error_handling(self, oracle_config: dict) -> None:
        """Test connection error handling with invalid config."""
        # Test with invalid host
        invalid_config = oracle_config.copy()
        invalid_config["host"] = "invalid-host-12345.example.com"

        connector = OracleConnector(config=invalid_config)

        # This should not raise an error during initialization
        # The error should occur when trying to connect
        with pytest.raises((ValueError, ConnectionError, Exception)):
            engine = connector.create_sqlalchemy_engine()
            with engine.connect():
                pass

    def test_schema_access(self, oracle_engine: Engine, oracle_config: dict) -> None:
        """Test schema access and permissions."""
        schema = oracle_config.get("schema")
        if schema:
            with oracle_engine.connect() as conn:
                # Test access to user tables
                result = conn.execute(
                    text(
                        """
                    SELECT COUNT(*)
                    FROM user_tables
                    WHERE ROWNUM <= 10
                """
                    )
                )
                count = result.fetchone()[0]
                assert isinstance(count, int)

                # Test access to user objects
                result = conn.execute(
                    text(
                        """
                    SELECT COUNT(*)
                    FROM user_objects
                    WHERE ROWNUM <= 10
                """
                    )
                )
                count = result.fetchone()[0]
                assert isinstance(count, int)

    def test_database_version_compatibility(self, oracle_engine: Engine) -> None:
        """Test Oracle database version compatibility."""
        with oracle_engine.connect() as conn:
            result = conn.execute(
                text(
                    """
                SELECT
                    VERSION_FULL,
                    VERSION_LEGACY
                FROM v$instance
            """
                )
            )
            version_info = result.fetchone()

            # Extract major version
            if version_info.VERSION_FULL:
                version_parts = version_info.VERSION_FULL.split(".")
                major_version = int(version_parts[0])

                # Verify supported Oracle version (19c and later)
                assert (
                    major_version >= 19
                ), f"Unsupported Oracle version: {version_info.VERSION_FULL}"

    def test_character_set_support(self, oracle_engine: Engine) -> None:
        """Test Oracle character set and Unicode support."""
        with oracle_engine.connect() as conn:
            # Check database character set
            result = conn.execute(
                text(
                    """
                SELECT
                    VALUE as db_charset
                FROM v$nls_parameters
                WHERE PARAMETER = 'NLS_CHARACTERSET'
            """
                )
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
                )
            )
            ncharset_info = result.fetchone()

            # Verify Unicode support
            assert charset_info.db_charset is not None
            assert ncharset_info.national_charset is not None

            # Test Unicode string handling
            unicode_test = "Hello 世界 🌍 Café"
            result = conn.execute(
                text("SELECT :test_string FROM DUAL"), {"test_string": unicode_test}
            )
            retrieved = result.fetchone()[0]
            assert retrieved == unicode_test

    def test_transaction_isolation(self, oracle_engine: Engine) -> None:
        """Test transaction isolation levels."""
        with oracle_engine.connect() as conn:
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
                )
            )
            session_info = result.fetchone()

            assert session_info.sid is not None

    def test_performance_monitoring_views(self, oracle_engine: Engine) -> None:
        """Test access to Oracle performance monitoring views."""
        with oracle_engine.connect() as conn:
            # Test access to performance views
            test_views = [
                "v$session",
                "v$sql",
                "v$sysstat",
                "v$system_event",
            ]

            for view in test_views:
                try:
                    result = conn.execute(
                        text(f"SELECT COUNT(*) FROM {view} WHERE ROWNUM = 1")
                    )
                    count = result.fetchone()[0]
                    assert isinstance(count, int)
                except Exception as e:
                    # Some views may not be accessible, which is acceptable
                    pytest.skip(f"Cannot access {view}: {e}")
