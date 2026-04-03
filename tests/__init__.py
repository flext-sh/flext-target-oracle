# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.decorators import FlextDecorators as d
from flext_core.exceptions import FlextExceptions as e
from flext_core.handlers import FlextHandlers as h
from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_core.mixins import FlextMixins as x
from flext_core.result import FlextResult as r
from flext_core.service import FlextService as s
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
    record,
    reset_settings_singleton,
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
from tests.constants import (
    FlextTargetOracleTestConstants,
    FlextTargetOracleTestConstants as c,
)
from tests.e2e.test_singer import TestSingerWorkflowE2E
from tests.integration.test_oracle import TestOracleIntegration, TestOracleTargetE2E
from tests.models import (
    FlextTargetOracleTestModels,
    FlextTargetOracleTestModels as m,
)
from tests.performance.test_performance import TestPerformance
from tests.protocols import (
    FlextTargetOracleTestProtocols,
    FlextTargetOracleTestProtocols as p,
)
from tests.typings import (
    FlextTargetOracleTestTypes,
    FlextTargetOracleTestTypes as t,
)
from tests.unit.test_config import TestOracleSettings
from tests.unit.test_loader import (
    loader_config,
    test_ensure_table_exists_returns_result,
    test_load_record_buffers_and_finalize,
    test_loader_execute_returns_ready_payload,
)
from tests.unit.test_target import TestOracleTarget, target
from tests.utilities import (
    FlextTargetOracleTestUtilities,
    FlextTargetOracleTestUtilities as u,
)

if _t.TYPE_CHECKING:
    import tests.conftest as _tests_conftest

    conftest = _tests_conftest
    import tests.constants as _tests_constants

    constants = _tests_constants
    import tests.e2e as _tests_e2e

    e2e = _tests_e2e
    import tests.e2e.test_singer as _tests_e2e_test_singer

    test_singer = _tests_e2e_test_singer
    import tests.integration as _tests_integration

    integration = _tests_integration
    import tests.integration.test_oracle as _tests_integration_test_oracle

    test_oracle = _tests_integration_test_oracle
    import tests.models as _tests_models

    models = _tests_models
    import tests.performance as _tests_performance

    performance = _tests_performance
    import tests.performance.test_performance as _tests_performance_test_performance

    test_performance = _tests_performance_test_performance
    import tests.protocols as _tests_protocols

    protocols = _tests_protocols
    import tests.typings as _tests_typings

    typings = _tests_typings
    import tests.unit as _tests_unit

    unit = _tests_unit
    import tests.unit.test_config as _tests_unit_test_config

    test_config = _tests_unit_test_config
    import tests.unit.test_loader as _tests_unit_test_loader

    test_loader = _tests_unit_test_loader
    import tests.unit.test_target as _tests_unit_test_target

    test_target = _tests_unit_test_target
    import tests.utilities as _tests_utilities

    utilities = _tests_utilities

    _ = (
        DOCKER_COMPOSE_PATH,
        FlextTargetOracleTestConstants,
        FlextTargetOracleTestModels,
        FlextTargetOracleTestProtocols,
        FlextTargetOracleTestTypes,
        FlextTargetOracleTestUtilities,
        ORACLE_CONTAINER_NAME,
        ORACLE_HOST,
        ORACLE_IMAGE,
        ORACLE_PASSWORD,
        ORACLE_PORT,
        ORACLE_SERVICE,
        ORACLE_USER,
        TEST_SCHEMA,
        TestOracleIntegration,
        TestOracleSettings,
        TestOracleTarget,
        TestOracleTargetE2E,
        TestPerformance,
        TestSingerWorkflowE2E,
        batch_records,
        c,
        clean_database,
        conftest,
        connected_loader,
        constants,
        d,
        docker_control,
        e,
        e2e,
        event_loop,
        h,
        integration,
        large_dataset,
        loader_config,
        logger,
        m,
        mock_loader,
        mock_oracle_api,
        models,
        nested_schema,
        oracle_api,
        oracle_config,
        oracle_engine,
        oracle_loader,
        oracle_target,
        p,
        performance,
        protocols,
        pytest_collection_modifyitems,
        pytest_configure,
        r,
        record,
        reset_settings_singleton,
        s,
        sample_config,
        sample_record,
        sample_target,
        schema,
        shared_oracle_container,
        simple_schema,
        singer_messages,
        state,
        state_message,
        t,
        target,
        temp_config_file,
        temporary_env_vars,
        test_config,
        test_ensure_table_exists_returns_result,
        test_load_record_buffers_and_finalize,
        test_loader,
        test_loader_execute_returns_ready_payload,
        test_oracle,
        test_performance,
        test_singer,
        test_target,
        typings,
        u,
        unit,
        utilities,
        x,
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
        "r": ("flext_core.result", "FlextResult"),
        "record": "tests.conftest",
        "reset_settings_singleton": "tests.conftest",
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
    "r",
    "record",
    "reset_settings_singleton",
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
