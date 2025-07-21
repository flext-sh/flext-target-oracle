# Copyright (c) 2025 FLEXT Team
# Licensed under the MIT License
# SPDX-License-Identifier: MIT

"""Compatibility module for legacy connector imports.

Provides a compatibility wrapper around flext-infrastructure.databases.flext-db-oracle.
"""

from __future__ import annotations

from typing import Any

from flext_db_oracle import OracleConfig, OracleConnectionService


class OracleConnector:
    """Compatibility wrapper for OracleConnectionService."""

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize with backward compatibility."""
        self.config = config

        # Convert config format for flext-infrastructure.databases.flext-db-oracle
        oracle_config = {
            "host": config.get("host", "localhost"),
            "port": config.get("port", 1521),
            "service_name": config.get("service_name"),
            "sid": config.get("database"),  # Map database to sid
            "username": config.get("username"),
            "password": config.get("password"),
            "protocol": config.get("protocol", "tcp"),
        }

        # Create the actual service (only if credentials provided)
        if oracle_config.get("username") and oracle_config.get("password"):
            self._oracle_config: OracleConfig | None = OracleConfig(**oracle_config)
            self._service: OracleConnectionService | None = OracleConnectionService(
                self._oracle_config,
            )
        else:
            self._oracle_config = None
            self._service = None

    @property
    def _engine(self) -> Any:
        """Get the underlying SQLAlchemy engine for compatibility."""
        if self._service is None:
            msg = "No database connection configured"
            raise RuntimeError(msg)

        # Return the engine from the connection service
        return self._service._engine if hasattr(self._service, "_engine") else None  # noqa: SLF001

    def prepare_table(
        self,
        *,
        full_table_name: str,
        schema: dict[str, Any],
        primary_keys: list[str],
        as_temp_table: bool = False,
    ) -> None:
        """Prepare table for data loading (compatibility method)."""
        if self._service is None:
            msg = "No database connection configured"
            raise RuntimeError(msg)

        # This is a compatibility method that doesn't do anything in the new architecture
        # The actual table creation is handled by the schema service

    def get_sqlalchemy_url(self, config: dict[str, Any] | None = None) -> str:
        """Build SQLAlchemy URL for backward compatibility."""
        cfg = config or self.config

        host = cfg.get("host", "localhost")
        port = cfg.get("port", 1521)
        service_name = cfg.get("service_name", "XE")
        username = cfg.get("username")
        password = cfg.get("password")
        protocol = cfg.get("protocol", "tcp")

        if not username or not password:
            msg = "Username and password are required"
            raise ValueError(msg)

        # Build appropriate URL based on protocol
        if protocol == "tcps":
            return f"oracle+oracledb://{username}:{password}@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCPS)(HOST={host})(PORT={port}))(CONNECT_DATA=(SERVICE_NAME={service_name})))"
        return f"oracle+oracledb://{username}:{password}@{host}:{port}/{service_name}"


__all__ = ["OracleConnector"]
