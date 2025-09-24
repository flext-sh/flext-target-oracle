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


def _env_enabled(flag_name: str, default: str = "1") -> bool:
    """Helper function to check if environment flag is enabled."""
    value = os.environ.get(flag_name, default)
    return value.lower() not in {"0", "false", "no"}


class FlextTargetOracleConstants(FlextConstants):
    """Target Oracle constants extending FlextConstants."""

    class Connection:
        """Connection-related constants for Oracle target."""

        DEFAULT_PORT: Final[int] = (
            1521  # From FlextMeltanoConstants.MeltanoSpecific.DEFAULT_ORACLE_PORT
        )
        MIN_PORT: Final[int] = FlextConstants.Network.MIN_PORT
        MAX_PORT: Final[int] = FlextConstants.Network.MAX_PORT
        DEFAULT_CONNECTION_TIMEOUT: Final[int] = FlextConstants.Network.DEFAULT_TIMEOUT

    class Processing:
        """Processing-related constants for Oracle target."""

        DEFAULT_BATCH_SIZE: Final[int] = (
            1000  # From FlextMeltanoConstants.Singer.DEFAULT_BATCH_SIZE
        )
        DEFAULT_MAX_PARALLEL_STREAMS: Final[int] = (
            4  # From FlextMeltanoConstants.Singer.DEFAULT_MAX_PARALLEL_STREAMS
        )

    class FeatureFlags:
        """Feature toggles for progressive dispatcher rollout."""

        ENABLE_DISPATCHER: ClassVar[bool] = _env_enabled(
            "FLEXT_TARGET_ORACLE_ENABLE_DISPATCHER",
        )


__all__ = [
    "FlextTargetOracleConstants",
]
