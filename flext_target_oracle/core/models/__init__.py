"""Core data models for flext-target-oracle.

These models use Pydantic for validation and immutability,
following Domain-Driven Design principles.
"""

from .batch import Batch, BatchResult, ProcessingStrategy
from .config import OracleConfig, PerformanceConfig, ValidationResult
from .connection import ConnectionConfig, ConnectionInfo, ConnectionStats
from .metrics import Metric, MetricType
from .schema import FieldMetadata, SchemaDefinition, TypeContext

__all__ = [
    # Batch models
    "Batch",
    "BatchResult",
    "ProcessingStrategy",
    # Config models
    "OracleConfig",
    "PerformanceConfig",
    "ValidationResult",
    # Connection models
    "ConnectionConfig",
    "ConnectionInfo",
    "ConnectionStats",
    # Schema models
    "SchemaDefinition",
    "FieldMetadata",
    "TypeContext",
    # Metrics models
    "Metric",
    "MetricType",
]
