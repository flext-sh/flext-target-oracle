"""Oracle connection implementation.

Concrete implementation of connection interfaces for Oracle database,
using oracledb driver with advanced features.
"""

from __future__ import annotations

import logging
import queue
import threading
import time
from contextlib import contextmanager
from datetime import datetime
from typing import TYPE_CHECKING, Any, Generator

import oracledb

from ...core.exceptions import ConnectionError, PoolExhaustedError
from ...core.interfaces.connection import (
    IConnection,
    IConnectionManager,
    IConnectionPool,
)
from ...core.models.connection import (
    ConnectionInfo,
    ConnectionProtocol,
    ConnectionState,
    ConnectionStats,
)

if TYPE_CHECKING:
    from ...core.models.config import OracleConfig

logger = logging.getLogger(__name__)


class OracleConnection:
    """Oracle database connection wrapper implementing IConnection."""

    def __init__(self, connection: oracledb.Connection, connection_id: str) -> None:
        """Initialize Oracle connection wrapper."""
        self._connection = connection
        self._connection_id = connection_id
        self._created_at = datetime.utcnow()
        self._last_used_at = self._created_at
        self._lock = threading.Lock()

    def execute(self, query: str, params: dict[str, Any] | None = None) -> Any:
        """Execute a query with optional parameters."""
        with self._lock:
            self._last_used_at = datetime.utcnow()
            cursor = self._connection.cursor()
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                # For SELECT queries, fetch results
                if query.strip().upper().startswith("SELECT"):
                    return cursor.fetchall()

                # For DML, return rowcount
                return cursor.rowcount
            finally:
                cursor.close()

    def executemany(self, query: str, params_list: list[dict[str, Any]]) -> Any:
        """Execute a query with multiple parameter sets."""
        with self._lock:
            self._last_used_at = datetime.utcnow()
            cursor = self._connection.cursor()
            try:
                cursor.executemany(query, params_list)
                return cursor.rowcount
            finally:
                cursor.close()

    def commit(self) -> None:
        """Commit the current transaction."""
        with self._lock:
            self._connection.commit()

    def rollback(self) -> None:
        """Rollback the current transaction."""
        with self._lock:
            self._connection.rollback()

    def close(self) -> None:
        """Close the connection."""
        with self._lock:
            if self._connection:
                self._connection.close()

    def is_alive(self) -> bool:
        """Check if connection is still alive."""
        try:
            with self._lock:
                self._connection.ping()
                return True
        except Exception:
            return False

    @property
    def connection_id(self) -> str:
        """Get connection ID."""
        return self._connection_id

    @property
    def native_connection(self) -> oracledb.Connection:
        """Get native Oracle connection for advanced operations."""
        return self._connection


class OracleConnectionPool:
    """Oracle connection pool implementation."""

    def __init__(
        self, manager: OracleConnectionManager, size: int = 10, max_overflow: int = 10
    ) -> None:
        """Initialize connection pool."""
        self._manager = manager
        self._size = size
        self._max_overflow = max_overflow
        self._pool: queue.Queue[OracleConnection] = queue.Queue(
            maxsize=size + max_overflow
        )
        self._all_connections: dict[str, OracleConnection] = {}
        self._active_connections: set[str] = set()
        self._lock = threading.Lock()
        self._stats = {
            "total_requests": 0,
            "failed_connections": 0,
            "peak_connections": 0,
            "total_wait_time": 0.0,
        }

        # Pre-populate pool
        self._initialize_pool()

    def _initialize_pool(self) -> None:
        """Pre-populate the pool with connections."""
        for i in range(self._size):
            try:
                conn = self._manager.connect()
                self._pool.put(conn)
                with self._lock:
                    self._all_connections[conn.connection_id] = conn
            except Exception as e:
                logger.warning(f"Failed to create connection {i+1}: {e}")
                self._stats["failed_connections"] += 1

    @contextmanager
    def acquire(self) -> Generator[IConnection, None, None]:
        """Acquire a connection from the pool."""
        start_time = time.time()
        connection = None

        try:
            # Try to get from pool
            try:
                connection = self._pool.get(timeout=30)
                wait_time = time.time() - start_time

                with self._lock:
                    self._stats["total_requests"] += 1
                    self._stats["total_wait_time"] += wait_time
                    self._active_connections.add(connection.connection_id)

                    # Update peak connections
                    active_count = len(self._active_connections)
                    if active_count > self._stats["peak_connections"]:
                        self._stats["peak_connections"] = active_count

                # Verify connection is alive
                if not connection.is_alive():
                    logger.info("Connection is dead, creating new one")
                    connection.close()
                    connection = self._manager.connect()
                    with self._lock:
                        self._all_connections[connection.connection_id] = connection

                yield connection

            except queue.Empty:
                # Pool exhausted, try to create overflow connection
                with self._lock:
                    total_connections = len(self._all_connections)
                    if total_connections < self._size + self._max_overflow:
                        connection = self._manager.connect()
                        self._all_connections[connection.connection_id] = connection
                        self._active_connections.add(connection.connection_id)
                        yield connection
                    else:
                        raise PoolExhaustedError(
                            f"Connection pool exhausted: {total_connections} connections in use"
                        )

        finally:
            # Return connection to pool
            if connection:
                with self._lock:
                    self._active_connections.discard(connection.connection_id)

                if connection.is_alive():
                    self._pool.put(connection)
                else:
                    # Connection is dead, remove it
                    with self._lock:
                        self._all_connections.pop(connection.connection_id, None)
                    connection.close()

    def release(self, connection: IConnection) -> None:
        """Release a connection back to the pool."""
        # Handled by context manager
        pass

    def close_all(self) -> None:
        """Close all connections in the pool."""
        with self._lock:
            # Close all connections
            for conn in self._all_connections.values():
                try:
                    conn.close()
                except Exception as e:
                    logger.warning(f"Error closing connection: {e}")

            self._all_connections.clear()
            self._active_connections.clear()

            # Clear the queue
            while not self._pool.empty():
                try:
                    self._pool.get_nowait()
                except queue.Empty:
                    break

    def get_stats(self) -> ConnectionStats:
        """Get pool statistics."""
        with self._lock:
            total = len(self._all_connections)
            active = len(self._active_connections)
            avg_wait = (
                self._stats["total_wait_time"] / self._stats["total_requests"]
                if self._stats["total_requests"] > 0
                else 0.0
            )

            return ConnectionStats(
                total_connections=total,
                active_connections=active,
                idle_connections=total - active,
                failed_connections=self._stats["failed_connections"],
                total_requests=self._stats["total_requests"],
                average_wait_time=avg_wait,
                peak_connections=self._stats["peak_connections"],
            )


class OracleConnectionManager:
    """Oracle connection manager implementation."""

    def __init__(self, config: OracleConfig) -> None:
        """Initialize connection manager."""
        self._config = config
        self._connection_count = 0
        self._lock = threading.Lock()

    def connect(self) -> OracleConnection:
        """Create a new connection."""
        # Build connection parameters
        params = oracledb.ConnectParams(
            host=self._config.host,
            port=self._config.port,
            service_name=self._config.service_name,
        )

        try:
            # Create connection
            connection = oracledb.connect(
                user=self._config.user,
                password=self._config.password.get_secret_value(),
                params=params,
            )

            # Configure connection
            connection.autocommit = False
            connection.stmtcachesize = 50

            # Create wrapper
            with self._lock:
                self._connection_count += 1
                connection_id = f"oracle_{self._connection_count}"

            logger.info(f"Created Oracle connection {connection_id}")
            return OracleConnection(connection, connection_id)

        except oracledb.Error as e:
            raise ConnectionError(f"Failed to connect to Oracle: {e}") from e

    def disconnect(self, connection: IConnection) -> None:
        """Close a connection."""
        if isinstance(connection, OracleConnection):
            connection.close()
            logger.info(f"Closed Oracle connection {connection.connection_id}")

    def test_connection(self) -> bool:
        """Test if a connection can be established."""
        try:
            conn = self.connect()
            result = conn.execute("SELECT 1 FROM DUAL")
            conn.close()
            return result[0][0] == 1
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False

    def get_connection_info(self) -> ConnectionInfo:
        """Get information about the connection."""
        try:
            conn = self.connect()

            # Get server version
            version = conn.execute("SELECT BANNER FROM V$VERSION WHERE ROWNUM = 1")[0][
                0
            ]

            # Get session info
            session_info = conn.execute(
                "SELECT SYS_CONTEXT('USERENV', 'SID'), "
                "SYS_CONTEXT('USERENV', 'HOST'), "
                "SYS_CONTEXT('USERENV', 'SERVICE_NAME') FROM DUAL"
            )[0]

            conn.close()

            return ConnectionInfo(
                state=ConnectionState.CONNECTED,
                protocol=ConnectionProtocol.TCP.value,
                server_version=version,
                server_host=self._config.host,
                server_port=self._config.port,
                service_name=session_info[2],
                session_id=str(session_info[0]),
                connected_at=datetime.utcnow(),
            )

        except Exception as e:
            logger.error(f"Failed to get connection info: {e}")
            return ConnectionInfo(
                state=ConnectionState.ERROR,
                protocol=ConnectionProtocol.TCP.value,
            )

    def create_pool(self, size: int = 10) -> IConnectionPool:
        """Create a connection pool."""
        return OracleConnectionPool(self, size, self._config.pool_max_overflow)

    @contextmanager
    def with_transaction(self) -> Generator[IConnection, None, None]:
        """Get a connection with automatic transaction management."""
        conn = self.connect()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
