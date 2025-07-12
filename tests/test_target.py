# Copyright (c) 2025 FLEXT Team
# Licensed under the MIT License
# SPDX-License-Identifier: MIT

"""Test modern Oracle target implementation.

Unit tests for target orchestration and sink management.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pytest

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flext_target_oracle.target import OracleTarget


class TestOracleTarget:  """Test Oracle target functionality."""

    @staticmethod
    def test_target_initialization(flat_oracle_config: dict[str, Any]) -> None:  """Test Oracle target initialization with configuration.

        Args: flat_oracle_config: Flat configuration dictionary for Oracle target.

        """
        target = OracleTarget(config=flat_oracle_config)
        assert target.name == "target-oracle"
        assert target.oracle_config.connection.host == "localhost"

    @staticmethod
    def test_get_sink_requires_schema(flat_oracle_config: dict[str, Any]) -> None:  """Test that get_sink method requires schema parameter.

        Args: flat_oracle_config: Flat configuration dictionary for Oracle target.

        """
        target = OracleTarget(config=flat_oracle_config)

        with pytest.raises(ValueError, match="Schema is required"): target.get_sink("test_stream")

    @staticmethod
    def test_get_sink_with_schema(
        flat_oracle_config: dict[str, Any],
        sample_schema: dict[str, Any],
    ) -> None:  """Test get_sink method with valid schema parameter.

        Args: flat_oracle_config: Flat configuration dictionary for Oracle target.
            sample_schema: Sample JSON schema for testing.

        """
        target = OracleTarget(config=flat_oracle_config)

        sink = target.get_sink(
            "test_stream",
            schema=sample_schema,
            key_properties=["id"],
        )

        # Just verify we get a sink instance
        assert sink is not None
        # Verify sink has the expected attributes
        assert hasattr(sink, "stream_name")
        assert hasattr(sink, "schema")

    @staticmethod
    def test_config_jsonschema_includes_required_fields() -> None:  """Test that configuration JSON schema includes all required fields.

        Validates that host, username, and password fields are present
        and marked as required in the configuration schema.
        """
        schema = OracleTarget.config_jsonschema
        properties = schema["properties"]

        # Check required connection fields
        assert "host" in properties
        assert "username" in properties
        assert "password" in properties

        # Check required field validation
        required = schema.get("required", [])
        assert "host" in required
        assert "username" in required
        assert "password" in required
