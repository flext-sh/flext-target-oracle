#!/usr/bin/env python3
"""
Teste para descobrir por que o flext-target-oracle não está gravando objetos.
"""

import json
from io import StringIO

from flext_target_oracle.target import OracleTarget


def test_simple_object_insertion() -> None:
    """Teste simples para ver se objetos são gravados."""

    # Configuração básica
    config = {
        "host": "localhost",
        "port": 1521,
        "service_name": "XEPDB1",
        "username": "test_user",
        "password": "test_password",
        "load_method": "append-only",
        "add_record_metadata": True,
        "batch_size": 1000,
        "debug_type_mapping": True,
        "log_level": "DEBUG",
    }

    # Dados de teste - mensagens Singer
    singer_messages = [
        # SCHEMA message
        {
            "type": "SCHEMA",
            "stream": "test_objects",
            "schema": {
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "status": {"type": "string"},
                }
            },
            "key_properties": ["id"],
        },
        # RECORD messages
        {
            "type": "RECORD",
            "stream": "test_objects",
            "record": {"id": 1, "name": "Test Object 1", "status": "active"},
        },
        {
            "type": "RECORD",
            "stream": "test_objects",
            "record": {"id": 2, "name": "Test Object 2", "status": "inactive"},
        },
    ]

    # Converter mensagens para JSON lines
    input_data = "\n".join(json.dumps(msg) for msg in singer_messages)
    print("🔍 Input data:")
    print(input_data)
    print("\n" + "=" * 80 + "\n")

    # Criar target
    target = OracleTarget(config=config)
    print("🎯 Target created")

    # Simular entrada via StringIO
    input_stream = StringIO(input_data)

    try:
        print("📝 Starting process_lines...")
        result = target.process_lines(input_stream)
        print(f"✅ Process completed, result: {result}")

    except Exception as e:
        print(f"❌ ERROR during processing: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 80)
    print("🏁 Test completed")


def test_debug_target_behavior() -> None:
    """Testa comportamento específico do target."""

    config = {
        "host": "localhost",
        "port": 1521,
        "service_name": "XEPDB1",
        "username": "test_user",
        "password": "test_password",
        "load_method": "append-only",
        "debug_type_mapping": True,
        "log_level": "DEBUG",
        "skip_table_optimization": True,
    }

    target = OracleTarget(config=config)

    print("🔍 Target config keys:")
    for key, value in target.config.items():
        print(f"  {key}: {value}")

    print(f"\n🎯 Target name: {target.name}")
    print(f"🎯 Default sink class: {target.default_sink_class}")
    print(f"🎯 Type conformance level: {target.TYPE_CONFORMANCE_LEVEL}")


if __name__ == "__main__":
    print("🚀 TESTE: Descobrindo por que objetos não são gravados")
    print("=" * 80)

    try:
        test_debug_target_behavior()
        print("\n" + "=" * 40 + "\n")
        test_simple_object_insertion()

    except Exception as e:
        print(f"💥 ERRO CRÍTICO: {e}")
        import traceback

        traceback.print_exc()
