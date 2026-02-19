"""Refactored CLI orchestration for Oracle target."""

from __future__ import annotations

import sys

from flext_core import FlextLogger, FlextResult

from .target_commands import OracleTargetCommandFactory

logger = FlextLogger(__name__)


class FlextTargetOracleCliService:
    """Simple CLI service that maps args to command executions."""

    def execute(self) -> FlextResult[str]:
        """Service readiness probe."""
        return FlextResult[str].ok("CLI ready")

    def run_cli(self, args: list[str] | None = None) -> FlextResult[str]:
        """Dispatch CLI args to the appropriate command."""
        argv = args if args is not None else sys.argv[1:]
        if not argv or argv[0] in {"help", "-h", "--help"}:
            return FlextResult[str].ok(self._get_help_text())

        command_name = argv[0]
        if command_name == "validate":
            command = OracleTargetCommandFactory.create_validate_command(None)
            return command.execute()
        if command_name == "load":
            command = OracleTargetCommandFactory.create_load_command(None, None)
            return command.execute()
        if command_name == "about":
            command = OracleTargetCommandFactory.create_about_command("json")
            return command.execute()
        return FlextResult[str].fail(f"Unknown command: {command_name}")

    def _get_help_text(self) -> str:
        """Return text help for target CLI usage."""
        return (
            "Usage: target-oracle [validate|load|about]\n"
            "  validate  validate config and connection\n"
            "  load      initialize target for loading\n"
            "  about     show project information"
        )


def main() -> None:
    """CLI entrypoint."""
    result = FlextTargetOracleCliService().run_cli()
    if result.is_failure:
        logger.error(result.error or "Command failed")
        sys.exit(1)
    if result.value is not None:
        logger.info(result.value)


if __name__ == "__main__":
    main()


__all__ = ["FlextTargetOracleCliService", "main"]
