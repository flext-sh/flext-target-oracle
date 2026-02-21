"""Target Models for FLEXT Target Oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import UTC, datetime

from flext_core import FlextModels, FlextResult
from pydantic import BaseModel, Field, field_validator

from flext_target_oracle.constants import c

# Oracle schema constants
PUBLIC = "PUBLIC"


# LoadMethodModel moved to constants.py as c.LoadMethod (DRY pattern)
LoadMethodModel = c.LoadMethod

# StorageModeModel moved to constants.py as c.StorageMode (DRY pattern)
StorageModeModel = c.StorageMode


class OracleConnectionModel(BaseModel):
    """Oracle database connection parameters model.

    Immutable value object representing Oracle database connection
    configuration with complete validation for production use.

    Attributes:
    host: Oracle database hostname or IP address
    port: Oracle listener port number (default: 1521)
    service_name: Oracle service name for connection
    username: Oracle database username
    schema: Target schema for table operations (default: PUBLIC)
    use_ssl: Enable SSL/TLS connection (default: False)
    connection_timeout: Connection timeout in seconds (default: 30)

    """

    host: str = Field(
        ...,
        description="Oracle database hostname or IP address",
        min_length=1,
        max_length=255,
    )
    port: int = Field(
        default=1521,
        description="Oracle listener port number",
        ge=1,
        le=65535,
    )
    service_name: str = Field(
        ...,
        description="Oracle service name for connection",
        min_length=1,
        max_length=64,
    )
    username: str = Field(
        ...,
        description="Oracle database username",
        min_length=1,
        max_length=128,
    )
    schema_name: str = Field(
        default=PUBLIC,
        description="Target schema for table operations",
        min_length=1,
        max_length=128,
        alias="schema",
    )
    use_ssl: bool = Field(
        default=False,
        description="Enable SSL/TLS connection",
    )
    connection_timeout: int = Field(
        default=30,
        description="Connection timeout in seconds",
        gt=0,
        le=3600,
    )

    def get_connection_string(self, *, include_credentials: bool = False) -> str:
        """Generate Oracle connection string.

        Args:
        include_credentials: Whether to include username in connection string

        Returns:
        Oracle connection string for logging and diagnostics

        """
        protocol = "tcps" if self.use_ssl else "tcp"

        if include_credentials:
            return f"{protocol}://{self.username}@{self.host}:{self.port}/{self.service_name}"
        return f"{protocol}://{self.host}:{self.port}/{self.service_name}"

    def validate_business_rules(self) -> FlextResult[bool]:
        """Validate Oracle connection business rules."""
        # Validate host is reachable format
        if not self.host or self.host.isspace():
            return FlextResult[bool].fail("Host cannot be empty or whitespace")

        # Validate service name format
        if not self.service_name or self.service_name.isspace():
            return FlextResult[bool].fail("Service name cannot be empty or whitespace")

        # Validate username
        if not self.username or self.username.isspace():
            return FlextResult[bool].fail("Username cannot be empty or whitespace")

        return FlextResult[bool].ok(value=True)


class SingerStreamModel(FlextModels.ArbitraryTypesModel):
    """Singer stream definition with Oracle mappings.

    Immutable value object representing a Singer stream configuration
    with Oracle-specific table mappings and transformation rules.

    Attributes:
    stream_name: Singer stream identifier
    table_name: Oracle table name (derived or mapped)
    schema_name: Oracle schema name for the table
    key_properties: List of primary key column names
    column_mappings: Column name mappings (singer_name -> oracle_name)
    ignored_columns: List of columns to ignore during loading
    storage_mode: How to store the data (flattened, json, hybrid)
    load_method: Loading strategy for this stream

    """

    stream_name: str = Field(
        ...,
        description="Singer stream identifier",
        min_length=1,
        max_length=128,
    )
    table_name: str = Field(
        ...,
        description="Oracle table name",
        min_length=1,
        max_length=30,  # Oracle table name limit
    )
    schema_name: str = Field(
        ...,
        description="Oracle schema name for the table",
        min_length=1,
        max_length=128,
    )
    key_properties: list[str] = Field(
        default_factory=list,
        description="List of primary key column names",
    )
    column_mappings: dict[str, str] = Field(
        default_factory=dict,
        description="Column name mappings (singer_name -> oracle_name)",
    )
    ignored_columns: list[str] = Field(
        default_factory=list,
        description="List of columns to ignore during loading",
    )
    storage_mode: StorageModeModel = Field(
        default=StorageModeModel.FLATTENED,
        description="How to store the data",
    )
    load_method: LoadMethodModel = Field(
        default=LoadMethodModel.INSERT,
        description="Loading strategy for this stream",
    )

    @field_validator("table_name")
    @classmethod
    def validate_table_name(cls, v: str) -> str:
        """Validate Oracle table name conventions."""
        # Convert to uppercase and ensure Oracle naming conventions
        table_name = v.upper()

        # Replace invalid characters
        table_name = table_name.replace("-", "_").replace(".", "_")

        # Ensure it starts with letter or underscore
        if table_name and not (table_name[0].isalpha() or table_name[0] == "_"):
            table_name = f"T_{table_name}"

        return table_name

    def get_qualified_table_name(self) -> str:
        """Get fully qualified Oracle table name."""
        return f"{self.schema_name}.{self.table_name}"


class LoadStatisticsModel(FlextModels.ArbitraryTypesModel):
    """Data loading statistics and metrics.

    Immutable value object representing complete statistics
    about Oracle data loading operations for monitoring and reporting.

    Attributes:
    stream_name: Singer stream name
    total_records_processed: Total number of records processed
    successful_records: Number of successfully loaded records
    failed_records: Number of failed records
    batches_processed: Number of batches processed
    processing_start_time: When processing started
    processing_end_time: When processing ended (None if ongoing)
    load_method_used: Loading method that was used
    average_batch_size: Average number of records per batch
    throughput_records_per_second: Processing throughput
    error_details: List of error messages encountered

    """

    stream_name: str = Field(
        ...,
        description="Singer stream name",
        min_length=1,
    )
    total_records_processed: int = Field(
        default=0,
        description="Total number of records processed",
        ge=0,
    )
    successful_records: int = Field(
        default=0,
        description="Number of successfully loaded records",
        ge=0,
    )
    failed_records: int = Field(
        default=0,
        description="Number of failed records",
        ge=0,
    )
    batches_processed: int = Field(
        default=0,
        description="Number of batches processed",
        ge=0,
    )
    processing_start_time: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When processing started",
    )
    processing_end_time: datetime | None = Field(
        default=None,
        description="When processing ended (None if ongoing)",
    )
    load_method_used: LoadMethodModel = Field(
        default=LoadMethodModel.INSERT,
        description="Loading method that was used",
    )
    error_details: list[str] = Field(
        default_factory=list,
        description="List of error messages encountered",
    )

    @property
    def is_completed(self) -> bool:
        """Whether processing has completed."""
        return self.processing_end_time is not None

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.total_records_processed == 0:
            return 0.0
        return (self.successful_records / self.total_records_processed) * 100.0

    @property
    def processing_duration_seconds(self) -> float:
        """Calculate processing duration in seconds."""
        end_time = self.processing_end_time or datetime.now(UTC)
        return (end_time - self.processing_start_time).total_seconds()

    @property
    def average_batch_size(self) -> float:
        """Calculate average batch size."""
        if self.batches_processed == 0:
            return 0.0
        return self.total_records_processed / self.batches_processed

    @property
    def throughput_records_per_second(self) -> float:
        """Calculate processing throughput in records per second."""
        duration = self.processing_duration_seconds
        if duration == 0:
            return 0.0
        return self.successful_records / duration

    def finalize(self) -> LoadStatisticsModel:
        """Mark statistics as completed (immutable operation)."""
        return self.model_copy(
            update={
                "processing_end_time": datetime.now(UTC),
            },
        )

    def add_error(self, error_message: str) -> LoadStatisticsModel:
        """Add an error message (immutable operation)."""
        new_errors = self.error_details.copy()
        new_errors.append(error_message)

        return self.model_copy(
            update={
                "error_details": "new_errors",
                "failed_records": self.failed_records + 1,
            },
        )

    def validate_business_rules(self) -> FlextResult[bool]:
        """Validate business rules for load statistics."""
        if not self.stream_name or self.stream_name.isspace():
            return FlextResult[bool].fail("Stream name cannot be empty or whitespace")
        if self.successful_records < 0:
            return FlextResult[bool].fail("Successful records count cannot be negative")
        if self.failed_records < 0:
            return FlextResult[bool].fail("Failed records count cannot be negative")
        if (
            self.total_records_processed
            != self.successful_records + self.failed_records
        ):
            return FlextResult[bool].fail(
                "Total records must equal successful + failed records",
            )
        return FlextResult[bool].ok(value=True)


__all__ = [
    # Enums
    "LoadMethodModel",
    "LoadStatisticsModel",
    # Value Objects
    "OracleConnectionModel",
    "SingerStreamModel",
    "StorageModeModel",
]
