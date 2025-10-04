"""Target Oracle protocols for FLEXT ecosystem."""

from typing import Any, Protocol, runtime_checkable

from flext_core import FlextProtocols, FlextResult, FlextTypes


class FlextTargetOracleProtocols:
    """Singer Target Oracle protocols with explicit re-exports from FlextProtocols foundation.

    Domain Extension Pattern (Phase 3):
    - Explicit re-export of foundation protocols (not inheritance)
    - Domain-specific protocols organized in TargetOracle namespace
    - 100% backward compatibility through aliases
    """

    # ============================================================================
    # RE-EXPORT FOUNDATION PROTOCOLS (EXPLICIT PATTERN)
    # ============================================================================

    Foundation = FlextProtocols.Foundation
    Domain = FlextProtocols.Domain
    Application = FlextProtocols.Application
    Infrastructure = FlextProtocols.Infrastructure
    Extensions = FlextProtocols.Extensions
    Commands = FlextProtocols.Commands

    # ============================================================================
    # SINGER TARGET ORACLE-SPECIFIC PROTOCOLS (DOMAIN NAMESPACE)
    # ============================================================================

    class TargetOracle:
        """Singer Target Oracle domain protocols for Oracle database loading."""

        @runtime_checkable
        class TargetProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for Oracle target operations."""

            def process_record(self, record: FlextTypes.Dict) -> FlextResult[None]: ...

        @runtime_checkable
        class ConnectionProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for Oracle connection management."""

            def connect(self, config: FlextTypes.Dict) -> FlextResult[Any]: ...

        @runtime_checkable
        class SchemaProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for Oracle schema management."""

            def create_table(self, schema: FlextTypes.Dict) -> FlextResult[None]: ...

        @runtime_checkable
        class BatchProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for Oracle batch operations."""

            def execute_batch(
                self, records: list[FlextTypes.Dict]
            ) -> FlextResult[None]: ...

        @runtime_checkable
        class RecordProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for Oracle record processing."""

            def transform_record(
                self, record: FlextTypes.Dict
            ) -> FlextResult[FlextTypes.Dict]: ...

        @runtime_checkable
        class SingerProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for Singer message handling."""

            def process_message(
                self, message: FlextTypes.Dict
            ) -> FlextResult[None]: ...

        @runtime_checkable
        class PerformanceProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for Oracle performance optimization."""

            def optimize_batch_size(self, size: int) -> FlextResult[int]: ...

        @runtime_checkable
        class SecurityProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for Oracle security operations."""

            def validate_credentials(
                self, config: FlextTypes.Dict
            ) -> FlextResult[bool]: ...

        @runtime_checkable
        class MonitoringProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for Oracle loading monitoring."""

            def track_progress(self, records: int) -> FlextResult[None]: ...

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
