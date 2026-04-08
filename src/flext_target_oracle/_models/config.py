"""Configuration models for Oracle target."""

from __future__ import annotations

from pydantic import Field

from flext_meltano import FlextMeltanoModels
from flext_target_oracle import t


class FlextTargetOracleModelsSettings:
    """Configuration MRO mixin for TargetOracle namespace."""

    class OracleConnectionConfig(FlextMeltanoModels.ArbitraryTypesModel):
        """Oracle connection configuration payload."""

        host: str = Field(description="Oracle database host")
        port: t.PortNumber = Field(description="Oracle database port")
        service_name: str = Field(description="Oracle service name")
        username: str = Field(description="Oracle database username")
        password: str = Field(description="Oracle database password")
        timeout: t.PositiveInt = Field(description="Connection timeout in seconds")
        pool_min: t.PositiveInt = Field(description="Oracle connection pool minimum")
        pool_max: t.PositiveInt = Field(description="Oracle connection pool maximum")
        pool_increment: t.PositiveInt = Field(
            description="Oracle connection pool increment",
        )
        encoding: str = Field(description="Oracle connection encoding")
        ssl_enabled: bool = Field(description="Whether SSL is enabled")
        autocommit: bool = Field(description="Whether autocommit is enabled")
        use_bulk_operations: bool = Field(
            default=False,
            description="Whether bulk operations are enabled",
        )
        parallel_degree: t.PositiveInt = Field(
            default=1,
            description="Oracle parallel execution degree",
        )

    class OracleConnectionModel(OracleConnectionConfig):
        """Oracle database connection configuration model."""

    class TargetConfig(FlextMeltanoModels.ArbitraryTypesModel):
        """Target runtime configuration payload."""

        default_target_schema: str = Field(description="Default Oracle target schema")
        use_bulk_operations: bool = Field(
            description="Whether bulk loading is enabled",
        )
        batch_size: t.BatchSize = Field(description="Target batch size")
        table_prefix: str = Field(description="Target table name prefix")
        table_suffix: str = Field(description="Target table name suffix")
