"""CLI orchestration for Oracle target."""

from __future__ import annotations

import sys
from typing import ClassVar

from flext_cli import cli
from flext_target_oracle import m, p, r, t, u
from flext_target_oracle.api import FlextTargetOracleService


class FlextTargetOracleCli:
    """CLI service that maps process args to Oracle target commands."""

    logger: ClassVar[p.Logger] = u.fetch_logger(__name__)

    def execute(self) -> p.Result[str]:
        """Service readiness probe."""
        return r[str].ok("CLI ready")

    def finalize_cli_result(self, result: p.Result[str]) -> int:
        """Convert a CLI result into process exit semantics."""
        if result.failure:
            self.logger.error(result.error or "Command failed")
            return 1
        self.logger.info(result.value)
        return 0

    def run_cli(self, args: t.StrSequence | None = None) -> p.Result[str]:
        """Dispatch CLI args to the appropriate command."""
        argv = args if args is not None else sys.argv[1:]
        if not argv or argv[0] in {"help", "-h", "--help"}:
            return r[str].ok(self._get_help_text())
        command_name = argv[0]
        # NOTE (multi-agent): mro-rn88 — CQRS: CLI composes the pure-data Command DTO and
        # hands it to the service handler; execution no longer lives on the model.
        service = FlextTargetOracleService.fetch_global()
        if command_name == "validate":
            return service.run_validate(m.TargetOracle.OracleTargetValidateCommand())
        if command_name == "load":
            return service.run_load(m.TargetOracle.OracleTargetLoadCommand())
        if command_name == "about":
            return service.run_about(m.TargetOracle.OracleTargetAboutCommand())
        return r[str].fail(f"Unknown command: {command_name}")

    def _get_help_text(self) -> str:
        """Return text help for target CLI usage."""
        return "Usage: target-oracle [validate|load|about]\n  validate  validate settings and connection\n  load      initialize target for loading\n  about     show project information"


def main() -> int:
    """Run the Oracle target CLI entrypoint."""
    cli_service = FlextTargetOracleCli()
    return cli_service.finalize_cli_result(cli_service.run_cli())


if __name__ == "__main__":
    cli.exit(main())


__all__: list[str] = ["FlextTargetOracleCli", "main"]
