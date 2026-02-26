"""Utility helpers for Oracle Singer target integration."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence

from flext_core import FlextResult, t


class FlextTargetOracleUtilities:
    """Focused utility namespace used by Oracle target modules."""

    class TargetOracle:
        """Singer message operations are handled by Pydantic model constructors."""

    class OracleDataProcessing:
        """Data conversion helpers for Oracle storage."""

        @staticmethod
        def transform_record_for_oracle(
            record: Mapping[str, t.GeneralValueType],
        ) -> FlextResult[Mapping[str, t.GeneralValueType]]:
            """Normalize record values for Oracle persistence."""
            transformed: dict[str, t.GeneralValueType] = {}
            for key, value in record.items():
                is_mapping = isinstance(value, Mapping)
                is_sequence = isinstance(value, Sequence) and not isinstance(
                    value,
                    str | bytes,
                )
                if is_mapping or is_sequence:
                    transformed[key.upper()] = json.dumps(value)
                    continue
                match value:
                    case bool() as bool_value:
                        transformed[key.upper()] = 1 if bool_value else 0
                    case _:
                        transformed[key.upper()] = value
            return FlextResult[Mapping[str, t.GeneralValueType]].ok(transformed)


u = FlextTargetOracleUtilities

__all__ = ["FlextTargetOracleUtilities", "u"]
