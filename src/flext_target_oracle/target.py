"""FLEXT Target Oracle - Main entry point using SOURCE OF TRUTH patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_target_oracle.target_client import FlextTargetOracle


# Main entry point - minimal wrapper for compatibility
def main() -> None:
    """Main entry point for Oracle Singer Target."""
    import sys

    # For Singer targets, the main entry typically reads from stdin
    # This is a basic stub - full Singer CLI would be handled by Meltano
    sys.exit(0)


if __name__ == "__main__":
    main()


__all__ = [
    "FlextTargetOracle",  # Re-export main class
    "main",
]
