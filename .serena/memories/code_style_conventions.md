# Code Style and Conventions

## Python Standards

- **Python Version**: 3.13+ (strict requirement)
- **Type Hints**: Mandatory for all functions, classes, and variables
- **MyPy**: Strict mode enabled with zero tolerance for errors
- **Pydantic**: v2+ for data validation and models
- **Docstrings**: Google style with comprehensive documentation

## FLEXT Patterns (Mandatory)

- **FlextResult Railway Pattern**: All business operations must return FlextResult[T]
- **FlextModels.Value**: Use for configuration and data models
- **flext-core Logging**: Use FlextLogger() for structured logging
- **Dependency Injection**: Use get_flext_container() for service registration
- **Error Handling**: Explicit FlextResult patterns, NO try/except fallbacks
- **Domain Services**: Inherit from FlextDomainService for business logic

## Code Organization

- **Single Class Per Module**: One unified class per module with nested helpers
- **Clean Architecture**: Foundation → Domain → Application → Infrastructure layers
- **Import Strategy**: Root-level imports only (from flext_core import X)
- **No Wrappers**: Use flext-core directly, no compatibility layers
- **No Any Types**: Explicit type annotations required, no type: ignore

## Naming Conventions

- **Classes**: PascalCase (FlextTargetOracle, FlextTargetOracleConfig)
- **Functions**: snake_case (validate_oracle_configuration)
- **Constants**: UPPER_SNAKE_CASE (DEFAULT_TIMEOUT)
- **Private Methods**: Leading underscore (\_validate_data)
- **Modules**: snake_case (target_config.py, target_loader.py)

## Quality Standards

- **Test Coverage**: 90%+ minimum requirement
- **Linting**: Ruff with zero tolerance for violations
- **Type Safety**: MyPy strict mode with zero errors
- **Security**: No SQL injection vulnerabilities, parameterized queries only
- **Documentation**: 100% docstring coverage for public APIs
