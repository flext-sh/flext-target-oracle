# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from . import e2e as e2e
    from . import integration as integration
    from . import performance as performance
    from . import unit as unit
    from flext_target_oracle import FlextTargetOracleConstants
    from flext_tests import FlextTestsConstants, d, e, h, r, td, tf, tk, tm, tv, x
    from typing import Final

    from .base import (
        TestsFlextTargetOracleServiceBase,
        TestsFlextTargetOracleServiceBase as s,
    )
    from .constants import (
        TestsFlextTargetOracleConstants,
        TestsFlextTargetOracleConstants as c,
    )
    from .models import TestsFlextTargetOracleModels, TestsFlextTargetOracleModels as m
    from .protocols import (
        TestsFlextTargetOracleProtocols,
        TestsFlextTargetOracleProtocols as p,
    )
    from .settings import TestsFlextTargetOracleSettings
    from .typings import TestsFlextTargetOracleTypes, TestsFlextTargetOracleTypes as t
    from .utilities import (
        TestsFlextTargetOracleUtilities,
        TestsFlextTargetOracleUtilities as u,
    )
__all__: tuple[str, ...] = (
    "Final",
    "FlextTargetOracleConstants",
    "FlextTestsConstants",
    "TestsFlextTargetOracleConstants",
    "TestsFlextTargetOracleModels",
    "TestsFlextTargetOracleProtocols",
    "TestsFlextTargetOracleServiceBase",
    "TestsFlextTargetOracleSettings",
    "TestsFlextTargetOracleTypes",
    "TestsFlextTargetOracleUtilities",
    "c",
    "d",
    "e",
    "e2e",
    "h",
    "integration",
    "m",
    "p",
    "performance",
    "r",
    "s",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "unit",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("TestsFlextTargetOracleServiceBase", "s"),
            ".constants": ("TestsFlextTargetOracleConstants", "c"),
            ".e2e": ("e2e",),
            ".integration": ("integration",),
            ".models": ("TestsFlextTargetOracleModels", "m"),
            ".performance": ("performance",),
            ".protocols": ("TestsFlextTargetOracleProtocols", "p"),
            ".settings": ("TestsFlextTargetOracleSettings",),
            ".typings": ("TestsFlextTargetOracleTypes", "t"),
            ".unit": ("unit",),
            ".utilities": ("TestsFlextTargetOracleUtilities", "u"),
            "flext_target_oracle": ("FlextTargetOracleConstants",),
            "flext_tests": (
                "FlextTestsConstants",
                "d",
                "e",
                "h",
                "r",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
                "x",
            ),
            "typing": ("Final",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
