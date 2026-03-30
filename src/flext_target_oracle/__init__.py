# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Production-Grade Singer Target for Oracle Database data loading.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if TYPE_CHECKING:
    from flext_target_oracle.__version__ import *
    from flext_target_oracle._models import *
    from flext_target_oracle._utilities import *
    from flext_target_oracle.constants import *
    from flext_target_oracle.models import *
    from flext_target_oracle.protocols import *
    from flext_target_oracle.settings import *
    from flext_target_oracle.typings import *
    from flext_target_oracle.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = merge_lazy_imports(
    (
        "flext_target_oracle._models",
        "flext_target_oracle._utilities",
    ),
    {
        "FlextTargetOracleConstants": "flext_target_oracle.constants",
        "FlextTargetOracleModels": "flext_target_oracle.models",
        "FlextTargetOracleProtocols": "flext_target_oracle.protocols",
        "FlextTargetOracleSettings": "flext_target_oracle.settings",
        "FlextTargetOracleTypes": "flext_target_oracle.typings",
        "FlextTargetOracleUtilities": "flext_target_oracle.utilities",
        "__author__": "flext_target_oracle.__version__",
        "__author_email__": "flext_target_oracle.__version__",
        "__description__": "flext_target_oracle.__version__",
        "__license__": "flext_target_oracle.__version__",
        "__title__": "flext_target_oracle.__version__",
        "__url__": "flext_target_oracle.__version__",
        "__version__": "flext_target_oracle.__version__",
        "__version_info__": "flext_target_oracle.__version__",
        "_models": "flext_target_oracle._models",
        "_utilities": "flext_target_oracle._utilities",
        "c": ("flext_target_oracle.constants", "FlextTargetOracleConstants"),
        "constants": "flext_target_oracle.constants",
        "d": "flext_db_oracle",
        "e": "flext_db_oracle",
        "h": "flext_db_oracle",
        "logger": "flext_target_oracle.settings",
        "m": ("flext_target_oracle.models", "FlextTargetOracleModels"),
        "models": "flext_target_oracle.models",
        "p": ("flext_target_oracle.protocols", "FlextTargetOracleProtocols"),
        "protocols": "flext_target_oracle.protocols",
        "r": "flext_db_oracle",
        "s": "flext_db_oracle",
        "settings": "flext_target_oracle.settings",
        "t": ("flext_target_oracle.typings", "FlextTargetOracleTypes"),
        "target_client": "flext_target_oracle.target_client",
        "target_exceptions": "flext_target_oracle.target_exceptions",
        "target_loader": "flext_target_oracle.target_loader",
        "target_observability": "flext_target_oracle.target_observability",
        "target_refactored": "flext_target_oracle.target_refactored",
        "target_service": "flext_target_oracle.target_service",
        "target_services": "flext_target_oracle.target_services",
        "typings": "flext_target_oracle.typings",
        "u": ("flext_target_oracle.utilities", "FlextTargetOracleUtilities"),
        "utilities": "flext_target_oracle.utilities",
        "x": "flext_db_oracle",
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
