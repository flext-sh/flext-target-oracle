# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Oracle package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports
from flext_target_oracle.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if TYPE_CHECKING:
    from flext_db_oracle import d, e, h, r, s, x

    from ._config import FlextTargetOracleConfig, config
    from ._settings import FlextTargetOracleSettings, settings
    from .api import FlextTargetOracleService, target_oracle
    from .cli import FlextTargetOracleCli, main
    from .constants import FlextTargetOracleConstants, FlextTargetOracleConstants as c
    from .models import FlextTargetOracleModels, FlextTargetOracleModels as m
    from .protocols import FlextTargetOracleProtocols, FlextTargetOracleProtocols as p
    from .typings import FlextTargetOracleTypes, FlextTargetOracleTypes as t
    from .utilities import FlextTargetOracleUtilities, FlextTargetOracleUtilities as u

    _ = (
        c,
        FlextTargetOracleConstants,
        t,
        FlextTargetOracleTypes,
        p,
        FlextTargetOracleProtocols,
        m,
        FlextTargetOracleModels,
        u,
        FlextTargetOracleUtilities,
        d,
        e,
        h,
        r,
        s,
        x,
        main,
        FlextTargetOracleCli,
        FlextTargetOracleConfig,
        config,
        FlextTargetOracleSettings,
        settings,
        FlextTargetOracleService,
        target_oracle,
    )


_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "._config": ("FlextTargetOracleConfig", "config"),
    "._settings": ("FlextTargetOracleSettings", "settings"),
    ".api": ("FlextTargetOracleService", "target_oracle"),
    ".cli": ("FlextTargetOracleCli", "main"),
    ".constants": ("FlextTargetOracleConstants", "c"),
    ".models": ("FlextTargetOracleModels", "m"),
    ".protocols": ("FlextTargetOracleProtocols", "p"),
    ".typings": ("FlextTargetOracleTypes", "t"),
    ".utilities": ("FlextTargetOracleUtilities", "u"),
    "flext_db_oracle": ("d", "e", "h", "r", "s", "x"),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_DIRECT_IMPORTS: tuple[str, ...] = (
    "FlextTargetOracleCli",
    "FlextTargetOracleConfig",
    "FlextTargetOracleConstants",
    "FlextTargetOracleModels",
    "FlextTargetOracleProtocols",
    "FlextTargetOracleService",
    "FlextTargetOracleSettings",
    "FlextTargetOracleTypes",
    "FlextTargetOracleUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "build_lazy_import_map",
    "c",
    "config",
    "d",
    "e",
    "h",
    "install_lazy_exports",
    "m",
    "main",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "target_oracle",
    "u",
    "x",
)

__all__: tuple[str, ...] = (
    "FlextTargetOracleCli",
    "FlextTargetOracleConfig",
    "FlextTargetOracleConstants",
    "FlextTargetOracleModels",
    "FlextTargetOracleProtocols",
    "FlextTargetOracleService",
    "FlextTargetOracleSettings",
    "FlextTargetOracleTypes",
    "FlextTargetOracleUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "config",
    "d",
    "e",
    "h",
    "m",
    "main",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "target_oracle",
    "u",
    "x",
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
