# Copyright (c) 2025 FLEXT Team
# Licensed under the MIT License
# SPDX-License-Identifier: MIT

"""Compatibility module for legacy sink imports.

Provides a compatibility wrapper around the new application services.
"""

from __future__ import annotations

from typing import Any

from flext_target_oracle.domain.models import TargetConfig


class OracleSink:
    """Compatibility wrapper for OracleLoaderService."""

    def __init__(
        self,
        target: object | None = None,
        stream_name: str = "default",
        schema: dict[str, Any] | None = None,
        config: dict[str, Any] | None = None,
    ) -> None:
        """Initialize Oracle sink with backward compatibility."""
        # Handle different initialization patterns
        if config is not None:
            self.config = config
        elif target is not None:
            # Extract config from target
            if hasattr(target, "config"):
                target_config = target.config
                if isinstance(target_config, TargetConfig):
                    # Convert TargetConfig to dict
                    self.config = {
                        "host": target_config.host,
                        "port": target_config.port,
                        "service_name": target_config.service_name,
                        "sid": target_config.sid,
                        "username": target_config.username,
                        "password": target_config.password,
                        "protocol": target_config.protocol,
                        "default_target_schema": target_config.default_target_schema,
                        "batch_size": target_config.batch_size,
                    }
                else:
                    self.config = target_config
            else:
                self.config = {}
        else:
            self.config = {}

        # Store for compatibility
        self.stream_name = stream_name
        self.schema = schema or {}
        self.key_properties = schema.get("key_properties", []) if schema else []

        # Create the actual service components
        from flext_db_oracle import (
            OracleConfig,
            OracleConnectionService,
            OracleQueryService,
        )

        oracle_config = OracleConfig(
            host=self.config.get("host", "localhost"),
            port=self.config.get("port", 1521),
            service_name=self.config.get("service_name", "XEPDB1"),
            username=self.config.get("username", ""),
            password=self.config.get("password", ""),
            protocol=self.config.get("protocol", "tcp"),
        )

        self.connection_service = OracleConnectionService(oracle_config)
        self.query_service = OracleQueryService(self.connection_service)

        # Add compatibility attribute
        self._connector = self.connection_service

        # Create target config for the actual service
        target_config = TargetConfig.model_validate({
            "host": oracle_config.host,
            "port": oracle_config.port,
            "service_name": oracle_config.service_name,
            "username": oracle_config.username,
            "password": oracle_config.password,
            "protocol": oracle_config.protocol,
            "default_target_schema": self.config.get("default_target_schema", "SINGER_DATA"),
            "batch_size": self.config.get("batch_size", 10000),
        })

        from flext_target_oracle.application.services import OracleLoaderService
        self._service = OracleLoaderService(
            self.connection_service,
            self.query_service,
            target_config,
        )

    async def process_records(self, records: list[dict[str, Any]]) -> None:
        """Process records using the underlying service."""
        # For compatibility, just pass through to the service
        for record in records:
            await self._service.load_record(self.stream_name, record)


__all__ = ["OracleSink"]
