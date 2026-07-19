# AGENTS.md — flext-target-oracle

> **General FLEXT law & workspace conventions live in the root [`../AGENTS.md`](../AGENTS.md) — read it first.** SSOT for facade layering, config/settings, `make`-only workflow, testing law, git discipline. This file adds ONLY `flext-target-oracle`-specific knowledge.
>
> **Standalone / independent mode:** if this package is checked out on its own (imported as a dependency, vendored, or cloned solo) there is no parent workspace, so `../AGENTS.md` does not resolve. Then read the root law from the raw file on the SAME branch/release the project is on: <https://raw.githubusercontent.com/flext-sh/flext/0.12.0-dev/AGENTS.md> (pin the branch/tag to your working line, never `main`).

**Package:** `flext_target_oracle` · deps: `flext-cli`, `flext-core`, `flext-db-oracle`, `flext-meltano`

## Overview

Singer **target** (loader) for Oracle Database. Thin driver over `flext-meltano` (ADR-006), delegating loading to `flext-db-oracle`. This is the connector's **CQRS variant**.

## Structure

```
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
