"""Configuration models with validation.

These models ensure configuration is valid and type-safe,
using Pydantic for automatic validation and serialization.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, SecretStr, field_validator


class LoadMethod(str, Enum):
    """Supported load methods."""

    APPEND_ONLY = "append-only"
    OVERWRITE = "overwrite"
    UPSERT = "upsert"


class CompressionType(str, Enum):
    """Oracle compression types."""

    NONE = "none"
    BASIC = "basic"
    ADVANCED = "advanced"
    QUERY_HIGH = "query_high"
    QUERY_LOW = "query_low"
    ARCHIVE_HIGH = "archive_high"
    ARCHIVE_LOW = "archive_low"


class OracleConfig(BaseModel):
    """Oracle connection configuration."""

    # Connection parameters
    host: str = Field(..., description="Oracle database host")
    port: int = Field(1521, description="Oracle database port")
    service_name: str = Field(..., description="Oracle service name")
    user: str = Field(..., description="Database user")
    password: SecretStr = Field(..., description="Database password")

    # Schema configuration
    default_target_schema: str | None = Field(None, description="Default schema for tables")

    # License compliance
    oracle_is_enterprise_edition: bool = Field(False, description="Using Enterprise Edition")
    oracle_has_partitioning: bool = Field(False, description="Has partitioning option")
    oracle_has_advanced_compression: bool = Field(False, description="Has advanced compression")

    # Connection pool settings
    pool_size: int = Field(10, ge=1, le=50, description="Connection pool size")
    pool_max_overflow: int = Field(10, ge=0, le=50, description="Max overflow connections")
    pool_timeout: int = Field(30, ge=1, description="Pool timeout in seconds")

    # Operation settings
    load_method: LoadMethod = Field(LoadMethod.APPEND_ONLY, description="Data load method")
    batch_size_rows: int = Field(50000, ge=1000, le=1000000, description="Batch size")

    model_config = {
        "frozen": True,  # Make immutable
        "use_enum_values": True,
    }

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        """Validate port is in valid range."""
        if not 1 <= v <= 65535:
            raise ValueError(f"Port must be between 1 and 65535, got {v}")
        return v


class PerformanceConfig(BaseModel):
    """Performance optimization configuration."""

    # Parallel processing
    parallel_threads: int = Field(8, ge=1, le=32, description="Parallel processing threads")
    use_direct_path: bool = Field(True, description="Use direct path loading")

    # Compression
    compression_type: CompressionType = Field(CompressionType.NONE, description="Compression type")

    # Memory settings
    in_memory: bool = Field(False, description="Use in-memory column store")
    in_memory_priority: str = Field("none", description="In-memory priority")

    # Performance hints
    enable_parallel_dml: bool = Field(False, description="Enable parallel DML")
    append_values_hint: bool = Field(True, description="Use APPEND_VALUES hint")
    nologging: bool = Field(False, description="Use NOLOGGING mode")

    model_config = {
        "frozen": True,
        "use_enum_values": True,
    }


class ValidationResult(BaseModel):
    """Result of a validation operation."""

    is_valid: bool = Field(..., description="Whether validation passed")
    errors: list[str] = Field(default_factory=list, description="Validation errors")
    warnings: list[str] = Field(default_factory=list, description="Validation warnings")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    model_config = {
        "frozen": True,
    }

    @classmethod
    def success(cls) -> ValidationResult:
        """Create a successful validation result."""
        return cls(is_valid=True)

    @classmethod
    def failure(cls, errors: list[str], warnings: list[str] | None = None) -> ValidationResult:
        """Create a failed validation result."""
        return cls(
            is_valid=False,
            errors=errors,
            warnings=warnings or [],
        )
