# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Oracle. Constants package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_oracle._constants.base import FlextTargetOracleConstantsBase


__all__: tuple[str, ...] = ("FlextTargetOracleConstantsBase",)

install_lazy_exports(
    __name__,
    globals(),
    {"FlextTargetOracleConstantsBase": ".base"},
    public_exports=__all__,
    deferred_members={
        "FlextTargetOracleConstantsBase": (
            "QUALIFIED_IDENTIFIER_PATTERN",
            "QUALIFIED_IDENTIFIER_RE",
            "LOAD_METHOD_INSERT",
            "LOAD_METHOD_MERGE",
            "LOAD_METHOD_BULK_INSERT",
            "LOAD_METHOD_BULK_MERGE",
            "STORAGE_MODE_FLATTENED",
            "STORAGE_MODE_JSON",
            "STORAGE_MODE_HYBRID",
            "COMMAND_TYPE_VALIDATE",
            "COMMAND_TYPE_LOAD",
            "COMMAND_TYPE_ABOUT",
            "OUTPUT_FORMAT_TEXT",
            "DEFAULT_PORT",
            "MAX_PORT",
            "DEFAULT_POOL_MIN",
            "DEFAULT_POOL_MAX",
        ),
    },
)
