"""Constants for FLEXT Target Oracle module.

This module defines centralized constants following the FlextConstants pattern
from flext-core, extending it with Oracle target-specific constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextConstants


class FlextTargetOracleConstants(FlextConstants):
    """Target Oracle constants extending flext-core.

    Provides a single source of truth for Target Oracle defaults while
    reusing platform-wide values from flext-core where applicable.
    """

    class Connection:
        """Connection-related constants for Oracle target."""

        DEFAULT_PORT = FlextConstants.Meltano.DEFAULT_ORACLE_PORT
        MIN_PORT = FlextConstants.Network.MIN_PORT
        MAX_PORT = FlextConstants.Network.MAX_PORT
        DEFAULT_CONNECTION_TIMEOUT = FlextConstants.Network.DEFAULT_TIMEOUT

    class Processing:
        """Processing-related constants for Oracle target."""

        DEFAULT_BATCH_SIZE = FlextConstants.Singer.DEFAULT_BATCH_SIZE
        DEFAULT_MAX_PARALLEL_STREAMS = (
            FlextConstants.Singer.DEFAULT_MAX_PARALLEL_STREAMS
        )


__all__ = [
    "FlextTargetOracleConstants",
]
