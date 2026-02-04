"""Parse OpenAPI YAML files into internal models.

Handles the individual endpoint YAML files in specs/openapi/{api}/*.yaml
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from generator.config import TYPE_MAP, to_snake_case, to_class_name
from generator.models import Parameter, Property, Schema, Endpoint


def parse_yaml_file(file_path: Path) -> dict[str, Any]:
    """Parse a single YAML file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def extract_path_and_method(
    data: dict[str, Any],
) -> tuple[str, str, dict[str, Any]]:
    """Extract the endpoint path, HTTP method, and operation from spec data."""
    paths = data.get("paths", {})
    if not paths:
        raise ValueError("No paths found in spec")

    path = next(iter(paths.keys()))
    methods = paths[path]
    method = next(iter(methods.keys()))
    operation = methods[method]

    return path, method.upper(), operation


def is_signed_endpoint(operation: dict[str, Any]) -> bool:
    """Determine if endpoint requires signature.

    Detection priority:
    1. Primary: 'security' section present (OpenAPI standard)
    2. Secondary: Required 'timestamp' parameter (Binance convention)
    3. Tertiary: POST/PUT with requestBody schema (likely signed)
    """
    # Primary: Check security section (most reliable)
    if "security" in operation:
        return True

    # Secondary: Check for timestamp in query parameters
    for param in operation.get("parameters", []):
        if param.get("name") == "timestamp" and param.get("required"):
            return True

    # Tertiary: Check for requestBody with schema (POST/PUT endpoints)
    # These typically require signature in Binance API
    request_body = operation.get("requestBody", {})
    if request_body:
        content = request_body.get("content", {})
        for content_type, media in content.items():
            if media.get("schema"):
                return True

    return False


def resolve_type(schema_data: dict[str, Any]) -> str:
    """Recursively resolve OpenAPI schema to Python type annotation."""
    # Handle $ref
    if "$ref" in schema_data:
        ref = schema_data["$ref"]
        return ref.split("/")[-1]

    # Handle oneOf union types
    if "oneOf" in schema_data:
        types = [resolve_type(option) for option in schema_data["oneOf"]]
        seen: set[str] = set()
        unique_types: list[str] = []
        for t in types:
            if t not in seen:
                seen.add(t)
                unique_types.append(t)
        return " | ".join(unique_types)

    # Handle anyOf (treat same as oneOf)
    if "anyOf" in schema_data:
        types = [resolve_type(option) for option in schema_data["anyOf"]]
        seen: set[str] = set()
        unique_types: list[str] = []
        for t in types:
            if t not in seen:
                seen.add(t)
                unique_types.append(t)
        return " | ".join(unique_types)

    type_str = schema_data.get("type", "object")
    format_str = schema_data.get("format")

    # Handle arrays recursively
    if type_str == "array":
        items = schema_data.get("items", {})
        if items:
            item_type = resolve_type(items)  # Recursive call!
            return f"list[{item_type}]"
        return "list[Any]"

    # Handle basic types
    py_type = TYPE_MAP.get((type_str, format_str))
    if py_type:
        return py_type

    py_type = TYPE_MAP.get((type_str, None))
    if py_type:
        return py_type

    return "Any"


def generate_literal_type(enum_values: list[str]) -> str:
    """Generate a Literal type annotation from enum values.

    Args:
        enum_values: List of allowed string values

    Returns:
        Literal type string, e.g., 'Literal["BUY", "SELL"]'
    """
    quoted = [f'"{v}"' for v in enum_values]
    return f'Literal[{", ".join(quoted)}]'


def parse_parameter(param_data: dict[str, Any]) -> Parameter:
    """Parse a single parameter definition.

    Handles regular types, arrays, $ref schemas, and generates
    Literal types for enum parameters.
    """
    name = param_data["name"]
    schema = param_data.get("schema", {})
    enum_values = schema.get("enum")

    # Handle $ref in parameter schema
    if "$ref" in schema:
        ref_name = schema["$ref"].split("/")[-1]
        py_type = to_class_name(ref_name)
        literal_type = None
    elif enum_values and isinstance(enum_values, list) and len(enum_values) <= 20:
        # Generate Literal type for enums (skip if too many values)
        literal_type = generate_literal_type(enum_values)
        py_type = literal_type
    else:
        # Use resolve_type for consistent type resolution
        py_type = resolve_type(schema)
        literal_type = None

    return Parameter(
        name=name,
        py_name=to_snake_case(name),
        type=py_type,
        required=param_data.get("required", False),
        default=schema.get("default"),
        description=param_data.get("description", ""),
        enum=enum_values,
        literal_type=literal_type,
    )


def parse_parameters(operation: dict[str, Any]) -> list[Parameter]:
    """Parse all parameters for an operation."""
    params = []
    for param_data in operation.get("parameters", []):
        if param_data.get("name") == "timestamp":
            continue
        params.append(parse_parameter(param_data))

    params.sort(key=lambda p: (not p.required, p.name))
    return params
