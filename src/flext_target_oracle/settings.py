"""FLEXT Target Oracle Configuration - Enhanced FlextSettings Implementation.

Single unified configuration class for Oracle Singer target operations following
FLEXT 1.0.0 patterns with enhanced singleton, SecretStr, and Pydantic 2.11+ features.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import warnings
from typing import Self

from flext_core import FlextConstants, FlextResult, FlextSettings
from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import SettingsConfigDict

from flext_target_oracle.constants import c
from flext_target_oracle.models import m
from flext_target_oracle.typings import t

# LoadMethod moved to constants.py as c.LoadMethod (DRY pattern)
LoadMethod = c.LoadMethod


class FlextTargetOracleSettings(FlextSettings):
    """Oracle Target Configuration using enhanced FlextSettings patterns.

    This class extends FlextSettings and includes all the configuration fields
    needed for Oracle target operations. Uses the enhanced singleton pattern
    with get_or_create_shared_instance for thread-safe configuration management.

    Follows standardized pattern:
    - Extends FlextSettings from flext-core
    - Uses SecretStr for sensitive data (oracle_password)
    - All defaults from FlextConstants where possible
    - Uses enhanced singleton pattern with inverse dependency injection
    - Uses Pydantic 2.11+ features (field_validator, model_validator)
    """

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_TARGET_ORACLE_",
        case_sensitive=False,
        extra="ignore",
        str_strip_whitespace=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        frozen=False,
        # Enhanced Pydantic 2.11+ features
        use_enum_values=True,
        validate_return=True,
        json_schema_extra={
            "title": "FLEXT Target Oracle Configuration",
            "description": "Oracle Singer target configuration extending FlextSettings",
        },
    )

    # Oracle connection settings using SecretStr for password
    oracle_host: str = Field(
        default="localhost",
        min_length=1,
        description="Oracle database host",
    )

    oracle_port: int = Field(
        default=1521,
        ge=1,
        le=65535,
        description="Oracle database port",
    )

    oracle_service_name: str = Field(
        default="XE",
        min_length=1,
        description="Oracle service name",
    )

    oracle_user: str = Field(
        default="target_user",
        min_length=1,
        description="Oracle database username",
    )

    oracle_password: SecretStr = Field(
        default_factory=lambda: SecretStr("default_password"),
        description="Oracle database password (sensitive)",
    )

    # Target configuration using FlextConstants where applicable
    default_target_schema: str = Field(
        default="SINGER_DATA",
        min_length=1,
        description="Default schema for loading data",
    )

    table_prefix: str = Field(
        default="",
        description="Prefix for target table names",
    )

    table_suffix: str = Field(
        default="",
        description="Suffix for target table names",
    )

    # Loading configuration using FlextConstants
    batch_size: int = Field(
        default=FlextConstants.Performance.DEFAULT_DB_POOL_SIZE * 250,  # 5000
        ge=1,
        le=50000,
        description="Number of records per batch",
    )

    use_bulk_operations: bool = Field(
        default=True,
        description="Use Oracle bulk operations for better performance",
    )

    parallel_degree: int = Field(
        default=1,
        ge=1,
        le=32,
        description="Oracle parallel degree for operations",
    )

    # Transaction settings using FlextConstants
    autocommit: bool = Field(
        default=False,
        description="Enable autocommit for operations",
    )

    commit_interval: int = Field(
        default=FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE,
        ge=1,
        description="Number of records between commits",
    )

    transaction_timeout: int = Field(
        default=FlextConstants.Defaults.TIMEOUT * 10,  # 300 seconds
        ge=1,
        le=3600,
        description="Transaction timeout in seconds",
    )

    # Project identification
    project_name: str = Field(
        default="flext-target-oracle",
        description="Project name",
    )

    project_version: str = Field(
        default="0.9.0",
        description="Project version",
    )

    # Pydantic 2.11+ field validators
    @field_validator("default_target_schema")
    @classmethod
    def validate_default_target_schema(cls, v: str) -> str:
        """Transform Oracle schema name to uppercase."""
        return v.strip().upper()

    @model_validator(mode="after")
    def validate_oracle_configuration_consistency(self) -> Self:
        """Validate Oracle configuration consistency (performance warnings only)."""
        # Validate batch size reasonable for performance
        if self.batch_size > FlextConstants.Performance.BatchProcessing.MAX_ITEMS // 5:
            warnings.warn(
                f"Large batch size ({self.batch_size}) may impact performance",
                UserWarning,
                stacklevel=2,
            )

        # Validate parallel degree settings
        if self.parallel_degree > FlextConstants.Validation.MAX_WORKERS_LIMIT:
            warnings.warn(
                f"High parallel degree ({self.parallel_degree}) may impact system resources",
                UserWarning,
                stacklevel=2,
            )

        return self

    def validate_business_rules(self) -> FlextResult[bool]:
        """Validate Oracle Target specific business rules."""
        try:
            # Validate connection requirements
            if not self.oracle_host or not self.oracle_user:
                return FlextResult[bool].fail("Oracle host and username are required")

            if not self.oracle_password.get_secret_value():
                return FlextResult[bool].fail("Oracle password is required")

            # Validate schema name
            if not self.default_target_schema:
                return FlextResult[bool].fail("Target schema is required")

            # Validate performance settings
            if self.batch_size < 1:
                return FlextResult[bool].fail("Batch size must be at least 1")

            if self.commit_interval > self.batch_size:
                return FlextResult[bool].fail(
                    "Commit interval cannot be larger than batch size",
                )

            return FlextResult[bool].ok(value=True)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            return FlextResult[bool].fail(f"Business rules validation failed: {e}")

    # Configuration helper methods that leverage the base model
    def get_oracle_config(self) -> m.TargetOracle.OracleConnectionConfig:
        """Convert to flext-db-oracle configuration format."""
        return m.TargetOracle.OracleConnectionConfig(
            host=self.oracle_host,
            port=self.oracle_port,
            service_name=self.oracle_service_name,
            username=self.oracle_user,
            password=self.oracle_password.get_secret_value(),
            timeout=self.transaction_timeout,
            pool_min=FlextConstants.Performance.MIN_DB_POOL_SIZE,
            pool_max=FlextConstants.Performance.DEFAULT_DB_POOL_SIZE * 5,
            pool_increment=FlextConstants.Performance.MIN_DB_POOL_SIZE,
            encoding="UTF-8",
            ssl_enabled=False,
            autocommit=self.autocommit,
            use_bulk_operations=self.use_bulk_operations,
            parallel_degree=self.parallel_degree,
        )

    def get_target_config(self) -> m.TargetOracle.TargetConfig:
        """Get target-specific configuration dictionary."""
        return m.TargetOracle.TargetConfig(
            default_target_schema=self.default_target_schema,
            use_bulk_operations=self.use_bulk_operations,
            batch_size=self.batch_size,
            table_prefix=self.table_prefix,
            table_suffix=self.table_suffix,
        )

    def get_table_name(self, stream_name: str) -> str:
        """Generate Oracle table name from Singer stream name."""
        # Standard transformation
        base_name = stream_name.replace("-", "_").replace(".", "_")

        # Apply prefix and suffix
        if self.table_prefix:
            base_name = f"{self.table_prefix}{base_name}"
        if self.table_suffix:
            base_name = f"{base_name}{self.table_suffix}"

        # Convert to uppercase and ensure Oracle naming limit (30 characters)
        table_name = base_name.upper()
        oracle_table_name_limit = 30  # Oracle table name limit

        if len(table_name) > oracle_table_name_limit:
            # Truncate intelligently - keep prefix/suffix if possible
            if self.table_prefix and self.table_suffix:
                prefix_len = len(self.table_prefix)
                suffix_len = len(self.table_suffix)
                remaining = oracle_table_name_limit - prefix_len - suffix_len
                if remaining > 0:
                    core = table_name[prefix_len:-suffix_len][:remaining]
                    table_name = f"{self.table_prefix}{core}{self.table_suffix}".upper()
                else:
                    table_name = table_name[:oracle_table_name_limit]
            else:
                table_name = table_name[:oracle_table_name_limit]

        return table_name

    @classmethod
    def create_for_environment(
        cls,
        environment: str,
        **_overrides: object,
    ) -> FlextTargetOracleSettings:
        """Create configuration for specific environment using enhanced singleton pattern."""
        env_overrides: dict[str, t.GeneralValueType] = {}

        if environment == "production":
            env_overrides.update({
                "batch_size": FlextConstants.Performance.BatchProcessing.MAX_ITEMS // 2,
                "use_bulk_operations": True,
                "transaction_timeout": FlextConstants.Network.DEFAULT_TIMEOUT
                * 10,  # 5 minutes for production
            })
        elif environment == "development":
            env_overrides.update({
                "batch_size": FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE,  # Smaller batches for development
                "use_bulk_operations": False,
                "transaction_timeout": FlextConstants.Network.DEFAULT_TIMEOUT * 2,
            })
        elif environment == "staging":
            env_overrides.update({
                "batch_size": FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE
                * 2.5,
                "use_bulk_operations": True,
                "transaction_timeout": FlextConstants.Network.DEFAULT_TIMEOUT * 6,
            })

        return cls.get_global_instance()

    @classmethod
    def get_global_instance(cls) -> Self:
        """Get the global singleton instance using enhanced FlextSettings pattern."""
        return super().get_global_instance()

    @classmethod
    def create_for_development(cls, **_overrides: object) -> Self:
        """Create configuration for development environment."""
        return super().get_global_instance()

    @classmethod
    def create_for_production(cls, **_overrides: object) -> Self:
        """Create configuration for production environment."""
        return super().get_global_instance()

    @classmethod
    def create_for_testing(cls, **_overrides: object) -> Self:
        """Create configuration for testing environment."""
        return super().get_global_instance()

    @classmethod
    def reset_global_instance(cls) -> None:
        """Reset the global FlextTargetOracleSettings instance (mainly for testing)."""
        super().reset_global_instance()


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
