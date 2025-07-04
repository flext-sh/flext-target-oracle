"""Batch processing interfaces.

These interfaces define the contract for batch processing operations,
enabling different strategies for handling data batches.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from ..models.batch import Batch, BatchResult, ProcessingStrategy


@runtime_checkable
class IBatchProcessor(Protocol):
    """Interface for batch processing operations."""

    @abstractmethod
    def process_batch(self, batch: Batch, strategy: ProcessingStrategy) -> BatchResult:
        """Process a batch of records using the specified strategy."""

    @abstractmethod
    def prepare_batch(self, records: list[dict[str, Any]]) -> Batch:
        """Prepare records for batch processing."""

    @abstractmethod
    def split_batch(self, batch: Batch, chunk_size: int) -> list[Batch]:
        """Split a batch into smaller chunks."""

    @abstractmethod
    def merge_results(self, results: list[BatchResult]) -> BatchResult:
        """Merge multiple batch results into one."""

    @abstractmethod
    def get_optimal_batch_size(self) -> int:
        """Get the optimal batch size based on current conditions."""


@runtime_checkable
class IBatchValidator(Protocol):
    """Interface for batch validation."""

    @abstractmethod
    def validate_batch(self, batch: Batch) -> BatchResult:
        """Validate a batch before processing."""

    @abstractmethod
    def validate_record(self, record: dict[str, Any]) -> list[str]:
        """Validate a single record and return errors."""

    @abstractmethod
    def can_recover(self, error: Exception) -> bool:
        """Check if batch processing can recover from an error."""

    @abstractmethod
    def sanitize_batch(self, batch: Batch) -> Batch:
        """Sanitize batch data, removing or fixing invalid records."""
