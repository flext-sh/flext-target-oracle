"""Singer Target Domain Layer.

Following flext-core DDD patterns.
"""

from flext_target_oracle.domain.models import (
    LoadJob,
    LoadJobStatus,
    LoadMethod,
    LoadStatistics,
    SingerRecord,
    SingerSchema,
    TargetConfig,
)

__all__ = [
    "LoadJob",
    "LoadJobStatus",
    "LoadMethod",
    "LoadStatistics",
    "SingerRecord",
    "SingerSchema",
    "TargetConfig",
]
