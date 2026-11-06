"""Configuration models for Oracle target.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_target_oracle/_models/settings
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_meltano import m

from flext_target_oracle import t


class FlextTargetOracleModelsSettings:
    """Configuration models for Oracle target."""

    class OracleConnectionConfig(m.ArbitraryTypesModel):
        """Oracle connection configuration payload."""

        host: Annotated[str, m.Field(description="Oracle database host")]
        port: Annotated[t.PortNumber, m.Field(description="Oracle database port")]
        service_name: Annotated[str, m.Field(description="Oracle service name")]
        username: Annotated[str, m.Field(description="Oracle database username")]
        password: Annotated[str, m.Field(description="Oracle database password")]
        timeout: Annotated[
            t.PositiveInt,
            m.Field(description="Connection timeout in seconds"),
        ] = 30
        pool_min: Annotated[
            t.PositiveInt,
            m.Field(description="Oracle connection pool minimum"),
        ] = 2
        pool_max: Annotated[
            t.PositiveInt,
            m.Field(description="Oracle connection pool maximum"),
        ] = 20
        pool_increment: Annotated[
            t.PositiveInt,
            m.Field(description="Oracle connection pool increment"),
        ] = 1
        encoding: Annotated[
            str,
            m.Field(description="Oracle connection encoding"),
        ] = "UTF-8"
        ssl_enabled: Annotated[
            bool,
            m.Field(description="Whether SSL is enabled"),
        ] = False
        autocommit: Annotated[
            bool,
            m.Field(description="Whether autocommit is enabled"),
        ] = False
        use_bulk_operations: Annotated[
            bool,
            m.Field(description="Whether bulk operations are enabled"),
        ] = False
        parallel_degree: Annotated[
            t.PositiveInt,
            m.Field(description="Oracle parallel execution degree"),
        ] = 1

    class OracleConnectionModel(OracleConnectionConfig):
        """Oracle database connection configuration model."""

    class TargetConfig(m.ArbitraryTypesModel):
        """Target runtime configuration payload."""

        default_target_schema: Annotated[
            str,
            m.Field(description="Default Oracle target schema"),
        ]
        use_bulk_operations: Annotated[
            bool,
            m.Field(description="Whether bulk loading is enabled"),
        ]
        batch_size: Annotated[t.BatchSize, m.Field(description="Target batch size")]
        table_prefix: Annotated[
            str,
            m.Field(description="Target table name prefix"),
        ]
        table_suffix: Annotated[
            str,
            m.Field(description="Target table name suffix"),
        ]


__all__: list[str] = ["FlextTargetOracleModelsSettings"]
