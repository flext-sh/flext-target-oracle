# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Utilities package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_target_oracle import cli, client, errors, loader, observability, services
    from flext_target_oracle.cli import FlextTargetOracleCliService, main
    from flext_target_oracle.client import FlextTargetOracle
    from flext_target_oracle.errors import (
        FlextTargetOracleExceptions,
        code,
        context,
        correlation_id,
    )
    from flext_target_oracle.loader import FlextTargetOracleLoader
    from flext_target_oracle.observability import (
        FlextOracleError,
        FlextOracleObs,
        configure_oracle_observability,
    )
    from flext_target_oracle.services import FlextTargetOracleConnectionService

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextOracleError": "flext_target_oracle.observability",
    "FlextOracleObs": "flext_target_oracle.observability",
    "FlextTargetOracle": "flext_target_oracle.client",
    "FlextTargetOracleCliService": "flext_target_oracle.cli",
    "FlextTargetOracleConnectionService": "flext_target_oracle.services",
    "FlextTargetOracleExceptions": "flext_target_oracle.errors",
    "FlextTargetOracleLoader": "flext_target_oracle.loader",
    "cli": "flext_target_oracle.cli",
    "client": "flext_target_oracle.client",
    "code": "flext_target_oracle.errors",
    "configure_oracle_observability": "flext_target_oracle.observability",
    "context": "flext_target_oracle.errors",
    "correlation_id": "flext_target_oracle.errors",
    "errors": "flext_target_oracle.errors",
    "loader": "flext_target_oracle.loader",
    "main": "flext_target_oracle.cli",
    "observability": "flext_target_oracle.observability",
    "services": "flext_target_oracle.services",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
