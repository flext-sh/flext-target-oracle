"""Test module for flext-target-oracle.

This module provides test infrastructure for flext-target-oracle using unified namespace patterns.
Test objects are accessed via m.Oracle.Tests.*, u.Oracle.*, etc.
Combines FlextTests* with project-specific functionality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

# Import test module aliases for unified test access
from .models import m
from .protocols import p
from .typings import t
from .utilities import u

__all__ = [
    "m",
    "p",
    "t",
    "u",
]
