"""Command helpers for Oracle target CLI flows.

All command classes live in FlextTargetOracleModels.TargetOracle (models.py).
This module re-exports them for backward compatibility.
"""

from __future__ import annotations

from flext_target_oracle.models import FlextTargetOracleModels as _m

OracleTargetAboutCommand = _m.TargetOracle.OracleTargetAboutCommand
OracleTargetLoadCommand = _m.TargetOracle.OracleTargetLoadCommand
OracleTargetValidateCommand = _m.TargetOracle.OracleTargetValidateCommand
OracleTargetCommandHandler = _m.TargetOracle.OracleTargetCommandHandler
OracleTargetCommandFactory = _m.TargetOracle.OracleTargetCommandFactory

__all__ = [
    "OracleTargetAboutCommand",
    "OracleTargetCommandFactory",
    "OracleTargetCommandHandler",
    "OracleTargetLoadCommand",
    "OracleTargetValidateCommand",
]
