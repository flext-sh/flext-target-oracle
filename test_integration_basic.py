#!/usr/bin/env python3
"""
Teste básico de integração para verificar se as modificações quebraram
funcionalidade essencial.
"""

import sys
import traceback

from flext_target_oracle.target import OracleTarget


def test_basic_initialization() -> None:
    """Testa inicialização básica sem config."""
    try:
        print("Testing basic initialization...")
        OracleTarget(config={}, validate_config=False)
        print("✅ Basic initialization successful")
        return True
    except Exception as e:
        print(f"❌ Basic initialization FAILED: {e}")
        traceback.print_exc()
        return False


def test_initialization_with_minimal_config() -> None:
    """Testa inicialização com config mínima."""
    try:
        print("Testing initialization with minimal config...")
        config = {
            "host": "localhost",
            "port": 1521,
            "username": "test",
            "password": "test",
            "database": "XE",
        }
        OracleTarget(config=config)
        print("✅ Minimal config initialization successful")
        return True
    except Exception as e:
        print(f"❌ Minimal config initialization FAILED: {e}")
        traceback.print_exc()
        return False


def test_initialization_with_none_config() -> None:
    """Testa inicialização com config None."""
    try:
        print("Testing initialization with None config...")
        OracleTarget(config=None, validate_config=False)
        print("✅ None config initialization successful")
        return True
    except Exception as e:
        print(f"❌ None config initialization FAILED: {e}")
        traceback.print_exc()
        return False


def main():
    """Execute todos os testes básicos."""
    print("🧪 EXECUTANDO TESTES DE INTEGRAÇÃO BÁSICA")
    print("=" * 50)

    results = []
    results.append(test_basic_initialization())
    results.append(test_initialization_with_minimal_config())
    results.append(test_initialization_with_none_config())

    print("\n📊 RESULTADOS:")
    print("=" * 50)
    passed = sum(results)
    total = len(results)

    print(f"✅ Passaram: {passed}/{total}")
    print(f"❌ Falharam: {total - passed}/{total}")

    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print("💥 ALGUNS TESTES FALHARAM!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
