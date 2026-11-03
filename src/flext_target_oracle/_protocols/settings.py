# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_target_oracle/_protocols/settings
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_meltano import FlextMeltanoProtocols

if TYPE_CHECKING:
    from flext_target_oracle import t


class FlextTargetOracleProtocolsSettings:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class OracleConnectionConfig(FlextMeltanoProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        host: str
        port: t.PortNumber
        service_name: str
        username: str
        password: str
        timeout: t.PositiveInt
        pool_min: t.PositiveInt
        pool_max: t.PositiveInt
        pool_increment: t.PositiveInt
        encoding: str
        ssl_enabled: bool
        autocommit: bool
        use_bulk_operations: bool
        parallel_degree: t.PositiveInt

    @runtime_checkable
    class OracleConnectionModel(OracleConnectionConfig, Protocol):
        """Structural data contract projected from the owning model."""

    @runtime_checkable
    class TargetConfig(FlextMeltanoProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        default_target_schema: str
        use_bulk_operations: bool
        batch_size: t.BatchSize
        table_prefix: str
        table_suffix: str


__all__: list[str] = [
    "FlextTargetOracleProtocolsSettings",
]
