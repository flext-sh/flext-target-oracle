# FLEXT-Target-Oracle

[![Singer SDK](https://img.shields.io/badge/singer--sdk-compliant-brightgreen.svg)](https://sdk.meltano.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**FLEXT-Target-Oracle** is a production-grade Singer target for loading data into Oracle Databases (11g through 23c). It is designed for high-performance enterprise data integration, supporting bulk loading, incremental updates, and schema evolution.

## 🚀 Key Features

- **Broad Version Support**: Tested compatibility from Oracle 11g to 23c.
- **High Performance**: Leverages bulk inserts, array DML, and direct path loading where possible.
- **Flexible Loading Strategies**: Configurable for INSERT, MERGE (UPSERT), and BULK operations.
- **Schema Evolution**: Automatically creates and alters tables to match incoming Singer schema messages.
- **FLEXT Integration**: Seamlessly works with `flext-core` patterns and `flext-meltano` orchestration.

## 📦 Installation

Install via Poetry:

```bash
poetry add flext-target-oracle
```

## 🛠️ Usage

### Using with Meltano

Add the target to your `meltano.yml` for orchestrated loading:

```yaml
loaders:
  - name: target-oracle
    namespace: flext_target_oracle
    pip_url: flext-target-oracle
    settings:
      - name: oracle_host
      - name: oracle_service
      - name: oracle_user
      - name: oracle_password
        kind: password
      - name: load_method
        value: "BULK_MERGE"
```

### CLI Execution

Pipe data directly into your Oracle warehouse:

```bash
tap-mysql | target-oracle --config oracle_config.json
```

### Configuration Options

Fine-tune your loading process:

```json
{
  "oracle_host": "db.example.com",
  "oracle_port": 1521,
  "oracle_service": "ORCL",
  "oracle_user": "LOADER_USER",
  "default_target_schema": "STAGING",
  "load_method": "BULK_insert",
  "batch_size": 5000,
  "connection_timeout": 60
}
```

## 🏗️ Architecture

Built on the Singer SDK, ensuring standard compliance:

- **Loader Engine**: Optimized for Oracle-specific SQL dialects and performance tuning.
- **Connection Pool**: Manages database connections efficiently for high-throughput scenarios.
- **Transaction Management**: Ensures data consistency with robust commit/rollback logic.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/development.md) for details on setting up a local Oracle test container.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
