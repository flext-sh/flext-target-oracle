# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Oracle. Protocols package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_oracle._protocols.base import FlextTargetOracleProtocolsBase
    from flext_target_oracle._protocols.commands import (
        FlextTargetOracleProtocolsCommands,
    )
    from flext_target_oracle._protocols.error_metadata import (
        FlextTargetOracleProtocolsErrorMetadata,
    )
    from flext_target_oracle._protocols.health_status import (
        FlextTargetOracleProtocolsHealthStatus,
    )
    from flext_target_oracle._protocols.results import FlextTargetOracleProtocolsResults
    from flext_target_oracle._protocols.settings import (
        FlextTargetOracleProtocolsSettings,
    )
    from flext_target_oracle._protocols.singer import FlextTargetOracleProtocolsSinger


__all__: tuple[str, ...] = (
    "FlextTargetOracleProtocolsBase",
    "FlextTargetOracleProtocolsCommands",
    "FlextTargetOracleProtocolsErrorMetadata",
    "FlextTargetOracleProtocolsHealthStatus",
    "FlextTargetOracleProtocolsResults",
    "FlextTargetOracleProtocolsSettings",
    "FlextTargetOracleProtocolsSinger",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextTargetOracleProtocolsBase": ".base",
        "FlextTargetOracleProtocolsCommands": ".commands",
        "FlextTargetOracleProtocolsErrorMetadata": ".error_metadata",
        "FlextTargetOracleProtocolsHealthStatus": ".health_status",
        "FlextTargetOracleProtocolsResults": ".results",
        "FlextTargetOracleProtocolsSettings": ".settings",
        "FlextTargetOracleProtocolsSinger": ".singer",
    },
    public_exports=__all__,
)
