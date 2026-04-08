# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if _t.TYPE_CHECKING:
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from tests.constants import (
        TestsFlextTargetOracleConstants,
        TestsFlextTargetOracleConstants as c,
    )
    from tests.models import (
        TestsFlextTargetOracleModels,
        TestsFlextTargetOracleModels as m,
    )
    from tests.protocols import (
        TestsFlextTargetOracleProtocols,
        TestsFlextTargetOracleProtocols as p,
    )
    from tests.typings import (
        TestsFlextTargetOracleTypes,
        TestsFlextTargetOracleTypes as t,
    )
    from tests.utilities import (
        TestsFlextTargetOracleUtilities,
        TestsFlextTargetOracleUtilities as u,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".constants": ("TestsFlextTargetOracleConstants",),
        ".models": ("TestsFlextTargetOracleModels",),
        ".protocols": ("TestsFlextTargetOracleProtocols",),
        ".typings": ("TestsFlextTargetOracleTypes",),
        ".utilities": ("TestsFlextTargetOracleUtilities",),
    },
    alias_groups={
        ".constants": (("c", "TestsFlextTargetOracleConstants"),),
        ".models": (("m", "TestsFlextTargetOracleModels"),),
        ".protocols": (("p", "TestsFlextTargetOracleProtocols"),),
        ".typings": (("t", "TestsFlextTargetOracleTypes"),),
        ".utilities": (("u", "TestsFlextTargetOracleUtilities"),),
        "flext_core.decorators": (("d", "FlextDecorators"),),
        "flext_core.exceptions": (("e", "FlextExceptions"),),
        "flext_core.handlers": (("h", "FlextHandlers"),),
        "flext_core.mixins": (("x", "FlextMixins"),),
        "flext_core.result": (("r", "FlextResult"),),
        "flext_core.service": (("s", "FlextService"),),
    },
)

__all__ = [
    "TestsFlextTargetOracleConstants",
    "TestsFlextTargetOracleModels",
    "TestsFlextTargetOracleProtocols",
    "TestsFlextTargetOracleTypes",
    "TestsFlextTargetOracleUtilities",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
