# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
<<<<<<< HEAD
    from flext_cli import cli
    from flext_db_oracle import db_oracle, e
    from flext_meltano import meltano, s
    from pydantic_core import from_json, to_json, to_jsonable_python
=======
    from flext_db_oracle import e, s

    from flext_core import d, h, r, x
    from flext_target_oracle import FlextTargetOracleConstants
>>>>>>> origin/0.12.0-dev

    from flext_core import (
        core,
        d,
        h,
        lazy,
        lazy_attribute,
        normalize_lazy_imports,
        r,
        x,
    )
    from flext_target_oracle import c, config, m, main, p, settings, t, target_oracle, u

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
    "cli",
    "config",
    "core",
    "d",
    "db_oracle",
    "e",
    "from_json",
    "h",
    "lazy",
    "lazy_attribute",
    "m",
    "main",
    "meltano",
    "normalize_lazy_imports",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "target_oracle",
    "to_json",
    "to_jsonable_python",
    "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
<<<<<<< HEAD
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
=======
            ".constants": ("ExamplesFlextTargetOracleConstants", "c"),
            ".models": ("ExamplesFlextTargetOracleModels", "m"),
            ".protocols": ("ExamplesFlextTargetOracleProtocols", "p"),
            ".typings": ("ExamplesFlextTargetOracleTypes", "t"),
            ".utilities": ("ExamplesFlextTargetOracleUtilities", "u"),
            "flext_core": ("d", "h", "r", "x"),
            "flext_db_oracle": ("e", "s"),
            "flext_target_oracle": ("FlextTargetOracleConstants",),
>>>>>>> origin/0.12.0-dev
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
