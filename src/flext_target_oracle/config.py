"""FLEXT Target Oracle Configuration - Enhanced FlextConfig Implementation.

Single unified configuration class for Oracle Singer target operations following
FLEXT 1.0.0 patterns with enhanced singleton, SecretStr, and Pydantic 2.11+ features.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from flext_core import FlextConfig, FlextConstants, FlextResult, FlextTypes
from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import SettingsConfigDict


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

    Follows standardized pattern:
    - Extends FlextConfig from flext-core
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
            "description": "Oracle Singer target configuration extending FlextConfig",
        },
    )

    # Oracle connection settings using SecretStr for password
    oracle_host: str = Field(
        default="localhost",
        description="Oracle database host",
    )

    oracle_port: int = Field(
        default=FlextConstants.Platform.DATABASE_DEFAULT_PORT,
        ge=1,
        le=65535,
        description="Oracle database port",
    )

    oracle_service_name: str = Field(
        default="XE",
        description="Oracle service name",
    )

    oracle_user: str = Field(
        default="target_user",
        description="Oracle database username",
    )

    oracle_password: SecretStr = Field(
        default_factory=lambda: SecretStr("default_password"),
        description="Oracle database password (sensitive)",
    )

    # Backward compatibility properties for old attribute names
    @property
    def host(self) -> str:
        """Backward compatibility property for oracle_host."""
        return self.oracle_host

    @property
    def port(self) -> int:
        """Backward compatibility property for oracle_port."""
        return self.oracle_port

    @property
    def service_name(self) -> str:
        """Backward compatibility property for oracle_service_name."""
        return self.oracle_service_name

    @property
    def username(self) -> str:
        """Backward compatibility property for oracle_username."""
        return self.oracle_user

    @property
    def protocol(self) -> str:
        """Backward compatibility property for connection protocol."""
        return "tcps"  # Default protocol for Oracle connections

    @property
    def ssl_enabled(self) -> bool:
        """Backward compatibility property for SSL configuration."""
        return True  # Default SSL enabled for Oracle connections

    @property
    def pool_min(self) -> int:
        """Backward compatibility property for minimum pool size."""
        return 1  # Default minimum pool size

    @property
    def pool_max(self) -> int:
        """Backward compatibility property for maximum pool size."""
        return 10  # Default maximum pool size

    @property
    def connection_pool_size(self) -> int:
        """Backward compatibility property for connection pool size."""
        return self.pool_max

    @property
    def connection_pool_max_overflow(self) -> int:
        """Backward compatibility property for connection pool max overflow."""
        return self.pool_max * 2  # Default overflow

    @property
    def use_ssl(self) -> bool:
        """Backward compatibility property for SSL usage."""
        return self.ssl_enabled

    @property
    def column_mappings(self) -> FlextTypes.StringDict:
        """Backward compatibility property for column mappings."""
        return {}

    @property
    def ignored_columns(self) -> FlextTypes.StringList:
        """Backward compatibility property for ignored columns."""
        return []

    @property
    def custom_type_mappings(self) -> FlextTypes.StringDict:
        """Backward compatibility property for custom type mappings."""
        return {}

    @property
    def load_method(self) -> str:
        """Backward compatibility property for load method."""
        return "upsert"  # Default load method

    @property
    def allow_alter_table(self) -> bool:
        """Backward compatibility property for allow alter table."""
        return True  # Default allow alter table

    # Target configuration using FlextConstants where applicable
    default_target_schema: str = Field(
        default="SINGER_DATA",
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
    @field_validator("oracle_host")
    @classmethod
    def validate_oracle_host(cls, v: str) -> str:
        """Validate Oracle host format."""
        if not v.strip():
            msg = "Oracle host cannot be empty"
            raise ValueError(msg)
        return v.strip()

    @field_validator("oracle_service_name")
    @classmethod
    def validate_oracle_service_name(cls, v: str) -> str:
        """Validate Oracle service name format."""
        if not v.strip():
            msg = "Oracle service name cannot be empty"
            raise ValueError(msg)
        return v.strip()

    @field_validator("oracle_user")
    @classmethod
    def validate_oracle_user(cls, v: str) -> str:
        """Validate Oracle user format."""
        if not v.strip():
            msg = "Oracle username cannot be empty"
            raise ValueError(msg)
        return v.strip()

    @field_validator("default_target_schema")
    @classmethod
    def validate_default_target_schema(cls, v: str) -> str:
        """Validate Oracle schema name format."""
        if not v.strip():
            msg = "Target schema cannot be empty"
            raise ValueError(msg)
        return v.strip().upper()

    @model_validator(mode="after")
    def validate_oracle_configuration_consistency(self) -> Self:
        """Validate Oracle configuration consistency."""
        # Validate password is not empty
        if not self.oracle_password.get_secret_value().strip():
            msg = "Oracle password cannot be empty"
            raise ValueError(msg)

        # Validate batch size reasonable for performance
        if self.batch_size > FlextConstants.Performance.BatchProcessing.MAX_ITEMS // 5:
            import warnings

            warnings.warn(
                f"Large batch size ({self.batch_size}) may impact performance",
                UserWarning,
                stacklevel=2,
            )

        # Validate parallel degree settings
        if self.parallel_degree > FlextConstants.Container.MAX_WORKERS:
            import warnings

            warnings.warn(
                f"High parallel degree ({self.parallel_degree}) may impact system resources",
                UserWarning,
                stacklevel=2,
            )

        return self

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate Oracle Target specific business rules."""
        try:
            # Validate connection requirements
            if not self.oracle_host or not self.oracle_user:
                return FlextResult[None].fail("Oracle host and username are required")

            if not self.oracle_password.get_secret_value():
                return FlextResult[None].fail("Oracle password is required")

            # Validate schema name
            if not self.default_target_schema:
                return FlextResult[None].fail("Target schema is required")

            # Validate performance settings
            if self.batch_size < 1:
                return FlextResult[None].fail("Batch size must be at least 1")

            if self.commit_interval > self.batch_size:
                return FlextResult[None].fail(
                    "Commit interval cannot be larger than batch size"
                )

            return FlextResult[None].ok(None)
        except Exception as e:
            return FlextResult[None].fail(f"Business rules validation failed: {e}")

    # Configuration helper methods that leverage the base model
    def get_oracle_config(self) -> FlextTypes.Dict:
        """Convert to flext-db-oracle configuration format."""
        oracle_config: FlextTypes.Dict = {
            "host": self.oracle_host,
            "port": self.oracle_port,
            "service_name": self.oracle_service_name,
            "username": self.oracle_user,
            "password": self.oracle_password.get_secret_value(),
            "timeout": self.transaction_timeout,
            "pool_min": FlextConstants.Performance.MIN_DB_POOL_SIZE,
            "pool_max": FlextConstants.Performance.DEFAULT_DB_POOL_SIZE * 5,
            "pool_increment": FlextConstants.Performance.MIN_DB_POOL_SIZE,
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

    def get_target_config(self) -> FlextTypes.Dict:
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
        oracle_table_name_limit = FlextConstants.Limits.MAX_STRING_LENGTH

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
        """Create configuration for specific environment using enhanced singleton pattern."""
        env_overrides: FlextTypes.Dict = {}

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

        all_overrides = {**env_overrides, **overrides}
        return cls.get_or_create_shared_instance(
            project_name="flext-target-oracle", environment=environment, **all_overrides
        )

    @classmethod
    def get_global_instance(cls) -> Self:
        """Get the global singleton instance using enhanced FlextConfig pattern."""
        return cls.get_or_create_shared_instance(project_name="flext-target-oracle")

    @classmethod
    def create_for_development(cls, **overrides: object) -> Self:
        """Create configuration for development environment."""
        dev_overrides: FlextTypes.Dict = {
            "batch_size": FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE,  # Smaller batches for development
            "use_bulk_operations": False,
            "transaction_timeout": FlextConstants.Network.DEFAULT_TIMEOUT * 2,
            **overrides,
        }
        return cls.get_or_create_shared_instance(
            project_name="flext-target-oracle", **dev_overrides
        )

    @classmethod
    def create_for_production(cls, **overrides: object) -> Self:
        """Create configuration for production environment."""
        prod_overrides: FlextTypes.Dict = {
            "batch_size": FlextConstants.Performance.BatchProcessing.MAX_ITEMS // 2,
            "use_bulk_operations": True,
            "transaction_timeout": FlextConstants.Network.DEFAULT_TIMEOUT
            * 10,  # 5 minutes for production
            **overrides,
        }
        return cls.get_or_create_shared_instance(
            project_name="flext-target-oracle", **prod_overrides
        )

    @classmethod
    def create_for_testing(cls, **overrides: object) -> Self:
        """Create configuration for testing environment."""
        test_overrides: FlextTypes.Dict = {
            "batch_size": FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE // 10,
            "use_bulk_operations": False,
            "transaction_timeout": FlextConstants.Network.DEFAULT_TIMEOUT,
            "oracle_host": "localhost",
            "oracle_service_name": "XE",
            **overrides,
        }
        return cls.get_or_create_shared_instance(
            project_name="flext-target-oracle", **test_overrides
        )

    @classmethod
    def reset_global_instance(cls) -> None:
        """Reset the global FlextTargetOracleConfig instance (mainly for testing)."""
        cls.reset_shared_instance()


def validate_oracle_configuration(
    config: FlextTargetOracleConfig,
) -> FlextResult[None]:
    """Validate Oracle configuration using FlextConfig patterns - ZERO DUPLICATION."""
    # Required string fields validation using direct validation
    required_fields = [
        (config.oracle_host, "Oracle host is required"),
        (config.oracle_service_name, "Oracle service name is required"),
        (config.oracle_user, "Oracle username is required"),
        (config.oracle_password.get_secret_value(), "Oracle password is required"),
        (config.default_target_schema, "Target schema is required"),
    ]

    # Validate required string fields using direct validation
    for field_value, error_message in required_fields:
        if not (field_value and str(field_value).strip()):
            return FlextResult[None].fail(error_message)

    # Validate Oracle port range
    if not (
        FlextConstants.Network.MIN_PORT
        <= config.oracle_port
        <= FlextConstants.Network.MAX_PORT
    ):
        return FlextResult[None].fail(
            f"Oracle port must be between {FlextConstants.Network.MIN_PORT} and {FlextConstants.Network.MAX_PORT}"
        )

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


__all__: FlextTypes.StringList = [
    "FlextTargetOracleConfig",
    "LoadMethod",
    "validate_oracle_configuration",
]
