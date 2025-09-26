"""Module docstring."""

from __future__ import annotations

"""Models for Oracle target operations.

This module provides data models for Oracle target operations.
"""

from flext_core import FlextModels


class FlextTargetOracleModels(FlextModels):
    """Models for Oracle target operations.

    Extends FlextModels to avoid duplication and ensure consistency.
    All Oracle target models benefit from FlextModels patterns.
    """

    OracleRecord = dict["str", "object"]
    OracleRecords = list[OracleRecord]
