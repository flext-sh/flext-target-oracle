"""Utility helpers for Oracle Singer target integration."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence

from flext_core import r
from flext_db_oracle import FlextDbOracleUtilities
from flext_meltano import FlextMeltanoUtilities
from pydantic import TypeAdapter

from flext_target_oracle import t
from flext_target_oracle._utilities.cli import (
    FlextTargetOracleCliService,
    main,
)
from flext_target_oracle._utilities.client import FlextTargetOracle
from flext_target_oracle._utilities.errors import (
    FlextTargetOracleErrorMetadata,
    FlextTargetOracleExceptions,
)
from flext_target_oracle._utilities.loader import FlextTargetOracleLoader
from flext_target_oracle._utilities.observability import (
    FlextOracleError,
    FlextOracleObs,
    configure_oracle_observability,
)
from flext_target_oracle._utilities.service import FlextTargetOracleService
from flext_target_oracle._utilities.services import (
    FlextTargetOracleBatchService,
    FlextTargetOracleConnectionService,
    FlextTargetOracleRecordService,
    FlextTargetOracleSchemaService,
    FlextTargetOracleServiceFactory,
)

_CONTAINER_VALUE_ADAPTER: TypeAdapter[t.ContainerValue] = TypeAdapter(t.ContainerValue)


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

    class OracleDataProcessing:
        """Data conversion helpers for Oracle storage."""

        @staticmethod
        def transform_record_for_oracle(
            record: Mapping[str, t.ContainerValue],
        ) -> r[Mapping[str, t.ContainerValue]]:
            """Normalize record values for Oracle persistence."""
            transformed: MutableMapping[str, t.ContainerValue] = {}
            for key, value in record.items():
                is_mapping = isinstance(value, Mapping)
                is_sequence = isinstance(value, Sequence) and (
                    not isinstance(value, str | bytes)
                )
                if is_mapping or is_sequence:
                    transformed[key.upper()] = _CONTAINER_VALUE_ADAPTER.dump_json(
                        value,
                    ).decode("utf-8")
                    continue
                match value:
                    case bool() as bool_value:
                        transformed[key.upper()] = 1 if bool_value else 0
                    case _:
                        transformed[key.upper()] = value
            return r[t.ContainerValueMapping].ok(transformed)


u = FlextTargetOracleUtilities
__all__ = ["FlextTargetOracleUtilities", "u"]
