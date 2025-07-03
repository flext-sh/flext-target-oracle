#!/usr/bin/env python3
"""
Teste para verificar logging detalhado de inserções do Oracle Target.
"""

import json
import sys
import io
from flext_target_oracle import OracleTarget

def test_detailed_logging():
    """Testar logging detalhado com dados simulados."""
    print("🧪 TESTANDO LOGGING DETALHADO DO ORACLE TARGET")
    print("=" * 60)
    
    # Configuração de teste (sem conexão real)
    config = {
        'host': 'localhost',
        'username': 'test',
        'password': 'test',
        'database': 'XE',
        'log_level': 'INFO',
        'log_format': 'text',  # Usar texto para facilitar leitura
        'log_batch_details': True,
        'echo': True,  # Habilitar SQL logging
        'log_sql_statements': True
    }
    
    # Criar target
    target = OracleTarget(config=config, validate_config=False)
    
    # Simular entrada Singer com schema e records
    singer_messages = [
        # Schema message
        json.dumps({
            "type": "SCHEMA",
            "stream": "test_orders",
            "schema": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "integer"},
                    "customer_name": {"type": "string", "maxLength": 100},
                    "order_date": {"type": "string", "format": "date-time"},
                    "total_amount": {"type": "number"},
                    "status": {"type": "string"}
                }
            },
            "key_properties": ["order_id"]
        }),
        # Record messages
        json.dumps({
            "type": "RECORD",
            "stream": "test_orders",
            "record": {
                "order_id": 1001,
                "customer_name": "João Silva",
                "order_date": "2024-01-15T10:30:00Z",
                "total_amount": 150.75,
                "status": "confirmed"
            }
        }),
        json.dumps({
            "type": "RECORD",
            "stream": "test_orders", 
            "record": {
                "order_id": 1002,
                "customer_name": "Maria Santos",
                "order_date": "2024-01-15T11:15:00Z",
                "total_amount": 89.90,
                "status": "pending"
            }
        }),
        json.dumps({
            "type": "RECORD",
            "stream": "test_orders",
            "record": {
                "order_id": 1003,
                "customer_name": "Pedro Costa",
                "order_date": "2024-01-15T12:00:00Z", 
                "total_amount": 275.50,
                "status": "confirmed"
            }
        }),
        # State message
        json.dumps({
            "type": "STATE",
            "value": {"bookmark_properties": ["order_date"]}
        })
    ]
    
    # Converter para input stream
    input_data = '\n'.join(singer_messages)
    input_stream = io.StringIO(input_data)
    
    print(f"📥 SIMULANDO INPUT COM {len(singer_messages)} MENSAGENS SINGER")
    print(f"📊 Mensagens: 1 SCHEMA, 3 RECORDS, 1 STATE")
    print()
    
    try:
        # Processar com logging detalhado
        print("🚀 INICIANDO PROCESSAMENTO...")
        target.process_lines(input_stream)
        print("✅ PROCESSAMENTO CONCLUÍDO")
        
    except Exception as e:
        print(f"❌ ERRO DURANTE PROCESSAMENTO: {e}")
        print("📋 Este erro é esperado pois não temos conexão real com Oracle")
        print("🎯 O IMPORTANTE é verificar se os logs detalhados aparecem acima")
        
    print()
    print("🔍 VERIFICAÇÕES:")
    print("1. Você deve ver logs '🔍 ORACLE TARGET - RECEIVED INPUT'")
    print("2. Você deve ver logs '📊 SINGER MESSAGE ANALYSIS'") 
    print("3. Você deve ver logs '📝 SAMPLE RECORDS PREVIEW'")
    print("4. Você deve ver logs '🏗️ CREATING ORACLE SINK'")
    print("5. Você deve ver logs '📋 SAMPLE RECORD FOR SINK'")
    print("6. Você deve ver logs '📐 SCHEMA FOR SINK'")
    print("7. Se chegarem até o sink, verá '📦 ORACLE SINK - PROCESSING BATCH'")

if __name__ == "__main__":
    test_detailed_logging()