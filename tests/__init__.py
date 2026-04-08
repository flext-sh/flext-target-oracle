# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if _t.TYPE_CHECKING:
    from flext_core.decorators import d
    from flext_core.exceptions import e
    from flext_core.handlers import h
    from flext_core.mixins import x
    from flext_core.result import r
    from flext_core.service import s
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
        "flext_core.decorators": ("d",),
        "flext_core.exceptions": ("e",),
        "flext_core.handlers": ("h",),
        "flext_core.mixins": ("x",),
        "flext_core.result": ("r",),
        "flext_core.service": ("s",),
    },
    alias_groups={
        ".constants": (("c", "TestsFlextTargetOracleConstants"),),
        ".models": (("m", "TestsFlextTargetOracleModels"),),
        ".protocols": (("p", "TestsFlextTargetOracleProtocols"),),
        ".typings": (("t", "TestsFlextTargetOracleTypes"),),
        ".utilities": (("u", "TestsFlextTargetOracleUtilities"),),
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
