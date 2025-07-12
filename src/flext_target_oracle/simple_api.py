"""Simple API for FLEXT target-oracle setup and configuration.

Provides a simple interface for setting up Oracle Database data loading.
"""

from __future__ import annotations

from flext_core import ServiceResult
from flext_observability.logging import setup_logging
from flext_target_oracle.domain.models import TargetConfig as TargetOracleConfig


def setup_oracle_target(
    config: TargetOracleConfig | None = None,
) -> ServiceResult[TargetOracleConfig]:
    """Set up Oracle target with configuration.

    Args:
        config: Optional target configuration instance

    Returns:
        ServiceResult containing the target configuration

    """
    try:
        if config is None:
            config = TargetOracleConfig()

        # Setup logging using flext-observability
        setup_logging()

        return ServiceResult.ok(config)

    except Exception as e:  # noqa: BLE001
        return ServiceResult.fail(f"Failed to setup Oracle target: {e}")


# Export convenience functions
__all__ = [
    "setup_oracle_target",
]
