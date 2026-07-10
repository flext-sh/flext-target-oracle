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
    from flext_db_oracle import d as d, e as e, h as h, r as r, s as s, x as x
    from flext_target_oracle.api import (
        FlextTargetOracleService as FlextTargetOracleService,
        target_oracle as target_oracle,
    )
    from flext_target_oracle.cli import (
        FlextTargetOracleCli as FlextTargetOracleCli,
        main as main,
    )
    from flext_target_oracle.constants import (
        FlextTargetOracleConstants as FlextTargetOracleConstants,
        c as c,
    )
    from flext_target_oracle.models import (
        FlextTargetOracleModels as FlextTargetOracleModels,
        m as m,
    )
    from flext_target_oracle.protocols import (
        FlextTargetOracleProtocols as FlextTargetOracleProtocols,
        p as p,
    )
    from flext_target_oracle.typings import (
        FlextTargetOracleTypes as FlextTargetOracleTypes,
        t as t,
    )
    from flext_target_oracle.utilities import (
        FlextTargetOracle as FlextTargetOracle,
        FlextTargetOracleUtilities as FlextTargetOracleUtilities,
        u as u,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        "._settings": ("FlextTargetOracleSettings", "settings"),
        ".api": (
            "FlextTargetOracleService",
            "target_oracle",
        ),
        ".cli": (
            "FlextTargetOracleCli",
            "main",
        ),
        ".constants": (
            "FlextTargetOracleConstants",
            "c",
        ),
        ".models": (
            "FlextTargetOracleModels",
            "m",
        ),
        ".protocols": (
            "FlextTargetOracleProtocols",
            "p",
        ),
        ".typings": (
            "FlextTargetOracleTypes",
            "t",
        ),
        ".utilities": (
            "FlextTargetOracle",
            "FlextTargetOracleUtilities",
            "u",
        ),
        "flext_db_oracle": (
            "d",
            "e",
            "h",
            "r",
            "s",
            "x",
        ),
    },
)


__all__: tuple[str, ...] = (
    "FlextTargetOracle",
    "FlextTargetOracleCli",
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
    _LAZY_IMPORTS,
    public_exports=__all__,
)
