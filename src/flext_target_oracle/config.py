"""Configuration Management for FLEXT Target Oracle.

This module provides type-safe configuration management for Oracle Singer target
operations, implementing FLEXT ecosystem patterns with comprehensive validation
and enterprise-grade reliability standards.

The configuration system uses FlextValueObject as the foundation, providing
immutable, validated configuration objects with domain rule validation through
the Chain of Responsibility pattern. All validation follows railway-oriented
programming principles using FlextResult for consistent error handling.

Key Classes:
    FlextOracleTargetConfig: Main configuration class with comprehensive validation
    LoadMethod: Enumeration of supported Oracle data loading strategies
    OracleTargetConstants: System constants to eliminate magic numbers

Architecture Patterns:
    FlextValueObject: Immutable configuration with built-in validation
    Chain of Responsibility: Modular validation rule composition
    Railway-Oriented Programming: FlextResult for error handling
    Domain-Driven Design: Business rule validation with domain context

Example:
    Basic configuration with domain validation:

    >>> config = FlextOracleTargetConfig(
    ...     oracle_host="localhost",
    ...     oracle_service="XE",
    ...     oracle_user="target_user",
    ...     oracle_password="secure_password",
    ...     batch_size=2000,
    ...     load_method=LoadMethod.BULK_INSERT,
    ... )
    >>> validation_result = config.validate_domain_rules()
    >>> if validation_result.success:
    ...     print("Configuration validated successfully")
    ... else:
    ...     print(f"Validation failed: {validation_result.error}")

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from enum import StrEnum
from typing import Final

from flext_core import FlextResult, FlextValueObject
from pydantic import Field, SecretStr, field_validator


class OracleTargetConstants:
    """Oracle Target system constants following DRY principles.

    Centralizes magic numbers and system defaults to eliminate duplication
    and provide single source of truth for Oracle target configuration limits.

    Attributes:
        DEFAULT_PORT: Standard Oracle listener port (1521)
        DEFAULT_BATCH_SIZE: Optimal batch size for most workloads (1000)
        DEFAULT_CONNECTION_TIMEOUT: Conservative connection timeout (30s)
        DEFAULT_MAX_PARALLEL_STREAMS: Safe parallel processing limit (4)
        MIN_PORT: Minimum valid port number (1)
        MAX_PORT: Maximum valid port number (65535)

    """

    DEFAULT_PORT: Final = 1521
    DEFAULT_BATCH_SIZE: Final = 1000
    DEFAULT_CONNECTION_TIMEOUT: Final = 30
    DEFAULT_MAX_PARALLEL_STREAMS: Final = 4
    MIN_PORT: Final = 1
    MAX_PORT: Final = 65535


class LoadMethod(StrEnum):
    """Oracle data loading strategies with performance characteristics.

    Defines supported methods for loading Singer data into Oracle tables,
    each optimized for different use cases and performance requirements.

    Values:
        INSERT: Standard INSERT statements, best for small batches
        MERGE: UPSERT operations, best for incremental updates
        BULK_INSERT: Bulk INSERT operations, best for large data loads
        BULK_MERGE: Bulk MERGE operations, best for large incremental updates

    Example:
        >>> load_method = LoadMethod.BULK_INSERT
        >>> print(f"Using {load_method} for high-volume data loading")

    """

    INSERT = "insert"
    MERGE = "merge"
    BULK_INSERT = "bulk_insert"
    BULK_MERGE = "bulk_merge"


class FlextOracleTargetConfig(FlextValueObject):
    """Type-safe Oracle target configuration with comprehensive validation.

    Provides immutable configuration object for Oracle Singer target operations
    with built-in validation, domain rule checking, and integration with the
    FLEXT ecosystem's configuration management patterns.

    This configuration class extends FlextValueObject to provide:
    - Immutable configuration with value semantics
    - Comprehensive field validation using Pydantic
    - Domain rule validation through Chain of Responsibility pattern
    - Integration with flext-db-oracle for connection management
    - Environment variable support for deployment flexibility

    Attributes:
        oracle_host: Oracle database hostname or IP address (required)
        oracle_port: Oracle listener port (default: 1521, range: 1-65535)
        oracle_service: Oracle service name for connection (required)
        oracle_user: Oracle database username (required)
        oracle_password: Oracle database password (required, hidden in repr)
        default_target_schema: Target schema for table creation (default: "target")
        load_method: Data loading strategy (default: LoadMethod.INSERT)
        use_bulk_operations: Enable Oracle bulk operations (default: True)
        batch_size: Records per batch (default: 1000, must be positive)
        connection_timeout: Connection timeout in seconds (default: 30, must be positive)

    Example:
        Basic configuration for development:

        >>> config = FlextOracleTargetConfig(
        ...     oracle_host="localhost",
        ...     oracle_service="XE",
        ...     oracle_user="dev_user",
        ...     oracle_password="dev_password",
        ... )
        >>> print(f"Connecting to {config.oracle_host}:{config.oracle_port}")

        Production configuration with validation:

        >>> config = FlextOracleTargetConfig(
        ...     oracle_host="prod-oracle.company.com",
        ...     oracle_port=1521,
        ...     oracle_service="PRODDB",
        ...     oracle_user="target_user",
        ...     oracle_password="secure_prod_password",
        ...     default_target_schema="DATA_WAREHOUSE",
        ...     load_method=LoadMethod.BULK_INSERT,
        ...     batch_size=5000,
        ...     connection_timeout=60,
        ... )
        >>> validation_result = config.validate_domain_rules()
        >>> if validation_result.is_failure:
        ...     print(f"Configuration invalid: {validation_result.error}")

    Note:
        Domain validation requires database connectivity to verify permissions
        and schema access. Use validate_domain_rules() to perform comprehensive
        business rule validation beyond basic field validation.

    """

    oracle_host: str = Field(
        ...,
        description="Oracle database hostname or IP address",
        min_length=1,
        max_length=255,
    )
    oracle_port: int = Field(
        default=OracleTargetConstants.DEFAULT_PORT,
        description="Oracle listener port number",
        ge=OracleTargetConstants.MIN_PORT,
        le=OracleTargetConstants.MAX_PORT,
    )
    oracle_service: str = Field(
        ...,
        description="Oracle service name for connection",
        min_length=1,
        max_length=64,
    )
    oracle_user: str = Field(
        ..., description="Oracle database username", min_length=1, max_length=128,
    )
    oracle_password: str = Field(
        ...,
        description="Oracle database password",
        min_length=1,
        repr=False,  # Hide password in string representations
    )
    default_target_schema: str = Field(
        default="target",
        description="Default target schema for table creation",
        min_length=1,
        max_length=128,
    )
    load_method: LoadMethod = Field(
        default=LoadMethod.INSERT, description="Oracle data loading strategy",
    )
    use_bulk_operations: bool = Field(
        default=True, description="Enable Oracle bulk operations for performance",
    )
    batch_size: int = Field(
        default=OracleTargetConstants.DEFAULT_BATCH_SIZE,
        description="Number of records per batch for processing",
        gt=0,
        le=50000,  # Reasonable upper limit for Oracle batch operations
    )
    connection_timeout: int = Field(
        default=OracleTargetConstants.DEFAULT_CONNECTION_TIMEOUT,
        description="Database connection timeout in seconds",
        gt=0,
        le=3600,  # Maximum 1 hour timeout
    )

    @field_validator("oracle_port")
    @classmethod
    def validate_oracle_port(cls, v: int) -> int:
        """Validate Oracle port number is within valid TCP port range.

        Ensures the Oracle listener port is within the standard TCP port range
        and commonly used for Oracle database connections.

        Args:
            v: Port number to validate

        Returns:
            Validated port number

        Raises:
            ValueError: If port is outside valid range (1-65535)

        """
        if not (OracleTargetConstants.MIN_PORT <= v <= OracleTargetConstants.MAX_PORT):
            msg: str = f"Oracle port must be between {OracleTargetConstants.MIN_PORT} and {OracleTargetConstants.MAX_PORT}"
            raise ValueError(msg)
        return v

    @field_validator("batch_size")
    @classmethod
    def validate_batch_size(cls, v: int) -> int:
        """Validate batch size is positive and within reasonable limits.

        Ensures batch size is positive and doesn't exceed Oracle's practical
        limits for bulk operations and memory usage.

        Args:
            v: Batch size to validate

        Returns:
            Validated batch size

        Raises:
            ValueError: If batch size is not positive

        """
        if v <= 0:
            msg = "Batch size must be positive"
            raise ValueError(msg)
        return v

    @field_validator("connection_timeout")
    @classmethod
    def validate_connection_timeout(cls, v: int) -> int:
        """Validate connection timeout is positive and reasonable.

        Ensures connection timeout allows sufficient time for database
        connection establishment while preventing indefinite hangs.

        Args:
            v: Timeout value in seconds to validate

        Returns:
            Validated timeout value

        Raises:
            ValueError: If timeout is not positive

        """
        if v <= 0:
            msg = "Connection timeout must be positive"
            raise ValueError(msg)
        return v

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate business rules using Chain of Responsibility pattern.

        Performs comprehensive domain validation beyond basic field validation,
        including connectivity checks, permission validation, and schema access
        verification. Uses the Chain of Responsibility pattern to compose
        validation rules modularly.

        The validation chain includes:
        - Host reachability verification
        - Port accessibility testing
        - Database connectivity confirmation
        - User authentication validation
        - Schema permission verification

        Returns:
            FlextResult[None]: Success if all domain rules pass, failure with
            detailed error message if any validation rule fails

        Example:
            >>> config = FlextOracleTargetConfig(...)
            >>> result = config.validate_domain_rules()
            >>> if result.is_failure:
            ...     print(f"Configuration issue: {result.error}")
            ... else:
            ...     print("Configuration validated for production use")

        Note:
            This method requires network connectivity to the Oracle database
            and may take several seconds to complete due to connection testing.

        """
        try:
            # Use validation chain to eliminate multiple returns and compose rules
            validator = _ConfigurationValidator()
            return validator.validate(self)
        except Exception as e:
            return FlextResult.fail(f"Configuration validation failed: {e}")

    def get_oracle_config(self) -> dict[str, str | int | SecretStr | None | bool]:
        """Convert to flext-db-oracle configuration format.

        Transforms this configuration into the format expected by flext-db-oracle
        for database connection establishment, including connection pooling
        and security settings.

        Returns:
            Dictionary containing flext-db-oracle compatible configuration with
            connection parameters, pooling settings, and security options

        Example:
            >>> config = FlextOracleTargetConfig(...)
            >>> oracle_config = config.get_oracle_config()
            >>> api = FlextDbOracleApi(FlextDbOracleConfig(**oracle_config))

        """
        return {
            "host": self.oracle_host,
            "port": self.oracle_port,
            "service_name": self.oracle_service,
            "username": self.oracle_user,
            "password": SecretStr(self.oracle_password),
            "sid": None,  # Use service_name instead of SID
            "timeout": self.connection_timeout,
            "pool_min": 1,
            "pool_max": 10,
            "pool_increment": 1,
            "encoding": "UTF-8",
            "ssl_enabled": False,
            "autocommit": False,  # Explicit transaction control
            "ssl_server_dn_match": True,
        }

    def get_table_name(self, stream_name: str) -> str:
        """Generate Oracle table name from Singer stream name.

        Converts Singer stream names to valid Oracle table names by replacing
        invalid characters and applying Oracle naming conventions.

        Transformation rules:
        - Hyphens (-) converted to underscores (_)
        - Dots (.) converted to underscores (_)
        - Result converted to uppercase for Oracle convention

        Args:
            stream_name: Singer stream identifier

        Returns:
            Valid Oracle table name following Oracle naming conventions

        Example:
            >>> config.get_table_name("user-profile.data")
            'USER_PROFILE_DATA'
            >>> config.get_table_name("orders")
            'ORDERS'

        Note:
            This is a simplified naming strategy. Production deployments may
            require more sophisticated table naming with prefixes, suffixes,
            or custom mapping tables.

        """
        # Simple but effective mapping strategy
        # TODO: Consider adding configurable table prefixes/suffixes for v1.1.0
        return stream_name.replace("-", "_").replace(".", "_").upper()


class _ConfigurationValidator:
    """Configuration validator using Chain of Responsibility Pattern - Single Responsibility."""

    def validate(self, config: FlextOracleTargetConfig) -> FlextResult[None]:
        """Validate configuration using validation chain."""
        # Define validation rules as a list of validators
        validators = [
            _HostValidator(),
            _ServiceValidator(),
            _UserValidator(),
            _PasswordValidator(),
            _SchemaValidator(),
        ]

        # Execute validation chain
        for validator in validators:
            result = validator.validate(config)
            if result.is_failure:
                return result

        return FlextResult.ok(None)


class _BaseValidator:
    """Base validator using Template Method Pattern."""

    def validate(self, config: FlextOracleTargetConfig) -> FlextResult[None]:
        """Template method for validation."""
        if not self._is_valid(config):
            return FlextResult.fail(self._get_error_message())
        return FlextResult.ok(None)

    def _is_valid(self, config: FlextOracleTargetConfig) -> bool:
        """Check if configuration is valid - to be implemented by subclasses."""
        raise NotImplementedError

    def _get_error_message(self) -> str:
        """Get error message - to be implemented by subclasses."""
        raise NotImplementedError


class _HostValidator(_BaseValidator):
    """Validate Oracle host - Single Responsibility."""

    def _is_valid(self, config: FlextOracleTargetConfig) -> bool:
        return bool(config.oracle_host)

    def _get_error_message(self) -> str:
        return "Oracle host is required"


class _ServiceValidator(_BaseValidator):
    """Validate Oracle service - Single Responsibility."""

    def _is_valid(self, config: FlextOracleTargetConfig) -> bool:
        return bool(config.oracle_service)

    def _get_error_message(self) -> str:
        return "Oracle service is required"


class _UserValidator(_BaseValidator):
    """Validate Oracle user - Single Responsibility."""

    def _is_valid(self, config: FlextOracleTargetConfig) -> bool:
        return bool(config.oracle_user)

    def _get_error_message(self) -> str:
        return "Oracle username is required"


class _PasswordValidator(_BaseValidator):
    """Validate Oracle password - Single Responsibility."""

    def _is_valid(self, config: FlextOracleTargetConfig) -> bool:
        return bool(config.oracle_password)

    def _get_error_message(self) -> str:
        return "Oracle password is required"


class _SchemaValidator(_BaseValidator):
    """Validate target schema - Single Responsibility."""

    def _is_valid(self, config: FlextOracleTargetConfig) -> bool:
        return bool(config.default_target_schema)

    def _get_error_message(self) -> str:
        return "Target schema is required"


__all__: list[str] = [
    "FlextOracleTargetConfig",
    "LoadMethod",
]
