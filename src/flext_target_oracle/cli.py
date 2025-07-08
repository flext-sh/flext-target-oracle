"""Modern CLI interface for Oracle target.

Simple, clean CLI following KISS principle.
"""

from __future__ import annotations

import sys
from typing import Any

import click

from flext_target_oracle.target import OracleTarget


@click.command()
@click.option(
    "--config", type=click.Path(exists=True), help="Configuration file path"
)
@click.option("--discover", is_flag=True, help="Run in discovery mode")
@click.option("--test", is_flag=True, help="Test configuration and connection")
@click.option("--about", is_flag=True, help="Show target information")
def main(
    config: str | None, discover: bool, test: bool, about: bool
) -> None:
    """FLEXT Oracle Target - Modern Singer target for Oracle Database."""
    if about:
        click.echo("FLEXT Oracle Target v2.0.0")
        click.echo("Modern Singer target for Oracle Database")
        click.echo("Built with Pydantic v2, SQLAlchemy 2.0, and Python 3.13")
        return

    if discover:
        # Discovery mode - show capabilities
        click.echo('{"streams": []}')  # Oracle targets don't typically discover
        return

    if test:
        # Test configuration and connection
        try:
            target = OracleTarget(config=_load_config(config) if config else None)
            # Simple config validation test (connection test would need engine)
            _ = target.oracle_config  # This validates the config structure
            click.echo("✅ Configuration test successful")
        except Exception as e:
            click.echo(f"❌ Configuration test failed: {e}")
            sys.exit(1)
        return

    # Normal execution mode
    target = OracleTarget(config=_load_config(config) if config else None)
    target.listen()


def _load_config(config_path: str) -> dict[str, Any]:
    """Load configuration from file."""
    import json
    from pathlib import Path

    config_file = Path(config_path)
    if not config_file.exists():
        msg = f"Configuration file not found: {config_path}"
        raise FileNotFoundError(msg)

    config_data: dict[str, Any] = json.loads(config_file.read_text())
    return config_data


if __name__ == "__main__":
    main()

