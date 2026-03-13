"""Example usage of FLEXT Target Oracle.

This example demonstrates how to use the Oracle target to load
Singer-formatted data into an Oracle database.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import TypeAdapter

from flext_target_oracle import FlextTargetOracle, FlextTargetOracleSettings


def load_config() -> dict[str, object]:
    """Load configuration from file."""
    config_path = Path("config.json")
    content = config_path.read_text(encoding="utf-8")
    return TypeAdapter(dict[str, object]).validate_json(content)


def load_singer_messages() -> list[dict[str, object]]:
    """Load Singer messages from JSONL file."""
    data_path = Path("singer_data.jsonl")
    adapter = TypeAdapter(dict[str, object])
    with data_path.open(encoding="utf-8") as f:
        return [adapter.validate_json(line) for line in f if line.strip()]


def main() -> None:
    """Run the example."""
    config_dict = load_config()
    config = FlextTargetOracleSettings.model_validate(config_dict)
    target = FlextTargetOracle(config=config)
    connection_result = target.test_connection()
    if connection_result.is_failure:
        return
    messages = load_singer_messages()
    for message in messages:
        msg_type = message.get("type", "UNKNOWN")
        if msg_type == "SCHEMA":
            message.get("stream", "unknown")
        elif msg_type == "RECORD":
            message.get("stream", "unknown")
            record = message.get("record", {})
            if isinstance(record, dict):
                record.get("id", "?")
        elif msg_type == "STATE":
            pass
        result = target.execute()
        if result.is_failure:
            return


if __name__ == "__main__":
    main()
