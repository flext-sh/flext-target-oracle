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
    from flext_target_oracle import test_config, test_loader, test_target
    from flext_target_oracle.test_config import TestOracleSettings
    from flext_target_oracle.test_loader import (
        finalize_result,
        load_result,
        loader,
        loader_config,
        record,
        result,
        schema_message,
        test_ensure_table_exists_returns_result,
        test_load_record_buffers_and_finalize,
        validated,
    )
    from flext_target_oracle.test_target import target

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "TestOracleSettings": "flext_target_oracle.test_config",
    "c": ("flext_core.constants", "FlextConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "finalize_result": "flext_target_oracle.test_loader",
    "h": ("flext_core.handlers", "FlextHandlers"),
    "load_result": "flext_target_oracle.test_loader",
    "loader": "flext_target_oracle.test_loader",
    "loader_config": "flext_target_oracle.test_loader",
    "m": ("flext_core.models", "FlextModels"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "record": "flext_target_oracle.test_loader",
    "result": "flext_target_oracle.test_loader",
    "s": ("flext_core.service", "FlextService"),
    "schema_message": "flext_target_oracle.test_loader",
    "t": ("flext_core.typings", "FlextTypes"),
    "target": "flext_target_oracle.test_target",
    "test_config": "flext_target_oracle.test_config",
    "test_ensure_table_exists_returns_result": "flext_target_oracle.test_loader",
    "test_load_record_buffers_and_finalize": "flext_target_oracle.test_loader",
    "test_loader": "flext_target_oracle.test_loader",
    "test_target": "flext_target_oracle.test_target",
    "u": ("flext_core.utilities", "FlextUtilities"),
    "validated": "flext_target_oracle.test_loader",
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
