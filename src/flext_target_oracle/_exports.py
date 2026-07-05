"""Lazy and public root exports for :mod:`flext_target_oracle`."""

from __future__ import annotations

from flext_core.lazy import merge_lazy_imports
from flext_target_oracle._exports_lazy_part_01 import (
    FLEXT_TARGET_ORACLE_LAZY_IMPORTS_PART_01,
)

_LOCAL_LAZY_IMPORTS = {
    **FLEXT_TARGET_ORACLE_LAZY_IMPORTS_PART_01,
}

FLEXT_TARGET_ORACLE_LAZY_IMPORTS = merge_lazy_imports(
    (),
    _LOCAL_LAZY_IMPORTS,
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
    module_name="flext_target_oracle",
)

FLEXT_TARGET_ORACLE_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextTargetOracle",
    "FlextTargetOracleCli",
    "FlextTargetOracleConstants",
    "FlextTargetOracleModels",
    "FlextTargetOracleProtocols",
    "FlextTargetOracleService",
    "FlextTargetOracleSettings",
    "FlextTargetOracleTypes",
    "FlextTargetOracleUtilities",
    "target_oracle",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "d",
    "e",
    "h",
    "m",
    "main",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
)

__all__: list[str] = [
    "FLEXT_TARGET_ORACLE_LAZY_IMPORTS",
    "FLEXT_TARGET_ORACLE_PUBLIC_EXPORTS",
]
