"""Modern Configuration System using Pydantic v2.

Single source of truth for all Oracle target configuration.
Follows enterprise standards with validation and type safety.
"""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConnectionConfig(BaseModel):
    """Oracle database connection configuration."""

    host: str
    port: Annotated[int, Field(ge=1, le=65535)] = 1521
    service_name: str | None = None
    database: str | None = None  # SID alternative
    username: str
    password: str
    oracle_schema: str | None = Field(
        default=None, alias="schema", description="Oracle schema name"
    )

    # Oracle-specific connection options
    protocol: Literal["tcp", "tcps"] = "tcp"
    wallet_location: str | None = None
    wallet_password: str | None = None

    @model_validator(mode="after")
    def validate_service_or_database(self) -> ConnectionConfig:
        """Ensure either service_name or database is provided."""
        if not self.service_name and not self.database:
            msg = "Either service_name or database (SID) must be provided"
            raise ValueError(msg)
        return self

    @field_validator("wallet_location")
    @classmethod
    def validate_wallet_path(cls, v: str | None) -> str | None:
        """Validate wallet directory exists if provided."""
        if v:
            from pathlib import Path
            path = Path(v)
            if not path.exists():
                msg = f"Wallet directory does not exist: {v}"
                raise ValueError(msg)
        return v


class PerformanceConfig(BaseModel):
    """Performance and optimization settings."""

    batch_size: Annotated[int, Field(ge=100, le=100000)] = 10000
    pool_size: Annotated[int, Field(ge=1, le=100)] = 10
    max_overflow: Annotated[int, Field(ge=0, le=100)] = 20
    pool_timeout: Annotated[float, Field(ge=1.0, le=300.0)] = 30.0

    # Oracle-specific performance
    use_bulk_operations: bool = True
    use_merge_statements: bool = True
    parallel_degree: Annotated[int, Field(ge=1, le=32)] = 1
    array_size: Annotated[int, Field(ge=50, le=10000)] = 1000


class TableConfig(BaseModel):
    """Table creation and management settings."""

    load_method: Literal["append-only", "upsert", "overwrite"] = "append-only"
    table_prefix: str = ""
    create_indexes: bool = True
    enable_compression: bool = False
    compression_type: Literal["basic", "advanced", "hybrid"] = "basic"
    add_metadata_columns: bool = True


class OracleConfig(BaseSettings):
    """Complete Oracle target configuration with validation."""

    model_config = SettingsConfigDict(
        env_prefix="ORACLE_TARGET_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Allow extra fields for Singer SDK compatibility
    )

    # Core configuration groups
    connection: ConnectionConfig
    performance: PerformanceConfig = Field(default_factory=PerformanceConfig)
    table: TableConfig = Field(default_factory=TableConfig)

    # Global settings
    default_target_schema: str | None = None
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    @classmethod
    def from_dict(cls, config_dict: dict[str, Any]) -> OracleConfig:
        """Create config from dictionary (Singer SDK compatibility)."""
        # Transform flat config to nested structure if needed
        if "connection" not in config_dict and "host" in config_dict:
            # Convert flat structure to nested
            connection_fields = {
                "host", "port", "service_name", "database", "username",
                "password", "schema", "protocol", "wallet_location", "wallet_password"
            }
            performance_fields = {
                "batch_size", "pool_size", "max_overflow", "pool_timeout",
                "use_bulk_operations", "use_merge_statements",
                "parallel_degree", "array_size"
            }
            table_fields = {
                "load_method", "table_prefix", "create_indexes",
                "enable_compression", "compression_type", "add_metadata_columns"
            }

            nested_config = {
                "connection": {
                    k: v for k, v in config_dict.items()
                    if k in connection_fields
                },
                "performance": {
                    k: v for k, v in config_dict.items()
                    if k in performance_fields
                },
                "table": {
                    k: v for k, v in config_dict.items()
                    if k in table_fields
                },
            }

            # Add global settings
            for key in ["default_target_schema", "log_level"]:
                if key in config_dict:
                    nested_config[key] = config_dict[key]

            # Override with nested structure if already present
            nested_config.update({k: v for k, v in config_dict.items()
                                 if k in ["connection", "performance", "table"]})

            return cls.model_validate(nested_config)

        return cls.model_validate(config_dict)

    def to_sqlalchemy_url(self) -> str:
        """Generate SQLAlchemy connection URL."""
        conn = self.connection

        if conn.service_name:
            dsn = f"{conn.host}:{conn.port}/{conn.service_name}"
        else:
            dsn = f"{conn.host}:{conn.port}/{conn.database}"

        if conn.protocol == "tcps":
            return f"oracle+oracledb://{conn.username}:{conn.password}@{dsn}?protocol=tcps"

        return f"oracle+oracledb://{conn.username}:{conn.password}@{dsn}"

    def get_engine_options(self) -> dict[str, Any]:
        """Get SQLAlchemy engine configuration options."""
        perf = self.performance

        return {
            "pool_size": perf.pool_size,
            "max_overflow": perf.max_overflow,
            "pool_timeout": perf.pool_timeout,
            "pool_pre_ping": True,
            "pool_recycle": 3600,  # 1 hour
            "echo": self.log_level == "DEBUG",
        }

