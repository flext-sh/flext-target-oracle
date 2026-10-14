"""CLI orchestration for Oracle target.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from typing import ClassVar

from flext_cli import cli

from flext_target_oracle import FlextTargetOracleService, m, p, r, t, u


class FlextTargetOracleCli:
    """CLI service that maps process args to Oracle target commands."""

    logger: ClassVar[p.Logger] = u.fetch_logger(__name__)

    @staticmethod
    def execute() -> p.Result[str]:
        """Service readiness probe.

        Returns:
            The readiness acknowledgement value.

        """
        return r[str].ok("CLI ready")

    def finalize_cli_result(self, result: p.Result[str]) -> int:
        """Convert a CLI result into process exit semantics.

        Returns:
            The resulting ``int``.

        Raises:
            SystemExit: If ``result.failure``.

        """
        if result.failure:
            self.logger.error(result.error or "Command failed")
            raise SystemExit(1)
        self.logger.info(result.value)
        return 0

    def run_cli(self, args: t.StrSequence | None = None) -> p.Result[str]:
        """Dispatch CLI args to the appropriate command.

        Args:
            args: CLI arguments; the first entry selects the command.
                Defaults to ``sys.argv[1:]``.

        Returns:
            The command output, the help text, or a failure result
            naming the unknown command.

        """
        argv = args if args is not None else sys.argv[1:]
        if not argv or argv[0] in {"help", "-h", "--help"}:
            return r[str].ok(self._get_help_text())
        command_name = argv[0]
        # NOTE (multi-agent): mro-rn88 — CQRS: CLI composes the pure-data Command DTO
        # and
        # hands it to the service handler; execution no longer lives on the model.
        service = FlextTargetOracleService.fetch_global()
        if command_name == "validate":
            return service.run_validate(m.TargetOracle.OracleTargetValidateCommand())
        if command_name == "load":
            return service.run_load(m.TargetOracle.OracleTargetLoadCommand())
        if command_name == "about":
            return service.run_about(m.TargetOracle.OracleTargetAboutCommand())
        return r[str].fail(f"Unknown command: {command_name}")

    @staticmethod
    def _get_help_text() -> str:
        """Return text help for target CLI usage."""
        return (
            "Usage: target-oracle [validate|load|about]\n"
            "  validate  validate settings and connection\n"
            "  load      initialize target for loading\n"
            "  about     show project information"
        )


def main() -> int:
    """Run the Oracle target CLI entrypoint.

    Returns:
        The CLI exit code.

    """
    cli_service = FlextTargetOracleCli()
    return cli_service.finalize_cli_result(cli_service.run_cli())


if __name__ == "__main__":
    cli.exit(main())


__all__: list[str] = ["FlextTargetOracleCli", "main"]
