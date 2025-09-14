"""Oracle Target Commands using FlextCommands SOURCE OF TRUTH.

ZERO DUPLICATION - Uses flext-core FlextCommands.Models.Command exclusively.
No local command implementations - everything from SOURCE OF TRUTH.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
import os
import uuid
from pathlib import Path

import yaml
from flext_core import FlextCommands, FlextResult, FlextTypes
from flext_db_oracle import FlextDbOracleApi, FlextDbOracleConfig
from pydantic import Field, SecretStr

from flext_target_oracle import __version__
from flext_target_oracle.target_client import FlextTargetOracle
from flext_target_oracle.target_config import FlextTargetOracleConfig
from flext_target_oracle.target_services import OracleConnectionService


class OracleTargetValidateCommand(FlextCommands.Models.Command):
    """Oracle target validation command using FlextCommands SOURCE OF TRUTH.

    ZERO DUPLICATION - Inherits from FlextCommands.Models.Command directly.
    """

    # Command-specific data using Pydantic fields
    config_file: str | None = Field(
        default=None, description="Path to configuration file"
    )

    def execute(self) -> FlextResult[str]:
        """Execute validation using pure flext-core patterns."""
        try:
            # Load configuration using direct instantiation - SOURCE OF TRUTH pattern
            if self.config_file:
                # Load configuration from file
                config_path = Path(self.config_file)
                if not config_path.exists():
                    return FlextResult[str].fail(
                        f"Configuration file not found: {self.config_file}"
                    )

                config_data = json.loads(config_path.read_text(encoding="utf-8"))
                config = FlextTargetOracleConfig(**config_data)
            else:
                # Load from environment variables
                config = FlextTargetOracleConfig(
                    oracle_host=os.getenv("ORACLE_HOST", "localhost"),
                    oracle_service=os.getenv("ORACLE_SERVICE", "XE"),
                    oracle_user=os.getenv("ORACLE_USER", "system"),
                    oracle_password=SecretStr(os.getenv("ORACLE_PASSWORD", "")),
                    oracle_port=int(os.getenv("ORACLE_PORT", "1521")),
                    default_target_schema=os.getenv("DEFAULT_TARGET_SCHEMA", "target"),
                )

            # Validate configuration using domain method
            validation_result = config.validate_domain_rules()
            if validation_result.is_failure:
                return FlextResult[str].fail(
                    f"Configuration validation failed: {validation_result.error}"
                )

            # Test Oracle connection using domain services
            # Create Oracle API configuration from our config
            oracle_api_config = FlextDbOracleConfig(
                host=config.oracle_host,
                port=config.oracle_port,
                name=config.oracle_service,  # Use 'name' instead of 'database'
                user=config.oracle_user,  # Use 'user' instead of 'username'
                password=config.oracle_password.get_secret_value()
                if hasattr(config.oracle_password, "get_secret_value")
                else str(config.oracle_password),
            )
            oracle_api = FlextDbOracleApi(oracle_api_config)

            connection_service = OracleConnectionService(
                config=config, oracle_api=oracle_api
            )

            test_result = connection_service.execute()
            if test_result.is_failure:
                return FlextResult[str].fail(
                    f"Oracle connection test failed: {test_result.error}"
                )

            return FlextResult[str].ok(
                "Oracle target validation completed successfully"
            )

        except Exception as e:
            return FlextResult[str].fail(f"Validation error: {e}")


class OracleTargetLoadCommand(FlextCommands.Models.Command):
    """Oracle target load command using FlextCommands SOURCE OF TRUTH.

    ZERO DUPLICATION - Inherits from FlextCommands.Models.Command directly.
    """

    # Command-specific data using Pydantic fields
    config_file: str | None = Field(
        default=None, description="Path to configuration file"
    )
    state_file: str | None = Field(default=None, description="Path to state file")

    def execute(self) -> FlextResult[str]:
        """Execute load using pure flext-core patterns."""
        try:
            # Load configuration using direct instantiation - SOURCE OF TRUTH pattern
            if self.config_file:
                # Load configuration from file

                config_path = Path(self.config_file)
                if not config_path.exists():
                    return FlextResult[str].fail(
                        f"Configuration file not found: {self.config_file}"
                    )

                config_data = json.loads(config_path.read_text(encoding="utf-8"))
                config = FlextTargetOracleConfig(**config_data)
            else:
                # Load from environment variables

                config = FlextTargetOracleConfig(
                    oracle_host=os.getenv("ORACLE_HOST", "localhost"),
                    oracle_service=os.getenv("ORACLE_SERVICE", "XE"),
                    oracle_user=os.getenv("ORACLE_USER", "system"),
                    oracle_password=SecretStr(os.getenv("ORACLE_PASSWORD", "")),
                    oracle_port=int(os.getenv("ORACLE_PORT", "1521")),
                    default_target_schema=os.getenv("DEFAULT_TARGET_SCHEMA", "target"),
                )

            # Create target instance using SOURCE OF TRUTH factory pattern
            # Create FlextTargetOracle instance directly - it accepts config in constructor
            target = FlextTargetOracle(config)

            # Singer targets are typically executed by reading stdin
            # For CLI purposes, we'll validate the target is ready for operation
            loader_result = target.loader.test_connection()
            if loader_result.is_failure:
                return FlextResult[str].fail(
                    f"Target initialization failed: {loader_result.error}"
                )

            # For now, we return success indicating target is ready for Singer data
            success_msg = "Oracle target initialized and ready for data loading"
            if self.state_file:
                success_msg += f" (state file: {self.state_file} would be processed by Singer orchestrator)"

            return FlextResult[str].ok(success_msg)

        except Exception as e:
            return FlextResult[str].fail(f"Load error: {e}")


class OracleTargetAboutCommand(FlextCommands.Models.Command):
    """Oracle target about command using FlextCommands SOURCE OF TRUTH.

    ZERO DUPLICATION - Inherits from FlextCommands.Models.Command directly.
    """

    # Command-specific data using Pydantic fields
    format: str = Field(default="json", description="Output format (json, text, yaml)")

    def execute(self) -> FlextResult[str]:
        """Execute about using pure flext-core patterns."""
        try:
            # Get about information using domain methods
            about_info: dict[str, object] = {
                "name": "flext-target-oracle",
                "version": __version__,
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
                try:
                    formatted_output = yaml.dump(about_info, default_flow_style=False)
                except ImportError:
                    return FlextResult[str].fail(
                        "YAML format requires PyYAML dependency"
                    )
            else:
                # Text format - extract configuration data safely
                config_data = about_info.get("configuration", {})
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
                capabilities = about_info.get("capabilities", [])
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


class OracleTargetCommandHandler(
    FlextCommands.Handlers.CommandHandler[FlextCommands.Models.Command, str]
):
    """Oracle target command handler using FlextCommands SOURCE OF TRUTH.

    ZERO DUPLICATION - Uses FlextCommands.Handlers.CommandHandler directly.
    """

    def handle(self, command: FlextCommands.Models.Command) -> FlextResult[str]:
        """Handle Oracle target commands using polymorphic dispatch."""
        # Use polymorphic dispatch - let the command execute itself
        if hasattr(command, "execute") and callable(command.execute):
            result = command.execute()
            if isinstance(result, FlextResult):
                return result
            return FlextResult[str].fail(
                f"Command {type(command).__name__} returned invalid result type"
            )

        return FlextResult[str].fail(
            f"Command {type(command).__name__} does not support execution"
        )


class OracleTargetCommandFactory:
    """Factory for creating Oracle target commands using SOURCE OF TRUTH patterns."""

    @staticmethod
    def create_validate_command(
        config_file: str | None = None,
    ) -> OracleTargetValidateCommand:
        """Create validation command using FlextCommands SOURCE OF TRUTH."""
        return OracleTargetValidateCommand(
            command_id=str(uuid.uuid4()),
            command_type="oracle_target_validate",
            config_file=config_file,
        )

    @staticmethod
    def create_load_command(
        config_file: str | None = None, state_file: str | None = None
    ) -> OracleTargetLoadCommand:
        """Create load command using FlextCommands SOURCE OF TRUTH."""
        return OracleTargetLoadCommand(
            command_id=str(uuid.uuid4()),
            command_type="oracle_target_load",
            config_file=config_file,
            state_file=state_file,
        )

    @staticmethod
    def create_about_command(output_format: str = "json") -> OracleTargetAboutCommand:
        """Create about command using FlextCommands SOURCE OF TRUTH."""
        return OracleTargetAboutCommand(
            command_id=str(uuid.uuid4()),
            command_type="oracle_target_about",
            format=output_format,
        )


__all__: FlextTypes.Core.StringList = [
    "OracleTargetAboutCommand",
    "OracleTargetCommandFactory",
    "OracleTargetCommandHandler",
    "OracleTargetLoadCommand",
    "OracleTargetValidateCommand",
]
