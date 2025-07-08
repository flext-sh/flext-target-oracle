"""Modern Oracle Target Implementation.

Clean, minimal implementation following SOLID principles.
Single responsibility: Orchestrate data loading pipeline.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from singer_sdk import Target
from singer_sdk import typing as th

from flext_target_oracle.config import OracleConfig
from flext_target_oracle.sink import OracleSink

if TYPE_CHECKING:
    from collections.abc import Sequence

    from singer_sdk.sinks import Sink


class OracleTarget(Target):
    """Modern Oracle Singer target.

    Responsibilities:
    - Pipeline orchestration
    - Configuration management
    - Sink lifecycle management
    """

    name = "target-oracle"
    config_jsonschema = th.PropertiesList(
        th.Property("host", th.StringType, required=True, description="Oracle host"),
        th.Property("port", th.IntegerType, default=1521, description="Oracle port"),
        th.Property("service_name", th.StringType, description="Oracle service name"),
        th.Property(
            "database",
            th.StringType,
            description="Oracle SID (alternative to service_name)",
        ),
        th.Property(
            "username", th.StringType, required=True, description="Oracle username"
        ),
        th.Property(
            "password", th.StringType, required=True, description="Oracle password"
        ),
        th.Property("schema", th.StringType, description="Default Oracle schema"),
        th.Property(
            "protocol", th.StringType, default="tcp", description="Connection protocol"
        ),
        th.Property(
            "batch_size",
            th.IntegerType,
            default=10000,
            description="Batch size for processing",
        ),
        th.Property(
            "pool_size", th.IntegerType, default=10, description="Connection pool size"
        ),
        th.Property(
            "load_method",
            th.StringType,
            default="append-only",
            description="Load method",
        ),
        th.Property(
            "log_level", th.StringType, default="INFO", description="Log level"
        ),
    ).to_dict()

    default_sink_class = OracleSink

    def __init__(
        self,
        config: dict[str, Any] | None = None,
        parse_env_config: bool = False,
        validate_config: bool = True,
    ) -> None:
        """Initialize Oracle target with typed configuration."""
        super().__init__(
            config=config,
            parse_env_config=parse_env_config,
            validate_config=validate_config,
        )

        # Create typed configuration
        self._oracle_config = OracleConfig.from_dict(dict(self.config))

    def get_sink(
        self,
        stream_name: str,
        *,
        record: dict[str, Any] | None = None,
        schema: dict[str, Any] | None = None,
        key_properties: Sequence[str] | None = None,
    ) -> Sink:
        """Get Oracle sink for stream."""
        if schema is None:
            msg = "Schema is required for Oracle sink"
            raise ValueError(msg)

        return self.default_sink_class(
            target=self,
            stream_name=stream_name,
            schema=schema,
            key_properties=key_properties,
        )

    @property
    def oracle_config(self) -> OracleConfig:
        """Get typed Oracle configuration."""
        return self._oracle_config


# CLI entry point
def main() -> None:
    """Run the Oracle target."""
    OracleTarget.cli()

