"""Target Oracle protocols for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_core import FlextProtocols
from flext_db_oracle.protocols import FlextDbOracleProtocols
from flext_meltano import FlextMeltanoProtocols

from .models import m


class FlextTargetOracleProtocols(FlextMeltanoProtocols, FlextDbOracleProtocols):
    """Singer Target Oracle protocols extending Oracle and Meltano protocols."""

    # Target Oracle-specific protocols
    class TargetOracle:
        """Singer Target domain protocols."""

        class Oracle:
            """Singer Target Oracle domain protocols for Oracle database loading."""

            @runtime_checkable
            class TargetProtocol(Protocol):
                """Protocol for Oracle target operations."""

                def process_record(
                    self, record: m.Meltano.SingerRecordMessage
                ) -> FlextProtocols.Result[bool]:
                    """Process a Singer record for Oracle target."""
                    ...

            @runtime_checkable
            class ConnectionProtocol(Protocol):
                """Protocol for Oracle connection management."""

                def connect_target(
                    self, config: m.TargetOracle.OracleConnectionConfig
                ) -> FlextProtocols.Result[bool]:
                    """Connect to Oracle database."""
                    ...

            @runtime_checkable
            class SchemaProtocol(Protocol):
                """Protocol for Oracle schema management."""

                def create_table_from_schema(
                    self,
                    table_name: str,
                    schema_message: m.Meltano.SingerSchemaMessage,
                ) -> FlextProtocols.Result[bool]:
                    """Create Oracle table from schema."""
                    ...

            @runtime_checkable
            class BatchProtocol(Protocol):
                """Protocol for Oracle batch operations."""

                def execute_batch_target(
                    self,
                    operations: list[m.Meltano.SingerRecordMessage],
                ) -> FlextProtocols.Result[list[bool]]:
                    """Execute batch of Oracle operations."""
                    ...

            @runtime_checkable
            class RecordProtocol(Protocol):
                """Protocol for Oracle record processing."""

                def transform_record_target(
                    self, record: m.Meltano.SingerRecordMessage
                ) -> FlextProtocols.Result[m.Meltano.SingerRecordMessage]:
                    """Transform Singer record for Oracle."""
                    ...

            @runtime_checkable
            class MessageProtocol(Protocol):
                """Protocol for Singer message handling."""

                def process_message_target(
                    self, message: m.Meltano.SingerRecordMessage
                ) -> FlextProtocols.Result[bool]:
                    """Process Singer message."""
                    ...

            @runtime_checkable
            class OptimizationProtocol(Protocol):
                """Protocol for Oracle performance optimization."""

                def optimize_batch_size_target(
                    self, record_count: int
                ) -> FlextProtocols.Result[int]:
                    """Optimize batch size for Oracle operations."""
                    ...

            @runtime_checkable
            class SecurityProtocol(Protocol):
                """Protocol for Oracle security operations."""

                def validate_target_credentials(
                    self, config: m.TargetOracle.OracleConnectionConfig
                ) -> FlextProtocols.Result[bool]:
                    """Validate Oracle credentials."""
                    ...

            @runtime_checkable
            class MonitoringProtocol(Protocol):
                """Protocol for Oracle loading monitoring."""

                def track_progress(self, records: int) -> FlextProtocols.Result[bool]:
                    """Track progress of Oracle loading operations."""
                    ...


# Runtime alias for simplified usage
p = FlextTargetOracleProtocols
__all__ = [
    "FlextTargetOracleProtocols",
    "p",
]
