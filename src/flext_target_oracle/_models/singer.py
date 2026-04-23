"""Singer message model specializations for Oracle target."""

from __future__ import annotations

from types import MappingProxyType
from typing import Annotated

from flext_meltano import m, t, u


class FlextTargetOracleModelsSinger:
    """Singer message MRO mixin for TargetOracle namespace."""

    class Meltano(m.Meltano):
        """Namespaced Meltano runtime model references (inherits all Singer types)."""

    class SingerSchemaMessage(m.Meltano.SingerSchemaMessage):
        """Singer SCHEMA message specialized for Oracle target domain."""

    class SingerRecordMessage(m.Meltano.SingerRecordMessage):
        """Singer RECORD message specialized for Oracle target domain."""

    class SingerStateMessage(m.Meltano.SingerStateMessage):
        """Singer STATE message specialized for Oracle target domain."""

    class SingerActivateVersionMessage(
        m.Meltano.SingerActivateVersionMessage,
    ):
        """Singer ACTIVATE_VERSION message specialized for Oracle target domain."""

    class SingerCatalogMetadata(m.Meltano.SingerCatalogMetadata):
        """Singer catalog metadata specialized for Oracle target domain."""

    class SingerCatalogEntry(m.Meltano.SingerCatalogEntry):
        """Singer catalog entry specialized for Oracle target domain."""

    class SingerCatalog(m.Meltano.SingerCatalog):
        """Singer catalog specialized for Oracle target domain."""

    class SingerStreamModel(m.ArbitraryTypesModel):
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
        ] = u.Field(default_factory=tuple)
        column_mappings: Annotated[
            t.StrMapping,
            u.Field(
                description="Singer column to Oracle column mapping",
            ),
        ] = u.Field(default_factory=lambda: MappingProxyType({}))
