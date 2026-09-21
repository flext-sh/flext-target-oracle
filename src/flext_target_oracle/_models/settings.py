"""Configuration models for Oracle target."""

from __future__ import annotations

from typing import Annotated, Self

from flext_core import FlextSettings
from flext_meltano import m, t, u


class FlextTargetOracleModelsSettings(FlextSettings):
    """Configuration MRO mixin for TargetOracle namespace.

    MRO carries ``FlextSettings`` (ENFORCE-042); the class is a namespace
    holder, never instantiated — nested namespaces resolve via the MRO.
    """

    # ENFORCE-042 namespace-holder contract: ``FlextSettings`` contributes
    # namespacing only — instance machinery stays plain object semantics so the
    # settings singleton/validation machinery cannot leak into instantiated
    # facade composites (e.g. the ``u`` logging facade).
    def __new__(cls, *args: object, **kwargs: object) -> Self:
        return object.__new__(cls)

    def __init__(self, *args: object, **kwargs: object) -> None:
        _ = self, args, kwargs

    def __setattr__(self, name: str, value: object) -> None:
        object.__setattr__(self, name, value)

    __eq__ = object.__eq__

    __hash__ = object.__hash__

    class OracleConnectionConfig(m.ArbitraryTypesModel):
        """Oracle connection configuration payload."""

        host: str = u.Field(
            ..., description="Oracle database host", validate_default=True
        )
        port: t.PortNumber = u.Field(
            ..., description="Oracle database port", validate_default=True
        )
        service_name: str = u.Field(
            ..., description="Oracle service name", validate_default=True
        )
        username: str = u.Field(
            ..., description="Oracle database username", validate_default=True
        )
        password: str = u.Field(
            ..., description="Oracle database password", validate_default=True
        )
        timeout: t.PositiveInt = u.Field(
            default=30,
            description="Connection timeout in seconds",
            validate_default=True,
        )
        pool_min: t.PositiveInt = u.Field(
            default=2,
            description="Oracle connection pool minimum",
            validate_default=True,
        )
        pool_max: t.PositiveInt = u.Field(
            default=20,
            description="Oracle connection pool maximum",
            validate_default=True,
        )
        pool_increment: t.PositiveInt = u.Field(
            default=1,
            description="Oracle connection pool increment",
            validate_default=True,
        )
        encoding: str = u.Field(
            default="UTF-8",
            description="Oracle connection encoding",
            validate_default=True,
        )
        ssl_enabled: bool = u.Field(
            default=False, description="Whether SSL is enabled", validate_default=True
        )
        autocommit: bool = u.Field(
            default=False,
            description="Whether autocommit is enabled",
            validate_default=True,
        )
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

        default_target_schema: str = u.Field(
            ..., description="Default Oracle target schema", validate_default=True
        )
        use_bulk_operations: bool = u.Field(
            ..., description="Whether bulk loading is enabled", validate_default=True
        )
        batch_size: t.BatchSize = u.Field(
            ..., description="Target batch size", validate_default=True
        )
        table_prefix: str = u.Field(
            ..., description="Target table name prefix", validate_default=True
        )
        table_suffix: str = u.Field(
            ..., description="Target table name suffix", validate_default=True
        )
