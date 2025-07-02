#!/usr/bin/env python3
"""
Debug test to understand type mapping behavior.
"""

import io
import json
from datetime import datetime

from flext_target_oracle import OracleTarget
from validate_production import load_oracle_config


def test_debug_type_mapping():
    """Test type mapping with debug enabled."""
    print("🔍 Testing Type Mapping with Debug...")

    base_config = load_oracle_config()

    # Test schema with WMS-like field names
    test_schema = {
        'properties': {
            'id': {'type': 'integer'},
            'customer_id': {'type': 'integer'},
            'order_key': {'type': 'string'},
            'is_active_flg': {'type': 'boolean'},
            'total_amount': {'type': 'number'},
            'description': {'type': 'string'},
            'status_code': {'type': 'string'},
            'created_ts': {'type': 'string', 'format': 'date-time'}
        }
    }

    # Enable debug mode
    config = {
        **base_config,
        'schema_naming_convention': 'wms',
        'enable_smart_typing': True,
        'varchar_default_length': 255,
        'debug_type_mapping': True  # Enable debug logging
    }

    target = OracleTarget(config=config)

    timestamp = datetime.now().isoformat()
    stream_name = f"test_debug_{int(datetime.now().timestamp())}"

    # Create schema message
    schema_msg = json.dumps({
        'type': 'SCHEMA',
        'stream': stream_name,
        'schema': test_schema,
        'key_properties': ['id']
    })

    # Create test record
    record_msg = json.dumps({
        'type': 'RECORD',
        'stream': stream_name,
        'record': {
            'id': 1,
            'customer_id': 12345,
            'order_key': 'ORD-2023-001',
            'is_active_flg': True,
            'total_amount': 999.99,
            'description': 'Test order description',
            'status_code': 'ACTIVE',
            'created_ts': timestamp
        }
    })

    test_data = '\n'.join([schema_msg, record_msg])

    try:
        # Process with debug enabled
        print("\n🔧 Processing data with debug enabled...")
        result = target.process_lines(io.StringIO(test_data))
        print(f"✅ Processing completed: {result}")

        return True

    except Exception as e:
        print(f"❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_debug_type_mapping()
    exit(0 if success else 1)
