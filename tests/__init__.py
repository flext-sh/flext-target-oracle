"""Test module for flext-target-oracle.

This module provides test infrastructure for flext-target-oracle using unified namespace patterns.
Test objects are accessed via m.Oracle.Tests.*, u.Oracle.*, etc.
Combines FlextTests* with project-specific functionality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core._utilities.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from models import m
    from protocols import p
    from typings import t
    from utilities import u

# Lazy import mapping: export_name -> (module_path, attr_name)
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "m": ("models", "m"),
    "p": ("protocols", "p"),
    "t": ("typings", "t"),
    "u": ("utilities", "u"),
}

__all__ = [
    "m",
    "p",
    "t",
    "u",
]


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
