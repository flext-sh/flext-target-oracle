"""Target Oracle protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_core import FlextCore


class FlextTargetOracleProtocols:
    """Singer Target Oracle protocols with explicit re-exports from FlextCore.Protocols foundation.

    Domain Extension Pattern (Phase 3):
    - Explicit re-export of foundation protocols (not inheritance)
    - Domain-specific protocols organized in TargetOracle namespace
    - 100% backward compatibility through aliases
    """

    # ============================================================================
    # RE-EXPORT FOUNDATION PROTOCOLS (EXPLICIT PATTERN)
    # ============================================================================

    Foundation = FlextCore.Protocols.Foundation
    Domain = FlextCore.Protocols.Domain
    Application = FlextCore.Protocols.Application
    Infrastructure = FlextCore.Protocols.Infrastructure
    Extensions = FlextCore.Protocols.Extensions
    Commands = FlextCore.Protocols.Commands

    # ============================================================================
    # SINGER TARGET ORACLE-SPECIFIC PROTOCOLS (DOMAIN NAMESPACE)
    # ============================================================================

    class TargetOracle:
        """Singer Target Oracle domain protocols for Oracle database loading."""

        @runtime_checkable
        class TargetProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for Oracle target operations."""

            def process_record(
                self, record: FlextCore.Types.Dict
            ) -> FlextCore.Result[None]: ...

        @runtime_checkable
        class ConnectionProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for Oracle connection management."""

            def connect(
                self, config: FlextCore.Types.Dict
            ) -> FlextCore.Result[object]: ...

        @runtime_checkable
        class SchemaProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for Oracle schema management."""

            def create_table(
                self, schema: FlextCore.Types.Dict
            ) -> FlextCore.Result[None]: ...

        @runtime_checkable
        class BatchProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for Oracle batch operations."""

            def execute_batch(
                self, records: list[FlextCore.Types.Dict]
            ) -> FlextCore.Result[None]: ...

        @runtime_checkable
        class RecordProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for Oracle record processing."""

            def transform_record(
                self, record: FlextCore.Types.Dict
            ) -> FlextCore.Result[FlextCore.Types.Dict]: ...

        @runtime_checkable
        class SingerProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for Singer message handling."""

            def process_message(
                self, message: FlextCore.Types.Dict
            ) -> FlextCore.Result[None]: ...

        @runtime_checkable
        class PerformanceProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for Oracle performance optimization."""

            def optimize_batch_size(self, size: int) -> FlextCore.Result[int]: ...

        @runtime_checkable
        class SecurityProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for Oracle security operations."""

            def validate_credentials(
                self, config: FlextCore.Types.Dict
            ) -> FlextCore.Result[bool]: ...

        @runtime_checkable
        class MonitoringProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for Oracle loading monitoring."""

            def track_progress(self, records: int) -> FlextCore.Result[None]: ...

    # ============================================================================
    # BACKWARD COMPATIBILITY ALIASES (100% COMPATIBILITY)
    # ============================================================================

    TargetProtocol = TargetOracle.TargetProtocol
    ConnectionProtocol = TargetOracle.ConnectionProtocol
    SchemaProtocol = TargetOracle.SchemaProtocol
    BatchProtocol = TargetOracle.BatchProtocol
    RecordProtocol = TargetOracle.RecordProtocol
    SingerProtocol = TargetOracle.SingerProtocol
    PerformanceProtocol = TargetOracle.PerformanceProtocol
    SecurityProtocol = TargetOracle.SecurityProtocol
    MonitoringProtocol = TargetOracle.MonitoringProtocol


__all__ = [
    "FlextTargetOracleProtocols",
]
