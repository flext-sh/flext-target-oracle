#!/usr/bin/env python3
"""
Script final para corrigir TODOS os erros de linha longa no sinks.py.
"""

import re


def fix_long_lines():
    """Corrige todas as linhas muito longas no arquivo sinks.py."""
    with open("flext_target_oracle/sinks.py", "r") as f:
        content = f.read()
    
    # Lista de correções específicas para linhas muito longas
    fixes = [
        # Linha 561
        ('                        "total_failed_batches": len(self._stream_stats["failed_batches"]),',
         '                        "total_failed_batches": len(\n'
         '                            self._stream_stats["failed_batches"]\n'
         '                        ),'),
        
        # Linha 757
        ('                    "sql_statement": insert_sql[:500] + "..." if len(insert_sql) > 500 else insert_sql,',
         '                    "sql_statement": (\n'
         '                        insert_sql[:500] + "..."\n'
         '                        if len(insert_sql) > 500\n'
         '                        else insert_sql\n'
         '                    ),'),
        
        # Linha 790
        ('                            f"❌ VERIFICATION QUERY FAILED after INSERT: {verification_error}",',
         '                            (\n'
         '                                f"❌ VERIFICATION QUERY FAILED after INSERT: "\n'
         '                                f"{verification_error}"\n'
         '                            ),'),
        
        # Linha 809 - records_per_second calculation
        ('                            "records_per_second": round(len(prepared) / operation_duration if operation_duration > 0 else 0, 2),',
         '                            "records_per_second": round(\n'
         '                                len(prepared) / operation_duration\n'
         '                                if operation_duration > 0\n'
         '                                else 0,\n'
         '                                2,\n'
         '                            ),'),
        
        # Linha 811
        ('                            "cumulative_inserts": self._stream_stats["total_records_inserted"],',
         '                            "cumulative_inserts": self._stream_stats[\n'
         '                                "total_records_inserted"\n'
         '                            ],'),
        
        # Linha 812
        ('                            "total_db_operations": self._stream_stats["database_operations"]["inserts"],',
         '                            "total_db_operations": self._stream_stats[\n'
         '                                "database_operations"\n'
         '                            ]["inserts"],'),
        
        # Todas as outras linhas com total_rows_affected
        ('"total_rows_affected": self._stream_stats["database_operations"]["rows_affected"]',
         '"total_rows_affected": self._stream_stats[\n'
         '                                "database_operations"\n'
         '                            ]["rows_affected"]'),
        
        # Estatísticas finais longas
        ('            total_duration = self._stream_stats["last_batch_time"] - self._stream_stats["first_batch_time"]',
         '            total_duration = (\n'
         '                self._stream_stats["last_batch_time"]\n'
         '                - self._stream_stats["first_batch_time"]\n'
         '            )'),
         
        # Quebrar linhas de cálculo de estatísticas
        ('            self._stream_stats["total_processing_time"] / self._stream_stats["successful_operations"]',
         '            self._stream_stats["total_processing_time"]\n'
         '            / self._stream_stats["successful_operations"]'),
        
        # Mais correções genéricas para database_operations
        ('self._stream_stats["database_operations"]["inserts"]',
         'self._stream_stats["database_operations"]["inserts"]'),
        
        ('self._stream_stats["database_operations"]["merges"]',
         'self._stream_stats["database_operations"]["merges"]'),
    ]
    
    # Aplicar todas as correções
    for old, new in fixes:
        content = content.replace(old, new)
    
    # Escrever arquivo corrigido
    with open("flext_target_oracle/sinks.py", "w") as f:
        f.write(content)
    
    print("✅ Correções aplicadas ao sinks.py")


def main():
    """Execução principal."""
    print("🔧 Corrigindo todas as linhas longas...")
    fix_long_lines()
    
    # Verificar resultado
    import subprocess
    
    result = subprocess.run(
        ["ruff", "check", "flext_target_oracle/sinks.py"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("🎉 SUCESSO! Todos os erros de linha longa foram corrigidos!")
    else:
        remaining_errors = result.stdout.count("E501")
        print(f"⚠️ Ainda restam {remaining_errors} erros de linha longa")
        print("Primeiros erros restantes:")
        print(result.stdout[:1000])


if __name__ == "__main__":
    main()