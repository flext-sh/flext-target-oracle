"""Type mapping interfaces.

These interfaces define the contract for type conversion between
source systems and Oracle, enabling flexible type mapping strategies.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from ..models.schema import FieldMetadata, TypeContext


@runtime_checkable
class ITypeStrategy(Protocol):
    """Interface for type mapping strategies."""

    @abstractmethod
    def can_handle(self, source_type: str) -> bool:
        """Check if this strategy can handle the given source type."""

    @abstractmethod
    def map(self, source_type: str, context: TypeContext) -> str:
        """Map source type to Oracle type."""

    @abstractmethod
    def validate(self, value: Any, context: TypeContext) -> bool:
        """Validate if value is compatible with the mapped type."""


@runtime_checkable
class ITypeMapper(Protocol):
    """Interface for type mapping operations."""

    @abstractmethod
    def map_type(self, source_type: str, context: TypeContext) -> str:
        """Map a source type to Oracle type using context."""

    @abstractmethod
    def map_field(self, field: FieldMetadata) -> str:
        """Map a field definition to Oracle type."""

    @abstractmethod
    def get_supported_types(self) -> list[str]:
        """Get list of supported source types."""

    @abstractmethod
    def register_strategy(self, strategy: ITypeStrategy) -> None:
        """Register a new type mapping strategy."""

    @abstractmethod
    def map_from_pattern(self, field_name: str, sample_value: Any | None = None) -> str:
        """Map type based on field name pattern and optional sample value."""


@runtime_checkable
class ITypeValidator(Protocol):
    """Interface for type validation."""

    @abstractmethod
    def is_compatible(self, source_type: str, target_type: str) -> bool:
        """Check if source type is compatible with target type."""

    @abstractmethod
    def validate_value(self, value: Any, target_type: str) -> bool:
        """Validate if value can be stored in target type."""

    @abstractmethod
    def coerce_value(self, value: Any, target_type: str) -> Any:
        """Coerce value to be compatible with target type."""

    @abstractmethod
    def get_validation_errors(self, value: Any, target_type: str) -> list[str]:
        """Get validation errors for a value and target type."""
