"""Oracle Target Commands using Flext CQRS SOURCE OF TRUTH.

ZERO DUPLICATION - Uses flext-core FlextModels.Command exclusively.
No local command implementations - everything from SOURCE OF TRUTH.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import override

import yaml
from pydantic import Field

from flext_core import FlextHandlers, FlextModels, FlextResult, FlextTypes
from flext_db_oracle import FlextDbOracleApi, FlextDbOracleModels
from flext_target_oracle.target_client import FlextTargetOracle
from flext_target_oracle.target_config import FlextTargetOracleConfig
from flext_target_oracle.target_services import OracleConnectionService


class OracleTargetValidateCommand(FlextModels.Command):
    """Oracle target validation command using Flext CQRS SOURCE OF TRUTH.

    ZERO DUPLICATION - Inherits from FlextModels.Command directly.
    """

    # Command-specific data using Pydantic fields
    config_file: str | None = Field(
        default=None,
        description="Path to configuration file",
    )

    @override
    def execute(self: object) -> FlextResult[str]:
        """Execute validation using pure flext-core patterns."""
        try:
            # Load configuration using direct instantiation - SOURCE OF TRUTH pattern
            if self.config_file:
                # Load configuration from file
                config_path: Path = Path(self.config_file)
                if not config_path.exists():
                    return FlextResult[str].fail(
                        f"Configuration file not found: {self.config_file}",
                    )

                config_data: FlextTypes.Core.Dict = json.loads(
                    config_path.read_text(encoding="utf-8")
                )
                config: FlextTargetOracleConfig = FlextTargetOracleConfig(**config_data)
            else:
                # Use FlextTargetOracleConfig's built-in environment loading
                # This uses Pydantic BaseSettings to automatically load environment variables
                config: FlextTargetOracleConfig = FlextTargetOracleConfig()

            # Validate configuration using domain method
            validation_result: FlextResult[object] = config.validate_domain_rules()
            if validation_result.is_failure:
                return FlextResult[str].fail(
                    f"Configuration validation failed: {validation_result.error}",
                )

            # Test Oracle connection using domain services
            # Create Oracle API configuration from our config
            oracle_api_config = FlextDbOracleModels.OracleConfig(
                host=config.oracle_host,
                port=config.oracle_port,
                name=config.oracle_service,  # Use 'name' instead of 'database'
                username=config.oracle_user,  # Use 'username' instead of 'user'
                password=config.oracle_password.get_secret_value()
                if hasattr(config.oracle_password, "get_secret_value")
                else str(config.oracle_password),
            )
            oracle_api = FlextDbOracleApi(oracle_api_config)

            connection_service = OracleConnectionService(
                config=config,
                oracle_api=oracle_api,
            )

            test_result: FlextResult[object] = connection_service.execute()
            if test_result.is_failure:
                return FlextResult[str].fail(
                    f"Oracle connection test failed: {test_result.error}",
                )

            return FlextResult[str].ok(
                "Oracle target validation completed successfully",
            )

        except Exception as e:
            return FlextResult[str].fail(f"Validation error: {e}")


class OracleTargetLoadCommand(FlextModels.Command):
    """Oracle target load command using Flext CQRS SOURCE OF TRUTH.

    ZERO DUPLICATION - Inherits from FlextModels.Command directly.
    """

    # Command-specific data using Pydantic fields
    config_file: str | None = Field(
        default=None,
        description="Path to configuration file",
    )
    state_file: str | None = Field(default=None, description="Path to state file")

    @override
    def execute(self: object) -> FlextResult[str]:
        """Execute load using pure flext-core patterns."""
        try:
            # Load configuration using direct instantiation - SOURCE OF TRUTH pattern
            if self.config_file:
                # Load configuration from file

                config_path: Path = Path(self.config_file)
                if not config_path.exists():
                    return FlextResult[str].fail(
                        f"Configuration file not found: {self.config_file}",
                    )

                config_data: FlextTypes.Core.Dict = json.loads(
                    config_path.read_text(encoding="utf-8")
                )
                config: FlextTargetOracleConfig = FlextTargetOracleConfig(**config_data)
            else:
                # Use FlextTargetOracleConfig's built-in environment loading
                # This uses Pydantic BaseSettings to automatically load environment variables
                config: FlextTargetOracleConfig = FlextTargetOracleConfig()

            # Create target instance using SOURCE OF TRUTH factory pattern
            # Create FlextTargetOracle instance directly - it accepts config in constructor
            target = FlextTargetOracle(config)

            # Singer targets are typically executed by reading stdin
            # For CLI purposes, we'll validate the target is ready for operation
            loader_result: FlextResult[object] = target.loader.test_connection()
            if loader_result.is_failure:
                return FlextResult[str].fail(
                    f"Target initialization failed: {loader_result.error}",
                )

            # For now, we return success indicating target is ready for Singer data
            success_msg = "Oracle target initialized and ready for data loading"
            if self.state_file:
                success_msg += f" (state file: {self.state_file} would be processed by Singer orchestrator)"

            return FlextResult[str].ok(success_msg)

        except Exception as e:
            return FlextResult[str].fail(f"Load error: {e}")


class OracleTargetAboutCommand(FlextModels.Command):
    """Oracle target about command using Flext CQRS SOURCE OF TRUTH.

    ZERO DUPLICATION - Inherits from FlextModels.Command directly.
    """

    # Command-specific data using Pydantic fields
    format: str = Field(default=json, description="Output format (json, text, yaml)")

    @override
    def execute(self: object) -> FlextResult[str]:
        """Execute about using pure flext-core patterns."""
        try:
            # Get about information using domain methods
            about_info: FlextTypes.Core.Dict = {
                "name": flext - target - oracle,
                "version": "__version__",
                "description": "Modern Oracle Singer Target using FLEXT framework",
                "capabilities": [
                    "Singer Protocol 1.5.0",
                    "Oracle Database connectivity",
                    "Batch loading with configurable sizes",
                    "Schema evolution and table creation",
                    "SSL/TLS connection support",
                    "Connection pooling",
                    "Structured logging with observability",
                ],
                "configuration": {
                    "required": [
                        "oracle_host",
                        "oracle_port",
                        "oracle_service",
                        "oracle_user",
                        "oracle_password",
                    ],
                    "optional": [
                        "batch_size",
                        "pool_size",
                        "ssl_settings",
                        "load_method",
                    ],
                },
            }

            if self.format == "json":
                formatted_output = json.dumps(about_info, indent=2)
            elif self.format == "yaml":
                formatted_output = yaml.dump(about_info, default_flow_style=False)
            else:
                # Text format - extract configuration data safely
                config_data: dict[str, object] = about_info.get("configuration", {})
                required_items = (
                    config_data.get("required", [])
                    if isinstance(config_data, dict)
                    else []
                )
                optional_items = (
                    config_data.get("optional", [])
                    if isinstance(config_data, dict)
                    else []
                )
                capabilities: list[object] = about_info.get("capabilities", [])
                capabilities_list = (
                    capabilities if isinstance(capabilities, list) else []
                )

                formatted_output = f"""

FLEXT Target Oracle v{about_info["version"]}
{about_info["description"]}

Capabilities:
{chr(10).join("  • " + str(cap) for cap in capabilities_list)}

Required Configuration:
{chr(10).join("  • " + str(req) for req in required_items)}

Optional Configuration:
{chr(10).join("  • " + str(opt) for opt in optional_items)}
"""

            return FlextResult[str].ok(formatted_output)

        except Exception as e:
            return FlextResult[str].fail(f"About error: {e}")


class OracleTargetCommandHandler(FlextHandlers[FlextModels.Command, str]):
    """Oracle target command handler using Flext CQRS SOURCE OF TRUTH.

    ZERO DUPLICATION - Uses FlextHandlers directly.
    """

    @override
    def __init__(self: object) -> None:
        """Initialize Oracle target command handler."""
        config: dict[str, object] = FlextModels.CqrsConfig.Handler(
            handler_id=oracle_target_command_handler,
            handler_name="Oracle Target Command Handler",
            handler_type=command,
            handler_mode=command,
            command_timeout=30000,
            max_command_retries=3,
            metadata={"description": "Oracle target Singer command handler"},
        )
        super().__init__(config=config)

    @override
    def handle(self, message: FlextModels.Command) -> FlextResult[str]:
        """Handle Oracle target commands using type-based dispatch."""
        # Dispatch based on command type
        if isinstance(message, OracleTargetValidateCommand):
            return self._handle_validate_command(message)
        if isinstance(message, OracleTargetLoadCommand):
            return self._handle_load_command(message)
        if isinstance(message, OracleTargetAboutCommand):
            return self._handle_about_command(message)
        return FlextResult[str].fail(f"Unknown command type: {type(message).__name__}")

    def _handle_validate_command(
        self,
        command: OracleTargetValidateCommand,
    ) -> FlextResult[str]:
        """Handle Oracle target validation command."""
        return FlextResult[str].ok(
            f"Validation command handled: {command.command_type}",
        )

    def _handle_load_command(
        self,
        command: OracleTargetLoadCommand,
    ) -> FlextResult[str]:
        """Handle Oracle target load command."""
        return FlextResult[str].ok(f"Load command handled: {command.command_type}")

    def _handle_about_command(
        self,
        command: OracleTargetAboutCommand,
    ) -> FlextResult[str]:
        """Handle Oracle target about command."""
        return FlextResult[str].ok(f"About command handled: {command.command_type}")


class OracleTargetCommandFactory:
    """Factory for creating Oracle target commands using SOURCE OF TRUTH patterns."""

    @staticmethod
    def create_validate_command(
        config_file: str | None = None,
    ) -> OracleTargetValidateCommand:
        """Create validation command using Flext CQRS SOURCE OF TRUTH."""
        return OracleTargetValidateCommand(
            command_id=str(uuid.uuid4()),
            command_type=oracle_target_validate,
            config_file=config_file,
        )

    @staticmethod
    def create_load_command(
        config_file: str | None = None,
        state_file: str | None = None,
    ) -> OracleTargetLoadCommand:
        """Create load command using Flext CQRS SOURCE OF TRUTH."""
        return OracleTargetLoadCommand(
            command_id=str(uuid.uuid4()),
            command_type=oracle_target_load,
            config_file=config_file,
            state_file=state_file,
        )

    @staticmethod
    def create_about_command(output_format: str = "json") -> OracleTargetAboutCommand:
        """Create about command using Flext CQRS SOURCE OF TRUTH."""
        return OracleTargetAboutCommand(
            command_id=str(uuid.uuid4()),
            command_type=oracle_target_about,
            format=output_format,
        )


__all__: FlextTypes.Core.StringList = [
    "OracleTargetAboutCommand",
    "OracleTargetCommandFactory",
    "OracleTargetCommandHandler",
    "OracleTargetLoadCommand",
    "OracleTargetValidateCommand",
]
