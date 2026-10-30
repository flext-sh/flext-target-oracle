# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Oracle package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_db_oracle import db_oracle, e
    from flext_meltano import (
        build_lazy_import_map,
        cleanup_submodule_namespace,
        cli,
        core,
        d,
        h,
        install_lazy_exports,
        lazy,
        lazy_getattr,
        lazy_member,
        meltano,
        merge_lazy_imports,
        normalize_lazy_imports,
        r,
        resolve_lazy_members,
        s,
        x,
    )

    from flext_target_oracle.__version__ import (
        FlextTargetOracleVersion,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
    )
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
        FlextTargetOracleUtilities,
        u,
    )


__all__: tuple[str, ...] = (
    "FlextTargetOracle",
    "FlextTargetOracleCli",
    "FlextTargetOracleConfig",
    "FlextTargetOracleConstants",
    "FlextTargetOracleModels",
    "FlextTargetOracleProtocols",
    "FlextTargetOracleService",
    "FlextTargetOracleSettings",
    "FlextTargetOracleTypes",
    "FlextTargetOracleUtilities",
    "FlextTargetOracleVersion",
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
    "cleanup_submodule_namespace",
    "cli",
    "config",
    "core",
    "d",
    "db_oracle",
    "e",
    "h",
    "install_lazy_exports",
    "lazy",
    "lazy_getattr",
    "lazy_member",
    "m",
    "main",
    "meltano",
    "merge_lazy_imports",
    "normalize_lazy_imports",
    "p",
    "r",
    "resolve_lazy_members",
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
        "FlextTargetOracleModels": ".models",
        "FlextTargetOracleProtocols": ".protocols",
        "FlextTargetOracleService": ".api",
        "FlextTargetOracleSettings": "._settings",
        "FlextTargetOracleTypes": ".typings",
        "FlextTargetOracleUtilities": ".utilities",
        "FlextTargetOracleVersion": ".__version__",
        "__author__": ".__version__",
        "__author_email__": ".__version__",
        "__description__": ".__version__",
        "__license__": ".__version__",
        "__title__": ".__version__",
        "__url__": ".__version__",
        "__version_info__": ".__version__",
        "build_lazy_import_map": "flext_meltano",
        "c": ".constants",
        "cleanup_submodule_namespace": "flext_meltano",
        "cli": "flext_meltano",
        "config": "._config",
        "core": "flext_meltano",
        "d": "flext_meltano",
        "db_oracle": "flext_db_oracle",
        "e": "flext_db_oracle",
        "h": "flext_meltano",
        "install_lazy_exports": "flext_meltano",
        "lazy": "flext_meltano",
        "lazy_getattr": "flext_meltano",
        "lazy_member": "flext_meltano",
        "m": ".models",
        "main": ".cli",
        "meltano": "flext_meltano",
        "merge_lazy_imports": "flext_meltano",
        "normalize_lazy_imports": "flext_meltano",
        "p": ".protocols",
        "r": "flext_meltano",
        "resolve_lazy_members": "flext_meltano",
        "s": "flext_meltano",
        "settings": "._settings",
        "t": ".typings",
        "target_oracle": ".api",
        "u": ".utilities",
        "x": "flext_meltano",
    }),
    public_exports=__all__,
)

if not TYPE_CHECKING:
    from flext_target_oracle.__version__ import __version__
