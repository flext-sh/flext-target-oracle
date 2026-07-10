"""FLEXT Target Oracle settings — namespaced under ``settings.TargetOracle``.

Universal fields via MRO; project fields in the ``TargetOracle`` group with
simple scalar types (env-settable). Connection models, table naming and
business validation are performed by consumers from these scalars, not stored
as complex settings fields.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

from flext_core import FlextSettings


class FlextTargetOracleSettings(FlextSettings):
    """Oracle Singer target settings; fields under ``settings.TargetOracle.*``."""

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_TARGET_ORACLE_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    class _TargetOracle(BaseModel):
        """Namespaced Oracle target settings."""

        oracle_host: Annotated[str, Field(default="localhost", description="Oracle host")]
        oracle_port: Annotated[int, Field(default=1521, ge=1, le=65535, description="Oracle port")]
        oracle_service_name: Annotated[str, Field(default="XEPDB1", description="Oracle service/SID")]
        oracle_user: Annotated[str, Field(default="", description="Oracle username")]
        oracle_password: Annotated[str, Field(default="", description="Oracle password")]
        default_target_schema: Annotated[str, Field(default="SINGER_DATA", description="Default target schema")]
        batch_size: Annotated[int, Field(default=1000, ge=1, description="Batch size for loading")]
        commit_interval: Annotated[int, Field(default=1000, ge=1, description="Commit interval")]
        transaction_timeout: Annotated[int, Field(default=30, ge=1, description="Transaction timeout (s)")]
        parallel_degree: Annotated[int, Field(default=1, ge=1, description="Oracle parallel degree")]
        table_prefix: Annotated[str, Field(default="", description="Table name prefix")]
        table_suffix: Annotated[str, Field(default="", description="Table name suffix")]
        load_method: Annotated[str, Field(default="INSERT", description="Oracle load strategy")]
        sdc_mode: Annotated[str, Field(default="insert", description="Singer upsert mode")]
        storage_mode: Annotated[str, Field(default="flattened", description="Record storage mode")]
        json_column_name: Annotated[str, Field(default="DATA", description="JSON payload column")]
        truncate_before_load: Annotated[bool, Field(default=False, description="Truncate before load")]
        column_ordering: Annotated[str, Field(default="", description="Column ordering strategy")]
        column_order_rules: Annotated[
            dict[str, int],
            Field(default_factory=dict, description="Column priority rules"),
        ]
        column_mappings: Annotated[
            dict[str, dict[str, str]],
            Field(default_factory=dict, description="Per-stream Singer-to-Oracle column mappings"),
        ]
        ignored_columns: Annotated[
            list[str],
            Field(default_factory=list, description="Ignored columns"),
        ]
        custom_indexes: Annotated[
            dict[str, list[str]],
            Field(default_factory=dict, description="Per-stream custom index definitions"),
        ]
        use_bulk_operations: Annotated[bool, Field(default=True, description="Use bulk operations")]
        autocommit: Annotated[bool, Field(default=False, description="Auto-commit transactions")]

    if TYPE_CHECKING:
        TargetOracle: _TargetOracle
    else:
        TargetOracle: _TargetOracle = Field(
            default_factory=_TargetOracle,
            description="Namespaced Oracle target settings.",
        )


settings: FlextTargetOracleSettings = FlextTargetOracleSettings.fetch_global()
"""Pre-instantiated project settings singleton — ``from flext_target_oracle import settings``."""

__all__: list[str] = ["FlextTargetOracleSettings", "settings"]
