"""Configuration models for Oracle target."""

from __future__ import annotations

from typing import Annotated

from flext_meltano import m, t, u


class FlextTargetOracleModelsSettings:
    """Configuration MRO mixin for TargetOracle namespace."""

    class OracleConnectionConfig(m.ArbitraryTypesModel):
        """Oracle connection configuration payload."""

        host: str = u.Field(description="Oracle database host")
        port: t.PortNumber = u.Field(description="Oracle database port")
        service_name: str = u.Field(description="Oracle service name")
        username: str = u.Field(description="Oracle database username")
        password: str = u.Field(description="Oracle database password")
        timeout: t.PositiveInt = u.Field(description="Connection timeout in seconds")
        pool_min: t.PositiveInt = u.Field(description="Oracle connection pool minimum")
        pool_max: t.PositiveInt = u.Field(description="Oracle connection pool maximum")
        pool_increment: t.PositiveInt = u.Field(
            description="Oracle connection pool increment",
        )
        encoding: str = u.Field(description="Oracle connection encoding")
        ssl_enabled: bool = u.Field(description="Whether SSL is enabled")
        autocommit: bool = u.Field(description="Whether autocommit is enabled")
        use_bulk_operations: Annotated[
            bool,
            u.Field(
                description="Whether bulk operations are enabled",
            ),
        ] = False
        parallel_degree: Annotated[
            t.PositiveInt,
            u.Field(
                description="Oracle parallel execution degree",
            ),
        ] = 1

    class OracleConnectionModel(OracleConnectionConfig):
        """Oracle database connection configuration model."""

    class TargetConfig(m.ArbitraryTypesModel):
        """Target runtime configuration payload."""

        default_target_schema: str = u.Field(description="Default Oracle target schema")
        use_bulk_operations: bool = u.Field(
            description="Whether bulk loading is enabled",
        )
        batch_size: t.BatchSize = u.Field(description="Target batch size")
        table_prefix: str = u.Field(description="Target table name prefix")
        table_suffix: str = u.Field(description="Target table name suffix")
