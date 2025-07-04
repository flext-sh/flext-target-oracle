#!/usr/bin/env python3
"""
Verificação REAL de campos URL no banco Oracle.
Análise completa da verdade sobre o que está acontecendo.
"""


from sqlalchemy import text

from flext_target_oracle.connectors import OracleConnector


def check_real_database():
    """Verificar estado real do banco de dados."""

    # Config do .env
    config = {
        'host': '10.93.10.114',
        'port': 1522,
        'service_name': 'gbe8f3f2dbbc562_dwpdb_low.adb.oraclecloud.com',
        'username': 'oic',
        'password': 'aehaz232dfNuupah_#',
        'protocol': 'tcps',
        'default_target_schema': 'OIC'
    }

    print('🔍 CONECTANDO AO BANCO ORACLE REAL...')

    connector = OracleConnector(config)
    engine = connector._engine

    with engine.connect() as conn:
        print('✅ Conectado com sucesso!')

        # 1. Listar todas as tabelas do usuário
        print('\n📋 TABELAS NO SCHEMA OIC:')
        result = conn.execute(text('''
            SELECT table_name
            FROM user_tables
            WHERE table_name LIKE '%TEST%'
               OR table_name LIKE '%USERS%'
               OR table_name LIKE '%PRODUCTS%'
               OR table_name LIKE '%WMS_%'
            ORDER BY table_name
        '''))

        tables = []
        for row in result:
            table_name = row[0]
            tables.append(table_name)
            print(f'  📊 {table_name}')

        if not tables:
            print('  ⚠️ Nenhuma tabela de teste encontrada')
            return

        # 2. Verificar campos URL em TODAS as tabelas
        print('\n🚨 INVESTIGANDO CAMPOS URL:')
        url_fields_found = []

        for table_name in tables:
            result = conn.execute(text('''
                SELECT column_name, data_type, nullable
                FROM user_tab_columns
                WHERE table_name = :table_name
                AND (column_name LIKE '%URL%' OR column_name = 'URL')
                ORDER BY column_id
            '''), {'table_name': table_name})

            for row in result:
                column_name, data_type, nullable = row
                nullable_str = 'NULL' if nullable == 'Y' else 'NOT NULL'
                url_fields_found.append(f'{table_name}.{column_name}')
                print(f'  🚨 {table_name}.{column_name} ({data_type}) {nullable_str}')

        if not url_fields_found:
            print('  ✅ NENHUM CAMPO URL ENCONTRADO!')
        else:
            print(
                f'\n❌ PROBLEMA CONFIRMADO: {len(url_fields_found)} campos URL '
                f'encontrados!'
            )

        # 3. Verificar estrutura completa de uma tabela específica
        if tables:
            sample_table = tables[0]
            print(f'\n📊 ESTRUTURA COMPLETA DA TABELA {sample_table}:')

            result = conn.execute(text('''
                SELECT column_name, data_type, nullable
                FROM user_tab_columns
                WHERE table_name = :table_name
                ORDER BY column_id
            '''), {'table_name': sample_table})

            all_columns = []
            for row in result:
                column_name, data_type, nullable = row
                nullable_str = 'NULL' if nullable == 'Y' else 'NOT NULL'
                all_columns.append(column_name)

                # Destacar campos URL
                if 'URL' in column_name:
                    print(
                        f'  🚨 {column_name} {data_type} {nullable_str} '
                        f'<<<< CAMPO URL!'
                    )
                else:
                    print(f'  📝 {column_name} {data_type} {nullable_str}')

            print(f'\n📈 TOTAL DE COLUNAS: {len(all_columns)}')
            url_columns = [col for col in all_columns if 'URL' in col]
            if url_columns:
                print(f'❌ COLUNAS URL: {url_columns}')
            else:
                print('✅ Nenhuma coluna URL nesta tabela')

        # 4. Verificar dados reais em uma tabela
        if tables:
            sample_table = tables[0]
            try:
                result = conn.execute(text(f'''
                    SELECT COUNT(*) FROM {sample_table}
                '''))
                row_count = result.scalar()
                print(f'\n📊 DADOS NA TABELA {sample_table}: {row_count} registros')

                if row_count > 0:
                    result = conn.execute(text(f'''
                        SELECT * FROM {sample_table} WHERE ROWNUM <= 3
                    '''))
                    print('\n🔍 AMOSTRA DOS DADOS:')
                    for i, row in enumerate(result, 1):
                        print(f'  Registro {i}: {dict(row._mapping)}')

            except Exception as e:
                print(f'⚠️ Erro ao verificar dados: {e}')

if __name__ == '__main__':
    check_real_database()
