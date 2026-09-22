"""Example usage of FLEXT Target Oracle.

This example demonstrates how to use the Oracle target to load
Singer-formatted data into an Oracle database.
"""

from __future__ import annotations

from pathlib import Path

from flext_target_oracle import FlextTargetOracleSettings, m, p, t
from flext_target_oracle.utilities import FlextTargetOracle

OracleMessage = (
    m.Meltano.SingerSchemaMessage
    | m.Meltano.SingerRecordMessage
    | m.Meltano.SingerStateMessage
    | m.Meltano.SingerActivateVersionMessage
)


def load_config() -> t.JsonMapping:
    """Load configuration from file."""
    config_path = Path("settings.json")
    content = config_path.read_text(encoding="utf-8")
    adapter: m.TypeAdapter[t.JsonMapping] = m.TypeAdapter(t.JsonMapping)
    config: t.JsonMapping = adapter.validate_json(content)
    return config


def load_singer_messages() -> t.SequenceOf[t.JsonMapping]:
    """Load Singer messages from JSONL file."""
    data_path = Path("singer_data.jsonl")
    adapter: m.TypeAdapter[t.JsonMapping] = m.TypeAdapter(t.JsonMapping)
    with data_path.open(encoding="utf-8") as f:
        return [adapter.validate_json(line) for line in f if line.strip()]


def main() -> None:
    """Run the example."""
    config_dict = load_config()
    settings = FlextTargetOracleSettings.model_validate(config_dict)
    target = FlextTargetOracle(settings)
    connection_result = target.test_connection()
    if connection_result.failure:
        raise SystemExit(1)
    messages = load_singer_messages()
    adapter: m.TypeAdapter[OracleMessage] = m.TypeAdapter(OracleMessage)
    for raw_message in messages:
        message: OracleMessage = adapter.validate_python(raw_message)
        result: p.Result[bool] = target.process_singer_message(message)
        if result.failure:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
