"""Configuration classes for FLEXT Target Oracle using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final

from flext_core import FlextResult, FlextValueObject
from pydantic import Field, SecretStr, field_validator


# Constants to eliminate magic numbers - SOLID DRY principle
class OracleTargetConstants:
    """Oracle Target configuration constants."""

    DEFAULT_PORT: Final = 1521
    DEFAULT_BATCH_SIZE: Final = 1000
    DEFAULT_CONNECTION_TIMEOUT: Final = 30
    DEFAULT_MAX_PARALLEL_STREAMS: Final = 4
    MIN_PORT: Final = 1
    MAX_PORT: Final = 65535


class LoadMethod(StrEnum):
    """Oracle load methods."""

    INSERT = "insert"
    MERGE = "merge"
    BULK_INSERT = "bulk_insert"
    BULK_MERGE = "bulk_merge"


class FlextOracleTargetConfig(FlextValueObject):
    """Configuration for FLEXT Target Oracle using flext-core patterns."""

    oracle_host: str = Field(..., description="Oracle host")
    oracle_port: int = Field(
        default=OracleTargetConstants.DEFAULT_PORT,
        description="Oracle port",
    )
    oracle_service: str = Field(..., description="Oracle service name")
    oracle_user: str = Field(..., description="Oracle username")
    oracle_password: str = Field(..., description="Oracle password")
    default_target_schema: str = Field(
        default="target",
        description="Default target schema",
    )
    load_method: LoadMethod = Field(
        default=LoadMethod.INSERT,
        description="Load method",
    )
    use_bulk_operations: bool = Field(default=True, description="Use bulk operations")
    batch_size: int = Field(
        default=OracleTargetConstants.DEFAULT_BATCH_SIZE,
        description="Batch size for operations",
    )
    connection_timeout: int = Field(
        default=OracleTargetConstants.DEFAULT_CONNECTION_TIMEOUT,
        description="Connection timeout in seconds",
    )

    @field_validator("oracle_port")
    @classmethod
    def validate_oracle_port(cls, v: int) -> int:
        """Validate Oracle port is in valid range."""
        if not (OracleTargetConstants.MIN_PORT <= v <= OracleTargetConstants.MAX_PORT):
            msg = f"Oracle port must be between {OracleTargetConstants.MIN_PORT} and {OracleTargetConstants.MAX_PORT}"
            raise ValueError(msg)
        return v

    @field_validator("batch_size")
    @classmethod
    def validate_batch_size(cls, v: int) -> int:
        """Validate batch size is positive."""
        if v <= 0:
            msg = "Batch size must be positive"
            raise ValueError(msg)
        return v

    @field_validator("connection_timeout")
    @classmethod
    def validate_connection_timeout(cls, v: int) -> int:
        """Validate connection timeout is positive."""
        if v <= 0:
            msg = "Connection timeout must be positive"
            raise ValueError(msg)
        return v

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate domain-specific business rules using Chain of Responsibility Pattern."""
        try:
            # Use validation chain to eliminate multiple returns
            validator = _ConfigurationValidator()
            return validator.validate(self)
        except Exception as e:
            return FlextResult.fail(f"Configuration validation failed: {e}")

    def get_oracle_config(self) -> dict[str, str | int | SecretStr | None | bool]:
        """Get Oracle configuration for flext-db-oracle with proper types."""
        return {
            "host": self.oracle_host,
            "port": self.oracle_port,
            "service_name": self.oracle_service,
            "username": self.oracle_user,
            "password": SecretStr(self.oracle_password),
            "sid": None,  # Required field
            "timeout": self.connection_timeout,
            "pool_min": 1,
            "pool_max": 10,
            "pool_increment": 1,
            "encoding": "UTF-8",
            "ssl_enabled": False,
            # Additional required fields for extended config
            "autocommit": False,
            "ssl_server_dn_match": True,
        }

    def get_table_name(self, stream_name: str) -> str:
        """Get table name for a stream."""
        # Simple mapping - could be enhanced with custom table naming
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


__all__ = [
    "FlextOracleTargetConfig",
    "LoadMethod",
]
