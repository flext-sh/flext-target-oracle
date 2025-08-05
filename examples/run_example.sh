#!/bin/bash

# Example script to demonstrate flext-target-oracle usage

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🎯 FLEXT Target Oracle - Example Usage${NC}"
echo -e "${BLUE}=====================================${NC}"

# Check if Oracle is running
echo -e "${YELLOW}Checking Oracle container...${NC}"
if ! docker ps | grep -q "flext-oracle-test"; then
	echo -e "${YELLOW}Starting Oracle container...${NC}"
	cd .. && make oracle-start && cd examples
fi

# Create example config
echo -e "${BLUE}Creating example configuration...${NC}"
cat >config.json <<EOF
{
    "oracle_host": "localhost",
    "oracle_port": 1521,
    "oracle_service": "XE",
    "oracle_user": "FLEXT_TEST",
    "oracle_password": "test_password",
    "default_target_schema": "FLEXT_TEST",
    "batch_size": 1000,
    "load_method": "bulk_insert",
    "sdc_mode": "merge",
    "storage_mode": "flattened",
    "column_ordering": "alphabetical",
    "create_foreign_key_indexes": true,
    "custom_indexes": {
        "users": [
            {"name": "IDX_USERS_EMAIL", "columns": ["EMAIL"], "unique": true}
        ]
    }
}
EOF

# Create example Singer data
echo -e "${BLUE}Creating example Singer data...${NC}"
cat >singer_data.jsonl <<EOF
{"type": "SCHEMA", "stream": "users", "schema": {"type": "object", "properties": {"id": {"type": "integer"}, "name": {"type": "string"}, "email": {"type": "string", "format": "email"}, "age": {"type": "integer"}, "address": {"type": "object", "properties": {"street": {"type": "string"}, "city": {"type": "string"}, "country": {"type": "string"}}}, "created_at": {"type": "string", "format": "date-time"}}}, "key_properties": ["id"]}
{"type": "RECORD", "stream": "users", "record": {"id": 1, "name": "John Doe", "email": "john@example.com", "age": 30, "address": {"street": "123 Main St", "city": "New York", "country": "USA"}, "created_at": "2025-01-20T12:00:00Z"}}
{"type": "RECORD", "stream": "users", "record": {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "age": 25, "address": {"street": "456 Oak Ave", "city": "Los Angeles", "country": "USA"}, "created_at": "2025-01-20T12:01:00Z"}}
{"type": "RECORD", "stream": "users", "record": {"id": 3, "name": "Bob Johnson", "email": "bob@example.com", "age": 35, "address": {"street": "789 Pine Rd", "city": "Chicago", "country": "USA"}, "created_at": "2025-01-20T12:02:00Z"}}
{"type": "SCHEMA", "stream": "products", "schema": {"type": "object", "properties": {"id": {"type": "integer"}, "name": {"type": "string"}, "price": {"type": "number"}, "category": {"type": "string"}, "in_stock": {"type": "boolean"}}}, "key_properties": ["id"]}
{"type": "RECORD", "stream": "products", "record": {"id": 1, "name": "Laptop", "price": 999.99, "category": "Electronics", "in_stock": true}}
{"type": "RECORD", "stream": "products", "record": {"id": 2, "name": "Mouse", "price": 29.99, "category": "Electronics", "in_stock": true}}
{"type": "RECORD", "stream": "products", "record": {"id": 3, "name": "Keyboard", "price": 79.99, "category": "Electronics", "in_stock": false}}
{"type": "STATE", "value": {"bookmarks": {"users": {"replication_key": "created_at", "replication_key_value": "2025-01-20T12:02:00Z"}, "products": {"version": 1}}}}
EOF

# Run the target
echo -e "${BLUE}Running flext-target-oracle...${NC}"
python example_usage.py

# Show results
echo -e "${GREEN}✅ Example completed successfully!${NC}"
echo -e "${BLUE}Check the Oracle database for the loaded data:${NC}"
echo "  - Table: USERS (with flattened address columns)"
echo "  - Table: PRODUCTS"
echo "  - Custom index on USERS.EMAIL"

# Cleanup
echo -e "${YELLOW}Cleaning up example files...${NC}"
rm -f config.json singer_data.jsonl

echo -e "${GREEN}Done!${NC}"
