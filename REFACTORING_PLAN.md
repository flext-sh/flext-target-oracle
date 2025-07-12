# REFACTORING PLAN - ELIMINAÇÃO DE DUPLICAÇÕES

## 🚨 PROBLEMA IDENTIFICADO: MÚLTIPLAS IMPLEMENTAÇÕES

### DUPLICAÇÕES CRÍTICAS:

1. **CONFIGURAÇÃO DUPLICADA:**
   - ✅ MANTER: `domain/models.py:TargetConfig` (FLEXT DDD padrão)
   - ❌ ELIMINAR: `config.py:TargetOracleConfig` (complexo demais, duplicação)

2. **CONEXÃO DUPLICADA:**
   - ✅ MANTER: `application/services.py` usando `flext-db-oracle`
   - ❌ ELIMINAR: `connector.py:OracleConnector` (duplica flext-db-oracle)

3. **SINK DUPLICADO:**
   - ✅ MANTER: `application/services.py:OracleLoaderService` (FLEXT padrão)
   - ❌ ELIMINAR: `sink.py:OracleSink` (duplica funcionalidade)

4. **COMPATIBILIDADE:**
   - ✅ MANTER: `target.py:OracleTarget` (interface Singer padrão)
   - ✅ MANTER: `sinks.py`, `connectors.py` (alias para compatibilidade)

## AÇÕES DE REFATORAÇÃO:

### FASE 1: Eliminar config.py
- Remover `config.py` completamente
- Usar apenas `domain/models.py:TargetConfig`

### FASE 2: Eliminar connector.py
- Remover `connector.py` 
- Usar apenas flext-db-oracle via services.py

### FASE 3: Eliminar sink.py
- Remover `sink.py`
- Usar apenas `application/services.py`

### FASE 4: Manter compatibilidade
- Manter `target.py` como interface principal
- Manter aliases em `sinks.py` e `connectors.py`

## RESULTADO:
- ✅ Zero duplicação de código
- ✅ Padrão FLEXT consistente
- ✅ Funcionalidade preservada
- ✅ Compatibilidade mantida