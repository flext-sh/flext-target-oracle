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
from flext_db_oracle import FlextDbOracleConstants


def _env_enabled(flag_name: str, default: str = "1") -> bool:
    """Helper function to check if environment flag is enabled."""
    value = os.environ.get(flag_name, default)
    return value.lower() not in {"0", "false", "no"}


class FlextTargetOracleConstants(FlextConstants):
    """Target Oracle constants extending FlextConstants.

    Composes with FlextDbOracleConstants to avoid duplication and ensure consistency.
    """

    # Import Oracle database-specific constants from flext-db-oracle (composition pattern)
    from flext_db_oracle.constants import FlextDbOracleConstants

    class Connection:
        """Connection-related constants for Oracle target."""

        DEFAULT_PORT: Final[int] = FlextDbOracleConstants.Network.DEFAULT_PORT
        MIN_PORT: Final[int] = FlextDbOracleConstants.Network.MIN_PORT
        MAX_PORT: Final[int] = FlextDbOracleConstants.Network.MAX_PORT
        DEFAULT_CONNECTION_TIMEOUT: Final[int] = (
            FlextDbOracleConstants.Connection.DEFAULT_CONNECTION_TIMEOUT
        )

        # Oracle-specific connection settings
        DEFAULT_HOST: Final[str] = FlextDbOracleConstants.Defaults.DEFAULT_HOST
        DEFAULT_SERVICE_NAME: Final[str] = (
            FlextDbOracleConstants.Defaults.DEFAULT_SERVICE_NAME
        )
        DEFAULT_USERNAME: Final[str] = FlextDbOracleConstants.Defaults.DEFAULT_USERNAME

    class Processing:
        """Processing-related constants for Oracle target."""

        DEFAULT_BATCH_SIZE: Final[int] = (
            FlextDbOracleConstants.Defaults.DEFAULT_BATCH_SIZE
        )
        DEFAULT_COMMIT_SIZE: Final[int] = (
            FlextDbOracleConstants.Performance.DEFAULT_COMMIT_SIZE
        )
        DEFAULT_QUERY_TIMEOUT: Final[int] = (
            FlextDbOracleConstants.Defaults.DEFAULT_QUERY_TIMEOUT
        )

        DEFAULT_MAX_PARALLEL_STREAMS: Final[int] = (
            4  # Singer-specific parallel streams setting
        )

    class Loading:
        """Target-specific loading configuration."""

        DEFAULT_POOL_MIN: Final[int] = (
            FlextDbOracleConstants.Connection.DEFAULT_POOL_MIN
        )
        DEFAULT_POOL_MAX: Final[int] = (
            FlextDbOracleConstants.Connection.DEFAULT_POOL_MAX
        )
        DEFAULT_POOL_TIMEOUT: Final[int] = (
            FlextDbOracleConstants.Connection.DEFAULT_POOL_TIMEOUT
        )

    class Validation:
        """Target-specific validation configuration."""

        MAX_TABLE_NAME_LENGTH: Final[int] = (
            FlextDbOracleConstants.Validation.MAX_TABLE_NAME_LENGTH
        )
        MAX_COLUMN_NAME_LENGTH: Final[int] = (
            FlextDbOracleConstants.Validation.MAX_COLUMN_NAME_LENGTH
        )
        MAX_IDENTIFIER_LENGTH: Final[int] = (
            FlextDbOracleConstants.Validation.MAX_IDENTIFIER_LENGTH
        )

    class FeatureFlags:
        """Feature toggles for progressive dispatcher rollout."""

        ENABLE_DISPATCHER: ClassVar[bool] = _env_enabled(
            "FLEXT_TARGET_ORACLE_ENABLE_DISPATCHER",
        )


__all__ = [
    "FlextTargetOracleConstants",
]
