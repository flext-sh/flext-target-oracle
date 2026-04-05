# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _t.TYPE_CHECKING:
    import tests.conftest as _tests_conftest

    conftest = _tests_conftest
    import tests.constants as _tests_constants
    from tests.conftest import (
        DOCKER_COMPOSE_PATH,
        ORACLE_CONTAINER_NAME,
        ORACLE_HOST,
        ORACLE_IMAGE,
        ORACLE_PASSWORD,
        ORACLE_PORT,
        ORACLE_SERVICE,
        ORACLE_USER,
        TEST_SCHEMA,
        batch_records,
        clean_database,
        connected_loader,
        docker_control,
        event_loop,
        large_dataset,
        logger,
        mock_loader,
        mock_oracle_api,
        nested_schema,
        oracle_api,
        oracle_config,
        oracle_engine,
        oracle_loader,
        oracle_target,
        pytest_collection_modifyitems,
        pytest_configure,
        pytest_plugins,
        record,
        sample_config,
        sample_record,
        sample_target,
        schema,
        shared_oracle_container,
        simple_schema,
        singer_messages,
        state,
        state_message,
        temp_config_file,
        temporary_env_vars,
    )

    constants = _tests_constants
    import tests.e2e as _tests_e2e
    from tests.constants import (
        FlextTargetOracleTestConstants,
        FlextTargetOracleTestConstants as c,
    )

    e2e = _tests_e2e
    import tests.integration as _tests_integration
    from tests.e2e import TestSingerWorkflowE2E, test_singer

    integration = _tests_integration
    import tests.models as _tests_models
    from tests.integration import (
        TestOracleIntegration,
        TestOracleTargetE2E,
        test_oracle,
    )

    models = _tests_models
    import tests.performance as _tests_performance
    from tests.models import (
        FlextTargetOracleTestModels,
        FlextTargetOracleTestModels as m,
    )

    performance = _tests_performance
    import tests.protocols as _tests_protocols
    from tests.performance import TestPerformance, test_performance

    protocols = _tests_protocols
    import tests.typings as _tests_typings
    from tests.protocols import (
        FlextTargetOracleTestProtocols,
        FlextTargetOracleTestProtocols as p,
    )

    typings = _tests_typings
    import tests.unit as _tests_unit
    from tests.typings import (
        FlextTargetOracleTestTypes,
        FlextTargetOracleTestTypes as t,
    )

    unit = _tests_unit
    import tests.utilities as _tests_utilities
    from tests.unit import (
        TestOracleSettings,
        TestOracleTarget,
        loader_config,
        target,
        test_config,
        test_ensure_table_exists_returns_result,
        test_load_record_buffers_and_finalize,
        test_loader,
        test_loader_execute_returns_ready_payload,
        test_target,
    )

    utilities = _tests_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from tests.utilities import (
        FlextTargetOracleTestUtilities,
        FlextTargetOracleTestUtilities as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
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
        "d": ("flext_core.decorators", "FlextDecorators"),
        "docker_control": "tests.conftest",
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "e2e": "tests.e2e",
        "event_loop": "tests.conftest",
        "h": ("flext_core.handlers", "FlextHandlers"),
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
        "pytest_plugins": "tests.conftest",
        "r": ("flext_core.result", "FlextResult"),
        "record": "tests.conftest",
        "s": ("flext_core.service", "FlextService"),
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
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)

__all__ = [
    "DOCKER_COMPOSE_PATH",
    "ORACLE_CONTAINER_NAME",
    "ORACLE_HOST",
    "ORACLE_IMAGE",
    "ORACLE_PASSWORD",
    "ORACLE_PORT",
    "ORACLE_SERVICE",
    "ORACLE_USER",
    "TEST_SCHEMA",
    "FlextTargetOracleTestConstants",
    "FlextTargetOracleTestModels",
    "FlextTargetOracleTestProtocols",
    "FlextTargetOracleTestTypes",
    "FlextTargetOracleTestUtilities",
    "TestOracleIntegration",
    "TestOracleSettings",
    "TestOracleTarget",
    "TestOracleTargetE2E",
    "TestPerformance",
    "TestSingerWorkflowE2E",
    "batch_records",
    "c",
    "clean_database",
    "conftest",
    "connected_loader",
    "constants",
    "d",
    "docker_control",
    "e",
    "e2e",
    "event_loop",
    "h",
    "integration",
    "large_dataset",
    "loader_config",
    "logger",
    "m",
    "mock_loader",
    "mock_oracle_api",
    "models",
    "nested_schema",
    "oracle_api",
    "oracle_config",
    "oracle_engine",
    "oracle_loader",
    "oracle_target",
    "p",
    "performance",
    "protocols",
    "pytest_collection_modifyitems",
    "pytest_configure",
    "pytest_plugins",
    "r",
    "record",
    "s",
    "sample_config",
    "sample_record",
    "sample_target",
    "schema",
    "shared_oracle_container",
    "simple_schema",
    "singer_messages",
    "state",
    "state_message",
    "t",
    "target",
    "temp_config_file",
    "temporary_env_vars",
    "test_config",
    "test_ensure_table_exists_returns_result",
    "test_load_record_buffers_and_finalize",
    "test_loader",
    "test_loader_execute_returns_ready_payload",
    "test_oracle",
    "test_performance",
    "test_singer",
    "test_target",
    "typings",
    "u",
    "unit",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
