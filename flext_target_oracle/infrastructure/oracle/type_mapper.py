"""Oracle type mapper implementation.

Implements type mapping strategies for converting between
source types and Oracle-specific types.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from ...core.exceptions import UnsupportedTypeError
from ...core.interfaces.type_mapper import ITypeMapper, ITypeStrategy, ITypeValidator

if TYPE_CHECKING:
    from ...core.models.schema import FieldMetadata, TypeContext

logger = logging.getLogger(__name__)


class StringTypeStrategy:
    """Strategy for mapping string types to Oracle."""

    def can_handle(self, source_type: str) -> bool:
        """Check if this strategy can handle the given source type."""
        return source_type.lower() in {"string", "text", "varchar", "char"}

    def map(self, source_type: str, context: TypeContext) -> str:
        """Map string type to Oracle type."""
        max_length = context.get_max_length()

        # Check for special patterns
        if context.has_pattern("*_set"):
            return "VARCHAR2(4000 CHAR)"

        if context.has_pattern("*_desc*") or context.has_pattern("*_description"):
            return "VARCHAR2(4000 CHAR)"

        if context.has_pattern("*_code"):
            return "VARCHAR2(50 CHAR)"

        if context.has_pattern("*_name"):
            return "VARCHAR2(255 CHAR)"

        # Check length constraints
        if max_length > 4000:
            return "CLOB"

        return f"VARCHAR2({max_length} CHAR)"

    def validate(self, value: Any, context: TypeContext) -> bool:
        """Validate if value is compatible with the mapped type."""
        if value is None:
            return True

        if not isinstance(value, str):
            return False

        max_length = context.get_max_length()
        if max_length < 4000:
            return len(value) <= max_length

        return True


class IntegerTypeStrategy:
    """Strategy for mapping integer types to Oracle."""

    def can_handle(self, source_type: str) -> bool:
        """Check if this strategy can handle the given source type."""
        return source_type.lower() in {"integer", "int", "bigint", "smallint"}

    def map(self, source_type: str, context: TypeContext) -> str:
        """Map integer type to Oracle type."""
        # Check for ID patterns
        if context.has_pattern("*_id") or context.field_name.lower() == "id":
            return "NUMBER"

        # Check for flag/boolean patterns
        if context.has_pattern("*_flg") or context.has_pattern("*_flag"):
            return "NUMBER(1,0)"

        # Default integer mapping
        if context.precision:
            return f"NUMBER({context.precision},0)"

        return "NUMBER"

    def validate(self, value: Any, context: TypeContext) -> bool:
        """Validate if value is compatible with the mapped type."""
        if value is None:
            return True

        try:
            int(value)
            return True
        except (ValueError, TypeError):
            return False


class NumberTypeStrategy:
    """Strategy for mapping numeric/decimal types to Oracle."""

    def can_handle(self, source_type: str) -> bool:
        """Check if this strategy can handle the given source type."""
        return source_type.lower() in {
            "number",
            "numeric",
            "decimal",
            "float",
            "double",
            "real",
        }

    def map(self, source_type: str, context: TypeContext) -> str:
        """Map numeric type to Oracle type."""
        # Check for price/money patterns
        if any(
            context.has_pattern(p) for p in ["*_price", "*_cost", "*_amount", "*_value"]
        ):
            return "NUMBER(19,4)"

        # Check for percentage patterns
        if context.has_pattern("*_percent*") or context.has_pattern("*_rate"):
            return "NUMBER(5,2)"

        # Check for quantity patterns
        if any(context.has_pattern(p) for p in ["*_qty", "*_quantity", "*_count"]):
            return "NUMBER(19,6)"

        # Use precision and scale if provided
        if context.precision and context.scale:
            return f"NUMBER({context.precision},{context.scale})"
        elif context.precision:
            return f"NUMBER({context.precision})"

        return "NUMBER"

    def validate(self, value: Any, context: TypeContext) -> bool:
        """Validate if value is compatible with the mapped type."""
        if value is None:
            return True

        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False


class BooleanTypeStrategy:
    """Strategy for mapping boolean types to Oracle."""

    def can_handle(self, source_type: str) -> bool:
        """Check if this strategy can handle the given source type."""
        return source_type.lower() in {"boolean", "bool"}

    def map(self, source_type: str, context: TypeContext) -> str:
        """Map boolean type to Oracle type."""
        return "NUMBER(1,0)"

    def validate(self, value: Any, context: TypeContext) -> bool:
        """Validate if value is compatible with the mapped type."""
        if value is None:
            return True

        if isinstance(value, bool):
            return True

        if isinstance(value, str):
            return value.lower() in {"true", "false", "1", "0", "yes", "no", "y", "n"}

        if isinstance(value, (int, float)):
            return value in {0, 1}

        return False


class DateTimeTypeStrategy:
    """Strategy for mapping date/time types to Oracle."""

    def can_handle(self, source_type: str) -> bool:
        """Check if this strategy can handle the given source type."""
        return source_type.lower() in {
            "date",
            "datetime",
            "timestamp",
            "time",
            "date-time",
            "datetime-tz",
            "timestamp-tz",
        }

    def map(self, source_type: str, context: TypeContext) -> str:
        """Map date/time type to Oracle type."""
        source_lower = source_type.lower()

        if source_lower == "date":
            return "DATE"

        if source_lower == "time":
            return "TIMESTAMP(6)"

        if "tz" in source_lower:
            return "TIMESTAMP(6) WITH TIME ZONE"

        # Default timestamp
        return "TIMESTAMP(6)"

    def validate(self, value: Any, context: TypeContext) -> bool:
        """Validate if value is compatible with the mapped type."""
        if value is None:
            return True

        # Accept string dates/timestamps
        if isinstance(value, str):
            return True  # Oracle will validate format

        # Accept datetime objects
        try:
            from datetime import datetime, date

            return isinstance(value, (datetime, date))
        except ImportError:
            return False


class ObjectTypeStrategy:
    """Strategy for mapping object/JSON types to Oracle."""

    def can_handle(self, source_type: str) -> bool:
        """Check if this strategy can handle the given source type."""
        return source_type.lower() in {"object", "json", "jsonb", "struct"}

    def map(self, source_type: str, context: TypeContext) -> str:
        """Map object type to Oracle type."""
        # Use CLOB for JSON storage (Oracle 19c+ supports JSON data type)
        return "CLOB"

    def validate(self, value: Any, context: TypeContext) -> bool:
        """Validate if value is compatible with the mapped type."""
        if value is None:
            return True

        # Must be serializable to JSON
        try:
            import json

            json.dumps(value)
            return True
        except (TypeError, ValueError):
            return False


class ArrayTypeStrategy:
    """Strategy for mapping array types to Oracle."""

    def can_handle(self, source_type: str) -> bool:
        """Check if this strategy can handle the given source type."""
        return source_type.lower() in {"array", "list"}

    def map(self, source_type: str, context: TypeContext) -> str:
        """Map array type to Oracle type."""
        # Store as JSON in CLOB
        return "CLOB"

    def validate(self, value: Any, context: TypeContext) -> bool:
        """Validate if value is compatible with the mapped type."""
        if value is None:
            return True

        # Must be a list and serializable
        if not isinstance(value, list):
            return False

        try:
            import json

            json.dumps(value)
            return True
        except (TypeError, ValueError):
            return False


class OracleTypeMapper:
    """Oracle type mapper implementation."""

    def __init__(self) -> None:
        """Initialize type mapper with strategies."""
        self._strategies: list[ITypeStrategy] = [
            StringTypeStrategy(),
            IntegerTypeStrategy(),
            NumberTypeStrategy(),
            BooleanTypeStrategy(),
            DateTimeTypeStrategy(),
            ObjectTypeStrategy(),
            ArrayTypeStrategy(),
        ]

        # Pattern-based mappings for field names
        self._pattern_mappings = {
            # ID patterns
            "*_id": "NUMBER",
            "id": "NUMBER",
            # Key patterns
            "*_key": "VARCHAR2(255 CHAR)",
            # Quantity patterns
            "*_qty": "NUMBER",
            "*_quantity": "NUMBER",
            "*_count": "NUMBER",
            "*_amount": "NUMBER",
            "*_number": "NUMBER",
            "*_total": "NUMBER",
            # Price patterns
            "*_price": "NUMBER(19,4)",
            "*_cost": "NUMBER(19,4)",
            "*_rate": "NUMBER(5,2)",
            "*_percent": "NUMBER(5,2)",
            "*_value": "NUMBER(19,4)",
            # Date patterns
            "*_date": "DATE",
            "*_time": "TIMESTAMP(6)",
            "*_ts": "TIMESTAMP(6)",
            "*_timestamp": "TIMESTAMP(6)",
            "*_datetime": "TIMESTAMP(6)",
            "*_at": "TIMESTAMP(6)",
            "created_*": "TIMESTAMP(6)",
            "updated_*": "TIMESTAMP(6)",
            "modified_*": "TIMESTAMP(6)",
            # Flag patterns
            "*_flg": "NUMBER(1,0)",
            "*_flag": "NUMBER(1,0)",
            "*_enabled": "NUMBER(1,0)",
            "*_active": "NUMBER(1,0)",
            # Description patterns
            "*_desc": "VARCHAR2(4000 CHAR)",
            "*_description": "VARCHAR2(4000 CHAR)",
            "*_comment": "VARCHAR2(4000 CHAR)",
            "*_note": "VARCHAR2(4000 CHAR)",
            # Code patterns
            "*_code": "VARCHAR2(50 CHAR)",
            "*_cd": "VARCHAR2(50 CHAR)",
            # Name patterns
            "*_name": "VARCHAR2(255 CHAR)",
            "*_nm": "VARCHAR2(255 CHAR)",
            # Address patterns
            "*_addr*": "VARCHAR2(500 CHAR)",
            "*_address*": "VARCHAR2(500 CHAR)",
            # Set patterns (complex fields)
            "*_set": "VARCHAR2(4000 CHAR)",
        }

    def map_type(self, source_type: str, context: TypeContext) -> str:
        """Map a source type to Oracle type using context."""
        # First try pattern-based mapping
        oracle_type = self.map_from_pattern(context.field_name, context.sample_value)
        if oracle_type:
            return oracle_type

        # Then try strategy-based mapping
        for strategy in self._strategies:
            if strategy.can_handle(source_type):
                return strategy.map(source_type, context)

        # Default mapping
        logger.warning(f"No specific mapping for type '{source_type}', using VARCHAR2")
        return "VARCHAR2(255 CHAR)"

    def map_field(self, field: FieldMetadata) -> str:
        """Map a field definition to Oracle type."""
        # Handle multiple types (nullable)
        field_type = field.type
        if isinstance(field_type, list):
            # Filter out null type
            non_null_types = [t for t in field_type if t.value != "null"]
            if non_null_types:
                field_type = non_null_types[0]
            else:
                field_type = field.type[0]

        context = TypeContext(
            field_name=field.name,
            source_type=field_type.value,
            max_length=field.max_length,
            precision=field.precision,
            scale=field.scale,
            metadata=field.metadata,
        )

        return self.map_type(field_type.value, context)

    def get_supported_types(self) -> list[str]:
        """Get list of supported source types."""
        supported = []
        for strategy in self._strategies:
            # Get types from strategy
            if hasattr(strategy, "can_handle"):
                # Check common types
                for t in [
                    "string",
                    "integer",
                    "number",
                    "boolean",
                    "date",
                    "datetime",
                    "object",
                    "array",
                ]:
                    if strategy.can_handle(t):
                        supported.append(t)
        return list(set(supported))

    def register_strategy(self, strategy: ITypeStrategy) -> None:
        """Register a new type mapping strategy."""
        self._strategies.insert(0, strategy)  # Add at beginning for priority

    def map_from_pattern(self, field_name: str, sample_value: Any | None = None) -> str:
        """Map type based on field name pattern and optional sample value."""
        field_lower = field_name.lower()

        import fnmatch

        for pattern, oracle_type in self._pattern_mappings.items():
            if pattern.startswith("*") and pattern.endswith("*"):
                # Contains pattern
                if pattern[1:-1] in field_lower:
                    return oracle_type
            elif pattern.startswith("*"):
                # Suffix pattern
                if field_lower.endswith(pattern[1:]):
                    return oracle_type
            elif pattern.endswith("*"):
                # Prefix pattern
                if field_lower.startswith(pattern[:-1]):
                    return oracle_type
            else:
                # Exact match or glob pattern
                if field_lower == pattern or fnmatch.fnmatch(field_lower, pattern):
                    return oracle_type

        return ""  # No pattern matched


class OracleTypeValidator:
    """Oracle type validator implementation."""

    def is_compatible(self, source_type: str, target_type: str) -> bool:
        """Check if source type is compatible with target type."""
        # Normalize types
        source_upper = source_type.upper()
        target_upper = target_type.upper()

        # Extract base type (remove size specifications)
        source_base = source_upper.split("(")[0].strip()
        target_base = target_upper.split("(")[0].strip()

        # Compatible mappings
        compatible = {
            "VARCHAR2": {"STRING", "TEXT", "VARCHAR", "CHAR", "VARCHAR2"},
            "NUMBER": {
                "INTEGER",
                "INT",
                "BIGINT",
                "SMALLINT",
                "NUMERIC",
                "DECIMAL",
                "FLOAT",
                "DOUBLE",
                "NUMBER",
            },
            "DATE": {"DATE"},
            "TIMESTAMP": {"DATETIME", "TIMESTAMP", "TIME"},
            "CLOB": {"OBJECT", "JSON", "ARRAY", "TEXT", "CLOB"},
        }

        # Check compatibility
        for oracle_type, source_types in compatible.items():
            if target_base == oracle_type and source_base in source_types:
                return True

        return False

    def validate_value(self, value: Any, target_type: str) -> bool:
        """Validate if value can be stored in target type."""
        if value is None:
            return True

        target_upper = target_type.upper()

        # VARCHAR2 validation
        if "VARCHAR2" in target_upper:
            if not isinstance(value, str):
                return False

            # Extract length
            import re

            match = re.search(r"VARCHAR2\((\d+)", target_upper)
            if match:
                max_length = int(match.group(1))
                return len(value) <= max_length

            return True

        # NUMBER validation
        if "NUMBER" in target_upper:
            try:
                float(value)
                return True
            except (ValueError, TypeError):
                return False

        # DATE/TIMESTAMP validation
        if any(t in target_upper for t in ["DATE", "TIMESTAMP"]):
            # Oracle will handle conversion
            return isinstance(value, (str, int, float))

        # CLOB validation
        if "CLOB" in target_upper:
            return True  # CLOBs can store almost anything

        return False

    def coerce_value(self, value: Any, target_type: str) -> Any:
        """Coerce value to be compatible with target type."""
        if value is None:
            return None

        target_upper = target_type.upper()

        # NUMBER coercion
        if "NUMBER" in target_upper and "NUMBER(1,0)" in target_upper:
            # Boolean coercion
            if isinstance(value, bool):
                return 1 if value else 0
            if isinstance(value, str):
                return 1 if value.lower() in {"true", "1", "yes", "y"} else 0
            return int(bool(value))

        if "NUMBER" in target_upper:
            if isinstance(value, str):
                if value == "":
                    return None
                try:
                    return float(value)
                except ValueError:
                    return None
            return value

        # VARCHAR2 coercion
        if "VARCHAR2" in target_upper:
            return str(value)

        # CLOB coercion
        if "CLOB" in target_upper:
            if isinstance(value, (dict, list)):
                import json

                return json.dumps(value)
            return str(value)

        return value

    def get_validation_errors(self, value: Any, target_type: str) -> list[str]:
        """Get validation errors for a value and target type."""
        errors = []

        if not self.validate_value(value, target_type):
            errors.append(
                f"Value '{value}' is not compatible with Oracle type '{target_type}'"
            )

        return errors
