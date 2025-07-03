#!/usr/bin/env python3
"""
Examples of Oracle Target configurations for different use cases.
Demonstrates generic vs WMS-specific schema conventions.
"""


def generic_config():
    """Generic Oracle configuration - works for any application."""
    return {
        "host": "oracle-server.company.com",
        "port": 1521,
        "service_name": "PRODDB",
        "username": "app_user",
        "password": "secure_password",
        "protocol": "tcp",
        # Generic schema settings
        "schema_naming_convention": "generic",
        "enable_smart_typing": True,
        "varchar_default_length": 255,
        "varchar_max_length": 4000,
        # Standard Oracle features
        "oracle_is_enterprise_edition": False,
        "use_merge_statements": True,
        "batch_size": 10000,
    }


def wms_config():
    """WMS-specific Oracle configuration - follows WMS conventions."""
    return {
        "host": "wms-oracle.company.com",
        "port": 1522,
        "service_name": "WMS_PROD",
        "username": "wms_user",
        "password": "wms_secure_password",
        "protocol": "tcps",
        # WMS schema settings
        "schema_naming_convention": "wms",
        "enable_smart_typing": True,
        "varchar_default_length": 255,
        "varchar_max_length": 255,  # WMS uses consistent 255
        # WMS Oracle features
        "oracle_is_enterprise_edition": True,
        "oracle_has_partitioning_option": True,
        "use_merge_statements": True,
        "parallel_degree": 4,
        "batch_size": 5000,
    }


def custom_config():
    """Custom configuration with specific type rules."""
    return {
        "host": "custom-oracle.company.com",
        "port": 1521,
        "service_name": "CUSTOM_DB",
        "username": "custom_user",
        "password": "custom_password",
        "protocol": "tcp",
        # Custom schema settings
        "schema_naming_convention": "custom",
        "enable_smart_typing": False,  # Disable automatic rules
        "varchar_default_length": 500,  # Larger default
        "varchar_max_length": 2000,
        # Custom type rules (example - not implemented yet)
        "custom_type_rules": {
            "patterns": {
                "*_code": {"type": "VARCHAR2", "length": 50},
                "*_status": {"type": "VARCHAR2", "length": 20},
                "*_flag": {"type": "CHAR", "length": 1},
                "*_amount": {"type": "NUMBER", "precision": 15, "scale": 2},
            }
        },
    }


def demonstrate_configurations():
    """Demonstrate different configuration approaches."""
    print("🔧 Oracle Target Configuration Examples")
    print("=" * 60)

    configs = {
        "Generic": generic_config(),
        "WMS": wms_config(),
        "Custom": custom_config(),
    }

    for name, config in configs.items():
        print(f"\n📋 {name} Configuration:")
        print("-" * 30)

        # Show key schema settings
        schema_settings = {
            "schema_naming_convention": config.get("schema_naming_convention"),
            "enable_smart_typing": config.get("enable_smart_typing"),
            "varchar_default_length": config.get("varchar_default_length"),
            "varchar_max_length": config.get("varchar_max_length"),
        }

        for key, value in schema_settings.items():
            print(f"  {key}: {value}")

    print("\n" + "=" * 60)
    print("🎯 Type Mapping Examples")
    print("=" * 60)

    # Examples of how different configurations handle the same field
    examples = [
        ("customer_id", "integer"),
        ("order_key", "string"),
        ("is_active_flg", "boolean"),
        ("total_amount", "number"),
        ("description", "string"),
        ("created_ts", "string with date-time format"),
    ]

    print(f"\n{'Field':<15} {'Type':<20} {'Generic':<15} {'WMS':<15} {'Custom':<15}")
    print("-" * 80)

    # Show expected mappings (simplified)
    mappings = {
        "customer_id": {"generic": "NUMBER", "wms": "NUMBER", "custom": "NUMBER(38,0)"},
        "order_key": {
            "generic": "VARCHAR2(100)",
            "wms": "VARCHAR2(255)",
            "custom": "VARCHAR2(500)",
        },
        "is_active_flg": {
            "generic": "NUMBER(1,0)",
            "wms": "CHAR(1)",
            "custom": "NUMBER(1,0)",
        },
        "total_amount": {
            "generic": "NUMBER",
            "wms": "NUMBER",
            "custom": "NUMBER(15,2)",
        },
        "description": {
            "generic": "VARCHAR2(500)",
            "wms": "VARCHAR2(255)",
            "custom": "VARCHAR2(500)",
        },
        "created_ts": {
            "generic": "TIMESTAMP(6)",
            "wms": "TIMESTAMP(6)",
            "custom": "TIMESTAMP(6)",
        },
    }

    for field, _ in examples:
        if field in mappings:
            m = mappings[field]
            print(
                f"{field:<15} {_:<20} {m['generic']:<15} "
                f"{m['wms']:<15} {m['custom']:<15}"
            )


if __name__ == "__main__":
    demonstrate_configurations()
