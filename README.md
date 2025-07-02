# flext-target-oracle

Singer Target for Oracle Database - FLEXT ETL Framework

## Overview

A Singer-compliant target for loading data into Oracle databases, designed for the FLEXT ecosystem.

## Features

- Singer protocol compliance
- Oracle database connectivity
- Batch loading capabilities
- Schema management
- Error handling and retry logic

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Load data from stdin
cat data.jsonl | flext-target-oracle --config config.json

# Load data from Singer tap
tap-some-source | flext-target-oracle --config config.json
```

## Configuration

```json
{
  "host": "localhost",
  "port": 1521,
  "database": "XE",
  "user": "username",
  "password": "password",
  "default_target_schema": "target_schema"
}
```

## Development

This target is part of the FLEXT framework and follows Singer specification standards.

## License

MIT License