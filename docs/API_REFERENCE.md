# FLEXT Target Oracle API Reference

## FLEXT Architecture Components

This API implements FLEXT enterprise patterns for Singer protocol compliance:

- [SingerTargetService](#singertargetservice) - FLEXT application service pattern
- [OracleLoaderService](#oracleloaderservice) - flext-db-oracle integration
- [Domain Models](#domain-models) - flext-core DDD patterns
- [FLEXT Configuration](#flext-configuration) - Standard FLEXT config patterns

## SingerTargetService

FLEXT application service implementing Singer message processing with enterprise patterns.

### FLEXT Service Pattern Usage

```python
from flext_target_oracle.application.services import SingerTargetService
from flext_target_oracle.domain.models import TargetConfig
from flext_core import ServiceResult

# FLEXT configuration with validation
config = TargetConfig(
    oracle_config={"host": "localhost", "service_name": "XEPDB1"},
    default_target_schema="FLEXT_DW"
)

# Initialize service with FLEXT dependencies
service = SingerTargetService(config)

# Process Singer message with ServiceResult pattern
result: ServiceResult[None] = await service.process_singer_message({
    "type": "RECORD",
    "stream": "users", 
    "record": {"id": 1, "name": "Alice"}
})

# FLEXT error handling
if result.is_success:
    logger.info("Message processed successfully")
else:
    logger.error(f"Processing failed: {result.error}")
```

### Methods

#### process_singer_message

```python
async def process_singer_message(
    self, 
    message: dict[str, Any]
) -> ServiceResult[None]
```

Process RECORD, SCHEMA, or STATE messages according to Singer protocol.

#### finalize_all_streams

```python
async def finalize_all_streams(self) -> ServiceResult[LoadStatistics]
```

Flush all pending batches and return load statistics.

## OracleLoaderService

Oracle data loading service implementing flext-db-oracle patterns for enterprise performance.

### Methods

#### ensure_table_exists

```python
async def ensure_table_exists(
    self,
    stream_name: str,
    schema: SingerSchema
) -> ServiceResult[None]
```

Create table if it doesn't exist based on Singer schema.

#### load_record

```python
async def load_record(
    self,
    stream_name: str, 
    record_data: dict[str, Any]
) -> ServiceResult[None]
```

Buffer record for batch processing. Automatically flushes when batch size reached.

## FLEXT Domain Models

### TargetConfig (DomainValueObject)

FLEXT-compliant configuration using flext-core patterns.

```python
class TargetConfig(DomainValueObject):
    """Target configuration following FLEXT domain modeling."""
    oracle_config: dict[str, Any] = Field(..., description="Oracle connection settings")
    default_target_schema: str = Field(..., description="Target schema (e.g., FLEXT_DW)")
    batch_size: int = Field(10000, description="Records per batch")
    load_method: LoadMethod = Field(LoadMethod.APPEND_ONLY, description="Load strategy")
    table_prefix: str = Field("", description="Table name prefix")
```

### LoadJob (DomainEntity)

```python
class LoadJob(DomainEntity):
    """Load job entity with FLEXT patterns."""
    stream_name: str
    table_name: str
    status: LoadJobStatus
    records_processed: int = 0
    records_failed: int = 0
    started_at: datetime
    completed_at: datetime | None = None
```

### LoadMethod (StrEnum)

```python
class LoadMethod(StrEnum):
    """FLEXT standard load methods."""
    APPEND_ONLY = "append_only"  # FLEXT default for high performance
    UPSERT = "upsert"           # Oracle MERGE operations
    OVERWRITE = "overwrite"     # Full table refresh
```

### SingerRecord (DomainValueObject)

```python
class SingerRecord(DomainValueObject):
    """Singer message following FLEXT value object patterns."""
    type: str
    stream: str | None = None
    record: dict[str, Any] | None = None
    record_schema: dict[str, Any] | None = None
    value: dict[str, Any] | None = None
```

## FLEXT Configuration

### FLEXT Environment Standards

Environment variables following FLEXT workspace patterns:

| Variable | Type | Description | FLEXT Standard |
|----------|------|-------------|----------------|
| `DATABASE__HOST` | string | Oracle hostname | Standard FLEXT env pattern |
| `DATABASE__SERVICE_NAME` | string | Oracle service | Standard FLEXT env pattern |
| `DATABASE__USERNAME` | string | Database user | Standard FLEXT env pattern |
| `DATABASE__PASSWORD` | string | Database password | Standard FLEXT env pattern |
| `DATABASE__SCHEMA` | string | Target schema | Typically FLEXT_DW |

### FLEXT Target Configuration

Configuration following FLEXT patterns:

| Option | Type | Default | FLEXT Standard |
|--------|------|---------|----------------|
| `oracle_config` | object | required | flext-db-oracle connection config |
| `default_target_schema` | string | required | Use FLEXT_DW for data warehouse |
| `batch_size` | int | 10000 | FLEXT performance standard |
| `load_method` | enum | append_only | FLEXT default for performance |

### FLEXT Integration Example

```json
{
  "oracle_config": {
    "host": "oracle.flext.local",
    "service_name": "FLEXT_DB",
    "username": "flext_etl",
    "password": "${DATABASE__PASSWORD}"
  },
  "default_target_schema": "FLEXT_DW",
  "batch_size": 10000,
  "load_method": "append_only"
}
```

## Type Mappings

Intelligent Oracle type selection based on column names and JSON schema:

| JSON Schema | Column Pattern | Oracle Type | Example |
|-------------|---------------|-------------|---------|
| `integer` | `*_ID` | NUMBER(38,0) | USER_ID |
| `boolean` | `*_FLG` | NUMBER(1,0) | ACTIVE_FLG |
| `string` | `*_TS` | TIMESTAMP | CREATE_TS |
| `number` | `*_AMOUNT` | NUMBER(19,4) | TOTAL_AMOUNT |
| `string` | default | VARCHAR2(4000) | NAME |
| `object/array` | any | CLOB | JSON_DATA |

## Example Usage

### FLEXT Implementation Example

```python
from flext_target_oracle.application.services import SingerTargetService
from flext_target_oracle.domain.models import TargetConfig, LoadMethod
from flext_core import ServiceResult
from flext_observability.logging import get_logger

logger = get_logger(__name__)

# FLEXT-standard configuration
config = TargetConfig(
    oracle_config={
        "host": "oracle.flext.local",
        "service_name": "FLEXT_DB", 
        "username": "flext_etl",
        "password": "secure_password"
    },
    default_target_schema="FLEXT_DW",
    batch_size=10000,
    load_method=LoadMethod.APPEND_ONLY
)

# Initialize with FLEXT dependencies
service = SingerTargetService(config)

# Process with ServiceResult pattern
result: ServiceResult[None] = await service.process_singer_message({
    "type": "RECORD",
    "stream": "users",
    "record": {"id": 1, "name": "Alice", "active_flg": 1}
})

# FLEXT error handling
if result.is_success:
    logger.info("Message processed successfully")
else:
    logger.error(f"Processing failed: {result.error}")

# Finalize with statistics
stats_result = await service.finalize_all_streams()
if stats_result.is_success:
    stats = stats_result.value
    logger.info(f"FLEXT target completed: {stats.successful_records} records loaded")
```
