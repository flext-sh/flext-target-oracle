"""Constants for FLEXT Target Oracle module.

This module defines centralized constants following the FlextConstants pattern
from flext-core, extending it with Oracle target-specific constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from enum import StrEnum, unique
from typing import Final

from flext_db_oracle import FlextDbOracleConstants
from flext_meltano import FlextMeltanoConstants


class FlextTargetOracleConstants(FlextMeltanoConstants, FlextDbOracleConstants):
    """Target Oracle constants extending FlextConstants."""

    @unique
    class LoadMethod(StrEnum):
        """Oracle data loading strategies."""

        INSERT = "INSERT"
        MERGE = "MERGE"
        BULK_INSERT = "BULK_INSERT"
        BULK_MERGE = "BULK_MERGE"

    @unique
    class StorageMode(StrEnum):
        """Data storage modes for Oracle target operations."""

        FLATTENED = "flattened"
        JSON = "json"
        HYBRID = "hybrid"

    class TargetOracle:
        """Connection-related constants for Oracle target."""

        @unique
        class CommandTypes(StrEnum):
            """Command type identifiers for Oracle target operations."""

            VALIDATE = "oracle_target_validate"
            LOAD = "oracle_target_load"
            ABOUT = "oracle_target_about"

        @unique
        class OutputFormats(StrEnum):
            """Output format options for command responses."""

            JSON = "json"
            TEXT = "text"

        DEFAULT_PORT: Final[int] = 1521
        MAX_PORT: Final[int] = 65535

        # Loading configuration (formerly separate Loading class)
        DEFAULT_POOL_MIN: Final[int] = 5
        DEFAULT_POOL_MAX: Final[int] = 20


c = FlextTargetOracleConstants
__all__ = ["FlextTargetOracleConstants", "c"]
