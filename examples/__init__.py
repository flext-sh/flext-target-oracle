# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if _t.TYPE_CHECKING:
    from flext_target_oracle import c, m, p, t, u
_LAZY_IMPORTS = build_lazy_import_map(
    {
        "flext_target_oracle": (
            "c",
            "m",
            "p",
            "t",
            "u",
        ),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "c",
    "m",
    "p",
    "t",
    "u",
]
