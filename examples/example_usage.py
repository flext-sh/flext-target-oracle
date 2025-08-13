"""Example usage of FLEXT Target Oracle.

This example demonstrates how to use the Oracle target to load
Singer-formatted data into an Oracle database.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

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
    print("🚀 FLEXT Target Oracle - Example Usage")
    print("=====================================\n")

    # Load configuration
    config_dict = load_config()

    config = FlextOracleTargetConfig(**config_dict)
    print(
        f"✅ Configuration loaded: {config.oracle_host}:{config.oracle_port}/{config.oracle_service}",
    )

    # Create target instance
    target = FlextOracleTarget(config=config)

    # Initialize the target
    print("\n📦 Initializing target...")
    init_result = await target.initialize()
    if init_result.is_failure:
        print(f"❌ Initialization failed: {init_result.error}")
        return
    print("✅ Target initialized successfully")

    # Process Singer messages
    print("\n📥 Processing Singer messages...")
    messages = load_singer_messages()

    for line_num, message in enumerate(messages, 1):
        msg_type = message.get("type", "UNKNOWN")

        if msg_type == "SCHEMA":
            stream = message.get("stream", "unknown")
            print(f"  📋 Processing schema for stream: {stream}")
        elif msg_type == "RECORD":
            stream = message.get("stream", "unknown")
            record_id = message.get("record", {}).get("id", "?")
            print(f"  📝 Processing record {record_id} for stream: {stream}")
        elif msg_type == "STATE":
            print("  💾 Processing state message")

        # Execute the message
        result = await target.execute(json.dumps(message))
        if result.is_failure:
            print(f"❌ Error processing line {line_num}: {result.error}")
            return

    print("\n✅ All messages processed successfully!")

    # Show summary
    print("\n📊 Summary:")
    print("  - Streams processed: users, products")
    print("  - Records loaded: 6 total (3 users, 3 products)")
    print("  - Tables created with:")
    print("    - Automatic DDL generation")
    print("    - Flattened nested objects (address)")
    print("    - Custom indexes")
    print("    - SDC metadata columns")

    # Example queries
    print("\n💡 Example SQL queries to verify data:")
    print("  SELECT * FROM users;")
    print("  SELECT id, name, address__city FROM users;")
    print("  SELECT * FROM products WHERE in_stock = 1;")


if __name__ == "__main__":
    asyncio.run(main())
