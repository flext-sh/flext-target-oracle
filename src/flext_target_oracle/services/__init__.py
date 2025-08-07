"""FLEXT Target Oracle Services - SOLID Architecture Implementation.

This module provides specialized services following Single Responsibility Principle
to replace the monolithic FlextTargetOracleLoader class. Each service has a focused
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

# NOTE: Service modules currently implemented inline in target.py and loader.py
# Future expansion could include dedicated service classes following SOLID principles:
# - OracleBatchProcessor for batch processing operations
# - OracleConnectionManager for connection lifecycle management
# - OracleRecordTransformer for data transformation
# - OracleSchemaManager for schema operations
# - OracleSQLGenerator for SQL statement generation

__all__: list[str] = [
    # Services to be implemented:
    # "OracleBatchProcessor",
    # "OracleConnectionManager",
    # "OracleRecordTransformer",
    # "OracleSQLGenerator",
    # "OracleSchemaManager",
]
