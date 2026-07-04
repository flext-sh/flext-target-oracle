"""Singer message model specializations for Oracle target."""

from __future__ import annotations

from types import MappingProxyType
from typing import Annotated

from flext_meltano import m, t, u


class FlextTargetOracleModelsSinger:
    """Oracle-target additions on top of canonical m.Meltano Singer models."""

    class SingerStreamModel(m.ArbitraryTypesModel):
        """Singer stream mapping to Oracle table with column configuration."""

        stream_name: Annotated[str, u.Field(..., description="Singer stream name", validate_default=True)]
        table_name: Annotated[
            str,
            u.Field(..., description="Oracle destination table name", validate_default=True),
        ]
        ignored_columns: Annotated[
            t.StrSequence,
            u.Field(
                ...,
                description="Columns ignored during record transformation",
                validate_default=True,
            ),
        ] = u.Field(default_factory=tuple, validate_default=True)
        column_mappings: Annotated[
            t.StrMapping,
            u.Field(
                ...,
                description="Singer column to Oracle column mapping",
                validate_default=True,
            ),
        ] = u.Field(default_factory=lambda: MappingProxyType({}), validate_default=True)
