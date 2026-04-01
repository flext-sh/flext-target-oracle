# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from tests.unit.test_cli_dispatcher import *
    from tests.unit.test_config import *
    from tests.unit.test_loader import *
    from tests.unit.test_target import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "TestOracleSettings": "tests.unit.test_config",
    "TestOracleTarget": "tests.unit.test_target",
    "loader_config": "tests.unit.test_loader",
    "target": "tests.unit.test_target",
    "test_cli_dispatcher": "tests.unit.test_cli_dispatcher",
    "test_cli_service_falls_back_to_bus_when_flag_disabled": "tests.unit.test_cli_dispatcher",
    "test_cli_service_uses_dispatcher_when_flag_enabled": "tests.unit.test_cli_dispatcher",
    "test_config": "tests.unit.test_config",
    "test_ensure_table_exists_returns_result": "tests.unit.test_loader",
    "test_load_record_buffers_and_finalize": "tests.unit.test_loader",
    "test_loader": "tests.unit.test_loader",
    "test_loader_execute_returns_ready_payload": "tests.unit.test_loader",
    "test_target": "tests.unit.test_target",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
