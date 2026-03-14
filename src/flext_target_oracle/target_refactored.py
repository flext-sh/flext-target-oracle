"""Refactored CLI orchestration for Oracle target."""

from __future__ import annotations

import sys

from flext_core import FlextLogger, r

from .target_commands import OracleTargetCommandFactory

logger = FlextLogger(__name__)


class FlextTargetOracleCliService:
    """Simple CLI service that maps args to command executions."""

    def execute(self) -> r[str]:
        """Service readiness probe."""
        return r[str].ok("CLI ready")

    def run_cli(self, args: list[str] | None = None) -> r[str]:
        """Dispatch CLI args to the appropriate command."""
        argv = args if args is not None else sys.argv[1:]
        if not argv or argv[0] in {"help", "-h", "--help"}:
            return r[str].ok(self._get_help_text())
        command_name = argv[0]
        if command_name == "validate":
            return OracleTargetCommandFactory.create_validate_command(None).execute()
        if command_name == "load":
            return OracleTargetCommandFactory.create_load_command(None, None).execute()
        if command_name == "about":
            return OracleTargetCommandFactory.create_about_command("json").execute()
        return r[str].fail(f"Unknown command: {command_name}")

    def _get_help_text(self) -> str:
        """Return text help for target CLI usage."""
        return "Usage: target-oracle [validate|load|about]\n  validate  validate config and connection\n  load      initialize target for loading\n  about     show project information"


def main() -> int:
    """CLI entrypoint."""
    result = FlextTargetOracleCliService().run_cli()
    if result.is_failure:
        logger.error(result.error or "Command failed")
        return 1
    logger.info(result.value)
    return 0


if __name__ == "__main__":
    sys.exit(main())
__all__ = ["FlextTargetOracleCliService", "main"]
