# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if TYPE_CHECKING:
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

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = merge_lazy_imports(
    (
        "tests.e2e",
        "tests.integration",
        "tests.performance",
        "tests.unit",
    ),
    {
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
        "batch_records": "tests.conftest",
        "c": ("tests.constants", "FlextTargetOracleTestConstants"),
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
        "logger": "tests.conftest",
        "m": ("tests.models", "FlextTargetOracleTestModels"),
        "mock_loader": "tests.conftest",
        "mock_oracle_api": "tests.conftest",
        "models": "tests.models",
        "nested_schema": "tests.conftest",
        "oracle_api": "tests.conftest",
        "oracle_config": "tests.conftest",
        "oracle_engine": "tests.conftest",
        "oracle_loader": "tests.conftest",
        "oracle_target": "tests.conftest",
        "p": ("tests.protocols", "FlextTargetOracleTestProtocols"),
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
        "t": ("tests.typings", "FlextTargetOracleTestTypes"),
        "temp_config_file": "tests.conftest",
        "temporary_env_vars": "tests.conftest",
        "typings": "tests.typings",
        "u": ("tests.utilities", "FlextTargetOracleTestUtilities"),
        "unit": "tests.unit",
        "utilities": "tests.utilities",
        "x": "flext_tests",
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
