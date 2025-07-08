"""Test Oracle database connection.

This module tests the basic connection to Oracle Database.
"""

from __future__ import annotations

import logging
from typing import Any

import pytest
from sqlalchemy import text

from flext_target_oracle import OracleTarget
from flext_target_oracle.connectors import OracleConnector
from tests.helpers import requires_oracle_connection

log = logging.getLogger(__name__)


@requires_oracle_connection
class TestOracleConnection:
    """Test Oracle database connection."""

    @pytest.mark.integration
    def test_basic_connection(self, oracle_config: dict[str, Any]) -> None:
        """Test basic database connection."""
        # Create connector
        connector = OracleConnector(config=oracle_config)

        # Test we can create engine
        engine = connector.create_engine()
        assert engine is not None

        # Clean up
        engine.dispose()

    @pytest.mark.integration
    def test_query_execution(self, oracle_config: dict[str, Any]) -> None:
        """Test executing a simple query."""
        connector = OracleConnector(config=oracle_config)
        engine = connector.create_engine()

        try:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1 FROM DUAL"))
                row = result.fetchone()
                assert row[0] == 1
        finally:
            engine.dispose()

    @pytest.mark.integration
    def test_oracle_version_detection(self, oracle_config: dict[str, Any]) -> None:
        """Test Oracle version detection."""
        connector = OracleConnector(config=oracle_config)
        engine = connector.create_engine()

        try:
            with engine.connect() as conn:
                # Get Oracle version
                result = conn.execute(
                    text(
                        """
                    SELECT BANNER
                    FROM V$VERSION
                    WHERE ROWNUM = 1
                """,
                    ),
                )
                banner = result.fetchone()
                assert banner is not None
                assert "Oracle" in banner[0]
                log.error(
                    f"\nOracle Version: {banner[0]}",
                # TODO(@dev): Replace with proper logging  # Link:
                # https://github.com/issue/todo
                )
        finally:
            engine.dispose()

    @pytest.mark.integration
    def test_target_initialization(self, oracle_config: dict[str, Any]) -> None:
        """Test target can be initialized with Oracle config."""
        target = OracleTarget(config=oracle_config)
        assert target.name == "flext-target-oracle"
        assert target.config["host"] == oracle_config["host"]

    @pytest.mark.integration
    def test_table_creation(
        self,
        oracle_engine,
        test_table_name: str,
        table_cleanup,
    ) -> None:
        """Test creating a table."""
        table_cleanup(test_table_name)

        with oracle_engine.connect() as conn:
            # Create simple table
            conn.execute(
                text(
                    f"""
                CREATE TABLE {test_table_name} (
                    id NUMBER PRIMARY KEY,
                    name VARCHAR2(100)
                )
            """,
                ),
            )
            conn.commit()

            # Verify table exists
            result = conn.execute(
                text(
                    f"""
                SELECT COUNT(*)
                FROM USER_TABLES
                WHERE TABLE_NAME = UPPER('{test_table_name}')
            """,
                ),
            )
            count = result.fetchone()[0]
            assert count == 1

    @pytest.mark.integration
    def test_insert_and_select(
        self,
        oracle_engine,
        test_table_name: str,
        table_cleanup,
    ) -> None:
        """Test basic insert and select operations."""
        table_cleanup(test_table_name)

        with oracle_engine.connect() as conn:
            # Create table
            conn.execute(
                text(
                    f"""
                CREATE TABLE {test_table_name} (
                    id NUMBER PRIMARY KEY,
                    value VARCHAR2(100)
                )
            """,
                ),
            )
            conn.commit()

            # Insert data
            conn.execute(
                text(
                    f"""
                INSERT INTO {test_table_name} (id, value)
                VALUES (1, 'test_value')
            """,
                ),
            )
            conn.commit()

            # Select data
            result = conn.execute(
                text(
                    f"""
                SELECT id, value
                FROM {test_table_name}
                WHERE id = 1
            """,
                ),
            )
            row = result.fetchone()
            assert row[0] == 1
            assert row[1] == "test_value"
