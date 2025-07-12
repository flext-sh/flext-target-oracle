"""Configuration for target-oracle using flext-core patterns.

REFACTORED:
            Uses flext-core SingerTargetConfig with structured value objects.  Zero tolerance for code duplication.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import ConfigDict, Field, field_validator, model_validator

from flext_core.config.adapters.singer import SingerTargetConfig
from flext_core.domain.pydantic_base import DomainValueObject


class OracleConnectionConfig(DomainValueObject):
    """Oracle database connection configuration value object."""

    host: str | None = Field(
        None,
        description="Oracle database host",
    )
    port: int = Field(
        1521,
        description="Oracle database port",
        ge=1,
        le=65535,
    )
    service_name: str | None = Field(
        None,
        description="Oracle service name",
    )
    database: str | None = Field(
        None,
        description="Oracle database name (SID)",
    )
    dsn: str | None = Field(
        None,
        description="Full DSN connection string",
    )
    username: str = Field(
        ...,
        description="Database username",
    )
    password: str = Field(
        ...,
        description="Database password",
        json_schema_extra={"secret": True},
    )
    target_schema: str | None = Field(
        None,
        alias="schema",
        description="Target schema (defaults to username)",
    )
    protocol: str = Field(
        "tcp",
        description="Connection protocol (tcp, tcps)",
        pattern="^(tcp|tcps)$",
    )
    wallet_location: str | None = Field(
        None,
        description="Oracle wallet directory for secure connections",
    )
    wallet_password: str | None = Field(
        None,
        description="Oracle wallet password",
        json_schema_extra={"secret": True},
    )

    @property
    def effective_schema(self) -> str:
        """Get the effective schema name.

        Returns:
            The schema name or username if schema is not specified.

        """
        return self.target_schema or self.username

    @field_validator("wallet_location")
    @classmethod
    def validate_wallet_path(cls, v: str | None) -> str | None:
        """Validate Oracle wallet location path.

        Args:
            v: Wallet location path to validate.

        Returns:
            Validated wallet location path.

        Raises:
            ValueError: If wallet directory does not exist.

        """
        if v:
            path = Path(v)
            if not path.exists():
                msg = f"Wallet directory does not exist: {v}"
                raise ValueError(msg)
        return v


class OraclePerformanceConfig(DomainValueObject):
    """Oracle performance and optimization configuration value object."""

    batch_size: int = Field(
        10000,
        description="Records per batch",
        ge=100,
        le=100000,
    )
    pool_size: int = Field(
        10,
        description="Connection pool size",
        ge=1,
        le=100,
    )
    max_overflow: int = Field(
        20,
        description="Maximum overflow connections",
        ge=0,
        le=100,
    )
    pool_timeout: float = Field(
        30.0,
        description="Connection pool timeout in seconds",
        ge=1.0,
        le=300.0,
    )
    use_bulk_operations: bool = Field(
        default=True,
        description="Use Oracle bulk operations",
    )
    use_merge_statements: bool = Field(
        default=True,
        description="Use MERGE for upserts",
    )
    parallel_degree: int = Field(
        1,
        description="Oracle parallel DML degree",
        ge=1,
        le=32,
    )
    array_size: int = Field(
        1000,
        description="Oracle array fetch size",
        ge=50,
        le=10000,
    )
    commit_interval: int = Field(
        10000,
        description="Records between commits",
        ge=100,
    )


class OracleTableConfig(DomainValueObject):
    """Oracle table creation and management configuration value object."""

    load_method: str = Field(
        "append-only",
        description="Load method: append-only, upsert, overwrite",
        pattern="^(append-only|upsert|overwrite)$",
    )
    table_prefix: str = Field(
        "",
        description="Prefix for created tables",
    )
    create_indexes: bool = Field(
        default=True,
        description="Create indexes on primary keys",
    )
    enable_compression: bool = Field(
        default=False,
        description="Enable Oracle table compression",
    )
    compression_type: str = Field(
        "basic",
        description="Compression type: basic, advanced, hybrid",
        pattern="^(basic|advanced|hybrid)$",
    )
    add_metadata_columns: bool = Field(
        default=True,
        description="Add Singer metadata columns",
    )
    enable_partitioning: bool = Field(
        default=False,
        description="Enable Oracle table partitioning",
    )
    partition_key: str | None = Field(
        None,
        description="Column to use for partitioning",
    )
    tablespace: str | None = Field(
        None,
        description="Oracle tablespace for tables",
    )


class OracleSchemaConfig(DomainValueObject):
    """Oracle schema management configuration value object."""

    create_tables: bool = Field(
        default=True,
        description="Automatically create missing tables",
    )
    drop_existing_tables: bool = Field(
        default=False,
        description="Drop existing tables before creating",
    )
    alter_existing_tables: bool = Field(
        default=True,
        description="Alter tables to add missing columns",
    )
    preserve_source_schema: bool = Field(
        default=False,
        description="Preserve source schema structure",
    )


class OracleProcessingConfig(DomainValueObject):
    """Oracle data processing configuration value object."""

    validate_records: bool = Field(
        default=True,
        description="Validate records before loading",
    )
    validation_strict_mode: bool = Field(
        default=False,
        description="Fail on validation errors (vs. warnings)",
    )
    max_errors: int = Field(
        10,
        description="Maximum errors before stopping",
        ge=0,
    )
    continue_on_error: bool = Field(
        default=False,
        description="Continue processing on errors",
    )
    migration_mode: bool = Field(
        default=False,
        description="Enable migration-specific optimizations",
    )
    dry_run_mode: bool = Field(
        default=False,
        description="Validate without actually loading data",
    )
    log_sql: bool = Field(
        default=False,
        description="Log generated SQL statements",
    )


class TargetOracleConfig(SingerTargetConfig):
    """Complete configuration for target-oracle v0.7.0.

    Uses flext-core SingerTargetConfig with structured value objects.
    Zero tolerance for legacy patterns or code duplication.
    """

    # Provide defaults for inherited SingerTargetConfig fields
    stream_maps: dict[str, Any] | None = Field(
        default=None,
        description="Configuration for stream maps including aliasing and filtering",
    )
    stream_map_config: dict[str, Any] | None = Field(
        default=None,
        description="Additional configuration for stream maps",
    )
    state: dict[str, Any] | None = Field(
        default=None,
        description="Singer state for incremental replication",
    )
    max_parallel_streams: int = Field(
        default=0,
        description="Maximum number of parallel streams (0 = sequential)",
        ge=0,
    )
    batch_config: dict[str, Any] | None = Field(
        default=None,
        description="Batch configuration for targets",
    )
    api_url: str | None = Field(
        default=None,
        description="Base API URL",
    )
    timeout: float = Field(
        default=300.0,
        description="Request timeout in seconds",
        gt=0,
    )
    retry_count: int = Field(
        default=3,
        description="Number of retries for failed requests",
        ge=0,
    )
    page_size: int = Field(
        default=100,
        description="Page size for paginated requests",
        gt=0,
    )
    load_method: str = Field(
        default="append",
        description="Method for loading data (append, upsert, overwrite)",
        pattern="^(append|upsert|overwrite)$",
    )
    flattening_max_depth: int = Field(
        default=10,
        description="Maximum depth for flattening nested objects",
        gt=0,
        le=20,
    )

    # Structured configuration using value objects
    connection: OracleConnectionConfig | None = Field(
        default=None,
        description="Connection configuration",
    )
    performance: OraclePerformanceConfig | None = Field(
        default=None,
        description="Performance configuration",
    )
    tables: OracleTableConfig | None = Field(
        default=None,
        description="Table configuration",
    )
    schema_management: OracleSchemaConfig | None = Field(
        default=None,
        description="Schema management configuration",
    )
    processing: OracleProcessingConfig | None = Field(
        default=None,
        description="Processing configuration",
    )

    # Environment variable support
    model_config = ConfigDict(
        extra="forbid",
    )

    @model_validator(mode="after")
    def validate_connection_params(self) -> TargetOracleConfig:
        """Validate Oracle connection parameters.

        Returns:
            Validated configuration instance.

        Raises:
            ValueError: If required connection parameters are missing.

        """
        if self.connection is None:
            msg = "Connection configuration is required"
            raise ValueError(msg)

        if self.connection.dsn:
            return self

        if not self.connection.host:
            msg = "Either 'dsn' or 'host' must be provided"
            raise ValueError(msg)

        if not self.connection.service_name and not self.connection.database:
            msg = (
                "Either service_name or database (SID) must be provided when using host"
            )
            raise ValueError(
                msg,
            )

        return self

    def to_sqlalchemy_url(self) -> str:
        """Build SQLAlchemy connection URL for Oracle.

        Returns:
            SQLAlchemy connection URL string.

        """
        if self.connection is None:
            msg = "Connection configuration is required"
            raise ValueError(msg)

        if self.connection.dsn:
            # Use DSN directly
            return (
                f"oracle+oracledb://{self.connection.username}:"
                f"{self.connection.password}@{self.connection.dsn}"
            )

        # Build DSN from components
        if self.connection.service_name:
            dsn = f"{self.connection.host}:{self.connection.port}/{self.connection.service_name}"
        else:
            dsn = f"{self.connection.host}:{self.connection.port}/{self.connection.database}"

        if self.connection.protocol == "tcps":
            return (
                f"oracle+oracledb://{self.connection.username}:"
                f"{self.connection.password}@{dsn}?protocol=tcps"
            )

        return f"oracle+oracledb://{self.connection.username}:{self.connection.password}@{dsn}"

    def get_engine_options(self) -> dict[str, Any]:
        """Get SQLAlchemy engine options.

        Returns:
            Dictionary of engine configuration options.

        """
        if self.performance is None or self.processing is None:
            msg = "Performance and processing configuration is required"
            raise ValueError(msg)

        return {
            "pool_size": self.performance.pool_size,
            "max_overflow": self.performance.max_overflow,
            "pool_timeout": self.performance.pool_timeout,
            "pool_pre_ping": True,
            "pool_recycle": 3600,  # 1 hour
            "echo": self.processing.log_sql,
            "arraysize": self.performance.array_size,
        }
