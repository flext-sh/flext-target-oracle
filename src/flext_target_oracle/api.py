"""FLEXT service orchestrator for target-oracle.

from flext_target_oracle.utilities import u
Thin facade — all infrastructure from ``FlextMeltanoTargetServiceBase`` via MRO.
Oracle sink creation requires FlextTargetOracleLoader integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated, Never, override

from flext_meltano.services.consumer_bases.target_service_base import (
    FlextMeltanoTargetServiceBase,
)
from flext_target_oracle import c, m, p, r, t, u


class FlextTargetOracleService(FlextMeltanoTargetServiceBase):
    """Orchestrator for target-oracle. Loader-based, not Singer sink."""

    target_name: Annotated[
        t.NonEmptyStr,
        u.Field(description="Canonical Singer target identifier."),
    ] = "target-oracle"

    @override
    def create_sink(
        self,
        stream_name: str,
        schema: t.JsonMapping,
    ) -> Never:
        """Not supported — use FlextTargetOracleLoader directly."""
        msg = "target-oracle uses Loader pattern, not Singer sink"
        raise TypeError(msg)

    # NOTE (multi-agent): mro-rn88 — CQRS handlers: Command models are pure data; the
    # service (a flext-core FlextService via MRO) owns execution. Behavior moved here
    # out of the model layer to respect the c→t→p→m→u order and SRP.
    def run_about(
        self,
        command: m.TargetOracle.OracleTargetAboutCommand,
    ) -> p.Result[str]:
        """Return target metadata for the about command message."""
        payload: t.StrMapping = {
            "name": "flext-target-oracle",
            "description": "Singer target for Oracle loading",
            "format": command.format,
        }
        if command.format == c.TargetOracle.OUTPUT_FORMAT_TEXT:
            return r[str].ok("flext-target-oracle")
        return r[str].ok(
            t.TargetOracle.STR_MAP_ADAPTER.dump_json(payload).decode(
                c.DEFAULT_ENCODING,
            ),
        )

    def run_load(
        self,
        command: m.TargetOracle.OracleTargetLoadCommand,
    ) -> p.Result[str]:
        """Initialize the target for loading from a load command message."""
        settings_result = u.TargetOracle.load_target_settings(command.config_file)
        if settings_result.failure:
            return r[str].fail(settings_result.error or "Invalid settings")
        _ = command.state_file
        return r[str].ok("load_ready")

    def run_validate(
        self,
        command: m.TargetOracle.OracleTargetValidateCommand,
    ) -> p.Result[str]:
        """Validate target configuration from a validate command message."""
        settings_result = u.TargetOracle.load_target_settings(command.config_file)
        if settings_result.failure:
            return r[str].fail(
                settings_result.error or "Configuration validation failed",
            )
        settings: p.TargetOracle.OracleSettingsProtocol = settings_result.value
        validation_result = (
            r[bool].fail("oracle_host is required")
            if not settings.TargetOracle.oracle_host
            else r[bool].fail("oracle_service_name is required")
            if not settings.TargetOracle.oracle_service_name
            else r[bool].fail("default_target_schema is required")
            if not settings.TargetOracle.default_target_schema
            else r[bool].fail("commit_interval must be <= batch size")
            if settings.TargetOracle.commit_interval > settings.TargetOracle.batch_size
            else r[bool].ok(True)
        )
        if validation_result.failure:
            return r[str].fail(
                validation_result.error or "Configuration validation failed",
            )
        return r[str].ok("validation_ok")


target_oracle = FlextTargetOracleService

__all__: list[str] = ["FlextTargetOracleService", "target_oracle"]
