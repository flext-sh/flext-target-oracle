# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_target_oracle import FlextTargetOracleConstants, d, e, h, r, s, x

    from .constants import (
        ExamplesFlextTargetOracleConstants,
        ExamplesFlextTargetOracleConstants as c,
    )
    from .models import (
        ExamplesFlextTargetOracleModels,
        ExamplesFlextTargetOracleModels as m,
    )
    from .protocols import (
        ExamplesFlextTargetOracleProtocols,
        ExamplesFlextTargetOracleProtocols as p,
    )
    from .typings import (
        ExamplesFlextTargetOracleTypes,
        ExamplesFlextTargetOracleTypes as t,
    )
    from .utilities import (
        ExamplesFlextTargetOracleUtilities,
        ExamplesFlextTargetOracleUtilities as u,
    )
__all__: tuple[str, ...] = (
    "ExamplesFlextTargetOracleConstants",
    "ExamplesFlextTargetOracleModels",
    "ExamplesFlextTargetOracleProtocols",
    "ExamplesFlextTargetOracleTypes",
    "ExamplesFlextTargetOracleUtilities",
    "FlextTargetOracleConstants",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".constants": ("ExamplesFlextTargetOracleConstants", "c"),
            ".models": ("ExamplesFlextTargetOracleModels", "m"),
            ".protocols": ("ExamplesFlextTargetOracleProtocols", "p"),
            ".typings": ("ExamplesFlextTargetOracleTypes", "t"),
            ".utilities": ("ExamplesFlextTargetOracleUtilities", "u"),
            "flext_target_oracle": (
                "FlextTargetOracleConstants",
                "d",
                "e",
                "h",
                "r",
                "s",
                "x",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
