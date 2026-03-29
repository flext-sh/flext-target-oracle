"""Configuration models for Oracle target."""

from __future__ import annotations

from typing import Annotated, Protocol

from flext_core import r
from flext_meltano import FlextMeltanoModels
from pydantic import Field

from flext_target_oracle import t


class FlextTargetOracleModelsConfig:
    """Configuration MRO mixin for TargetOracle namespace."""

    class OracleSettingsProtocol(Protocol):
        """Protocol for Oracle settings used by command classes."""

        def validate_business_rules(self) -> r[bool]:
            """Validate Oracle target configuration business rules."""
            ...

    class OracleConnectionConfig(FlextMeltanoModels.ArbitraryTypesModel):
        """Oracle connection configuration payload."""

        host: Annotated[str, Field(description="Oracle database host")]
        port: Annotated[
            t.PortNumber,
            Field(description="Oracle database port"),
        ]
        service_name: Annotated[str, Field(description="Oracle service name")]
        username: Annotated[str, Field(description="Oracle database username")]
        password: Annotated[str, Field(description="Oracle database password")]
        timeout: Annotated[
            t.PositiveInt,
            Field(description="Connection timeout in seconds"),
        ]
        pool_min: Annotated[
            t.PositiveInt,
            Field(description="Oracle connection pool minimum"),
        ]
        pool_max: Annotated[
            t.PositiveInt,
            Field(description="Oracle connection pool maximum"),
        ]
        pool_increment: Annotated[
            t.PositiveInt,
            Field(
                description="Oracle connection pool increment",
            ),
        ]
        encoding: Annotated[str, Field(description="Oracle connection encoding")]
        ssl_enabled: Annotated[bool, Field(description="Whether SSL is enabled")]
        autocommit: Annotated[
            bool,
            Field(description="Whether autocommit is enabled"),
        ]
        use_bulk_operations: Annotated[
            bool,
            Field(
                default=False,
                description="Whether bulk operations are enabled",
            ),
        ]
        parallel_degree: Annotated[
            t.PositiveInt,
            Field(
                default=1,
                description="Oracle parallel execution degree",
            ),
        ]

    class OracleConnectionModel(OracleConnectionConfig):
        """Oracle database connection configuration model."""

    class TargetConfig(FlextMeltanoModels.ArbitraryTypesModel):
        """Target runtime configuration payload."""

        default_target_schema: Annotated[
            str,
            Field(
                description="Default Oracle target schema",
            ),
        ]
        use_bulk_operations: Annotated[
            bool,
            Field(
                description="Whether bulk loading is enabled",
            ),
        ]
        batch_size: Annotated[t.BatchSize, Field(description="Target batch size")]
        table_prefix: Annotated[str, Field(description="Target table name prefix")]
        table_suffix: Annotated[str, Field(description="Target table name suffix")]
