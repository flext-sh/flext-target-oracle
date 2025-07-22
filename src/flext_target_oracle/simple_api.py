"""Simple API for FLEXT target-oracle setup and configuration.

Provides a simple interface for setting up Oracle Database data loading.
"""

from __future__ import annotations

from typing import Any

from flext_core.domain.shared_types import ServiceResult
from flext_observability.logging import setup_logging

from flext_target_oracle.domain.models import TargetConfig as TargetOracleConfig


def setup_oracle_target(
    config: TargetOracleConfig | None = None,
) -> ServiceResult[Any]:
    """Set up Oracle target with configuration.

    Args:
        config: Optional target configuration instance

    Returns:
        ServiceResult containing the target configuration

    """
    try:
        if config is None:
            config = TargetOracleConfig.model_validate(
                {
                    "host": "localhost",
                    "username": "oracle_user",
                    "password": "oracle_password",
                },
            )

        # Setup logging using flext-infrastructure.monitoring.flext-observability
        setup_logging()

        return ServiceResult.ok(config)

    except (ValueError, TypeError, RuntimeError, ImportError) as e:
        return ServiceResult.fail(f"Failed to setup Oracle target: {e}")


# Export convenience functions
__all__ = [
    "setup_oracle_target",
]
