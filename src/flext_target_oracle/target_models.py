"""Target Models for FLEXT Target Oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pydantic import Field

from flext_target_oracle.constants import c

from .models import m

PUBLIC = "PUBLIC"


class OracleConnectionModel(m.TargetOracle.OracleConnectionConfig):
    pass


class SingerStreamModel(m.ArbitraryTypesModel):
    stream_name: str = Field(description="Singer stream name")
    table_name: str = Field(description="Oracle destination table name")
    ignored_columns: list[str] = Field(
        default_factory=list,
        description="Columns ignored during record transformation",
    )
    column_mappings: dict[str, str] = Field(
        default_factory=dict,
        description="Singer column to Oracle column mapping",
    )


class LoadStatisticsModel(m.ArbitraryTypesModel):
    stream_name: str = Field(description="Stream identifier")
    total_records_processed: int = Field(
        ge=0,
        description="Total processed records",
    )
    successful_records: int = Field(ge=0, description="Successful records")
    failed_records: int = Field(ge=0, description="Failed records")
    batches_processed: int = Field(ge=0, description="Processed batch count")

    def finalize(self) -> LoadStatisticsModel:
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
