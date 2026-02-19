"""Utility helpers for Oracle Singer target integration."""

from __future__ import annotations

import json

from flext_core import FlextResult, FlextTypes as t


class FlextTargetOracleUtilities:
    """Focused utility namespace used by Oracle target modules."""

    class TargetOracle:
        """Singer message creation and validation helpers."""

        @staticmethod
        def create_schema_message(
            stream_name: str,
            schema: dict[str, t.GeneralValueType],
            key_properties: list[str] | None = None,
        ) -> dict[str, t.GeneralValueType]:
            """Create a Singer SCHEMA message."""
            return {
                "type": "SCHEMA",
                "stream": stream_name,
                "schema": schema,
                "key_properties": key_properties or [],
            }

        @staticmethod
        def create_record_message(
            stream_name: str,
            record: dict[str, t.GeneralValueType],
            time_extracted: str | None = None,
        ) -> dict[str, t.GeneralValueType]:
            """Create a Singer RECORD message."""
            message: dict[str, t.GeneralValueType] = {
                "type": "RECORD",
                "stream": stream_name,
                "record": record,
            }
            if time_extracted is not None:
                message["time_extracted"] = time_extracted
            return message

        @staticmethod
        def create_state_message(
            state: dict[str, t.GeneralValueType],
        ) -> dict[str, t.GeneralValueType]:
            """Create a Singer STATE message."""
            return {"type": "STATE", "value": state}

        @staticmethod
        def validate_singer_message(
            message: dict[str, t.GeneralValueType],
        ) -> FlextResult[dict[str, t.GeneralValueType]]:
            """Validate supported Singer message types."""
            msg_type = message.get("type")
            if msg_type not in {"SCHEMA", "RECORD", "STATE"}:
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    f"Unsupported Singer message type: {msg_type}",
                )
            return FlextResult[dict[str, t.GeneralValueType]].ok(message)

    class OracleDataProcessing:
        """Data conversion helpers for Oracle storage."""

        @staticmethod
        def transform_record_for_oracle(
            record: dict[str, t.GeneralValueType],
        ) -> FlextResult[dict[str, t.GeneralValueType]]:
            """Normalize record values for Oracle persistence."""
            transformed: dict[str, t.GeneralValueType] = {}
            for key, value in record.items():
                if isinstance(value, (dict, list)):
                    transformed[key.upper()] = json.dumps(value)
                elif isinstance(value, bool):
                    transformed[key.upper()] = 1 if value else 0
                else:
                    transformed[key.upper()] = value
            return FlextResult[dict[str, t.GeneralValueType]].ok(transformed)

    class ConfigValidation:
        """Configuration validation helpers."""

        @staticmethod
        def validate_oracle_connection_config(
            config: dict[str, t.GeneralValueType],
        ) -> FlextResult[dict[str, t.GeneralValueType]]:
            """Ensure mandatory Oracle connection keys are present."""
            required = ["host", "port", "service_name", "username", "password"]
            for key in required:
                if key not in config:
                    return FlextResult[dict[str, t.GeneralValueType]].fail(
                        f"Missing required Oracle config field: {key}",
                    )
            return FlextResult[dict[str, t.GeneralValueType]].ok(config)


u = FlextTargetOracleUtilities

__all__ = ["FlextTargetOracleUtilities", "u"]
