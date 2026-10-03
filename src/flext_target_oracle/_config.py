"""FlextTargetOracleConfig — frozen config singleton for flext-target-oracle (ADR-005 §7).

Model-less: business rules live in ``config/*.yaml`` under the ``TargetOracle:`` key and
are exposed through the open ``config.TargetOracle`` namespace (``extra="allow"``), with
no per-domain model. Access is ``config.TargetOracle.<domain>[<key>...]``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated, Self

from flext_meltano import FlextMeltanoConfig, m


class _TargetOracleNamespace(m.BaseModel):
    """Open, frozen namespace exposing every ``config/*.yaml`` domain model-less."""

    model_config = m.ConfigDict(extra="allow", frozen=True)


class FlextTargetOracleConfig(FlextMeltanoConfig):
    """TargetOracle config auto-loaded model-less from ``config/*.yaml``.

    MRO carries ``FlextSettings`` FIRST (ENFORCE-042); the class stays a frozen,
    YAML-validated config singleton.
    """

    # ENFORCE-042 namespace-holder contract: ``FlextSettings`` contributes
    # namespacing only — instance machinery stays plain object semantics so the
    # settings singleton ``__new__`` cannot leak into the config singleton.
    # The inherited pydantic ``__init__`` still runs the frozen, YAML-validated
    # construction, and the inherited pydantic ``__setattr__`` keeps the frozen
    # guard.
    def __new__(cls, *args: object, **kwargs: object) -> Self:
        _ = args, kwargs
        return object.__new__(cls)

    __eq__ = object.__eq__

    __hash__ = object.__hash__

    TargetOracle: Annotated[
        _TargetOracleNamespace,
        m.Field(
            description="Open namespace exposing ``config/*.yaml`` under ``TargetOracle``."
        ),
    ] = _TargetOracleNamespace()


config: FlextTargetOracleConfig = FlextTargetOracleConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_target_oracle import config``."""

__all__: list[str] = ["FlextTargetOracleConfig", "config"]
