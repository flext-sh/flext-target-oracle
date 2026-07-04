"""Configuration models for Oracle target."""

from __future__ import annotations

from typing import Annotated

from flext_meltano import m, t, u


class FlextTargetOracleModelsSettings:
    """Configuration MRO mixin for TargetOracle namespace."""

    class OracleConnectionConfig(m.ArbitraryTypesModel):
        """Oracle connection configuration payload."""

        host: str = u.Field(..., description="Oracle database host", validate_default=True)
        port: t.PortNumber = u.Field(..., description="Oracle database port", validate_default=True)
        service_name: str = u.Field(..., description="Oracle service name", validate_default=True)
        username: str = u.Field(..., description="Oracle database username", validate_default=True)
        password: str = u.Field(..., description="Oracle database password", validate_default=True)
        timeout: t.PositiveInt = u.Field(..., description="Connection timeout in seconds", validate_default=True)
        pool_min: t.PositiveInt = u.Field(..., description="Oracle connection pool minimum", validate_default=True)
        pool_max: t.PositiveInt = u.Field(..., description="Oracle connection pool maximum", validate_default=True)
        pool_increment: t.PositiveInt = u.Field(
            ...,
            description="Oracle connection pool increment",
            validate_default=True,
        )
        encoding: str = u.Field(..., description="Oracle connection encoding", validate_default=True)
        ssl_enabled: bool = u.Field(..., description="Whether SSL is enabled", validate_default=True)
        autocommit: bool = u.Field(..., description="Whether autocommit is enabled", validate_default=True)
        use_bulk_operations: Annotated[
            bool,
            u.Field(
                ...,
                description="Whether bulk operations are enabled",
                validate_default=True,
            ),
        ] = False
        parallel_degree: Annotated[
            t.PositiveInt,
            u.Field(
                ...,
                description="Oracle parallel execution degree",
                validate_default=True,
            ),
        ] = 1

    class OracleConnectionModel(OracleConnectionConfig):
        """Oracle database connection configuration model."""

    class TargetConfig(m.ArbitraryTypesModel):
        """Target runtime configuration payload."""

        default_target_schema: str = u.Field(..., description="Default Oracle target schema", validate_default=True)
        use_bulk_operations: bool = u.Field(
            ...,
            description="Whether bulk loading is enabled",
            validate_default=True,
        )
        batch_size: t.BatchSize = u.Field(..., description="Target batch size", validate_default=True)
        table_prefix: str = u.Field(..., description="Target table name prefix", validate_default=True)
        table_suffix: str = u.Field(..., description="Target table name suffix", validate_default=True)
