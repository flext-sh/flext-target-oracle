# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Oracle package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import (
    __author__ as __author__,
    __author_email__ as __author_email__,
    __description__ as __description__,
    __license__ as __license__,
    __title__ as __title__,
    __url__ as __url__,
    __version__ as __version__,
    __version_info__ as __version_info__,
)

if TYPE_CHECKING:
    from flext_db_oracle import FlextDbOracleConstants
    from flext_meltano import d, e, h, r, s, x

    from ._config import FlextTargetOracleConfig, config
    from ._settings import FlextTargetOracleSettings, settings
    from .api import FlextTargetOracleService, target_oracle
    from .cli import FlextTargetOracleCli, main
    from .constants import FlextTargetOracleConstants, FlextTargetOracleConstants as c
    from .models import FlextTargetOracleModels, FlextTargetOracleModels as m
    from .protocols import FlextTargetOracleProtocols, FlextTargetOracleProtocols as p
    from .typings import FlextTargetOracleTypes, FlextTargetOracleTypes as t
    from .utilities import (
        FlextTargetOracle,
        FlextTargetOracleExceptions,
        FlextTargetOracleUtilities,
        FlextTargetOracleUtilities as u,
    )
__all__: tuple[str, ...] = (
    "FlextDbOracleConstants",
    "FlextTargetOracle",
    "FlextTargetOracleCli",
    "FlextTargetOracleConfig",
    "FlextTargetOracleConstants",
    "FlextTargetOracleExceptions",
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

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._config": ("FlextTargetOracleConfig", "config"),
            "._settings": ("FlextTargetOracleSettings", "settings"),
            ".api": ("FlextTargetOracleService", "target_oracle"),
            ".cli": ("FlextTargetOracleCli", "main"),
            ".constants": ("FlextTargetOracleConstants", "c"),
            ".models": ("FlextTargetOracleModels", "m"),
            ".protocols": ("FlextTargetOracleProtocols", "p"),
            ".typings": ("FlextTargetOracleTypes", "t"),
            ".utilities": (
                "FlextTargetOracle",
                "FlextTargetOracleExceptions",
                "FlextTargetOracleUtilities",
                "u",
            ),
            "flext_db_oracle": ("FlextDbOracleConstants",),
            "flext_meltano": ("d", "e", "h", "r", "s", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
