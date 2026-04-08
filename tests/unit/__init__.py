# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import tests.unit.test_config as _tests_unit_test_config

    test_config = _tests_unit_test_config
    import tests.unit.test_loader as _tests_unit_test_loader
    from tests.unit.test_config import TestOracleSettings

    test_loader = _tests_unit_test_loader
    import tests.unit.test_target as _tests_unit_test_target
    from tests.unit.test_loader import (
        loader_config,
        test_ensure_table_exists_returns_result,
        test_flush_batch_uses_db_oracle_owned_sql_builders,
        test_load_record_buffers_and_finalize,
        test_loader_execute_returns_ready_payload,
    )

    test_target = _tests_unit_test_target
    from flext_core.constants import FlextConstants as c
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.models import FlextModels as m
    from flext_core.protocols import FlextProtocols as p
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_core.typings import FlextTypes as t
    from flext_core.utilities import FlextUtilities as u
    from tests.unit.test_target import TestOracleTarget, target
_LAZY_IMPORTS = {
    "TestOracleSettings": ("tests.unit.test_config", "TestOracleSettings"),
    "TestOracleTarget": ("tests.unit.test_target", "TestOracleTarget"),
    "c": ("flext_core.constants", "FlextConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "loader_config": ("tests.unit.test_loader", "loader_config"),
    "m": ("flext_core.models", "FlextModels"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("flext_core.typings", "FlextTypes"),
    "target": ("tests.unit.test_target", "target"),
    "test_config": "tests.unit.test_config",
    "test_ensure_table_exists_returns_result": (
        "tests.unit.test_loader",
        "test_ensure_table_exists_returns_result",
    ),
    "test_flush_batch_uses_db_oracle_owned_sql_builders": (
        "tests.unit.test_loader",
        "test_flush_batch_uses_db_oracle_owned_sql_builders",
    ),
    "test_load_record_buffers_and_finalize": (
        "tests.unit.test_loader",
        "test_load_record_buffers_and_finalize",
    ),
    "test_loader": "tests.unit.test_loader",
    "test_loader_execute_returns_ready_payload": (
        "tests.unit.test_loader",
        "test_loader_execute_returns_ready_payload",
    ),
    "test_target": "tests.unit.test_target",
    "u": ("flext_core.utilities", "FlextUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
    "TestOracleSettings",
    "TestOracleTarget",
    "c",
    "d",
    "e",
    "h",
    "loader_config",
    "m",
    "p",
    "r",
    "s",
    "t",
    "target",
    "test_config",
    "test_ensure_table_exists_returns_result",
    "test_flush_batch_uses_db_oracle_owned_sql_builders",
    "test_load_record_buffers_and_finalize",
    "test_loader",
    "test_loader_execute_returns_ready_payload",
    "test_target",
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
