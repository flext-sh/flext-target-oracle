# Copyright (c) 2025 FLEXT Team
# Licensed under the MIT License
# SPDX-License-Identifier: MIT

"""Test environment configuration validation.

This module validates that the .env file contains the required configuration
for connecting to Oracle Database and conditionally runs tests based on: environment availability.
"""

from pathlib import Path

import pytest


class TestEnvironmentValidation:  """Test environment configuration validation."""

    @staticmethod
    def test_env_file_exists(project_root: Path) -> None: env_path = project_root / ".env"
        if not env_path.exists(): pytest.skip(".env file not found - copy .env.example to .env and configure")
        assert env_path.exists(), "Environment file .env is required for tests"

    @staticmethod
    def test_env_example_exists(project_root: Path) -> None: env_example_path = project_root / ".env.example"
        assert env_example_path.exists(), ".env.example file should exist"

    @staticmethod
    def test_required_env_vars(env_config: dict[str, str]) -> None: required_vars = ["host", "username", "password", "service_name"]

        for var in required_vars: assert var in env_config, f"Required environment variable {var} is missing"
            assert env_config[var], f"Required environment variable {var} is empty"

    @staticmethod
    def test_port_configuration(env_config: dict[str, str]) -> None:
            port = env_config.get("port", 1521)
        assert isinstance(port, int), "Port must be an integer"
        assert 1 <= port <= 65535, f"Port {port} is out of valid range"

    @staticmethod
    def test_protocol_configuration(env_config: dict[str, str]) -> None:
            protocol = env_config.get("protocol", "tcp")
        assert protocol in {"tcp", "tcps"}, f"Invalid protocol: {protocol}"

        # If using TCPS, additional fields might be required
        if protocol == "tcps" and "wallet_location" in env_config: # Check for SSL-related configuration
            assert env_config[
                "wallet_location"
            ], "Wallet location cannot be empty for TCPS"

    @staticmethod
    def test_optional_performance_settings(env_config: dict[str, str]) -> None:
        # Check batch size if specified: if "batch_size" in env_config: batch_size = int(env_config["batch_size"])
            assert batch_size > 0, "Batch size must be positive"
            assert batch_size <= 100000, "Batch size seems too large"

        # Check parallel threads if specified: if "parallel_threads" in env_config: threads = int(env_config["parallel_threads"])
            assert threads > 0, "Parallel threads must be positive"
            assert threads <= 32, "Too many parallel threads"

        # Check pool size if specified: if "pool_size" in env_config: pool_size = int(env_config["pool_size"])
            assert pool_size > 0, "Pool size must be positive"
            assert pool_size <= 100, "Pool size seems too large"

    @pytest.mark.skipif(
        not Path(".env").exists(),
        reason="Requires .env file with Oracle configuration",
    )

    @staticmethod
    def test_connection_string_format(env_config: dict[str, str]) -> None:
        # Verify we can build a connection string
        host = env_config["host"]
        env_config.get("port", 1521)
        service_name = env_config.get("service_name", "")

        # Basic validation
        assert ":" not in host or "[" in host, "IPv6 addresses should be bracketed"
        assert service_name or env_config.get(
            "database",
        ), "Either service_name or database (SID) must be provided"

    @staticmethod
    def test_schema_configuration(env_config: dict[str, str]) -> None:
            if "schema" in env_config: schema =  env_config["schema"]
            assert schema, "Schema cannot be empty if specified"
            assert len(schema) <= 30, "Oracle schema name too long (max 30 chars)"
            assert (
                schema.replace("_", "").replace("$", "").replace("#", "").isalnum()
            ), "Schema name contains invalid characters"

    @staticmethod
    def test_license_flags(env_config: dict[str, str]) -> None:
                license_flags = [
            "oracle_has_partitioning_option",
            "oracle_has_compression_option",
            "oracle_has_inmemory_option",
            "oracle_has_advanced_security_option",
        ]

        for flag in license_flags: if flag in env_config = env_config[flag]:
                # Should be convertible to boolean
                assert value.lower() in {
                    "true",
                    "false",
                    "1",
                    "0",
                    "yes",
                    "no",
                }, f"License flag {flag} must be a boolean value"

    @pytest.mark.parametrize(
        ("config_key", "max_value"),
        [
            ("array_size", 100000),
            ("prefetch_rows", 50000),
            ("statement_cache_size", 1000),
            ("chunk_size", 100000),
            ("merge_batch_size", 50000),
        ],
    )

    @staticmethod
    def test_numeric_limits(
        env_config: dict[str, str],
        config_key: str,
        max_value: int,
    ) -> None: if config_key in env_config:
            value = int(env_config[config_key])
                assert value > 0, f"{config_key} must be positive"
                assert (
                    value <= max_value
                ), f"{config_key} value {value} exceeds reasonable limit {max_value}"
            except Exception: # TODO(@flext-team): Consider using else block
                pytest.fail(f"{config_key} must be a valid integer")

    @staticmethod
    def test_compression_settings(env_config: dict[str, str]) -> None: if env_config.get("enable_compression", "").lower() == "true": compression_type = env_config.get("compression_type", "basic")
            assert compression_type in {
                "basic",
                "advanced",
                "hybrid",
                "archive",
            }, f"Invalid compression type: {compression_type}"

            # If advanced compression is used, license flag should be set
            if compression_type != "basic" and "oracle_has_compression_option" in env_config: assert env_config["oracle_has_compression_option"].lower() in {
                    "true",
                    "1",
                    "yes",
                }, (
                    f"Advanced compression type '{compression_type}' requires "
                    f"oracle_has_compression_option=true"
                )
