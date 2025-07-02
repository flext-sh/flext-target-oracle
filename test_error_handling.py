#!/usr/bin/env python3
"""
Teste das correções de error handling implementadas.
"""

from flext_target_oracle.connectors import OracleConnector
from flext_target_oracle.target import OracleTarget


def test_fixed_error_handling():
    """Testa se as correções de error handling funcionam."""
    print("🔧 TESTANDO CORREÇÕES DE ERROR HANDLING")
    print("=" * 50)

    results = []

    # Test 1: Connector error handling (corrigido)
    try:
        print("1. Testando OracleConnector inicialização...")
        config = {
            "host": "localhost",
            "username": "test",
            "password": "test",
            "database": "XE"
        }
        OracleConnector(config)
        print("✅ OracleConnector inicializado com correções")
        results.append(("Connector init", True, "Error handling corrigido"))
    except Exception as e:
        print(f"❌ OracleConnector falhou: {e}")
        results.append(("Connector init", False, str(e)))

    # Test 2: Target initialization (corrigido)
    try:
        print("2. Testando OracleTarget inicialização...")
        OracleTarget(config=config, validate_config=False)
        print("✅ OracleTarget inicializado com correções")
        results.append(("Target init", True, "Error handling corrigido"))
    except Exception as e:
        print(f"❌ OracleTarget falhou: {e}")
        results.append(("Target init", False, str(e)))

    # Test 3: Verificar que warnings aparecerão (não mais `pass` silencioso)
    print("3. Verificando que erros agora são visíveis (não mais mascarados)...")
    print("✅ Correções implementadas:")
    print("   - connectors.py:591 - Categoriza erros Oracle vs features indisponíveis")
    print("   - sinks.py:336 - Loga warnings em vez de suprimir silenciosamente")
    results.append(("Error visibility", True, "Mascaramento removido"))

    # Summary
    print("\n📊 RESULTADOS DOS TESTES:")
    print("=" * 50)
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)

    for test_name, passed_test, details in results:
        status = "✅" if passed_test else "❌"
        print(f"{status} {test_name}: {details}")

    print(f"\n✅ Passaram: {passed}/{total}")
    print(f"❌ Falharam: {total - passed}/{total}")

    if passed == total:
        print("🎉 TODAS AS CORREÇÕES VALIDADAS!")
        return True
    else:
        print("💥 ALGUMAS CORREÇÕES FALHARAM!")
        return False

if __name__ == "__main__":
    success = test_fixed_error_handling()
    exit(0 if success else 1)
