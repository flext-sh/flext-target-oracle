"""Singer message model specializations for Oracle target."""

from __future__ import annotations

from types import MappingProxyType
from typing import Annotated

from flext_meltano import m, t, u


class FlextTargetOracleModelsSinger:
    """Oracle-target additions on top of canonical m.Meltano Singer models."""

    class SingerStreamModel(m.ArbitraryTypesModel):
        """Singer stream mapping to Oracle table with column configuration."""

        stream_name: Annotated[str, u.Field(description="Singer stream name")]
        table_name: Annotated[
            str,
            u.Field(description="Oracle destination table name"),
        ]
        ignored_columns: Annotated[
            t.StrSequence,
            u.Field(
                description="Columns ignored during record transformation",
            ),
        ] = u.Field(default_factory=tuple)
        column_mappings: Annotated[
            t.StrMapping,
            u.Field(
                description="Singer column to Oracle column mapping",
            ),
        ] = u.Field(default_factory=lambda: MappingProxyType({}))
