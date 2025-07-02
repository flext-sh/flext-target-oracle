#!/usr/bin/env python3
"""Simple test to verify the Oracle target works with Python 3.9+"""

import sys

from flext_target_oracle import OracleTarget, __version__

print(f"FLEXT Target Oracle version: {__version__}")
print(f"Python version: {sys.version}")

# Test configuration validation
config = {
    "host": "localhost",
    "port": 1521,
    "service_name": "XEPDB1",
    "username": "test_user",
    "password": "test_password",
}

# Create target instance
target = OracleTarget(config=config)
print(f"Target created: {target.name}")

# Show capabilities
print("\nAll configuration parameters:")
schema = target.config_jsonschema
print(f"Total parameters: {len(schema['properties'])}")

# List some key parameters
key_params = [
    "host", "port", "service_name", "batch_config", "pool_size",
    "use_bulk_operations", "use_merge_statements", "parallel_degree",
    "enable_compression", "load_method"
]

print("\nKey configuration parameters:")
for param in key_params:
    if param in schema['properties']:
        prop = schema['properties'][param]
        print(f"  - {param}: {prop.get('description', 'No description')}")

print("\nTarget is ready to use!")
print("Usage: tap-source | flext-target-oracle --config config.json")
