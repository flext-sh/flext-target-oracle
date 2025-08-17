"""Centralized typings facade for flext-target-oracle.

- Extends flext-core types
- Add Target Oracle-specific type aliases and Protocols here
"""

from __future__ import annotations

from flext_core import E, F, FlextTypes as CoreFlextTypes, P, R, T, U, V


class FlextTypes(CoreFlextTypes):
    """Target Oracle domain-specific types can extend here."""


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
