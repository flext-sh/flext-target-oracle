"""FLEXT Target Oracle - Modern Enterprise Singer Target.

Clean implementation following SOLID, KISS, and DRY principles.
Built with Pydantic v2, Python 3.13 typing, and modern patterns.
"""

from __future__ import annotations

__version__ = "2.0.0"

from flext_target_oracle.config import OracleConfig
from flext_target_oracle.connector import OracleConnector
from flext_target_oracle.sink import OracleSink
from flext_target_oracle.target import OracleTarget

__all__ = [
    "OracleConfig",
    "OracleConnector",
    "OracleSink",
    "OracleTarget",
    "__version__",
]

