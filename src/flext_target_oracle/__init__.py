"""Production-Grade Singer Target for Oracle Database data loading.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextResult
    from flext_meltano import (
        FlextMeltanoSettings,
        FlextMeltanoTargetAbstractions,
        FlextMeltanoTypes,
    )

    from flext_target_oracle.constants import (
        FlextTargetOracleConstants,
        FlextTargetOracleConstants as c,
    )
    from flext_target_oracle.models import (
        FlextTargetOracleModels,
        FlextTargetOracleModels as m,
    )
    from flext_target_oracle.protocols import (
        FlextTargetOracleProtocols,
        FlextTargetOracleProtocols as p,
    )
    from flext_target_oracle.settings import FlextTargetOracleSettings, LoadMethod
    from flext_target_oracle.target_client import FlextTargetOracle
    from flext_target_oracle.target_commands import OracleTargetCommandFactory
    from flext_target_oracle.target_exceptions import (
        FlextTargetOracleAuthenticationError,
        FlextTargetOracleConnectionError,
        FlextTargetOracleError,
        FlextTargetOracleProcessingError,
        FlextTargetOracleSchemaError,
    )
    from flext_target_oracle.target_loader import FlextTargetOracleLoader
    from flext_target_oracle.target_models import (
        LoadMethodModel,
        LoadStatisticsModel,
        OracleConnectionModel,
        SingerStreamModel,
        StorageModeModel,
    )
    from flext_target_oracle.target_observability import (
        FlextOracleError,
        FlextOracleObs,
        configure_oracle_observability,
    )
    from flext_target_oracle.target_refactored import FlextTargetOracleCliService
    from flext_target_oracle.target_services import (
        BatchServiceProtocol,
        ConnectionServiceProtocol,
        OracleBatchService,
        OracleConnectionService,
        OracleRecordService,
        OracleSchemaService,
        OracleTargetServiceFactory,
        RecordServiceProtocol,
        SchemaServiceProtocol,
    )
    from flext_target_oracle.typings import (
        FlextTargetOracleTypes,
        FlextTargetOracleTypes as t,
    )
    from flext_target_oracle.utilities import (
        FlextTargetOracleUtilities,
        FlextTargetOracleUtilities as u,
    )

# Lazy import mapping: export_name -> (module_path, attr_name)
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "BatchServiceProtocol": (
        "flext_target_oracle.target_services",
        "BatchServiceProtocol",
    ),
    "ConnectionServiceProtocol": (
        "flext_target_oracle.target_services",
        "ConnectionServiceProtocol",
    ),
    "FlextMeltanoSettings": ("flext_meltano", "FlextMeltanoSettings"),
    "FlextMeltanoTargetAbstractions": (
        "flext_meltano",
        "FlextMeltanoTargetAbstractions",
    ),
    "FlextMeltanoTypes": ("flext_meltano", "FlextMeltanoTypes"),
    "FlextOracleError": (
        "flext_target_oracle.target_observability",
        "FlextOracleError",
    ),
    "FlextOracleObs": ("flext_target_oracle.target_observability", "FlextOracleObs"),
    "FlextResult": ("flext_core", "FlextResult"),
    "FlextTargetOracle": ("flext_target_oracle.target_client", "FlextTargetOracle"),
    "FlextTargetOracleAuthenticationError": (
        "flext_target_oracle.target_exceptions",
        "FlextTargetOracleAuthenticationError",
    ),
    "FlextTargetOracleCliService": (
        "flext_target_oracle.target_refactored",
        "FlextTargetOracleCliService",
    ),
    "FlextTargetOracleConnectionError": (
        "flext_target_oracle.target_exceptions",
        "FlextTargetOracleConnectionError",
    ),
    "FlextTargetOracleConstants": (
        "flext_target_oracle.constants",
        "FlextTargetOracleConstants",
    ),
    "FlextTargetOracleError": (
        "flext_target_oracle.target_exceptions",
        "FlextTargetOracleError",
    ),
    "FlextTargetOracleLoader": (
        "flext_target_oracle.target_loader",
        "FlextTargetOracleLoader",
    ),
    "FlextTargetOracleModels": (
        "flext_target_oracle.models",
        "FlextTargetOracleModels",
    ),
    "FlextTargetOracleProcessingError": (
        "flext_target_oracle.target_exceptions",
        "FlextTargetOracleProcessingError",
    ),
    "FlextTargetOracleProtocols": (
        "flext_target_oracle.protocols",
        "FlextTargetOracleProtocols",
    ),
    "FlextTargetOracleSchemaError": (
        "flext_target_oracle.target_exceptions",
        "FlextTargetOracleSchemaError",
    ),
    "FlextTargetOracleSettings": (
        "flext_target_oracle.settings",
        "FlextTargetOracleSettings",
    ),
    "FlextTargetOracleTypes": ("flext_target_oracle.typings", "FlextTargetOracleTypes"),
    "FlextTargetOracleUtilities": (
        "flext_target_oracle.utilities",
        "FlextTargetOracleUtilities",
    ),
    "LoadMethod": ("flext_target_oracle.settings", "LoadMethod"),
    "LoadMethodModel": ("flext_target_oracle.target_models", "LoadMethodModel"),
    "LoadStatisticsModel": ("flext_target_oracle.target_models", "LoadStatisticsModel"),
    "OracleBatchService": ("flext_target_oracle.target_services", "OracleBatchService"),
    "OracleConnectionModel": (
        "flext_target_oracle.target_models",
        "OracleConnectionModel",
    ),
    "OracleConnectionService": (
        "flext_target_oracle.target_services",
        "OracleConnectionService",
    ),
    "OracleRecordService": (
        "flext_target_oracle.target_services",
        "OracleRecordService",
    ),
    "OracleSchemaService": (
        "flext_target_oracle.target_services",
        "OracleSchemaService",
    ),
    "OracleTargetCommandFactory": (
        "flext_target_oracle.target_commands",
        "OracleTargetCommandFactory",
    ),
    "OracleTargetServiceFactory": (
        "flext_target_oracle.target_services",
        "OracleTargetServiceFactory",
    ),
    "RecordServiceProtocol": (
        "flext_target_oracle.target_services",
        "RecordServiceProtocol",
    ),
    "SchemaServiceProtocol": (
        "flext_target_oracle.target_services",
        "SchemaServiceProtocol",
    ),
    "SingerStreamModel": ("flext_target_oracle.target_models", "SingerStreamModel"),
    "StorageModeModel": ("flext_target_oracle.target_models", "StorageModeModel"),
    "c": ("flext_target_oracle.constants", "FlextTargetOracleConstants"),
    "configure_oracle_observability": (
        "flext_target_oracle.target_observability",
        "configure_oracle_observability",
    ),
    "m": ("flext_target_oracle.models", "FlextTargetOracleModels"),
    "p": ("flext_target_oracle.protocols", "FlextTargetOracleProtocols"),
    "t": ("flext_target_oracle.typings", "FlextTargetOracleTypes"),
    "u": ("flext_target_oracle.utilities", "FlextTargetOracleUtilities"),
}

__all__ = [
    "BatchServiceProtocol",
    "ConnectionServiceProtocol",
    "FlextMeltanoSettings",
    "FlextMeltanoTargetAbstractions",
    "FlextMeltanoTypes",
    "FlextOracleError",
    "FlextOracleObs",
    "FlextResult",
    "FlextTargetOracle",
    "FlextTargetOracleAuthenticationError",
    "FlextTargetOracleCliService",
    "FlextTargetOracleConnectionError",
    "FlextTargetOracleConstants",
    "FlextTargetOracleError",
    "FlextTargetOracleLoader",
    "FlextTargetOracleModels",
    "FlextTargetOracleProcessingError",
    "FlextTargetOracleProtocols",
    "FlextTargetOracleSchemaError",
    "FlextTargetOracleSettings",
    "FlextTargetOracleTypes",
    "FlextTargetOracleUtilities",
    "LoadMethod",
    "LoadMethodModel",
    "LoadStatisticsModel",
    "OracleBatchService",
    "OracleConnectionModel",
    "OracleConnectionService",
    "OracleRecordService",
    "OracleSchemaService",
    "OracleTargetCommandFactory",
    "OracleTargetServiceFactory",
    "RecordServiceProtocol",
    "SchemaServiceProtocol",
    "SingerStreamModel",
    "StorageModeModel",
    "c",
    "configure_oracle_observability",
    "m",
    "p",
    "t",
    "u",
]


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
