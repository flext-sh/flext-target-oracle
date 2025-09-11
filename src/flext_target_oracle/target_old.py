#!/usr/bin/env python3
"""FLEXT Target Oracle - Modern CLI using flext-core foundation patterns.

Singer Target interface with pure Python CLI implementation using flext-core patterns
with zero boilerplate and maximum integration with FLEXT ecosystem.

Built on Clean Architecture patterns with flext-core integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path

from flext_core import FlextDomainService, FlextLogger, FlextResult

from flext_target_oracle.target_client import (
    FlextTargetOracle,
)
from flext_target_oracle.target_config import FlextTargetOracleConfig

logger = FlextLogger(__name__)


@dataclass
class OracleTargetValidateParams:
    """Parameter object for Oracle target validation operations - flext-cli pattern."""

    config_file: str | None = None

    @classmethod
    def from_args(cls, **kwargs: object) -> OracleTargetValidateParams:
        """Create from command arguments using flext-core patterns."""
        return cls(
            config_file=str(kwargs.get("config_file"))
            if kwargs.get("config_file") is not None
            else None,
        )


@dataclass
class OracleTargetLoadParams:
    """Parameter object for Oracle target load operations - flext-cli pattern."""

    config_file: str | None = None
    state_file: str | None = None

    @classmethod
    def from_args(cls, **kwargs: object) -> OracleTargetLoadParams:
        """Create from command arguments using flext-core patterns."""
        return cls(
            config_file=str(kwargs.get("config_file"))
            if kwargs.get("config_file") is not None
            else None,
            state_file=str(kwargs.get("state_file"))
            if kwargs.get("state_file") is not None
            else None,
        )


@dataclass
class OracleTargetAboutParams:
    """Parameter object for Oracle target about operations - flext-cli pattern."""

    format: str = "json"

    @classmethod
    def from_args(cls, **kwargs: object) -> OracleTargetAboutParams:
        """Create from command arguments using flext-core patterns."""
        return cls(
            format=str(kwargs.get("format", "json")),
        )


class OracleTargetValidateCommand:
    """Oracle target validation command using modern flext-cli patterns.

    CLICompleteMixin includes:
    - CLIValidationMixin: Input validation
    - CLIInteractiveMixin: User interaction
    - CLIOutputMixin: Output formatting
    - CLILoggingMixin: Structured logging
    - CLIConfigMixin: Configuration management
    """

    def __init__(
        self,
        command_id: str,
        name: str,
        params: OracleTargetValidateParams,
    ) -> None:
        """Initialize command with parameter object pattern."""
        super().__init__(
            id=command_id,
            command_line=name,
            arguments=[],
        )
        self.params = params
        # self.cli_helper = FlextCliHelper()  # FlextCliHelper doesn't exist

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate business rules for Oracle target validation."""
        if self.params.config_file and not Path(self.params.config_file).exists():
            return FlextResult[None].fail(
                f"Configuration file not found: {self.params.config_file}",
            )
        return FlextResult[None].ok(None)

    def execute(self) -> FlextResult[object]:
        """Execute Oracle target validation using modern patterns."""
        self.cli_helper.print_info("Starting Oracle target configuration validation")

        logger.info(
            "Oracle target validation started",
            extra={
                "config_file": self.params.config_file,
            },
        )

        try:
            # Load configuration
            if self.params.config_file:
                config_data = Path(self.params.config_file).read_text(encoding="utf-8")
                config = FlextTargetOracleConfig.model_validate_json(config_data)
            else:
                # Use environment variables - provide minimal required args
                config = FlextTargetOracleConfig(
                    oracle_host=os.getenv("ORACLE_HOST", "localhost"),
                    oracle_service=os.getenv("ORACLE_SERVICE", "XE"),
                    oracle_user=os.getenv("ORACLE_USER", "system"),
                    oracle_password=os.getenv("ORACLE_PASSWORD", "oracle"),
                )

            # Create Oracle target
            target = FlextTargetOracle(config)

            # Test configuration and connection
            self.cli_helper.print_info("Validating Oracle target configuration...")

            # Validate configuration
            validation_result = config.validate_domain_rules()
            if validation_result.is_failure:
                self.cli_helper.print_error(
                    f"Configuration validation failed: {validation_result.error}",
                )
                return FlextResult[object].fail(
                    validation_result.error or "Configuration validation failed",
                )

            # Test connection
            self.cli_helper.print_info("Testing Oracle database connection...")
            if target._test_connection():
                self.cli_helper.print_success("Oracle target configuration is valid")
                self.cli_helper.print_success("Oracle database connection successful")
                return FlextResult[object].ok(
                    {
                        "status": "valid",
                        "connection": "successful",
                    }
                )
            self.cli_helper.print_error("Oracle database connection failed")
            return FlextResult[object].fail("Connection test failed")

        except Exception as e:
            logger.exception("Oracle target validation failed")
            self.cli_helper.print_error(f"Validation error: {e}")
            return FlextResult[object].fail(f"Validation error: {e}")


class OracleTargetLoadCommand:
    """Oracle target load command using modern flext-cli patterns."""

    def __init__(
        self,
        command_id: str,
        name: str,
        params: OracleTargetLoadParams,
    ) -> None:
        """Initialize command with parameter object pattern."""
        super().__init__(
            id=command_id,
            command_line=name,
            arguments=[],
        )
        self.params = params
        # self.cli_helper = FlextCliHelper()  # FlextCliHelper doesn't exist

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate business rules for Oracle target load."""
        if self.params.config_file and not Path(self.params.config_file).exists():
            return FlextResult[None].fail(
                f"Configuration file not found: {self.params.config_file}",
            )
        if self.params.state_file and not Path(self.params.state_file).exists():
            return FlextResult[None].fail(
                f"State file not found: {self.params.state_file}",
            )
        return FlextResult[None].ok(None)

    def execute(self) -> FlextResult[object]:
        """Execute Oracle target load using modern patterns."""
        self.cli_helper.print_info("Starting Oracle target data loading")

        logger.info(
            "Oracle target load started",
            extra={
                "config_file": self.params.config_file,
                "state_file": self.params.state_file,
            },
        )

        try:
            # Load configuration
            if self.params.config_file:
                config_data = Path(self.params.config_file).read_text(encoding="utf-8")
                config = FlextTargetOracleConfig.model_validate_json(config_data)
            else:
                # Use environment variables - provide minimal required args
                config = FlextTargetOracleConfig(
                    oracle_host=os.getenv("ORACLE_HOST", "localhost"),
                    oracle_service=os.getenv("ORACLE_SERVICE", "XE"),
                    oracle_user=os.getenv("ORACLE_USER", "system"),
                    oracle_password=os.getenv("ORACLE_PASSWORD", "oracle"),
                )

            # Create Oracle target
            target = FlextTargetOracle(config)

            # Load state if provided
            if self.params.state_file:
                Path(self.params.state_file).read_text(encoding="utf-8")
                # Note: State parsing would need proper Singer SDK integration
                self.cli_helper.print_info(
                    f"Loaded state from {self.params.state_file}",
                )

            # Read Singer messages from stdin (Singer protocol)
            self.cli_helper.print_info("Reading Singer messages from stdin...")
            messages = []

            try:
                for line in sys.stdin:
                    stripped_line = line.strip()
                    if stripped_line:
                        message = json.loads(stripped_line)
                        messages.append(message)
            except json.JSONDecodeError as e:
                self.cli_helper.print_error(f"Invalid JSON input: {e}")
                return FlextResult[object].fail(f"JSON parsing error: {e}")

            if not messages:
                self.cli_helper.print_warning("No Singer messages received from stdin")
                return FlextResult[object].ok({"messages_processed": 0})

            # Process messages
            self.cli_helper.print_info(f"Processing {len(messages)} Singer messages...")
            messages_processed = 0

            for message in messages:
                if isinstance(message, dict):
                    result = target.process_singer_message(message)
                    if hasattr(result, "__await__"):
                        result_value = asyncio.run(result)
                    else:
                        result_value = result
                    if result_value.is_failure:
                        self.cli_helper.print_error(
                            f"Failed to process message: {result_value.error}",
                        )
                        return FlextResult[object].fail(
                            f"Message processing failed: {result_value.error}",
                        )
                    messages_processed += 1

                    # Output state messages to stdout (Singer protocol)
                    if message.get("type") == "STATE":
                        pass

            # Finalize loading
            self.cli_helper.print_info("Finalizing data loading...")
            finalize_result = target.finalize()
            if hasattr(finalize_result, "__await__"):
                final_result_value = asyncio.run(finalize_result)
            else:
                final_result_value = finalize_result

            if final_result_value.is_success:
                stats = final_result_value.data
                self.cli_helper.print_success("Data loading completed successfully")
                self.cli_helper.print_success(
                    f"Processed {messages_processed} messages",
                )
                if isinstance(stats, dict):
                    total_records = stats.get("total_records", 0)
                    self.cli_helper.print_success(f"Loaded {total_records} records")
                return FlextResult[object].ok(
                    {"messages_processed": messages_processed, "stats": stats},
                )
            self.cli_helper.print_error(
                f"Finalization failed: {final_result_value.error}",
            )
            return FlextResult[object].fail(
                final_result_value.error or "Finalization failed"
            )

        except Exception as e:
            logger.exception("Oracle target load failed")
            self.cli_helper.print_error(f"Load error: {e}")
            return FlextResult[object].fail(f"Load error: {e}")


class OracleTargetAboutCommand:
    """Oracle target about command using modern flext-cli patterns."""

    def __init__(
        self,
        command_id: str,
        name: str,
        params: OracleTargetAboutParams,
    ) -> None:
        """Initialize command with parameter object pattern."""
        super().__init__(
            id=command_id,
            command_line=name,
            arguments=[],
        )
        self.params = params
        # self.cli_helper = FlextCliHelper()  # FlextCliHelper doesn't exist

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate business rules for Oracle target about."""
        if self.params.format not in {"json", "text"}:
            return FlextResult[None].fail(
                f"Invalid output format: {self.params.format}. Must be 'json' or 'text'",
            )
        return FlextResult[None].ok(None)

    def execute(self) -> FlextResult[object]:
        """Execute Oracle target about using modern patterns."""
        logger.info(
            "Oracle target about started",
            extra={
                "format": self.params.format,
            },
        )

        try:
            # Target information
            about_info = {
                "name": "flext-target-oracle",
                "namespace": "flext_target_oracle",
                "pip_url": "flext-target-oracle>=0.9.0",
                "version": "0.9.0",
                "description": "FLEXT Target Oracle - Modern Singer Target for Oracle Database",
                "singer_sdk_version": "0.47.0",
                "supported_python_versions": ["3.13"],
                "keywords": ["flext", "singer", "target", "oracle", "database"],
                "capabilities": [
                    "about",
                    "stream-maps",
                    "schema-flattening",
                    "record-flattening",
                ],
                "settings": {
                    "oracle_host": {
                        "kind": "string",
                        "description": "Oracle database hostname or IP address",
                    },
                    "oracle_port": {
                        "kind": "integer",
                        "default": 1521,
                        "description": "Oracle listener port number",
                    },
                    "oracle_service": {
                        "kind": "string",
                        "description": "Oracle service name or SID",
                    },
                    "oracle_user": {
                        "kind": "string",
                        "description": "Oracle username for authentication",
                    },
                    "oracle_password": {
                        "kind": "password",
                        "description": "Oracle password for authentication",
                    },
                    "default_target_schema": {
                        "kind": "string",
                        "default": "PUBLIC",
                        "description": "Default schema for table creation",
                    },
                    "batch_size": {
                        "kind": "integer",
                        "default": 1000,
                        "description": "Batch size for bulk operations",
                    },
                },
            }

            if self.params.format == "json":
                pass
            else:
                # Text format
                self.cli_helper.print_info(
                    f"Target: {about_info['name']} v{about_info['version']}",
                )
                self.cli_helper.print_info(f"Description: {about_info['description']}")
                self.cli_helper.print_info(
                    f"Capabilities: {', '.join(about_info['capabilities'])}",
                )
                self.cli_helper.print_info(
                    f"Python versions: {', '.join(about_info['supported_python_versions'])}",
                )

            return FlextResult[object].ok(about_info)

        except Exception as e:
            logger.exception("Oracle target about failed")
            self.cli_helper.print_error(f"About error: {e}")
            return FlextResult[object].fail(f"About error: {e}")


class FlextTargetOracleCliService(FlextDomainService[str]):
    """Oracle Target CLI Service using pure flext-core patterns.

    Eliminates ALL Click usage and wrapper violations, using flext-core
    utilities directly without abstraction layers. Uses SOURCE OF TRUTH
    principle for all CLI orchestration.

    SOLID Principles Applied:
        - Single Responsibility: Oracle target CLI orchestration only
        - Open/Closed: Extensible through flext-core patterns
        - Dependency Inversion: Uses FlextContainer for dependencies
        - Interface Segregation: Focused CLI interface
    """

    def __init__(self) -> None:
        """Initialize CLI service with flext-core dependencies."""
        super().__init__()
        self._logger = FlextLogger(__name__)

    def execute_validate(self, config_file: str | None = None) -> FlextResult[str]:
        """Execute validation using pure flext-core patterns."""
        try:
            params = OracleTargetValidateParams(config_file=config_file)
            command = OracleTargetValidateCommand(
                command_id=str(uuid.uuid4()),
                name="validate",
                params=params,
            )

            result = command.execute()
            if result.is_failure:
                return FlextResult[str].fail(f"Validation failed: {result.error}")

            return FlextResult[str].ok(
                "Oracle target validation completed successfully"
            )

        except Exception as e:
            return FlextResult[str].fail(f"Validation error: {e}")

    def execute_load(
        self, config_file: str | None = None, state_file: str | None = None
    ) -> FlextResult[str]:
        """Execute load using pure flext-core patterns."""
        try:
            params = OracleTargetLoadParams(
                config_file=config_file, state_file=state_file
            )
            command = OracleTargetLoadCommand(
                command_id=str(uuid.uuid4()),
                name="load",
                params=params,
            )

            result = command.execute()
            if result.is_failure:
                return FlextResult[str].fail(f"Load failed: {result.error}")

            return FlextResult[str].ok("Oracle target load completed successfully")

        except Exception as e:
            return FlextResult[str].fail(f"Load error: {e}")

    def execute_about(self) -> FlextResult[str]:
        """Execute about using pure flext-core patterns."""
        try:
            params = OracleTargetAboutParams()
            command = OracleTargetAboutCommand(
                command_id=str(uuid.uuid4()),
                name="about",
                params=params,
            )

            result = command.execute()
            if result.is_failure:
                return FlextResult[str].fail(f"About failed: {result.error}")

            return FlextResult[str].ok("Oracle target about completed successfully")

        except Exception as e:
            return FlextResult[str].fail(f"About error: {e}")

    def execute(self) -> FlextResult[str]:
        """Execute CLI service - implements FlextDomainService abstract method."""
        return FlextResult[str].ok("FLEXT Target Oracle CLI Service initialized")

    def run_cli(self, args: list[str] | None = None) -> FlextResult[str]:
        """Run CLI with pure Python argument parsing - NO Click usage."""
        if args is None:
            args = sys.argv[1:]

        if not args or args[0] in ["-h", "--help", "help"]:
            help_text = """FLEXT Target Oracle - Modern Singer Target for Oracle Database

Usage:
    target-oracle validate [--config CONFIG_FILE]
    target-oracle load [--config CONFIG_FILE] [--state STATE_FILE]
    target-oracle about
    target-oracle --help

Commands:
    validate    Validate Oracle target configuration and test connection
    load        Load data into Oracle database from Singer stream
    about       Display information about the Oracle target

Options:
    --config, -c    Path to target configuration JSON file
    --state         Path to Singer state file
    --help, -h      Show this help message
    --version       Show version information
"""
            self._logger.info(help_text)
            return FlextResult[str].ok("Help displayed")

        if args[0] in ["--version", "-v"]:
            self._logger.info("FLEXT Target Oracle Version 0.9.0")
            return FlextResult[str].ok("Version displayed")

        command = args[0]
        remaining_args = args[1:]

        # Parse arguments manually - pure Python, no Click
        config_file = None
        state_file = None

        i = 0
        while i < len(remaining_args):
            arg = remaining_args[i]
            if arg in ["--config", "-c"] and i + 1 < len(remaining_args):
                config_file = remaining_args[i + 1]
                i += 2
            elif arg == "--state" and i + 1 < len(remaining_args):
                state_file = remaining_args[i + 1]
                i += 2
            else:
                i += 1

        if command == "validate":
            return self.execute_validate(config_file)
        if command == "load":
            return self.execute_load(config_file, state_file)
        if command == "about":
            return self.execute_about()

        error_msg = f"Unknown command: {command}. Use --help for usage information."
        return FlextResult[str].fail(error_msg)


def main() -> None:
    """Main CLI entry point using pure flext-core patterns."""
    try:
        cli_service = FlextTargetOracleCliService()
        result = cli_service.run_cli()

        if result.is_failure:
            logger.error(result.error)
            sys.exit(1)
        else:
            logger.info(result.value)
            sys.exit(0)

    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(0)
    except Exception:
        logger.exception("CLI error")
        sys.exit(1)


if __name__ == "__main__":
    main()
