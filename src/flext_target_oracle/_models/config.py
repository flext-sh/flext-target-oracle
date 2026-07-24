"""flext-target-oracle config models — typed business-rule shapes.

Frozen Pydantic shapes for the ``config/target_oracle.yaml`` business-rule SSOT.
The ``_config.py`` facade validates the model-less YAML slice into these
classes and exposes the ready objects under ``config.TargetOracle``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class FlextTargetOracleConfigModels:
    """Namespace of typed flext-target-oracle config models."""

    class Defaults(BaseModel):
        """Oracle target default loading and connection policy."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        port: int = Field(ge=1, le=65535, description="Default Oracle listener port.")
        max_port: int = Field(
            ge=1, le=65535, description="Maximum valid Oracle listener port."
        )
        target_schema: str = Field(
            description="Default target schema for Singer loads."
        )
        batch_size: int = Field(ge=1, description="Batch size for loading.")
        commit_interval: int = Field(ge=1, description="Commit interval in rows.")
        transaction_timeout: int = Field(
            ge=1, description="Transaction timeout in seconds."
        )
        parallel_degree: int = Field(ge=1, description="Oracle parallel degree.")
        load_method: str = Field(description="Default Oracle load strategy.")
        storage_mode: str = Field(description="Default record storage mode.")
        json_column_name: str = Field(description="JSON payload column name.")
        truncate_before_load: bool = Field(
            description="Whether to truncate before load."
        )
        use_bulk_operations: bool = Field(description="Whether to use bulk operations.")
        autocommit: bool = Field(description="Whether to auto-commit transactions.")

    class Pool(BaseModel):
        """Connection pool defaults."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        min: int = Field(ge=0, description="Minimum pool size.")
        max: int = Field(ge=1, description="Maximum pool size.")

    class CommandTypes(BaseModel):
        """Oracle target CLI command identifiers."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        validate_command: str = Field(description="Validate command identifier.")
        load_command: str = Field(description="Load command identifier.")
        about_command: str = Field(description="About command identifier.")

    class TargetOracle(BaseModel):
        """Root Oracle target business-rule namespace."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        defaults: FlextTargetOracleConfigModels.Defaults = Field(
            description="Oracle target default loading and connection policy."
        )
        pool: FlextTargetOracleConfigModels.Pool = Field(
            description="Connection pool defaults."
        )
        load_methods: tuple[str, ...] = Field(
            description="Supported Oracle load methods."
        )
        storage_modes: tuple[str, ...] = Field(
            description="Supported record storage modes."
        )
        command_types: FlextTargetOracleConfigModels.CommandTypes = Field(
            description="Oracle target CLI command identifiers."
        )
        output_format: str = Field(description="Default CLI output format.")

    class Root(BaseModel):
        """Root flext-target-oracle config validated from ``config/*.yaml``."""

        model_config = ConfigDict(frozen=True, extra="ignore")

        TargetOracle: FlextTargetOracleConfigModels.TargetOracle = Field(
            description="Oracle target business-rule config namespace."
        )


__all__: list[str] = ["FlextTargetOracleConfigModels"]
