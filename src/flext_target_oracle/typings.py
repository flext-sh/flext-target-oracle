"""Centralized typings facade for flext-target-oracle.

Re-exports flext-core types without duplication - SOURCE OF TRUTH pattern.
Oracle Target-specific type extensions can be added here if needed.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# SOURCE OF TRUTH: Use flext-core types directly, no duplication
from flext_core import E, F, FlextTypes, P, R, T, U, V

__all__ = [
    "E",
    "F",
    "FlextTypes",
    "P",
    "R",
    "T",
    "U",
    "V",
]
