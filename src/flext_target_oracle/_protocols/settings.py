# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_target_oracle/_protocols/settings
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_meltano import FlextMeltanoProtocols

from flext_target_oracle import t


class FlextTargetOracleProtocolsSettings:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class OracleConnectionConfig(FlextMeltanoProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def host(self) -> str:
            """Oracle database host."""
            ...

        @property
        def port(self) -> t.PortNumber:
            """Oracle database port."""
            ...

        @property
        def service_name(self) -> str:
            """Oracle service name."""
            ...

        @property
        def username(self) -> str:
            """Oracle database username."""
            ...

        @property
        def password(self) -> str:
            """Oracle database password."""
            ...

        @property
        def timeout(self) -> t.PositiveInt:
            """Connection timeout in seconds."""
            ...

        @property
        def pool_min(self) -> t.PositiveInt:
            """Oracle connection pool minimum."""
            ...

        @property
        def pool_max(self) -> t.PositiveInt:
            """Oracle connection pool maximum."""
            ...

        @property
        def pool_increment(self) -> t.PositiveInt:
            """Oracle connection pool increment."""
            ...

        @property
        def encoding(self) -> str:
            """Oracle connection encoding."""
            ...

        @property
        def ssl_enabled(self) -> bool:
            """Whether SSL is enabled."""
            ...

        @property
        def autocommit(self) -> bool:
            """Whether autocommit is enabled."""
            ...

        @property
        def use_bulk_operations(self) -> bool:
            """Whether bulk operations are enabled."""
            ...

        @property
        def parallel_degree(self) -> t.PositiveInt:
            """Oracle parallel execution degree."""
            ...

    @runtime_checkable
    class OracleConnectionModel(FlextMeltanoProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def host(self) -> str:
            """Oracle database host."""
            ...

        @property
        def port(self) -> t.PortNumber:
            """Oracle database port."""
            ...

        @property
        def service_name(self) -> str:
            """Oracle service name."""
            ...

        @property
        def username(self) -> str:
            """Oracle database username."""
            ...

        @property
        def password(self) -> str:
            """Oracle database password."""
            ...

        @property
        def timeout(self) -> t.PositiveInt:
            """Connection timeout in seconds."""
            ...

        @property
        def pool_min(self) -> t.PositiveInt:
            """Oracle connection pool minimum."""
            ...

        @property
        def pool_max(self) -> t.PositiveInt:
            """Oracle connection pool maximum."""
            ...

        @property
        def pool_increment(self) -> t.PositiveInt:
            """Oracle connection pool increment."""
            ...

        @property
        def encoding(self) -> str:
            """Oracle connection encoding."""
            ...

        @property
        def ssl_enabled(self) -> bool:
            """Whether SSL is enabled."""
            ...

        @property
        def autocommit(self) -> bool:
            """Whether autocommit is enabled."""
            ...

        @property
        def use_bulk_operations(self) -> bool:
            """Whether bulk operations are enabled."""
            ...

        @property
        def parallel_degree(self) -> t.PositiveInt:
            """Oracle parallel execution degree."""
            ...

    @runtime_checkable
    class TargetConfig(FlextMeltanoProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def default_target_schema(self) -> str:
            """Default Oracle target schema."""
            ...

        @property
        def use_bulk_operations(self) -> bool:
            """Whether bulk loading is enabled."""
            ...

        @property
        def batch_size(self) -> t.BatchSize:
            """Target batch size."""
            ...

        @property
        def table_prefix(self) -> str:
            """Target table name prefix."""
            ...

        @property
        def table_suffix(self) -> str:
            """Target table name suffix."""
            ...


__all__: list[str] = [
    "FlextTargetOracleProtocolsSettings",
]
