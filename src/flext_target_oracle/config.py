"""Oracle Target Configuration - Simple and clean.

Uses flext-core patterns for configuration management.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from flext_core import FlextResult, FlextValueObject


class LoadMethod(StrEnum):
    """Oracle load methods."""

    APPEND_ONLY = "append-only"
    UPSERT = "upsert"
    TRUNCATE_INSERT = "truncate-insert"


class FlextOracleTargetConfig(FlextValueObject):
    """Oracle target configuration using flext-core patterns."""

    # Oracle connection settings
    oracle_host: str
    oracle_port: int = 1521
    oracle_service_name: str | None = None
    oracle_sid: str | None = None
    oracle_username: str
    oracle_password: str
    oracle_protocol: str = "tcp"
    oracle_pool_min_size: int = 1
    oracle_pool_max_size: int = 2

    # Target settings
    default_target_schema: str = "SINGER_DATA"
    table_prefix: str = ""
    batch_size: int = 1000
    max_parallel_streams: int = 1
    load_method: LoadMethod = LoadMethod.APPEND_ONLY
    use_bulk_operations: bool = True

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate Oracle configuration rules."""
        # Validate Oracle connection
        if not self.oracle_host:
            return FlextResult.fail("Oracle host is required")

        if not (1 <= self.oracle_port <= 65535):
            return FlextResult.fail("Oracle port must be between 1 and 65535")

        if not self.oracle_username:
            return FlextResult.fail("Oracle username is required")

        if not self.oracle_password:
            return FlextResult.fail("Oracle password is required")

        if not self.oracle_service_name and not self.oracle_sid:
            return FlextResult.fail("Either service_name or sid is required")

        # Validate target settings
        if self.batch_size <= 0:
            return FlextResult.fail("Batch size must be positive")

        if self.max_parallel_streams <= 0:
            return FlextResult.fail("Max parallel streams must be positive")

        return FlextResult.ok(None)

    def get_oracle_config(self) -> dict[str, Any]:
        """Get Oracle connection configuration."""
        return {
            "host": self.oracle_host,
            "port": self.oracle_port,
            "service_name": self.oracle_service_name,
            "sid": self.oracle_sid,
            "username": self.oracle_username,
            "password": self.oracle_password,
            "protocol": self.oracle_protocol,
            "pool_min_size": self.oracle_pool_min_size,
            "pool_max_size": self.oracle_pool_max_size,
        }

    def get_table_name(self, stream_name: str) -> str:
        """Generate table name from stream name."""
        # Clean stream name
        clean_name = stream_name.upper().replace("-", "_").replace(".", "_")

        # Add prefix if configured
        if self.table_prefix:
            return f"{self.table_prefix}{clean_name}"

        return clean_name

    def get_raw_config(self) -> dict[str, Any]:
        """Get raw configuration as dict for compatibility with flext-meltano."""
        return {
            "host": self.oracle_host,
            "port": self.oracle_port,
            "service_name": self.oracle_service_name,
            "sid": self.oracle_sid,
            "username": self.oracle_username,
            "password": self.oracle_password,
            "protocol": self.oracle_protocol,
            "pool_min_size": self.oracle_pool_min_size,
            "pool_max_size": self.oracle_pool_max_size,
            "default_target_schema": self.default_target_schema,
            "table_prefix": self.table_prefix,
            "batch_size": self.batch_size,
            "max_parallel_streams": self.max_parallel_streams,
            "load_method": self.load_method.value
            if self.load_method
            else "append-only",
        }
