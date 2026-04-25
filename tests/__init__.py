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
    from tests.e2e.test_singer import TestsFlextTargetOracleSinger
    from tests.integration.test_oracle import TestsFlextTargetOracleOracle
    from tests.models import TestsFlextTargetOracleModels, m
    from tests.performance.test_performance import TestsFlextTargetOraclePerformance
    from tests.protocols import TestsFlextTargetOracleProtocols, p
    from tests.typings import TestsFlextTargetOracleTypes, t
    from tests.unit.test_config import TestsFlextTargetOracleConfig
    from tests.unit.test_loader import TestsFlextTargetOracleLoader
    from tests.unit.test_target import TestsFlextTargetOracleTarget
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
            ".e2e.test_singer": ("TestsFlextTargetOracleSinger",),
            ".integration.test_oracle": ("TestsFlextTargetOracleOracle",),
            ".models": (
                "TestsFlextTargetOracleModels",
                "m",
            ),
            ".performance.test_performance": ("TestsFlextTargetOraclePerformance",),
            ".protocols": (
                "TestsFlextTargetOracleProtocols",
                "p",
            ),
            ".typings": (
                "TestsFlextTargetOracleTypes",
                "t",
            ),
            ".unit.test_config": ("TestsFlextTargetOracleConfig",),
            ".unit.test_loader": ("TestsFlextTargetOracleLoader",),
            ".unit.test_target": ("TestsFlextTargetOracleTarget",),
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
        "pytest_addoption",
        "pytest_collect_file",
        "pytest_collection_modifyitems",
        "pytest_configure",
        "pytest_runtest_setup",
        "pytest_runtest_teardown",
        "pytest_sessionfinish",
        "pytest_sessionstart",
        "pytest_terminal_summary",
        "pytest_warning_recorded",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "TestsFlextTargetOracleConfig",
    "TestsFlextTargetOracleConstants",
    "TestsFlextTargetOracleLoader",
    "TestsFlextTargetOracleModels",
    "TestsFlextTargetOracleOracle",
    "TestsFlextTargetOraclePerformance",
    "TestsFlextTargetOracleProtocols",
    "TestsFlextTargetOracleSinger",
    "TestsFlextTargetOracleTarget",
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
