"""Oracle Target Exception Hierarchy - Using flext-core SOURCE OF TRUTH.

Direct usage of flext-core exception classes without duplication or factories.
Oracle-specific exceptions inherit directly from flext-core bases.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Annotated

from flext_meltano import u
from flext_target_oracle import e, m, t


class FlextTargetOracleErrorMetadata(m.FlexibleInternalModel):
    """Structured metadata attached to Oracle target error responses."""

    code: Annotated[str, u.Field(description="Canonical error code")]
    context: Annotated[
        t.JsonMapping | None, u.Field(description="Structured error context")
    ] = None
    correlation_id: Annotated[
        str | None, u.Field(description="Cross-service correlation identifier")
    ] = None


class FlextTargetOracleExceptions(e):
    """Oracle Target exceptions using flext-core SOURCE OF TRUTH."""

    class Error(e.Error):
        """Oracle Target main error - inherits from base error."""

    class ConfigurationError(e.ConfigurationError):
        """Oracle configuration error using flext-core foundation."""

    class OracleConnectionError(e.OracleConnectionError):
        """Oracle connection error with Oracle-specific context."""

    class ValidationError(e.ValidationError):
        """Oracle validation error using flext-core foundation."""

    class AuthenticationError(e.AuthenticationError):
        """Oracle authentication error with Oracle-specific context."""

    class ProcessingError(e.ProcessingError):
        """Oracle processing error with Oracle-specific context."""

    class OracleTimeoutError(e.OracleTimeoutError):
        """Oracle timeout error using flext-core foundation."""

    class SchemaError(ValidationError):
        """Oracle schema-specific validation errors."""


__all__: t.StrSequence = (
    "FlextTargetOracleErrorMetadata",
    "FlextTargetOracleExceptions",
)
