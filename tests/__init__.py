# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _t.TYPE_CHECKING:
    import tests.conftest as _tests_conftest

    conftest = _tests_conftest
    import tests.constants as _tests_constants

    constants = _tests_constants
    import tests.e2e as _tests_e2e
    from tests.constants import (
        TestsFlextTargetOracleConstants,
        TestsFlextTargetOracleConstants as c,
    )

    e2e = _tests_e2e
    import tests.integration as _tests_integration

    integration = _tests_integration
    import tests.models as _tests_models

    models = _tests_models
    import tests.performance as _tests_performance
    from tests.models import (
        TestsFlextTargetOracleModels,
        TestsFlextTargetOracleModels as m,
    )

    performance = _tests_performance
    import tests.protocols as _tests_protocols

    protocols = _tests_protocols
    import tests.test_module_governance as _tests_test_module_governance
    from tests.protocols import (
        TestsFlextTargetOracleProtocols,
        TestsFlextTargetOracleProtocols as p,
    )

    test_module_governance = _tests_test_module_governance
    import tests.typings as _tests_typings

    typings = _tests_typings
    import tests.unit as _tests_unit
    from tests.typings import (
        TestsFlextTargetOracleTypes,
        TestsFlextTargetOracleTypes as t,
    )

    unit = _tests_unit
    import tests.utilities as _tests_utilities

    utilities = _tests_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from tests.utilities import (
        TestsFlextTargetOracleUtilities,
        TestsFlextTargetOracleUtilities as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "tests.e2e",
        "tests.integration",
        "tests.performance",
        "tests.unit",
    ),
    {
        "TestsFlextTargetOracleConstants": (
            "tests.constants",
            "TestsFlextTargetOracleConstants",
        ),
        "TestsFlextTargetOracleModels": (
            "tests.models",
            "TestsFlextTargetOracleModels",
        ),
        "TestsFlextTargetOracleProtocols": (
            "tests.protocols",
            "TestsFlextTargetOracleProtocols",
        ),
        "TestsFlextTargetOracleTypes": ("tests.typings", "TestsFlextTargetOracleTypes"),
        "TestsFlextTargetOracleUtilities": (
            "tests.utilities",
            "TestsFlextTargetOracleUtilities",
        ),
        "c": ("tests.constants", "TestsFlextTargetOracleConstants"),
        "conftest": "tests.conftest",
        "constants": "tests.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "e2e": "tests.e2e",
        "h": ("flext_core.handlers", "FlextHandlers"),
        "integration": "tests.integration",
        "m": ("tests.models", "TestsFlextTargetOracleModels"),
        "models": "tests.models",
        "p": ("tests.protocols", "TestsFlextTargetOracleProtocols"),
        "performance": "tests.performance",
        "protocols": "tests.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "t": ("tests.typings", "TestsFlextTargetOracleTypes"),
        "test_module_governance": "tests.test_module_governance",
        "typings": "tests.typings",
        "u": ("tests.utilities", "TestsFlextTargetOracleUtilities"),
        "unit": "tests.unit",
        "utilities": "tests.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)
_ = _LAZY_IMPORTS.pop("cleanup_submodule_namespace", None)
_ = _LAZY_IMPORTS.pop("install_lazy_exports", None)
_ = _LAZY_IMPORTS.pop("lazy_getattr", None)
_ = _LAZY_IMPORTS.pop("logger", None)
_ = _LAZY_IMPORTS.pop("merge_lazy_imports", None)
_ = _LAZY_IMPORTS.pop("output", None)
_ = _LAZY_IMPORTS.pop("output_reporting", None)

__all__ = [
    "TestsFlextTargetOracleConstants",
    "TestsFlextTargetOracleModels",
    "TestsFlextTargetOracleProtocols",
    "TestsFlextTargetOracleTypes",
    "TestsFlextTargetOracleUtilities",
    "c",
    "conftest",
    "constants",
    "d",
    "e",
    "e2e",
    "h",
    "integration",
    "m",
    "models",
    "p",
    "performance",
    "protocols",
    "r",
    "s",
    "t",
    "test_module_governance",
    "typings",
    "u",
    "unit",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
