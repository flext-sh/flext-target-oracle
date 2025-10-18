"""Example usage of FLEXT Target Oracle.

This example demonstrates how to use the Oracle target to load
Singer-formatted data into an Oracle database.
"""

import json
from pathlib import Path

from flext_target_oracle import FlextTargetOracle, FlextTargetOracleConfig


def load_config() -> dict[str, object]:
    """Load configuration from file."""
    config_path = Path("config.json")
    with config_path.open(encoding="utf-8") as f:
        return json.load(f)


def load_singer_messages() -> list[dict[str, object]]:
    """Load Singer messages from JSONL file."""
    data_path = Path("singer_data.jsonl")
    with data_path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def main() -> None:
    """Run the example."""
    # Load configuration
    config_dict = load_config()

    config = FlextTargetOracleConfig.model_validate(config_dict)

    # Create target instance
    target = FlextTargetOracle(config=config)

    # Test connection to ensure target is ready
    connection_result = target.test_connection()
    if connection_result.is_failure:
        print(f"Connection failed: {connection_result.error}")
        return

    # Process Singer messages
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

        # Execute the target (no message processing in this API)
        result = target.execute()
        if result.is_failure:
            return

    # Show summary

    # Example queries


if __name__ == "__main__":
    main()
