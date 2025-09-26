"""Target Configuration Management for FLEXT Target Oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import threading
from enum import StrEnum
from typing import ClassVar

from pydantic import Field, SecretStr, field_validator, model_validator

from flext_core import FlextConfig, FlextResult, FlextTypes

from .constants import FlextTargetOracleConstants


class LoadMethod(StrEnum):
    """Oracle data loading strategies with performance characteristics."""

    INSERT = "INSERT"
    MERGE = "MERGE"
    BULK_INSERT = "BULK_INSERT"
    BULK_MERGE = "BULK_MERGE"


class FlextTargetOracleConfig(FlextConfig):
    """Oracle Target Configuration extending FlextConfig.

    Follows standardized [Project]Config pattern:
    - Extends FlextConfig from flext-core
    - Uses SecretStr for sensitive data
    - All defaults from FlextTargetOracleConstants
    - Proper Pydantic 2 validation
    - Singleton pattern with proper typing

    Type-safe Oracle target configuration with comprehensive validation.
    """

    # Singleton pattern attributes
    _global_instance: ClassVar[FlextTargetOracleConfig | None] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()

    # Oracle Database Configuration
    oracle_host: str = Field(
        ...,
        description="Oracle database hostname or IP address",
        min_length=1,
        max_length=255,
    )

    oracle_port: int = Field(
        default=FlextTargetOracleConstants.Connection.DEFAULT_PORT,
        ge=FlextTargetOracleConstants.Connection.MIN_PORT,
        le=FlextTargetOracleConstants.Connection.MAX_PORT,
        description="Oracle listener port number",
    )

    oracle_service: str = Field(
        ...,
        description="Oracle service name for connection",
        min_length=1,
        max_length=64,
    )

    oracle_user: str = Field(
        ...,
        description="Oracle database username",
        min_length=1,
        max_length=128,
    )

    oracle_password: SecretStr = Field(
        ...,
        description="Oracle database password (sensitive)",
    )

    default_target_schema: str = Field(
        default=target,
        description="Default target schema for table creation",
        min_length=1,
        max_length=128,
    )

    # Data Loading Configuration
    load_method: LoadMethod = Field(
        default=LoadMethod.INSERT,
        description="Oracle data loading strategy",
    )

    use_bulk_operations: bool = Field(
        default=True,
        description="Enable Oracle bulk operations for performance",
    )

    batch_size: int = Field(
        default=FlextTargetOracleConstants.Processing.DEFAULT_BATCH_SIZE,
        gt=0,
        le=50000,  # Reasonable upper limit for Oracle batch operations
        description="Number of records per batch for processing",
    )

    connection_timeout: int = Field(
        default=FlextTargetOracleConstants.Connection.DEFAULT_CONNECTION_TIMEOUT,
        gt=0,
        le=3600,  # Maximum 1 hour timeout
        description="Database connection timeout in seconds",
    )

    # SSL/TLS Configuration
    use_ssl: bool = Field(
        default=False,
        description="Enable SSL/TLS for Oracle connection (TCP/TCPS)",
    )

    ssl_verify: bool = Field(
        default=True,
        description="Verify SSL certificates",
    )

    ssl_wallet_location: str | None = Field(
        default=None,
        max_length=500,
        description="Oracle wallet location for SSL connections",
    )

    ssl_wallet_password: SecretStr | None = Field(
        default=None,
        description="Oracle wallet password (sensitive)",
    )

    disable_dn_matching: bool = Field(
        default=False,
        description="Disable DN (Distinguished Name) matching for SSL connections",
    )

    # Connection Pool Configuration
    pool_min_size: int = Field(
        default=1,
        ge=1,
        le=100,
        description="Minimum number of connections in pool",
    )

    pool_max_size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of connections in pool",
    )

    pool_increment: int = Field(
        default=1,
        ge=1,
        le=10,
        description="Number of connections to add when pool is exhausted",
    )

    # Advanced Oracle Features
    enable_auto_commit: bool = Field(
        default=True,
        description="Enable auto-commit for each batch",
    )

    use_direct_path: bool = Field(
        default=False,
        description="Use Oracle direct path load for bulk operations",
    )

    parallel_degree: int | None = Field(
        default=None,
        ge=1,
        le=64,
        description="Degree of parallelism for Oracle operations",
    )

    # Table and Column Configuration
    table_prefix: str | None = Field(
        default=None,
        max_length=30,
        description="Prefix to add to all table names",
    )

    table_suffix: str | None = Field(
        default=None,
        max_length=30,
        description="Suffix to add to all table names",
    )

    add_metadata_columns: bool = Field(
        default=True,
        description="Add Singer metadata columns (_sdc_*)",
    )

    # Data Storage Configuration
    default_string_length: int = Field(
        default=4000,
        ge=1,
        le=32767,
        description="Default length for VARCHAR2 columns",
    )

    default_timestamp_precision: int = Field(
        default=6,
        ge=0,
        le=9,
        description="Default precision for TIMESTAMP columns",
    )

    use_clob_threshold: int = Field(
        default=4000,
        ge=1,
        description="String length threshold to use CLOB instead of VARCHAR2",
    )

    # Table Management
    truncate_before_load: bool = Field(
        default=False,
        description="Truncate table before loading data",
    )

    force_recreate_tables: bool = Field(
        default=False,
        description="Drop and recreate tables even if they exist",
    )

    allow_alter_table: bool = Field(
        default=False,
        description="Allow ALTER TABLE for schema evolution",
    )

    # Index Management
    maintain_indexes: bool = Field(
        default=True,
        description="Maintain existing indexes when modifying tables",
    )

    create_foreign_key_indexes: bool = Field(
        default=True,
        description="Create indexes for foreign key relationships from schema",
    )

    # Pydantic 2 field validators
    @field_validator("oracle_port")
    @classmethod
    def validate_oracle_port(cls, v: int) -> int:
        """Validate Oracle port number is within valid TCP port range."""
        if not (
            FlextTargetOracleConstants.Connection.MIN_PORT
            <= v
            <= FlextTargetOracleConstants.Connection.MAX_PORT
        ):
            msg = f"Oracle port must be between {FlextTargetOracleConstants.Connection.MIN_PORT} and {FlextTargetOracleConstants.Connection.MAX_PORT}"
            raise ValueError(msg)
        return v

    @field_validator("batch_size")
    @classmethod
    def validate_batch_size(cls, v: int) -> int:
        """Validate batch size is positive and within reasonable limits."""
        if v <= 0:
            msg = "Batch size must be positive"
            raise ValueError(msg)
        return v

    @field_validator("connection_timeout")
    @classmethod
    def validate_connection_timeout(cls, v: int) -> int:
        """Validate connection timeout is positive and reasonable."""
        if v <= 0:
            msg = "Connection timeout must be positive"
            raise ValueError(msg)
        return v

    @model_validator(mode="after")
    def validate_pool_configuration(self) -> FlextTargetOracleConfig:
        """Validate connection pool configuration."""
        if self.pool_min_size > self.pool_max_size:
            msg = "pool_min_size cannot be greater than pool_max_size"
            raise ValueError(msg)

        if self.pool_increment > self.pool_max_size:
            msg = "pool_increment cannot be greater than pool_max_size"
            raise ValueError(msg)

        return self

    @model_validator(mode="after")
    def validate_ssl_configuration(self) -> FlextTargetOracleConfig:
        """Validate SSL configuration."""
        if (
            self.use_ssl
            and self.ssl_wallet_location
            and self.ssl_wallet_password is None
        ):
            msg = "ssl_wallet_password is required when ssl_wallet_location is provided"
            raise ValueError(msg)

        return self

    # Configuration helper methods
    def get_oracle_config(self) -> dict[str, object]:
        """Convert to flext-db-oracle configuration format."""
        oracle_config: dict[str, object] = {
            "host": self.oracle_host,
            "port": self.oracle_port,
            "service_name": self.oracle_service,
            "username": self.oracle_user,
            "password": self.oracle_password.get_secret_value(),
            "sid": "None",  # Use service_name instead of SID
            "timeout": self.connection_timeout,
            "pool_min": self.pool_min_size,
            "pool_max": self.pool_max_size,
            "pool_increment": self.pool_increment,
            "encoding": UTF - 8,
            "ssl_enabled": self.use_ssl,
            "autocommit": self.enable_auto_commit,
            "ssl_server_dn_match": not self.disable_dn_matching,
        }

        # Add SSL wallet configuration if provided
        if self.use_ssl and self.ssl_wallet_location:
            oracle_config["ssl_wallet_location"] = self.ssl_wallet_location
            if self.ssl_wallet_password:
                oracle_config["ssl_wallet_password"] = (
                    self.ssl_wallet_password.get_secret_value()
                )

        # Add advanced Oracle features if enabled
        if self.use_direct_path:
            oracle_config["use_direct_path"] = True
        if self.parallel_degree:
            oracle_config["parallel_degree"] = self.parallel_degree

        return oracle_config

    def get_target_config(self) -> dict[str, object]:
        """Get target-specific configuration dictionary."""
        return {
            "default_target_schema": self.default_target_schema,
            "load_method": self.load_method.value,
            "use_bulk_operations": self.use_bulk_operations,
            "batch_size": self.batch_size,
            "add_metadata_columns": self.add_metadata_columns,
            "table_prefix": self.table_prefix,
            "table_suffix": self.table_suffix,
        }

    def get_storage_config(self) -> dict[str, object]:
        """Get data storage configuration dictionary."""
        return {
            "default_string_length": self.default_string_length,
            "default_timestamp_precision": self.default_timestamp_precision,
            "use_clob_threshold": self.use_clob_threshold,
        }

    def get_table_management_config(self) -> dict[str, object]:
        """Get table management configuration dictionary."""
        return {
            "truncate_before_load": self.truncate_before_load,
            "force_recreate_tables": self.force_recreate_tables,
            "allow_alter_table": self.allow_alter_table,
            "maintain_indexes": self.maintain_indexes,
            "create_foreign_key_indexes": self.create_foreign_key_indexes,
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

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate Oracle target configuration business rules."""
        try:
            # Validate Oracle configuration
            if not self.oracle_host:
                return FlextResult[None].fail("Oracle host is required")

            if not self.oracle_user:
                return FlextResult[None].fail("Oracle username is required")

            if not self.oracle_password.get_secret_value():
                return FlextResult[None].fail("Oracle password is required")

            # Validate service name
            if not self.oracle_service:
                return FlextResult[None].fail("Oracle service name is required")

            # Validate SSL configuration
            if (
                self.use_ssl
                and self.ssl_wallet_location
                and self.ssl_wallet_password is None
            ):
                return FlextResult[None].fail(
                    "SSL wallet password is required when wallet location is provided"
                )

            # Validate pool configuration
            if self.pool_min_size > self.pool_max_size:
                return FlextResult[None].fail(
                    "pool_min_size cannot be greater than pool_max_size"
                )

            return FlextResult[None].ok(None)

        except Exception as e:
            return FlextResult[None].fail(f"Business rules validation failed: {e}")

    @classmethod
    def create_for_environment(
        cls, environment: str, **overrides: object
    ) -> FlextTargetOracleConfig:
        """Create configuration for specific environment."""
        env_overrides: dict[str, object] = {}

        if environment == "production":
            env_overrides.update({
                "batch_size": FlextTargetOracleConstants.Processing.DEFAULT_BATCH_SIZE,
                "use_bulk_operations": "True",
                "pool_max_size": 10,
                "connection_timeout": 300,  # 5 minutes for production
            })
        elif environment == "development":
            env_overrides.update({
                "batch_size": 1000,  # Smaller batches for development
                "use_bulk_operations": "False",
                "pool_max_size": 2,
                "connection_timeout": 60,
            })
        elif environment == "staging":
            env_overrides.update({
                "batch_size": FlextTargetOracleConstants.Processing.DEFAULT_BATCH_SIZE
                // 2,
                "use_bulk_operations": "True",
                "pool_max_size": 5,
                "connection_timeout": 180,
            })

        all_overrides = {**env_overrides, **overrides}
        # Pydantic BaseSettings handles kwargs validation and type conversion automatically
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
                        oracle_host=localhost,
                        oracle_service=xe,
                        oracle_user=target_user,
                        oracle_password=SecretStr("default_password"),
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
