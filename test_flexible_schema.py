#!/usr/bin/env python3
"""
Test flexible schema conventions: Generic vs WMS vs Custom.
"""

import io
import json
from datetime import datetime

from sqlalchemy import create_engine, text

from flext_target_oracle import OracleTarget
from validate_production import load_oracle_config


def test_schema_conventions():
    """Test different schema conventions."""
    print("🧪 Testing Flexible Schema Conventions...")

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

    conventions = {
        'generic': {
            'schema_naming_convention': 'generic',
            'enable_smart_typing': True,
            'varchar_default_length': 255
        },
        'wms': {
            'schema_naming_convention': 'wms',
            'enable_smart_typing': True,
            'varchar_default_length': 255
        },
        'custom': {
            'schema_naming_convention': 'custom',
            'enable_smart_typing': False,
            'varchar_default_length': 500
        }
    }

    results = {}

    for convention_name, convention_config in conventions.items():
        print(f"\n📋 Testing {convention_name.upper()} Convention...")

        # Merge base config with convention config
        config = {**base_config, **convention_config}
        target = OracleTarget(config=config)

        timestamp = datetime.now().isoformat()
        stream_name = f"test_{convention_name}_{int(datetime.now().timestamp())}"

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
            # Process with this convention
            result = target.process_lines(io.StringIO(test_data))
            print(f"  ✅ {convention_name.upper()}: Table created successfully")

            # Analyze the table structure
            table_structure = analyze_table_structure(stream_name.upper(), base_config)
            results[convention_name] = table_structure

        except Exception as e:
            print(f"  ❌ {convention_name.upper()}: Failed - {e}")

    # Compare results
    print("\n" + "="*80)
    print("📊 Schema Convention Comparison")
    print("="*80)

    if results:
        compare_schema_results(results)

    return len(results) > 0

def analyze_table_structure(table_name, config):
    """Analyze table structure and return type mappings."""
    password = str(config['password']).strip('"')
    dsn = f"(DESCRIPTION=(ADDRESS=(PROTOCOL=TCPS)(HOST={config['host']})(PORT={config['port']}))(CONNECT_DATA=(SERVICE_NAME={config['service_name']})))"

    connect_args = {
        'user': config['username'],
        'password': password,
        'dsn': dsn,
        'ssl_server_dn_match': False,
    }

    engine = create_engine('oracle+oracledb://@', connect_args=connect_args)

    structure = {}

    with engine.connect() as conn:
        columns_query = text(f"""
            SELECT 
                column_name,
                data_type,
                data_length,
                data_precision,
                data_scale
            FROM user_tab_columns 
            WHERE table_name = '{table_name}'
            AND column_name NOT LIKE '_SDC_%'
            AND column_name NOT LIKE '_LOADED_%'
            AND column_name NOT LIKE '_EXTRACTED_%'
            AND column_name NOT LIKE '_ENTITY_%'
            AND column_name NOT LIKE '_BATCH_%'
            ORDER BY column_id
        """)

        columns = conn.execute(columns_query).fetchall()

        for col in columns:
            col_name, data_type, length, precision, scale = col
            type_info = data_type

            if data_type == 'VARCHAR2':
                type_info = f"VARCHAR2({length})"
            elif data_type == 'CHAR':
                type_info = f"CHAR({length})"
            elif data_type == 'NUMBER':
                if precision and scale:
                    type_info = f"NUMBER({precision},{scale})"
                elif precision:
                    type_info = f"NUMBER({precision})"
                else:
                    type_info = "NUMBER"
            elif data_type == 'TIMESTAMP':
                type_info = "TIMESTAMP(6)"

            structure[col_name.lower()] = type_info

    return structure

def compare_schema_results(results):
    """Compare schema results across conventions."""
    # Get all field names
    all_fields = set()
    for structure in results.values():
        all_fields.update(structure.keys())

    sorted_fields = sorted(all_fields)

    # Print comparison table
    print(f"\n{'Field':<15} {'Generic':<20} {'WMS':<20} {'Custom':<20}")
    print("-" * 80)

    for field in sorted_fields:
        generic_type = results.get('generic', {}).get(field, 'N/A')
        wms_type = results.get('wms', {}).get(field, 'N/A')
        custom_type = results.get('custom', {}).get(field, 'N/A')

        print(f"{field:<15} {generic_type:<20} {wms_type:<20} {custom_type:<20}")

    print("\n🎯 Key Differences:")
    differences = []

    # Check for specific differences
    if 'is_active_flg' in sorted_fields:
        generic_flg = results.get('generic', {}).get('is_active_flg', '')
        wms_flg = results.get('wms', {}).get('is_active_flg', '')

        if 'CHAR(1)' in wms_flg and 'NUMBER' in generic_flg:
            differences.append("✓ WMS uses CHAR(1) for _FLG fields (vs NUMBER for generic)")

    # Check VARCHAR2 sizes
    for field in ['order_key', 'description', 'status_code']:
        if field in sorted_fields:
            generic_type = results.get('generic', {}).get(field, '')
            wms_type = results.get('wms', {}).get(field, '')
            custom_type = results.get('custom', {}).get(field, '')

            if generic_type != wms_type:
                differences.append(f"✓ Different VARCHAR2 sizes for {field}: Generic({generic_type}) vs WMS({wms_type})")

    if differences:
        for diff in differences:
            print(f"  {diff}")
    else:
        print("  No significant differences detected in this test")

if __name__ == "__main__":
    success = test_schema_conventions()
    exit(0 if success else 1)
