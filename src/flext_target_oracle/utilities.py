"""Utility helpers for Oracle Singer target integration."""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleUtilities
from flext_meltano import FlextMeltanoUtilities

from flext_target_oracle import (
    FlextOracleError,
    FlextOracleObs,
    FlextTargetOracle,
    FlextTargetOracleBatchService,
    FlextTargetOracleCliService,
    FlextTargetOracleConnectionService,
    FlextTargetOracleErrorMetadata,
    FlextTargetOracleExceptions,
    FlextTargetOracleLoader,
    FlextTargetOracleRecordService,
    FlextTargetOracleSchemaService,
    FlextTargetOracleService,
    FlextTargetOracleServiceFactory,
    configure_oracle_observability,
    main,
)


class FlextTargetOracleUtilities(FlextMeltanoUtilities, FlextDbOracleUtilities):
    """Focused utility namespace used by Oracle target modules."""

    class TargetOracle:
        """Oracle target utility namespace with absorbed loose classes."""

        Client = FlextTargetOracle
        Loader = FlextTargetOracleLoader
        Service = FlextTargetOracleService
        CliService = FlextTargetOracleCliService
        Exceptions = FlextTargetOracleExceptions
        ErrorMetadata = FlextTargetOracleErrorMetadata
        ConnectionService = FlextTargetOracleConnectionService
        SchemaService = FlextTargetOracleSchemaService
        BatchService = FlextTargetOracleBatchService
        RecordService = FlextTargetOracleRecordService
        ServiceFactory = FlextTargetOracleServiceFactory
        OracleError = FlextOracleError
        OracleObs = FlextOracleObs
        configure_observability = configure_oracle_observability
        cli_main = main


u = FlextTargetOracleUtilities
__all__ = ["FlextTargetOracleUtilities", "u"]
