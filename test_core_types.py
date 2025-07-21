#!/usr/bin/env python3
"""
Test core type mapping fixes based on user feedback.
"""

import io
import json
from datetime import datetime

from sqlalchemy import create_engine, text

from flext_target_oracle import OracleTarget
from validate_production import load_oracle_config


def test_core_type_mapping():
    """Test that core type mapping works according to user feedback."""
    print("🎯 Testing Core Type Mapping Fixes...")

    config = load_oracle_config()

    # Test schema focused on core user feedback
    test_schema = {
        'properties': {
            'test_integer': {'type': 'integer'},
            'test_number': {'type': 'number'},
            'test_datetime': {'type': 'string', 'format': 'date-time'},
            'test_string': {'type': 'string'}
        }
    }

    target = OracleTarget(config=config)

    timestamp = datetime.now().isoformat()
    stream_name = f"test_core_types_{int(datetime.now().timestamp())}"

    # Create schema and record messages
    schema_msg = json.dumps({
        'type': 'SCHEMA',
        'stream': stream_name,
        'schema': test_schema,
        'key_properties': ['test_integer']
    })

    record_msg = json.dumps({
        'type': 'RECORD',
        'stream': stream_name,
        'record': {
            'test_integer': 123,
            'test_number': 456.78,
            'test_datetime': timestamp,
            'test_string': 'Test string'
        }
    })

    test_data = '\n'.join([schema_msg, record_msg])

    try:
        # Process the data
        result = target.process_lines(io.StringIO(test_data))
        print(f"✅ Processing completed: {result}")

        # Check the actual database types
        print("\n📊 Checking actual Oracle types created...")
        check_oracle_types(stream_name.upper(), config)

        return True

    except Exception as e:
        print(f"❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_oracle_types(table_name, config):
    """Check the actual Oracle types created."""
    password = str(config['password']).strip('"')
    dsn = f"(DESCRIPTION=(ADDRESS=(PROTOCOL=TCPS)(HOST={config['host']})(PORT={config['port']}))(CONNECT_DATA=(SERVICE_NAME={config['service_name']})))"

    connect_args = {
        'user': config['username'],
        'password': password,
        'dsn': dsn,
        'ssl_server_dn_match': False,
    }

    engine = create_engine('oracle+oracledb://@', connect_args=connect_args)

    with engine.connect() as conn:
        columns = conn.execute(text(f"""
            SELECT
                column_name,
                data_type,
                data_length,
                data_precision,
                data_scale
            FROM user_tab_columns
            WHERE table_name = '{table_name}'
            AND column_name IN ('TEST_INTEGER', 'TEST_NUMBER', 'TEST_DATETIME', 'TEST_STRING')
            ORDER BY column_id
        """)).fetchall()

        print(f"\n{'Column':<15} {'Oracle Type':<25} {'User Expectation':<20} {'Status'}")
        print("-" * 75)

        for col in columns:
            col_name, data_type, length, precision, scale = col
            type_info = data_type

            if data_type == 'VARCHAR2':
                type_info = f"VARCHAR2({length})"
            elif data_type == 'NUMBER':
                if precision and scale is not None:
                    type_info = f"NUMBER({precision},{scale})"
                elif precision:
                    type_info = f"NUMBER({precision})"
                else:
                    type_info = "NUMBER"
            elif data_type.startswith('TIMESTAMP'):
                type_info = data_type

            # Determine expectation and status
            if col_name == 'TEST_INTEGER' or col_name == 'TEST_NUMBER':
                expected = "NUMBER"
                status = "✅" if type_info == "NUMBER" else "❌"
            elif col_name == 'TEST_DATETIME':
                expected = "TIMESTAMP(6)"
                status = "✅" if "TIMESTAMP(6)" in type_info else "❌"
            elif col_name == 'TEST_STRING':
                expected = "VARCHAR2(255)"
                status = "✅" if "VARCHAR2" in type_info else "❌"
            else:
                expected = "N/A"
                status = "?"

            print(f"{col_name:<15} {type_info:<25} {expected:<20} {status}")

if __name__ == "__main__":
    success = test_core_type_mapping()
    exit(0 if success else 1)
