"""Singer message model specializations for Oracle target."""

from __future__ import annotations

from typing import Annotated

from flext_meltano import FlextMeltanoModels, u
from flext_target_oracle import t


class FlextTargetOracleModelsSinger:
    """Singer message MRO mixin for TargetOracle namespace."""

    class Meltano(FlextMeltanoModels.Meltano):
        """Namespaced Meltano runtime model references (inherits all Singer types)."""

    class SingerSchemaMessage(FlextMeltanoModels.Meltano.SingerSchemaMessage):
        """Singer SCHEMA message specialized for Oracle target domain."""

    class SingerRecordMessage(FlextMeltanoModels.Meltano.SingerRecordMessage):
        """Singer RECORD message specialized for Oracle target domain."""

    class SingerStateMessage(FlextMeltanoModels.Meltano.SingerStateMessage):
        """Singer STATE message specialized for Oracle target domain."""

    class SingerActivateVersionMessage(
        FlextMeltanoModels.Meltano.SingerActivateVersionMessage,
    ):
        """Singer ACTIVATE_VERSION message specialized for Oracle target domain."""

    class SingerCatalogMetadata(FlextMeltanoModels.Meltano.SingerCatalogMetadata):
        """Singer catalog metadata specialized for Oracle target domain."""

    class SingerCatalogEntry(FlextMeltanoModels.Meltano.SingerCatalogEntry):
        """Singer catalog entry specialized for Oracle target domain."""

    class SingerCatalog(FlextMeltanoModels.Meltano.SingerCatalog):
        """Singer catalog specialized for Oracle target domain."""

    class SingerStreamModel(FlextMeltanoModels.ArbitraryTypesModel):
        """Singer stream mapping to Oracle table with column configuration."""

        stream_name: Annotated[str, u.Field(description="Singer stream name")]
        table_name: Annotated[
            str,
            u.Field(description="Oracle destination table name"),
        ]
        ignored_columns: Annotated[
            t.StrSequence,
            u.Field(
                description="Columns ignored during record transformation",
            ),
        ] = u.Field(default_factory=list)
        column_mappings: Annotated[
            t.StrMapping,
            u.Field(
                description="Singer column to Oracle column mapping",
            ),
        ] = u.Field(default_factory=dict)
