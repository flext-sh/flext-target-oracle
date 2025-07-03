#!/usr/bin/env python3
"""
Script integrado de verificação de qualidade do código.
Executa todos os checks necessários e falha no primeiro erro encontrado.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> None:
    """Executa um comando e aborta se houver erro."""
    print(f"🔍 {description}...")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        if result.returncode != 0:
            print(f"❌ ERRO: {description}")
            print(f"STDOUT:\n{result.stdout}")
            print(f"STDERR:\n{result.stderr}")
            sys.exit(1)
        else:
            print(f"✅ {description} - OK")
            if result.stdout.strip():
                print(f"   {result.stdout.strip()}")
                
    except Exception as e:
        print(f"❌ ERRO CRÍTICO ao executar {description}: {e}")
        sys.exit(1)


def main():
    """Execução principal dos checks."""
    print("🚀 INICIANDO VERIFICAÇÃO COMPLETA DE QUALIDADE")
    
    # 1. Verificação MyPy - tipos estáticos
    run_command(
        ["mypy", "flext_target_oracle/", "--show-error-codes"],
        "Verificação de tipos (MyPy)"
    )
    
    # 2. Verificação Ruff - linting e formatação
    run_command(
        ["ruff", "check", "flext_target_oracle/"],
        "Verificação de linting (Ruff)"
    )
    
    # 3. Verificação de importações circulares
    run_command(
        ["python", "-m", "flext_target_oracle.target", "--help"],
        "Verificação de importações (target funcional)"
    )
    
    print("\n🎉 TODAS AS VERIFICAÇÕES PASSARAM!")
    print("✅ Código está 100% conforme aos padrões de qualidade")


if __name__ == "__main__":
    main()