# flext-target-oracle - FLEXT Singer Ecosystem

**Hierarchy**: PROJECT
**Parent**: [../CLAUDE.md](../CLAUDE.md) - Workspace standards
**Last Update**: 2025-12-07

---

## Project Overview

**FLEXT-Target-Oracle** is the Singer target for Oracle Database loading in the FLEXT ecosystem.

**Version**: 0.9.0  
**Status**: Production-ready  
**Python**: 3.13+

**CRITICAL INTEGRATION DEPENDENCIES**:
- **flext-meltano**: MANDATORY for ALL Singer operations (ZERO TOLERANCE for direct singer-sdk without flext-meltano)
- **flext-db-oracle**: MANDATORY for ALL Oracle operations (ZERO TOLERANCE for direct SQLAlchemy/oracledb imports)
- **flext-core**: Foundation patterns (FlextResult, FlextService, FlextContainer)

---

## Essential Commands

```bash
# Setup and validation
make setup                    # Complete development environment setup
make validate                 # Complete validation (lint + type + security + test)
make check                    # Quick check (lint + type)

# Quality gates
make lint                     # Ruff linting
make type-check               # Pyrefly type checking
make security                 # Bandit security scan
make test                     # Run tests
```

---

## Key Patterns

### Singer Target Implementation

```python
from flext_core import FlextResult
from flext_target_oracle import FlextTargetOracle

target = FlextTargetOracle()

# Process records
result = target.write_record(record)
if result.is_success:
    print("Record written to Oracle")
```

---

## Critical Development Rules

### ZERO TOLERANCE Policies

**ABSOLUTELY FORBIDDEN**:
- ❌ Direct singer-sdk imports (use flext-meltano)
- ❌ Direct SQLAlchemy/oracledb imports (use flext-db-oracle)
- ❌ Exception-based error handling (use FlextResult)
- ❌ Type ignores or `Any` types

**MANDATORY**:
- ✅ Use `FlextResult[T]` for all operations
- ✅ Use flext-meltano for Singer operations
- ✅ Use flext-db-oracle for Oracle operations
- ✅ Complete type annotations
- ✅ Zero Ruff violations

---

**See Also**:
- [Workspace Standards](../CLAUDE.md)
- [flext-core Patterns](../flext-core/CLAUDE.md)
- [flext-db-oracle Patterns](../flext-db-oracle/CLAUDE.md)
- [flext-meltano Patterns](../flext-meltano/CLAUDE.md)
