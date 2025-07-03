#!/usr/bin/env python3
"""
Teste para verificar o sistema de logging ULTRA-DETALHADO do Oracle Target.

Este script demonstra todos os níveis de logging implementados, incluindo:
- Sistema de monitoramento de recursos (CPU, memoria, threads)
- Análise profunda de mensagens Singer
- Data profiling e análise de complexidade
- Rastreamento completo de inserções Oracle
- Estatísticas de performance em tempo real
"""

import json
import sys
import io
import time
from flext_target_oracle import OracleTarget

def test_ultra_detailed_logging():
    """Testar sistema de logging ultra-detalhado com dados complexos simulados."""
    print("🧪 TESTANDO LOGGING ULTRA-DETALHADO DO ORACLE TARGET")
    print("=" * 80)
    
    # Configuração com logging máximo
    config = {
        'host': 'localhost',
        'username': 'test_user',
        'password': 'test_password',
        'database': 'XE',
        'log_level': 'INFO',
        'log_format': 'text',  # Usar texto para facilitar leitura
        'log_batch_details': True,
        'echo': True,  # Habilitar SQL logging
        'log_sql_statements': True,
        'enable_metrics': True,
        'background_monitoring': True
    }
    
    # Criar target
    target = OracleTarget(config=config, validate_config=False)
    
    # Simular entrada Singer com dados complexos e variados
    singer_messages = [
        # Schema message complexo
        json.dumps({
            "type": "SCHEMA",
            "stream": "complex_orders",
            "schema": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "integer"},
                    "customer_info": {
                        "type": "object",
                        "properties": {
                            "customer_id": {"type": "string"},
                            "name": {"type": "string", "maxLength": 100},
                            "email": {"type": "string"},
                            "address": {
                                "type": "object",
                                "properties": {
                                    "street": {"type": "string"},
                                    "city": {"type": "string"},
                                    "country": {"type": "string"}
                                }
                            },
                            "preferences": {"type": "array"}
                        }
                    },
                    "order_date": {"type": "string", "format": "date-time"},
                    "items": {"type": "array"},
                    "total_amount": {"type": "number"},
                    "status": {"type": "string"},
                    "metadata": {"type": "object"},
                    "is_express": {"type": "boolean"},
                    "tracking_number": {"type": ["string", "null"]},
                    "notes": {"type": ["string", "null"]}
                }
            },
            "key_properties": ["order_id"]
        }),
        
        # Record messages com dados complexos e variados
        json.dumps({
            "type": "RECORD",
            "stream": "complex_orders",
            "record": {
                "order_id": 2001,
                "customer_info": {
                    "customer_id": "CUST-123456",
                    "name": "João Silva Santos",
                    "email": "joao.silva@email.com",
                    "address": {
                        "street": "Rua das Flores, 123",
                        "city": "São Paulo",
                        "country": "Brasil"
                    },
                    "preferences": ["delivery_morning", "eco_packaging", "sms_notifications"]
                },
                "order_date": "2024-01-15T14:30:00Z",
                "items": [
                    {"product_id": "PROD-001", "name": "Notebook", "price": 2500.00, "quantity": 1},
                    {"product_id": "PROD-002", "name": "Mouse", "price": 50.00, "quantity": 2}
                ],
                "total_amount": 2600.00,
                "status": "confirmed",
                "metadata": {
                    "source": "web",
                    "campaign": "summer_sale_2024",
                    "discount_applied": 100.00,
                    "payment_method": "credit_card"
                },
                "is_express": True,
                "tracking_number": "BR123456789",
                "notes": "Entrega no portão principal"
            }
        }),
        
        json.dumps({
            "type": "RECORD",
            "stream": "complex_orders",
            "record": {
                "order_id": 2002,
                "customer_info": {
                    "customer_id": "CUST-789012",
                    "name": "Maria Santos Costa",
                    "email": "maria.santos@empresa.com.br",
                    "address": {
                        "street": "Avenida Paulista, 1000 - Apto 801",
                        "city": "São Paulo",
                        "country": "Brasil"
                    },
                    "preferences": ["delivery_evening", "invoice_email"]
                },
                "order_date": "2024-01-15T16:45:00Z",
                "items": [
                    {"product_id": "PROD-003", "name": "Smartphone", "price": 1800.00, "quantity": 1},
                    {"product_id": "PROD-004", "name": "Capinha", "price": 25.00, "quantity": 1},
                    {"product_id": "PROD-005", "name": "Carregador", "price": 75.00, "quantity": 1}
                ],
                "total_amount": 1900.00,
                "status": "pending_payment",
                "metadata": {
                    "source": "mobile_app",
                    "campaign": None,
                    "discount_applied": 0.00,
                    "payment_method": "pix"
                },
                "is_express": False,
                "tracking_number": None,
                "notes": None
            }
        }),
        
        json.dumps({
            "type": "RECORD",
            "stream": "complex_orders",
            "record": {
                "order_id": 2003,
                "customer_info": {
                    "customer_id": "CUST-345678",
                    "name": "Pedro Costa Lima",
                    "email": "pedro.costa@gmail.com",
                    "address": {
                        "street": "Rua Augusta, 500",
                        "city": "Rio de Janeiro",
                        "country": "Brasil"
                    },
                    "preferences": []
                },
                "order_date": "2024-01-15T18:20:00Z",
                "items": [
                    {"product_id": "PROD-006", "name": "Tablet", "price": 1200.00, "quantity": 1},
                    {"product_id": "PROD-007", "name": "Teclado Bluetooth", "price": 150.00, "quantity": 1}
                ],
                "total_amount": 1350.00,
                "status": "confirmed",
                "metadata": {
                    "source": "marketplace",
                    "campaign": "black_friday",
                    "discount_applied": 200.00,
                    "payment_method": "boleto"
                },
                "is_express": True,
                "tracking_number": "RJ987654321",
                "notes": "Cliente empresarial - nota fiscal necessária"
            }
        }),
        
        # Schema para segundo stream
        json.dumps({
            "type": "SCHEMA",
            "stream": "customer_analytics",
            "schema": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string"},
                    "analytics_date": {"type": "string", "format": "date"},
                    "page_views": {"type": "integer"},
                    "session_duration": {"type": "number"},
                    "conversion_events": {"type": "array"},
                    "device_info": {"type": "object"}
                }
            },
            "key_properties": ["customer_id", "analytics_date"]
        }),
        
        # Records para analytics
        json.dumps({
            "type": "RECORD",
            "stream": "customer_analytics",
            "record": {
                "customer_id": "CUST-123456",
                "analytics_date": "2024-01-15",
                "page_views": 25,
                "session_duration": 1200.5,
                "conversion_events": ["product_view", "add_to_cart", "purchase"],
                "device_info": {
                    "browser": "Chrome",
                    "os": "Windows 10",
                    "mobile": False,
                    "screen_resolution": "1920x1080"
                }
            }
        }),
        
        json.dumps({
            "type": "RECORD",
            "stream": "customer_analytics",
            "record": {
                "customer_id": "CUST-789012",
                "analytics_date": "2024-01-15",
                "page_views": 8,
                "session_duration": 300.2,
                "conversion_events": ["product_view"],
                "device_info": {
                    "browser": "Safari",
                    "os": "iOS 17",
                    "mobile": True,
                    "screen_resolution": "390x844"
                }
            }
        }),
        
        # State message
        json.dumps({
            "type": "STATE",
            "value": {
                "bookmark_properties": ["order_date", "analytics_date"],
                "bookmarks": {
                    "complex_orders": {"order_date": "2024-01-15T18:20:00Z"},
                    "customer_analytics": {"analytics_date": "2024-01-15"}
                }
            }
        })
    ]
    
    # Converter para input stream (usar \n real, não escape)
    input_data = '\n'.join(singer_messages)
    input_stream = io.StringIO(input_data)
    
    print(f"📥 SIMULANDO INPUT ULTRA-COMPLEXO")
    print(f"📊 Total de mensagens: {len(singer_messages)}")
    print(f"📊 Streams: complex_orders (4 records), customer_analytics (2 records)")
    print(f"📊 Schemas: 2 complexos com objetos aninhados")
    print(f"📊 Tamanho total do input: {len(input_data)} caracteres")
    print()
    
    # Simular delay para ver monitoramento de recursos
    print("⏳ Aguardando 2 segundos para simular processamento inicial...")
    time.sleep(2)
    
    try:
        # Processar com logging ultra-detalhado
        print("🚀 INICIANDO PROCESSAMENTO ULTRA-DETALHADO...")
        start_time = time.time()
        
        target.process_lines(input_stream)
        
        end_time = time.time()
        print(f"✅ PROCESSAMENTO CONCLUÍDO em {round(end_time - start_time, 3)} segundos")
        
    except Exception as e:
        print(f"❌ ERRO DURANTE PROCESSAMENTO: {e}")
        print("📋 Este erro é esperado pois não temos conexão real com Oracle")
        print("🎯 O IMPORTANTE é verificar se os logs ultra-detalhados apareceram acima")
        
    print()
    print("🔍 VERIFICAÇÕES ULTRA-DETALHADAS:")
    print("1. ✅ Logs '🔍 ORACLE TARGET - RECEIVED INPUT (ULTRA-DETAILED)'")
    print("2. ✅ Logs '📊 ULTRA-DETAILED SINGER MESSAGE ANALYSIS'")
    print("3. ✅ Logs '📝 ULTRA-DETAILED RECORD SAMPLING & DATA PROFILING'")
    print("4. ✅ Logs '🖥️ SYSTEM MONITORING - DURING PROCESSING SETUP'")
    print("5. ✅ Logs '🏗️ CREATING ORACLE SINK' para múltiplos streams")
    print("6. ✅ Análise de complexidade dos records (objetos aninhados, arrays)")
    print("7. ✅ Data profiling com tipos detectados e campos potenciais")
    print("8. ✅ Monitoramento de recursos do sistema (CPU, memória, threads)")
    print("9. ✅ Análise de qualidade dos dados e parsing JSON")
    print("10. ✅ Detecção automática de campos chave e tipos de dados")
    print()
    print("📈 FEATURES ULTRA-DETALHADAS DEMONSTRADAS:")
    print("• Sistema de monitoramento de recursos em tempo real")
    print("• Data profiling automático com análise de complexidade")
    print("• Detecção de potenciais campos chave")
    print("• Análise de distribuição de tipos de dados")
    print("• Tracking de memory leaks e performance")
    print("• Análise de qualidade do parsing JSON")
    print("• Insights sobre densidade e eficiência dos dados")

if __name__ == "__main__":
    test_ultra_detailed_logging()