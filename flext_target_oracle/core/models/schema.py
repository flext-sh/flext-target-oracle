"""Schema and type mapping models.

These models represent database schemas and type mapping contexts,
providing a clear structure for schema management.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class FieldType(str, Enum):
    """Supported field types."""

    STRING = "string"
    INTEGER = "integer"
    NUMBER = "number"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    TIME = "time"
    OBJECT = "object"
    ARRAY = "array"
    NULL = "null"


class FieldMetadata(BaseModel):
    """Metadata for a field in a schema."""

    name: str = Field(..., description="Field name")
    type: FieldType | list[FieldType] = Field(..., description="Field type(s)")
    nullable: bool = Field(True, description="Whether field is nullable")
    max_length: int | None = Field(None, description="Maximum length for string types")
    precision: int | None = Field(None, description="Precision for numeric types")
    scale: int | None = Field(None, description="Scale for numeric types")
    format: str | None = Field(
        None, description="Format hint (e.g., 'date-time', 'email')"
    )
    pattern: str | None = Field(None, description="Regex pattern for validation")
    default: Any = Field(None, description="Default value")
    description: str | None = Field(None, description="Field description")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    model_config = {
        "frozen": True,
    }

    def is_numeric(self) -> bool:
        """Check if field is numeric type."""
        if isinstance(self.type, list):
            return any(t in (FieldType.INTEGER, FieldType.NUMBER) for t in self.type)
        return self.type in (FieldType.INTEGER, FieldType.NUMBER)

    def is_temporal(self) -> bool:
        """Check if field is temporal type."""
        if isinstance(self.type, list):
            return any(
                t in (FieldType.DATE, FieldType.DATETIME, FieldType.TIME)
                for t in self.type
            )
        return self.type in (FieldType.DATE, FieldType.DATETIME, FieldType.TIME)


class SchemaDefinition(BaseModel):
    """Complete schema definition for a table/stream."""

    name: str = Field(..., description="Schema/stream name")
    fields: list[FieldMetadata] = Field(..., description="Field definitions")
    primary_keys: list[str] = Field(
        default_factory=list, description="Primary key fields"
    )
    unique_keys: list[list[str]] = Field(
        default_factory=list, description="Unique key combinations"
    )
    indexes: list[list[str]] = Field(
        default_factory=list, description="Index definitions"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    model_config = {
        "frozen": True,
    }

    def get_field(self, name: str) -> FieldMetadata | None:
        """Get field by name."""
        return next((f for f in self.fields if f.name == name), None)

    def get_primary_key_fields(self) -> list[FieldMetadata]:
        """Get primary key field definitions."""
        return [f for f in self.fields if f.name in self.primary_keys]

    def to_json_schema(self) -> dict[str, Any]:
        """Convert to JSON Schema format."""
        properties = {}
        required = []

        for field in self.fields:
            field_schema: dict[str, Any] = {}

            # Handle type
            if isinstance(field.type, list):
                field_schema["type"] = [t.value for t in field.type]
            else:
                field_schema["type"] = field.type.value

            # Add constraints
            if field.max_length is not None:
                field_schema["maxLength"] = field.max_length
            if field.pattern is not None:
                field_schema["pattern"] = field.pattern
            if field.format is not None:
                field_schema["format"] = field.format
            if field.description is not None:
                field_schema["description"] = field.description

            properties[field.name] = field_schema

            if not field.nullable:
                required.append(field.name)

        return {
            "type": "object",
            "properties": properties,
            "required": required,
            "additionalProperties": False,
        }


class TypeContext(BaseModel):
    """Context for type mapping decisions."""

    field_name: str = Field(..., description="Field name being mapped")
    source_type: str = Field(..., description="Source type")
    sample_value: Any = Field(None, description="Sample value for inference")
    max_length: int | None = Field(None, description="Maximum length constraint")
    precision: int | None = Field(None, description="Numeric precision")
    scale: int | None = Field(None, description="Numeric scale")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional context"
    )

    model_config = {
        "frozen": True,
    }

    def get_max_length(self, default: int = 255) -> int:
        """Get maximum length with default."""
        return self.max_length or default

    def has_pattern(self, pattern: str) -> bool:
        """Check if field name matches pattern."""
        import fnmatch

        return fnmatch.fnmatch(self.field_name.lower(), pattern.lower())
