"""
Example usage of FLEXT Target Oracle.

This example shows how to use the target programmatically.
Compatible with Python 3.9+
"""

from __future__ import annotations

import json
import sys

from flext_target_oracle import OracleTarget


def main():
    """Example usage of Oracle target."""

    # Configuration
    config = {
        "host": "localhost",
        "port": 1521,
        "service_name": "XEPDB1",
        "username": "target_user",
        "password": "secure_password",
        "schema": "TARGET_SCHEMA",

        # Performance settings
        "batch_config": {
            "batch_size": 10000,
        },
        "pool_size": 10,
        "use_bulk_operations": True,
        "parallel_degree": 2,

        # Load method
        "load_method": "upsert",  # or "append-only", "overwrite"

        # Oracle optimizations
        "enable_compression": True,
        "compression_type": "basic",
        "create_table_indexes": True,
    }

    # Create target
    _target = OracleTarget(config=config)

    # Example: Process Singer messages from stdin
    # In real usage, this would come from a tap
    example_messages = [
        # Schema message
        {
            "type": "SCHEMA",
            "stream": "users",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string", "maxLength": 100},
                    "email": {"type": "string", "maxLength": 255},
                    "active": {"type": "boolean"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "metadata": {"type": "object"},
                }
            },
            "key_properties": ["id"]
        },
        # Record messages
        {
            "type": "RECORD",
            "stream": "users",
            "record": {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "active": True,
                "created_at": "2025-07-02T10:00:00Z",
                "metadata": {"source": "web"}
            }
        },
        {
            "type": "RECORD",
            "stream": "users",
            "record": {
                "id": 2,
                "name": "Jane Smith",
                "email": "jane@example.com",
                "active": True,
                "created_at": "2025-07-02T11:00:00Z",
                "metadata": {"source": "api"}
            }
        }
    ]

    # Process messages
    for message in example_messages:
        print(json.dumps(message))
        sys.stdout.flush()

    # In real usage:
    # tap-postgres --config tap_config.json | \
    #   flext-target-oracle --config target_config.json


if __name__ == "__main__":
    main()
