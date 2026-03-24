"""Command helpers for Oracle target CLI flows.

All command classes live in FlextTargetOracleModels.TargetOracle (models.py).
This module re-exports them for backward compatibility.
"""

from __future__ import annotations

from flext_target_oracle import m

OracleTargetAboutCommand = m.TargetOracle.OracleTargetAboutCommand
OracleTargetLoadCommand = m.TargetOracle.OracleTargetLoadCommand
OracleTargetValidateCommand = m.TargetOracle.OracleTargetValidateCommand
OracleTargetCommandHandler = m.TargetOracle.OracleTargetCommandHandler
OracleTargetCommandFactory = m.TargetOracle.OracleTargetCommandFactory

__all__ = [
    "OracleTargetAboutCommand",
    "OracleTargetCommandFactory",
    "OracleTargetCommandHandler",
    "OracleTargetLoadCommand",
    "OracleTargetValidateCommand",
]
