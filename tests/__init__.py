# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_db_oracle import e
    from flext_tests import api, td, tf, tk, tm

    from flext_target_oracle import d, h, r, x
    from tests.base import TestsFlextTargetOracleServiceBase, s
    from tests.conftest import (
        clean_database,
        docker_control,
        isolate_target_oracle_env,
        nested_schema,
        oracle_config,
        oracle_engine,
        oracle_loader,
        pytest_collection_modifyitems,
        pytest_configure,
        shared_oracle_container,
        simple_schema,
        singer_messages,
    )
    from tests.constants import TestsFlextTargetOracleConstants, c
    from tests.models import TestsFlextTargetOracleModels, m
    from tests.protocols import TestsFlextTargetOracleProtocols, p
    from tests.settings import TestsFlextTargetOracleSettings
    from tests.typings import TestsFlextTargetOracleTypes, t
    from tests.utilities import TestsFlextTargetOracleUtilities, u


__all__: tuple[str, ...] = (
    "TestsFlextTargetOracleConstants",
    "TestsFlextTargetOracleModels",
    "TestsFlextTargetOracleProtocols",
    "TestsFlextTargetOracleServiceBase",
    "TestsFlextTargetOracleSettings",
    "TestsFlextTargetOracleTypes",
    "TestsFlextTargetOracleUtilities",
    "api",
    "c",
    "clean_database",
    "d",
    "docker_control",
    "e",
    "h",
    "isolate_target_oracle_env",
    "m",
    "nested_schema",
    "oracle_config",
    "oracle_engine",
    "oracle_loader",
    "p",
    "pytest_collection_modifyitems",
    "pytest_configure",
    "r",
    "s",
    "shared_oracle_container",
    "simple_schema",
    "singer_messages",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "TestsFlextTargetOracleConstants": ".constants",
        "TestsFlextTargetOracleModels": ".models",
        "TestsFlextTargetOracleProtocols": ".protocols",
        "TestsFlextTargetOracleServiceBase": ".base",
        "TestsFlextTargetOracleSettings": ".settings",
        "TestsFlextTargetOracleTypes": ".typings",
        "TestsFlextTargetOracleUtilities": ".utilities",
        "api": "flext_tests",
        "c": ".constants",
        "clean_database": ".conftest",
        "d": "flext_target_oracle",
        "docker_control": ".conftest",
        "e": "flext_db_oracle",
        "h": "flext_target_oracle",
        "isolate_target_oracle_env": ".conftest",
        "m": ".models",
        "nested_schema": ".conftest",
        "oracle_config": ".conftest",
        "oracle_engine": ".conftest",
        "oracle_loader": ".conftest",
        "p": ".protocols",
        "pytest_collection_modifyitems": ".conftest",
        "pytest_configure": ".conftest",
        "r": "flext_target_oracle",
        "s": ".base",
        "shared_oracle_container": ".conftest",
        "simple_schema": ".conftest",
        "singer_messages": ".conftest",
        "t": ".typings",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "x": "flext_target_oracle",
    }),
    public_exports=__all__,
)
