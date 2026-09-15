"""Oracle Target exceptions through the public exception facade.

The public facade exposes the flext-db-oracle exception hierarchy.
Target-specific exceptions extend those domain bases.

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
    """Target exceptions extending the public flext-db-oracle hierarchy."""

    class Error(e.Error):
        """Oracle Target main error - inherits from base error."""

    class ConfigurationError(e.ConfigurationError):
        """Oracle configuration error extending the public exception facade."""

    class OracleConnectionError(e.OracleConnectionError):
        """Oracle connection error with Oracle-specific context."""

    class ValidationError(e.ValidationError):
        """Oracle validation error extending the public exception facade."""

    class AuthenticationError(e.AuthenticationError):
        """Oracle authentication error with Oracle-specific context."""

    class ProcessingError(e.ProcessingError):
        """Oracle processing error with Oracle-specific context."""

    class OracleTimeoutError(e.OracleTimeoutError):
        """Oracle timeout error extending the database exception hierarchy."""

    class SchemaError(ValidationError):
        """Oracle schema-specific validation errors."""


__all__: t.StrSequence = (
    "FlextTargetOracleErrorMetadata",
    "FlextTargetOracleExceptions",
)
