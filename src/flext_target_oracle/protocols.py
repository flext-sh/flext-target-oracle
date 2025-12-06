"""Target Oracle protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_core import FlextResult, p


class FlextTargetOracleProtocols:
    """Singer Target Oracle protocols with explicit re-exports from p foundation.

    Domain Extension Pattern (Phase 3):
    - Explicit re-export of foundation protocols (not inheritance)
    - Domain-specific protocols organized in TargetOracle namespace
    - 100% backward compatibility through aliases
    """

    # ============================================================================
    # RE-EXPORT FOUNDATION PROTOCOLS (EXPLICIT PATTERN)
    # ============================================================================

    # ============================================================================
    # SINGER TARGET ORACLE-SPECIFIC PROTOCOLS (DOMAIN NAMESPACE)
    # ============================================================================

    class TargetOracle:
        """Singer Target Oracle domain protocols for Oracle database loading."""

        @runtime_checkable
        class TargetProtocol(p.Service, Protocol):
            """Protocol for Oracle target operations."""

            def process_record(self, record: dict[str, object]) -> FlextResult[None]:
                """Process a Singer record for Oracle target."""

        @runtime_checkable
        class ConnectionProtocol(p.Service, Protocol):
            """Protocol for Oracle connection management."""

            def connect(self, config: dict[str, object]) -> FlextResult[object]:
                """Connect to Oracle database."""

        @runtime_checkable
        class SchemaProtocol(p.Service, Protocol):
            """Protocol for Oracle schema management."""

            def create_table(self, schema: dict[str, object]) -> FlextResult[None]:
                """Create Oracle table from schema."""

        @runtime_checkable
        class BatchProtocol(p.Service, Protocol):
            """Protocol for Oracle batch operations."""

            def execute_batch(
                self,
                records: list[dict[str, object]],
            ) -> FlextResult[None]:
                """Execute batch of Oracle operations."""

        @runtime_checkable
        class RecordProtocol(p.Service, Protocol):
            """Protocol for Oracle record processing."""

            def transform_record(
                self,
                record: dict[str, object],
            ) -> FlextResult[dict[str, object]]:
                """Transform Singer record for Oracle."""

        @runtime_checkable
        class SingerProtocol(p.Service, Protocol):
            """Protocol for Singer message handling."""

            def process_message(self, message: dict[str, object]) -> FlextResult[None]:
                """Process Singer message."""

        @runtime_checkable
        class PerformanceProtocol(p.Service, Protocol):
            """Protocol for Oracle performance optimization."""

            def optimize_batch_size(self, size: int) -> FlextResult[int]:
                """Optimize batch size for Oracle operations."""

        @runtime_checkable
        class SecurityProtocol(p.Service, Protocol):
            """Protocol for Oracle security operations."""

            def validate_credentials(
                self,
                config: dict[str, object],
            ) -> FlextResult[bool]:
                """Validate Oracle credentials."""

        @runtime_checkable
        class MonitoringProtocol(p.Service, Protocol):
            """Protocol for Oracle loading monitoring."""

            def track_progress(self, records: int) -> FlextResult[None]:
                """Track progress of Oracle loading operations."""

    # ============================================================================
    # BACKWARD COMPATIBILITY ALIASES (100% COMPATIBILITY)
    # ============================================================================

    @runtime_checkable
    class TargetProtocol(TargetOracle.TargetProtocol):
        """TargetProtocol - real inheritance."""

    @runtime_checkable
    class ConnectionProtocol(TargetOracle.ConnectionProtocol):
        """ConnectionProtocol - real inheritance."""

    @runtime_checkable
    class SchemaProtocol(TargetOracle.SchemaProtocol):
        """SchemaProtocol - real inheritance."""

    @runtime_checkable
    class BatchProtocol(TargetOracle.BatchProtocol):
        """BatchProtocol - real inheritance."""

    @runtime_checkable
    class RecordProtocol(TargetOracle.RecordProtocol):
        """RecordProtocol - real inheritance."""

    @runtime_checkable
    class SingerProtocol(TargetOracle.SingerProtocol):
        """SingerProtocol - real inheritance."""

    @runtime_checkable
    class PerformanceProtocol(TargetOracle.PerformanceProtocol):
        """PerformanceProtocol - real inheritance."""

    @runtime_checkable
    class SecurityProtocol(TargetOracle.SecurityProtocol):
        """SecurityProtocol - real inheritance."""

    @runtime_checkable
    class MonitoringProtocol(TargetOracle.MonitoringProtocol):
        """MonitoringProtocol - real inheritance."""


__all__ = [
    "FlextTargetOracleProtocols",
]
