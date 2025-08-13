#!/usr/bin/env python3
"""FLEXT Target Oracle - Modern CLI using flext-cli foundation patterns.

Singer Target interface with modern Click CLI integration using flext-cli patterns
with zero boilerplate and maximum integration with FLEXT ecosystem.

Built on Clean Architecture patterns with flext-core integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
import uuid
from dataclasses import dataclass
from pathlib import Path

import click
from flext_cli import CLICommand
from flext_cli.core.helpers import FlextCliHelper
from flext_cli.foundation import (
    create_cli_config as create_flext_cli_config,
    setup_cli as setup_flext_cli,
)
from flext_core import FlextResult, get_logger
from rich.console import Console

from flext_target_oracle.target_client import (
    FlextTargetOracle,
)
from flext_target_oracle.target_config import FlextTargetOracleConfig

logger = get_logger(__name__)
console = Console()

# =============================================================================
# FLEXT-CLI PARAMETER OBJECTS - ELIMINATE ARGUMENT EXPLOSION
# =============================================================================


@dataclass
class OracleTargetValidateParams:
    """Parameter object for Oracle target validation operations - flext-cli pattern."""

    config_file: str | None = None

    @classmethod
    def from_click_args(cls, **kwargs: object) -> OracleTargetValidateParams:
        """Create from Click arguments using flext-cli patterns."""
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
    def from_click_args(cls, **kwargs: object) -> OracleTargetLoadParams:
        """Create from Click arguments using flext-cli patterns."""
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
    def from_click_args(cls, **kwargs: object) -> OracleTargetAboutParams:
        """Create from Click arguments using flext-cli patterns."""
        return cls(
            format=str(kwargs.get("format", "json")),
        )


class OracleTargetValidateCommand(CLICommand):
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
        self.cli_helper = FlextCliHelper()

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate business rules for Oracle target validation."""
        if self.params.config_file and not Path(self.params.config_file).exists():
            return FlextResult.fail(
                f"Configuration file not found: {self.params.config_file}",
            )
        return FlextResult.ok(None)

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
                import os

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
                return FlextResult.fail(
                    validation_result.error or "Configuration validation failed",
                )

            # Test connection
            self.cli_helper.print_info("Testing Oracle database connection...")
            if target._test_connection():
                self.cli_helper.print_success("Oracle target configuration is valid")
                self.cli_helper.print_success("Oracle database connection successful")
                return FlextResult.ok({"status": "valid", "connection": "successful"})
            self.cli_helper.print_error("Oracle database connection failed")
            return FlextResult.fail("Connection test failed")

        except Exception as e:
            logger.exception("Oracle target validation failed")
            self.cli_helper.print_error(f"Validation error: {e}")
            return FlextResult.fail(f"Validation error: {e}")


class OracleTargetLoadCommand(CLICommand):
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
        self.cli_helper = FlextCliHelper()

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate business rules for Oracle target load."""
        if self.params.config_file and not Path(self.params.config_file).exists():
            return FlextResult.fail(
                f"Configuration file not found: {self.params.config_file}",
            )
        if self.params.state_file and not Path(self.params.state_file).exists():
            return FlextResult.fail(
                f"State file not found: {self.params.state_file}",
            )
        return FlextResult.ok(None)

    def execute(self) -> FlextResult[object]:  # noqa: PLR0912, PLR0915
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
                import os

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
                import json

                for line in sys.stdin:
                    stripped_line = line.strip()
                    if stripped_line:
                        message = json.loads(stripped_line)
                        messages.append(message)
            except json.JSONDecodeError as e:
                self.cli_helper.print_error(f"Invalid JSON input: {e}")
                return FlextResult.fail(f"JSON parsing error: {e}")

            if not messages:
                self.cli_helper.print_warning("No Singer messages received from stdin")
                return FlextResult.ok({"messages_processed": 0})

            # Process messages
            self.cli_helper.print_info(f"Processing {len(messages)} Singer messages...")
            messages_processed = 0

            for message in messages:
                if isinstance(message, dict):
                    result = target.process_singer_message(message)
                    if hasattr(result, "__await__"):
                        import asyncio

                        result_value = asyncio.run(result)
                    else:
                        result_value = result  # type: ignore[assignment]
                    if result_value.is_failure:
                        self.cli_helper.print_error(
                            f"Failed to process message: {result_value.error}",
                        )
                        return FlextResult.fail(
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
                import asyncio

                final_result_value = asyncio.run(finalize_result)
            else:
                final_result_value = finalize_result  # type: ignore[assignment]

            if final_result_value.is_success:
                stats = final_result_value.data
                self.cli_helper.print_success("Data loading completed successfully")
                self.cli_helper.print_success(
                    f"Processed {messages_processed} messages",
                )
                if isinstance(stats, dict):
                    total_records = stats.get("total_records", 0)
                    self.cli_helper.print_success(f"Loaded {total_records} records")
                return FlextResult.ok(
                    {"messages_processed": messages_processed, "stats": stats},
                )
            self.cli_helper.print_error(
                f"Finalization failed: {final_result_value.error}",
            )
            return FlextResult.fail(final_result_value.error or "Finalization failed")

        except Exception as e:
            logger.exception("Oracle target load failed")
            self.cli_helper.print_error(f"Load error: {e}")
            return FlextResult.fail(f"Load error: {e}")


class OracleTargetAboutCommand(CLICommand):
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
        self.cli_helper = FlextCliHelper()

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate business rules for Oracle target about."""
        if self.params.format not in {"json", "text"}:
            return FlextResult.fail(
                f"Invalid output format: {self.params.format}. Must be 'json' or 'text'",
            )
        return FlextResult.ok(None)

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

            return FlextResult.ok(about_info)

        except Exception as e:
            logger.exception("Oracle target about failed")
            self.cli_helper.print_error(f"About error: {e}")
            return FlextResult.fail(f"About error: {e}")


# =============================================================================
# MODERN CLICK CLI WITH FLEXT-CLI INTEGRATION
# =============================================================================


@click.group(name="target-oracle")
@click.version_option(version="0.9.0", prog_name="FLEXT Target Oracle")
@click.help_option("--help", "-h")
def cli() -> None:
    """FLEXT Target Oracle - Modern Singer Target for Oracle Database.

    Modern CLI using flext-cli foundation with zero boilerplate.
    Built on Clean Architecture patterns with flext-core integration.
    """
    # Initialize flext-cli
    cli_config_result = create_flext_cli_config(
        debug=False,
        profile="oracle-target",
    )

    if cli_config_result.is_failure:
        console.print(f"[red]CLI configuration failed: {cli_config_result.error}[/red]")
        return

    setup_result = setup_flext_cli(cli_config_result.data)
    if setup_result.is_failure:
        console.print(f"[red]CLI setup failed: {setup_result.error}[/red]")
        return


@cli.command()
@click.option(
    "--config", "-c", "config_file", help="Path to target configuration JSON file",
)
def validate(**kwargs: object) -> None:
    """Validate Oracle target configuration and test connection.

    Example:
        target-oracle validate --config config.json
        target-oracle validate  # Uses environment variables

    """
    params = OracleTargetValidateParams.from_click_args(**kwargs)

    command = OracleTargetValidateCommand(
        command_id=str(uuid.uuid4()),
        name="oracle-validate",
        params=params,
    )

    result = command.execute()
    if result.is_failure:
        console.print(f"[red]Validation failed: {result.error}[/red]")
        sys.exit(1)


@cli.command()
@click.option(
    "--config", "-c", "config_file", help="Path to target configuration JSON file",
)
@click.option("--state", "state_file", help="Path to Singer state file")
def load(**kwargs: object) -> None:
    """Load data into Oracle database using Singer protocol.

    Reads Singer messages from stdin and loads data into Oracle.

    Example:
        cat messages.jsonl | target-oracle load --config config.json
        meltano elt tap-source target-oracle --state state.json

    """
    params = OracleTargetLoadParams.from_click_args(**kwargs)

    command = OracleTargetLoadCommand(
        command_id=str(uuid.uuid4()),
        name="oracle-load",
        params=params,
    )

    result = command.execute()
    if result.is_failure:
        console.print(f"[red]Load failed: {result.error}[/red]")
        sys.exit(1)


@cli.command()
@click.option(
    "--format",
    type=click.Choice(["json", "text"]),
    default="json",
    help="Output format",
)
def about(**kwargs: object) -> None:
    """Display information about the Oracle target.

    Shows target capabilities, configuration options, and metadata.

    Example:
        target-oracle about
        target-oracle about --format text

    """
    params = OracleTargetAboutParams.from_click_args(**kwargs)

    command = OracleTargetAboutCommand(
        command_id=str(uuid.uuid4()),
        name="oracle-about",
        params=params,
    )

    result = command.execute()
    if result.is_failure:
        console.print(f"[red]About failed: {result.error}[/red]")
        sys.exit(1)


def main() -> None:
    """Provide CLI entry point using flext-cli patterns."""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("[blue]Operation cancelled by user[/blue]")
        raise SystemExit(0) from None
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()
