"""Example usage of FLEXT Target Oracle.

This example demonstrates how to use the Oracle target to load
Singer-formatted data into an Oracle database.
"""

from __future__ import annotations

import json
from pathlib import Path

from flext_core import t

from flext_target_oracle import FlextTargetOracle, FlextTargetOracleSettings


def load_config() -> dict[str, t.ContainerValue]:
    """Load configuration from file."""
    config_path = Path("config.json")
    with config_path.open(encoding="utf-8") as f:
        return json.load(f)


def load_singer_messages() -> list[dict[str, t.ContainerValue]]:
    """Load Singer messages from JSONL file."""
    data_path = Path("singer_data.jsonl")
    with data_path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


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
