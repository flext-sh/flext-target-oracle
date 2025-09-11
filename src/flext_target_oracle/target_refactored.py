"""Oracle Target CLI using FlextDomainService and FlextCommands SOURCE OF TRUTH.

ZERO DUPLICATION - Uses flext-core patterns exclusively.
ZERO WRAPPERS - Direct method usage only.
SOLID COMPLIANCE - Single responsibility, proper domains.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys

from flext_core import (
    FlextCommands,
    FlextDomainService,
    FlextLogger,
    FlextResult,
    FlextTypes,
)
from pydantic import Field

from flext_target_oracle.target_commands import (
    OracleTargetCommandFactory,
    OracleTargetCommandHandler,
)


class FlextTargetOracleCliService(FlextDomainService[str]):
    """Oracle Target CLI Service using FlextDomainService and FlextCommands SOURCE OF TRUTH.

    ZERO DUPLICATION - Uses FlextDomainService base class directly.
    ZERO WRAPPERS - No CLI abstractions, direct command execution.
    SOLID COMPLIANCE - Single responsibility: CLI orchestration only.

    Architecture:
    - Single Responsibility: CLI argument parsing and command dispatch
    - Open/Closed: Extensible through command factory
    - Liskov Substitution: Proper FlextDomainService inheritance
    - Interface Segregation: Focused CLI interface
    - Dependency Inversion: Depends on FlextCommands abstractions
    """

    # Pydantic fields - flext-core SOURCE OF TRUTH patterns
    command_bus: FlextCommands.Bus = Field(
        default_factory=FlextCommands.Factories.create_command_bus,
        description="Command bus for routing commands",
    )
    command_handler: OracleTargetCommandHandler = Field(
        default_factory=OracleTargetCommandHandler,
        description="Oracle target command handler",
    )

    def model_post_init(self, __context: object = None) -> None:
        """Initialize CLI service using Pydantic post-init pattern."""
        # Register command handler using FlextCommands bus
        self.command_bus.register_handler(self.command_handler)

    def execute(self) -> FlextResult[str]:
        """Execute CLI service - implements FlextDomainService abstract method."""
        return FlextResult[str].ok(
            "FLEXT Target Oracle CLI Service initialized successfully"
        )

    def run_cli(self, args: list[str] | None = None) -> FlextResult[str]:
        """Run CLI with pure Python argument parsing - NO Click/Rich usage."""
        if args is None:
            args = sys.argv[1:]

        if not args or args[0] in ["-h", "--help", "help"]:
            help_text = self._get_help_text()
            self.log_info(help_text)
            return FlextResult[str].ok("Help displayed")

        command_name = args[0]
        command_args = args[1:]

        try:
            if command_name == "validate":
                return self._handle_validate_command(command_args)
            if command_name == "load":
                return self._handle_load_command(command_args)
            if command_name == "about":
                return self._handle_about_command(command_args)
            return FlextResult[str].fail(f"Unknown command: {command_name}")

        except Exception as e:
            self.log_error(f"CLI execution error: {e}")
            return FlextResult[str].fail(f"CLI error: {e}")

    def _handle_validate_command(self, args: list[str]) -> FlextResult[str]:
        """Handle validate command using FlextCommands SOURCE OF TRUTH."""
        config_file = None

        i = 0
        while i < len(args):
            if args[i] in ["--config", "-c"] and i + 1 < len(args):
                config_file = args[i + 1]
                i += 2
            else:
                i += 1

        # Create command using factory - SOURCE OF TRUTH patterns
        command = OracleTargetCommandFactory.create_validate_command(config_file)

        # Execute using command bus - FlextCommands SOURCE OF TRUTH
        result = self.command_bus.execute(command)

        if result.is_success:
            self.log_info("Oracle target validation completed successfully")
            return FlextResult[str].ok(str(result.value))
        self.log_error(f"Validation failed: {result.error}")
        return FlextResult[str].fail(str(result.error))

    def _handle_load_command(self, args: list[str]) -> FlextResult[str]:
        """Handle load command using FlextCommands SOURCE OF TRUTH."""
        config_file = None
        state_file = None

        i = 0
        while i < len(args):
            if args[i] in ["--config", "-c"] and i + 1 < len(args):
                config_file = args[i + 1]
                i += 2
            elif args[i] in ["--state", "-s"] and i + 1 < len(args):
                state_file = args[i + 1]
                i += 2
            else:
                i += 1

        # Create command using factory - SOURCE OF TRUTH patterns
        command = OracleTargetCommandFactory.create_load_command(
            config_file, state_file
        )

        # Execute using command bus - FlextCommands SOURCE OF TRUTH
        result = self.command_bus.execute(command)

        if result.is_success:
            self.log_info("Oracle target load completed successfully")
            return FlextResult[str].ok(str(result.value))
        self.log_error(f"Load failed: {result.error}")
        return FlextResult[str].fail(str(result.error))

    def _handle_about_command(self, args: list[str]) -> FlextResult[str]:
        """Handle about command using FlextCommands SOURCE OF TRUTH."""
        format_type = "json"

        i = 0
        while i < len(args):
            if args[i] in ["--format", "-f"] and i + 1 < len(args):
                format_type = args[i + 1]
                i += 2
            else:
                i += 1

        # Create command using factory - SOURCE OF TRUTH patterns
        command = OracleTargetCommandFactory.create_about_command(format_type)

        # Execute using command bus - FlextCommands SOURCE OF TRUTH
        result = self.command_bus.execute(command)

        if result.is_success:
            # Output directly - no CLI helpers needed
            return FlextResult[str].ok("About information displayed")
        self.log_error(f"About command failed: {result.error}")
        return FlextResult[str].fail(str(result.error))

    def _get_help_text(self) -> str:
        """Get help text using pure string formatting - no external dependencies."""
        return """FLEXT Target Oracle - Modern Singer Target for Oracle Database

Usage:
    target-oracle validate [--config CONFIG_FILE]
    target-oracle load [--config CONFIG_FILE] [--state STATE_FILE]
    target-oracle about [--format FORMAT]
    target-oracle --help

Commands:
    validate    Validate Oracle target configuration and connection
    load        Load Singer data into Oracle database
    about       Show information about the target

Options:
    --config, -c    Path to configuration file
    --state, -s     Path to state file (load command only)
    --format, -f    Output format: json, text, yaml (about command only)
    --help, -h      Show this help message

Examples:
    target-oracle validate --config config.json
    target-oracle load --config config.json --state state.json
    target-oracle about --format text

Environment Variables:
    ORACLE_HOST         Oracle database host
    ORACLE_PORT         Oracle database port (default: 1521)
    ORACLE_SERVICE      Oracle service name
    ORACLE_USER         Oracle username
    ORACLE_PASSWORD     Oracle password
    DEFAULT_TARGET_SCHEMA Oracle target schema
"""


def main() -> None:
    """Main CLI entry point using FlextDomainService and FlextCommands SOURCE OF TRUTH."""
    try:
        # Create CLI service using Pydantic patterns - SOURCE OF TRUTH
        cli_service = FlextTargetOracleCliService()

        # Execute CLI - direct method call, no wrappers
        result = cli_service.run_cli()

        if result.is_failure:
            logger = FlextLogger(__name__)
            logger.error(result.error or "CLI execution failed")
            sys.exit(1)

    except Exception as e:
        logger = FlextLogger(__name__)
        logger.exception(f"Fatal CLI error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


__all__: FlextTypes.Core.StringList = [
    "FlextTargetOracleCliService",
    "main",
]
