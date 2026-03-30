# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import *

    from tests import conftest, constants, models, protocols, typings, utilities
    from tests.conftest import *
    from tests.constants import *
    from tests.e2e import *
    from tests.integration import *
    from tests.models import *
    from tests.performance import *
    from tests.protocols import *
    from tests.typings import *
    from tests.unit import *
    from tests.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "DOCKER_COMPOSE_PATH": "tests.conftest",
    "FlextTargetOracleTestConstants": "tests.constants",
    "FlextTargetOracleTestModels": "tests.models",
    "FlextTargetOracleTestProtocols": "tests.protocols",
    "FlextTargetOracleTestTypes": "tests.typings",
    "FlextTargetOracleTestUtilities": "tests.utilities",
    "ORACLE_CONTAINER_NAME": "tests.conftest",
    "ORACLE_HOST": "tests.conftest",
    "ORACLE_IMAGE": "tests.conftest",
    "ORACLE_PASSWORD": "tests.conftest",
    "ORACLE_PORT": "tests.conftest",
    "ORACLE_SERVICE": "tests.conftest",
    "ORACLE_USER": "tests.conftest",
    "TEST_SCHEMA": "tests.conftest",
    "TestOracleIntegration": "tests.integration.test_oracle",
    "TestOracleSettings": "tests.unit.test_config",
    "TestOracleTarget": "tests.unit.test_target",
    "TestOracleTargetE2E": "tests.integration.test_oracle",
    "TestPerformance": "tests.performance.test_performance",
    "TestSingerWorkflowE2E": "tests.e2e.test_singer",
    "batch_records": "tests.conftest",
    "c": ["tests.constants", "FlextTargetOracleTestConstants"],
    "clean_database": "tests.conftest",
    "conftest": "tests.conftest",
    "connected_loader": "tests.conftest",
    "constants": "tests.constants",
    "d": "flext_tests",
    "docker_control": "tests.conftest",
    "e": "flext_tests",
    "e2e": "tests.e2e",
    "event_loop": "tests.conftest",
    "h": "flext_tests",
    "integration": "tests.integration",
    "large_dataset": "tests.conftest",
    "loader_config": "tests.unit.test_loader",
    "logger": "tests.conftest",
    "m": ["tests.models", "FlextTargetOracleTestModels"],
    "mock_loader": "tests.conftest",
    "mock_oracle_api": "tests.conftest",
    "models": "tests.models",
    "nested_schema": "tests.conftest",
    "oracle_api": "tests.conftest",
    "oracle_config": "tests.conftest",
    "oracle_engine": "tests.conftest",
    "oracle_loader": "tests.conftest",
    "oracle_target": "tests.conftest",
    "p": ["tests.protocols", "FlextTargetOracleTestProtocols"],
    "performance": "tests.performance",
    "protocols": "tests.protocols",
    "pytest_collection_modifyitems": "tests.conftest",
    "pytest_configure": "tests.conftest",
    "r": "flext_tests",
    "record": "tests.conftest",
    "reset_settings_singleton": "tests.conftest",
    "s": "flext_tests",
    "sample_config": "tests.conftest",
    "sample_record": "tests.conftest",
    "sample_target": "tests.conftest",
    "schema": "tests.conftest",
    "shared_oracle_container": "tests.conftest",
    "simple_schema": "tests.conftest",
    "singer_messages": "tests.conftest",
    "state": "tests.conftest",
    "state_message": "tests.conftest",
    "t": ["tests.typings", "FlextTargetOracleTestTypes"],
    "target": "tests.unit.test_target",
    "temp_config_file": "tests.conftest",
    "temporary_env_vars": "tests.conftest",
    "test_cli_dispatcher": "tests.unit.test_cli_dispatcher",
    "test_cli_service_falls_back_to_bus_when_flag_disabled": "tests.unit.test_cli_dispatcher",
    "test_cli_service_uses_dispatcher_when_flag_enabled": "tests.unit.test_cli_dispatcher",
    "test_config": "tests.unit.test_config",
    "test_ensure_table_exists_returns_result": "tests.unit.test_loader",
    "test_load_record_buffers_and_finalize": "tests.unit.test_loader",
    "test_loader": "tests.unit.test_loader",
    "test_loader_execute_returns_ready_payload": "tests.unit.test_loader",
    "test_oracle": "tests.integration.test_oracle",
    "test_performance": "tests.performance.test_performance",
    "test_singer": "tests.e2e.test_singer",
    "test_target": "tests.unit.test_target",
    "typings": "tests.typings",
    "u": ["tests.utilities", "FlextTargetOracleTestUtilities"],
    "unit": "tests.unit",
    "utilities": "tests.utilities",
    "x": "flext_tests",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
