"""CLI for FLEXT Target Oracle.

Compatible with Python 3.9+
"""

from __future__ import annotations

from flext_target_oracle.target import OracleTarget


def main() -> None:
    """Main CLI entry point - let Singer SDK handle everything."""
    OracleTarget.cli()


if __name__ == "__main__":
    main()
