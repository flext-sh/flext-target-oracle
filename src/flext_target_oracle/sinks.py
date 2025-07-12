# Copyright (c) 2025 FLEXT Team
# Licensed under the MIT License
# SPDX-License-Identifier: MIT

"""Compatibility module for legacy imports.

Exports OracleSink from the main sink module.
"""

from __future__ import annotations

from flext_target_oracle.sink import OracleSink

__all__ = ["OracleSink"]
