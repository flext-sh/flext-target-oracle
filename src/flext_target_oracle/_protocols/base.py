"""Base protocols for Target Oracle module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Sequence,
)
from typing import TYPE_CHECKING, ClassVar, Protocol, runtime_checkable

from flext_meltano import p

if TYPE_CHECKING:
    from flext_target_oracle import m, t


class FlextTargetOracleProtocolsBase:
    """TargetOracle domain protocols namespace."""

    @runtime_checkable
    class ConnectionOperationResult(Protocol):
        """Protocol for connection operation results from Oracle API."""

        @property
        def failure(self) -> bool:
            """Return True if the operation failed."""
            ...

        @property
        def error(self) -> t.Container | None:
            """Return the error value if the operation failed, else None."""
            ...

    @runtime_checkable
    class Target(Protocol):
        """Protocol for Oracle target operations."""

        def process_record(
            self,
            record: m.TargetOracle.Meltano.SingerRecordMessage,
        ) -> p.Result[bool]:
            """Process a Singer record for Oracle target."""
            ...

    @runtime_checkable
    class Connection(Protocol):
        """Protocol for Oracle connection management."""

        def connect_target(
            self,
            settings: m.TargetOracle.OracleConnectionConfig,
        ) -> p.Result[bool]:
            """Connect to Oracle database."""
            ...

    @runtime_checkable
    class Schema(Protocol):
        """Protocol for Oracle schema management."""

        def create_table_from_schema(
            self,
            table_name: str,
            schema_message: m.TargetOracle.Meltano.SingerSchemaMessage,
        ) -> p.Result[bool]:
            """Create Oracle table from schema."""
            ...

    @runtime_checkable
    class Batch(Protocol):
        """Protocol for Oracle batch operations."""

        def execute_batch_target(
            self,
            operations: Sequence[m.TargetOracle.Meltano.SingerRecordMessage],
        ) -> p.Result[Sequence[bool]]:
            """Execute batch of Oracle operations."""
            ...

    @runtime_checkable
    class Record(Protocol):
        """Protocol for Oracle record processing."""

        def transform_record_target(
            self,
            record: m.TargetOracle.Meltano.SingerRecordMessage,
        ) -> p.Result[m.TargetOracle.Meltano.SingerRecordMessage]:
            """Transform Singer record for Oracle."""
            ...

    @runtime_checkable
    class Message(Protocol):
        """Protocol for Singer message handling."""

        _flext_enforcement_exempt: ClassVar[bool] = True

        def process_message_target(
            self,
            message: m.TargetOracle.Meltano.SingerRecordMessage,
        ) -> p.Result[bool]:
            """Process Singer message."""
            ...

    @runtime_checkable
    class Optimization(Protocol):
        """Protocol for Oracle performance optimization."""

        def optimize_batch_size_target(
            self,
            record_count: int,
        ) -> p.Result[int]:
            """Optimize batch size for Oracle operations."""
            ...

    @runtime_checkable
    class Security(Protocol):
        """Protocol for Oracle security operations."""

        def validate_target_credentials(
            self,
            settings: m.TargetOracle.OracleConnectionConfig,
        ) -> p.Result[bool]:
            """Validate Oracle credentials."""
            ...

    @runtime_checkable
    class Monitoring(Protocol):
        """Protocol for Oracle loading monitoring."""

        def track_progress(
            self,
            records: int,
        ) -> p.Result[bool]:
            """Track progress of Oracle loading operations."""
            ...

    # Canonical MRO facade protocols
    @runtime_checkable
    class ConnectionService(Protocol):
        """Contract for Oracle connection services."""

        def get_connection_info(
            self,
        ) -> p.Result[m.TargetOracle.OracleConnectionConfig]:
            """Return effective Oracle connection information."""
            ...

        def test_connection(self) -> p.Result[None]:
            """Validate Oracle connectivity."""
            ...

    @runtime_checkable
    class SchemaService(Protocol):
        """Contract for Oracle schema services."""

        def ensure_table_exists(
            self,
            stream: m.TargetOracle.SingerStreamModel,
            schema_message: m.TargetOracle.Meltano.SingerSchemaMessage,
        ) -> p.Result[None]:
            """Ensure destination table exists for a stream."""
            ...

    @runtime_checkable
    class BatchService(Protocol):
        """Contract for Oracle batch services."""

        def add_record(
            self,
            stream_name: str,
            record_message: m.TargetOracle.Meltano.SingerRecordMessage,
        ) -> p.Result[None]:
            """Queue one record for batch processing."""
            ...

        def flush_all_batches(self) -> p.Result[m.TargetOracle.LoadStatisticsModel]:
            """Flush all queued batches and return aggregated stats."""
            ...

    @runtime_checkable
    class RecordService(Protocol):
        """Contract for record transformation services."""

        def transform_record(
            self,
            record_message: m.TargetOracle.Meltano.SingerRecordMessage,
            stream: m.TargetOracle.SingerStreamModel,
        ) -> p.Result[m.TargetOracle.Meltano.SingerRecordMessage]:
            """Transform one Singer record into Oracle-ready payload."""
            ...

    @runtime_checkable
    class OracleSettingsProtocol(Protocol):
        """Protocol for Oracle settings used by command classes."""

        def validate_business_rules(self) -> p.Result[bool]:
            """Validate Oracle target configuration business rules."""
            ...
