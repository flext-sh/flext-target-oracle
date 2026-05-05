"""Base constants for Target Oracle module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, ClassVar, Final

from flext_db_oracle import FlextDbOracleConstants
from flext_meltano import c

if TYPE_CHECKING:
    from flext_target_oracle import t


class FlextTargetOracleConstantsBase:
    """TargetOracle domain constants namespace."""

    # === Regex authority for the TargetOracle domain ===
    QUALIFIED_IDENTIFIER_PATTERN: Final[str] = r"[A-Za-z_][A-Za-z0-9_$.]*"
    QUALIFIED_IDENTIFIER_RE: ClassVar[t.RegexPattern] = re.compile(
        QUALIFIED_IDENTIFIER_PATTERN
    )

    # LoadMethods
    LOAD_METHOD_INSERT: Final[str] = "INSERT"
    LOAD_METHOD_MERGE: Final[str] = "MERGE"
    LOAD_METHOD_BULK_INSERT: Final[str] = "BULK_INSERT"
    LOAD_METHOD_BULK_MERGE: Final[str] = "BULK_MERGE"

    # StorageModes
    STORAGE_MODE_FLATTENED: Final[str] = "flattened"
    STORAGE_MODE_JSON: Final[str] = "json"
    STORAGE_MODE_HYBRID: Final[str] = "hybrid"

    # CommandTypes
    COMMAND_TYPE_VALIDATE: Final[str] = "oracle_target_validate"
    COMMAND_TYPE_LOAD: Final[str] = "oracle_target_load"
    COMMAND_TYPE_ABOUT: Final[str] = "oracle_target_about"

    # OutputFormats
    OUTPUT_FORMAT_TEXT: Final[str] = "text"

    DEFAULT_PORT: Final[int] = 1521
    MAX_PORT: Final[int] = 65535

    # Loading configuration (formerly separate Loading class)
    DEFAULT_POOL_MIN: Final[int] = 5
    DEFAULT_POOL_MAX: Final[int] = 20


class FlextTargetOracleConstants(c, FlextDbOracleConstants):
    """Oracle target constant facade."""

    class TargetOracle(FlextTargetOracleConstantsBase):
        """Oracle target constant namespace."""
