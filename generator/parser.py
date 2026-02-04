"""Parse OpenAPI YAML files into internal models.

Handles the individual endpoint YAML files in specs/openapi/{api}/*.yaml
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from generator.config import (
    TYPE_MAP,
    to_snake_case,
    to_class_name,
    to_method_name,
    get_module_for_path,
)
from generator.models import (
    Parameter,
    Property,
    Schema,
    Endpoint,
    ParsedSpec,
    ParseError,
    ParseErrorSeverity,
    ParseResult,
)


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
    # Handle $ref - use clean class name
    if "$ref" in schema_data:
        ref = schema_data["$ref"]
        ref_name = ref.split("/")[-1]
        return to_class_name(ref_name)

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


def parse_property(
    name: str,
    prop_data: dict[str, Any],
    required_list: list[str],
) -> Property:
    """Parse a single schema property."""
    py_type = resolve_type(prop_data)
    is_array = prop_data.get("type") == "array"

    ref_type: str | None = None
    if "$ref" in prop_data:
        ref_type = prop_data["$ref"].split("/")[-1]
    elif is_array and "$ref" in prop_data.get("items", {}):
        ref_type = prop_data["items"]["$ref"].split("/")[-1]

    return Property(
        name=name,
        py_name=to_snake_case(name),
        type=py_type,
        required=name in required_list,
        description=prop_data.get("description", ""),
        is_array=is_array,
        ref_type=ref_type,
    )


def parse_schema(
    clean_name: str,
    original_name: str,
    schema_data: dict[str, Any],
) -> Schema:
    """Parse a schema definition."""
    type_str = schema_data.get("type", "object")
    is_array = type_str == "array"

    properties: list[Property] = []
    item_type: str | None = None
    raw_type: str | None = None

    if is_array:
        items = schema_data.get("items", {})
        if "$ref" in items:
            ref = items["$ref"]
            item_type = ref.split("/")[-1]
        elif "properties" in items:
            required_list = items.get("required", [])
            for prop_name, prop_data in items.get("properties", {}).items():
                properties.append(parse_property(prop_name, prop_data, required_list))
        else:
            raw_type = resolve_type(schema_data)
    else:
        required_list = schema_data.get("required", [])
        for prop_name, prop_data in schema_data.get("properties", {}).items():
            properties.append(parse_property(prop_name, prop_data, required_list))

    return Schema(
        name=clean_name,
        original_name=original_name,
        properties=properties,
        is_array=is_array,
        description=schema_data.get("description", ""),
        item_type=item_type,
        raw_type=raw_type,
    )


# Success response codes to check (in priority order)
SUCCESS_CODES = ["200", "201", "202", "default"]


def get_response_schema_ref(operation: dict[str, Any]) -> str | None:
    """Extract response schema reference from operation.

    Iterates through success codes (200, 201, 202, default) and finds the first
    response with a JSON-like content type that has a schema.
    """
    responses = operation.get("responses", {})

    for code in SUCCESS_CODES:
        if code not in responses:
            continue

        content = responses[code].get("content", {})

        # Match any JSON-like content type (application/json, application/json;charset=utf-8)
        for content_type, media in content.items():
            if content_type.startswith("application/json"):
                schema = media.get("schema", {})

                if "$ref" in schema:
                    return schema["$ref"].split("/")[-1]

                if schema.get("type") == "array":
                    items = schema.get("items", {})
                    if "$ref" in items:
                        return items["$ref"].split("/")[-1]

                # Found a JSON response but no $ref - still valid, just no schema type
                if schema:
                    return None

    return None


def get_first_content_schema(content: dict[str, Any]) -> dict[str, Any] | None:
    """Get the first content schema from a content dict.

    Prioritizes form-urlencoded, then JSON-like types, then any type with a schema.
    """
    # Priority order for content types
    priority_prefixes = [
        "application/x-www-form-urlencoded",
        "application/json",
    ]

    # Check priority types first
    for prefix in priority_prefixes:
        for content_type, media in content.items():
            if content_type.startswith(prefix):
                if schema := media.get("schema"):
                    return schema

    # Fall back to any content type with a schema
    for content_type, media in content.items():
        if schema := media.get("schema"):
            return schema

    return None


def parse_request_body(
    operation: dict[str, Any],
    components: dict[str, Any],
) -> list[Parameter]:
    """Parse parameters from requestBody (for POST/PUT endpoints).

    Handles $ref chains and selects the first content type with a schema.
    """
    request_body = operation.get("requestBody", {})
    if not request_body:
        return []

    content = request_body.get("content", {})
    schema_data = get_first_content_schema(content)

    if not schema_data:
        return []

    # Resolve $ref chain
    while "$ref" in schema_data:
        ref_name = schema_data["$ref"].split("/")[-1]
        schema_data = components.get("schemas", {}).get(ref_name, {})
        if not schema_data:
            return []

    params: list[Parameter] = []
    required_list = schema_data.get("required", [])

    for prop_name, prop_data in schema_data.get("properties", {}).items():
        if prop_name in ("timestamp", "signature"):
            continue

        params.append(Parameter(
            name=prop_name,
            py_name=to_snake_case(prop_name),
            type=resolve_type(prop_data),
            required=prop_name in required_list,
            default=prop_data.get("default"),
            description=prop_data.get("description", ""),
        ))

    return params


def get_rate_limit_weight(operation: dict[str, Any]) -> int:
    """Extract rate limit weight from x-weight extension.

    Args:
        operation: OpenAPI operation object

    Returns:
        Weight value (defaults to 1 if not specified)
    """
    # Check for x-weight extension (Binance custom extension)
    weight = operation.get("x-weight", 1)
    if isinstance(weight, int):
        return weight
    # Some specs may have weight as string
    if isinstance(weight, str) and weight.isdigit():
        return int(weight)
    return 1


def parse_endpoint(
    data: dict[str, Any],
) -> tuple[Endpoint, dict[str, Schema]]:
    """Parse a single endpoint file data."""
    path, method, operation = extract_path_and_method(data)

    schemas: dict[str, Schema] = {}
    components = data.get("components", {})
    schema_defs = components.get("schemas", {})

    for schema_name, schema_data in schema_defs.items():
        if schema_name == "APIError" or schema_name.endswith("Req"):
            continue
        clean_name = to_class_name(schema_name)
        schemas[schema_name] = parse_schema(clean_name, schema_name, schema_data)

    response_ref = get_response_schema_ref(operation)
    response_schema: str | None = None
    is_array_response = False
    raw_response_type: str | None = None

    if response_ref and response_ref in schemas:
        schema = schemas[response_ref]
        response_schema = schema.name
        is_array_response = schema.is_array
        raw_response_type = schema.raw_type

    # Merge query parameters and body parameters
    query_params = parse_parameters(operation)
    body_params = parse_request_body(operation, components)
    all_params = query_params + body_params
    all_params.sort(key=lambda p: (not p.required, p.name))

    endpoint = Endpoint(
        operation_id=operation["operationId"],
        method_name=to_method_name(operation["operationId"]),
        http_method=method,
        path=path,
        parameters=all_params,
        response_schema=response_schema,
        is_array_response=is_array_response,
        requires_signature=is_signed_endpoint(operation),
        description=operation.get("description", operation.get("summary", "")),
        module=get_module_for_path(path),
        raw_response_type=raw_response_type,
        weight=get_rate_limit_weight(operation),
    )

    return endpoint, schemas


def parse_endpoint_file(file_path: Path) -> tuple[Endpoint, dict[str, Schema]]:
    """Parse a single endpoint YAML file."""
    data = parse_yaml_file(file_path)
    return parse_endpoint(data)


def parse_spec_directory(spec_dir: Path, name: str) -> ParseResult:
    """Parse all YAML files in a spec directory.

    Args:
        spec_dir: Path to directory containing endpoint YAML files
        name: Name for this spec (e.g., "spot", "umfutures")

    Returns:
        ParseResult containing parsed spec and any errors/warnings
    """
    endpoints: list[Endpoint] = []
    schemas: dict[str, Schema] = {}
    errors: list[ParseError] = []

    # Find all YAML files
    yaml_files = sorted(spec_dir.glob("*.yaml"))

    for file_path in yaml_files:
        try:
            endpoint, file_schemas = parse_endpoint_file(file_path)
            endpoints.append(endpoint)

            # Deduplicate schemas by original_name
            for schema_name, schema in file_schemas.items():
                if schema_name not in schemas:
                    schemas[schema_name] = schema

        except ValueError as e:
            # Expected errors (e.g., missing paths)
            errors.append(ParseError(
                file=file_path,
                severity=ParseErrorSeverity.WARNING,
                message=str(e),
                exception=e,
            ))
        except KeyError as e:
            # Missing required fields
            errors.append(ParseError(
                file=file_path,
                severity=ParseErrorSeverity.WARNING,
                message=f"Missing required field: {e}",
                exception=e,
            ))
        except Exception as e:
            # Unexpected errors
            errors.append(ParseError(
                file=file_path,
                severity=ParseErrorSeverity.ERROR,
                message=f"Unexpected error: {e}",
                exception=e,
            ))

    spec = ParsedSpec(
        name=name,
        endpoints=endpoints,
        schemas=schemas,
    )

    return ParseResult(spec=spec, errors=errors)
