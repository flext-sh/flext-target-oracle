"""Singer Target Domain Models.

Following flext-core DDD patterns for Singer-specific entities.
"""

from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING, Any, ClassVar
from uuid import uuid4

from flext_core.domain import (
    FlextEntity as DomainEntity,
    FlextValueObject,
    FlextValueObject as FlextDomainBaseModel,
)
from pydantic import ConfigDict, Field, field_validator, model_validator

from flext_target_oracle.exceptions import (
    FlextOracleTargetSchemaError,
    FlextOracleTargetSingerRecordError,
)

if TYPE_CHECKING:
    from datetime import datetime


class LoadMethod(StrEnum):
    """Data loading strategy."""

    APPEND_ONLY = "append-only"
    UPSERT = "upsert"
    OVERWRITE = "overwrite"


class SingerSchema(FlextValueObject):
    """Singer schema definition."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        extra="forbid",  # No backward compatibility
        frozen=True,  # Immutable value object
        validate_assignment=True,
    )

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

    def validate_domain_rules(self) -> None:
        """Validate Singer schema domain rules."""
        if not self.type:
            raise FlextOracleTargetSchemaError(
                schema_name="unknown",
                message="Schema type is required",
                schema_data=self.model_dump(),
            )

        if self.type not in {
            "object",
            "array",
            "string",
            "number",
            "integer",
            "boolean",
            "null",
        }:
            raise FlextOracleTargetSchemaError(
                schema_name="unknown",
                message=f"Invalid schema type: {self.type}",
                schema_data=self.model_dump(),
            )

        if self.type == "object" and not isinstance(self.properties, dict):
            raise FlextOracleTargetSchemaError(
                schema_name="unknown",
                message="Properties must be a dictionary for object type schemas",
                schema_data=self.model_dump(),
            )

        # Validate key_properties are in properties
        if self.key_properties and self.properties:
            for key_prop in self.key_properties:
                if key_prop not in self.properties:
                    raise FlextOracleTargetSchemaError(
                        schema_name="unknown",
                        message=f"Key property '{key_prop}' not found in schema properties",
                        schema_data=self.model_dump(),
                    )


class SingerRecord(FlextValueObject):
    """Singer record data."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        extra="forbid",  # No backward compatibility
        frozen=True,  # Immutable value object
        validate_assignment=True,
    )

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
            raise FlextOracleTargetSingerRecordError(
                record_type=str(v),
                message=msg,
                record_data={"type": v},
            )
        return v

    def validate_domain_rules(self) -> None:
        """Validate Singer record domain rules."""
        if not self.type:
            raise FlextOracleTargetSingerRecordError(
                record_type="unknown",
                message="Record type is required",
                record_data=self.model_dump(),
            )

        # Validate type-specific requirements
        if self.type == "RECORD":
            if not self.stream:
                msg = "Stream name is required for RECORD type"
                raise ValueError(msg)
            if self.record is None:
                msg = "Record data is required for RECORD type"
                raise ValueError(msg)
        elif self.type == "SCHEMA":
            if not self.stream:
                msg = "Stream name is required for SCHEMA type"
                raise ValueError(msg)
            if not self.record_schema:
                msg = "Schema definition is required for SCHEMA type"
                raise ValueError(msg)


class FlextTargetOracleConfig(FlextDomainBaseModel):
    """Target configuration combining Oracle and Singer settings."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        extra="forbid",  # Strict validation - no extra fields
        frozen=False,  # Allow mutations during validation
        validate_assignment=True,
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
    def validate_service_or_sid(self) -> FlextTargetOracleConfig:
        """Ensure either service_name or sid is provided."""
        if not self.service_name and not self.sid:
            msg = "Either service_name or sid must be provided"
            raise ValueError(msg)
        return self

    @property
    def oracle_config(self) -> dict[str, Any]:
        """Get Oracle configuration for flext-db-oracle."""
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

    def validate_domain_rules(self) -> None:
        """Validate Oracle target configuration domain rules."""
        # Validate Oracle connection parameters
        if not self.host:
            msg = "Oracle host is required"
            raise ValueError(msg)

        if not (1 <= self.port <= 65535):
            msg = f"Invalid Oracle port: {self.port}"
            raise ValueError(msg)

        if not self.username:
            msg = "Oracle username is required"
            raise ValueError(msg)

        if not self.password:
            msg = "Oracle password is required"
            raise ValueError(msg)

        # Validate performance settings
        if self.batch_size <= 0:
            msg = "Batch size must be positive"
            raise ValueError(msg)

        if self.max_parallelism <= 0:
            msg = "Max parallelism must be positive"
            raise ValueError(msg)

    def to_connection_config(self) -> dict[str, Any]:
        """Convert to connection config for flext-db-oracle.

        Returns:
            Dictionary with connection parameters

        """
        return {
            "host": self.host,
            "port": self.port,
            "service_name": self.service_name,
            "sid": self.sid,
            "username": self.username,
            "password": self.password,
        }


# Compatibility alias
TargetConfig = FlextTargetOracleConfig


class LoadJobStatus(StrEnum):
    """Load job status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class LoadJob(DomainEntity):
    """Data loading job entity."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        frozen=False,  # Allow field mutations
        validate_assignment=True,
    )

    id: str = Field(default_factory=lambda: str(uuid4()))
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

    def validate_domain_rules(self) -> None:
        """Validate load job domain rules."""
        if not self.stream_name:
            msg = "Stream name is required"
            raise ValueError(msg)
        if not self.table_name:
            msg = "Table name is required"
            raise ValueError(msg)
        if self.records_processed < 0:
            msg = "Records processed cannot be negative"
            raise ValueError(msg)
        if self.records_failed < 0:
            msg = "Records failed cannot be negative"
            raise ValueError(msg)

        # Validate status consistency
        if self.status == LoadJobStatus.COMPLETED and self.completed_at is None:
            msg = "Completed jobs must have completion time"
            raise ValueError(msg)
        if (
            self.status in {LoadJobStatus.RUNNING, LoadJobStatus.COMPLETED}
            and self.started_at is None
        ):
            msg = "Running/completed jobs must have start time"
            raise ValueError(msg)


class LoadStatistics(FlextDomainBaseModel):
    """Load operation statistics."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        frozen=False,  # Allow field mutations
        validate_assignment=True,
    )

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

    def validate_domain_rules(self) -> None:
        """Validate load statistics domain rules."""
        if self.total_records < 0:
            msg = "Total records cannot be negative"
            raise ValueError(msg)
        if self.successful_records < 0:
            msg = "Successful records cannot be negative"
            raise ValueError(msg)
        if self.failed_records < 0:
            msg = "Failed records cannot be negative"
            raise ValueError(msg)
        if self.total_batches < 0:
            msg = "Total batches cannot be negative"
            raise ValueError(msg)
        if self.duration_seconds < 0:
            msg = "Duration cannot be negative"
            raise ValueError(msg)
        if self.records_per_second < 0:
            msg = "Records per second cannot be negative"
            raise ValueError(msg)

        # Validate consistency
        if self.successful_records + self.failed_records != self.total_records:
            msg = "Successful + failed records must equal total records"
            raise ValueError(msg)


# Rebuild models after imports are resolved
SingerRecord.model_rebuild()
LoadJob.model_rebuild()
