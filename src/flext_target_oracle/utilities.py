"""Utility helpers for Oracle Singer target integration."""

from __future__ import annotations

from pathlib import Path

from flext_core import r
from flext_db_oracle import FlextDbOracleUtilities
from flext_meltano import FlextMeltanoUtilities
from flext_target_oracle import c
from flext_target_oracle._models.config import FlextTargetOracleModelsConfig
from flext_target_oracle.settings import FlextTargetOracleSettings


class FlextTargetOracleUtilities(FlextMeltanoUtilities, FlextDbOracleUtilities):
    """Focused utility namespace used by Oracle target modules."""

    class TargetOracle:
        """Oracle target utility namespace."""

        @staticmethod
        def load_target_settings(
            config_file: str | None,
        ) -> r[FlextTargetOracleModelsConfig.OracleSettingsProtocol]:
            """Load settings from JSON file or environment defaults."""
            result_type: type[
                r[FlextTargetOracleModelsConfig.OracleSettingsProtocol]
            ] = r[FlextTargetOracleModelsConfig.OracleSettingsProtocol]
            if config_file is None:
                return result_type.ok(
                    FlextTargetOracleSettings.model_validate({}),
                )
            config_path = Path(config_file)
            if not config_path.exists():
                return result_type.fail(
                    f"Configuration file not found: {config_file}",
                )
            try:
                content = config_path.read_text(encoding="utf-8")
                settings = FlextTargetOracleSettings.model_validate_json(content)
            except c.Meltano.Singer.SAFE_EXCEPTIONS as exc:
                return result_type.fail(f"Invalid configuration file: {exc}")
            return result_type.ok(settings)


u = FlextTargetOracleUtilities
__all__ = ["FlextTargetOracleUtilities", "u"]
