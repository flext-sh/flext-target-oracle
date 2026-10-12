"""Settings bootstrap utilities for the Oracle target.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_target_oracle import FlextTargetOracleSettings, c, p, r


class FlextTargetOracleUtilitiesBootstrap:
    """Bootstraps Oracle target settings from files or environment defaults."""

    @staticmethod
    def load_target_settings(
        config_file: str | None,
    ) -> p.Result[FlextTargetOracleSettings]:
        """Load settings from a JSON file or environment defaults.

        Returns:
            The resulting ``p.Result[FlextTargetOracleSettings]``.
        """
        result_type: type[r[FlextTargetOracleSettings]] = r[FlextTargetOracleSettings]
        if config_file is None:
            return result_type.ok(FlextTargetOracleSettings.model_validate({}))
        config_path = Path(config_file)
        if not config_path.exists():
            return result_type.fail(f"Configuration file not found: {config_file}")
        try:
            content = config_path.read_text(encoding=c.DEFAULT_ENCODING)
            settings = FlextTargetOracleSettings.model_validate_json(content)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            return result_type.fail(f"Invalid configuration file: {exc}")
        return result_type.ok(settings)


__all__: list[str] = ["FlextTargetOracleUtilitiesBootstrap"]
