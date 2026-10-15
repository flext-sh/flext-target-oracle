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

    from flext_target_oracle import c, d, h, m, p, r, t, u, x


__all__: tuple[str, ...] = ("c", "d", "e", "h", "m", "p", "r", "s", "t", "u", "x")

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "c": "flext_target_oracle",
        "d": "flext_target_oracle",
        "e": "flext_db_oracle",
        "h": "flext_target_oracle",
        "m": "flext_target_oracle",
        "p": "flext_target_oracle",
        "r": "flext_target_oracle",
        "s": "flext_meltano",
        "t": "flext_target_oracle",
        "u": "flext_target_oracle",
        "x": "flext_target_oracle",
    }),
    public_exports=__all__,
)
