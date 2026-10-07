# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Oracle package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports
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
        FlextTargetOracleLoader,
        FlextTargetOracleUtilities,
        u,
    )


__all__: tuple[str, ...] = (
    "FlextTargetOracle",
    "FlextTargetOracleCli",
    "FlextTargetOracleConfig",
    "FlextTargetOracleConstants",
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

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTargetOracle": ".utilities",
        "FlextTargetOracleCli": ".cli",
        "FlextTargetOracleConfig": "._config",
        "FlextTargetOracleConstants": ".constants",
        "FlextTargetOracleLoader": ".utilities",
        "FlextTargetOracleModels": ".models",
        "FlextTargetOracleProtocols": ".protocols",
        "FlextTargetOracleService": ".api",
        "FlextTargetOracleSettings": "._settings",
        "FlextTargetOracleTypes": ".typings",
        "FlextTargetOracleUtilities": ".utilities",
        "c": ".constants",
        "config": "._config",
        "d": "flext_meltano",
        "e": "flext_db_oracle",
        "h": "flext_meltano",
        "m": ".models",
        "main": ".cli",
        "p": ".protocols",
        "r": "flext_meltano",
        "s": "flext_meltano",
        "settings": "._settings",
        "t": ".typings",
        "target_oracle": ".api",
        "u": ".utilities",
        "x": "flext_meltano",
    }),
    public_exports=__all__,
)
