#!/usr/bin/env python3
"""
DEEP SCAN - Procurar padrões silenciosos mais sutis.

Este teste procura por padrões que podem estar mascarando erros de forma mais sutil.
"""

import os
import re
import glob
from typing import List, Dict, Any

def analyze_exception_handler(file_path: str, line_num: int, lines: List[str]) -> Dict[str, Any]:
    """Analisar um exception handler específico para padrões problemáticos."""
    analysis = {
        "file": file_path,
        "line": line_num,
        "suspicious": False,
        "reasons": [],
        "code": "",
        "severity": "low"
    }
    
    # Extrair o bloco completo do exception handler
    except_line = lines[line_num - 1].strip()
    analysis["code"] = except_line
    
    # Procurar por linhas após o except
    handler_lines = []
    for i in range(line_num, min(line_num + 10, len(lines))):
        line = lines[i].strip()
        if line and not line.startswith('#'):
            handler_lines.append(line)
            # Parar se encontrar outro try/except/def/class
            if any(keyword in line for keyword in ['def ', 'class ', 'try:', 'except', 'finally:']):
                if i > line_num:  # Não parar na própria linha except
                    break
    
    handler_code = '\n'.join(handler_lines)
    
    # Padrões suspeitos mais sutis
    
    # 1. Exception handlers que apenas fazem return sem logging
    if re.search(r'except.*:\s*return', handler_code):
        if not any(keyword in handler_code for keyword in ['print', 'log', 'error', 'warning', 'debug']):
            analysis["suspicious"] = True
            analysis["reasons"].append("Returns without logging")
            analysis["severity"] = "high"
    
    # 2. Exception handlers que fazem assignments silenciosos
    if re.search(r'except.*:\s*[a-zA-Z_]\w*\s*=', handler_code):
        if not any(keyword in handler_code for keyword in ['print', 'log', 'error', 'warning']):
            analysis["suspicious"] = True
            analysis["reasons"].append("Silent assignment in exception handler")
            analysis["severity"] = "medium"
    
    # 3. Exception handlers que apenas incrementam contadores
    if re.search(r'except.*:\s*\w+\s*\+=\s*1', handler_code):
        if not any(keyword in handler_code for keyword in ['print', 'log', 'error', 'warning']):
            analysis["suspicious"] = True
            analysis["reasons"].append("Silent counter increment")
            analysis["severity"] = "medium"
    
    # 4. Exception handlers que fazem append sem logging
    if re.search(r'except.*:\s*\w+\.append\(', handler_code):
        if not any(keyword in handler_code for keyword in ['print', 'log', 'error', 'warning']):
            analysis["suspicious"] = True
            analysis["reasons"].append("Silent append operation")
            analysis["severity"] = "medium"
    
    # 5. Exception handlers que fazem close/cleanup sem logging erro
    if any(word in handler_code for word in ['close()', 'cleanup()', 'dispose()']):
        if not any(keyword in handler_code for keyword in ['print', 'log', 'error', 'warning']):
            analysis["suspicious"] = True
            analysis["reasons"].append("Silent cleanup without error logging")
            analysis["severity"] = "low"
    
    # 6. Exception handlers muito pequenos (só 1-2 linhas) sem log
    if len(handler_lines) <= 2:
        if not any(keyword in handler_code for keyword in ['print', 'log', 'error', 'warning', 'raise', 'pass']):
            analysis["suspicious"] = True
            analysis["reasons"].append("Very short handler without logging")
            analysis["severity"] = "medium"
    
    # 7. Exception handlers com comentários genéricos
    if re.search(r'#.*ignore|#.*skip|#.*continue|#.*ok', handler_code, re.IGNORECASE):
        if not any(keyword in handler_code for keyword in ['print', 'log', 'error', 'warning']):
            analysis["suspicious"] = True
            analysis["reasons"].append("Generic ignore comment without logging")
            analysis["severity"] = "medium"
    
    return analysis

def deep_scan_file(file_path: str) -> List[Dict[str, Any]]:
    """Fazer scan profundo de um arquivo para padrões sutis."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"⚠️ Could not read {file_path}: {e}")
        return []
    
    issues = []
    
    for line_num, line in enumerate(lines, 1):
        # Procurar por linhas except
        if re.search(r'except.*:', line.strip()):
            analysis = analyze_exception_handler(file_path, line_num, lines)
            if analysis["suspicious"]:
                issues.append(analysis)
    
    return issues

def main():
    print("🔍 DEEP SCAN - Procurando padrões silenciosos sutis")
    print("=" * 70)
    
    # Arquivos para escanear
    file_patterns = [
        "flext_target_oracle/*.py",
        "tests/*.py"
    ]
    
    all_issues = []
    files_scanned = 0
    
    for pattern in file_patterns:
        files = glob.glob(pattern)
        for file_path in files:
            # Pular nossos próprios arquivos de teste
            if file_path.endswith(('test_deep_silent_scan.py', 'test_zero_silent_errors_FINAL.py')):
                continue
                
            files_scanned += 1
            issues = deep_scan_file(file_path)
            all_issues.extend(issues)
            
            if issues:
                print(f"🔍 {file_path}: {len(issues)} padrões suspeitos")
            else:
                print(f"✅ {file_path}: limpo")
    
    print(f"\n📊 DEEP SCAN COMPLETO:")
    print(f"   Arquivos escaneados: {files_scanned}")
    print(f"   Padrões suspeitos encontrados: {len(all_issues)}")
    
    if all_issues:
        print(f"\n🔍 PADRÕES SUSPEITOS ENCONTRADOS:")
        print("=" * 70)
        
        # Agrupar por severidade
        by_severity = {"high": [], "medium": [], "low": []}
        for issue in all_issues:
            by_severity[issue["severity"]].append(issue)
        
        for severity in ["high", "medium", "low"]:
            issues_of_severity = by_severity[severity]
            if issues_of_severity:
                print(f"\n🚨 SEVERIDADE {severity.upper()} ({len(issues_of_severity)} issues):")
                for issue in issues_of_severity:
                    print(f"📁 {issue['file']}:{issue['line']}")
                    print(f"   Razões: {', '.join(issue['reasons'])}")
                    print(f"   Código: {issue['code']}")
                    print()
        
        return False
    else:
        print(f"\n🎉 EXCELENTE! Nenhum padrão suspeito encontrado!")
        print("✅ Código está limpo de padrões sutis de mascaramento")
        return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)