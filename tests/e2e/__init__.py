# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""End-to-end tests for flext-data.targets.flext-target-oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from tests.e2e import test_singer
    from tests.e2e.test_singer import TestSingerWorkflowE2E

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "TestSingerWorkflowE2E": "tests.e2e.test_singer",
    "test_singer": "tests.e2e.test_singer",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
