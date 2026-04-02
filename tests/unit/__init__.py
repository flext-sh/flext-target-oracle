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

    from tests.unit import test_config, test_loader, test_target
    from tests.unit.test_config import TestOracleSettings
    from tests.unit.test_loader import (
        loader_config,
        test_ensure_table_exists_returns_result,
        test_load_record_buffers_and_finalize,
        test_loader_execute_returns_ready_payload,
    )
    from tests.unit.test_target import TestOracleTarget, target

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "TestOracleSettings": "tests.unit.test_config",
    "TestOracleTarget": "tests.unit.test_target",
    "loader_config": "tests.unit.test_loader",
    "target": "tests.unit.test_target",
    "test_config": "tests.unit.test_config",
    "test_ensure_table_exists_returns_result": "tests.unit.test_loader",
    "test_load_record_buffers_and_finalize": "tests.unit.test_loader",
    "test_loader": "tests.unit.test_loader",
    "test_loader_execute_returns_ready_payload": "tests.unit.test_loader",
    "test_target": "tests.unit.test_target",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
