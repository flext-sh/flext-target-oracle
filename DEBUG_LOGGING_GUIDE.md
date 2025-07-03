# 🔍 Oracle Target - Guia de Logging ULTRA-DETALHADO para Debug de Inserções

## 📋 Visão Geral

O Oracle Target agora possui **logging ULTRA-DETALHADO consolidado** para rastrear todos os dados que chegam e identificar problemas de inserção no banco Oracle. Todo o logging é **consolidado em uma única saída abrangente** para facilitar análise.

## 🎯 Configuração para Debug

### Configurações Recomendadas

```json
{
  "host": "your-oracle-host",
  "username": "your-username", 
  "password": "your-password",
  "database": "your-database",
  
  // CONFIGURAÇÕES DE DEBUG
  "log_level": "INFO",
  "log_format": "text",
  "log_batch_details": true,
  "log_sql_statements": true,
  "echo": true,
  "echo_pool": false
}
```

## 📊 Log Consolidado Ultra-Detalhado

### 🎯 **Saída Única Abrangente**
```
🎯 ORACLE TARGET - COMPREHENSIVE INPUT ANALYSIS & PROCESSING START
```

**Inclui todas as seguintes seções em uma única entrada de log:**

#### **=== INPUT ANALYSIS ===**
- Tipo de entrada e tamanho total
- Análise de linhas vazias e formato
- Estatísticas de tamanho de entrada

#### **=== SINGER MESSAGE BREAKDOWN ===**
- Contagem de mensagens SCHEMA/RECORD/STATE
- Streams únicos detectados
- Análise de validade de protocolo Singer

#### **=== DATA QUALITY ANALYSIS ===**
- Taxa de sucesso de parsing JSON
- Densidade de dados (HIGH/MEDIUM/LOW)
- Falhas de parsing e qualidade geral

#### **=== SIZE & PERFORMANCE ANALYSIS ===**
- Tamanhos médios de mensagens
- Ratios de eficiência de processamento
- Análise de performance de entrada

#### **=== SYSTEM MONITORING ===**
- CPU, memória, threads em tempo real
- Timestamp de processamento
- Estágio atual de processamento

#### **=== SAMPLE DATA PREVIEW ===**
- Primeiras linhas de exemplo
- Distribuição de tipos de mensagem
- Preview de estrutura de dados

## 🚨 **Detecção Automática de Erros Críticos**

O sistema agora detecta e **aborta automaticamente** com erros apropriados:

### ❌ **Entrada Vazia**
```
❌ CRITICAL ERROR: No input data received - Target cannot process empty input
```

### ❌ **Formato Inválido**  
```
❌ CRITICAL ERROR: No valid Singer messages found in input - Input format appears invalid
```

### ❌ **Sem Records**
```
❌ CRITICAL ERROR: No RECORD messages found - No data available for processing
```

### ❌ **Qualidade de Dados Ruim**
```
❌ CRITICAL ERROR: High JSON parse failure rate (XX.X%) - Input data quality issues
```

## 🚨 Diagnóstico de Problemas

### Problema: "NO VALID RECORD MESSAGES FOUND"

**Significado:** Target não encontrou mensagens RECORD válidas

**Verificações:**
1. ✅ Formato Singer correto?
2. ✅ Mensagens estão chegando ao target?
3. ✅ Tap está gerando records válidos?

### Problema: Sink criado mas sem batch processing

**Significado:** Schema processado mas records não chegaram aos batches

**Verificações:**  
1. ✅ Records têm stream name correto?
2. ✅ Singer SDK está fazendo batching?
3. ✅ Configuração de batch_size adequada?

### Problema: SQL execution failed

**Significado:** Erro na execução do SQL no Oracle

**Verificações:**
1. ✅ Conectividade com Oracle ok?
2. ✅ Permissões de DDL/DML?
3. ✅ Schema de tabela compatível?
4. ✅ Tipos de dados corretos?

## 🔧 Exemplo de Uso

### Comando de Debug
```bash
# Habilitar logging máximo
your-tap | flext-target-oracle --config config.json 2>&1 | tee debug.log

# Filtrar apenas logs relevantes
your-tap | flext-target-oracle --config config.json 2>&1 | grep -E "(🔍|📊|📝|🏗️|📦|💾|✅|❌)"
```

### Script de Teste
```python
# Use o test_logging_inserts.py para testar localmente
python test_logging_inserts.py
```

## 📈 Métricas de Performance

Os logs também incluem métricas úteis:

- **Batch sizes**: Quantos records por batch
- **Processing time**: Tempo de processamento
- **SQL execution time**: Tempo de execução SQL
- **Records processed**: Total processado
- **Rows affected**: Linhas afetadas no Oracle

## 🎯 Próximos Passos

1. **Execute com configuração de debug**
2. **Analise os logs gerados**
3. **Identifique onde o processo para**
4. **Verifique configuração específica da etapa problemática**

## 📞 Troubleshooting Rápido

| Log Esperado | Não Aparece | Possível Causa |
|-------------|-------------|----------------|
| 🔍 RECEIVED INPUT | ❌ | Target não inicializou |
| 📊 MESSAGE ANALYSIS | ❌ | Input vazio ou formato inválido |
| 📝 SAMPLE RECORDS | ❌ | Nenhum RECORD message válido |
| 🏗️ CREATING SINK | ❌ | Erro no schema processing |
| 📦 PROCESSING BATCH | ❌ | Records não chegaram ao sink |
| 💾 EXECUTING INSERT | ❌ | Erro de conectividade Oracle |
| ✅ INSERT SUCCESSFUL | ❌ | Erro de SQL/permissões |

---

**Com este logging detalhado, você conseguirá identificar exatamente onde os dados param de fluir para o Oracle!** 🎯