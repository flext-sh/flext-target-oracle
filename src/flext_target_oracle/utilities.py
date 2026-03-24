"""Utility helpers for Oracle Singer target integration."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from flext_core import r
from flext_db_oracle import FlextDbOracleUtilities
from flext_meltano import FlextMeltanoUtilities
from pydantic import TypeAdapter

from flext_target_oracle import t

_CONTAINER_VALUE_ADAPTER: TypeAdapter[t.ContainerValue] = TypeAdapter(t.ContainerValue)


class FlextTargetOracleUtilities(FlextMeltanoUtilities, FlextDbOracleUtilities):
    """Focused utility namespace used by Oracle target modules."""

    class TargetOracle:
        """Singer message operations are handled by Pydantic model constructors."""

    class OracleDataProcessing:
        """Data conversion helpers for Oracle storage."""

        @staticmethod
        def transform_record_for_oracle(
            record: Mapping[str, t.ContainerValue],
        ) -> r[Mapping[str, t.ContainerValue]]:
            """Normalize record values for Oracle persistence."""
            transformed: dict[str, t.ContainerValue] = {}
            for key, value in record.items():
                is_mapping = isinstance(value, Mapping)
                is_sequence = isinstance(value, Sequence) and (
                    not isinstance(value, str | bytes)
                )
                if is_mapping or is_sequence:
                    transformed[key.upper()] = _CONTAINER_VALUE_ADAPTER.dump_json(
                        value
                    ).decode("utf-8")
                    continue
                match value:
                    case bool() as bool_value:
                        transformed[key.upper()] = 1 if bool_value else 0
                    case _:
                        transformed[key.upper()] = value
            return r[t.ContainerValueMapping].ok(transformed)


u = FlextTargetOracleUtilities
__all__ = ["FlextTargetOracleUtilities", "u"]
