# Triagem Snyk Code (SAST) — flext-sh/flext-target-oracle

Gerado do scan Snyk da org Datacosmos (dump 2026-08-06).

**2 achados** — critical 0, high 0, medium 0, low 2

| categoria | achados |
|---|---|
| Use of Hardcoded Passwords | 2 |

## Achados

Coluna **Decisão**: `corrigir` / `falso-positivo` / `risco-aceito`.

| # | sev | categoria | arquivo | linha | CWE | Decisão |
|---|---|---|---|---|---|---|
| 1 | low | Use of Hardcoded Passwords | `tests/conftest.py` | 89 | - | |
| 2 | low | Use of Hardcoded Passwords | `tests/integration/test_oracle.py` | 476 | - | |

## Como triar

1. Abrir `arquivo:linha` e seguir o fluxo de dados até o sink.
2. Classificar: **corrigir** (entrada externa alcança o sink sem sanitização), **falso-positivo** (credencial de fixture, path de constante — registrar em `.snyk` com justificativa), **risco-aceito** (com prazo de revisão).

Dados brutos: `~/snyk-violations/sast/flext-sh__flext-target-oracle.sast.json`

