"""Target Configuration Management for FLEXT Target Oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import threading
from enum import StrEnum
from typing import ClassVar

from flext_core import FlextResult, FlextTypes

from .models import FlextTargetOracleModels


class LoadMethod(StrEnum):
    """Oracle data loading strategies with performance characteristics."""

    INSERT = "INSERT"
    MERGE = "MERGE"
    BULK_INSERT = "BULK_INSERT"
    BULK_MERGE = "BULK_MERGE"


class FlextTargetOracleConfig(FlextTargetOracleModels.OracleTargetConfig):
    """Oracle Target Configuration following standardized [Project]Models pattern.

    This class now properly extends FlextTargetOracleModels.OracleTargetConfig,
    ensuring we use the standardized models throughout the codebase instead
    of duplicating validation logic.

    All configuration fields and validation are now inherited from the
    FlextTargetOracleModels.OracleTargetConfig class.
    """

    # Singleton pattern attributes
    _global_instance: ClassVar[FlextTargetOracleConfig | None] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()

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

    # Singleton pattern override for proper typing
    @classmethod
    def get_global_instance(cls) -> FlextTargetOracleConfig:
        """Get the global singleton instance of FlextTargetOracleConfig."""
        if cls._global_instance is None:
            with cls._lock:
                if cls._global_instance is None:
                    # This will require manual initialization with required fields
                    # in production use
                    cls._global_instance = cls(
                        oracle_host="localhost",
                        oracle_service_name="xe",
                        oracle_user="target_user",
                        oracle_password="default_password",
                    )
        return cls._global_instance

    @classmethod
    def reset_global_instance(cls) -> None:
        """Reset the global FlextTargetOracleConfig instance (mainly for testing)."""
        cls._global_instance = None


def validate_oracle_configuration(config: FlextTargetOracleConfig) -> FlextResult[None]:
    """Validate Oracle configuration using flext-core FlextValidations - ZERO DUPLICATION."""
    # Required string fields validation using flext-core
    required_fields = [
        (config.oracle_host, "Oracle host is required"),
        (config.oracle_service, "Oracle service is required"),
        (config.oracle_user, "Oracle username is required"),
        (
            config.oracle_password.get_secret_value()
            if config.oracle_password
            else None,
            "Oracle password is required",
        ),
        (config.default_target_schema, "Target schema is required"),
    ]

    # Validate required string fields using direct validation
    for field_value, error_message in required_fields:
        if not (field_value and str(field_value).strip()):
            return FlextResult[None].fail(error_message)

    # Validate pool size constraints using direct number validation
    if not isinstance(config.pool_min_size, (int, float)) or config.pool_min_size < 0:
        return FlextResult[None].fail("Pool min size must be a non-negative number")

    if config.pool_max_size < config.pool_min_size:
        return FlextResult[None].fail(
            "Pool max size must be greater than or equal to pool min size",
        )

    # SSL configuration consistency validation
    if (
        config.use_ssl
        and config.ssl_wallet_password
        and not (config.ssl_wallet_location and str(config.ssl_wallet_location).strip())
    ):
        return FlextResult[None].fail(
            "SSL wallet location is required when wallet password is provided",
        )

    return FlextResult[None].ok(None)


__all__: FlextTypes.Core.StringList = [
    "FlextTargetOracleConfig",
    "LoadMethod",
    "validate_oracle_configuration",
]
