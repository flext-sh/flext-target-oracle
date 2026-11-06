# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_target_oracle/_protocols/singer
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Protocol, runtime_checkable

from flext_meltano import FlextMeltanoProtocols


class FlextTargetOracleProtocolsSinger:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class SingerStreamModel(FlextMeltanoProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        stream_name: str
        table_name: str
        ignored_columns: Sequence[str]
        column_mappings: Mapping[str, str]


__all__: list[str] = [
    "FlextTargetOracleProtocolsSinger",
]
