"""Internal data models for parsed OpenAPI specs.

These dataclasses represent the parsed OpenAPI spec in a form
that's easy to use with Jinja2 templates.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


@dataclass
class Parameter:
    """Represents an endpoint parameter (query, path, body)."""

    name: str  # Original name from spec (camelCase)
    py_name: str  # Python name (snake_case)
    type: str  # Python type annotation (may include Literal for enums)
    required: bool
    default: str | int | float | bool | None
    description: str
    enum: list[str] | None = None
    literal_type: str | None = None  # e.g., 'Literal["1m", "5m", "1h"]' for enums


@dataclass
class Property:
    """Represents a property within a schema."""

    name: str  # Original name from spec (camelCase)
    py_name: str  # Python name (snake_case)
    type: str  # Python type annotation
    required: bool
    description: str = ""
    is_array: bool = False
    ref_type: str | None = None  # For nested schema references


@dataclass
class Schema:
    """Represents a response/request schema."""

    name: str  # Clean Python class name
    original_name: str  # Original name from spec
    properties: list[Property]
    is_array: bool  # True if this schema is an array of items
    description: str = ""
    item_type: str | None = None  # For array of $ref (e.g., list[Trade])
    raw_type: str | None = None  # For raw array types (e.g., list[list[int | str]])


@dataclass
class Endpoint:
    """Represents a single API endpoint."""

    operation_id: str  # Original operationId
    method_name: str  # Python method name (snake_case)
    http_method: str  # GET, POST, DELETE, PUT
    path: str  # API path
    parameters: list[Parameter]
    response_schema: str | None  # Response schema class name (e.g., "Order")
    is_array_response: bool  # True if response is array
    requires_signature: bool  # True if endpoint needs signing
    description: str
    module: str  # Target module (general, market, trade, account)
    request_schema: str | None = None  # For POST with body
    raw_response_type: str | None = None  # For raw types like "list[list[int | str]]"
    weight: int = 1  # Rate limit weight from x-weight extension


@dataclass
class ParsedSpec:
    """Container for all parsed data from a spec directory."""

    name: str  # spot, umfutures, cmfutures
    endpoints: list[Endpoint]
    schemas: dict[str, Schema]  # Deduplicated schemas


# ============ Error Handling ============


class ParseErrorSeverity(Enum):
    """Severity level for parse errors."""

    WARNING = "warning"  # Can skip, doesn't affect other files
    ERROR = "error"  # Serious issue, but continue processing


@dataclass
class ParseError:
    """Represents a parsing error or warning."""

    file: Path | None
    severity: ParseErrorSeverity
    message: str
    exception: Exception | None = None


@dataclass
class ParseResult:
    """Result of parsing a spec directory, including errors."""

    spec: ParsedSpec
    errors: list[ParseError] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        """Check if there are any ERROR-level issues."""
        return any(e.severity == ParseErrorSeverity.ERROR for e in self.errors)

    @property
    def warning_count(self) -> int:
        """Count warnings."""
        return sum(1 for e in self.errors if e.severity == ParseErrorSeverity.WARNING)

    @property
    def error_count(self) -> int:
        """Count errors."""
        return sum(1 for e in self.errors if e.severity == ParseErrorSeverity.ERROR)
