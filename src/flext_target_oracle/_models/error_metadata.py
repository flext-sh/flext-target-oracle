"""Error metadata model for flext-target-oracle.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_meltano import m

from flext_target_oracle import t


class FlextTargetOracleModelsErrorMetadata:
    """Error metadata namespace composed into ``m.TargetOracle``."""

    class ErrorMetadata(m.ArbitraryTypesModel):
        """Structured metadata attached to Oracle target error responses."""

        code: Annotated[str, m.Field(description="Canonical error code")]
        context: Annotated[
            t.JsonMapping | None,
            m.Field(description="Structured error context"),
        ] = None
        correlation_id: Annotated[
            str | None,
            m.Field(description="Cross-service correlation identifier"),
        ] = None


__all__: list[str] = ["FlextTargetOracleModelsErrorMetadata"]
