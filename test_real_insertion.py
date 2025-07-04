#!/usr/bin/env python3
"""
Teste REAL de inserção de dados no Oracle.
Verificar onde está o erro específico.
"""

import json
from io import StringIO

from sqlalchemy import text

from flext_target_oracle.target import OracleTarget


def test_real_data_insertion():
    """Testar inserção real de dados com schema que tem URL."""

    print('🚀 TESTE REAL DE INSERÇÃO DE DADOS')

    # Configuração real
    config = {
        'host': '10.93.10.114',
        'port': 1522,
        'service_name': 'gbe8f3f2dbbc562_dwpdb_low.adb.oraclecloud.com',
        'username': 'oic',
        'password': 'aehaz232dfNuupah_#',
        'protocol': 'tcps',
        'default_target_schema': 'OIC',
        'load_method': 'append-only'
    }

    # Schema com campo URL (o que estava causando problema)
    schema_with_url = {
        "type": "SCHEMA",
        "stream": "test_url_filtering",
        "schema": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "url": {"type": "string"},  # ESTE CAMPO DEVERIA SER FILTRADO
                "product_url": {"type": "string"},  # ESTE TAMBÉM
                "metadata": {"type": "object"}
            }
        },
        "key_properties": ["id"]
    }

    # Record com dados URL
    record_with_url = {
        "type": "RECORD",
        "stream": "test_url_filtering",
        "record": {
            "id": 1,
            "name": "Test Product",
            "url": "https://example.com/product/1",  # ESTE DADO DEVERIA SER FILTRADO
            "product_url": "https://shop.com/item/1",  # ESTE TAMBÉM
            "metadata": {"category": "electronics"}
        },
        "time_extracted": "2025-07-03T20:30:00Z"
    }

    try:
        print('\n1️⃣ Criando target Oracle...')
        target = OracleTarget(config=config)
        print('✅ Target criado com sucesso')

        print('\n2️⃣ Processando schema...')
        # Simular processamento do schema
        input_data = json.dumps(schema_with_url) + '\n' + json.dumps(record_with_url)

        print('\n3️⃣ Testando filtros de schema...')
        # Testar se o schema está sendo filtrado corretamente
        sink = target.get_sink(
            "test_url_filtering",
            schema=schema_with_url["schema"],
            key_properties=["id"]
        )

        print(
            f'📊 Schema original: {len(schema_with_url["schema"]["properties"])} '
            f'campos'
        )
        print(
            f'📊 Campos originais: '
            f'{list(schema_with_url["schema"]["properties"].keys())}'
        )

        # Verificar schema conformado
        conformed_schema = sink.conform_schema(schema_with_url["schema"])
        print(f'📊 Schema conformado: {len(conformed_schema["properties"])} campos')
        print(f'📊 Campos conformados: {list(conformed_schema["properties"].keys())}')

        print('\n4️⃣ Testando filtros de record...')
        # Testar se o record está sendo filtrado corretamente
        conformed_record = sink._conform_record(record_with_url["record"])
        print(f'📊 Record original: {len(record_with_url["record"])} campos')
        print(f'📊 Campos originais: {list(record_with_url["record"].keys())}')
        print(f'📊 Record conformado: {len(conformed_record)} campos')
        print(f'📊 Campos conformados: {list(conformed_record.keys())}')

        print('\n5️⃣ Processando dados reais...')
        with StringIO(input_data) as input_stream:
            target.process_lines(input_stream)

        print('\n6️⃣ Verificando no banco...')
        # Verificar se os dados foram inseridos
        from flext_target_oracle.connectors import OracleConnector
        connector = OracleConnector(config)
        with connector._engine.connect() as conn:
            result = conn.execute(
                text('SELECT COUNT(*) FROM TEST_URL_FILTERING')
            )
            count = result.scalar()
            print(f'📊 Registros inseridos: {count}')

            if count > 0:
                result = conn.execute(
                    text('SELECT * FROM TEST_URL_FILTERING WHERE ROWNUM <= 1')
                )
                for row in result:
                    print(f'📊 Dados inseridos: {dict(row._mapping)}')

            # Verificar estrutura da tabela criada
            result = conn.execute(text('''
                SELECT column_name FROM user_tab_columns
                WHERE table_name = 'TEST_URL_FILTERING'
                ORDER BY column_id
            '''))

            columns = [row[0] for row in result]
            print(f'📊 Colunas na tabela: {columns}')

            # Verificar se há campos URL
            url_columns = [col for col in columns if 'URL' in col]
            if url_columns:
                print(f'❌ AINDA HÁ CAMPOS URL: {url_columns}')
                return False
            else:
                print('✅ Nenhum campo URL na tabela criada!')
                return True

    except Exception as e:
        print(f'\n❌ ERRO DURANTE TESTE: {e}')
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = test_real_data_insertion()
    print(f'\n📊 RESULTADO: {"✅ SUCESSO" if success else "❌ FALHOU"}')
