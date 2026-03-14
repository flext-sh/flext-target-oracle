"""Service facade for Oracle Singer target operations."""

from __future__ import annotations

from flext_core import r

from .models import m
from .settings import FlextTargetOracleSettings
from .target_client import FlextTargetOracle


class FlextTargetOracleService:
    """Thin service wrapper around `FlextTargetOracle`."""

    def __init__(self, config: FlextTargetOracleSettings) -> None:
        """Initialize service wrapper with target client dependencies."""
        self.name = "flext-oracle-target"
        self.config = config
        self.client = FlextTargetOracle(config)

    def discover_catalog(self) -> r[m.Meltano.SingerCatalog]:
        """Delegate Singer catalog discovery."""
        return self.client.discover_catalog()

    def execute(self) -> r[m.TargetOracle.ExecuteResult]:
        """Execute connectivity readiness checks."""
        return self.client.execute()

    def finalize(self) -> r[m.TargetOracle.LoaderFinalizeResult]:
        """Flush pending loader data."""
        return self.client.finalize()

    def get_implementation_metrics(self) -> m.TargetOracle.ImplementationMetrics:
        """Return implementation metrics."""
        return self.client.get_implementation_metrics()

    def process_singer_messages(
        self,
        messages: list[
            m.TargetOracle.SingerSchemaMessage
            | m.TargetOracle.SingerRecordMessage
            | m.TargetOracle.SingerStateMessage
            | m.TargetOracle.SingerActivateVersionMessage
        ],
    ) -> r[m.TargetOracle.ProcessingSummary]:
        """Delegate processing of Singer message batches."""
        return self.client.process_singer_messages(messages)

    def test_connection(self) -> r[bool]:
        """Validate Oracle connectivity."""
        return self.client.test_connection()

    def validate_configuration(self) -> r[bool]:
        """Validate target configuration."""
        return self.client.validate_configuration()


__all__ = ["FlextTargetOracleService"]
