"""
FLEXT Target Oracle - Advanced Singer Target for Oracle Database.

Maximizes Singer SDK 0.47.4 and SQLAlchemy 2.0+ features.
Compatible with Python 3.9+
"""

from __future__ import annotations

__version__ = "1.0.0"

from .connectors import OracleConnector
from .sinks import OracleSink
from .target import OracleTarget

__all__ = [
    "OracleTarget",
    "OracleSink",
    "OracleConnector",
    "__version__",
]
