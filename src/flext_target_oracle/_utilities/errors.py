"""Oracle Target Exception Hierarchy - Using flext-core SOURCE OF TRUTH.

Direct usage of flext-core exception classes without duplication or factories.
Oracle-specific exceptions inherit directly from flext-core bases.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Annotated

from flext_meltano import u

from flext_core import e as core_e
from flext_target_oracle import m, t


class FlextTargetOracleUtilities:
    """Utilities namespace for the Oracle target family."""

    # Oracle Target exceptions inherit directly from the flext-core SOURCE OF
    # TRUTH; nesting under the db-oracle facade would shadow its typed init
    # signatures.
    class ErrorMetadata(m.FlexibleInternalModel):
        """Structured metadata attached to Oracle target error responses."""

        code: Annotated[str, u.Field(description="Canonical error code")]
        context: Annotated[
            t.JsonMapping | None, u.Field(description="Structured error context")
        ] = None
        correlation_id: Annotated[
            str | None, u.Field(description="Cross-service correlation identifier")
        ] = None

    class Exceptions(core_e):
        """Oracle Target exceptions using flext-core SOURCE OF TRUTH."""

        class Error(core_e.BaseError):
            """Oracle Target main error - inherits from base error."""

        class ConfigurationError(core_e.ConfigurationError):
            """Oracle configuration error using flext-core foundation."""

        class OracleConnectionError(core_e.FlextConnectionError):
            """Oracle connection error with Oracle-specific context."""

        class ValidationError(core_e.ValidationError):
            """Oracle validation error using flext-core foundation."""

        class AuthenticationError(core_e.AuthenticationError):
            """Oracle authentication error with Oracle-specific context."""

        class ProcessingError(core_e.OperationError):
            """Oracle processing error with Oracle-specific context."""

        class OracleTimeoutError(core_e.FlextTimeoutError):
            """Oracle timeout error using flext-core foundation."""

        class SchemaError(ValidationError):
            """Oracle schema-specific validation errors."""


FlextTargetOracleErrorMetadata = FlextTargetOracleUtilities.ErrorMetadata
FlextTargetOracleExceptions = FlextTargetOracleUtilities.Exceptions

__all__: t.StrSequence = (
    "FlextTargetOracleErrorMetadata",
    "FlextTargetOracleExceptions",
)
