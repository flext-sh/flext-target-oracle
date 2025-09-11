#!/usr/bin/env python3
"""FLEXT Target Oracle - Main entry point using SOURCE OF TRUTH patterns.

This module provides the main entry point for the Oracle Singer Target with 
clean architecture and SOLID compliance.

ZERO DUPLICATION - Uses FlextTargetOracle from target_client exclusively.
SOLID COMPLIANCE - Single responsibility: Main entry point only.

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
    print("FLEXT Target Oracle - Use with Meltano or Singer CLI")
    print("Direct Python usage: from flext_target_oracle import FlextTargetOracle")
    sys.exit(0)


if __name__ == "__main__":
    main()


__all__ = [
    "FlextTargetOracle",  # Re-export main class
    "main",
]