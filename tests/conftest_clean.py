"""Clean test configuration - NO external dependencies.

ELIMINATES all dependency issues for clean testing.
"""

from collections.abc import Generator
from typing import Any
from unittest.mock import Mock, patch

import pytest


@pytest.fixture(autouse=True)
def mock_external_dependencies() -> Generator[None]:
    """Mock ALL external dependencies to eliminate import errors."""
    # Mock flext-db-oracle imports
    with patch.dict("sys.modules", {
        "flext_db_oracle": Mock(),
        "flext_db_oracle.FlextDbOracleConfig": Mock(),
        "flext_db_oracle.FlextDbOracleDataTransformer": Mock(),
        "flext_db_oracle.FlextDbOracleSchemaMapper": Mock(),
        "flext_db_oracle.FlextDbOracleTableManager": Mock(),
        "flext_db_oracle.FlextDbOracleTypeConverter": Mock(),
        "flext_db_oracle.application.services.FlextDbOracleConnectionService": Mock(),
    }):
        yield


@pytest.fixture
def clean_config() -> dict[str, Any]:
    """Clean test configuration."""
    return {
        "host": "localhost",
        "port": 1521,
        "service_name": "XEPDB1",
        "username": "test_user",
        "password": "test_pass",
        "default_target_schema": "TEST_SCHEMA",
        "batch_size": 1000,
        "load_method": "append-only",
        "max_parallelism": 2,
    }
