# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests.unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import c, d, e, h, m, p, r, s, t, td, tf, tk, tm, tv, u, x

    from .test_config import TestsFlextTargetOracleConfig
    from .test_loader import TestsFlextTargetOracleLoader, loader_config
    from .test_module_governance import TestsFlextTargetOracleModuleGovernance
    from .test_target import TestsFlextTargetOracleTarget, target
__all__: tuple[str, ...] = (
    "TestsFlextTargetOracleConfig",
    "TestsFlextTargetOracleLoader",
    "TestsFlextTargetOracleModuleGovernance",
    "TestsFlextTargetOracleTarget",
    "c",
    "d",
    "e",
    "h",
    "loader_config",
    "m",
    "p",
    "r",
    "s",
    "t",
    "target",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".test_config": ("TestsFlextTargetOracleConfig",),
            ".test_loader": ("TestsFlextTargetOracleLoader", "loader_config"),
            ".test_module_governance": ("TestsFlextTargetOracleModuleGovernance",),
            ".test_target": ("TestsFlextTargetOracleTarget", "target"),
            "flext_tests": (
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
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
