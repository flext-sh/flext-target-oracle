# Oracle Target API Reference

## Table of Contents

- [OracleTarget](#oracletarget)
- [OracleConnector](#oracleconnector)
- [OracleSink](#oraclesink)
- [Configuration Options](#configuration-options)
- [Type Mappings](#type-mappings)

## OracleTarget

Main Singer target class for Oracle databases.

### Class Definition

```python
class OracleTarget(Target):
    """Target for Oracle databases using SQLAlchemy 2.0."""
```

### Properties

#### name
```python
name: str = "target-oracle"
```
The canonical name of the target.

#### config_jsonschema
```python
config_jsonschema: dict
```
JSON schema for configuration validation.

#### default_sink_class
```python
default_sink_class: Type[OracleSink]
```
Default sink class for streams.

### Methods

#### __init__
```python
def __init__(self, config: dict | None = None, **kwargs) -> None
```
Initialize the Oracle target.

**Parameters:**
- `config`: Configuration dictionary
- `**kwargs`: Additional keyword arguments passed to parent

#### _initialize_engines
```python
def _initialize_engines(self) -> None
```
Initialize both sync and async SQLAlchemy engines.

**Internal method** for engine setup.

#### _build_connection_url
```python
def _build_connection_url(self) -> str
```
Build Oracle connection URL from configuration.

**Returns:** Connection URL string

#### _check_engine_health
```python
def _check_engine_health(self) -> dict[str, Any]
```
Check health of database engines.

**Returns:** Dictionary with health status

## OracleConnector

Database connector using SQLAlchemy 2.0.

### Class Definition

```python
class OracleConnector(SQLConnector):
    """Oracle database connector with SQLAlchemy 2.0."""
```

### Methods

#### get_sqlalchemy_url
```python
def get_sqlalchemy_url(self, config: dict[str, Any]) -> URL
```
Construct SQLAlchemy URL using URL.create().

**Parameters:**
- `config`: Configuration dictionary

**Returns:** SQLAlchemy URL object

**Example:**
```python
url = connector.get_sqlalchemy_url({
    "host": "localhost",
    "user": "scott",
    "password": "tiger",
    "service_name": "ORCL"
})
```

#### create_engine
```python
def create_engine(self) -> Engine
```
Create SQLAlchemy engine with Oracle optimizations.

**Returns:** Configured SQLAlchemy engine

#### to_sql_type
```python
def to_sql_type(self, schema: dict[str, Any]) -> TypeEngine
```
Convert JSON Schema type to Oracle SQL type.

**Parameters:**
- `schema`: JSON Schema type definition

**Returns:** SQLAlchemy TypeEngine

**Example:**
```python
# Integer type
sql_type = connector.to_sql_type({"type": "integer"})
# Returns: NUMBER(38, 0)

# String with length
sql_type = connector.to_sql_type({"type": "string", "maxLength": 100})
# Returns: VARCHAR2(100)
```

#### get_column_type
```python
def get_column_type(self, column_name: str, schema: dict[str, Any]) -> TypeEngine
```
Get Oracle type for column with pattern recognition.

**Parameters:**
- `column_name`: Name of the column
- `schema`: JSON Schema definition

**Returns:** Optimized Oracle type

#### _get_pool_class
```python
def _get_pool_class(self) -> Type[Pool]
```
Select appropriate connection pool class.

**Returns:** SQLAlchemy pool class

## OracleSink

High-performance data sink for Oracle.

### Class Definition

```python
class OracleSink(SQLSink[OracleConnector]):
    """Oracle sink with bulk operations and parallelism."""
```

### Properties

#### connector_class
```python
connector_class = OracleConnector
```
Connector class to use.

#### full_table_name
```python
@property
def full_table_name(self) -> str
```
Get fully qualified table name with schema.

### Methods

#### __init__
```python
def __init__(
    self,
    target: Target,
    stream_name: str,
    schema: dict[str, Any],
    key_properties: list[str] | None = None,
) -> None
```
Initialize Oracle sink.

**Parameters:**
- `target`: Parent target instance
- `stream_name`: Name of the stream
- `schema`: JSON Schema for the stream
- `key_properties`: Primary key columns

#### process_batch
```python
def process_batch(self, context: dict[str, Any]) -> None
```
Process a batch of records.

**Parameters:**
- `context`: Batch context with records

**Example:**
```python
sink.process_batch({
    "records": [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ]
})
```

#### _prepare_records
```python
def _prepare_records(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]
```
Prepare records for database insertion.

**Parameters:**
- `records`: Raw records from stream

**Returns:** Prepared records with audit fields

#### clean_up
```python
def clean_up(self) -> None
```
Clean up resources after processing.

## Configuration Options

### Connection Settings

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `host` | string | Yes | - | Oracle server hostname |
| `port` | integer | No | 1521 | Oracle server port |
| `user` / `username` | string | Yes | - | Database username |
| `password` | string | Yes | - | Database password |
| `service_name` | string | Yes* | - | Oracle service name |
| `sid` | string | Yes* | - | Oracle SID (alternative to service_name) |
| `dsn` | string | No | - | Full connection string |

*Either `service_name` or `sid` is required

### Performance Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `batch_size_rows` | integer | 10000 | Records per batch |
| `parallel_threads` | integer | 1 | Number of parallel threads |
| `pool_size` | integer | 10 | Connection pool size |
| `pool_recycle` | integer | 3600 | Pool connection lifetime (seconds) |
| `pool_timeout` | integer | 30 | Pool timeout (seconds) |
| `use_direct_path` | boolean | False | Enable direct path loading |
| `enable_parallel_dml` | boolean | False | Enable parallel DML |

### Table Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `default_target_schema` | string | None | Default schema for tables |
| `table_prefix` | string | None | Prefix for all table names |
| `load_method` | string | "append-only" | Load method: append-only, upsert, overwrite |
| `add_record_metadata` | boolean | True | Add audit fields |

### Advanced Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enable_column_patterns` | boolean | True | Enable intelligent type mapping |
| `echo` | boolean | False | Log SQL statements |
| `optimizer_mode` | string | None | Oracle optimizer mode |
| `alter_session` | list | [] | Session parameters to set |

## Type Mappings

### JSON Schema to Oracle

| JSON Schema Type | Oracle Type | Notes |
|-----------------|-------------|-------|
| `integer` | NUMBER(38,0) | Full precision integer |
| `number` | NUMBER | Floating point |
| `boolean` | NUMBER(1,0) | 0 or 1 |
| `string` | VARCHAR2(n) | n from maxLength |
| `string` (>4000) | CLOB | Large text |
| `string` + date-time | TIMESTAMP WITH TIME ZONE | ISO 8601 dates |
| `array` | CLOB | JSON serialized |
| `object` | CLOB | JSON serialized |

### Column Pattern Recognition

When `enable_column_patterns` is true:

| Pattern | Oracle Type | Example Columns |
|---------|-------------|-----------------|
| `*_ID` | NUMBER(38,0) | USER_ID, ORDER_ID |
| `*_FLG` | NUMBER(1,0) | ACTIVE_FLG, DELETED_FLG |
| `*_FLAG` | NUMBER(1,0) | IS_ACTIVE_FLAG |
| `*_TS` | TIMESTAMP WITH TIME ZONE | CREATE_TS, UPDATE_TS |
| `*_DATE` | DATE | BIRTH_DATE, ORDER_DATE |
| `*_TIME` | TIMESTAMP | START_TIME, END_TIME |
| `*_AMOUNT` | NUMBER(19,4) | TOTAL_AMOUNT, TAX_AMOUNT |
| `*_QTY` | NUMBER(19,4) | ORDER_QTY, STOCK_QTY |
| `*_QUANTITY` | NUMBER(19,4) | ITEM_QUANTITY |
| `*_PCT` | NUMBER(5,2) | DISCOUNT_PCT |
| `*_PERCENT` | NUMBER(5,2) | TAX_PERCENT |
| `*_PERCENTAGE` | NUMBER(5,2) | COMPLETION_PERCENTAGE |

## Examples

### Basic Usage

```python
from flext_target_oracle import OracleTarget

# Initialize target
target = OracleTarget({
    "host": "oracle.example.com",
    "user": "etl_user",
    "password": "secure_password",
    "service_name": "PROD",
    "default_target_schema": "DW"
})

# Process Singer messages
target.listen(file_input=sys.stdin)
```

### Custom Configuration

```python
config = {
    # Connection
    "host": "oracle.example.com",
    "port": 1521,
    "user": "etl_user",
    "password": "secure_password",
    "service_name": "PROD",
    
    # Performance
    "batch_size_rows": 50000,
    "parallel_threads": 8,
    "pool_size": 20,
    "use_direct_path": True,
    
    # Table settings
    "default_target_schema": "DW",
    "table_prefix": "SINGER_",
    "load_method": "upsert",
    
    # Advanced
    "enable_parallel_dml": True,
    "alter_session": [
        "ALTER SESSION SET NLS_DATE_FORMAT='YYYY-MM-DD HH24:MI:SS'"
    ]
}

target = OracleTarget(config)
```

### Error Handling

```python
try:
    target = OracleTarget(config)
    target.listen(file_input=sys.stdin)
except Exception as e:
    logger.error(f"Target failed: {e}")
    sys.exit(1)
```