"""Utility helpers for Oracle Singer target integration."""

from __future__ import annotations

import json

from flext_core import FlextResult, t


class FlextTargetOracleUtilities:
    """Focused utility namespace used by Oracle target modules."""

    class TargetOracle:
        """Singer message operations are handled by Pydantic model constructors."""

    class OracleDataProcessing:
        """Data conversion helpers for Oracle storage."""

        @staticmethod
        def transform_record_for_oracle(
            record: dict[str, t.GeneralValueType],
        ) -> FlextResult[dict[str, t.GeneralValueType]]:
            """Normalize record values for Oracle persistence."""
            transformed: dict[str, t.GeneralValueType] = {}
            for key, value in record.items():
                if isinstance(value, (dict, list)):
                    transformed[key.upper()] = json.dumps(value)
                elif isinstance(value, bool):
                    transformed[key.upper()] = 1 if value else 0
                else:
                    transformed[key.upper()] = value
            return FlextResult[dict[str, t.GeneralValueType]].ok(transformed)


u = FlextTargetOracleUtilities

__all__ = ["FlextTargetOracleUtilities", "u"]
