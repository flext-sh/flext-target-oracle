"""Connection management interfaces.

These interfaces define the contract for database connection management,
following SOLID principles for extensibility and testability.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from contextlib import AbstractContextManager

    from ..models.connection import ConnectionInfo, ConnectionStats


@runtime_checkable
class IConnection(Protocol):
    """Interface for a database connection."""

    @abstractmethod
    def execute(self, query: str, params: dict[str, Any] | None = None) -> Any:
        """Execute a query with optional parameters."""

    @abstractmethod
    def executemany(self, query: str, params_list: list[dict[str, Any]]) -> Any:
        """Execute a query with multiple parameter sets."""

    @abstractmethod
    def commit(self) -> None:
        """Commit the current transaction."""

    @abstractmethod
    def rollback(self) -> None:
        """Rollback the current transaction."""

    @abstractmethod
    def close(self) -> None:
        """Close the connection."""

    @abstractmethod
    def is_alive(self) -> bool:
        """Check if connection is still alive."""


@runtime_checkable
class IConnectionPool(Protocol):
    """Interface for connection pooling."""

    @abstractmethod
    def acquire(self) -> AbstractContextManager[IConnection]:
        """Acquire a connection from the pool."""

    @abstractmethod
    def release(self, connection: IConnection) -> None:
        """Release a connection back to the pool."""

    @abstractmethod
    def close_all(self) -> None:
        """Close all connections in the pool."""

    @abstractmethod
    def get_stats(self) -> ConnectionStats:
        """Get pool statistics."""


@runtime_checkable
class IConnectionManager(Protocol):
    """Interface for managing database connections."""

    @abstractmethod
    def connect(self) -> IConnection:
        """Create a new connection."""

    @abstractmethod
    def disconnect(self, connection: IConnection) -> None:
        """Close a connection."""

    @abstractmethod
    def test_connection(self) -> bool:
        """Test if a connection can be established."""

    @abstractmethod
    def get_connection_info(self) -> ConnectionInfo:
        """Get information about the connection."""

    @abstractmethod
    def create_pool(self, size: int = 10) -> IConnectionPool:
        """Create a connection pool."""

    @abstractmethod
    def with_transaction(self) -> AbstractContextManager[IConnection]:
        """Get a connection with automatic transaction management."""
