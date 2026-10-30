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
    from flext_tests import api, install_local_packages, td, tf, tk, tm

    from flext_target_oracle import (
        build_lazy_import_map,
        cleanup_submodule_namespace,
        cli,
        config,
        core,
        d,
        db_oracle,
        h,
        install_lazy_exports,
        lazy,
        lazy_getattr,
        lazy_member,
        main,
        meltano,
        merge_lazy_imports,
        normalize_lazy_imports,
        r,
        resolve_lazy_members,
        settings,
        target_oracle,
        x,
    )
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
    "build_lazy_import_map",
    "c",
    "clean_database",
    "cleanup_submodule_namespace",
    "cli",
    "config",
    "core",
    "d",
    "db_oracle",
    "docker_control",
    "e",
    "h",
    "install_lazy_exports",
    "install_local_packages",
    "isolate_target_oracle_env",
    "lazy",
    "lazy_getattr",
    "lazy_member",
    "m",
    "main",
    "meltano",
    "merge_lazy_imports",
    "nested_schema",
    "normalize_lazy_imports",
    "oracle_config",
    "oracle_engine",
    "oracle_loader",
    "p",
    "pytest_collection_modifyitems",
    "pytest_configure",
    "r",
    "resolve_lazy_members",
    "s",
    "settings",
    "shared_oracle_container",
    "simple_schema",
    "singer_messages",
    "t",
    "target_oracle",
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
        "build_lazy_import_map": "flext_target_oracle",
        "c": ".constants",
        "clean_database": ".conftest",
        "cleanup_submodule_namespace": "flext_target_oracle",
        "cli": "flext_target_oracle",
        "config": "flext_target_oracle",
        "core": "flext_target_oracle",
        "d": "flext_target_oracle",
        "db_oracle": "flext_target_oracle",
        "docker_control": ".conftest",
        "e": "flext_db_oracle",
        "h": "flext_target_oracle",
        "install_lazy_exports": "flext_target_oracle",
        "install_local_packages": "flext_tests",
        "isolate_target_oracle_env": ".conftest",
        "lazy": "flext_target_oracle",
        "lazy_getattr": "flext_target_oracle",
        "lazy_member": "flext_target_oracle",
        "m": ".models",
        "main": "flext_target_oracle",
        "meltano": "flext_target_oracle",
        "merge_lazy_imports": "flext_target_oracle",
        "nested_schema": ".conftest",
        "normalize_lazy_imports": "flext_target_oracle",
        "oracle_config": ".conftest",
        "oracle_engine": ".conftest",
        "oracle_loader": ".conftest",
        "p": ".protocols",
        "pytest_collection_modifyitems": ".conftest",
        "pytest_configure": ".conftest",
        "r": "flext_target_oracle",
        "resolve_lazy_members": "flext_target_oracle",
        "s": ".base",
        "settings": "flext_target_oracle",
        "shared_oracle_container": ".conftest",
        "simple_schema": ".conftest",
        "singer_messages": ".conftest",
        "t": ".typings",
        "target_oracle": "flext_target_oracle",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "x": "flext_target_oracle",
    }),
    public_exports=__all__,
)
