# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
<<<<<<< HEAD
    from flext_db_oracle import e
    from flext_meltano import s

    from flext_target_oracle import c, d, h, m, p, r, t, u, x
=======
    from flext_target_oracle import c, d, e, h, m, p, r, s, t, u, x
>>>>>>> recovery/rope-automation-20260921

    from .constants import ExamplesFlextTargetOracleConstants
    from .models import ExamplesFlextTargetOracleModels
    from .protocols import ExamplesFlextTargetOracleProtocols
    from .typings import ExamplesFlextTargetOracleTypes
    from .utilities import ExamplesFlextTargetOracleUtilities


__all__: tuple[str, ...] = (
    "ExamplesFlextTargetOracleConstants",
    "ExamplesFlextTargetOracleModels",
    "ExamplesFlextTargetOracleProtocols",
    "ExamplesFlextTargetOracleTypes",
    "ExamplesFlextTargetOracleUtilities",
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
            ".constants": ("ExamplesFlextTargetOracleConstants",),
            ".models": ("ExamplesFlextTargetOracleModels",),
            ".protocols": ("ExamplesFlextTargetOracleProtocols",),
            ".typings": ("ExamplesFlextTargetOracleTypes",),
            ".utilities": ("ExamplesFlextTargetOracleUtilities",),
<<<<<<< HEAD
            "flext_db_oracle": ("e",),
            "flext_meltano": ("s",),
            "flext_target_oracle": ("c", "d", "h", "m", "p", "r", "t", "u", "x"),
=======
            "flext_target_oracle": (
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
            ),
>>>>>>> recovery/rope-automation-20260921
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
