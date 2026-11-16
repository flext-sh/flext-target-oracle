"""Base constants for Target Oracle module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from flext_target_oracle import t


class FlextTargetOracleConstantsBase:
    """TargetOracle domain constants namespace."""

    # === Regex authority for the TargetOracle domain ===
    QUALIFIED_IDENTIFIER_PATTERN: ClassVar[str] = r"[A-Za-z_][A-Za-z0-9_$.]*"
    QUALIFIED_IDENTIFIER_RE: ClassVar[t.RegexPattern] = re.compile(
        QUALIFIED_IDENTIFIER_PATTERN,
    )

    # LoadMethods
    LOAD_METHOD_INSERT: ClassVar[str] = "INSERT"
    LOAD_METHOD_MERGE: ClassVar[str] = "MERGE"
    LOAD_METHOD_BULK_INSERT: ClassVar[str] = "BULK_INSERT"
    LOAD_METHOD_BULK_MERGE: ClassVar[str] = "BULK_MERGE"

    # StorageModes
    STORAGE_MODE_FLATTENED: ClassVar[str] = "flattened"
    STORAGE_MODE_JSON: ClassVar[str] = "json"
    STORAGE_MODE_HYBRID: ClassVar[str] = "hybrid"

    # CommandTypes
    COMMAND_TYPE_VALIDATE: ClassVar[str] = "oracle_target_validate"
    COMMAND_TYPE_LOAD: ClassVar[str] = "oracle_target_load"
    COMMAND_TYPE_ABOUT: ClassVar[str] = "oracle_target_about"

    # OutputFormats
    OUTPUT_FORMAT_TEXT: ClassVar[str] = "text"

    DEFAULT_PORT: ClassVar[int] = 1521
    MAX_PORT: ClassVar[int] = 65535

    # Loading configuration (formerly separate Loading class)
    DEFAULT_POOL_MIN: ClassVar[int] = 5
    DEFAULT_POOL_MAX: ClassVar[int] = 20


__all__: list[str] = ["FlextTargetOracleConstantsBase"]
