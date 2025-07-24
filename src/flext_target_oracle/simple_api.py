"""Simple API for FLEXT target-oracle setup and configuration.

Provides a simple interface for setting up Oracle Database data loading.
"""

from __future__ import annotations

# Removed circular dependency - use DI pattern
import logging

# 🚨 ARCHITECTURAL COMPLIANCE
from flext_target_oracle.infrastructure.di_container import (
    get_domain_entity,
    get_field,
    get_service_result,
)

ServiceResult = get_service_result()
DomainEntity = get_domain_entity()
Field = get_field()

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
            config = TargetOracleConfig.model_validate(
                {
                    "host": "localhost",
                    "username": "oracle_user",
                    "password": "oracle_password",
                },
            )

        # Setup logging using flext-infrastructure.monitoring.flext-observability
        # Note: Logging setup is handled globally by flext-observability
        logging.getLogger(__name__)

        return ServiceResult.ok(config)

    except (ValueError, TypeError, RuntimeError, ImportError) as e:
        return ServiceResult.fail(f"Failed to setup Oracle target: {e}")


# Export convenience functions
__all__ = [
    "setup_oracle_target",
]
