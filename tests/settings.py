"""Runtime settings for flext-target-oracle tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
tests/settings
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsSettings

from flext_target_oracle import FlextTargetOracleSettings


class TestsFlextTargetOracleSettings(FlextTargetOracleSettings, FlextTestsSettings):
    """Target Oracle settings extended with the shared test namespace."""


__all__: list[str] = ["TestsFlextTargetOracleSettings"]
