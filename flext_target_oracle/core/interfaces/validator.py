"""Validation interfaces.

These interfaces define contracts for different types of validation
in the system, following Interface Segregation Principle.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from ..models.config import ValidationResult
    from ..models.schema import SchemaDefinition


@runtime_checkable
class IConfigValidator(Protocol):
    """Interface for configuration validation."""

    @abstractmethod
    def validate(self, config: dict[str, Any]) -> ValidationResult:
        """Validate configuration and return result."""

    @abstractmethod
    def validate_connection_params(self, config: dict[str, Any]) -> ValidationResult:
        """Validate database connection parameters."""

    @abstractmethod
    def validate_performance_settings(self, config: dict[str, Any]) -> ValidationResult:
        """Validate performance-related settings."""

    @abstractmethod
    def validate_license_compliance(self, config: dict[str, Any]) -> ValidationResult:
        """Validate Oracle license compliance settings."""


@runtime_checkable
class IDataValidator(Protocol):
    """Interface for data validation."""

    @abstractmethod
    def validate_record(
        self, record: dict[str, Any], schema: SchemaDefinition
    ) -> ValidationResult:
        """Validate a single record against schema."""

    @abstractmethod
    def validate_batch(
        self, records: list[dict[str, Any]], schema: SchemaDefinition
    ) -> ValidationResult:
        """Validate a batch of records."""

    @abstractmethod
    def validate_field(
        self, field_name: str, value: Any, field_schema: dict[str, Any]
    ) -> ValidationResult:
        """Validate a single field value."""

    @abstractmethod
    def sanitize_record(
        self, record: dict[str, Any], schema: SchemaDefinition
    ) -> dict[str, Any]:
        """Sanitize a record to fix common issues."""


@runtime_checkable
class ISchemaValidator(Protocol):
    """Interface for schema validation."""

    @abstractmethod
    def validate_schema(self, schema: SchemaDefinition) -> ValidationResult:
        """Validate a schema definition."""

    @abstractmethod
    def validate_field_definition(self, field: dict[str, Any]) -> ValidationResult:
        """Validate a field definition."""

    @abstractmethod
    def check_schema_compatibility(
        self, source: SchemaDefinition, target: SchemaDefinition
    ) -> ValidationResult:
        """Check if source schema is compatible with target."""

    @abstractmethod
    def suggest_schema_improvements(self, schema: SchemaDefinition) -> list[str]:
        """Suggest improvements for schema definition."""
