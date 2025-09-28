"""Target Configuration Management for FLEXT Target Oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic_settings import SettingsConfigDict

from flext_core import FlextConfig, FlextResult, FlextTypes


class LoadMethod(StrEnum):
    """Oracle data loading strategies with performance characteristics."""

    INSERT = "INSERT"
    MERGE = "MERGE"
    BULK_INSERT = "BULK_INSERT"
    BULK_MERGE = "BULK_MERGE"


class FlextTargetOracleConfig(FlextConfig):
    """Oracle Target Configuration using enhanced FlextConfig patterns.

    This class extends FlextConfig and includes all the configuration fields
    needed for Oracle target operations. Uses the enhanced singleton pattern
    with get_or_create_shared_instance for thread-safe configuration management.
    """

    # Oracle connection settings - moved from models to main config
    oracle_host: str = "localhost"
    oracle_port: int = 1521
    oracle_service_name: str = "XE"
    oracle_user: str = "target_user"
    oracle_password: str = "default_password"

    # Target configuration
    default_target_schema: str = "SINGER_DATA"
    table_prefix: str = ""
    table_suffix: str = ""

    # Loading configuration
    batch_size: int = 5000
    use_bulk_operations: bool = True
    parallel_degree: int = 1

    # Transaction settings
    autocommit: bool = False
    commit_interval: int = 1000
    transaction_timeout: int = 300

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_TARGET_ORACLE_",
        case_sensitive=False,
        extra="ignore",
        str_strip_whitespace=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        frozen=False,
    )

    # Configuration helper methods that leverage the base model
    def get_oracle_config(self) -> dict[str, object]:
        """Convert to flext-db-oracle configuration format."""
        oracle_config: dict[str, object] = {
            "host": self.oracle_host,
            "port": self.oracle_port,
            "service_name": self.oracle_service_name,
            "username": self.oracle_user,
            "password": self.oracle_password,
            "timeout": self.transaction_timeout,
            "pool_min": 1,
            "pool_max": 10,
            "pool_increment": 1,
            "encoding": "UTF-8",
            "ssl_enabled": False,
            "autocommit": self.autocommit,
        }

        # Add advanced Oracle features if enabled
        if self.use_bulk_operations:
            oracle_config["use_bulk_operations"] = True
        if self.parallel_degree and self.parallel_degree > 1:
            oracle_config["parallel_degree"] = self.parallel_degree

        return oracle_config

    def get_target_config(self) -> dict[str, object]:
        """Get target-specific configuration dictionary."""
        return {
            "default_target_schema": self.default_target_schema,
            "use_bulk_operations": self.use_bulk_operations,
            "batch_size": self.batch_size,
            "table_prefix": self.table_prefix,
            "table_suffix": self.table_suffix,
        }

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
        oracle_table_name_limit = 30

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
        cls, environment: str, **overrides: object
    ) -> FlextTargetOracleConfig:
        """Create configuration for specific environment."""
        env_overrides: dict[str, object] = {}

        if environment == "production":
            env_overrides.update({
                "batch_size": 5000,
                "use_bulk_operations": True,
                "transaction_timeout": 300,  # 5 minutes for production
            })
        elif environment == "development":
            env_overrides.update({
                "batch_size": 1000,  # Smaller batches for development
                "use_bulk_operations": False,
                "transaction_timeout": 60,
            })
        elif environment == "staging":
            env_overrides.update({
                "batch_size": 2500,
                "use_bulk_operations": True,
                "transaction_timeout": 180,
            })

        all_overrides = {**env_overrides, **overrides}
        return cls(**all_overrides)

    @classmethod
    def get_global_instance(cls) -> Self:
        """Get the global singleton instance using enhanced FlextConfig pattern."""
        return cls.get_or_create_shared_instance(project_name="flext-target-oracle")

    @classmethod
    def create_for_development(cls, **overrides: object) -> Self:
        """Create configuration for development environment."""
        dev_overrides: dict[str, object] = {
            "batch_size": 1000,  # Smaller batches for development
            "use_bulk_operations": False,
            "transaction_timeout": 60,
            **overrides,
        }
        return cls.get_or_create_shared_instance(
            project_name="flext-target-oracle", **dev_overrides
        )

    @classmethod
    def create_for_production(cls, **overrides: object) -> Self:
        """Create configuration for production environment."""
        prod_overrides: dict[str, object] = {
            "batch_size": 5000,
            "use_bulk_operations": True,
            "transaction_timeout": 300,  # 5 minutes for production
            **overrides,
        }
        return cls.get_or_create_shared_instance(
            project_name="flext-target-oracle", **prod_overrides
        )

    @classmethod
    def create_for_testing(cls, **overrides: object) -> Self:
        """Create configuration for testing environment."""
        test_overrides: dict[str, object] = {
            "batch_size": 100,
            "use_bulk_operations": False,
            "transaction_timeout": 30,
            "oracle_host": "localhost",
            "oracle_service_name": "XE",
            **overrides,
        }
        return cls.get_or_create_shared_instance(
            project_name="flext-target-oracle", **test_overrides
        )


def validate_oracle_configuration(config: FlextTargetOracleConfig) -> FlextResult[None]:
    """Validate Oracle configuration using FlextConfig patterns - ZERO DUPLICATION."""
    # Required string fields validation using direct validation
    required_fields = [
        (config.oracle_host, "Oracle host is required"),
        (config.oracle_service_name, "Oracle service name is required"),
        (config.oracle_user, "Oracle username is required"),
        (config.oracle_password, "Oracle password is required"),
        (config.default_target_schema, "Target schema is required"),
    ]

    # Validate required string fields using direct validation
    for field_value, error_message in required_fields:
        if not (field_value and str(field_value).strip()):
            return FlextResult[None].fail(error_message)

    # Validate Oracle port range
    if not (1 <= config.oracle_port <= 65535):
        return FlextResult[None].fail("Oracle port must be between 1 and 65535")

    # Validate batch size constraints
    if config.batch_size < 1:
        return FlextResult[None].fail("Batch size must be at least 1")

    # Validate parallel degree
    if config.parallel_degree < 1:
        return FlextResult[None].fail("Parallel degree must be at least 1")

    # Validate transaction timeout
    if config.transaction_timeout < 1:
        return FlextResult[None].fail("Transaction timeout must be at least 1 second")

    return FlextResult[None].ok(None)


__all__: FlextTypes.Core.StringList = [
    "FlextTargetOracleConfig",
    "LoadMethod",
    "validate_oracle_configuration",
]
