"""
Test helpers for Oracle Target tests.

This module provides utilities for testing Oracle functionality including
connection management, table cleanup, and test configuration.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import pytest
from dotenv import load_dotenv
from sqlalchemy import text


def has_valid_env_config() -> bool:
    """Check if we have valid Oracle configuration in .env file."""
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
    return os.getenv("DATABASE__SERVICE_NAME") or os.getenv("DATABASE__DATABASE")


def get_test_config(include_licensed_features: bool = False) -> dict:
    """Get test configuration from environment with safe defaults."""
    if not has_valid_env_config():
        raise ValueError("Valid Oracle configuration not found in .env file")

    config = {
        # Connection settings from env
        "host": os.getenv("DATABASE__HOST"),
        "port": int(os.getenv("DATABASE__PORT", "1521")),
        "username": os.getenv("DATABASE__USERNAME"),
        "password": os.getenv("DATABASE__PASSWORD").strip('"')
        if os.getenv("DATABASE__PASSWORD")
        else None,
        "protocol": os.getenv("DATABASE__PROTOCOL", "tcp"),
        "schema": os.getenv("DATABASE__SCHEMA", os.getenv("DATABASE__USERNAME")),
        # Service name or database
        "service_name": os.getenv("DATABASE__SERVICE_NAME"),
        "database": os.getenv("DATABASE__DATABASE"),
        # SSL/TCPS settings
        "ssl_server_dn_match": os.getenv(
            "DATABASE__SSL_SERVER_DN_MATCH", "false"
        ).lower()
        == "true",
        "ssl_server_cert_dn": os.getenv("DATABASE__SSL_SERVER_CERT_DN"),
        "wallet_location": os.getenv("DATABASE__WALLET_LOCATION"),
        "wallet_password": os.getenv("DATABASE__WALLET_PASSWORD"),
        # Default safe settings
        "add_record_metadata": True,
        "validate_records": True,
        "default_target_schema": os.getenv(
            "DEFAULT_TARGET_SCHEMA", os.getenv("DATABASE__USERNAME")
        ),
        # Performance settings (safe defaults)
        "pool_size": 5,
        "max_overflow": 10,
        "array_size": 100,
        "prefetch_rows": 100,
        "batch_config": {"batch_size": 100, "batch_wait_limit_seconds": 1.0},
        # Check if EE from environment or default to True for Autonomous DB
        "oracle_is_enterprise_edition": os.getenv(
            "ORACLE_IS_ENTERPRISE_EDITION", "true"
        ).lower()
        == "true",
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
    config = {k: v for k, v in config.items() if v is not None}

    return config


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


def validate_oracle_features(connection) -> dict[str, bool]:
    """Check which Oracle features are available in the database."""
    features = {
        "is_enterprise_edition": False,
        "partitioning": False,
        "advanced_compression": False,
        "inmemory": False,
        "advanced_security": False,
    }

    # First check if it's Enterprise Edition
    try:
        result = connection.execute("""
            SELECT BANNER FROM v$version
            WHERE BANNER LIKE '%Enterprise Edition%'
        """).fetchone()
        features["is_enterprise_edition"] = result is not None
    except:
        # If we can't check, assume it's not EE
        features["is_enterprise_edition"] = False

    # Only check EE features if it's Enterprise Edition
    if not features["is_enterprise_edition"]:
        return features

    try:
        # Check for partitioning
        result = connection.execute("""
            SELECT COUNT(*) FROM v$option
            WHERE parameter = 'Partitioning' AND value = 'TRUE'
        """).scalar()
        features["partitioning"] = result > 0
    except:
        pass

    try:
        # Check for advanced compression
        result = connection.execute("""
            SELECT COUNT(*) FROM v$option
            WHERE parameter = 'Advanced Compression' AND value = 'TRUE'
        """).scalar()
        features["advanced_compression"] = result > 0
    except:
        pass

    try:
        # Check for in-memory
        result = connection.execute("""
            SELECT COUNT(*) FROM v$option
            WHERE parameter = 'In-Memory Column Store' AND value = 'TRUE'
        """).scalar()
        features["inmemory"] = result > 0
    except:
        pass

    try:
        # Check for advanced security
        result = connection.execute("""
            SELECT COUNT(*) FROM v$option
            WHERE parameter = 'Advanced Security' AND value = 'TRUE'
        """).scalar()
        features["advanced_security"] = result > 0
    except:
        pass

    return features


@contextmanager
def oracle_connection(config: dict[str, Any] | None = None):
    """Context manager for Oracle connections."""
    if config is None:
        config = get_test_config()

    from flext_target_oracle.connectors import OracleConnector

    connector = OracleConnector(config)
    engine = connector._engine

    try:
        with engine.connect() as conn:
            yield conn
    finally:
        engine.dispose()


def clean_test_table(table_name: str, config: dict[str, Any] | None = None) -> None:
    """Clean up a specific test table."""
    if config is None:
        config = get_test_config()

    try:
        with oracle_connection(config) as conn, conn.begin():
            conn.execute(text(f"DROP TABLE {table_name} CASCADE CONSTRAINTS"))
            print(f"✅ Cleaned test table: {table_name}")
    except Exception as e:
        print(f"⚠️ Could not clean table {table_name}: {e}")


def clean_all_test_tables(config: dict[str, Any] | None = None) -> None:
    """Clean up all test tables."""
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
                    text(f"""
                        SELECT table_name
                        FROM user_tables
                        WHERE table_name LIKE '{pattern}'
                    """)
                )

                for row in result:
                    table_name = row[0]
                    try:
                        conn.execute(
                            text(f"DROP TABLE {table_name} CASCADE CONSTRAINTS")
                        )
                        print(f"✅ Cleaned test table: {table_name}")
                    except Exception as e:
                        print(f"⚠️ Could not clean table {table_name}: {e}")

    except Exception as e:
        print(f"❌ Error during cleanup: {e}")


def setup_test_table(
    table_name: str, schema: dict, config: dict[str, Any] | None = None
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
    print(f"✅ Created test table: {table_name}")


class TestTableManager:
    """Context manager for test table lifecycle."""

    def __init__(
        self, table_name: str, schema: dict, config: dict[str, Any] | None = None
    ):
        self.table_name = table_name
        self.schema = schema
        self.config = config or get_test_config()

    def __enter__(self):
        setup_test_table(self.table_name, self.schema, self.config)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        clean_test_table(self.table_name, self.config)


def count_test_tables(config: dict[str, Any] | None = None) -> int:
    """Count how many test tables exist."""
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
                    text(f"""
                    SELECT COUNT(*)
                    FROM user_tables
                    WHERE table_name LIKE '{pattern}'
                """)
                )
                count = result.scalar()
                total_count += count

    except Exception as e:
        print(f"❌ Error counting test tables: {e}")

    return total_count


def validate_table_structure(
    table_name: str, expected_columns: list[str], config: dict[str, Any] | None = None
) -> bool:
    """Validate that a table has the expected structure."""
    if config is None:
        config = get_test_config()

    try:
        with oracle_connection(config) as conn:
            result = conn.execute(
                text(f"""
                SELECT column_name
                FROM user_tab_columns
                WHERE table_name = '{table_name.upper()}'
                ORDER BY column_name
            """)
            )

            actual_columns = {row[0] for row in result}
            expected_columns_set = {col.upper() for col in expected_columns}

            return expected_columns_set.issubset(actual_columns)

    except Exception as e:
        print(f"❌ Error validating table structure: {e}")
        return False


def get_table_row_count(table_name: str, config: dict[str, Any] | None = None) -> int:
    """Get the number of rows in a table."""
    if config is None:
        config = get_test_config()

    try:
        with oracle_connection(config) as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            return result.scalar()
    except Exception as e:
        print(f"❌ Error getting row count for {table_name}: {e}")
        return 0
