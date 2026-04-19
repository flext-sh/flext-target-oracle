"""Base utilities for Target Oracle module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from importlib import import_module
from pathlib import Path

from flext_target_oracle import c, p, r


class FlextTargetOracleUtilitiesBase:
    """Base target Oracle utility namespace."""

    @staticmethod
    def load_target_settings(
        config_file: str | None,
    ) -> p.Result[p.TargetOracle.OracleSettingsProtocol]:
        """Load settings from JSON file or environment defaults."""
        result_type: type[r[p.TargetOracle.OracleSettingsProtocol]] = r[
            p.TargetOracle.OracleSettingsProtocol
        ]
        settings_module = import_module("flext_target_oracle.settings")
        settings_cls = settings_module.FlextTargetOracleSettings

        if config_file is None:
            return result_type.ok(
                settings_cls.model_validate({}),
            )
        config_path = Path(config_file)
        if not config_path.exists():
            return result_type.fail(
                f"Configuration file not found: {config_file}",
            )
        try:
            content = config_path.read_text(encoding="utf-8")
            settings = settings_cls.model_validate_json(content)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            return result_type.fail(f"Invalid configuration file: {exc}")
        return result_type.ok(settings)
