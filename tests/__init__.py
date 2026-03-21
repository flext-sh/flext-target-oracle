# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from . import (
        e2e as e2e,
        integration as integration,
        performance as performance,
        unit as unit,
    )
    from .conftest import (
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
    from .constants import (
        TestsFlextTargetOracleConstants,
        TestsFlextTargetOracleConstants as c,
    )
    from .e2e.test_singer import TestSingerWorkflowE2E
    from .integration.test_oracle import TestOracleIntegration, TestOracleTargetE2E
    from .models import TestsFlextTargetOracleModels, TestsFlextTargetOracleModels as m
    from .performance.test_performance import TestPerformance
    from .protocols import (
        TestsFlextTargetOracleProtocols,
        TestsFlextTargetOracleProtocols as p,
        _protocols,
    )
    from .typings import (
        TestsFlextTargetOracleTypes,
        TestsFlextTargetOracleTypes as t,
        _types,
    )
    from .unit.test_cli_dispatcher import (
        test_cli_service_falls_back_to_bus_when_flag_disabled,
        test_cli_service_uses_dispatcher_when_flag_enabled,
    )
    from .unit.test_config import TestOracleSettings
    from .unit.test_loader import (
        loader_config,
        test_ensure_table_exists_returns_result,
        test_load_record_buffers_and_finalize,
        test_loader_execute_returns_ready_payload,
    )
    from .unit.test_target import TestOracleTarget, target
    from .utilities import (
        TestsFlextTargetOracleUtilities,
        TestsFlextTargetOracleUtilities as u,
        _utilities,
    )

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "DOCKER_COMPOSE_PATH": ("tests.conftest", "DOCKER_COMPOSE_PATH"),
    "ORACLE_CONTAINER_NAME": ("tests.conftest", "ORACLE_CONTAINER_NAME"),
    "ORACLE_HOST": ("tests.conftest", "ORACLE_HOST"),
    "ORACLE_IMAGE": ("tests.conftest", "ORACLE_IMAGE"),
    "ORACLE_PASSWORD": ("tests.conftest", "ORACLE_PASSWORD"),
    "ORACLE_PORT": ("tests.conftest", "ORACLE_PORT"),
    "ORACLE_SERVICE": ("tests.conftest", "ORACLE_SERVICE"),
    "ORACLE_USER": ("tests.conftest", "ORACLE_USER"),
    "TEST_SCHEMA": ("tests.conftest", "TEST_SCHEMA"),
    "TestOracleIntegration": ("tests.integration.test_oracle", "TestOracleIntegration"),
    "TestOracleSettings": ("tests.unit.test_config", "TestOracleSettings"),
    "TestOracleTarget": ("tests.unit.test_target", "TestOracleTarget"),
    "TestOracleTargetE2E": ("tests.integration.test_oracle", "TestOracleTargetE2E"),
    "TestPerformance": ("tests.performance.test_performance", "TestPerformance"),
    "TestSingerWorkflowE2E": ("tests.e2e.test_singer", "TestSingerWorkflowE2E"),
    "TestsFlextTargetOracleConstants": ("tests.constants", "TestsFlextTargetOracleConstants"),
    "TestsFlextTargetOracleModels": ("tests.models", "TestsFlextTargetOracleModels"),
    "TestsFlextTargetOracleProtocols": ("tests.protocols", "TestsFlextTargetOracleProtocols"),
    "TestsFlextTargetOracleTypes": ("tests.typings", "TestsFlextTargetOracleTypes"),
    "TestsFlextTargetOracleUtilities": ("tests.utilities", "TestsFlextTargetOracleUtilities"),
    "_protocols": ("tests.protocols", "_protocols"),
    "_types": ("tests.typings", "_types"),
    "_utilities": ("tests.utilities", "_utilities"),
    "batch_records": ("tests.conftest", "batch_records"),
    "c": ("tests.constants", "TestsFlextTargetOracleConstants"),
    "clean_database": ("tests.conftest", "clean_database"),
    "connected_loader": ("tests.conftest", "connected_loader"),
    "docker_control": ("tests.conftest", "docker_control"),
    "e2e": ("tests.e2e", ""),
    "event_loop": ("tests.conftest", "event_loop"),
    "integration": ("tests.integration", ""),
    "large_dataset": ("tests.conftest", "large_dataset"),
    "loader_config": ("tests.unit.test_loader", "loader_config"),
    "logger": ("tests.conftest", "logger"),
    "m": ("tests.models", "TestsFlextTargetOracleModels"),
    "mock_loader": ("tests.conftest", "mock_loader"),
    "mock_oracle_api": ("tests.conftest", "mock_oracle_api"),
    "nested_schema": ("tests.conftest", "nested_schema"),
    "oracle_api": ("tests.conftest", "oracle_api"),
    "oracle_config": ("tests.conftest", "oracle_config"),
    "oracle_engine": ("tests.conftest", "oracle_engine"),
    "oracle_loader": ("tests.conftest", "oracle_loader"),
    "oracle_target": ("tests.conftest", "oracle_target"),
    "p": ("tests.protocols", "TestsFlextTargetOracleProtocols"),
    "performance": ("tests.performance", ""),
    "pytest_collection_modifyitems": ("tests.conftest", "pytest_collection_modifyitems"),
    "pytest_configure": ("tests.conftest", "pytest_configure"),
    "record": ("tests.conftest", "record"),
    "reset_settings_singleton": ("tests.conftest", "reset_settings_singleton"),
    "sample_config": ("tests.conftest", "sample_config"),
    "sample_record": ("tests.conftest", "sample_record"),
    "sample_target": ("tests.conftest", "sample_target"),
    "schema": ("tests.conftest", "schema"),
    "shared_oracle_container": ("tests.conftest", "shared_oracle_container"),
    "simple_schema": ("tests.conftest", "simple_schema"),
    "singer_messages": ("tests.conftest", "singer_messages"),
    "state": ("tests.conftest", "state"),
    "state_message": ("tests.conftest", "state_message"),
    "t": ("tests.typings", "TestsFlextTargetOracleTypes"),
    "target": ("tests.unit.test_target", "target"),
    "temp_config_file": ("tests.conftest", "temp_config_file"),
    "temporary_env_vars": ("tests.conftest", "temporary_env_vars"),
    "test_cli_service_falls_back_to_bus_when_flag_disabled": ("tests.unit.test_cli_dispatcher", "test_cli_service_falls_back_to_bus_when_flag_disabled"),
    "test_cli_service_uses_dispatcher_when_flag_enabled": ("tests.unit.test_cli_dispatcher", "test_cli_service_uses_dispatcher_when_flag_enabled"),
    "test_ensure_table_exists_returns_result": ("tests.unit.test_loader", "test_ensure_table_exists_returns_result"),
    "test_load_record_buffers_and_finalize": ("tests.unit.test_loader", "test_load_record_buffers_and_finalize"),
    "test_loader_execute_returns_ready_payload": ("tests.unit.test_loader", "test_loader_execute_returns_ready_payload"),
    "u": ("tests.utilities", "TestsFlextTargetOracleUtilities"),
    "unit": ("tests.unit", ""),
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
    "TestOracleIntegration",
    "TestOracleSettings",
    "TestOracleTarget",
    "TestOracleTargetE2E",
    "TestPerformance",
    "TestSingerWorkflowE2E",
    "TestsFlextTargetOracleConstants",
    "TestsFlextTargetOracleModels",
    "TestsFlextTargetOracleProtocols",
    "TestsFlextTargetOracleTypes",
    "TestsFlextTargetOracleUtilities",
    "_protocols",
    "_types",
    "_utilities",
    "batch_records",
    "c",
    "clean_database",
    "connected_loader",
    "docker_control",
    "e2e",
    "event_loop",
    "integration",
    "large_dataset",
    "loader_config",
    "logger",
    "m",
    "mock_loader",
    "mock_oracle_api",
    "nested_schema",
    "oracle_api",
    "oracle_config",
    "oracle_engine",
    "oracle_loader",
    "oracle_target",
    "p",
    "performance",
    "pytest_collection_modifyitems",
    "pytest_configure",
    "record",
    "reset_settings_singleton",
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
    "test_cli_service_falls_back_to_bus_when_flag_disabled",
    "test_cli_service_uses_dispatcher_when_flag_enabled",
    "test_ensure_table_exists_returns_result",
    "test_load_record_buffers_and_finalize",
    "test_loader_execute_returns_ready_payload",
    "u",
    "unit",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
