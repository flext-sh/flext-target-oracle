"""Target Models for FLEXT Target Oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from .constants import c
from .models import m

PUBLIC = "PUBLIC"


class OracleConnectionModel(m.TargetOracle.OracleConnectionConfig):
    """Oracle database connection configuration model."""


class SingerStreamModel(m.ArbitraryTypesModel):
    """Singer stream mapping to Oracle table with column configuration."""

    stream_name: Annotated[str, Field(description="Singer stream name")]
    table_name: Annotated[str, Field(description="Oracle destination table name")]
    ignored_columns: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="Columns ignored during record transformation",
        ),
    ]
    column_mappings: Annotated[
        dict[str, str],
        Field(
            default_factory=dict,
            description="Singer column to Oracle column mapping",
        ),
    ]


class LoadStatisticsModel(m.ArbitraryTypesModel):
    """Statistics for data load operation."""

    stream_name: Annotated[str, Field(description="Stream identifier")]
    total_records_processed: Annotated[
        int,
        Field(
            ge=0,
            description="Total processed records",
        ),
    ]
    successful_records: Annotated[int, Field(ge=0, description="Successful records")]
    failed_records: Annotated[int, Field(ge=0, description="Failed records")]
    batches_processed: Annotated[int, Field(ge=0, description="Processed batch count")]

    def finalize(self) -> LoadStatisticsModel:
        """Finalize statistics and return self."""
        return self


LoadMethodModel = c.LoadMethod
StorageModeModel = c.StorageMode
__all__ = [
    "LoadMethodModel",
    "LoadStatisticsModel",
    "OracleConnectionModel",
    "SingerStreamModel",
    "StorageModeModel",
]
