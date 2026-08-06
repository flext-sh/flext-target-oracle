# Triagem Snyk Code (SAST) — flext-sh/flext-target-oracle

Gerado do scan Snyk (dump 2026-08-06). Bead: `mro-26ga`

## Resumo

**2 achados** — critical 0, high 0, medium 0, low 2

| categoria | achados |
|---|---|
| Use of Hardcoded Passwords | 2 |

## Como usar este documento

Cada achado traz o **código real** extraído da worktree (linha `>>>` = sink reportado), a regra completa e o CWE.
Preencha **Decisão**: `corrigir` / `falso-positivo` (registrar em `.snyk`) / `risco-aceito` (com prazo).

## Achados

### 1 · ⚪ LOW · Use of Hardcoded Passwords
**Local**: `tests/conftest.py:89` · **CWE**: -

```python
       85              "host": os.environ["TEST_ORACLE_HOST"],
       86              "port": int(os.environ["TEST_ORACLE_PORT"]),
       87              "service_name": os.environ["TEST_ORACLE_SERVICE"],
       88              "username": "system",
>>>    89              "password": "flext_oracle_test",
       90          }
       91      })
       92      oracle_settings = FlextDbOracleSettings.model_validate({
       93          "DbOracle": {
```

**Decisão**: 

### 2 · ⚪ LOW · Use of Hardcoded Passwords
**Local**: `tests/integration/test_oracle.py:476` · **CWE**: -

```python
      472              "record": {
      473                  "id": 1,
      474                  "name": "John Doe",
      475                  "email": "john@example.com",
>>>   476                  "password": "secret123",
      477                  "internal_id": "INT-001",
      478              },
      479          }
      480          record_msg_value: t.JsonValue = t.json_value_adapter().validate_python(
```

**Decisão**: 

