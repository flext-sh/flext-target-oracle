"""Test helpers for Oracle Target tests.

This module provides utilities for testing Oracle functionality including
connection management, table cleanup, and test configuration.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Any, Self

import pytest
import structlog
from dotenv import load_dotenv
from sqlalchemy import text

if TYPE_CHECKING:
    from collections.abc import Generator

# Copyright (c) 2025 FLEXT Team
# Licensed under the MIT License
# SPDX-License-Identifier: MIT

# Configure logger
log = structlog.get_logger(__name__)


def has_valid_env_config() -> bool:
    """Check if valid Oracle environment configuration exists in .env files."""
        # Try to load .env from various locations
    env_locations = [
        Path(".env"),
        Path(__file__).parent.parent / ".env",
        Path.cwd() / ".env",
    ]

    env_loaded = False
    for env_path in env_locations:
        if env_path.exists():
            load_dotenv(env_path)
            env_loaded = True
            break

    if not env_loaded:
        return False

    # Check minimum required environment variables
    required_vars = ["DATABASE__HOST", "DATABASE__USERNAME", "DATABASE__PASSWORD"]

    for var in required_vars:
        if not os.getenv(var):
            return False

    # Must have either service_name or database
    return bool(os.getenv("DATABASE__SERVICE_NAME") or os.getenv("DATABASE__DATABASE"))


def get_test_config(*, include_licensed_features: bool = False) -> dict[str, Any]:
    """Get Oracle test configuration from environment variables."""
    if not has_valid_env_config():
        msg = "Valid Oracle configuration not found in .env file"
        raise ValueError(msg) from None

    config = {
        # Connection settings from env
        "host": os.getenv("DATABASE__HOST"),
        "port": int(os.getenv("DATABASE__PORT", "1521")),
        "username": os.getenv("DATABASE__USERNAME"),
        "password": (
            password.strip('"')
            if (password := os.getenv("DATABASE__PASSWORD"))
            else None
        ),
        "protocol": os.getenv("DATABASE__PROTOCOL", "tcp"),
        "schema": os.getenv("DATABASE__SCHEMA", os.getenv("DATABASE__USERNAME")),
        # Service name or database
        "service_name": os.getenv("DATABASE__SERVICE_NAME"),
        "database": os.getenv("DATABASE__DATABASE"),
        # SSL/TCPS settings
        "ssl_server_dn_match": os.getenv(
            "DATABASE__SSL_SERVER_DN_MATCH",
            "false",
        ).lower()
        == "true",
        "ssl_server_cert_dn": os.getenv("DATABASE__SSL_SERVER_CERT_DN"),
        "wallet_location": os.getenv("DATABASE__WALLET_LOCATION"),
        "wallet_password": os.getenv("DATABASE__WALLET_PASSWORD"),
        # Default safe settings
        "add_record_metadata": True,
        "validate_records": True,
        "default_target_schema": os.getenv(
            "DEFAULT_TARGET_SCHEMA",
            os.getenv("DATABASE__USERNAME"),
        ),
        # Performance settings (safe defaults)
        "pool_size": 5,
        "max_overflow": 10,
        "array_size": 100,
        "prefetch_rows": 100,
        "batch_config": {"batch_size": 100, "batch_wait_limit_seconds": 1.0},
        # Check if EE from environment or default to True for Autonomous DB
        "oracle_is_enterprise_edition": (
            os.getenv(
                "ORACLE_IS_ENTERPRISE_EDITION",
                "true",
            ).lower()
            == "true"
        ),
        "oracle_has_partitioning_option": include_licensed_features,
        "oracle_has_compression_option": include_licensed_features,
        "oracle_has_inmemory_option": include_licensed_features,
        "oracle_has_advanced_security_option": include_licensed_features,
        # Disable features that require licenses
        "enable_compression": False,
        "compression_type": "basic",  # Basic compression is free
        "enable_partitioning": False,
        "use_inmemory": False,
        "index_compression": False,
        "lob_compression": False,
        "lob_deduplication": False,
        "enable_ado": False,
        "enable_ilm": False,
        "enable_heat_map": False,
        # Safe features that don't require licenses
        "use_merge_statements": True,
        "use_bulk_operations": True,
        "create_table_indexes": True,
        "gather_statistics": False,  # Can be slow, disable for tests
        "parallel_degree": 1,  # No parallel by default
    }

    # Remove None values
    return {k: v for k, v in config.items() if v is not None}


# Pytest marker for tests that require Oracle connection
requires_oracle_connection = pytest.mark.skipif(
    not has_valid_env_config(),
    reason="Oracle connection not configured (check .env file)",
)

# Pytest marker for tests that require Enterprise Edition
requires_enterprise_edition = pytest.mark.skipif(
    not (
        has_valid_env_config()
        and os.getenv("ORACLE_IS_ENTERPRISE_EDITION", "false").lower() == "true"
    ),
    reason="Oracle Enterprise Edition features not available",
)

# Pytest marker for tests that require specific Oracle options
requires_partitioning_option = pytest.mark.skipif(
    not (
        has_valid_env_config()
        and os.getenv("ORACLE_HAS_PARTITIONING_OPTION", "false").lower() == "true"
    ),
    reason="Oracle Partitioning option not licensed",
)

requires_compression_option = pytest.mark.skipif(
    not (
        has_valid_env_config()
        and os.getenv("ORACLE_HAS_COMPRESSION_OPTION", "false").lower() == "true"
    ),
    reason="Oracle Advanced Compression option not licensed",
)

requires_inmemory_option = pytest.mark.skipif(
    not (
        has_valid_env_config()
        and os.getenv("ORACLE_HAS_INMEMORY_OPTION", "false").lower() == "true"
    ),
    reason="Oracle In-Memory option not licensed",
)


def validate_oracle_features(connection: Any) -> dict[str, bool]:  # noqa: ANN401
    """Validate Oracle database features and capabilities."""
    features = {
        "is_enterprise_edition": False,
        "partitioning": False,
        "advanced_compression": False,
        "inmemory": False,
        "advanced_security": False,
    }

    # First check if it's Enterprise Edition
    try:
        result = connection.execute(
            """
            SELECT BANNER FROM v$version
            WHERE BANNER LIKE '%Enterprise Edition%'
            """,
        ).fetchone()
        features["is_enterprise_edition"] = result is not None
    except Exception:
        log.exception("Could not detect Oracle edition")
        features["is_enterprise_edition"] = False

    # Only check EE features if it's Enterprise Edition
    if not features["is_enterprise_edition"]:
        return features

    try:
        # Check for partitioning
        result = connection.execute(
            """
            SELECT COUNT(*) FROM v$option
            WHERE parameter = 'Partitioning' AND value = 'TRUE'
            """,
        ).scalar()
        features["partitioning"] = result > 0
    except Exception:
        log.exception("Could not detect partitioning feature")

    try:  # Check for advanced compression
        result = connection.execute(
            """
            SELECT COUNT(*) FROM v$option
            WHERE parameter = 'Advanced Compression' AND value = 'TRUE'
            """,
        ).scalar()
        features["advanced_compression"] = result > 0
    except Exception:
        log.exception("Could not detect advanced compression feature")

    try:  # Check for in-memory
        result = connection.execute(
            """
            SELECT COUNT(*) FROM v$option
            WHERE parameter = 'In-Memory Column Store' AND value = 'TRUE'
            """,
        ).scalar()
        features["inmemory"] = result > 0
    except Exception:
        log.exception("Could not detect in-memory feature")

    try:  # Check for advanced security
        result = connection.execute(
            """
            SELECT COUNT(*) FROM v$option
            WHERE parameter = 'Advanced Security' AND value = 'TRUE'
            """,
        ).scalar()
        features["advanced_security"] = result > 0
    except Exception:
        log.exception("Could not detect advanced security feature")

    return features


@contextmanager
def oracle_connection(config: dict[str, Any] | None = None) -> Generator[Any]:
    """Create Oracle database connection for testing."""
    if config is None:
        config = get_test_config()

    from flext_target_oracle.connectors import (
        OracleConnector,
    )

    connector = OracleConnector(config)
    engine = connector._engine  # noqa: SLF001

    try:
        with engine.connect() as conn:
            yield conn
    finally:
        engine.dispose()


def clean_test_table(table_name: str, config: dict[str, Any] | None = None) -> None:
    """Drop a specific test table if it exists."""
    if config is None:
        config = get_test_config()

    try:
        with oracle_connection(config) as conn, conn.begin():
            conn.execute(text(f"DROP TABLE {table_name} CASCADE CONSTRAINTS"))
            log.error(
                "✅ Cleaned test table: %s",
                table_name,
            )
            # Link: https://github.com/issue/todo
    except Exception:
        log.exception(
            "⚠️ Could not clean table %s",
            table_name,
        )
        # Link: https://github.com/issue/todo


def clean_all_test_tables(config: dict[str, Any] | None = None) -> None:
    """Drop all test tables matching common test patterns."""
    if config is None:
        config = get_test_config()

    test_table_patterns = [
        "test_%",
        "TEST_%",
        "%_test",
        "%_TEST",
    ]

    try:
        with oracle_connection(config) as conn, conn.begin():
            # Find all test tables
            for pattern in test_table_patterns:
                result = conn.execute(
                    text("""
                        SELECT table_name
                        FROM user_tables
                        WHERE table_name LIKE :pattern
                        """),
                    {"pattern": pattern},
                )

                for row in result:
                    table_name = row[0]
                    try:
                        conn.execute(
                            text(f"DROP TABLE {table_name} CASCADE CONSTRAINTS"),
                        )
                        log.error(
                            "✅ Cleaned test table: %s",
                            table_name,
                        )
                    except Exception:

                        log.exception("Could not clean table %s", table_name)

    except Exception:
        log.exception("Error during cleanup")


def setup_test_table(
    table_name: str,
    schema: dict[str, Any],
    config: dict[str, Any] | None = None,
) -> None:
    """Set up a test table with the given schema."""
    if config is None:
        config = get_test_config()

    # Clean up first
    clean_test_table(table_name, config)

    # Create table using connector
    from flext_target_oracle.connectors import OracleConnector

    connector = OracleConnector(config)
    connector.prepare_table(
        full_table_name=table_name,
        schema=schema,
        primary_keys=[],
        as_temp_table=False,
    )
    log.error(
        "✅ Created test table: %s",
        table_name,
    )


class TestTableManager:
    """Context manager for test table lifecycle."""

    def __init__(
        self,
        table_name: str,
        schema: dict[str, Any],
        config: dict[str, Any] | None = None,
    ) -> None:
        """Initialize test table manager."""
        self.table_name = table_name
        self.schema = schema
        self.config = config or get_test_config()

    def __enter__(self) -> Self:
        """Enter the context manager."""
        setup_test_table(self.table_name, self.schema, self.config)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """Exit the context manager."""
        clean_test_table(self.table_name, self.config)


def count_test_tables(config: dict[str, Any] | None = None) -> int:
    """Count all test tables matching common test patterns."""
    if config is None:
        config = get_test_config()

    test_table_patterns = [
        "test_%",
        "TEST_%",
        "%_test",
        "%_TEST",
    ]

    total_count = 0
    try:
        with oracle_connection(config) as conn:
            for pattern in test_table_patterns:
                result = conn.execute(
                    text("""
                        SELECT COUNT(*)
                        FROM user_tables
                        WHERE table_name LIKE :pattern
                        """),
                    {"pattern": pattern},
                )
                count = result.scalar()
                total_count += count

    except Exception:
        log.exception("Error counting test tables")

    return total_count


def validate_table_structure(
    table_name: str,
    expected_columns: list[str],
    config: dict[str, Any] | None = None,
) -> bool:
    """Validate that a table contains all expected columns."""
    if config is None:
        config = get_test_config()

    try:
        with oracle_connection(config) as conn:
            result = conn.execute(
                text("""
                    SELECT column_name
                    FROM user_tab_columns
                    WHERE table_name = :table_name
                    ORDER BY column_name
                """),
                {"table_name": table_name.upper()},
            )

            actual_columns = {row[0] for row in result}
            expected_columns_set = {col.upper() for col in expected_columns}

            return expected_columns_set.issubset(actual_columns)

    except Exception:
        log.exception("Error validating table structure")
        return False


def get_table_row_count(table_name: str, config: dict[str, Any] | None = None) -> int:
    """Get the number of rows in a table."""
    if config is None:
        config = get_test_config()

    try:
        with oracle_connection(config) as conn:
            result = conn.execute(
                text("SELECT COUNT(*) FROM user_tables WHERE table_name = :table_name"),
                {"table_name": table_name.upper()},
            )
            scalar_result = result.scalar()
            return scalar_result if scalar_result is not None else 0
    except Exception:
        log.exception("Error getting row count for %s", table_name)
        return 0
