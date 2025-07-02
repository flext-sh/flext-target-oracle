#!/usr/bin/env python3
"""
Validação final completa do projeto após correções e limpeza.
"""

import sys
import traceback
from flext_target_oracle import OracleTarget, OracleSink, OracleConnector


def test_project_final_validation():
    """Validação final completa do projeto."""
    print("🏆 VALIDAÇÃO FINAL COMPLETA DO PROJETO")
    print("=" * 60)
    
    results = []
    
    # Test 1: Import dos módulos principais
    try:
        print("1. Testando imports principais...")
        from flext_target_oracle import __version__
        assert __version__ == "1.0.0"
        print(f"✅ Imports funcionando - versão {__version__}")
        results.append(("Imports principais", True, f"Versão {__version__}"))
    except Exception as e:
        print(f"❌ Imports falharam: {e}")
        results.append(("Imports principais", False, str(e)))
    
    # Test 2: Ausência de arquivos V2 
    try:
        print("2. Verificando remoção de arquivos V2...")
        try:
            from flext_target_oracle.target_v2 import OracleTargetV2
            print("❌ Arquivo V2 ainda existe!")
            results.append(("Limpeza V2", False, "target_v2.py ainda importável"))
        except ImportError:
            print("✅ Arquivos V2 removidos com sucesso")
            results.append(("Limpeza V2", True, "Over-engineering removido"))
    except Exception as e:
        print(f"❌ Teste limpeza V2 falhou: {e}")
        results.append(("Limpeza V2", False, str(e)))
    
    # Test 3: Funcionalidade básica
    try:
        print("3. Testando funcionalidade básica...")
        config = {
            "host": "localhost",
            "username": "test", 
            "password": "test",
            "database": "XE"
        }
        
        # Connector
        connector = OracleConnector(config)
        print("   ✅ OracleConnector - OK")
        
        # Target
        target = OracleTarget(config=config, validate_config=False)
        print("   ✅ OracleTarget - OK")
        
        print("✅ Funcionalidade básica preservada")
        results.append(("Funcionalidade básica", True, "Todos os componentes funcionando"))
    except Exception as e:
        print(f"❌ Funcionalidade básica falhou: {e}")
        results.append(("Funcionalidade básica", False, str(e)))
    
    # Test 4: Correções de error handling implementadas
    try:
        print("4. Verificando correções de error handling...")
        
        # Verificar que connectors.py tem categorização
        with open("flext_target_oracle/connectors.py", "r") as f:
            content = f.read()
            if "Categorize Oracle optimization errors" in content and "except Exception: pass" not in content:
                print("   ✅ connectors.py - Error categorization implementada")
            else:
                raise Exception("connectors.py ainda tem mascaramento")
        
        # Verificar que sinks.py tem logging
        with open("flext_target_oracle/sinks.py", "r") as f:
            content = f.read()
            if "Monitor engine setup failed (will retry later)" in content:
                print("   ✅ sinks.py - Warning logging implementado")
            else:
                raise Exception("sinks.py ainda tem mascaramento")
        
        print("✅ Correções de error handling validadas")
        results.append(("Error handling", True, "Mascaramento removido, categorização implementada"))
    except Exception as e:
        print(f"❌ Correções error handling falharam: {e}")
        results.append(("Error handling", False, str(e)))
    
    # Test 5: Estrutura de arquivos final
    try:
        print("5. Verificando estrutura final de arquivos...")
        import os
        expected_files = [
            "flext_target_oracle/__init__.py",
            "flext_target_oracle/target.py", 
            "flext_target_oracle/sinks.py",
            "flext_target_oracle/connectors.py",
            "flext_target_oracle/config_validator.py",
            "flext_target_oracle/logging_config.py",
            "flext_target_oracle/monitoring.py"
        ]
        
        missing_files = []
        for file_path in expected_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            raise Exception(f"Arquivos obrigatórios ausentes: {missing_files}")
        
        # Verificar que V2 não existem
        v2_files = ["flext_target_oracle/target_v2.py", "flext_target_oracle/sinks_v2.py"]
        existing_v2 = [f for f in v2_files if os.path.exists(f)]
        
        if existing_v2:
            raise Exception(f"Arquivos V2 ainda existem: {existing_v2}")
        
        print("✅ Estrutura de arquivos correta")
        results.append(("Estrutura arquivos", True, "Arquivos principais presentes, V2 removidos"))
    except Exception as e:
        print(f"❌ Estrutura arquivos incorreta: {e}")
        results.append(("Estrutura arquivos", False, str(e)))
    
    # Summary
    print("\n🎯 RESULTADO FINAL DA VALIDAÇÃO:")
    print("=" * 60)
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for test_name, passed_test, details in results:
        status = "✅" if passed_test else "❌"
        print(f"{status} {test_name}: {details}")
    
    print(f"\n📊 SCORE FINAL:")
    print(f"✅ Passaram: {passed}/{total}")
    print(f"❌ Falharam: {total - passed}/{total}")
    print(f"📈 Taxa de Sucesso: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🏆 PROJETO VALIDADO COM SUCESSO!")
        print("✨ Mascaramento de erros corrigido")
        print("✨ Over-engineering removido") 
        print("✨ Funcionalidade preservada")
        return True
    else:
        print("\n💥 VALIDAÇÃO FALHOU!")
        return False

if __name__ == "__main__":
    success = test_project_final_validation()
    sys.exit(0 if success else 1)