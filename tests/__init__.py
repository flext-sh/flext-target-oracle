# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

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

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "TestsFlextTargetOracleConstants": ".constants",
        "TestsFlextTargetOracleModels": ".models",
        "TestsFlextTargetOracleProtocols": ".protocols",
        "TestsFlextTargetOracleServiceBase": ".base",
        "TestsFlextTargetOracleSettings": ".settings",
        "TestsFlextTargetOracleTypes": ".typings",
        "TestsFlextTargetOracleUtilities": ".utilities",
        "api": "flext_tests",
        "c": ".constants",
        "d": "flext_target_oracle",
        "e": "flext_db_oracle",
        "e2e": ".e2e",
        "h": "flext_target_oracle",
        "integration": ".integration",
        "m": ".models",
        "p": ".protocols",
        "performance": ".performance",
        "r": "flext_target_oracle",
        "s": ".base",
        "t": ".typings",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "unit": ".unit",
        "x": "flext_target_oracle",
    }),
    public_exports=__all__,
)
