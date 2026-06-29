# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
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
            ".conftest": ("conftest",),
            ".constants": (
                "TestsFlextTargetOracleConstants",
                "c",
            ),
            ".e2e": ("e2e",),
            ".e2e.test_singer": ("TestsFlextTargetOracleSinger",),
            ".integration": ("integration",),
            ".integration.test_oracle": ("TestsFlextTargetOracleOracle",),
            ".models": (
                "TestsFlextTargetOracleModels",
                "m",
            ),
            ".performance": ("performance",),
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
            ".unit": ("unit",),
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
                "tm",
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


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
