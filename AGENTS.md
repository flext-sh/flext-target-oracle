# AGENTS.md — flext-target-oracle

> **Parent workspace law** lives in [`../AGENTS.md`](../AGENTS.md) — read it first.
> Universal engineering core: `~/.agents/UNIVERSAL_CORE.md`. Composition: global skills + parent/root `AGENTS.md` + this scope delta. Do not re-embed universal law.
>
> **Standalone / independent mode:** when `../AGENTS.md` does not resolve, pin the parent raw `AGENTS.md` URL to the same branch/release as this package (never `main`).

<!-- AIHUB-AGENTS-SCOPE-LOCAL-BEGIN -->
**Package:** `flext_target_oracle` · deps: `flext-cli`, `flext-core`, `flext-db-oracle`, `flext-meltano`

## Overview

Singer **target** (loader) for Oracle Database. Thin driver over `flext-meltano` (ADR-006), delegating loading to `flext-db-oracle`. This is the connector's **CQRS variant**.

## Structure

```text
src/flext_target_oracle/
├── api.py            # FlextTargetOracleService(FlextMeltanoTargetServiceBase) — create_sink() raises (loader pattern, not Singer sink)
├── cli.py
├── _models/commands.py   # CQRS command DTOs — PURE DATA (no execute())
├── constants.py typings.py protocols.py models.py utilities.py   # AUTO-GENERATED facets
└── _constants/ _protocols/ _typings/ _utilities/
```

## Code Map

| Symbol | Kind | Location | Role |
|--------|------|----------|------|
| `FlextTargetOracleService` | class | `api.py` | target service; uses a loader pattern (rejects `create_sink`) |
| command DTOs | models | `_models/commands.py` | pure-data CQRS commands |

## Conventions (specific to this package)

- **CQRS:** command `_models` are data-only DTOs; **execution belongs to services/handlers**, never `execute()` on a model.
- Uses a loader pattern, not a Singer sink — `create_sink` intentionally raises.
- Oracle settings namespaced (`settings.DbOracle.*`).

## Commands

```bash
make check PROJECT=flext-target-oracle
make test  PROJECT=flext-target-oracle       # tests/{unit,integration,e2e,performance}
```
<!-- AIHUB-AGENTS-SCOPE-LOCAL-END -->
