"""FLEXT Target Oracle settings — namespaced under ``settings.TargetOracle``.

Universal fields via MRO; project fields in the ``TargetOracle`` group with
simple scalar types (env-settable). Connection models, table naming and
business validation are performed by consumers from these scalars, not stored
as complex settings fields.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Annotated

from flext_core import FlextSettings, m, t, u


class FlextTargetOracleSettings(FlextSettings):
    """Oracle Singer target settings; fields under ``settings.TargetOracle.*``."""

    model_config = m.SettingsConfigDict(
        env_prefix="FLEXT_TARGET_ORACLE_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    class _TargetOracle(m.StrictModel):
        """Namespaced Oracle target settings."""

        oracle_host: Annotated[str, m.Field(description="Oracle host")] = "localhost"
        oracle_port: Annotated[
            int, m.Field(ge=1, le=65535, description="Oracle port")
        ] = 1521
        oracle_service_name: Annotated[
            str, m.Field(description="Oracle service/SID")
        ] = "XEPDB1"
        oracle_user: Annotated[str, m.Field(description="Oracle username")] = ""
        oracle_password: Annotated[str, m.Field(description="Oracle password")] = ""
        default_target_schema: Annotated[
            str, m.Field(description="Default target schema")
        ] = "SINGER_DATA"
        batch_size: Annotated[
            int, m.Field(ge=1, description="Batch size for loading")
        ] = 1000
        commit_interval: Annotated[
            int, m.Field(ge=1, description="Commit interval")
        ] = 1000
        transaction_timeout: Annotated[
            int, m.Field(ge=1, description="Transaction timeout (s)")
        ] = 30
        parallel_degree: Annotated[
            int, m.Field(ge=1, description="Oracle parallel degree")
        ] = 1
        table_prefix: Annotated[str, m.Field(description="Table name prefix")] = ""
        table_suffix: Annotated[str, m.Field(description="Table name suffix")] = ""
        load_method: Annotated[str, m.Field(description="Oracle load strategy")] = (
            "INSERT"
        )
        sdc_mode: Annotated[str, m.Field(description="Singer upsert mode")] = "insert"
        storage_mode: Annotated[str, m.Field(description="Record storage mode")] = (
            "flattened"
        )
        json_column_name: Annotated[str, m.Field(description="JSON payload column")] = (
            "DATA"
        )
        truncate_before_load: Annotated[
            bool, m.Field(description="Truncate before load")
        ] = False
        column_ordering: Annotated[
            str, m.Field(description="Column ordering strategy")
        ] = ""
        column_order_rules: Annotated[
            Mapping[str, int], m.Field(description="Column priority rules")
        ] = m.Field(default_factory=u.empty(t.TypeForm(Mapping[str, int])))
        column_mappings: Annotated[
            str,
            m.Field(
                description="Per-stream Singer-to-Oracle column mappings (JSON)",
            ),
        ] = "{}"
        ignored_columns: Annotated[
            Sequence[str], m.Field(description="Ignored columns")
        ] = m.Field(default_factory=tuple)
        custom_indexes: Annotated[
            str,
            m.Field(
                description="Per-stream custom index definitions (JSON)",
            ),
        ] = "{}"
        use_bulk_operations: Annotated[
            bool, m.Field(description="Use bulk operations")
        ] = True
        autocommit: Annotated[bool, m.Field(description="Auto-commit transactions")] = (
            False
        )

    if TYPE_CHECKING:
        TargetOracle: _TargetOracle
    else:
        TargetOracle: _TargetOracle = m.Field(
            default_factory=_TargetOracle,
            description="Namespaced Oracle target settings.",
        )


settings: FlextTargetOracleSettings = FlextTargetOracleSettings.fetch_global()
"""Pre-instantiated project settings singleton.

Exposed as ``from flext_target_oracle import settings``.
"""

__all__: list[str] = ["FlextTargetOracleSettings", "settings"]
