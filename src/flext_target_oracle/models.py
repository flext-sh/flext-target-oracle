"""Models for Oracle target operations.

This module provides data models for Oracle target operations.
"""

from flext_core import FlextModels


class FlextTargetOracleModels:
    """Models for Oracle target operations."""

    Core = FlextModels

    OracleRecord = dict[str, object]
    OracleRecords = list[OracleRecord]
