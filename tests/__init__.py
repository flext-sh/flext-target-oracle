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
    from flext_tests import (
        d as d,
        e as e,
        h as h,
        r as r,
        td as td,
        tf as tf,
        tk as tk,
        tv as tv,
        x as x,
    )

    from tests.base import (
        TestsFlextTargetOracleServiceBase as TestsFlextTargetOracleServiceBase,
        s as s,
    )
    from tests.constants import (
        TestsFlextTargetOracleConstants as TestsFlextTargetOracleConstants,
        c as c,
    )
    from tests.e2e.test_singer import (
        TestsFlextTargetOracleSinger as TestsFlextTargetOracleSinger,
    )
    from tests.integration.test_oracle import (
        TestsFlextTargetOracleOracle as TestsFlextTargetOracleOracle,
    )
    from tests.models import (
        TestsFlextTargetOracleModels as TestsFlextTargetOracleModels,
        m as m,
    )
    from tests.performance.test_performance import (
        TestsFlextTargetOraclePerformance as TestsFlextTargetOraclePerformance,
    )
    from tests.protocols import (
        TestsFlextTargetOracleProtocols as TestsFlextTargetOracleProtocols,
        p as p,
    )
    from tests.settings import (
        TestsFlextTargetOracleSettings as TestsFlextTargetOracleSettings,
    )
    from tests.typings import (
        TestsFlextTargetOracleTypes as TestsFlextTargetOracleTypes,
        t as t,
    )
    from tests.unit.test_config import (
        TestsFlextTargetOracleConfig as TestsFlextTargetOracleConfig,
    )
    from tests.unit.test_loader import (
        TestsFlextTargetOracleLoader as TestsFlextTargetOracleLoader,
    )
    from tests.unit.test_module_governance import (
        TestsFlextTargetOracleModuleGovernance as TestsFlextTargetOracleModuleGovernance,
    )
    from tests.unit.test_target import (
        TestsFlextTargetOracleTarget as TestsFlextTargetOracleTarget,
    )
    from tests.utilities import (
        TestsFlextTargetOracleUtilities as TestsFlextTargetOracleUtilities,
        u as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (
        ".e2e",
        ".integration",
        ".performance",
        ".unit",
    ),
    build_lazy_import_map(
        {
            ".base": (
                "TestsFlextTargetOracleServiceBase",
                "s",
            ),
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
            ".settings": ("TestsFlextTargetOracleSettings",),
            ".typings": (
                "TestsFlextTargetOracleTypes",
                "t",
            ),
            ".unit.test_config": ("TestsFlextTargetOracleConfig",),
            ".unit.test_loader": ("TestsFlextTargetOracleLoader",),
            ".unit.test_module_governance": ("TestsFlextTargetOracleModuleGovernance",),
            ".unit.test_target": ("TestsFlextTargetOracleTarget",),
            ".utilities": (
                "TestsFlextTargetOracleUtilities",
                "u",
            ),
            "flext_tests": (
                "d",
                "e",
                "h",
                "r",
                "td",
                "tf",
                "tk",
                "tv",
                "x",
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
    "TestsFlextTargetOracleModuleGovernance",
    "TestsFlextTargetOracleOracle",
    "TestsFlextTargetOraclePerformance",
    "TestsFlextTargetOracleProtocols",
    "TestsFlextTargetOracleServiceBase",
    "TestsFlextTargetOracleSettings",
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
    "tv",
    "u",
    "x",
]
