# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export map part."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map

FLEXT_TARGET_ORACLE_LAZY_IMPORTS_PART_01 = build_lazy_import_map(
    {
        "._constants.base": ("FlextTargetOracleConstantsBase",),
        "._models.commands": ("FlextTargetOracleModelsCommands",),
        "._models.results": ("FlextTargetOracleModelsResults",),
        "._models.settings": ("FlextTargetOracleModelsSettings",),
        "._models.singer": ("FlextTargetOracleModelsSinger",),
        "._protocols.base": ("FlextTargetOracleProtocolsBase",),
        "._typings.base": ("FlextTargetOracleTypesBase",),
        "._utilities.base": ("FlextTargetOracleUtilitiesBase",),
        "._utilities.cli": ("FlextTargetOracleCliService",),
        "._utilities.client": ("FlextTargetOracle",),
        "._utilities.errors": (
            "FlextTargetOracleErrorMetadata",
            "FlextTargetOracleExceptions",
        ),
        "._utilities.loader": ("FlextTargetOracleLoader",),
        "._utilities.observability": ("FlextTargetOracleUtilitiesObservability",),
        "._utilities.services": (
            "FlextTargetOracleBatchService",
            "FlextTargetOracleConnectionService",
            "FlextTargetOracleRecordService",
            "FlextTargetOracleSchemaService",
        ),
        ".api": (
            "FlextTargetOracleService",
            "target_oracle",
        ),
        ".constants": (
            "FlextTargetOracleConstants",
            "c",
        ),
        ".models": (
            "FlextTargetOracleModels",
            "m",
        ),
        ".protocols": (
            "FlextTargetOracleProtocols",
            "p",
        ),
        ".settings": ("FlextTargetOracleSettings",),
        ".typings": (
            "FlextTargetOracleTypes",
            "t",
        ),
        ".utilities": (
            "FlextTargetOracleUtilities",
            "u",
        ),
    },
)

__all__: list[str] = ["FLEXT_TARGET_ORACLE_LAZY_IMPORTS_PART_01"]
