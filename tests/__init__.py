# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_target_oracle import (
        conftest,
        constants,
        e2e,
        integration,
        models,
        performance,
        protocols,
        test_config,
        test_loader,
        test_oracle,
        test_performance,
        test_singer,
        test_target,
        typings,
        unit,
        utilities,
    )
    from flext_target_oracle.conftest import (
        DOCKER_COMPOSE_PATH,
        ORACLE_CONTAINER_NAME,
        ORACLE_HOST,
        ORACLE_IMAGE,
        ORACLE_PASSWORD,
        ORACLE_PORT,
        ORACLE_SERVICE,
        ORACLE_USER,
        TEST_SCHEMA,
        batch_records,
        clean_database,
        connected_loader,
        docker_control,
        event_loop,
        large_dataset,
        logger,
        mock_api,
        mock_loader,
        mock_oracle_api,
        nested_schema,
        oracle_api,
        oracle_config,
        oracle_engine,
        oracle_loader,
        oracle_target,
        pytest_configure,
        reset_settings_singleton,
        sample_config,
        sample_record,
        sample_target,
        schema,
        shared_oracle_container,
        simple_schema,
        singer_messages,
        state,
        state_message,
        temp_config_file,
        temporary_env_vars,
    )
    from flext_target_oracle.constants import (
        FlextTargetOracleTestConstants,
        FlextTargetOracleTestConstants as c,
    )
    from flext_target_oracle.e2e import TestSingerWorkflowE2E
    from flext_target_oracle.integration import (
        TestOracleIntegration,
        TestOracleTargetE2E,
    )
    from flext_target_oracle.models import (
        FlextTargetOracleTestModels,
        FlextTargetOracleTestModels as m,
    )
    from flext_target_oracle.performance import TestPerformance
    from flext_target_oracle.protocols import (
        FlextTargetOracleTestProtocols,
        FlextTargetOracleTestProtocols as p,
    )
    from flext_target_oracle.typings import (
        FlextTargetOracleTestTypes,
        FlextTargetOracleTestTypes as t,
    )
    from flext_target_oracle.unit import (
        TestOracleSettings,
        finalize_result,
        load_result,
        loader,
        loader_config,
        record,
        result,
        schema_message,
        target,
        test_ensure_table_exists_returns_result,
        test_load_record_buffers_and_finalize,
        validated,
    )
    from flext_target_oracle.utilities import (
        FlextTargetOracleTestUtilities,
        FlextTargetOracleTestUtilities as u,
    )

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = merge_lazy_imports(
    (
        "flext_target_oracle.e2e",
        "flext_target_oracle.integration",
        "flext_target_oracle.performance",
        "flext_target_oracle.unit",
    ),
    {
        "DOCKER_COMPOSE_PATH": "flext_target_oracle.conftest",
        "FlextTargetOracleTestConstants": "flext_target_oracle.constants",
        "FlextTargetOracleTestModels": "flext_target_oracle.models",
        "FlextTargetOracleTestProtocols": "flext_target_oracle.protocols",
        "FlextTargetOracleTestTypes": "flext_target_oracle.typings",
        "FlextTargetOracleTestUtilities": "flext_target_oracle.utilities",
        "ORACLE_CONTAINER_NAME": "flext_target_oracle.conftest",
        "ORACLE_HOST": "flext_target_oracle.conftest",
        "ORACLE_IMAGE": "flext_target_oracle.conftest",
        "ORACLE_PASSWORD": "flext_target_oracle.conftest",
        "ORACLE_PORT": "flext_target_oracle.conftest",
        "ORACLE_SERVICE": "flext_target_oracle.conftest",
        "ORACLE_USER": "flext_target_oracle.conftest",
        "TEST_SCHEMA": "flext_target_oracle.conftest",
        "batch_records": "flext_target_oracle.conftest",
        "c": ("flext_target_oracle.constants", "FlextTargetOracleTestConstants"),
        "clean_database": "flext_target_oracle.conftest",
        "conftest": "flext_target_oracle.conftest",
        "connected_loader": "flext_target_oracle.conftest",
        "constants": "flext_target_oracle.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "docker_control": "flext_target_oracle.conftest",
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "e2e": "flext_target_oracle.e2e",
        "event_loop": "flext_target_oracle.conftest",
        "h": ("flext_core.handlers", "FlextHandlers"),
        "integration": "flext_target_oracle.integration",
        "large_dataset": "flext_target_oracle.conftest",
        "logger": "flext_target_oracle.conftest",
        "m": ("flext_target_oracle.models", "FlextTargetOracleTestModels"),
        "mock_api": "flext_target_oracle.conftest",
        "mock_loader": "flext_target_oracle.conftest",
        "mock_oracle_api": "flext_target_oracle.conftest",
        "models": "flext_target_oracle.models",
        "nested_schema": "flext_target_oracle.conftest",
        "oracle_api": "flext_target_oracle.conftest",
        "oracle_config": "flext_target_oracle.conftest",
        "oracle_engine": "flext_target_oracle.conftest",
        "oracle_loader": "flext_target_oracle.conftest",
        "oracle_target": "flext_target_oracle.conftest",
        "p": ("flext_target_oracle.protocols", "FlextTargetOracleTestProtocols"),
        "performance": "flext_target_oracle.performance",
        "protocols": "flext_target_oracle.protocols",
        "pytest_configure": "flext_target_oracle.conftest",
        "r": ("flext_core.result", "FlextResult"),
        "reset_settings_singleton": "flext_target_oracle.conftest",
        "s": ("flext_core.service", "FlextService"),
        "sample_config": "flext_target_oracle.conftest",
        "sample_record": "flext_target_oracle.conftest",
        "sample_target": "flext_target_oracle.conftest",
        "schema": "flext_target_oracle.conftest",
        "shared_oracle_container": "flext_target_oracle.conftest",
        "simple_schema": "flext_target_oracle.conftest",
        "singer_messages": "flext_target_oracle.conftest",
        "state": "flext_target_oracle.conftest",
        "state_message": "flext_target_oracle.conftest",
        "t": ("flext_target_oracle.typings", "FlextTargetOracleTestTypes"),
        "temp_config_file": "flext_target_oracle.conftest",
        "temporary_env_vars": "flext_target_oracle.conftest",
        "test_config": "flext_target_oracle.test_config",
        "test_loader": "flext_target_oracle.test_loader",
        "test_oracle": "flext_target_oracle.test_oracle",
        "test_performance": "flext_target_oracle.test_performance",
        "test_singer": "flext_target_oracle.test_singer",
        "test_target": "flext_target_oracle.test_target",
        "typings": "flext_target_oracle.typings",
        "u": ("flext_target_oracle.utilities", "FlextTargetOracleTestUtilities"),
        "unit": "flext_target_oracle.unit",
        "utilities": "flext_target_oracle.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
