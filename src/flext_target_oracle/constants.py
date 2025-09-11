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

        DEFAULT_PORT = FlextConstants.Infrastructure.DEFAULT_ORACLE_PORT
        MIN_PORT = FlextConstants.Platform.MIN_PORT_NUMBER
        MAX_PORT = FlextConstants.Platform.MAX_PORT_NUMBER
        DEFAULT_CONNECTION_TIMEOUT = FlextConstants.Defaults.TIMEOUT

    class Processing:
        """Processing-related constants for Oracle target."""

        DEFAULT_BATCH_SIZE = FlextConstants.Singer.DEFAULT_BATCH_SIZE
        DEFAULT_MAX_PARALLEL_STREAMS = (
            FlextConstants.Singer.DEFAULT_MAX_PARALLEL_STREAMS
        )


__all__ = [
    "FlextTargetOracleConstants",
]
