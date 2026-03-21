# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes


if TYPE_CHECKING:
    from .test_cli_dispatcher import (
        test_cli_service_falls_back_to_bus_when_flag_disabled,
        test_cli_service_uses_dispatcher_when_flag_enabled,
    )
    from .test_config import TestOracleSettings
    from .test_loader import (
        loader_config,
        test_ensure_table_exists_returns_result,
        test_load_record_buffers_and_finalize,
        test_loader_execute_returns_ready_payload,
    )
    from .test_target import TestOracleTarget, target

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "TestOracleSettings": ("tests.unit.test_config", "TestOracleSettings"),
    "TestOracleTarget": ("tests.unit.test_target", "TestOracleTarget"),
    "loader_config": ("tests.unit.test_loader", "loader_config"),
    "target": ("tests.unit.test_target", "target"),
    "test_cli_service_falls_back_to_bus_when_flag_disabled": (
        "tests.unit.test_cli_dispatcher",
        "test_cli_service_falls_back_to_bus_when_flag_disabled",
    ),
    "test_cli_service_uses_dispatcher_when_flag_enabled": (
        "tests.unit.test_cli_dispatcher",
        "test_cli_service_uses_dispatcher_when_flag_enabled",
    ),
    "test_ensure_table_exists_returns_result": (
        "tests.unit.test_loader",
        "test_ensure_table_exists_returns_result",
    ),
    "test_load_record_buffers_and_finalize": (
        "tests.unit.test_loader",
        "test_load_record_buffers_and_finalize",
    ),
    "test_loader_execute_returns_ready_payload": (
        "tests.unit.test_loader",
        "test_loader_execute_returns_ready_payload",
    ),
}

__all__ = [
    "TestOracleSettings",
    "TestOracleTarget",
    "loader_config",
    "target",
    "test_cli_service_falls_back_to_bus_when_flag_disabled",
    "test_cli_service_uses_dispatcher_when_flag_enabled",
    "test_ensure_table_exists_returns_result",
    "test_load_record_buffers_and_finalize",
    "test_loader_execute_returns_ready_payload",
]


_LAZY_CACHE: dict[str, FlextTypes.ModuleExport] = {}


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


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
