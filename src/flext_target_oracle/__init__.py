"""FLEXT Target Oracle - Modern Enterprise Singer Target.

Built on flext-core foundation with zero duplication.
Uses flext-db-oracle for all Oracle database operations.
"""

from __future__ import annotations

# Version from flext-core
__version__ = "0.7.0"

# Core imports from flext-core
# Oracle operations from flext-db-oracle (no duplication)
from flext_db_oracle import (
    OracleConfig,
    OracleConnectionService,
    OracleQueryService,
)

from flext_core import DomainBaseModel, ServiceResult
from flext_target_oracle.application.services import (
    OracleLoaderService,
    SingerTargetService,
)

# Target-specific implementations
from flext_target_oracle.domain.models import (
    SingerRecord,
    SingerSchema,
    TargetConfig,
)
from flext_target_oracle.target import OracleTarget

__all__ = [
    "BaseConfig",
    # Re-exported from flext-core
    "DomainBaseModel",
    # Re-exported from flext-db-oracle
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
