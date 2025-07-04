"""Connection-related models.

These models represent connection configuration and state,
providing type safety for connection management.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ConnectionState(str, Enum):
    """Connection states."""

    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"
    CLOSED = "closed"


class ConnectionProtocol(str, Enum):
    """Oracle connection protocols."""

    TCP = "tcp"
    TCPS = "tcps"


class ConnectionConfig(BaseModel):
    """Database connection configuration."""

    host: str = Field(..., description="Database host")
    port: int = Field(1521, description="Database port")
    service_name: str = Field(..., description="Service name")
    protocol: ConnectionProtocol = Field(
        ConnectionProtocol.TCP, description="Connection protocol"
    )
    connect_timeout: int = Field(30, description="Connection timeout in seconds")
    retry_count: int = Field(3, description="Number of connection retries")
    retry_delay: int = Field(5, description="Delay between retries in seconds")

    model_config = {
        "frozen": True,
        "use_enum_values": True,
    }


class ConnectionInfo(BaseModel):
    """Information about a database connection."""

    state: ConnectionState = Field(..., description="Current connection state")
    protocol: str = Field(..., description="Connection protocol used")
    server_version: str | None = Field(None, description="Database server version")
    server_host: str | None = Field(None, description="Connected server host")
    server_port: int | None = Field(None, description="Connected server port")
    service_name: str | None = Field(None, description="Connected service name")
    session_id: str | None = Field(None, description="Database session ID")
    connected_at: datetime | None = Field(None, description="Connection timestamp")
    last_used_at: datetime | None = Field(None, description="Last activity timestamp")

    model_config = {
        "frozen": True,
    }


class ConnectionStats(BaseModel):
    """Connection pool statistics."""

    total_connections: int = Field(0, description="Total connections in pool")
    active_connections: int = Field(0, description="Currently active connections")
    idle_connections: int = Field(0, description="Currently idle connections")
    failed_connections: int = Field(0, description="Failed connection attempts")
    total_requests: int = Field(0, description="Total connection requests")
    average_wait_time: float = Field(0.0, description="Average wait time in seconds")
    peak_connections: int = Field(0, description="Peak concurrent connections")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Stats creation time"
    )

    model_config = {
        "frozen": True,
    }

    @property
    def utilization(self) -> float:
        """Calculate pool utilization percentage."""
        if self.total_connections == 0:
            return 0.0
        return (self.active_connections / self.total_connections) * 100
