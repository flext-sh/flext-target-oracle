#!/usr/bin/env python3
"""
Teste com mock do Oracle para ver o comportamento real do target.
"""

import json
import unittest.mock
from io import StringIO

from flext_target_oracle.target import OracleTarget


def test_with_mocked_oracle() -> None:
    """Testa comportamento com Oracle mockado."""

    config = {
        "host": "localhost",
        "port": 1521,
        "service_name": "XEPDB1",
        "username": "test_user",
        "password": "test_password",
        "load_method": "append-only",
        "add_record_metadata": True,
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

    # Mock das operações de banco
    with unittest.mock.patch("sqlalchemy.create_engine") as mock_engine:
        # Setup do mock engine
        mock_conn = unittest.mock.MagicMock()
        mock_engine.return_value.connect.return_value.__enter__.return_value = mock_conn
        mock_engine.return_value.connect.return_value.__exit__.return_value = None
        mock_engine.return_value.begin = mock_conn

        # Mock do inspector para table_exists
        mock_inspector = unittest.mock.MagicMock()
        mock_inspector.has_table.return_value = False  # Tabela não existe

        with (
            unittest.mock.patch("sqlalchemy.inspect", return_value=mock_inspector),
            unittest.mock.patch.object(
                "flext_target_oracle.connectors.OracleConnector",
                "table_exists",
                return_value=False,
            ),
        ):

            # Criar target
            target = OracleTarget(config=config)
            print("🎯 Target created with mocked Oracle")

            # Simular entrada via StringIO
            input_stream = StringIO(input_data)

            try:
                print("📝 Starting process_lines with mocked Oracle...")
                result = target.process_lines(input_stream)
                print(f"✅ Process completed successfully, result: {result}")

                # Verificar quais métodos foram chamados
                print("\n🔍 Verificando chamadas para o banco:")
                connect_called = mock_engine.return_value.connect.called
                has_table_called = mock_inspector.has_table.called
                print(f"Engine.connect chamado: {connect_called}")
                print(f"Inspector.has_table chamado: {has_table_called}")

                if mock_conn.execute.called:
                    print("✅ Execute foi chamado - objetos foram processados!")
                    for call in mock_conn.execute.call_args_list:
                        print(f"  SQL executado: {call}")
                else:
                    print(
                        "❌ Execute NÃO foi chamado - objetos não foram " "processados!"
                    )

            except Exception as e:
                print(f"❌ ERROR during processing: {e}")
                import traceback

                traceback.print_exc()


def test_target_sink_creation() -> None:
    """Testa criação de sink especificamente."""

    config = {
        "host": "localhost",
        "port": 1521,
        "service_name": "XEPDB1",
        "username": "test_user",
        "password": "test_password",
        "load_method": "append-only",
    }

    # Mock do SQLAlchemy
    with unittest.mock.patch("sqlalchemy.create_engine"):
        mock_inspector = unittest.mock.MagicMock()
        mock_inspector.has_table.return_value = False

        with unittest.mock.patch("sqlalchemy.inspect", return_value=mock_inspector):
            target = OracleTarget(config=config)

            # Tentar criar um sink
            schema = {
                "properties": {"id": {"type": "integer"}, "name": {"type": "string"}}
            }

            try:
                sink = target.add_sink("test_stream", schema, ["id"])
                print(f"✅ Sink criado: {sink}")
                print(f"🔍 Sink class: {sink.__class__}")
                print(f"🔍 Sink stream: {sink.stream_name}")
                print(f"🔍 Sink schema: {sink.schema}")

                # Testar processamento de um batch
                test_records = [
                    {"id": 1, "name": "Test 1"},
                    {"id": 2, "name": "Test 2"},
                ]

                with unittest.mock.patch.object(
                    sink, "_execute_insert_batch"
                ) as mock_insert:
                    context = {"records": test_records}
                    sink.process_batch(context)
                    print("✅ process_batch chamado")

                    if mock_insert.called:
                        print("✅ _execute_insert_batch foi chamado!")
                    else:
                        print("❌ _execute_insert_batch NÃO foi chamado!")

            except Exception as e:
                print(f"❌ Erro ao criar sink: {e}")
                import traceback

                traceback.print_exc()


if __name__ == "__main__":
    print("🚀 TESTE: Análise de comportamento com Oracle mockado")
    print("=" * 80)

    try:
        test_target_sink_creation()
        print("\n" + "=" * 40 + "\n")
        test_with_mocked_oracle()

    except Exception as e:
        print(f"💥 ERRO CRÍTICO: {e}")
        import traceback

        traceback.print_exc()
