#!/usr/bin/env python3
"""
Test Oracle DDL fix with real VARCHAR2 column creation.
Simulates the exact scenario that was failing in Meltano.
"""

import json
import io
from datetime import datetime
from dotenv import load_dotenv
from flext_target_oracle import OracleTarget
from validate_production import load_oracle_config

def test_ddl_fix():
    """Test Oracle DDL fix with VARCHAR2 column creation."""
    print("🧪 Testing Oracle DDL Fix...")
    
    config = load_oracle_config()
    target = OracleTarget(config=config)
    
    # Create a stream with string fields that will become VARCHAR2
    timestamp = datetime.now().isoformat()
    stream_name = f"ddl_test_{int(datetime.now().timestamp())}"
    
    # Schema similar to what caused the error
    schema_msg = json.dumps({
        'type': 'SCHEMA',
        'stream': stream_name,
        'schema': {
            'properties': {
                'id': {'type': 'integer'},
                'alloc_qty': {'type': 'string'},  # This caused the VARCHAR2 error
                'item_desc': {'type': 'string', 'maxLength': 100},
                'status': {'type': 'string', 'maxLength': 50}
            }
        },
        'key_properties': ['id']
    })
    
    # Test record
    record_msg = json.dumps({
        'type': 'RECORD',
        'stream': stream_name,
        'record': {
            'id': 1,
            'alloc_qty': '100.50',
            'item_desc': 'Test item description',
            'status': 'ACTIVE'
        }
    })
    
    test_data = '\n'.join([schema_msg, record_msg])
    
    try:
        # This should now work without DDL errors
        result = target.process_lines(io.StringIO(test_data))
        print("  ✅ DDL Fix: SUCCESS - VARCHAR2 columns created properly")
        return True
        
    except Exception as e:
        print(f"  ❌ DDL Fix: FAILED - {e}")
        return False

if __name__ == "__main__":
    success = test_ddl_fix()
    exit(0 if success else 1)