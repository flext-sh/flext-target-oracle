# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Performance test module.

This module is part of the FLEXT ecosystem. Docstrings follow PEP 257 and Google style.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from tests.performance import test_performance as test_performance
    from tests.performance.test_performance import TestPerformance as TestPerformance

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "TestPerformance": ["tests.performance.test_performance", "TestPerformance"],
    "test_performance": ["tests.performance.test_performance", ""],
}

_EXPORTS: Sequence[str] = [
    "TestPerformance",
    "test_performance",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
