# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if _t.TYPE_CHECKING:
    from flext_tests import td, tf, tk, tm, tv

    from flext_target_oracle import d, e, h, r, s, x
    from tests.constants import TestsFlextTargetOracleConstants, c
    from tests.e2e.test_singer import TestSingerWorkflowE2E
    from tests.integration.test_oracle import TestOracleIntegration, TestOracleTargetE2E
    from tests.models import TestsFlextTargetOracleModels, m
    from tests.performance.test_performance import TestPerformance
    from tests.protocols import TestsFlextTargetOracleProtocols, p
    from tests.typings import TestsFlextTargetOracleTypes, t
    from tests.unit.test_config import TestOracleSettings
    from tests.unit.test_target import TestOracleTarget
    from tests.utilities import TestsFlextTargetOracleUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    (
        ".e2e",
        ".integration",
        ".performance",
        ".unit",
    ),
    build_lazy_import_map(
        {
            ".constants": (
                "TestsFlextTargetOracleConstants",
                "c",
            ),
            ".e2e.test_singer": ("TestSingerWorkflowE2E",),
            ".integration.test_oracle": (
                "TestOracleIntegration",
                "TestOracleTargetE2E",
            ),
            ".models": (
                "TestsFlextTargetOracleModels",
                "m",
            ),
            ".performance.test_performance": ("TestPerformance",),
            ".protocols": (
                "TestsFlextTargetOracleProtocols",
                "p",
            ),
            ".typings": (
                "TestsFlextTargetOracleTypes",
                "t",
            ),
            ".unit.test_config": ("TestOracleSettings",),
            ".unit.test_target": ("TestOracleTarget",),
            ".utilities": (
                "TestsFlextTargetOracleUtilities",
                "u",
            ),
            "flext_target_oracle": (
                "d",
                "e",
                "h",
                "r",
                "s",
                "x",
            ),
            "flext_tests": (
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
            ),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "TestOracleIntegration",
    "TestOracleSettings",
    "TestOracleTarget",
    "TestOracleTargetE2E",
    "TestPerformance",
    "TestSingerWorkflowE2E",
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
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "x",
]
