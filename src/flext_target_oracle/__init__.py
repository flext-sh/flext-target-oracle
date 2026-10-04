# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Oracle package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports
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
    from flext_db_oracle import e
    from flext_meltano import d, h, r, s, x

    from flext_target_oracle._config import FlextTargetOracleConfig, config
    from flext_target_oracle._settings import FlextTargetOracleSettings, settings
    from flext_target_oracle.api import FlextTargetOracleService, target_oracle
    from flext_target_oracle.cli import FlextTargetOracleCli, main
    from flext_target_oracle.constants import FlextTargetOracleConstants, c
    from flext_target_oracle.models import FlextTargetOracleModels, m
    from flext_target_oracle.protocols import FlextTargetOracleProtocols, p
    from flext_target_oracle.typings import FlextTargetOracleTypes, t
    from flext_target_oracle.utilities import (
        FlextTargetOracle,
        FlextTargetOracleExceptions,
        FlextTargetOracleLoader,
        FlextTargetOracleUtilities,
        u,
    )


__all__: tuple[str, ...] = (
    "FlextTargetOracle",
    "FlextTargetOracleCli",
    "FlextTargetOracleConfig",
    "FlextTargetOracleConstants",
    "FlextTargetOracleExceptions",
    "FlextTargetOracleLoader",
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
                "FlextTargetOracleLoader",
                "FlextTargetOracleUtilities",
                "u",
            ),
            "flext_db_oracle": ("e",),
            "flext_meltano": ("d", "h", "r", "s", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
