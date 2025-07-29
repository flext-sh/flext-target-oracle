"""Configuration classes for FLEXT Target Oracle using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from flext_core import FlextResult, FlextValueObject
from pydantic import Field, field_validator


class LoadMethod(StrEnum):
    """Oracle load methods."""

    INSERT = "insert"
    MERGE = "merge"
    BULK_INSERT = "bulk_insert"
    BULK_MERGE = "bulk_merge"


class FlextOracleTargetConfig(FlextValueObject):
    """Configuration for FLEXT Target Oracle using flext-core patterns."""

    oracle_host: str = Field(..., description="Oracle host")
    oracle_port: int = Field(default=1521, description="Oracle port")
    oracle_service: str = Field(..., description="Oracle service name")
    oracle_user: str = Field(..., description="Oracle username")
    oracle_password: str = Field(..., description="Oracle password")
    default_target_schema: str = Field(default="target", description="Default target schema")
    load_method: LoadMethod = Field(default=LoadMethod.INSERT, description="Load method")
    use_bulk_operations: bool = Field(default=True, description="Use bulk operations")
    batch_size: int = Field(default=1000, description="Batch size for operations")
    connection_timeout: int = Field(default=30, description="Connection timeout in seconds")

    @field_validator("oracle_port")
    @classmethod
    def validate_oracle_port(cls, v: int) -> int:
        """Validate Oracle port is in valid range."""
        if not (1 <= v <= 65535):
            msg = "Oracle port must be between 1 and 65535"
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
        """Validate domain-specific business rules."""
        try:
            # Validate required connection fields
            if not self.oracle_host:
                return FlextResult.fail("Oracle host is required")

            if not self.oracle_service:
                return FlextResult.fail("Oracle service is required")

            if not self.oracle_user:
                return FlextResult.fail("Oracle username is required")

            if not self.oracle_password:
                return FlextResult.fail("Oracle password is required")

            # Validate schema name
            if not self.default_target_schema:
                return FlextResult.fail("Target schema is required")

            return FlextResult.ok(None)
        except Exception as e:
            return FlextResult.fail(f"Configuration validation failed: {e}")

    def get_oracle_config(self) -> dict[str, Any]:
        """Get Oracle configuration for flext-db-oracle."""
        return {
            "host": self.oracle_host,
            "port": self.oracle_port,
            "service": self.oracle_service,
            "user": self.oracle_user,
            "password": self.oracle_password,
            "connection_timeout": self.connection_timeout,
        }

    def get_table_name(self, stream_name: str) -> str:
        """Get table name for a stream."""
        # Simple mapping - could be enhanced with custom table naming
        return stream_name.replace("-", "_").replace(".", "_").upper()


__all__ = [
    "FlextOracleTargetConfig",
    "LoadMethod",
]
