"""FLEXT Target Oracle - Modern Enterprise Singer Target.

Built on flext-core foundation with zero duplication.
Uses flext-infrastructure.databases.flext-db-oracle for all Oracle database operations.
"""

from __future__ import annotations

# Version from flext-core
__version__ = "0.7.0"

# 🚨 ARCHITECTURAL COMPLIANCE
from flext_target_oracle.infrastructure.di_container import (
    get_domain_entity,
    get_field,
    get_service_result,
)

ServiceResult = get_service_result()
DomainEntity = get_domain_entity()
Field = get_field()

# Core imports from flext-core
# Oracle operations from flext-infrastructure.databases.flext-db-oracle (no duplication)
from flext_db_oracle import OracleConfig, OracleConnectionService, OracleQueryService

from flext_target_oracle.application.services import (
    OracleLoaderService,
    SingerTargetService,
)

# Target-specific implementations
from flext_target_oracle.domain.models import SingerRecord, SingerSchema, TargetConfig
from flext_target_oracle.target import OracleTarget

__all__ = [
    # Re-exported from flext-core
    "DomainBaseModel",
    # Re-exported from flext-infrastructure.databases.flext-db-oracle
    "OracleConfig",
    "OracleConnectionService",
    "OracleLoaderService",
    "OracleQueryService",
    # Main target
    "OracleTarget",
    "ServiceResult",
    # Target-specific models
    "SingerRecord",
    "SingerSchema",
    # Target services
    "SingerTargetService",
    "TargetConfig",
    "__version__",
]
