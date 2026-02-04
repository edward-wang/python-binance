# Phase 2: Parser (Tasks 5-9)

> **Navigation:** [Overview](00-overview.md) | [Foundation](01-foundation.md) | **Parser** | [Templates & Emitter](03-templates-emitter.md) | [CLI & Integration](04-cli-integration.md)

> **Prerequisites:** Complete Tasks 0-4 in [01-foundation.md](01-foundation.md) first.

---

## Task 5: Implement YAML Parser - Basic Structure

**Files:**
- Modify: `generator/parser.py`
- Create: `tests/unit/generator/test_parser.py`

**Step 1: Write the failing test**

```python
# tests/unit/generator/test_parser.py
from pathlib import Path

import pytest


def test_parse_yaml_file():
    """Test parsing a single YAML spec file."""
    from generator.parser import parse_yaml_file

    spec_file = Path("specs/openapi/spot/get_api_v3_klines.yaml")
    if not spec_file.exists():
        pytest.skip("Spec file not found")

    data = parse_yaml_file(spec_file)

    assert "components" in data
    assert "paths" in data


def test_extract_path_and_method():
    """Test extracting path and method from spec data."""
    from generator.parser import extract_path_and_method

    data = {
        "paths": {
            "/api/v3/klines": {
                "get": {"operationId": "GetKlinesV3"}
            }
        }
    }

    path, method, operation = extract_path_and_method(data)

    assert path == "/api/v3/klines"
    assert method == "GET"
    assert operation["operationId"] == "GetKlinesV3"


def test_is_signed_endpoint():
    """Test detecting signed endpoints."""
    from generator.parser import is_signed_endpoint

    # Unsigned
    operation = {"parameters": [{"name": "symbol"}]}
    assert is_signed_endpoint(operation) is False

    # Signed with security
    operation = {"security": [{"ApiKey": []}]}
    assert is_signed_endpoint(operation) is True

    # Signed with timestamp param
    operation = {"parameters": [{"name": "timestamp", "required": True}]}
    assert is_signed_endpoint(operation) is True
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/generator/test_parser.py::test_parse_yaml_file -v`
Expected: FAIL with "cannot import name 'parse_yaml_file' from 'generator.parser'"

**Step 3: Implement basic parser functions**

```python
# generator/parser.py
"""Parse OpenAPI YAML files into internal models.

Handles the individual endpoint YAML files in specs/openapi/{api}/*.yaml
"""
from pathlib import Path
from typing import Any

import yaml


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
    """Determine if endpoint requires signature."""
    if "security" in operation:
        return True

    for param in operation.get("parameters", []):
        if param.get("name") == "timestamp" and param.get("required"):
            return True

    request_body = operation.get("requestBody", {})
    content = request_body.get("content", {})
    form_data = content.get("application/x-www-form-urlencoded", {})
    schema_ref = form_data.get("schema", {}).get("$ref", "")
    if schema_ref:
        return True

    return False
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/generator/test_parser.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add generator/parser.py tests/unit/generator/test_parser.py
git commit -m "feat: implement basic YAML parser functions"
```

---

## Task 6: Implement Parameter Parsing

**Files:**
- Modify: `generator/parser.py`
- Modify: `tests/unit/generator/test_parser.py`

**Step 1: Write the failing test**

```python
# Add to tests/unit/generator/test_parser.py

def test_parse_parameter():
    """Test parsing a single parameter."""
    from generator.parser import parse_parameter

    param_data = {
        "name": "symbol",
        "in": "query",
        "required": True,
        "schema": {"type": "string", "default": ""},
        "description": "Trading pair"
    }

    param = parse_parameter(param_data)

    assert param.name == "symbol"
    assert param.py_name == "symbol"
    assert param.type == "str"
    assert param.required is True


def test_parse_parameter_with_int64():
    """Test parsing int64 parameter."""
    from generator.parser import parse_parameter

    param_data = {
        "name": "startTime",
        "in": "query",
        "schema": {"type": "integer", "format": "int64"}
    }

    param = parse_parameter(param_data)

    assert param.type == "int"
    assert param.required is False


def test_parse_parameter_with_enum():
    """Test parsing enum parameter."""
    from generator.parser import parse_parameter

    param_data = {
        "name": "interval",
        "in": "query",
        "required": True,
        "schema": {
            "type": "string",
            "enum": ["1m", "5m", "1h", "1d"]
        }
    }

    param = parse_parameter(param_data)

    assert param.enum == ["1m", "5m", "1h", "1d"]


def test_parse_parameters():
    """Test parsing all parameters for an operation."""
    from generator.parser import parse_parameters

    operation = {
        "parameters": [
            {"name": "symbol", "in": "query", "required": True, "schema": {"type": "string"}},
            {"name": "limit", "in": "query", "schema": {"type": "integer", "default": 500}},
        ]
    }

    params = parse_parameters(operation)

    assert len(params) == 2
    assert params[0].name == "symbol"
    assert params[1].default == 500
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/generator/test_parser.py::test_parse_parameter -v`
Expected: FAIL

**Step 3: Implement parameter parsing**

```python
# Add to generator/parser.py

from generator.models import Parameter, Property, Schema, Endpoint
from generator.config import TYPE_MAP, to_snake_case


def parse_parameter(param_data: dict[str, Any]) -> Parameter:
    """Parse a single parameter definition."""
    name = param_data["name"]
    schema = param_data.get("schema", {})

    type_str = schema.get("type", "string")
    format_str = schema.get("format")
    py_type = TYPE_MAP.get((type_str, format_str), TYPE_MAP.get((type_str, None), "Any"))

    if type_str == "array":
        items = schema.get("items", {})
        item_type = items.get("type", "str")
        py_type = f"list[{TYPE_MAP.get((item_type, None), 'Any')}]"

    return Parameter(
        name=name,
        py_name=to_snake_case(name),
        type=py_type,
        required=param_data.get("required", False),
        default=schema.get("default"),
        description=param_data.get("description", ""),
        enum=schema.get("enum"),
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
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/generator/test_parser.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add generator/parser.py tests/unit/generator/test_parser.py
git commit -m "feat: implement parameter parsing for generator"
```

---

## Task 7: Implement Schema Parsing with Recursive Type Resolution

**Files:**
- Modify: `generator/parser.py`
- Modify: `tests/unit/generator/test_parser.py`

**Design: Recursive Type Resolution**

The parser needs to handle complex nested types like klines response:
```yaml
type: array
items:
  type: array
  items:
    oneOf:
      - type: integer
      - type: string
```

This should resolve to: `list[list[int | str]]`

**Step 1: Write the failing test**

```python
# Add to tests/unit/generator/test_parser.py

def test_resolve_type_basic():
    """Test resolving basic types."""
    from generator.parser import resolve_type

    assert resolve_type({"type": "string"}) == "str"
    assert resolve_type({"type": "integer"}) == "int"
    assert resolve_type({"type": "integer", "format": "int64"}) == "int"
    assert resolve_type({"type": "boolean"}) == "bool"
    assert resolve_type({"type": "number"}) == "float"


def test_resolve_type_array():
    """Test resolving array types."""
    from generator.parser import resolve_type

    assert resolve_type({
        "type": "array",
        "items": {"type": "string"}
    }) == "list[str]"


def test_resolve_type_nested_array():
    """Test resolving nested array types."""
    from generator.parser import resolve_type

    schema = {
        "type": "array",
        "items": {
            "type": "array",
            "items": {"type": "string"}
        }
    }
    assert resolve_type(schema) == "list[list[str]]"


def test_resolve_type_oneof():
    """Test resolving oneOf union types."""
    from generator.parser import resolve_type

    schema = {
        "oneOf": [
            {"type": "integer", "format": "int64"},
            {"type": "string"}
        ]
    }
    assert resolve_type(schema) == "int | str"


def test_resolve_type_klines():
    """Test resolving klines response type (most complex case)."""
    from generator.parser import resolve_type

    schema = {
        "type": "array",
        "items": {
            "type": "array",
            "items": {
                "oneOf": [
                    {"type": "integer", "format": "int64"},
                    {"type": "string"}
                ]
            }
        }
    }
    assert resolve_type(schema) == "list[list[int | str]]"


def test_resolve_type_ref():
    """Test resolving $ref types."""
    from generator.parser import resolve_type

    schema = {"$ref": "#/components/schemas/OrderResponse"}
    assert resolve_type(schema) == "OrderResponse"


def test_parse_schema_klines():
    """Test parsing klines schema (raw array response)."""
    from generator.parser import parse_schema

    schema_data = {
        "type": "array",
        "items": {
            "type": "array",
            "items": {
                "oneOf": [
                    {"type": "integer", "format": "int64"},
                    {"type": "string"}
                ]
            }
        }
    }

    schema = parse_schema("Kline", "GetKlinesV3Resp", schema_data)

    assert schema.is_array is True
    assert schema.raw_type == "list[list[int | str]]"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/generator/test_parser.py::test_resolve_type_basic -v`
Expected: FAIL

**Step 3: Implement recursive type resolution**

```python
# Add to generator/parser.py

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
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/generator/test_parser.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add generator/parser.py tests/unit/generator/test_parser.py
git commit -m "feat: implement schema parsing with recursive type resolution"
```

---

## Task 8: Implement Endpoint Parsing with requestBody Support

**Files:**
- Modify: `generator/parser.py`
- Modify: `tests/unit/generator/test_parser.py`

**Design: requestBody Parameter Extraction**

POST/PUT endpoints often define parameters in `requestBody` instead of `parameters`. The parser needs to extract and merge these.

**Step 1: Write the failing test**

```python
# Add to tests/unit/generator/test_parser.py

def test_parse_request_body():
    """Test parsing requestBody parameters (POST endpoints)."""
    from generator.parser import parse_request_body

    components = {
        "schemas": {
            "CreateOrderReq": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "side": {"type": "string"},
                    "quantity": {"type": "string"},
                    "timestamp": {"type": "integer"},
                },
                "required": ["symbol", "side", "timestamp"]
            }
        }
    }

    operation = {
        "requestBody": {
            "content": {
                "application/x-www-form-urlencoded": {
                    "schema": {"$ref": "#/components/schemas/CreateOrderReq"}
                }
            }
        }
    }

    params = parse_request_body(operation, components)

    assert len(params) == 3  # timestamp excluded
    param_names = [p.name for p in params]
    assert "symbol" in param_names
    assert "timestamp" not in param_names


def test_parse_post_endpoint():
    """Test parsing POST endpoint with requestBody."""
    from generator.parser import parse_endpoint

    data = {
        "components": {
            "schemas": {
                "CreateOrderReq": {
                    "type": "object",
                    "properties": {
                        "symbol": {"type": "string"},
                        "side": {"type": "string"},
                        "timestamp": {"type": "integer"},
                    },
                    "required": ["symbol", "side", "timestamp"]
                },
                "CreateOrderResp": {
                    "type": "object",
                    "properties": {"orderId": {"type": "integer"}}
                }
            },
            "securitySchemes": {"ApiKey": {"type": "apiKey"}}
        },
        "paths": {
            "/api/v3/order": {
                "post": {
                    "operationId": "CreateOrderV3",
                    "security": [{"ApiKey": []}],
                    "requestBody": {
                        "content": {
                            "application/x-www-form-urlencoded": {
                                "schema": {"$ref": "#/components/schemas/CreateOrderReq"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/CreateOrderResp"}
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    endpoint, schemas = parse_endpoint(data)

    assert endpoint.method_name == "create_order"
    assert endpoint.http_method == "POST"
    assert endpoint.requires_signature is True
    assert len(endpoint.parameters) == 2  # symbol, side (timestamp excluded)
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/generator/test_parser.py::test_parse_request_body -v`
Expected: FAIL

**Step 3: Implement endpoint parsing with requestBody support**

```python
# Add to generator/parser.py

from generator.config import to_method_name, to_class_name, get_module_for_path


def get_response_schema_ref(operation: dict[str, Any]) -> str | None:
    """Extract response schema reference from operation."""
    responses = operation.get("responses", {})
    success_response = responses.get("200", {})
    content = success_response.get("content", {})
    json_content = content.get("application/json", {})
    schema = json_content.get("schema", {})

    if "$ref" in schema:
        return schema["$ref"].split("/")[-1]

    if schema.get("type") == "array":
        items = schema.get("items", {})
        if "$ref" in items:
            return items["$ref"].split("/")[-1]

    return None


def parse_request_body(
    operation: dict[str, Any],
    components: dict[str, Any],
) -> list[Parameter]:
    """Parse parameters from requestBody (for POST/PUT endpoints)."""
    request_body = operation.get("requestBody", {})
    if not request_body:
        return []

    content = request_body.get("content", {})
    form_data = content.get("application/x-www-form-urlencoded", {})
    json_data = content.get("application/json", {})

    schema_data = form_data.get("schema", {}) or json_data.get("schema", {})
    if not schema_data:
        return []

    if "$ref" in schema_data:
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
    )

    return endpoint, schemas


def parse_endpoint_file(file_path: Path) -> tuple[Endpoint, dict[str, Schema]]:
    """Parse a single endpoint YAML file."""
    data = parse_yaml_file(file_path)
    return parse_endpoint(data)
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/generator/test_parser.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add generator/parser.py tests/unit/generator/test_parser.py
git commit -m "feat: implement endpoint parsing with requestBody support"
```

---

## Task 9: Implement Directory Parser with Structured Error Handling

**Files:**
- Modify: `generator/parser.py`
- Modify: `tests/unit/generator/test_parser.py`

**Design: Structured Error Handling**

Instead of printing warnings and continuing silently, we collect all errors and warnings into a structured `ParseResult`.

**Step 1: Write the failing test**

```python
# Add to tests/unit/generator/test_parser.py

def test_parse_spec_directory():
    """Test parsing all endpoints in a spec directory."""
    from generator.parser import parse_spec_directory
    from generator.config import SPEC_PATHS

    spec_dir = SPEC_PATHS.get("spot")
    if not spec_dir or not spec_dir.exists():
        pytest.skip("Spec directory not found")

    result = parse_spec_directory(spec_dir, limit=5)

    assert result.spec.name == "spot"
    assert len(result.spec.endpoints) <= 5
    assert len(result.spec.schemas) > 0
    assert isinstance(result.errors, list)


def test_parse_spec_directory_collects_errors():
    """Test that parsing collects errors into ParseResult."""
    from generator.parser import parse_spec_directory
    from generator.models import ParseErrorSeverity
    from generator.config import SPEC_PATHS

    spec_dir = SPEC_PATHS.get("spot")
    if not spec_dir or not spec_dir.exists():
        pytest.skip("Spec directory not found")

    result = parse_spec_directory(spec_dir, limit=50)

    assert isinstance(result.errors, list)
    for error in result.errors:
        assert hasattr(error, "file")
        assert hasattr(error, "severity")
        assert hasattr(error, "message")


def test_parse_result_summary():
    """Test ParseResult summary methods."""
    from generator.models import ParseResult, ParsedSpec, ParseError, ParseErrorSeverity
    from pathlib import Path

    spec = ParsedSpec(name="test", endpoints=[], schemas={})
    errors = [
        ParseError(Path("a.yaml"), ParseErrorSeverity.WARNING, "warning 1"),
        ParseError(Path("b.yaml"), ParseErrorSeverity.WARNING, "warning 2"),
        ParseError(Path("c.yaml"), ParseErrorSeverity.ERROR, "error 1"),
    ]
    result = ParseResult(spec=spec, errors=errors)

    assert result.warning_count == 2
    assert result.error_count == 1
    assert result.has_errors is True
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/generator/test_parser.py::test_parse_spec_directory -v`
Expected: FAIL

**Step 3: Implement directory parser with structured error handling**

```python
# Add to generator/parser.py

from generator.models import (
    ParsedSpec,
    ParseResult,
    ParseError,
    ParseErrorSeverity,
)
from generator.config import detect_naming_conflicts


def collect_schema_mappings(
    schemas_list: list[dict[str, Schema]],
) -> dict[str, str]:
    """Collect original -> clean name mappings from all schemas."""
    mappings: dict[str, str] = {}
    for schemas in schemas_list:
        for original_name, schema in schemas.items():
            mappings[original_name] = schema.name
    return mappings


def deduplicate_schemas(
    schemas_list: list[dict[str, Schema]],
) -> dict[str, Schema]:
    """Deduplicate schemas from multiple endpoints."""
    result: dict[str, Schema] = {}

    for schemas in schemas_list:
        for original_name, schema in schemas.items():
            clean_name = schema.name

            if clean_name not in result:
                result[clean_name] = schema
            elif len(schema.properties) > len(result[clean_name].properties):
                result[clean_name] = schema

    return result


def create_conflict_errors(
    conflicts: dict[str, list[str]],
) -> list[ParseError]:
    """Create ParseError objects for naming conflicts."""
    errors: list[ParseError] = []

    for clean_name, originals in sorted(conflicts.items()):
        suggestions = []
        for i, original in enumerate(sorted(originals)):
            if i == 0:
                suggestions.append(f"  # {original}: {clean_name}  # keep")
            else:
                suggested = f"{clean_name}{i + 1}"
                suggestions.append(f"  {original}: {suggested}")

        message = (
            f"Naming conflict: {len(originals)} schemas map to '{clean_name}'. "
            f"Add to generator/overrides.yaml under conflict_resolutions:\n"
            + "\n".join(suggestions)
        )

        errors.append(ParseError(
            file=Path("generator/overrides.yaml"),
            severity=ParseErrorSeverity.WARNING,
            message=message,
        ))

    return errors


def parse_spec_directory(
    spec_dir: Path,
    limit: int | None = None,
) -> ParseResult:
    """Parse all endpoint files in a spec directory."""
    name = spec_dir.name
    endpoints: list[Endpoint] = []
    all_schemas: list[dict[str, Schema]] = []
    errors: list[ParseError] = []

    yaml_files = sorted(spec_dir.glob("*.yaml"))
    if limit:
        yaml_files = yaml_files[:limit]

    for yaml_file in yaml_files:
        try:
            endpoint, schemas = parse_endpoint_file(yaml_file)
            endpoints.append(endpoint)
            all_schemas.append(schemas)
        except Exception as e:
            errors.append(ParseError(
                file=yaml_file,
                severity=ParseErrorSeverity.WARNING,
                message=f"Failed to parse: {e}",
                exception=e,
            ))
            continue

    mappings = collect_schema_mappings(all_schemas)
    conflicts = detect_naming_conflicts(mappings)
    errors.extend(create_conflict_errors(conflicts))

    deduped_schemas = deduplicate_schemas(all_schemas)

    spec = ParsedSpec(
        name=name,
        endpoints=endpoints,
        schemas=deduped_schemas,
    )

    return ParseResult(spec=spec, errors=errors)


def report_parse_result(result: ParseResult) -> None:
    """Print a summary report of parse results."""
    print(f"Parsed {len(result.spec.endpoints)} endpoints, "
          f"{len(result.spec.schemas)} schemas")

    if not result.errors:
        print("No errors or warnings.")
        return

    print(f"\n{result.warning_count} warnings, {result.error_count} errors:\n")

    for error in result.errors:
        prefix = "WARNING" if error.severity == ParseErrorSeverity.WARNING else "ERROR"
        print(f"[{prefix}] [{error.file}] {error.message}")

    if result.has_errors:
        print("\nParsing completed with errors.")
    else:
        print("\nParsing completed with warnings.")
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/generator/test_parser.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add generator/parser.py tests/unit/generator/test_parser.py
git commit -m "feat: implement directory parser with structured error handling

- Return ParseResult with errors list instead of printing
- Collect parse failures as ParseError with severity
- Detect naming conflicts and report with actionable guidance
- Add report_parse_result() for summary output"
```

---

> **Next:** Continue with [03-templates-emitter.md](03-templates-emitter.md) for Tasks 10-12 (Templates and Emitter)
