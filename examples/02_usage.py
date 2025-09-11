"""Example usage of FLEXT Target Oracle.

This example demonstrates how to use the Oracle target to load
Singer-formatted data into an Oracle database.
"""

import asyncio
import json
from pathlib import Path

from flext_target_oracle import FlextOracleTarget, FlextOracleTargetConfig


def load_config() -> dict:
    """Load configuration from file."""
    config_path = Path("config.json")
    with config_path.open(encoding="utf-8") as f:
        return json.load(f)


def load_singer_messages() -> list[dict]:
    """Load Singer messages from JSONL file."""
    data_path = Path("singer_data.jsonl")
    with data_path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


async def main() -> None:
    """Run the example."""
    # Load configuration
    config_dict = load_config()

    config = FlextOracleTargetConfig(**config_dict)

    # Create target instance
    target = FlextOracleTarget(config=config)

    # Initialize the target
    init_result = await target.initialize()
    if init_result.is_failure:
        return

    # Process Singer messages
    messages = load_singer_messages()

    for message in messages:
        msg_type = message.get("type", "UNKNOWN")

        if msg_type == "SCHEMA":
            message.get("stream", "unknown")
        elif msg_type == "RECORD":
            message.get("stream", "unknown")
            message.get("record", {}).get("id", "?")
        elif msg_type == "STATE":
            pass

        # Execute the message
        result = await target.execute(json.dumps(message))
        if result.is_failure:
            return

    # Show summary

    # Example queries


if __name__ == "__main__":
    asyncio.run(main())
