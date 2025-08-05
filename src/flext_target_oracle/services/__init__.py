"""FLEXT Target Oracle Services - SOLID Architecture Implementation.

This module provides specialized services following Single Responsibility Principle
to replace the monolithic FlextOracleTargetLoader class. Each service has a focused
responsibility and uses dependency injection via FlextContainer.

Services:
    OracleConnectionManager: Connection lifecycle management
    OracleSchemaManager: Table creation and schema operations
    OracleBatchProcessor: Batch processing logic
    OracleSQLGenerator: SQL generation for different operations
    OracleRecordTransformer: Record transformation and flattening

Following docs/patterns/foundation.md:
    - FlextResult for all operations
    - FlextEntity/FlextValue where appropriate
    - Constructor injection via dependencies
    - Interface segregation with protocols

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from .batch_processor import OracleBatchProcessor
from .connection_manager import OracleConnectionManager
from .record_transformer import OracleRecordTransformer
from .schema_manager import OracleSchemaManager
from .sql_generator import OracleSQLGenerator

__all__ = [
    "OracleBatchProcessor",
    "OracleConnectionManager",
    "OracleRecordTransformer",
    "OracleSQLGenerator",
    "OracleSchemaManager",
]
