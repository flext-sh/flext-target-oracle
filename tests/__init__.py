# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_db_oracle import e
    from flext_tests import api, td, tf, tk, tm

    from flext_target_oracle import d, h, r, x
    from tests import e2e, integration, performance, unit
    from tests.base import TestsFlextTargetOracleServiceBase, s
    from tests.constants import TestsFlextTargetOracleConstants, c
    from tests.models import TestsFlextTargetOracleModels, m
    from tests.protocols import TestsFlextTargetOracleProtocols, p
    from tests.settings import TestsFlextTargetOracleSettings
    from tests.typings import TestsFlextTargetOracleTypes, t
    from tests.utilities import TestsFlextTargetOracleUtilities, u


__all__: tuple[str, ...] = (
    "TestsFlextTargetOracleConstants",
    "TestsFlextTargetOracleModels",
    "TestsFlextTargetOracleProtocols",
    "TestsFlextTargetOracleServiceBase",
    "TestsFlextTargetOracleSettings",
    "TestsFlextTargetOracleTypes",
    "TestsFlextTargetOracleUtilities",
    "api",
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
            "flext_db_oracle": ("e",),
            "flext_target_oracle": ("d", "h", "r", "x"),
            "flext_tests": ("api", "td", "tf", "tk", "tm"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
