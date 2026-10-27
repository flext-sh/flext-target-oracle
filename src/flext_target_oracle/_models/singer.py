"""Singer message model specializations for Oracle target.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_target_oracle/_models/singer
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Annotated

from flext_meltano import m

from flext_target_oracle import t


class FlextTargetOracleModelsSinger:
    """Oracle-target additions on top of canonical m.Meltano Singer models."""

    class SingerStreamModel(m.ArbitraryTypesModel):
        """Singer stream mapping to Oracle table with column configuration."""

        stream_name: Annotated[
            str,
            m.Field(..., description="Singer stream name", validate_default=True),
        ]
        table_name: Annotated[
            str,
            m.Field(
                ...,
                description="Oracle destination table name",
                validate_default=True,
            ),
        ]
        ignored_columns: Annotated[
            t.StrSequence,
            m.Field(
                ...,
                description="Columns ignored during record transformation",
                validate_default=True,
            ),
        ] = m.Field(default_factory=tuple, validate_default=True)
        column_mappings: Annotated[
            t.StrMapping,
            m.Field(
                ...,
                description="Singer column to Oracle column mapping",
                validate_default=True,
            ),
        ] = m.Field(
            default_factory=lambda: MappingProxyType[str, str]({}),
            validate_default=True,
        )


__all__: list[str] = ["FlextTargetOracleModelsSinger"]
