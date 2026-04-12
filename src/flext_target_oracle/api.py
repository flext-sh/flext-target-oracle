"""FLEXT service orchestrator for target-oracle.

Thin facade — all infrastructure from ``FlextMeltanoTargetServiceBase`` via MRO.
Oracle sink creation requires FlextTargetOracleLoader integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Never, override

from flext_meltano import FlextMeltanoTargetServiceBase
from flext_target_oracle import t


class FlextTargetOracleService(FlextMeltanoTargetServiceBase):
    """Orchestrator for target-oracle. Loader-based, not Singer sink."""

    target_name: t.NonEmptyStr = "target-oracle"

    @override
    def create_sink(
        self,
        stream_name: str,
        schema: t.FlatContainerMapping,
    ) -> Never:
        """Not supported — use FlextTargetOracleLoader directly."""
        msg = "target-oracle uses Loader pattern, not Singer sink"
        raise TypeError(msg)


target_oracle = FlextTargetOracleService

__all__: list[str] = ["FlextTargetOracleService", "target_oracle"]
