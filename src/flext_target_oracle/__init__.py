# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Oracle package."""

from __future__ import annotations

from flext_core import d, e, h, r, s, x
from flext_core.lazy import install_lazy_exports
from flext_target_oracle.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)
from flext_target_oracle._exports_lazy import FLEXT_TARGET_ORACLE_LAZY_IMPORTS

_LAZY_IMPORTS = FLEXT_TARGET_ORACLE_LAZY_IMPORTS


_EAGER_EXPORTS = (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
    d,
    e,
    h,
    r,
    s,
    x,
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    *_LAZY_IMPORTS,
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "d",
    "e",
    "h",
    "r",
    "s",
    "x",
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    public_exports=_PUBLIC_EXPORTS,
)
