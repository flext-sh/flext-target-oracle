# Contributing to FLEXT Target Oracle

Thank you for your interest in contributing to FLEXT Target Oracle! This document provides guidelines and instructions for contributing to the project.

## 🏗️ Development Setup

### Prerequisites

- Python 3.13+
- Docker and Docker Compose (for Oracle database)
- Poetry for dependency management
- Git

### Setting Up Your Development Environment

1. **Clone the repository:**

   ```bash
   git clone https://github.com/flext-sh/flext-target-oracle.git
   cd flext-target-oracle
   ```

2. **Install dependencies:**

   ```bash
   make dev-setup
   # or
   poetry install --all-extras
   pip install -r requirements-test.txt
   ```

3. **Start Oracle container:**

   ```bash
   make oracle-start
   ```

4. **Run tests to verify setup:**

   ```bash
   make test-unit  # Unit tests (no Docker required)
   make test       # All tests (requires Oracle)
   ```

## 🧪 Testing

### Test Structure

```
tests/
├── unit/         # Fast unit tests with mocked dependencies
├── integration/  # Tests with real Oracle database
├── e2e/         # End-to-end workflow tests
└── performance/ # Performance benchmarks
```

### Running Tests

```bash
# All tests
make test

# Specific test categories
make test-unit        # Unit tests only
make test-integration # Integration tests
make test-e2e        # End-to-end tests

# With coverage
make coverage

# Run specific test
pytest tests/unit/test_loader.py::TestOracleLoaderConnection::test_connect_success -v
```

### Writing Tests

1. **Unit Tests**: Mock all external dependencies

   ```python
   @pytest.mark.unit
   def test_feature(mock_oracle_api):
       # Test isolated functionality
   ```

2. **Integration Tests**: Use real Oracle database

   ```python
   @pytest.mark.integration
   @pytest.mark.oracle
   async def test_database_operation(oracle_loader, oracle_engine):
       # Test with real database
   ```

3. **Use fixtures** from `conftest.py` for common test data and setup

## 📝 Code Style

### Standards

- **Type Hints**: All code must be fully typed
- **Docstrings**: Google-style docstrings for all public APIs
- **Formatting**: Black + Ruff (configured in `pyproject.toml`)
- **Imports**: Organized with isort

### Automated Checks

```bash
# Format code
make format

# Run linters
make lint

# Type checking
make type-check

# All quality checks
make check
```

### Pre-commit Hooks

Install pre-commit hooks to run checks automatically:

```bash
pre-commit install
```

## 🏛️ Architecture

### Key Components

1. **Target Class** (`src/flext_target_oracle/target.py`):

   - Main Singer target implementation
   - Implements `FlextSingerUnifiedInterface`
   - Handles message routing and state management

2. **Loader Class** (`src/flext_target_oracle/loader.py`):

   - Core data loading logic
   - DDL/DML operations via `flext-db-oracle`
   - Schema flattening and type mapping

3. **Configuration** (`src/flext_target_oracle/config.py`):

   - Pydantic models for configuration
   - Validation and defaults
   - Feature flags and customization

4. **Exceptions** (`src/flext_target_oracle/exceptions.py`):
   - Custom exception hierarchy
   - Specific error scenarios

### Design Principles

1. **Railway-Oriented Programming**: Use `FlextResult` for error handling
2. **Dependency Injection**: Configuration-driven behavior
3. **Clean Architecture**: Separation of concerns
4. **Type Safety**: Strict typing throughout

## 🚀 Adding Features

### 1. Configuration Options

Add new fields to `FlextOracleTargetConfig`:

```python
class FlextOracleTargetConfig(BaseModel):
    my_new_option: bool = Field(
        default=False,
        description="Enable my new feature",
    )
```

### 2. New Functionality

1. Add logic to appropriate module
2. Add tests (unit + integration)
3. Update documentation
4. Add example if applicable

### 3. Database Features

For new DDL/DML operations:

1. Implement in `flext-db-oracle` first
2. Use via `FlextDbOracleApi` in loader
3. Never generate SQL directly in target

## 📚 Documentation

### Required Documentation

1. **Docstrings**: All public methods and classes
2. **Type hints**: Complete type annotations
3. **Examples**: For new features
4. **Tests**: Demonstrating usage

### Documentation Style

```python
def process_record(
    self,
    stream_name: str,
    record: Dict[str, Any],
    schema: Dict[str, Any],
) -> FlextResult[None]:
    """Process a single record for insertion.

    Args:
        stream_name: Name of the Singer stream
        record: Record data to process
        schema: Singer schema for validation

    Returns:
        FlextResult indicating success/failure

    Raises:
        FlextOracleTargetProcessingError: If processing fails
    """
```

## 🐛 Debugging

### Debug Mode

Set environment variables:

```bash
export FLEXT_DEBUG=true
export FLEXT_LOG_LEVEL=DEBUG
```

### Common Issues

1. **Import Errors**: Ensure all FLEXT dependencies are installed
2. **Oracle Connection**: Check Docker container is running
3. **Type Errors**: Run `mypy` to catch type issues

## 📦 Submitting Changes

### 1. Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation
- `refactor/description` - Code refactoring

### 2. Commit Messages

Follow conventional commits:

```
feat: add bulk merge support
fix: handle NULL values in JSON columns
docs: update configuration examples
test: add performance benchmarks
```

### 3. Pull Request Process

1. **Create PR** with clear description
2. **Ensure CI passes** (all tests, linting)
3. **Update documentation** if needed
4. **Add tests** for new functionality
5. **Request review** from maintainers

### 4. PR Checklist

- [ ] Tests pass locally (`make test`)
- [ ] Code is formatted (`make format`)
- [ ] Type checking passes (`make type-check`)
- [ ] Documentation updated
- [ ] Changelog entry added (if applicable)

## 🤝 Community

### Getting Help

- Open an issue for bugs or features
- Check existing issues first
- Provide minimal reproducible examples

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to FLEXT Target Oracle! 🎯🐘
