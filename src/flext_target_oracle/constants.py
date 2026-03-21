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
    """Target Oracle constants extending FlextConstants.

    Composes with 1000 to avoid duplication and ensure consistency.
    """

    @unique
    class LoadMethod(StrEnum):
        """Oracle data loading strategies with performance characteristics.

        Defines the available strategies for loading Singer data into Oracle
        tables, each optimized for different use cases and performance requirements.

        DRY Pattern:
            StrEnum is the single source of truth. Use LoadMethod.INSERT.value
            or LoadMethod.INSERT directly - no base strings needed.
        """

        INSERT = "INSERT"
        MERGE = "MERGE"
        BULK_INSERT = "BULK_INSERT"
        BULK_MERGE = "BULK_MERGE"

    @unique
    class StorageMode(StrEnum):
        """Data storage modes for Oracle target operations.

        Defines how Singer data should be stored in Oracle tables,
        with different approaches for handling nested JSON data.

        DRY Pattern:
            StrEnum is the single source of truth. Use StorageMode.FLATTENED.value
            or StorageMode.FLATTENED directly - no base strings needed.
        """

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
        MIN_PORT: Final[int] = 1024
        MAX_PORT: Final[int] = 65535
        DEFAULT_HOST: Final[str] = FlextDbOracleConstants.LOCALHOST
        DEFAULT_SERVICE_NAME: Final[str] = "XE"
        DEFAULT_USERNAME: Final[str] = "system"

    class TargetOracleProcessing:
        """Processing-related constants for Oracle target.

        Note: Does not override parent Processing class to avoid inheritance conflicts.
        """

        DEFAULT_BATCH_SIZE: Final[int] = FlextDbOracleConstants.DEFAULT_BATCH_SIZE
        DEFAULT_COMMIT_SIZE: Final[int] = FlextMeltanoConstants.DEFAULT_BATCH_SIZE

    class Loading:
        """Target-specific loading configuration."""

        DEFAULT_POOL_MIN: Final[int] = 5
        DEFAULT_POOL_MAX: Final[int] = 20

    class TargetOracleValidation:
        """Target-specific validation configuration.

        Note: Does not override parent Validation class to avoid inheritance conflicts.
        """

        MAX_IDENTIFIER_LENGTH: Final[int] = 30

    class FeatureFlags:
        """Feature toggles for progressive dispatcher rollout."""

        ENABLE_DISPATCHER: Final[bool] = False

    class Observability:
        """Observability and monitoring constants."""


c = FlextTargetOracleConstants
__all__ = ["FlextTargetOracleConstants", "c"]
