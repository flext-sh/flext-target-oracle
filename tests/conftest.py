"""
Pytest configuration and fixtures for FLEXT Target Oracle tests.

This module provides comprehensive test fixtures for end-to-end testing
with Oracle Autonomous Database using TCPS connections.
"""

from __future__ import annotations

import json
import os
import tempfile
from contextlib import contextmanager, suppress
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest
import structlog
from sqlalchemy import text

from flext_target_oracle.target import OracleTarget

if TYPE_CHECKING:
    from collections.abc import Generator

    from sqlalchemy.engine import Engine

# Configure structured logging for tests
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def env_config(project_root: Path) -> dict[str, Any]:
    """Load configuration from .env file."""
    env_path = project_root / ".env"
    env_example_path = project_root / ".env.example"

    if not env_path.exists():
        skip_msg = f"Environment file not found: {env_path}\n"
        skip_msg += f"Please copy {env_example_path} to {env_path} and configure with your Oracle database credentials."
        pytest.skip(skip_msg)

    config = {}
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                # Remove quotes if present
                value = value.strip("\"'")

                # Convert boolean strings to actual booleans (except for cert DN)
                if value.lower() in ("true", "false") and "cert_dn" not in key.lower():
                    value = value.lower() == "true"
                elif value.isdigit():
                    # Check if it's a port or other numeric value
                    if key.lower() in ["database__port", "port"]:
                        value = int(value)

                # Handle special case for ssl_server_cert_dn
                if (
                    key.lower()
                    in ["database__ssl_server_cert_dn", "ssl_server_cert_dn"]
                    and value == "false"
                ):
                    # Skip this field if it's false (not a valid DN)
                    continue

                # Convert DATABASE__ prefix to target config format
                if key.startswith("DATABASE__"):
                    config_key = key.replace("DATABASE__", "").lower()
                    config[config_key] = value
                else:
                    config[key.lower()] = value

    # Validate required configuration
    required_keys = ["host", "username", "password"]
    # Either service_name or database (SID) must be provided
    if "service_name" not in config and "database" not in config:
        required_keys.append("service_name or database")

    missing_keys = [key for key in required_keys if key not in config]

    if missing_keys:
        skip_msg = f"Missing required configuration keys: {missing_keys}\n"
        skip_msg += "Please ensure your .env file contains all required fields. See .env.example for reference."
        pytest.skip(skip_msg)

    # Convert port to integer if not already converted
    if "port" in config and isinstance(config["port"], str):
        config["port"] = int(config["port"])

    return config


@pytest.fixture(scope="session")
def oracle_config(env_config: dict[str, Any]) -> dict[str, Any]:
    """Create Oracle target configuration for testing."""
    return {
        **env_config,
        # Test-specific settings
        "batch_size": 1000,
        "max_workers": 2,
        "pool_size": 3,
        "max_overflow": 5,
        "upsert_method": "merge",
        "use_bulk_operations": True,
        "enable_metrics": True,
        "log_sql_statements": False,
        "log_performance_stats": True,
        "max_retries": 3,
        "retry_delay": 1.0,
        "retry_backoff": 1.5,
        "connection_timeout": 30,
        "pool_pre_ping": True,
        "pool_recycle": 3600,
        # Oracle-specific test settings
        "varchar_max_length": 2000,
        "number_precision": 20,
        "number_scale": 5,
        "parallel_degree": 2,
        "array_size": 500,
    }


@pytest.fixture(scope="session")
def oracle_engine(oracle_config: dict[str, Any]) -> Generator[Engine, None, None]:
    """Create SQLAlchemy engine for direct database operations."""
    from flext_target_oracle.connectors import OracleConnector

    # Create connector and engine
    connector = OracleConnector(config=oracle_config)

    try:
        engine = connector.create_engine()

        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 FROM DUAL"))
            row = result.fetchone()
            assert row[0] == 1, "Database connection test failed"

    except Exception as e:
        pytest.skip(f"Cannot connect to Oracle database: {e}")

    yield engine

    # Cleanup
    engine.dispose()


@pytest.fixture(scope="session")
def oracle_edition_info(
    oracle_engine: Engine, oracle_config: dict[str, Any]
) -> dict[str, bool]:
    """Detect Oracle edition and available features."""
    edition_info = {
        "is_enterprise": oracle_config.get("oracle_is_enterprise_edition", False),
        "has_partitioning": oracle_config.get("oracle_has_partitioning_option", False),
        "has_compression": oracle_config.get("oracle_has_compression_option", False),
        "has_inmemory": oracle_config.get("oracle_has_inmemory_option", False),
        "has_advanced_security": oracle_config.get(
            "oracle_has_advanced_security_option", False
        ),
    }

    # If not explicitly set, try to detect edition from database
    if not oracle_config.get("oracle_is_enterprise_edition"):
        try:
            with oracle_engine.connect() as conn:
                # Check V$VERSION for edition info
                result = conn.execute(
                    text("""
                    SELECT BANNER
                    FROM V$VERSION
                    WHERE BANNER LIKE 'Oracle Database%'
                """)
                )
                banner = result.fetchone()
                if banner and banner[0]:
                    edition_info["is_enterprise"] = "Enterprise Edition" in banner[0]

        except Exception as e:
            # If we can't detect, assume Standard Edition but log the issue
            print(f"⚠️ Could not detect Oracle edition from database: {e}")

    return edition_info


@pytest.fixture(scope="function")
def oracle_target(oracle_config: dict[str, Any]) -> OracleTarget:
    """Create Oracle target instance for testing."""
    return OracleTarget(config=oracle_config)


@pytest.fixture(scope="function")
def temp_config_file(oracle_config: dict[str, Any]) -> Generator[str, None, None]:
    """Create temporary configuration file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(oracle_config, f, indent=2)
        config_path = f.name

    yield config_path

    # Cleanup
    with suppress(OSError):
        os.unlink(config_path)


@pytest.fixture(scope="function")
def test_schema_prefix() -> str:
    """Generate unique schema prefix for test isolation."""
    import uuid

    return f"test_{uuid.uuid4().hex[:8]}"


@pytest.fixture(scope="function")
def test_table_name(test_schema_prefix: str) -> str:
    """Generate unique table name for tests."""
    return f"{test_schema_prefix}_users"


@pytest.fixture(scope="function")
def sample_singer_records() -> list[dict[str, Any]]:
    """Generate sample Singer records for testing."""
    return [
        {
            "type": "RECORD",
            "stream": "users",
            "record": {
                "id": 1,
                "name": "John Doe",
                "email": "john.doe@example.com",
                "age": 30,
                "active": True,
                "created_at": "2025-07-02T10:00:00Z",
                "metadata": {"department": "Engineering", "level": "Senior"},
                "score": 95.5,
            },
            "time_extracted": "2025-07-02T10:00:00Z",
        },
        {
            "type": "RECORD",
            "stream": "users",
            "record": {
                "id": 2,
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "age": 28,
                "active": True,
                "created_at": "2025-07-02T10:01:00Z",
                "metadata": {"department": "Marketing", "level": "Manager"},
                "score": 87.3,
            },
            "time_extracted": "2025-07-02T10:01:00Z",
        },
        {
            "type": "RECORD",
            "stream": "users",
            "record": {
                "id": 3,
                "name": "Bob Wilson",
                "email": "bob.wilson@example.com",
                "age": 35,
                "active": False,
                "created_at": "2025-07-02T10:02:00Z",
                "metadata": {"department": "Sales", "level": "Director"},
                "score": 92.1,
            },
            "time_extracted": "2025-07-02T10:02:00Z",
        },
    ]


@pytest.fixture(scope="function")
def sample_singer_schema() -> dict[str, Any]:
    """Generate sample Singer schema for testing."""
    return {
        "type": "SCHEMA",
        "stream": "users",
        "schema": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string", "maxLength": 100},
                "email": {"type": "string", "maxLength": 255},
                "age": {"type": "integer"},
                "active": {"type": "boolean"},
                "created_at": {"type": "string", "format": "date-time"},
                "metadata": {"type": "object"},
                "score": {"type": "number"},
            },
        },
        "key_properties": ["id"],
    }


@pytest.fixture(scope="function")
def bulk_singer_records(test_schema_prefix: str) -> list[dict[str, Any]]:
    """Generate bulk Singer records for performance testing."""
    import random
    from datetime import datetime, timedelta

    records = []
    base_time = datetime.now()

    for i in range(1000):
        record_time = base_time + timedelta(seconds=i)
        records.append(
            {
                "type": "RECORD",
                "stream": "bulk_test",
                "record": {
                    "id": i + 1,
                    "name": f"User {i + 1}",
                    "email": f"user{i + 1}@example.com",
                    "age": random.randint(18, 65),
                    "active": random.choice([True, False]),
                    "created_at": record_time.isoformat() + "Z",
                    "department": random.choice(
                        ["Engineering", "Marketing", "Sales", "HR"]
                    ),
                    "score": round(random.uniform(60.0, 100.0), 2),
                    "metadata": {
                        "region": random.choice(["US", "EU", "APAC"]),
                        "tier": random.choice(["Bronze", "Silver", "Gold", "Platinum"]),
                    },
                },
                "time_extracted": record_time.isoformat() + "Z",
            }
        )

    return records


@pytest.fixture(scope="function")
def bulk_singer_schema() -> dict[str, Any]:
    """Generate bulk Singer schema for performance testing."""
    return {
        "type": "SCHEMA",
        "stream": "bulk_test",
        "schema": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string", "maxLength": 100},
                "email": {"type": "string", "maxLength": 255},
                "age": {"type": "integer"},
                "active": {"type": "boolean"},
                "created_at": {"type": "string", "format": "date-time"},
                "department": {"type": "string", "maxLength": 50},
                "score": {"type": "number"},
                "metadata": {"type": "object"},
            },
        },
        "key_properties": ["id"],
    }


@contextmanager
def cleanup_test_tables(engine: Engine, table_names: list[str]):
    """Context manager to cleanup test tables after tests."""
    try:
        yield
    finally:
        with engine.connect() as conn:
            for table_name in table_names:
                try:
                    conn.execute(text(f"DROP TABLE {table_name} CASCADE CONSTRAINTS"))
                    conn.commit()
                except Exception as e:
                    # Log cleanup errors for debugging but continue
                    print(f"⚠️ Could not cleanup table {table_name}: {e}")


@pytest.fixture(scope="function")
def table_cleanup(oracle_engine: Engine):
    """Fixture to automatically cleanup test tables."""
    tables_to_cleanup = []

    def register_table(table_name: str):
        tables_to_cleanup.append(table_name)

    yield register_table

    # Cleanup
    with oracle_engine.connect() as conn:
        for table_name in tables_to_cleanup:
            try:
                conn.execute(text(f"DROP TABLE {table_name} CASCADE CONSTRAINTS"))
                conn.commit()
            except Exception as e:
                # Log cleanup errors for debugging but continue
                print(f"⚠️ Could not cleanup table {table_name}: {e}")


# Performance test utilities
class PerformanceTimer:
    """Utility class for measuring test performance."""

    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        import time

        self.start_time = time.perf_counter()

    def stop(self):
        import time

        self.end_time = time.perf_counter()

    @property
    def duration(self) -> float:
        if self.start_time is None or self.end_time is None:
            return 0.0
        return self.end_time - self.start_time

    @property
    def duration_ms(self) -> float:
        return self.duration * 1000


@pytest.fixture(scope="function")
def performance_timer() -> PerformanceTimer:
    """Provide performance timing utility."""
    return PerformanceTimer()


# Test data generators
def generate_test_data(record_count: int = 100) -> list[dict[str, Any]]:
    """Generate test data for various test scenarios."""
    import random
    import string
    from datetime import datetime, timedelta

    records = []
    base_time = datetime.now()

    for i in range(record_count):
        # Generate random string data
        name_length = random.randint(5, 30)
        name = "".join(random.choices(string.ascii_letters + " ", k=name_length))

        record_time = base_time + timedelta(seconds=i)
        records.append(
            {
                "type": "RECORD",
                "stream": "test_data",
                "record": {
                    "id": i + 1,
                    "name": name.strip(),
                    "email": f"user{i + 1}@example.com",
                    "age": random.randint(18, 80),
                    "active": random.choice([True, False]),
                    "created_at": record_time.isoformat() + "Z",
                    "score": round(random.uniform(0.0, 100.0), 3),
                    "category": random.choice(["A", "B", "C", "D"]),
                    "notes": "".join(
                        random.choices(
                            string.ascii_letters + " ", k=random.randint(10, 200)
                        )
                    ),
                    "metadata": {
                        "source": random.choice(["web", "api", "mobile"]),
                        "version": f"v{random.randint(1, 10)}.{random.randint(0, 9)}",
                        "tags": random.sample(
                            ["urgent", "normal", "low", "critical", "review"],
                            k=random.randint(1, 3),
                        ),
                    },
                },
                "time_extracted": record_time.isoformat() + "Z",
            }
        )

    return records


# Markers for different test categories
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as requiring database connection"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test (no database required)"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as performance benchmark"
    )
    config.addinivalue_line("markers", "slow: mark test as slow running")
