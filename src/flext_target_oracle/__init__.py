# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Oracle package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import __author__ as __author__
from .__version__ import __author_email__ as __author_email__
from .__version__ import __description__ as __description__
from .__version__ import __license__ as __license__
from .__version__ import __title__ as __title__
from .__version__ import __url__ as __url__
from .__version__ import __version__ as __version__
from .__version__ import __version_info__ as __version_info__

if TYPE_CHECKING:
    from flext_db_oracle import d as d
    from flext_db_oracle import e as e
    from flext_db_oracle import h as h
    from flext_db_oracle import r as r
    from flext_db_oracle import s as s
    from flext_db_oracle import x as x

    from ._config import FlextTargetOracleConfig as FlextTargetOracleConfig
    from ._config import config as config
    from ._settings import FlextTargetOracleSettings as FlextTargetOracleSettings
    from ._settings import settings as settings
    from .api import FlextTargetOracleService as FlextTargetOracleService
    from .api import target_oracle as target_oracle
    from .cli import FlextTargetOracleCli as FlextTargetOracleCli
    from .cli import main as main
    from .constants import FlextTargetOracleConstants as FlextTargetOracleConstants

    c: type[FlextTargetOracleConstants]
    from .models import (
        FlextTargetOracleModels as FlextTargetOracleModels,
        FlextTargetOracleModels as m,
    )
    from .protocols import FlextTargetOracleProtocols as FlextTargetOracleProtocols

    p: type[FlextTargetOracleProtocols]
    from .typings import FlextTargetOracleTypes as FlextTargetOracleTypes

    t: type[FlextTargetOracleTypes]
    from .utilities import FlextTargetOracle as FlextTargetOracle
    from .utilities import FlextTargetOracleUtilities as FlextTargetOracleUtilities

    u: type[FlextTargetOracleUtilities]

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "._config": ("FlextTargetOracleConfig", "config"),
    "._settings": ("FlextTargetOracleSettings", "settings"),
    ".api": ("FlextTargetOracleService", "target_oracle"),
    ".cli": ("FlextTargetOracleCli", "main"),
    ".constants": ("FlextTargetOracleConstants", "c"),
    ".models": ("FlextTargetOracleModels", "m"),
    ".protocols": ("FlextTargetOracleProtocols", "p"),
    ".typings": ("FlextTargetOracleTypes", "t"),
    ".utilities": ("FlextTargetOracle", "FlextTargetOracleUtilities", "u"),
    "flext_db_oracle": ("d", "e", "h", "r", "s", "x"),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
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

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
