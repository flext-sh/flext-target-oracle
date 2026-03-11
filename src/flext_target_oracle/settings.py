"""FLEXT Target Oracle Configuration - Enhanced FlextSettings Implementation.

Single unified configuration class for Oracle Singer target operations following
FLEXT 1.0.0 patterns with enhanced singleton, SecretStr, and Pydantic 2.11+ features.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextLogger, FlextResult, FlextSettings
from pydantic import Field, SecretStr

from .constants import c
from .target_models import OracleConnectionModel

logger = FlextLogger(__name__)
LoadMethod = c.LoadMethod


class FlextTargetOracleSettings(FlextSettings):
    """Runtime settings for Oracle Singer target operations."""

    oracle_host: str = Field(default="localhost", description="Oracle database host")
    oracle_port: int = Field(default=1521, description="Oracle database port")
    oracle_service_name: str = Field(
        default="ORCL", description="Oracle service name or SID"
    )
    oracle_user: SecretStr = Field(
        default_factory=lambda: SecretStr(""),
        description="Oracle database username",
    )
    oracle_password: SecretStr = Field(
        default_factory=lambda: SecretStr(""),
        description="Oracle database password",
    )
    default_target_schema: str = Field(
        default="SINGER_DATA", description="Default target schema for data loading"
    )
    batch_size: int = Field(
        default=1000, ge=1, description="Batch size for data loading"
    )
    commit_interval: int = Field(
        default=1000, ge=1, description="Commit interval for transactions"
    )
    transaction_timeout: int = Field(
        default=30, ge=1, description="Transaction timeout in seconds"
    )
    parallel_degree: int = Field(
        default=1, ge=1, description="Oracle parallel execution degree"
    )
    table_prefix: str = Field(default="", description="Prefix applied to table names")
    table_suffix: str = Field(default="", description="Suffix applied to table names")
    use_bulk_operations: bool = Field(
        default=True, description="Use bulk operations for faster loading"
    )
    autocommit: bool = Field(default=False, description="Auto-commit transactions")

    def get_table_name(self, stream_name: str) -> str:
        """Get table name from stream name."""
        normalized_stream_name = stream_name.replace("-", "_").replace(".", "_")
        full_table_name = (
            f"{self.table_prefix}{normalized_stream_name}{self.table_suffix}"
        )
        return full_table_name.upper()

    def validate_business_rules(self) -> FlextResult[bool]:
        """Validate Oracle target configuration business rules."""
        if not self.oracle_host:
            return FlextResult[bool].fail("Oracle host is required")
        if not self.oracle_service_name:
            return FlextResult[bool].fail("Oracle service name is required")
        if not self.default_target_schema:
            return FlextResult[bool].fail("Default target schema is required")
        if self.commit_interval > self.batch_size:
            return FlextResult[bool].fail(
                "Commit interval must be less than or equal to batch size"
            )
        return FlextResult[bool].ok(True)

    def get_oracle_config(self) -> OracleConnectionModel:
        """Get Oracle database connection configuration."""
        return OracleConnectionModel(
            host=self.oracle_host,
            port=self.oracle_port,
            service_name=self.oracle_service_name,
            username=self.oracle_user.get_secret_value(),
            password=self.oracle_password.get_secret_value(),
            timeout=self.transaction_timeout,
            pool_min=c.Loading.DEFAULT_POOL_MIN,
            pool_max=c.Loading.DEFAULT_POOL_MAX,
            pool_increment=1,
            encoding="UTF-8",
            ssl_enabled=False,
            autocommit=self.autocommit,
            use_bulk_operations=self.use_bulk_operations,
            parallel_degree=self.parallel_degree,
        )


def validate_oracle_configuration(
    config: FlextTargetOracleSettings,
) -> FlextResult[bool]:
    """Validate Oracle configuration using FlextSettings patterns - ZERO DUPLICATION."""
    return config.validate_business_rules()


__all__: list[str] = [
    "FlextTargetOracleSettings",
    "LoadMethod",
    "validate_oracle_configuration",
]
