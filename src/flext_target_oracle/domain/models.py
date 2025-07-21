"""Singer Target Domain Models.

Following flext-core DDD patterns for Singer-specific entities.
"""

from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING, Any, ClassVar
from uuid import uuid4

from flext_core import DomainBaseModel, DomainEntity, DomainValueObject, EntityId
from pydantic import ConfigDict, Field, field_validator, model_validator

if TYPE_CHECKING:
    from datetime import datetime
else:
    # Import datetime for runtime to fix Pydantic model_rebuild issue
    pass


class LoadMethod(StrEnum):
    """Data loading strategy."""

    APPEND_ONLY = "append-only"
    UPSERT = "upsert"
    OVERWRITE = "overwrite"


class SingerSchema(DomainValueObject):
    """Singer schema definition."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        extra="allow",
    )  # Allow extra fields like additionalProperties

    type: str = Field("object", description="Schema type")
    properties: dict[str, Any] = Field(
        default_factory=dict,
        description="Schema properties",
    )
    key_properties: list[str] = Field(
        default_factory=list,
        description="Primary key fields",
    )
    required: list[str] = Field(default_factory=list, description="Required fields")

    @property
    def table_name(self) -> str:
        """Extract table name from schema."""
        table_name = self.properties.get("table_name")
        return table_name if isinstance(table_name, str) else "unknown_table"


class SingerRecord(DomainValueObject):
    """Singer record data."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        extra="allow",
    )  # Allow extra fields like key_properties

    type: str = Field(..., description="Record type (RECORD, SCHEMA, STATE)")
    stream: str | None = Field(None, description="Stream name")
    record: dict[str, Any] | None = Field(None, description="Record data")
    record_schema: dict[str, Any] | None = Field(
        None,
        alias="schema",
        description="Schema definition",
    )
    time_extracted: datetime | None = Field(None, description="Extraction timestamp")

    @field_validator("type")
    @classmethod
    def validate_record_type(cls, v: str) -> str:
        """Validate record type."""
        valid_types = {"RECORD", "SCHEMA", "STATE"}
        if v not in valid_types:
            msg = f"Invalid record type '{v}'. Must be one of {valid_types}"
            raise ValueError(msg)
        return v


class TargetConfig(DomainBaseModel):
    """Target configuration combining Oracle and Singer settings."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        extra="allow",  # Allow extra fields for backward compatibility
    )

    # Oracle connection (delegate to flext-infrastructure.databases.flext-db-oracle)
    host: str = Field(..., description="Oracle host")
    port: int = Field(1521, description="Oracle port")
    service_name: str | None = Field(None, description="Oracle service name")
    sid: str | None = Field(None, description="Oracle SID")
    username: str = Field(..., description="Oracle username")
    password: str = Field(..., description="Oracle password")
    protocol: str = Field("tcp", description="Connection protocol (tcp or tcps)")

    # Target-specific settings
    default_target_schema: str = Field(
        "SINGER_DATA",
        description="Default schema for tables",
    )
    table_prefix: str = Field("", description="Prefix for all target tables")
    load_method: LoadMethod = Field(
        LoadMethod.APPEND_ONLY,
        description="Data loading strategy",
    )
    batch_size: int = Field(10000, ge=1, description="Records per batch")
    max_parallelism: int = Field(4, ge=1, description="Maximum parallel streams")

    # Performance settings
    use_bulk_operations: bool = Field(
        default=True,
        description="Enable Oracle bulk operations",
    )
    compression: bool = Field(default=False, description="Enable Oracle compression")
    parallel_degree: int = Field(
        1,
        ge=1,
        le=64,
        description="Oracle parallel processing degree",
    )

    @model_validator(mode="after")
    def validate_service_or_sid(self) -> TargetConfig:
        """Ensure either service_name or sid is provided."""
        if not self.service_name and not self.sid:
            # For backward compatibility, provide default service name
            self.service_name = "XEPDB1"  # Default Oracle Express service
        return self

    @property
    def oracle_config(self) -> dict[str, Any]:
        """Get Oracle configuration for flext-infrastructure.databases.flext-db-oracle."""
        return {
            "host": self.host,
            "port": self.port,
            "service_name": self.service_name,
            "sid": self.sid,
            "username": self.username,
            "password": self.password,
            "protocol": self.protocol,
            "pool_min_size": 1,
            "pool_max_size": self.max_parallelism,
        }


class LoadJobStatus(StrEnum):
    """Load job status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class LoadJob(DomainEntity):
    """Data loading job entity."""

    id: EntityId = Field(default_factory=uuid4)
    stream_name: str = Field(..., description="Singer stream name")
    table_name: str = Field(..., description="Target table name")
    status: LoadJobStatus = Field(
        default=LoadJobStatus.PENDING,
        description="Job status",
    )
    records_processed: int = Field(default=0, ge=0, description="Records processed")
    records_failed: int = Field(default=0, ge=0, description="Records failed")
    started_at: datetime | None = Field(default=None, description="Job start time")
    completed_at: datetime | None = Field(
        default=None,
        description="Job completion time",
    )
    error_message: str | None = Field(
        default=None,
        description="Error message if failed",
    )

    @property
    def is_running(self) -> bool:
        """Check if job is currently running."""
        return self.status == LoadJobStatus.RUNNING

    @property
    def is_completed(self) -> bool:
        """Check if job completed successfully."""
        return self.status == LoadJobStatus.COMPLETED

    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage."""
        total = self.records_processed + self.records_failed
        if total == 0:
            return 0.0
        return (self.records_processed / total) * 100.0


class LoadStatistics(DomainBaseModel):
    """Load operation statistics."""

    total_records: int = Field(default=0, ge=0, description="Total records processed")
    successful_records: int = Field(
        default=0,
        ge=0,
        description="Successfully loaded records",
    )
    failed_records: int = Field(default=0, ge=0, description="Failed records")
    total_batches: int = Field(default=0, ge=0, description="Total batches processed")
    duration_seconds: float = Field(
        default=0.0,
        ge=0,
        description="Total duration in seconds",
    )
    records_per_second: float = Field(default=0.0, ge=0, description="Processing rate")

    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage."""
        if self.total_records == 0:
            return 0.0
        return (self.successful_records / self.total_records) * 100.0


# Rebuild models after imports are resolved
SingerRecord.model_rebuild()
LoadJob.model_rebuild()
