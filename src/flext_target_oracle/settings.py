"""FLEXT Target Oracle Configuration - Enhanced FlextSettings Implementation.

Single unified configuration class for Oracle Singer target operations following
FLEXT 1.0.0 patterns with enhanced singleton, SecretStr, and Pydantic 2.11+ features.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Annotated, ClassVar

from flext_core import FlextSettingsBase, e, r
from flext_meltano import m, u
from flext_target_oracle import c, p, t
from flext_target_oracle._models.settings import FlextTargetOracleModelsSettings


class FlextTargetOracleSettings(FlextSettingsBase):
    """Runtime settings for Oracle Singer target operations."""

    model_config: ClassVar[m.SettingsConfigDict] = m.SettingsConfigDict(
        env_prefix="FLEXT_TARGET_ORACLE_", extra="ignore"
    )

    oracle_host: Annotated[
        str,
        u.Field(
            ...,
            description="Oracle database host",
            validate_default=True,
        ),
    ] = c.DbOracle.DEFAULT_HOST
    oracle_port: Annotated[
        int,
        u.Field(
            ...,
            description="Oracle database port",
            validate_default=True,
        ),
    ] = c.DbOracle.DEFAULT_PORT
    oracle_service_name: Annotated[
        str,
        u.Field(
            ...,
            description="Oracle service name or SID",
            validate_default=True,
        ),
    ] = c.DbOracle.DEFAULT_SERVICE_NAME
    oracle_user: Annotated[
        t.SecretStr,
        u.Field(
            ...,
            description="Oracle database username",
            validate_default=True,
        ),
    ] = u.Field(default_factory=lambda: t.SecretStr(""), validate_default=True)
    oracle_password: Annotated[
        t.SecretStr,
        u.Field(
            ...,
            description="Oracle database password",
            validate_default=True,
        ),
    ] = u.Field(default_factory=lambda: t.SecretStr(""), validate_default=True)
    default_target_schema: Annotated[
        str,
        u.Field(
            ...,
            description="Default target schema for data loading",
            validate_default=True,
        ),
    ] = "SINGER_DATA"
    batch_size: Annotated[
        int,
        u.Field(
            ...,
            ge=1,
            description="Batch size for data loading",
            validate_default=True,
        ),
    ] = 1000
    commit_interval: Annotated[
        int,
        u.Field(
            ...,
            ge=1,
            description="Commit interval for transactions",
            validate_default=True,
        ),
    ] = 1000
    transaction_timeout: Annotated[
        int,
        u.Field(
            ...,
            ge=1,
            description="Transaction timeout in seconds",
            validate_default=True,
        ),
    ] = 30
    parallel_degree: Annotated[
        int,
        u.Field(
            ...,
            ge=1,
            description="Oracle parallel execution degree",
            validate_default=True,
        ),
    ] = 1
    table_prefix: Annotated[
        str,
        u.Field(
            ..., description="Prefix applied to table names", validate_default=True
        ),
    ] = ""
    table_suffix: Annotated[
        str,
        u.Field(
            ..., description="Suffix applied to table names", validate_default=True
        ),
    ] = ""
    load_method: Annotated[
        str,
        u.Field(
            ...,
            description="Oracle loading strategy for record batches",
            validate_default=True,
        ),
    ] = c.TargetOracle.LOAD_METHOD_INSERT
    sdc_mode: Annotated[
        str,
        u.Field(
            ...,
            description="Singer upsert mode applied during loading",
            validate_default=True,
        ),
    ] = c.TargetOracle.LOAD_METHOD_INSERT.lower()
    storage_mode: Annotated[
        str,
        u.Field(
            ...,
            description="How record payloads are materialized into Oracle",
            validate_default=True,
        ),
    ] = c.TargetOracle.STORAGE_MODE_FLATTENED
    json_column_name: Annotated[
        str,
        u.Field(
            ...,
            description="Column name used to persist JSON payloads",
            validate_default=True,
        ),
    ] = "DATA"
    truncate_before_load: Annotated[
        bool,
        u.Field(
            ...,
            description="Truncate existing tables before reloading data",
            validate_default=True,
        ),
    ] = False
    column_ordering: Annotated[
        str,
        u.Field(
            ...,
            description="Column ordering strategy for generated DDL",
            validate_default=True,
        ),
    ] = ""
    column_order_rules: Annotated[
        dict[str, int],
        u.Field(
            ...,
            description="Priority rules applied to generated table columns",
            validate_default=True,
        ),
    ] = u.Field(default_factory=dict, validate_default=True)
    column_mappings: Annotated[
        dict[str, dict[str, str]],
        u.Field(
            ...,
            description="Per-stream Singer-to-Oracle column mappings",
            validate_default=True,
        ),
    ] = u.Field(default_factory=dict, validate_default=True)
    ignored_columns: Annotated[
        t.StrSequence,
        u.Field(
            ...,
            description="Columns ignored during schema and record handling",
            validate_default=True,
        ),
    ] = u.Field(default_factory=tuple, validate_default=True)
    custom_indexes: Annotated[
        dict[str, tuple[t.JsonMapping, ...]],
        u.Field(
            ...,
            description="Per-stream custom Oracle index definitions",
            validate_default=True,
        ),
    ] = u.Field(default_factory=dict, validate_default=True)
    use_bulk_operations: Annotated[
        bool,
        u.Field(
            ...,
            description="Use bulk operations for faster loading",
            validate_default=True,
        ),
    ] = True
    autocommit: Annotated[
        bool,
        u.Field(..., description="Auto-commit transactions", validate_default=True),
    ] = False

    def get_table_name(self, stream_name: str) -> str:
        """Get table name from stream name."""
        normalized_stream_name = stream_name.replace("-", "_").replace(".", "_")
        full_table_name = (
            f"{self.table_prefix}{normalized_stream_name}{self.table_suffix}"
        )
        return full_table_name.upper()

    def validate_business_rules(self) -> p.Result[bool]:
        """Validate Oracle target configuration business rules."""
        if not self.oracle_host:
            return e.fail_validation("oracle_host", error="is required")
        if not self.oracle_service_name:
            return e.fail_validation("oracle_service_name", error="is required")
        if not self.default_target_schema:
            return e.fail_validation("default_target_schema", error="is required")
        if self.commit_interval > self.batch_size:
            return e.fail_validation(
                "commit_interval",
                error="must be less than or equal to batch size",
            )
        return r[bool].ok(True)

    def get_oracle_config(
        self,
    ) -> FlextTargetOracleModelsSettings.OracleConnectionModel:
        """Get Oracle database connection configuration."""
        return FlextTargetOracleModelsSettings.OracleConnectionModel(
            host=self.oracle_host,
            port=self.oracle_port,
            service_name=self.oracle_service_name,
            username=self.oracle_user.get_secret_value(),
            password=self.oracle_password.get_secret_value(),
            timeout=self.transaction_timeout,
            pool_min=c.TargetOracle.DEFAULT_POOL_MIN,
            pool_max=c.TargetOracle.DEFAULT_POOL_MAX,
            pool_increment=1,
            encoding="UTF-8",
            ssl_enabled=False,
            autocommit=self.autocommit,
            use_bulk_operations=self.use_bulk_operations,
            parallel_degree=self.parallel_degree,
        )

    @staticmethod
    def validate_oracle_configuration(
        settings: FlextTargetOracleSettings,
    ) -> p.Result[bool]:
        """Validate Oracle configuration using FlextSettings patterns - ZERO DUPLICATION."""
        return settings.validate_business_rules()
