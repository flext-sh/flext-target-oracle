# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_tests import d, e, h, r, s, x

    from tests import (
        conftest,
        constants,
        e2e,
        integration,
        models,
        performance,
        protocols,
        typings,
        unit,
        utilities,
    )
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
    from tests.e2e import test_singer
    from tests.e2e.test_singer import TestSingerWorkflowE2E
    from tests.integration import test_oracle
    from tests.integration.test_oracle import TestOracleIntegration, TestOracleTargetE2E
    from tests.models import (
        FlextTargetOracleTestModels,
        FlextTargetOracleTestModels as m,
    )
    from tests.performance import test_performance
    from tests.performance.test_performance import TestPerformance
    from tests.protocols import (
        FlextTargetOracleTestProtocols,
        FlextTargetOracleTestProtocols as p,
    )
    from tests.typings import (
        FlextTargetOracleTestTypes,
        FlextTargetOracleTestTypes as t,
    )
    from tests.unit import test_cli_dispatcher, test_config, test_loader, test_target
    from tests.unit.test_cli_dispatcher import (
        test_cli_service_falls_back_to_bus_when_flag_disabled,
        test_cli_service_uses_dispatcher_when_flag_enabled,
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

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "DOCKER_COMPOSE_PATH": ["tests.conftest", "DOCKER_COMPOSE_PATH"],
    "FlextTargetOracleTestConstants": [
        "tests.constants",
        "FlextTargetOracleTestConstants",
    ],
    "FlextTargetOracleTestModels": ["tests.models", "FlextTargetOracleTestModels"],
    "FlextTargetOracleTestProtocols": [
        "tests.protocols",
        "FlextTargetOracleTestProtocols",
    ],
    "FlextTargetOracleTestTypes": ["tests.typings", "FlextTargetOracleTestTypes"],
    "FlextTargetOracleTestUtilities": [
        "tests.utilities",
        "FlextTargetOracleTestUtilities",
    ],
    "ORACLE_CONTAINER_NAME": ["tests.conftest", "ORACLE_CONTAINER_NAME"],
    "ORACLE_HOST": ["tests.conftest", "ORACLE_HOST"],
    "ORACLE_IMAGE": ["tests.conftest", "ORACLE_IMAGE"],
    "ORACLE_PASSWORD": ["tests.conftest", "ORACLE_PASSWORD"],
    "ORACLE_PORT": ["tests.conftest", "ORACLE_PORT"],
    "ORACLE_SERVICE": ["tests.conftest", "ORACLE_SERVICE"],
    "ORACLE_USER": ["tests.conftest", "ORACLE_USER"],
    "TEST_SCHEMA": ["tests.conftest", "TEST_SCHEMA"],
    "TestOracleIntegration": ["tests.integration.test_oracle", "TestOracleIntegration"],
    "TestOracleSettings": ["tests.unit.test_config", "TestOracleSettings"],
    "TestOracleTarget": ["tests.unit.test_target", "TestOracleTarget"],
    "TestOracleTargetE2E": ["tests.integration.test_oracle", "TestOracleTargetE2E"],
    "TestPerformance": ["tests.performance.test_performance", "TestPerformance"],
    "TestSingerWorkflowE2E": ["tests.e2e.test_singer", "TestSingerWorkflowE2E"],
    "batch_records": ["tests.conftest", "batch_records"],
    "c": ["tests.constants", "FlextTargetOracleTestConstants"],
    "clean_database": ["tests.conftest", "clean_database"],
    "conftest": ["tests.conftest", ""],
    "connected_loader": ["tests.conftest", "connected_loader"],
    "constants": ["tests.constants", ""],
    "d": ["flext_tests", "d"],
    "docker_control": ["tests.conftest", "docker_control"],
    "e": ["flext_tests", "e"],
    "e2e": ["tests.e2e", ""],
    "event_loop": ["tests.conftest", "event_loop"],
    "h": ["flext_tests", "h"],
    "integration": ["tests.integration", ""],
    "large_dataset": ["tests.conftest", "large_dataset"],
    "loader_config": ["tests.unit.test_loader", "loader_config"],
    "logger": ["tests.conftest", "logger"],
    "m": ["tests.models", "FlextTargetOracleTestModels"],
    "mock_loader": ["tests.conftest", "mock_loader"],
    "mock_oracle_api": ["tests.conftest", "mock_oracle_api"],
    "models": ["tests.models", ""],
    "nested_schema": ["tests.conftest", "nested_schema"],
    "oracle_api": ["tests.conftest", "oracle_api"],
    "oracle_config": ["tests.conftest", "oracle_config"],
    "oracle_engine": ["tests.conftest", "oracle_engine"],
    "oracle_loader": ["tests.conftest", "oracle_loader"],
    "oracle_target": ["tests.conftest", "oracle_target"],
    "p": ["tests.protocols", "FlextTargetOracleTestProtocols"],
    "performance": ["tests.performance", ""],
    "protocols": ["tests.protocols", ""],
    "pytest_collection_modifyitems": [
        "tests.conftest",
        "pytest_collection_modifyitems",
    ],
    "pytest_configure": ["tests.conftest", "pytest_configure"],
    "r": ["flext_tests", "r"],
    "record": ["tests.conftest", "record"],
    "reset_settings_singleton": ["tests.conftest", "reset_settings_singleton"],
    "s": ["flext_tests", "s"],
    "sample_config": ["tests.conftest", "sample_config"],
    "sample_record": ["tests.conftest", "sample_record"],
    "sample_target": ["tests.conftest", "sample_target"],
    "schema": ["tests.conftest", "schema"],
    "shared_oracle_container": ["tests.conftest", "shared_oracle_container"],
    "simple_schema": ["tests.conftest", "simple_schema"],
    "singer_messages": ["tests.conftest", "singer_messages"],
    "state": ["tests.conftest", "state"],
    "state_message": ["tests.conftest", "state_message"],
    "t": ["tests.typings", "FlextTargetOracleTestTypes"],
    "target": ["tests.unit.test_target", "target"],
    "temp_config_file": ["tests.conftest", "temp_config_file"],
    "temporary_env_vars": ["tests.conftest", "temporary_env_vars"],
    "test_cli_dispatcher": ["tests.unit.test_cli_dispatcher", ""],
    "test_cli_service_falls_back_to_bus_when_flag_disabled": [
        "tests.unit.test_cli_dispatcher",
        "test_cli_service_falls_back_to_bus_when_flag_disabled",
    ],
    "test_cli_service_uses_dispatcher_when_flag_enabled": [
        "tests.unit.test_cli_dispatcher",
        "test_cli_service_uses_dispatcher_when_flag_enabled",
    ],
    "test_config": ["tests.unit.test_config", ""],
    "test_ensure_table_exists_returns_result": [
        "tests.unit.test_loader",
        "test_ensure_table_exists_returns_result",
    ],
    "test_load_record_buffers_and_finalize": [
        "tests.unit.test_loader",
        "test_load_record_buffers_and_finalize",
    ],
    "test_loader": ["tests.unit.test_loader", ""],
    "test_loader_execute_returns_ready_payload": [
        "tests.unit.test_loader",
        "test_loader_execute_returns_ready_payload",
    ],
    "test_oracle": ["tests.integration.test_oracle", ""],
    "test_performance": ["tests.performance.test_performance", ""],
    "test_singer": ["tests.e2e.test_singer", ""],
    "test_target": ["tests.unit.test_target", ""],
    "typings": ["tests.typings", ""],
    "u": ["tests.utilities", "FlextTargetOracleTestUtilities"],
    "unit": ["tests.unit", ""],
    "utilities": ["tests.utilities", ""],
    "x": ["flext_tests", "x"],
}

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
    "test_cli_dispatcher",
    "test_cli_service_falls_back_to_bus_when_flag_disabled",
    "test_cli_service_uses_dispatcher_when_flag_enabled",
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


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
