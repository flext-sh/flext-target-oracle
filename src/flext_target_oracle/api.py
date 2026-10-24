"""FLEXT service orchestrator for target-oracle.

Thin facade — all infrastructure from ``FlextMeltanoTargetServiceBase`` via MRO.
Oracle sink creation requires FlextTargetOracleLoader integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated, Never, override

from flext_meltano import FlextMeltanoTargetServiceBase

from flext_target_oracle import c, m, p, r, t, u


class FlextTargetOracleService(FlextMeltanoTargetServiceBase):
    """Orchestrator for target-oracle. Loader-based, not Singer sink."""

    target_name: Annotated[
        t.NonEmptyStr,
        m.Field(description="Canonical Singer target identifier."),
    ] = "target-oracle"

    @override
    def create_sink(self, _stream_name: str, _schema: t.JsonMapping) -> Never:
        """Not supported — use FlextTargetOracleLoader directly.

        Args:
            _stream_name: Name of the Singer stream; unused.

            _schema: Singer schema for the stream; unused.

        Raises:
            TypeError: If target-oracle uses Loader pattern, not Singer sink.

        """
        msg = "target-oracle uses Loader pattern, not Singer sink"
        raise TypeError(msg)

    # NOTE (multi-agent): mro-rn88 — CQRS handlers: Command models are pure data; the
    # service (a flext-core FlextService via MRO) owns execution. Behavior moved here
    # out of the model layer to respect the c→t→p→m→u order and SRP.
    @staticmethod
    def run_about(
        command: m.TargetOracle.OracleTargetAboutCommand,
    ) -> p.Result[str]:
        """Return target metadata for the about command message.

        Args:
            command: About command carrying the requested output format.

        Returns:
            The project name, or its JSON metadata payload for the JSON
            output format.

        """
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

    @staticmethod
    def run_load(
        command: m.TargetOracle.OracleTargetLoadCommand,
    ) -> p.Result[str]:
        """Initialize the target for loading from a load command message.

        Args:
            command: Load command carrying the config and state files.

        Returns:
            The load acknowledgement, or a failure result when the
            settings cannot be loaded.

        """
        settings_result = u.TargetOracle.load_target_settings(command.config_file)
        if settings_result.failure:
            return r[str].from_failure(settings_result)
        _ = command.state_file
        return r[str].ok("load_ready")

    @staticmethod
    def run_validate(
        command: m.TargetOracle.OracleTargetValidateCommand,
    ) -> p.Result[str]:
        """Validate target configuration from a validate command message.

        Args:
            command: Validate command carrying the configuration file.

        Returns:
            The validation acknowledgement, or a failure result when the
            settings cannot be loaded or violate a required field rule.

        """
        settings_result = u.TargetOracle.load_target_settings(command.config_file)
        if settings_result.failure:
            return r[str].from_failure(settings_result)
        settings = settings_result.value
        validation_result = (
            r[bool].fail("oracle_host is required")
            if not settings.TargetOracle.oracle_host
            else r[bool].fail("oracle_service_name is required")
            if not settings.TargetOracle.oracle_service_name
            else r[bool].fail("default_target_schema is required")
            if not settings.TargetOracle.default_target_schema
            else r[bool].fail("commit_interval must be <= batch size")
            if settings.TargetOracle.commit_interval > settings.TargetOracle.batch_size
            else r[bool].ok(value=True)
        )
        if validation_result.failure:
            return r[str].from_failure(validation_result)
        return r[str].ok("validation_ok")


target_oracle: FlextTargetOracleService = FlextTargetOracleService.fetch_global()
"""Module-level singleton facade for the flext_target_oracle namespace."""

__all__: list[str] = ["FlextTargetOracleService", "target_oracle"]
