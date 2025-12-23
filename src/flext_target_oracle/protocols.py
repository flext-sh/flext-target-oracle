"""Target Oracle protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_db_oracle.protocols import p_db_oracle
from flext_meltano.protocols import p_meltano


class FlextTargetOracleProtocols(p_meltano, p_db_oracle):
    """Singer Target Oracle protocols extending Oracle and Meltano protocols.

    Extends both FlextDbOracleProtocols and FlextMeltanoProtocols via multiple inheritance
    to inherit all Oracle protocols, Meltano protocols, and foundation protocols.
    Architecture:
    - EXTENDS: FlextDbOracleProtocols (inherits .Database.* protocols)
    - EXTENDS: FlextMeltanoProtocols (inherits .Meltano.* protocols)
    - ADDS: Target Oracle-specific protocols in Target.Oracle namespace
    - PROVIDES: Root-level alias `p` for convenient access
    Usage:
    from flext_target_oracle.protocols import p
    # Foundation protocols (inherited)
    result: p.Result[str]
    service: p.Service[str]
    # Oracle protocols (inherited)
    connection: p.Database.ConnectionProtocol
    # Meltano protocols (inherited)
    target: p.Meltano.TargetProtocol
    # Target Oracle-specific protocols
    target_protocol: p.Target.Oracle.TargetProtocol.
    """

    class Target:
        """Singer Target domain protocols."""

        class Oracle:
            """Singer Target Oracle domain protocols for Oracle database loading.

            Provides protocol definitions for Oracle target operations, connection management,
            schema management, batch operations, record processing, Singer message handling,
            performance optimization, security operations, and monitoring.
            """

            @runtime_checkable
            class TargetProtocol(p_db_oracle.Service[object], Protocol):
                """Protocol for Oracle target operations.

                Defines the interface for processing Singer records for Oracle target.
                """

                def process_record(
                    self, record: dict[str, object]
                ) -> p_meltano.Result[bool]:
                    """Process a Singer record for Oracle target.

                    Args:
                        record: Singer record to process.

                    Returns:
                        Result indicating success or failure of the processing operation.

                    """

            class ConnectionProtocol(p_db_oracle.Service[object], Protocol):
                """Protocol for Oracle connection management.

                Defines the interface for managing Oracle database connections.
                """

                def connect(
                    self, config: dict[str, object]
                ) -> p_meltano.Result[object]:
                    """Connect to Oracle database.

                    Args:
                        config: Connection configuration dictionary.

                    Returns:
                        Result containing the connection object.

                    """

            class SchemaProtocol(p_db_oracle.Service[object], Protocol):
                """Protocol for Oracle schema management.

                Defines the interface for managing Oracle database schemas.
                """

                def create_table(
                    self, schema: dict[str, object]
                ) -> p_meltano.Result[object]:
                    """Create Oracle table from schema.

                    Args:
                        schema: Table schema definition.

                    Returns:
                        Result indicating success or failure of the table creation.

                    """

            class BatchProtocol(p_db_oracle.Service[object], Protocol):
                """Protocol for Oracle batch operations.

                Defines the interface for executing batch operations on Oracle database.
                """

                def execute_batch(
                    self, records: list[dict[str, object]]
                ) -> p_meltano.Result[object]:
                    """Execute batch of Oracle operations.

                    Args:
                        records: List of records to process in batch.

                    Returns:
                        Result indicating success or failure of the batch operation.

                    """

            class RecordProtocol(p_db_oracle.Service[object], Protocol):
                """Protocol for Oracle record processing.

                Defines the interface for transforming and processing records for Oracle.
                """

                def transform_record(
                    self, record: dict[str, object]
                ) -> p_meltano.Result[dict[str, object]]:
                    """Transform Singer record for Oracle.

                    Args:
                        record: Singer record to transform.

                    Returns:
                        Result containing the transformed record.

                    """

            class SingerProtocol(p_db_oracle.Service[object], Protocol):
                """Protocol for Singer message handling.

                Defines the interface for processing Singer messages.
                """

                def process_message(
                    self, message: dict[str, object]
                ) -> p_meltano.Result[object]:
                    """Process Singer message.

                    Args:
                        message: Singer message to process.

                    Returns:
                        Result indicating success or failure of the message processing.

                    """

            class PerformanceProtocol(p_db_oracle.Service[object], Protocol):
                """Protocol for Oracle performance optimization.

                Defines the interface for optimizing Oracle operations performance.
                """

                def optimize_batch_size(self, size: int) -> p_meltano.Result[int]:
                    """Optimize batch size for Oracle operations.

                    Args:
                        size: Current batch size.

                    Returns:
                        Result containing the optimized batch size.

                    """

            class SecurityProtocol(p_db_oracle.Service[object], Protocol):
                """Protocol for Oracle security operations.

                Defines the interface for validating Oracle credentials and security.
                """

                def validate_credentials(
                    self, config: dict[str, object]
                ) -> p_meltano.Result[bool]:
                    """Validate Oracle credentials.

                    Args:
                        config: Configuration containing credentials.

                    Returns:
                        Result indicating whether the credentials are valid.

                    """

            class MonitoringProtocol(p_db_oracle.Service[object], Protocol):
                """Protocol for Oracle loading monitoring.

                Defines the interface for monitoring Oracle loading operations.
                """

                def track_progress(self, records: int) -> p_meltano.Result[bool]:
                    """Track progress of Oracle loading operations.

                    Args:
                        records: Number of records processed.

                    Returns:
                        Result indicating success or failure of tracking.

                    """


# Runtime alias for simplified usage
p = FlextTargetOracleProtocols
__all__ = [
    "FlextTargetOracleProtocols",
    "p",
]
