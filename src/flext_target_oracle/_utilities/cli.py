"""Refactored CLI orchestration for Oracle target."""

from __future__ import annotations

import sys
from typing import ClassVar

from flext_meltano import u

from flext_target_oracle import m, p, r, t

OracleTargetCommandFactory = m.TargetOracle.OracleTargetCommandFactory


class FlextTargetOracleCliService:
    """Simple CLI service that maps args to command executions."""

    _logger: ClassVar[p.Logger] = u.fetch_logger(__name__)

    def execute(self) -> p.Result[str]:
        """Service readiness probe."""
        return r[str].ok("CLI ready")

    def finalize_cli_result(self, result: p.Result[str]) -> int:
        """Convert a CLI result into process exit semantics."""
        if result.failure:
            self._logger.error(result.error or "Command failed")
            return 1
        self._logger.info(result.value)
        return 0

    def run_cli(self, args: t.StrSequence | None = None) -> p.Result[str]:
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
        return "Usage: target-oracle [validate|load|about]\n  validate  validate settings and connection\n  load      initialize target for loading\n  about     show project information"


def main() -> int:
    """CLI entrypoint."""
    cli_service = FlextTargetOracleCliService()
    return cli_service.finalize_cli_result(cli_service.run_cli())


if __name__ == "__main__":
    sys.exit(main())
__all__: list[str] = ["FlextTargetOracleCliService", "main"]
