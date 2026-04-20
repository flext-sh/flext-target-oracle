"""FLEXT Target Oracle Configuration - Enhanced FlextSettings Implementation.

Single unified configuration class for Oracle Singer target operations following
FLEXT 1.0.0 patterns with enhanced singleton, SecretStr, and Pydantic 2.11+ features.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Annotated, ClassVar

from flext_core import FlextSettings

from flext_target_oracle import FlextTargetOracleModelsSettings, c, m, p, r, t, u


@FlextSettings.auto_register("target-oracle")
class FlextTargetOracleSettings(FlextSettings):
    """Runtime settings for Oracle Singer target operations."""

    model_config: ClassVar[m.SettingsConfigDict] = m.SettingsConfigDict(
        env_prefix="FLEXT_TARGET_ORACLE_", extra="ignore"
    )

    oracle_host: Annotated[
        str,
        u.Field(
            description="Oracle database host",
        ),
    ] = c.DbOracle.OracleDefaults.DEFAULT_HOST
    oracle_port: Annotated[
        int,
        u.Field(
            description="Oracle database port",
        ),
    ] = c.DbOracle.Connection.DEFAULT_PORT
    oracle_service_name: Annotated[
        str,
        u.Field(
            description="Oracle service name or SID",
        ),
    ] = c.DbOracle.Connection.DEFAULT_SERVICE_NAME
    oracle_user: Annotated[
        t.SecretStr,
        u.Field(
            description="Oracle database username",
        ),
    ] = u.Field(default_factory=lambda: t.SecretStr(""))
    oracle_password: Annotated[
        t.SecretStr,
        u.Field(
            description="Oracle database password",
        ),
    ] = u.Field(default_factory=lambda: t.SecretStr(""))
    default_target_schema: Annotated[
        str,
        u.Field(
            description="Default target schema for data loading",
        ),
    ] = "SINGER_DATA"
    batch_size: Annotated[
        int, u.Field(ge=1, description="Batch size for data loading")
    ] = 1000
    commit_interval: Annotated[
        int, u.Field(ge=1, description="Commit interval for transactions")
    ] = 1000
    transaction_timeout: Annotated[
        int, u.Field(ge=1, description="Transaction timeout in seconds")
    ] = 30
    parallel_degree: Annotated[
        int, u.Field(ge=1, description="Oracle parallel execution degree")
    ] = 1
    table_prefix: Annotated[
        str, u.Field(description="Prefix applied to table names")
    ] = ""
    table_suffix: Annotated[
        str, u.Field(description="Suffix applied to table names")
    ] = ""
    use_bulk_operations: Annotated[
        bool, u.Field(description="Use bulk operations for faster loading")
    ] = True
    autocommit: Annotated[bool, u.Field(description="Auto-commit transactions")] = False

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
            return r[bool].fail("Oracle host is required")
        if not self.oracle_service_name:
            return r[bool].fail("Oracle service name is required")
        if not self.default_target_schema:
            return r[bool].fail("Default target schema is required")
        if self.commit_interval > self.batch_size:
            return r[bool].fail(
                "Commit interval must be less than or equal to batch size",
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
