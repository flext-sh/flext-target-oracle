"""Re-export shim - canonical location: _utilities/observability.py."""

from __future__ import annotations

from flext_target_oracle._utilities.observability import (
    FlextOracleError,
    FlextOracleObs,
    configure_oracle_observability,
)

__all__ = ["FlextOracleError", "FlextOracleObs", "configure_oracle_observability"]
