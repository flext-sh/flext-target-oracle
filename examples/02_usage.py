"""Example usage of FLEXT Target Oracle.

This example demonstrates how to use the Oracle target to load
Singer-formatted data into an Oracle database.
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
    Sequence,
)
from pathlib import Path

from flext_core import t

from flext_target_oracle import FlextTargetOracle, FlextTargetOracleSettings, m


def load_config() -> Mapping[str, t.Container]:
    """Load configuration from file."""
    config_path = Path("settings.json")
    content = config_path.read_text(encoding="utf-8")
    adapter: m.TypeAdapter[Mapping[str, t.Container]] = m.TypeAdapter(
        Mapping[str, t.Container]
    )
    return adapter.validate_json(content)


def load_singer_messages() -> Sequence[Mapping[str, t.Container]]:
    """Load Singer messages from JSONL file."""
    data_path = Path("singer_data.jsonl")
    adapter: m.TypeAdapter[Mapping[str, t.Container]] = m.TypeAdapter(
        Mapping[str, t.Container]
    )
    with data_path.open(encoding="utf-8") as f:
        return [adapter.validate_json(line) for line in f if line.strip()]


def main() -> None:
    """Run the example."""
    config_dict = load_config()
    settings = FlextTargetOracleSettings.model_validate(config_dict)
    target = FlextTargetOracle(settings=settings)
    connection_result = target.test_connection()
    if connection_result.failure:
        return
    messages = load_singer_messages()
    for message in messages:
        msg_type = message.get("type", "UNKNOWN")
        if msg_type == "SCHEMA":
            message.get("stream", "unknown")
        elif msg_type == "RECORD":
            message.get("stream", "unknown")
            record_obj: t.Container = message.get("record", {})
            record_dict: Mapping[str, t.Container] = (
                record_obj if isinstance(record_obj, Mapping) else {}
            )
            record_dict.get("id", "?")
        elif msg_type == "STATE":
            pass
        result = target.execute()
        if result.failure:
            return


if __name__ == "__main__":
    main()
