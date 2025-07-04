"""Core interfaces for flext-target-oracle.

These interfaces define the contracts that all implementations must follow.
They enable dependency injection and make the system testable and extensible.
"""

from .batch_processor import IBatchProcessor, IBatchValidator
from .connection import IConnection, IConnectionManager, IConnectionPool
from .monitor import IMetricsCollector, IMonitor
from .type_mapper import ITypeMapper, ITypeStrategy, ITypeValidator
from .validator import IConfigValidator, IDataValidator, ISchemaValidator

__all__ = [
    # Batch processing
    "IBatchProcessor",
    "IBatchValidator",
    # Connection management
    "IConnection",
    "IConnectionManager",
    "IConnectionPool",
    # Type mapping
    "ITypeMapper",
    "ITypeStrategy",
    "ITypeValidator",
    # Validation
    "IConfigValidator",
    "IDataValidator",
    "ISchemaValidator",
    # Monitoring
    "IMonitor",
    "IMetricsCollector",
]
