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

logger = FlextLogger(__name__)
LoadMethod = c.LoadMethod


class FlextTargetOracleSettings(FlextSettings):
    """Runtime settings for Oracle Singer target operations."""

    oracle_host: str = Field(default="localhost", description="Oracle database host")
    oracle_port: int = Field(default=1521, description="Oracle database port")
    oracle_service_name: str = Field(
        default="ORCL", description="Oracle service name or SID"
    )
    oracle_user: SecretStr = Field(description="Oracle database username")
    oracle_password: SecretStr = Field(description="Oracle database password")
    default_target_schema: str = Field(
        default="public", description="Default target schema for data loading"
    )
    batch_size: int = Field(
        default=1000, ge=1, description="Batch size for data loading"
    )
    use_bulk_operations: bool = Field(
        default=False, description="Use bulk operations for faster loading"
    )
    autocommit: bool = Field(default=True, description="Auto-commit transactions")

    def get_table_name(self, stream_name: str) -> str:
        """Get table name from stream name."""
        return stream_name.replace("-", "_").lower()

    def validate_business_rules(self) -> FlextResult[bool]:
        """Validate Oracle target configuration business rules."""
        if not self.oracle_host:
            return FlextResult[bool].fail("Oracle host is required")
        if not self.oracle_service_name:
            return FlextResult[bool].fail("Oracle service name is required")
        if not self.default_target_schema:
            return FlextResult[bool].fail("Default target schema is required")
        return FlextResult[bool].ok(True)


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
