"""Compatibility module for legacy imports.

Exports OracleConnector from the main connector module.
"""

from __future__ import annotations

from flext_target_oracle.connector import OracleConnector

__all__ = ["OracleConnector"]
