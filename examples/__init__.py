# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_cli import cli
    from flext_db_oracle import db_oracle, e
    from flext_meltano import meltano, s
    from pydantic_core import from_json, to_json, to_jsonable_python

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
            ".constants": ("ExamplesFlextTargetOracleConstants",),
            ".models": ("ExamplesFlextTargetOracleModels",),
            ".protocols": ("ExamplesFlextTargetOracleProtocols",),
            ".typings": ("ExamplesFlextTargetOracleTypes",),
            ".utilities": ("ExamplesFlextTargetOracleUtilities",),
            "flext_cli": ("cli",),
            "flext_core": (
                "core",
                "d",
                "h",
                "lazy",
                "lazy_attribute",
                "normalize_lazy_imports",
                "r",
                "x",
            ),
            "flext_db_oracle": ("db_oracle", "e"),
            "flext_meltano": ("meltano", "s"),
            "flext_target_oracle": (
                "c",
                "config",
                "m",
                "main",
                "p",
                "settings",
                "t",
                "target_oracle",
                "u",
            ),
            "pydantic_core": ("from_json", "to_json", "to_jsonable_python"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
