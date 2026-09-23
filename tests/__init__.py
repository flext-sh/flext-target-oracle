# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_db_oracle import db_oracle, e
    from flext_meltano import meltano
    from flext_tests import (
        api,
        cli,
        core,
        d,
        h,
        install_local_packages,
        lazy_attribute,
        load_infra_report,
        r,
        services,
        td,
        tf,
        tk,
        tm,
        tv,
        x,
    )

    from flext_target_oracle import config, main, settings, target_oracle

    from . import e2e, integration, performance, unit
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
    "TestsFlextTargetOracleConstants",
    "TestsFlextTargetOracleModels",
    "TestsFlextTargetOracleProtocols",
    "TestsFlextTargetOracleServiceBase",
    "TestsFlextTargetOracleSettings",
    "TestsFlextTargetOracleTypes",
    "TestsFlextTargetOracleUtilities",
    "api",
    "c",
    "cli",
    "config",
    "core",
    "d",
    "db_oracle",
    "e",
    "e2e",
    "h",
    "install_local_packages",
    "integration",
    "lazy_attribute",
    "load_infra_report",
    "m",
    "main",
    "meltano",
    "p",
    "performance",
    "r",
    "s",
    "services",
    "settings",
    "t",
    "target_oracle",
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
            "flext_db_oracle": ("db_oracle", "e"),
            "flext_meltano": ("meltano",),
            "flext_target_oracle": ("config", "main", "settings", "target_oracle"),
            "flext_tests": (
                "api",
                "cli",
                "core",
                "d",
                "h",
                "install_local_packages",
                "lazy_attribute",
                "load_infra_report",
                "r",
                "services",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
                "x",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
