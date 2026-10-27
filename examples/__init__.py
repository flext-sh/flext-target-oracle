# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_db_oracle import e
    from flext_meltano import s

    from flext_target_oracle import (
        build_lazy_import_map,
        c,
        cleanup_submodule_namespace,
        cli,
        config,
        core,
        d,
        db_oracle,
        h,
        install_lazy_exports,
        lazy,
        lazy_getattr,
        lazy_member,
        m,
        main,
        meltano,
        merge_lazy_imports,
        normalize_lazy_imports,
        p,
        r,
        resolve_lazy_members,
        settings,
        t,
        target_oracle,
        u,
        x,
    )


__all__: tuple[str, ...] = (
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
        "build_lazy_import_map": "flext_target_oracle",
        "c": "flext_target_oracle",
        "cleanup_submodule_namespace": "flext_target_oracle",
        "cli": "flext_target_oracle",
        "config": "flext_target_oracle",
        "core": "flext_target_oracle",
        "d": "flext_target_oracle",
        "db_oracle": "flext_target_oracle",
        "e": "flext_db_oracle",
        "h": "flext_target_oracle",
        "install_lazy_exports": "flext_target_oracle",
        "lazy": "flext_target_oracle",
        "lazy_getattr": "flext_target_oracle",
        "lazy_member": "flext_target_oracle",
        "m": "flext_target_oracle",
        "main": "flext_target_oracle",
        "meltano": "flext_target_oracle",
        "merge_lazy_imports": "flext_target_oracle",
        "normalize_lazy_imports": "flext_target_oracle",
        "p": "flext_target_oracle",
        "r": "flext_target_oracle",
        "resolve_lazy_members": "flext_target_oracle",
        "s": "flext_meltano",
        "settings": "flext_target_oracle",
        "t": "flext_target_oracle",
        "target_oracle": "flext_target_oracle",
        "u": "flext_target_oracle",
        "x": "flext_target_oracle",
    }),
    public_exports=__all__,
)
