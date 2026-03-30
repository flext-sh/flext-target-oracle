# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from tests.unit import (
        test_cli_dispatcher as test_cli_dispatcher,
        test_config as test_config,
        test_loader as test_loader,
        test_target as test_target,
    )
    from tests.unit.test_cli_dispatcher import (
        test_cli_service_falls_back_to_bus_when_flag_disabled as test_cli_service_falls_back_to_bus_when_flag_disabled,
        test_cli_service_uses_dispatcher_when_flag_enabled as test_cli_service_uses_dispatcher_when_flag_enabled,
    )
    from tests.unit.test_config import TestOracleSettings as TestOracleSettings
    from tests.unit.test_loader import (
        loader_config as loader_config,
        test_ensure_table_exists_returns_result as test_ensure_table_exists_returns_result,
        test_load_record_buffers_and_finalize as test_load_record_buffers_and_finalize,
        test_loader_execute_returns_ready_payload as test_loader_execute_returns_ready_payload,
    )
    from tests.unit.test_target import (
        TestOracleTarget as TestOracleTarget,
        target as target,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "TestOracleSettings": ["tests.unit.test_config", "TestOracleSettings"],
    "TestOracleTarget": ["tests.unit.test_target", "TestOracleTarget"],
    "loader_config": ["tests.unit.test_loader", "loader_config"],
    "target": ["tests.unit.test_target", "target"],
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
    "test_target": ["tests.unit.test_target", ""],
}

_EXPORTS: Sequence[str] = [
    "TestOracleSettings",
    "TestOracleTarget",
    "loader_config",
    "target",
    "test_cli_dispatcher",
    "test_cli_service_falls_back_to_bus_when_flag_disabled",
    "test_cli_service_uses_dispatcher_when_flag_enabled",
    "test_config",
    "test_ensure_table_exists_returns_result",
    "test_load_record_buffers_and_finalize",
    "test_loader",
    "test_loader_execute_returns_ready_payload",
    "test_target",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
