# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import tests.conftest as _tests_conftest

    conftest = _tests_conftest
    import tests.constants as _tests_constants
    from tests.conftest import (
        DOCKER_COMPOSE_PATH,
        ORACLE_CONTAINER_NAME,
        ORACLE_HOST,
        ORACLE_IMAGE,
        ORACLE_PASSWORD,
        ORACLE_PORT,
        ORACLE_SERVICE,
        ORACLE_USER,
        TEST_SCHEMA,
        logger,
        pytest_collection_modifyitems,
        pytest_configure,
        pytest_plugins,
        temporary_env_vars,
    )

    constants = _tests_constants
    import tests.models as _tests_models
    from tests.constants import (
        FlextTargetOracleTestConstants,
        FlextTargetOracleTestConstants as c,
    )

    models = _tests_models
    import tests.protocols as _tests_protocols
    from tests.models import (
        FlextTargetOracleTestModels,
        FlextTargetOracleTestModels as m,
    )

    protocols = _tests_protocols
    import tests.test_module_governance as _tests_test_module_governance
    from tests.protocols import (
        FlextTargetOracleTestProtocols,
        FlextTargetOracleTestProtocols as p,
    )

    test_module_governance = _tests_test_module_governance
    import tests.typings as _tests_typings
    from tests.test_module_governance import ALLOWED_MODULE_FUNCTIONS, PACKAGE_ROOT

    typings = _tests_typings
    import tests.utilities as _tests_utilities
    from tests.typings import (
        FlextTargetOracleTestTypes,
        FlextTargetOracleTestTypes as t,
    )

    utilities = _tests_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from tests.utilities import (
        FlextTargetOracleTestUtilities,
        FlextTargetOracleTestUtilities as u,
    )
_LAZY_IMPORTS = {
    "ALLOWED_MODULE_FUNCTIONS": (
        "tests.test_module_governance",
        "ALLOWED_MODULE_FUNCTIONS",
    ),
    "DOCKER_COMPOSE_PATH": ("tests.conftest", "DOCKER_COMPOSE_PATH"),
    "FlextTargetOracleTestConstants": (
        "tests.constants",
        "FlextTargetOracleTestConstants",
    ),
    "FlextTargetOracleTestModels": ("tests.models", "FlextTargetOracleTestModels"),
    "FlextTargetOracleTestProtocols": (
        "tests.protocols",
        "FlextTargetOracleTestProtocols",
    ),
    "FlextTargetOracleTestTypes": ("tests.typings", "FlextTargetOracleTestTypes"),
    "FlextTargetOracleTestUtilities": (
        "tests.utilities",
        "FlextTargetOracleTestUtilities",
    ),
    "ORACLE_CONTAINER_NAME": ("tests.conftest", "ORACLE_CONTAINER_NAME"),
    "ORACLE_HOST": ("tests.conftest", "ORACLE_HOST"),
    "ORACLE_IMAGE": ("tests.conftest", "ORACLE_IMAGE"),
    "ORACLE_PASSWORD": ("tests.conftest", "ORACLE_PASSWORD"),
    "ORACLE_PORT": ("tests.conftest", "ORACLE_PORT"),
    "ORACLE_SERVICE": ("tests.conftest", "ORACLE_SERVICE"),
    "ORACLE_USER": ("tests.conftest", "ORACLE_USER"),
    "PACKAGE_ROOT": ("tests.test_module_governance", "PACKAGE_ROOT"),
    "TEST_SCHEMA": ("tests.conftest", "TEST_SCHEMA"),
    "c": ("tests.constants", "FlextTargetOracleTestConstants"),
    "conftest": "tests.conftest",
    "constants": "tests.constants",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "logger": ("tests.conftest", "logger"),
    "m": ("tests.models", "FlextTargetOracleTestModels"),
    "models": "tests.models",
    "p": ("tests.protocols", "FlextTargetOracleTestProtocols"),
    "protocols": "tests.protocols",
    "pytest_collection_modifyitems": (
        "tests.conftest",
        "pytest_collection_modifyitems",
    ),
    "pytest_configure": ("tests.conftest", "pytest_configure"),
    "pytest_plugins": ("tests.conftest", "pytest_plugins"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("tests.typings", "FlextTargetOracleTestTypes"),
    "temporary_env_vars": ("tests.conftest", "temporary_env_vars"),
    "test_module_governance": "tests.test_module_governance",
    "typings": "tests.typings",
    "u": ("tests.utilities", "FlextTargetOracleTestUtilities"),
    "utilities": "tests.utilities",
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
    "ALLOWED_MODULE_FUNCTIONS",
    "DOCKER_COMPOSE_PATH",
    "ORACLE_CONTAINER_NAME",
    "ORACLE_HOST",
    "ORACLE_IMAGE",
    "ORACLE_PASSWORD",
    "ORACLE_PORT",
    "ORACLE_SERVICE",
    "ORACLE_USER",
    "PACKAGE_ROOT",
    "TEST_SCHEMA",
    "FlextTargetOracleTestConstants",
    "FlextTargetOracleTestModels",
    "FlextTargetOracleTestProtocols",
    "FlextTargetOracleTestTypes",
    "FlextTargetOracleTestUtilities",
    "c",
    "conftest",
    "constants",
    "d",
    "e",
    "h",
    "logger",
    "m",
    "models",
    "p",
    "protocols",
    "pytest_collection_modifyitems",
    "pytest_configure",
    "pytest_plugins",
    "r",
    "s",
    "t",
    "temporary_env_vars",
    "test_module_governance",
    "typings",
    "u",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
