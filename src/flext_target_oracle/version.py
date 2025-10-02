"""Project metadata for flext target oracle."""

from __future__ import annotations

from typing import Final, cast

from flext_core.metadata import (
    FlextProjectVersion,
    build_metadata_exports,
)

_metadata = build_metadata_exports(__file__)
globals().update(_metadata)
_metadata_obj = cast("FlextProjectMetadata", _metadata["__flext_metadata__"])


class FlextTargetOracleVersion(FlextProjectVersion):
    """Structured metadata for the flext target oracle distribution."""

    @classmethod
    def current(cls) -> FlextTargetOracleVersion:
        """Return canonical metadata loaded from pyproject.toml."""
        return cls.from_metadata(_metadata_obj)


VERSION: Final[FlextTargetOracleVersion] = FlextTargetOracleVersion.current()
__version__: Final[str] = VERSION.version
__version_info__: Final[tuple[int | str, ...]] = VERSION.version_info

for _name in tuple(_metadata):
    if _name not in {"__version__", "__version_info__"}:
        globals().pop(_name, None)

__all__ = ["VERSION", "FlextTargetOracleVersion", "__version__", "__version_info__"]
