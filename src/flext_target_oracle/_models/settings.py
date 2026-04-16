"""Configuration models for Oracle target."""

from __future__ import annotations

from typing import Annotated

from flext_meltano import FlextMeltanoModels
from flext_target_oracle import m, t


class FlextTargetOracleModelsSettings:
    """Configuration MRO mixin for TargetOracle namespace."""

    class OracleConnectionConfig(FlextMeltanoModels.ArbitraryTypesModel):
        """Oracle connection configuration payload."""

        host: str = m.Field(description="Oracle database host")
        port: t.PortNumber = m.Field(description="Oracle database port")
        service_name: str = m.Field(description="Oracle service name")
        username: str = m.Field(description="Oracle database username")
        password: str = m.Field(description="Oracle database password")
        timeout: t.PositiveInt = m.Field(description="Connection timeout in seconds")
        pool_min: t.PositiveInt = m.Field(description="Oracle connection pool minimum")
        pool_max: t.PositiveInt = m.Field(description="Oracle connection pool maximum")
        pool_increment: t.PositiveInt = m.Field(
            description="Oracle connection pool increment",
        )
        encoding: str = m.Field(description="Oracle connection encoding")
        ssl_enabled: bool = m.Field(description="Whether SSL is enabled")
        autocommit: bool = m.Field(description="Whether autocommit is enabled")
        use_bulk_operations: Annotated[
            bool,
            m.Field(
                description="Whether bulk operations are enabled",
            ),
        ] = False
        parallel_degree: Annotated[
            t.PositiveInt,
            m.Field(
                description="Oracle parallel execution degree",
            ),
        ] = 1

    class OracleConnectionModel(OracleConnectionConfig):
        """Oracle database connection configuration model."""

    class TargetConfig(FlextMeltanoModels.ArbitraryTypesModel):
        """Target runtime configuration payload."""

        default_target_schema: str = m.Field(description="Default Oracle target schema")
        use_bulk_operations: bool = m.Field(
            description="Whether bulk loading is enabled",
        )
        batch_size: t.BatchSize = m.Field(description="Target batch size")
        table_prefix: str = m.Field(description="Target table name prefix")
        table_suffix: str = m.Field(description="Target table name suffix")
