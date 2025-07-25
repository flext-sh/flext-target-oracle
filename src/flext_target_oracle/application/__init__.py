"""Singer Target Application Layer.

Following flext-core application service patterns.
"""

from flext_target_oracle.application.services import (
    FlextOracleLoaderService,
    FlextSingerTargetService,
)

__all__ = [
    "FlextOracleLoaderService",
    "FlextSingerTargetService",
]
