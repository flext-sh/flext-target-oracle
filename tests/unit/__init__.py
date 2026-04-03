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
    from tests.unit import test_config, test_loader, test_target
    from tests.unit.test_config import TestOracleSettings
    from tests.unit.test_loader import (
        loader_config,
        test_ensure_table_exists_returns_result,
        test_load_record_buffers_and_finalize,
        test_loader_execute_returns_ready_payload,
    )
    from tests.unit.test_target import TestOracleTarget, target

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "TestOracleSettings": "tests.unit.test_config",
    "TestOracleTarget": "tests.unit.test_target",
    "c": ("flext_core.constants", "FlextConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "loader_config": "tests.unit.test_loader",
    "m": ("flext_core.models", "FlextModels"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("flext_core.typings", "FlextTypes"),
    "target": "tests.unit.test_target",
    "test_config": "tests.unit.test_config",
    "test_ensure_table_exists_returns_result": "tests.unit.test_loader",
    "test_load_record_buffers_and_finalize": "tests.unit.test_loader",
    "test_loader": "tests.unit.test_loader",
    "test_loader_execute_returns_ready_payload": "tests.unit.test_loader",
    "test_target": "tests.unit.test_target",
    "u": ("flext_core.utilities", "FlextUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
