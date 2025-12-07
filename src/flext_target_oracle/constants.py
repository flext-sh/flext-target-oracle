"""Constants for FLEXT Target Oracle module.

This module defines centralized constants following the FlextConstants pattern
from flext-core, extending it with Oracle target-specific constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import os
from typing import ClassVar, Final

from flext_core import FlextConstants

# No longer importing from flext_db_oracle


def _env_enabled(flag_name: str, default: str = "1") -> bool:
    """Helper function to check if environment flag is enabled."""
    value = os.environ.get(flag_name, default)
    return value.lower() not in {"0", "false", "no"}


class FlextTargetOracleConstants(FlextConstants):
    """Target Oracle constants extending FlextConstants.

    Composes with 1000 to avoid duplication and ensure consistency.
    """

    class Connection:
        """Connection-related constants for Oracle target."""

        DEFAULT_PORT: Final[int] = 1521
        MIN_PORT: Final[int] = 1024
        MAX_PORT: Final[int] = 65535
        DEFAULT_CONNECTION_TIMEOUT: Final[int] = 30

        # Oracle-specific connection settings
        DEFAULT_HOST: Final[str] = "localhost"
        DEFAULT_SERVICE_NAME: Final[str] = "XE"
        DEFAULT_USERNAME: Final[str] = "system"

    class TargetOracleProcessing:
        """Processing-related constants for Oracle target.

        Note: Does not override parent Processing class to avoid inheritance conflicts.
        """

        DEFAULT_BATCH_SIZE: Final[int] = 1000
        DEFAULT_COMMIT_SIZE: Final[int] = 1000
        DEFAULT_QUERY_TIMEOUT: Final[int] = 30

        DEFAULT_MAX_PARALLEL_STREAMS: Final[int] = (
            4  # Singer-specific parallel streams setting
        )

    class Loading:
        """Target-specific loading configuration."""

        DEFAULT_POOL_MIN: Final[int] = 5
        DEFAULT_POOL_MAX: Final[int] = 20
        DEFAULT_POOL_TIMEOUT: Final[int] = 30

    class TargetOracleValidation:
        """Target-specific validation configuration.

        Note: Does not override parent Validation class to avoid inheritance conflicts.
        """

        MAX_TABLE_NAME_LENGTH: Final[int] = 30
        MAX_COLUMN_NAME_LENGTH: Final[int] = 30
        MAX_IDENTIFIER_LENGTH: Final[int] = 30

    class FeatureFlags:
        """Feature toggles for progressive dispatcher rollout."""

        ENABLE_DISPATCHER: ClassVar[bool] = _env_enabled(
            "FLEXT_TARGET_ORACLE_ENABLE_DISPATCHER",
        )

    class Observability:
        """Observability and monitoring constants."""

        # Security audit constants
        DATABASE_LOGIN: Final[str] = "database_login"
        FAILURE: Final[str] = "failure"

        # Performance monitoring thresholds
        SLOW_QUERY_THRESHOLD_SECONDS: Final[float] = (
            30.0  # 30 second threshold for slow queries
        )
        HIGH_UTILIZATION_THRESHOLD: Final[float] = (
            0.8  # 80% threshold for high resource utilization
        )


c = FlextTargetOracleConstants

__all__ = [
    "FlextTargetOracleConstants",
    "c",
]
