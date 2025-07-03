"""
FLEXT Target Oracle - Advanced Singer Target for Oracle Database.

Enhanced implementation with smart error handling:
- Categorized Oracle error handling (critical vs non-critical vs features)
- Enhanced performance optimizations
- Comprehensive logging without masking

Compatible with Python 3.9+
"""

from __future__ import annotations

__version__ = "1.0.0"

# Import core implementations
from .connectors import OracleConnector
from .sinks import OracleSink
from .target import OracleTarget

__all__ = [
    "OracleConnector",  # Shared connector
    "OracleSink",  # Primary implementation
    "OracleTarget",  # Primary implementation
    "__version__",
]
