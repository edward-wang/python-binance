# Phase 2: Code Generator Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a code generator that parses OpenAPI YAML specs and outputs typed Python client code.

**Architecture:** The generator reads individual endpoint YAML files from `specs/openapi/`, parses them into an internal model (dataclasses), then uses Jinja2 templates to emit Python code. Schema deduplication ensures shared types are generated once.

**Tech Stack:** PyYAML (parsing), Jinja2 (templating), pathlib (file handling), dataclasses (internal model)

---

## Spec File Format Summary

Each endpoint file (e.g., `specs/openapi/spot/get_api_v3_klines.yaml`) contains:
- `components.schemas` - Request/response schema definitions
- `components.securitySchemes` - API key definition (if authenticated)
- `paths.{path}.{method}` - Endpoint definition with parameters, requestBody, responses, security

**Key patterns to handle:**
1. **Public endpoints** - No `security` section (e.g., `/api/v3/time`, `/api/v3/klines`)
2. **Signed endpoints** - Has `security` + `timestamp` parameter (e.g., `/api/v3/account`, `/api/v3/order`)
3. **Response types** - Object (`$ref`), array (`items.$ref`), raw array (`items.oneOf`)
4. **Parameters** - Query params with `required`, `default`, `type`, `format`, `enum`

---

## Task 1: Add Generator Dependencies

**Files:**
- Modify: `pyproject.toml`
- Modify: `requirements.txt`

**Step 1: Write the failing test**

```python
# tests/unit/test_generator_deps.py
def test_generator_dependencies_importable():
    """Test that generator dependencies are installed."""
    import yaml
    import jinja2
    assert yaml.__version__
    assert jinja2.__version__
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/test_generator_deps.py -v`
Expected: FAIL with "No module named 'yaml'" or "No module named 'jinja2'"

**Step 3: Update pyproject.toml with generator dependencies**

Add to `pyproject.toml` dependencies:
```toml
dependencies = [
    "aiohttp>=3.9",
    "msgspec>=0.18",
    "orjson>=3.9",
    "uvloop>=0.19; sys_platform != 'win32'",
    "pyyaml>=6.0",
    "jinja2>=3.1",
]
```

**Step 4: Update requirements.txt**

```
aiohttp>=3.9
msgspec>=0.18
orjson>=3.9
uvloop>=0.19; sys_platform != 'win32'
pyyaml>=6.0
jinja2>=3.1
```

**Step 5: Install dependencies**

Run: `pip install -e ".[dev]"`

**Step 6: Run test to verify it passes**

Run: `pytest tests/unit/test_generator_deps.py -v`
Expected: PASS

**Step 7: Commit**

```bash
git add pyproject.toml requirements.txt tests/unit/test_generator_deps.py
git commit -m "feat: add generator dependencies (pyyaml, jinja2)"
```

---

## Task 2: Create Generator Package Structure

**Files:**
- Create: `generator/__init__.py`
- Create: `generator/models.py` (stub)
- Create: `generator/parser.py` (stub)
- Create: `generator/emitter.py` (stub)
- Create: `generator/config.py` (stub)
- Create: `generator/__main__.py` (stub)

**Step 1: Write the failing test**

```python
# tests/unit/generator/test_package.py
def test_generator_package_importable():
    """Test that generator package structure exists."""
    import generator
    from generator import models, parser, emitter, config
    assert generator.__name__ == "generator"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/generator/test_package.py -v`
Expected: FAIL with "No module named 'generator'"

**Step 3: Create package structure**

```python
# generator/__init__.py
"""Code generator for Binance API client.

Reads OpenAPI YAML specs and generates typed Python code.
"""

__version__ = "0.1.0"
```

```python
# generator/models.py
"""Internal data models for parsed OpenAPI specs."""
```

```python
# generator/parser.py
"""Parse OpenAPI YAML files into internal models."""
```

```python
# generator/emitter.py
"""Emit Python code from internal models using templates."""
```

```python
# generator/config.py
"""Generator configuration and naming rules."""
```

```python
# generator/__main__.py
"""CLI entry point for generator."""

def main() -> None:
    """Run the generator."""
    print("Generator not yet implemented")

if __name__ == "__main__":
    main()
```

**Step 4: Create test directory**

```bash
mkdir -p tests/unit/generator
touch tests/unit/generator/__init__.py
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/unit/generator/test_package.py -v`
Expected: PASS

**Step 6: Commit**

```bash
git add generator/ tests/unit/generator/
git commit -m "feat: create generator package structure"
```

---

## Task 3: Implement Generator Config

**Files:**
- Modify: `generator/config.py`
- Create: `generator/overrides.yaml`
- Create: `tests/unit/generator/test_config.py`

**Design: Schema Class Name Generation**

The schema naming system uses **smart inference + override file + conflict detection**:

```
Input → Check overrides.yaml → Smart inference → Conflict detection → Output
```

1. **Override file** (`generator/overrides.yaml`) - Only for exceptions (~20-30 entries)
2. **Smart inference** - Handles 90% of cases automatically
3. **Conflict detection** - Warns when multiple schemas map to same name

**Step 1: Write the failing test**

```python
# tests/unit/generator/test_config.py
from pathlib import Path


def test_spec_paths_exist():
    """Test that spec path configuration points to real directories."""
    from generator.config import SPEC_PATHS

    assert "spot" in SPEC_PATHS
    assert SPEC_PATHS["spot"].exists()


def test_output_paths_configuration():
    """Test that output path configuration is defined."""
    from generator.config import OUTPUT_PATHS

    assert "api" in OUTPUT_PATHS
    assert "schemas" in OUTPUT_PATHS


def test_type_mapping():
    """Test OpenAPI to Python type mapping."""
    from generator.config import TYPE_MAP

    assert TYPE_MAP[("string", None)] == "str"
    assert TYPE_MAP[("integer", "int64")] == "int"
    assert TYPE_MAP[("boolean", None)] == "bool"


def test_snake_case_conversion():
    """Test camelCase to snake_case conversion."""
    from generator.config import to_snake_case

    assert to_snake_case("getUserById") == "get_user_by_id"
    assert to_snake_case("getAPIKey") == "get_api_key"
    assert to_snake_case("HTTPClient") == "http_client"
    assert to_snake_case("already_snake") == "already_snake"


def test_method_name_generation():
    """Test method name generation from operationId."""
    from generator.config import to_method_name

    assert to_method_name("GetKlinesV3") == "get_klines"
    assert to_method_name("CreateOrderV3") == "create_order"
    assert to_method_name("GetAccountV3") == "get_account"


def test_class_name_smart_inference():
    """Test smart class name inference without overrides."""
    from generator.config import to_class_name

    # Basic stripping of prefixes/suffixes
    assert to_class_name("GetKlinesV3Resp") == "Kline"  # strips Get, V3, Resp + singular
    assert to_class_name("GetTradesV3Resp") == "Trade"  # plural -> singular
    assert to_class_name("GetAvgPriceV3Resp") == "AvgPrice"  # no change needed
    assert to_class_name("GetAccountV3Resp") == "Account"

    # Handles various prefixes
    assert to_class_name("SpotCreateOrderV3Resp") == "CreateOrder"  # keeps verb
    assert to_class_name("PostOrderV3Resp") == "Order"  # strips Post


def test_class_name_with_overrides():
    """Test class name with semantic overrides."""
    from generator.config import to_class_name, load_overrides

    overrides = load_overrides()

    # Semantic rename: Depth -> OrderBook
    assert to_class_name("GetDepthV3Resp", overrides) == "OrderBook"


def test_class_name_edge_cases():
    """Test edge cases in class name generation."""
    from generator.config import to_class_name

    # Avoid empty string
    assert to_class_name("GetV3Resp") != ""
    assert to_class_name("GetV3Resp") == "GetV3Resp"  # fallback to original

    # Preserve meaningful names
    assert to_class_name("ExchangeInfo") == "ExchangeInfo"


def test_class_name_plural_to_singular():
    """Test plural to singular conversion."""
    from generator.config import to_singular

    assert to_singular("Trades") == "Trade"
    assert to_singular("Klines") == "Kline"
    assert to_singular("Balances") == "Balance"
    assert to_singular("Orders") == "Order"
    # Don't change words ending in 'ss'
    assert to_singular("Address") == "Address"
    # Don't change already singular
    assert to_singular("Order") == "Order"


def test_detect_naming_conflicts():
    """Test conflict detection for schema names."""
    from generator.config import detect_naming_conflicts

    mappings = {
        "GetOrderV3Resp": "Order",
        "PostOrderV3Resp": "Order",  # Conflict!
        "GetTradesV3Resp": "Trade",
    }

    conflicts = detect_naming_conflicts(mappings)

    assert len(conflicts) == 1
    assert "Order" in conflicts
    assert set(conflicts["Order"]) == {"GetOrderV3Resp", "PostOrderV3Resp"}


def test_load_overrides():
    """Test loading overrides from YAML file."""
    from generator.config import load_overrides

    overrides = load_overrides()

    assert "semantic_renames" in overrides
    assert "conflict_resolutions" in overrides
    assert overrides["semantic_renames"].get("Depth") == "OrderBook"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/generator/test_config.py -v`
Expected: FAIL with "cannot import name 'SPEC_PATHS' from 'generator.config'"

**Step 3: Create overrides.yaml**

```yaml
# generator/overrides.yaml
# Schema naming overrides - only for exceptions that smart inference can't handle
#
# semantic_renames: Map inferred names to better names
# conflict_resolutions: Resolve when multiple schemas map to same name

semantic_renames:
  # Business domain naming
  Depth: OrderBook
  AvgPrice: AveragePrice

conflict_resolutions:
  # When GetOrderV3Resp and PostOrderV3Resp both map to "Order"
  # Keep GetOrderV3Resp -> Order, rename the other
  PostOrderV3Resp: OrderResponse

  # Trade conflicts
  GetMyTradesV3Resp: MyTrade
  GetTradesV3Resp: PublicTrade

  # Account info variations
  GetAccountInfoV3Resp: AccountInfo
```

**Step 4: Implement generator config**

```python
# generator/config.py
"""Generator configuration and naming rules."""
import re
from pathlib import Path
from typing import Any

import yaml

# ============ Paths ============

PROJECT_ROOT = Path(__file__).parent.parent

SPEC_PATHS: dict[str, Path] = {
    "spot": PROJECT_ROOT / "specs" / "openapi" / "spot",
    "umfutures": PROJECT_ROOT / "specs" / "openapi" / "umfutures",
    "cmfutures": PROJECT_ROOT / "specs" / "openapi" / "cmfutures",
}

OUTPUT_PATHS: dict[str, Path] = {
    "api": PROJECT_ROOT / "binance" / "api",
    "schemas": PROJECT_ROOT / "binance" / "_schemas",
    "meta": PROJECT_ROOT / "binance" / "_meta",
}

TEMPLATE_DIR = Path(__file__).parent / "templates"
OVERRIDES_FILE = Path(__file__).parent / "overrides.yaml"

# ============ Type Mapping ============

TYPE_MAP: dict[tuple[str, str | None], str] = {
    ("string", None): "str",
    ("string", "int64"): "str",  # Some specs incorrectly mark strings as int64
    ("integer", None): "int",
    ("integer", "int32"): "int",
    ("integer", "int64"): "int",
    ("number", None): "float",
    ("number", "float"): "float",
    ("number", "double"): "float",
    ("boolean", None): "bool",
    ("array", None): "list",
    ("object", None): "dict",
}

# ============ Override Loading ============

_OVERRIDES_CACHE: dict[str, Any] | None = None


def load_overrides() -> dict[str, Any]:
    """Load naming overrides from YAML file.

    Returns:
        Dict with 'semantic_renames' and 'conflict_resolutions' keys
    """
    global _OVERRIDES_CACHE
    if _OVERRIDES_CACHE is not None:
        return _OVERRIDES_CACHE

    if OVERRIDES_FILE.exists():
        with open(OVERRIDES_FILE, "r") as f:
            _OVERRIDES_CACHE = yaml.safe_load(f) or {}
    else:
        _OVERRIDES_CACHE = {}

    # Ensure required keys exist
    _OVERRIDES_CACHE.setdefault("semantic_renames", {})
    _OVERRIDES_CACHE.setdefault("conflict_resolutions", {})

    return _OVERRIDES_CACHE


# ============ Naming Conventions ============

VERSION_SUFFIXES = re.compile(r"V\d+$")
RESP_SUFFIXES = re.compile(r"(Resp|Response|Result)$")
REQ_SUFFIXES = re.compile(r"(Req|Request)$")
PREFIX_PATTERNS = re.compile(r"^(Spot|Futures|Get|Post|Delete|Put)")

# Irregular plurals that need special handling
IRREGULAR_PLURALS: dict[str, str] = {
    "Indices": "Index",
    "Statuses": "Status",
}


def to_snake_case(name: str) -> str:
    """Convert camelCase or PascalCase to snake_case.

    Args:
        name: Input string in camelCase or PascalCase

    Returns:
        String converted to snake_case
    """
    # Handle consecutive uppercase (e.g., HTTPClient -> http_client)
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.lower()


def to_singular(name: str) -> str:
    """Convert plural noun to singular.

    Args:
        name: Potentially plural noun

    Returns:
        Singular form
    """
    # Check irregular plurals first
    if name in IRREGULAR_PLURALS:
        return IRREGULAR_PLURALS[name]

    # Don't change words ending in 'ss' (Address, Class, etc.)
    if name.endswith("ss"):
        return name

    # Don't change words ending in 'us' (Status, etc.)
    if name.endswith("us"):
        return name

    # Simple 's' suffix removal for common cases
    if name.endswith("s") and len(name) > 3:
        # Check it's likely a plural (e.g., Trades, Klines, Orders)
        # but not a word that naturally ends in 's' (e.g., Status)
        return name[:-1]

    return name


def to_method_name(operation_id: str) -> str:
    """Convert operationId to Python method name.

    Examples:
        GetKlinesV3 -> get_klines
        CreateOrderV3 -> create_order

    Args:
        operation_id: OpenAPI operationId

    Returns:
        Python method name in snake_case
    """
    # Remove version suffix (V3, V1, etc.)
    name = VERSION_SUFFIXES.sub("", operation_id)
    return to_snake_case(name)


def to_class_name(
    schema_name: str,
    overrides: dict[str, Any] | None = None,
) -> str:
    """Convert schema name to clean Python class name.

    Uses smart inference with optional overrides for exceptions.

    Strategy:
    1. Check conflict_resolutions override (exact match)
    2. Strip prefixes (Spot, Futures, Get, Post, Delete, Put)
    3. Strip suffixes (V3, Resp, Response, Request)
    4. Convert plural to singular
    5. Check semantic_renames override
    6. Fallback to original if result is empty

    Args:
        schema_name: OpenAPI schema name
        overrides: Optional override dict (loaded automatically if None)

    Returns:
        Clean Python class name
    """
    if overrides is None:
        overrides = load_overrides()

    # Step 1: Check for explicit conflict resolution
    conflict_resolutions = overrides.get("conflict_resolutions", {})
    if schema_name in conflict_resolutions:
        return conflict_resolutions[schema_name]

    # Step 2: Strip common prefixes
    name = PREFIX_PATTERNS.sub("", schema_name)

    # Step 3: Strip version suffix
    name = VERSION_SUFFIXES.sub("", name)

    # Step 4: Strip response/request suffixes
    name = RESP_SUFFIXES.sub("", name)
    name = REQ_SUFFIXES.sub("", name)

    # Step 5: Fallback if we stripped too much
    if not name or len(name) < 2:
        return schema_name  # Return original to avoid empty/useless names

    # Step 6: Check semantic renames
    semantic_renames = overrides.get("semantic_renames", {})
    if name in semantic_renames:
        return semantic_renames[name]

    # Step 7: Convert plural to singular
    name = to_singular(name)

    return name


def detect_naming_conflicts(
    mappings: dict[str, str],
) -> dict[str, list[str]]:
    """Detect when multiple schemas map to the same class name.

    Args:
        mappings: Dict of original_name -> class_name

    Returns:
        Dict of class_name -> list of original names that conflict
    """
    reverse: dict[str, list[str]] = {}
    for original, clean in mappings.items():
        reverse.setdefault(clean, []).append(original)

    # Return only actual conflicts (more than one mapping)
    return {clean: originals for clean, originals in reverse.items() if len(originals) > 1}


# ============ Endpoint Grouping ============

# Map path prefixes to module names
PATH_TO_MODULE: dict[str, str] = {
    "/api/v3/ping": "general",
    "/api/v3/time": "general",
    "/api/v3/exchangeInfo": "general",
    "/api/v3/depth": "market",
    "/api/v3/trades": "market",
    "/api/v3/historicalTrades": "market",
    "/api/v3/aggTrades": "market",
    "/api/v3/klines": "market",
    "/api/v3/uiKlines": "market",
    "/api/v3/avgPrice": "market",
    "/api/v3/ticker": "market",
    "/api/v3/order": "trade",
    "/api/v3/openOrders": "trade",
    "/api/v3/allOrders": "trade",
    "/api/v3/orderList": "trade",
    "/api/v3/account": "account",
    "/api/v3/myTrades": "account",
    "/api/v3/myAllocations": "account",
    "/api/v3/myPreventedMatches": "account",
    "/api/v3/rateLimit/order": "account",
}


def get_module_for_path(path: str) -> str:
    """Determine which module an endpoint belongs to.

    Args:
        path: API endpoint path

    Returns:
        Module name (general, market, trade, account, or other)
    """
    # Check exact matches first
    if path in PATH_TO_MODULE:
        return PATH_TO_MODULE[path]

    # Check prefix matches
    for prefix, module in PATH_TO_MODULE.items():
        if path.startswith(prefix):
            return module

    # Default to 'other' for sapi endpoints
    if "/sapi/" in path:
        return "other"

    return "other"
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/unit/generator/test_config.py -v`
Expected: PASS

**Step 6: Run mypy**

Run: `mypy generator/config.py --strict`
Expected: Success

**Step 7: Commit**

```bash
git add generator/config.py generator/overrides.yaml tests/unit/generator/test_config.py
git commit -m "feat: implement generator config with smart naming and overrides"
```

---

## Task 4: Implement Generator Models

**Files:**
- Modify: `generator/models.py`
- Create: `tests/unit/generator/test_models.py`

**Step 1: Write the failing test**

```python
# tests/unit/generator/test_models.py
from generator.models import (
    Parameter,
    Schema,
    Property,
    Endpoint,
    ParsedSpec,
)


def test_parameter_creation():
    """Test Parameter dataclass."""
    param = Parameter(
        name="symbol",
        py_name="symbol",
        type="str",
        required=True,
        default=None,
        description="Trading pair symbol",
    )
    assert param.name == "symbol"
    assert param.required is True


def test_parameter_optional():
    """Test optional Parameter with default."""
    param = Parameter(
        name="limit",
        py_name="limit",
        type="int",
        required=False,
        default=500,
        description="Max results",
    )
    assert param.required is False
    assert param.default == 500


def test_property_creation():
    """Test Property dataclass for schema fields."""
    prop = Property(
        name="orderId",
        py_name="order_id",
        type="int",
        required=True,
    )
    assert prop.name == "orderId"
    assert prop.py_name == "order_id"


def test_schema_creation():
    """Test Schema dataclass."""
    schema = Schema(
        name="Order",
        original_name="SpotCreateOrderV3Resp",
        properties=[
            Property(name="orderId", py_name="order_id", type="int", required=True),
            Property(name="symbol", py_name="symbol", type="str", required=True),
        ],
        is_array=False,
    )
    assert schema.name == "Order"
    assert len(schema.properties) == 2


def test_schema_with_raw_type():
    """Test Schema with raw_type for complex arrays like klines."""
    schema = Schema(
        name="Kline",
        original_name="GetKlinesV3Resp",
        properties=[],  # Raw arrays don't have properties
        is_array=True,
        raw_type="list[list[int | str]]",
    )
    assert schema.is_array is True
    assert schema.raw_type == "list[list[int | str]]"


def test_endpoint_creation():
    """Test Endpoint dataclass."""
    endpoint = Endpoint(
        operation_id="GetKlinesV3",
        method_name="get_klines",
        http_method="GET",
        path="/api/v3/klines",
        parameters=[
            Parameter(name="symbol", py_name="symbol", type="str", required=True, default=None, description=""),
        ],
        response_schema="Kline",
        is_array_response=True,
        requires_signature=False,
        description="Get kline data",
        module="market",
    )
    assert endpoint.method_name == "get_klines"
    assert endpoint.requires_signature is False


def test_endpoint_signed():
    """Test signed Endpoint."""
    endpoint = Endpoint(
        operation_id="CreateOrderV3",
        method_name="create_order",
        http_method="POST",
        path="/api/v3/order",
        parameters=[],
        response_schema="Order",
        is_array_response=False,
        requires_signature=True,
        description="Create new order",
        module="trade",
    )
    assert endpoint.requires_signature is True


def test_parsed_spec():
    """Test ParsedSpec container."""
    spec = ParsedSpec(
        name="spot",
        endpoints=[],
        schemas={},
    )
    assert spec.name == "spot"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/generator/test_models.py -v`
Expected: FAIL with "cannot import name 'Parameter' from 'generator.models'"

**Step 3: Implement generator models**

```python
# generator/models.py
"""Internal data models for parsed OpenAPI specs.

These dataclasses represent the parsed OpenAPI spec in a form
that's easy to use with Jinja2 templates.
"""
from dataclasses import dataclass, field


@dataclass
class Parameter:
    """Represents an endpoint parameter (query, path, body)."""

    name: str  # Original name from spec (camelCase)
    py_name: str  # Python name (snake_case)
    type: str  # Python type annotation
    required: bool
    default: str | int | float | bool | None
    description: str
    enum: list[str] | None = None


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
    ERROR = "error"      # Serious issue, but continue processing


@dataclass
class ParseError:
    """Represents a parsing error or warning."""

    file: Path
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
        return sum(1 for e in self.errors if e.severity == ParseErrorSeverity.WARNING)

    @property
    def error_count(self) -> int:
        return sum(1 for e in self.errors if e.severity == ParseErrorSeverity.ERROR)
```

Also add to imports at top of models.py:
```python
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/unit/generator/test_models.py -v`
Expected: PASS

**Step 5: Run mypy**

Run: `mypy generator/models.py --strict`
Expected: Success

**Step 6: Commit**

```bash
git add generator/models.py tests/unit/generator/test_models.py
git commit -m "feat: implement generator models (Parameter, Schema, Endpoint)"
```

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
    """Parse a single YAML file.

    Args:
        file_path: Path to YAML file

    Returns:
        Parsed YAML data as dict
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def extract_path_and_method(
    data: dict[str, Any],
) -> tuple[str, str, dict[str, Any]]:
    """Extract the endpoint path, HTTP method, and operation from spec data.

    Each spec file contains exactly one path with one method.

    Args:
        data: Parsed YAML data

    Returns:
        Tuple of (path, method, operation_data)

    Raises:
        ValueError: If spec structure is unexpected
    """
    paths = data.get("paths", {})
    if not paths:
        raise ValueError("No paths found in spec")

    # Should be exactly one path
    path = next(iter(paths.keys()))
    methods = paths[path]

    # Should be exactly one method
    method = next(iter(methods.keys()))
    operation = methods[method]

    return path, method.upper(), operation


def is_signed_endpoint(operation: dict[str, Any]) -> bool:
    """Determine if endpoint requires signature.

    Signed endpoints have either:
    - A 'security' section with ApiKey
    - A required 'timestamp' parameter

    Args:
        operation: The operation data from spec

    Returns:
        True if endpoint requires signing
    """
    # Check for security section
    if "security" in operation:
        return True

    # Check for required timestamp parameter
    for param in operation.get("parameters", []):
        if param.get("name") == "timestamp" and param.get("required"):
            return True

    # Check requestBody for timestamp
    request_body = operation.get("requestBody", {})
    content = request_body.get("content", {})
    form_data = content.get("application/x-www-form-urlencoded", {})
    schema_ref = form_data.get("schema", {}).get("$ref", "")
    # If there's a request body schema, it likely has timestamp
    if schema_ref:
        return True

    return False
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/generator/test_parser.py -v`
Expected: PASS

**Step 5: Run mypy**

Run: `mypy generator/parser.py --strict`
Expected: Success

**Step 6: Commit**

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
Expected: FAIL with "cannot import name 'parse_parameter' from 'generator.parser'"

**Step 3: Implement parameter parsing**

```python
# Add to generator/parser.py

from generator.models import Parameter, Property, Schema, Endpoint
from generator.config import TYPE_MAP, to_snake_case


def parse_parameter(param_data: dict[str, Any]) -> Parameter:
    """Parse a single parameter definition.

    Args:
        param_data: Parameter data from spec

    Returns:
        Parsed Parameter model
    """
    name = param_data["name"]
    schema = param_data.get("schema", {})

    # Get type
    type_str = schema.get("type", "string")
    format_str = schema.get("format")
    py_type = TYPE_MAP.get((type_str, format_str), TYPE_MAP.get((type_str, None), "Any"))

    # Handle array type
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
    """Parse all parameters for an operation.

    Args:
        operation: Operation data from spec

    Returns:
        List of parsed Parameters
    """
    params = []
    for param_data in operation.get("parameters", []):
        # Skip timestamp - we add it automatically for signed endpoints
        if param_data.get("name") == "timestamp":
            continue
        params.append(parse_parameter(param_data))

    # Sort: required params first, then optional
    params.sort(key=lambda p: (not p.required, p.name))

    return params
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/generator/test_parser.py -v`
Expected: PASS

**Step 5: Run mypy**

Run: `mypy generator/parser.py --strict`
Expected: Success

**Step 6: Commit**

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
# Klines: array of arrays with mixed types
type: array
items:
  type: array
  items:
    oneOf:
      - type: integer
      - type: string
```

This should resolve to: `list[list[int | str]]`

**Key patterns to support:**
| Pattern | Example | Python Type |
|---------|---------|-------------|
| Basic | `type: string` | `str` |
| Formatted | `type: integer, format: int64` | `int` |
| Reference | `$ref: '#/.../Order'` | `Order` |
| Array | `type: array, items: {type: string}` | `list[str]` |
| Nested array | `array → array → string` | `list[list[str]]` |
| Union (oneOf) | `oneOf: [{type: int}, {type: str}]` | `int \| str` |
| Complex | klines response | `list[list[int \| str]]` |

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

    # Simple array
    assert resolve_type({
        "type": "array",
        "items": {"type": "string"}
    }) == "list[str]"

    # Array with format
    assert resolve_type({
        "type": "array",
        "items": {"type": "integer", "format": "int64"}
    }) == "list[int]"


def test_resolve_type_nested_array():
    """Test resolving nested array types (like order book bids/asks)."""
    from generator.parser import resolve_type

    # list[list[str]] - like depth bids/asks
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

    # Actual klines schema: array of arrays with mixed int/str
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

    # Array of refs
    schema = {
        "type": "array",
        "items": {"$ref": "#/components/schemas/Trade"}
    }
    assert resolve_type(schema) == "list[Trade]"


def test_parse_property():
    """Test parsing a single schema property."""
    from generator.parser import parse_property

    prop_data = {
        "orderId": {"type": "integer", "format": "int64"}
    }
    required = ["orderId"]

    prop = parse_property("orderId", prop_data["orderId"], required)

    assert prop.name == "orderId"
    assert prop.py_name == "order_id"
    assert prop.type == "int"
    assert prop.required is True


def test_parse_property_array():
    """Test parsing array property."""
    from generator.parser import parse_property

    prop_data = {
        "type": "array",
        "items": {"type": "string"}
    }

    prop = parse_property("symbols", prop_data, [])

    assert prop.is_array is True
    assert prop.type == "list[str]"


def test_parse_property_nested_array():
    """Test parsing nested array property (like depth bids)."""
    from generator.parser import parse_property

    # Depth bids/asks are list[list[str]]
    prop_data = {
        "type": "array",
        "items": {
            "type": "array",
            "items": {"type": "string"}
        }
    }

    prop = parse_property("bids", prop_data, [])

    assert prop.type == "list[list[str]]"


def test_parse_schema():
    """Test parsing a schema definition."""
    from generator.parser import parse_schema

    schema_data = {
        "type": "object",
        "properties": {
            "orderId": {"type": "integer", "format": "int64"},
            "symbol": {"type": "string"},
        },
        "required": ["orderId", "symbol"]
    }

    schema = parse_schema("Order", "SpotCreateOrderV3Resp", schema_data)

    assert schema.name == "Order"
    assert len(schema.properties) == 2
    assert schema.is_array is False


def test_parse_schema_array():
    """Test parsing array schema."""
    from generator.parser import parse_schema

    schema_data = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "price": {"type": "string"},
                "qty": {"type": "string"},
            }
        }
    }

    schema = parse_schema("Trade", "GetTradesV3Resp", schema_data)

    assert schema.is_array is True


def test_parse_schema_klines():
    """Test parsing klines schema (raw array response)."""
    from generator.parser import parse_schema

    # Klines return raw array, not object
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
Expected: FAIL with "cannot import name 'resolve_type' from 'generator.parser'"

**Step 3: Implement recursive type resolution**

```python
# Add to generator/parser.py

def resolve_type(schema_data: dict[str, Any]) -> str:
    """Recursively resolve OpenAPI schema to Python type annotation.

    Handles:
    - Basic types (string, integer, boolean, number)
    - Arrays (including nested)
    - oneOf union types
    - $ref references

    Args:
        schema_data: OpenAPI schema definition

    Returns:
        Python type annotation string

    Examples:
        {"type": "string"} -> "str"
        {"type": "array", "items": {"type": "int"}} -> "list[int]"
        {"oneOf": [{"type": "int"}, {"type": "str"}]} -> "int | str"
    """
    # Handle $ref
    if "$ref" in schema_data:
        ref = schema_data["$ref"]
        return ref.split("/")[-1]

    # Handle oneOf union types
    if "oneOf" in schema_data:
        types = [resolve_type(option) for option in schema_data["oneOf"]]
        # Deduplicate while preserving order
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

    # Fallback
    return "Any"


def parse_property(
    name: str,
    prop_data: dict[str, Any],
    required_list: list[str],
) -> Property:
    """Parse a single schema property.

    Args:
        name: Property name
        prop_data: Property definition
        required_list: List of required property names

    Returns:
        Parsed Property model
    """
    py_type = resolve_type(prop_data)
    is_array = prop_data.get("type") == "array"

    # Extract ref type if present
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
    """Parse a schema definition.

    Args:
        clean_name: Clean Python class name
        original_name: Original name from spec
        schema_data: Schema definition data

    Returns:
        Parsed Schema model
    """
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
            # Inline object in array - parse properties
            required_list = items.get("required", [])
            for prop_name, prop_data in items.get("properties", {}).items():
                properties.append(parse_property(prop_name, prop_data, required_list))
        else:
            # Raw array type (like klines) - compute full type
            raw_type = resolve_type(schema_data)
    else:
        # Regular object
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
        raw_type=raw_type,  # New field for complex array types
    )
```

**Step 4: Update Schema model to include raw_type**

Add `raw_type` field to Schema in `generator/models.py`:

```python
@dataclass
class Schema:
    """Represents a response/request schema."""

    name: str
    original_name: str
    properties: list[Property]
    is_array: bool
    description: str = ""
    item_type: str | None = None  # For array of $ref
    raw_type: str | None = None   # For raw array types like list[list[int | str]]
```

**Step 5: Run tests to verify they pass**

Run: `pytest tests/unit/generator/test_parser.py -v`
Expected: PASS

**Step 6: Run mypy**

Run: `mypy generator/parser.py --strict`
Expected: Success

**Step 6: Commit**

```bash
git add generator/parser.py tests/unit/generator/test_parser.py
git commit -m "feat: implement schema parsing for generator"
```

---

## Task 8: Implement Endpoint Parsing with requestBody Support

**Files:**
- Modify: `generator/parser.py`
- Modify: `tests/unit/generator/test_parser.py`

**Design: requestBody Parameter Extraction**

POST/PUT/DELETE endpoints often define parameters in `requestBody` instead of `parameters`:

```yaml
# POST /api/v3/order
requestBody:
  content:
    application/x-www-form-urlencoded:
      schema:
        $ref: '#/components/schemas/SpotCreateOrderV3Req'
```

The parser needs to:
1. Extract parameters from `requestBody` schema
2. Dereference `$ref` to get the actual schema
3. Merge with query `parameters`
4. Skip `timestamp` (auto-added for signed requests)

**Step 1: Write the failing test**

```python
# Add to tests/unit/generator/test_parser.py
from pathlib import Path


def test_parse_endpoint():
    """Test parsing a complete endpoint."""
    from generator.parser import parse_endpoint

    data = {
        "components": {
            "schemas": {
                "GetKlinesV3Resp": {
                    "type": "array",
                    "items": {"type": "array", "items": {"oneOf": [{"type": "integer"}, {"type": "string"}]}}
                }
            }
        },
        "paths": {
            "/api/v3/klines": {
                "get": {
                    "operationId": "GetKlinesV3",
                    "description": "Get kline data",
                    "parameters": [
                        {"name": "symbol", "in": "query", "required": True, "schema": {"type": "string"}},
                        {"name": "interval", "in": "query", "required": True, "schema": {"type": "string"}},
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/GetKlinesV3Resp"}
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    endpoint, schemas = parse_endpoint(data)

    assert endpoint.method_name == "get_klines"
    assert endpoint.http_method == "GET"
    assert endpoint.requires_signature is False
    assert len(endpoint.parameters) == 2


def test_parse_signed_endpoint():
    """Test parsing a signed endpoint."""
    from generator.parser import parse_endpoint

    data = {
        "components": {
            "schemas": {
                "GetAccountV3Resp": {"type": "object", "properties": {}}
            },
            "securitySchemes": {"ApiKey": {"type": "apiKey"}}
        },
        "paths": {
            "/api/v3/account": {
                "get": {
                    "operationId": "GetAccountV3",
                    "description": "Get account info",
                    "security": [{"ApiKey": []}],
                    "parameters": [
                        {"name": "timestamp", "in": "query", "required": True, "schema": {"type": "integer"}},
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/GetAccountV3Resp"}
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    endpoint, schemas = parse_endpoint(data)

    assert endpoint.requires_signature is True
    # timestamp should be excluded from parameters
    assert len(endpoint.parameters) == 0


def test_parse_request_body():
    """Test parsing requestBody parameters (POST endpoints)."""
    from generator.parser import parse_request_body

    components = {
        "schemas": {
            "CreateOrderReq": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "default": ""},
                    "side": {"type": "string", "default": ""},
                    "type": {"type": "string", "default": ""},
                    "quantity": {"type": "string", "default": ""},
                    "price": {"type": "string", "default": ""},
                    "timestamp": {"type": "integer", "format": "int64"},
                },
                "required": ["symbol", "side", "type", "timestamp"]
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

    # Should have 5 params (timestamp excluded)
    assert len(params) == 5
    param_names = [p.name for p in params]
    assert "symbol" in param_names
    assert "side" in param_names
    assert "timestamp" not in param_names  # Auto-added, should be excluded

    # Check required/optional
    symbol_param = next(p for p in params if p.name == "symbol")
    assert symbol_param.required is True

    price_param = next(p for p in params if p.name == "price")
    assert price_param.required is False


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
                        "type": {"type": "string"},
                        "quantity": {"type": "string"},
                        "timestamp": {"type": "integer"},
                    },
                    "required": ["symbol", "side", "type", "timestamp"]
                },
                "CreateOrderResp": {
                    "type": "object",
                    "properties": {
                        "orderId": {"type": "integer"},
                        "symbol": {"type": "string"},
                    }
                }
            },
            "securitySchemes": {"ApiKey": {"type": "apiKey"}}
        },
        "paths": {
            "/api/v3/order": {
                "post": {
                    "operationId": "CreateOrderV3",
                    "description": "Create new order",
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

    # Should have body params (minus timestamp)
    assert len(endpoint.parameters) == 4  # symbol, side, type, quantity
    param_names = [p.name for p in endpoint.parameters]
    assert "symbol" in param_names
    assert "timestamp" not in param_names


def test_parse_endpoint_file():
    """Test parsing a real endpoint file."""
    from generator.parser import parse_endpoint_file

    spec_file = Path("specs/openapi/spot/get_api_v3_klines.yaml")
    if not spec_file.exists():
        pytest.skip("Spec file not found")

    endpoint, schemas = parse_endpoint_file(spec_file)

    assert endpoint.method_name == "get_klines"
    assert endpoint.path == "/api/v3/klines"


def test_parse_post_endpoint_file():
    """Test parsing a real POST endpoint file."""
    from generator.parser import parse_endpoint_file

    spec_file = Path("specs/openapi/spot/post_api_v3_order.yaml")
    if not spec_file.exists():
        pytest.skip("Spec file not found")

    endpoint, schemas = parse_endpoint_file(spec_file)

    assert endpoint.method_name == "create_order"
    assert endpoint.http_method == "POST"
    assert endpoint.requires_signature is True
    assert len(endpoint.parameters) > 0  # Should have parsed body params
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/generator/test_parser.py::test_parse_endpoint -v`
Expected: FAIL with "cannot import name 'parse_endpoint' from 'generator.parser'"

**Step 3: Implement endpoint parsing with requestBody support**

```python
# Add to generator/parser.py

from generator.config import to_method_name, to_class_name, get_module_for_path


def get_response_schema_ref(operation: dict[str, Any]) -> str | None:
    """Extract response schema reference from operation.

    Args:
        operation: Operation data

    Returns:
        Schema reference name or None
    """
    responses = operation.get("responses", {})
    success_response = responses.get("200", {})
    content = success_response.get("content", {})
    json_content = content.get("application/json", {})
    schema = json_content.get("schema", {})

    if "$ref" in schema:
        return schema["$ref"].split("/")[-1]

    # Check for inline array
    if schema.get("type") == "array":
        items = schema.get("items", {})
        if "$ref" in items:
            return items["$ref"].split("/")[-1]

    return None


def parse_request_body(
    operation: dict[str, Any],
    components: dict[str, Any],
) -> list[Parameter]:
    """Parse parameters from requestBody (for POST/PUT endpoints).

    Args:
        operation: Operation definition
        components: Spec's components section (for dereferencing)

    Returns:
        List of Parameters extracted from requestBody schema
    """
    request_body = operation.get("requestBody", {})
    if not request_body:
        return []

    content = request_body.get("content", {})
    # Support both form-urlencoded and json
    form_data = content.get("application/x-www-form-urlencoded", {})
    json_data = content.get("application/json", {})

    schema_data = form_data.get("schema", {}) or json_data.get("schema", {})
    if not schema_data:
        return []

    # Dereference $ref
    if "$ref" in schema_data:
        ref_name = schema_data["$ref"].split("/")[-1]
        schema_data = components.get("schemas", {}).get(ref_name, {})

    if not schema_data:
        return []

    # Parse properties as Parameters
    params: list[Parameter] = []
    required_list = schema_data.get("required", [])

    for prop_name, prop_data in schema_data.get("properties", {}).items():
        # Skip timestamp (auto-added for signed requests)
        if prop_name == "timestamp":
            continue
        # Skip signature (auto-added)
        if prop_name == "signature":
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
    """Parse a single endpoint file data.

    Args:
        data: Parsed YAML data

    Returns:
        Tuple of (Endpoint, dict of Schema)
    """
    path, method, operation = extract_path_and_method(data)

    # Parse schemas from components
    schemas: dict[str, Schema] = {}
    components = data.get("components", {})
    schema_defs = components.get("schemas", {})

    for schema_name, schema_data in schema_defs.items():
        # Skip APIError and Request schemas
        if schema_name == "APIError":
            continue
        if schema_name.endswith("Req"):
            continue  # Request schemas don't need to be emitted
        clean_name = to_class_name(schema_name)
        schemas[schema_name] = parse_schema(clean_name, schema_name, schema_data)

    # Get response schema reference
    response_ref = get_response_schema_ref(operation)
    response_schema: str | None = None
    is_array_response = False
    raw_response_type: str | None = None

    if response_ref and response_ref in schemas:
        schema = schemas[response_ref]
        response_schema = schema.name
        is_array_response = schema.is_array
        raw_response_type = schema.raw_type

    # Check for inline array response
    responses = operation.get("responses", {})
    success_response = responses.get("200", {})
    content = success_response.get("content", {})
    json_content = content.get("application/json", {})
    resp_schema = json_content.get("schema", {})
    if resp_schema.get("type") == "array" and not response_schema:
        is_array_response = True
        raw_response_type = resolve_type(resp_schema)

    # Merge query parameters and body parameters
    query_params = parse_parameters(operation)
    body_params = parse_request_body(operation, components)
    all_params = query_params + body_params

    # Sort: required params first, then by name
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
    """Parse a single endpoint YAML file.

    Args:
        file_path: Path to YAML file

    Returns:
        Tuple of (Endpoint, dict of Schema)
    """
    data = parse_yaml_file(file_path)
    return parse_endpoint(data)
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/generator/test_parser.py -v`
Expected: PASS

**Step 5: Run mypy**

Run: `mypy generator/parser.py --strict`
Expected: Success

**Step 6: Commit**

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

Instead of printing warnings and continuing silently, we collect all errors and warnings
into a structured `ParseResult`. This allows callers to:
- Decide how to handle errors (fail fast, continue, etc.)
- Generate summary reports
- Log errors consistently
- Detect naming conflicts with actionable guidance

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

    # Parse only first 5 files for speed
    result = parse_spec_directory(spec_dir, limit=5)

    # Result is a ParseResult containing spec and errors
    assert result.spec.name == "spot"
    assert len(result.spec.endpoints) <= 5
    assert len(result.spec.schemas) > 0
    # Can check errors
    assert isinstance(result.errors, list)


def test_deduplicate_schemas():
    """Test schema deduplication."""
    from generator.parser import deduplicate_schemas
    from generator.models import Schema, Property

    schemas_list = [
        {"OrderResp": Schema("Order", "OrderResp", [], False)},
        {"OrderResp": Schema("Order", "OrderResp", [], False)},  # Duplicate
        {"TradeResp": Schema("Trade", "TradeResp", [], False)},
    ]

    deduped = deduplicate_schemas(schemas_list)

    assert len(deduped) == 2
    assert "Order" in deduped
    assert "Trade" in deduped


def test_collect_schema_mappings():
    """Test collecting schema name mappings for conflict detection."""
    from generator.parser import collect_schema_mappings
    from generator.models import Schema

    schemas_list = [
        {"GetOrderV3Resp": Schema("Order", "GetOrderV3Resp", [], False)},
        {"PostOrderV3Resp": Schema("Order", "PostOrderV3Resp", [], False)},  # Conflict!
        {"GetTradesV3Resp": Schema("Trade", "GetTradesV3Resp", [], False)},
    ]

    mappings = collect_schema_mappings(schemas_list)

    assert mappings["GetOrderV3Resp"] == "Order"
    assert mappings["PostOrderV3Resp"] == "Order"
    assert mappings["GetTradesV3Resp"] == "Trade"


def test_parse_spec_directory_collects_errors():
    """Test that parsing collects errors into ParseResult."""
    from generator.parser import parse_spec_directory
    from generator.models import ParseErrorSeverity
    from generator.config import SPEC_PATHS

    spec_dir = SPEC_PATHS.get("spot")
    if not spec_dir or not spec_dir.exists():
        pytest.skip("Spec directory not found")

    # Parse enough files to potentially find conflicts
    result = parse_spec_directory(spec_dir, limit=50)

    # Errors should be collected, not printed
    assert isinstance(result.errors, list)
    # Check error structure if any exist
    for error in result.errors:
        assert hasattr(error, "file")
        assert hasattr(error, "severity")
        assert hasattr(error, "message")
        assert error.severity in (ParseErrorSeverity.WARNING, ParseErrorSeverity.ERROR)


def test_parse_spec_directory_detects_conflicts():
    """Test that naming conflicts are reported as warnings."""
    from generator.parser import parse_spec_directory
    from generator.models import ParseErrorSeverity
    from generator.config import SPEC_PATHS

    spec_dir = SPEC_PATHS.get("spot")
    if not spec_dir or not spec_dir.exists():
        pytest.skip("Spec directory not found")

    result = parse_spec_directory(spec_dir, limit=50)

    # Check for conflict warnings (may or may not exist)
    conflict_warnings = [
        e for e in result.errors
        if "conflict" in e.message.lower()
    ]
    # If conflicts exist, they should have actionable message
    for warning in conflict_warnings:
        assert "overrides.yaml" in warning.message


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
Expected: FAIL with "cannot import name 'parse_spec_directory' from 'generator.parser'"

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
    """Collect original -> clean name mappings from all schemas.

    Args:
        schemas_list: List of schema dicts from each endpoint

    Returns:
        Dict mapping original schema name to clean class name
    """
    mappings: dict[str, str] = {}
    for schemas in schemas_list:
        for original_name, schema in schemas.items():
            mappings[original_name] = schema.name
    return mappings


def deduplicate_schemas(
    schemas_list: list[dict[str, Schema]],
) -> dict[str, Schema]:
    """Deduplicate schemas from multiple endpoints.

    Schemas are deduplicated by their clean name. If multiple schemas
    have the same clean name, the one with more properties wins.

    Args:
        schemas_list: List of schema dicts from each endpoint

    Returns:
        Deduplicated dict mapping clean name to Schema
    """
    result: dict[str, Schema] = {}

    for schemas in schemas_list:
        for original_name, schema in schemas.items():
            clean_name = schema.name

            if clean_name not in result:
                result[clean_name] = schema
            elif len(schema.properties) > len(result[clean_name].properties):
                # Keep the schema with more properties
                result[clean_name] = schema

    return result


def create_conflict_errors(
    conflicts: dict[str, list[str]],
) -> list[ParseError]:
    """Create ParseError objects for naming conflicts.

    Args:
        conflicts: Dict of clean_name -> list of original names that conflict

    Returns:
        List of ParseError warnings with actionable guidance
    """
    errors: list[ParseError] = []

    for clean_name, originals in sorted(conflicts.items()):
        # Build actionable message
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
            file=Path("generator/overrides.yaml"),  # Where to fix
            severity=ParseErrorSeverity.WARNING,
            message=message,
        ))

    return errors


def parse_spec_directory(
    spec_dir: Path,
    limit: int | None = None,
) -> ParseResult:
    """Parse all endpoint files in a spec directory.

    Args:
        spec_dir: Directory containing endpoint YAML files
        limit: Optional limit on number of files to parse (for testing)

    Returns:
        ParseResult containing spec and any errors/warnings
    """
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
            # Collect error instead of printing
            errors.append(ParseError(
                file=yaml_file,
                severity=ParseErrorSeverity.WARNING,
                message=f"Failed to parse: {e}",
                exception=e,
            ))
            continue

    # Check for naming conflicts before deduplication
    mappings = collect_schema_mappings(all_schemas)
    conflicts = detect_naming_conflicts(mappings)
    errors.extend(create_conflict_errors(conflicts))

    # Deduplicate schemas
    deduped_schemas = deduplicate_schemas(all_schemas)

    spec = ParsedSpec(
        name=name,
        endpoints=endpoints,
        schemas=deduped_schemas,
    )

    return ParseResult(spec=spec, errors=errors)


def report_parse_result(result: ParseResult) -> None:
    """Print a summary report of parse results.

    Args:
        result: ParseResult from parse_spec_directory
    """
    print(f"Parsed {len(result.spec.endpoints)} endpoints, "
          f"{len(result.spec.schemas)} schemas")

    if not result.errors:
        print("No errors or warnings.")
        return

    print(f"\n{result.warning_count} warnings, {result.error_count} errors:\n")

    for error in result.errors:
        prefix = "⚠️ " if error.severity == ParseErrorSeverity.WARNING else "❌ "
        print(f"{prefix}[{error.file}] {error.message}")

    if result.has_errors:
        print("\n❌ Parsing completed with errors.")
    else:
        print("\n✓ Parsing completed with warnings.")
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/generator/test_parser.py -v`
Expected: PASS

**Step 5: Run mypy**

Run: `mypy generator/parser.py --strict`
Expected: Success

**Step 6: Commit**

```bash
git add generator/parser.py tests/unit/generator/test_parser.py
git commit -m "feat: implement directory parser with structured error handling

- Return ParseResult with errors list instead of printing
- Collect parse failures as ParseError with severity
- Detect naming conflicts and report with actionable guidance
- Add report_parse_result() for summary output"
```

---

## Task 10: Create Jinja2 Templates - Schema Template

**Files:**
- Create: `generator/templates/schema.py.j2`
- Create: `tests/unit/generator/test_templates.py`

**Step 1: Write the failing test**

```python
# tests/unit/generator/test_templates.py
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader


def get_template_env() -> Environment:
    """Create Jinja2 environment with template directory."""
    template_dir = Path(__file__).parent.parent.parent.parent / "generator" / "templates"
    env = Environment(
        loader=FileSystemLoader(template_dir),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    # Register custom filters
    env.filters["repr"] = repr
    return env


def test_schema_template_exists():
    """Test that schema template exists."""
    template_dir = Path(__file__).parent.parent.parent.parent / "generator" / "templates"
    assert (template_dir / "schema.py.j2").exists()


def test_schema_template_renders():
    """Test rendering schema template."""
    from generator.models import Schema, Property

    env = get_template_env()
    template = env.get_template("schema.py.j2")

    schemas = [
        Schema(
            name="Order",
            original_name="SpotCreateOrderV3Resp",
            properties=[
                Property(name="orderId", py_name="order_id", type="int", required=True),
                Property(name="symbol", py_name="symbol", type="str", required=True),
                Property(name="status", py_name="status", type="str", required=False),
            ],
            is_array=False,
        )
    ]

    output = template.render(schemas=schemas, module_name="spot")

    assert "class Order(BaseStruct):" in output
    assert "order_id: int" in output
    assert "symbol: str" in output
    assert "status: str | None = None" in output
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/generator/test_templates.py -v`
Expected: FAIL with "schema.py.j2" does not exist

**Step 3: Create templates directory and schema template**

```bash
mkdir -p generator/templates
```

```jinja2
{# generator/templates/schema.py.j2 #}
"""Generated schema definitions for {{ module_name }} API.

DO NOT EDIT - This file is auto-generated by the code generator.
"""
from binance._schemas.common import BaseStruct


{% for schema in schemas %}
class {{ schema.name }}(BaseStruct):
    """{{ schema.description or schema.original_name }}"""
    {% if schema.is_array and schema.item_type %}
    # Note: This schema represents an array of {{ schema.item_type }}
    {% endif %}

    {% for prop in schema.properties %}
    {% if prop.required %}
    {{ prop.py_name }}: {{ prop.type }}
    {% else %}
    {{ prop.py_name }}: {{ prop.type }} | None = None
    {% endif %}
    {% endfor %}
    {% if not schema.properties %}
    pass
    {% endif %}


{% endfor %}
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/unit/generator/test_templates.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add generator/templates/ tests/unit/generator/test_templates.py
git commit -m "feat: add schema Jinja2 template"
```

---

## Task 11: Create Jinja2 Templates - Endpoint Template

**Files:**
- Create: `generator/templates/endpoint.py.j2`
- Modify: `tests/unit/generator/test_templates.py`

**Design: Schema Import Generation**

The template needs to import schema classes used in return type annotations:

```python
# Generated market.py
from binance._schemas.spot import Kline, Trade, OrderBook  # ← Must generate this!

async def get_klines(...) -> list[Kline]:
    ...
```

The emitter will collect all unique schema names from endpoints and pass them to the template as `schema_imports`.

**Step 1: Write the failing test**

```python
# Add to tests/unit/generator/test_templates.py

def test_endpoint_template_exists():
    """Test that endpoint template exists."""
    template_dir = Path(__file__).parent.parent.parent.parent / "generator" / "templates"
    assert (template_dir / "endpoint.py.j2").exists()


def test_endpoint_template_renders():
    """Test rendering endpoint template."""
    from generator.models import Endpoint, Parameter

    env = get_template_env()
    template = env.get_template("endpoint.py.j2")

    endpoints = [
        Endpoint(
            operation_id="GetKlinesV3",
            method_name="get_klines",
            http_method="GET",
            path="/api/v3/klines",
            parameters=[
                Parameter(name="symbol", py_name="symbol", type="str", required=True, default=None, description=""),
                Parameter(name="interval", py_name="interval", type="str", required=True, default=None, description=""),
                Parameter(name="limit", py_name="limit", type="int", required=False, default=500, description=""),
            ],
            response_schema="Kline",
            is_array_response=True,
            requires_signature=False,
            description="Get kline data",
            module="market",
        )
    ]

    output = template.render(
        endpoints=endpoints,
        module_name="market",
        spec_name="spot",
        schema_imports=["Kline"],  # Schema imports passed by emitter
    )

    assert "async def get_klines(" in output
    assert "symbol: str" in output
    assert "interval: str" in output
    assert "limit: int = 500" in output


def test_endpoint_template_generates_imports():
    """Test that endpoint template generates schema import statements."""
    from generator.models import Endpoint, Parameter

    env = get_template_env()
    template = env.get_template("endpoint.py.j2")

    endpoints = [
        Endpoint(
            operation_id="GetKlinesV3",
            method_name="get_klines",
            http_method="GET",
            path="/api/v3/klines",
            parameters=[],
            response_schema="Kline",
            is_array_response=True,
            requires_signature=False,
            description="Get klines",
            module="market",
        ),
        Endpoint(
            operation_id="GetTradesV3",
            method_name="get_trades",
            http_method="GET",
            path="/api/v3/trades",
            parameters=[],
            response_schema="Trade",
            is_array_response=True,
            requires_signature=False,
            description="Get trades",
            module="market",
        ),
    ]

    output = template.render(
        endpoints=endpoints,
        module_name="market",
        spec_name="spot",
        schema_imports=["Kline", "Trade"],
    )

    # Check import statement is generated
    assert "from binance._schemas.spot import Kline, Trade" in output


def test_endpoint_template_no_imports_for_raw_types():
    """Test that raw types (like list[list[int | str]]) don't generate imports."""
    from generator.models import Endpoint, Parameter

    env = get_template_env()
    template = env.get_template("endpoint.py.j2")

    endpoints = [
        Endpoint(
            operation_id="GetKlinesV3",
            method_name="get_klines",
            http_method="GET",
            path="/api/v3/klines",
            parameters=[],
            response_schema=None,  # No schema, using raw_response_type
            raw_response_type="list[list[int | str]]",  # Raw type
            is_array_response=True,
            requires_signature=False,
            description="Get klines",
            module="market",
        ),
    ]

    output = template.render(
        endpoints=endpoints,
        module_name="market",
        spec_name="spot",
        schema_imports=[],  # No schemas to import
    )

    # Should not have schema import line (or empty import)
    assert "from binance._schemas" not in output or "import " not in output.split("from binance._schemas")[1].split("\n")[0]


def test_endpoint_template_signed():
    """Test rendering signed endpoint."""
    from generator.models import Endpoint, Parameter

    env = get_template_env()
    template = env.get_template("endpoint.py.j2")

    endpoints = [
        Endpoint(
            operation_id="GetAccountV3",
            method_name="get_account",
            http_method="GET",
            path="/api/v3/account",
            parameters=[],
            response_schema="Account",
            is_array_response=False,
            requires_signature=True,
            description="Get account info",
            module="account",
        )
    ]

    output = template.render(
        endpoints=endpoints,
        module_name="account",
        spec_name="spot",
        schema_imports=["Account"],
    )

    assert "signed=True" in output
    assert "from binance._schemas.spot import Account" in output
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/generator/test_templates.py::test_endpoint_template_exists -v`
Expected: FAIL

**Step 3: Create endpoint template**

```jinja2
{# generator/templates/endpoint.py.j2 #}
"""Generated {{ module_name }} API endpoints.

DO NOT EDIT - This file is auto-generated by the code generator.
"""
from typing import TYPE_CHECKING, Any
{% if schema_imports %}

from binance._schemas.{{ spec_name }} import {{ schema_imports | join(", ") }}
{% endif %}

if TYPE_CHECKING:
    from binance._core.http import HTTPClient

{% for endpoint in endpoints %}

async def {{ endpoint.method_name }}(
    client: "HTTPClient",
    {% for param in endpoint.parameters %}
    {% if param.required %}
    {{ param.py_name }}: {{ param.type }},
    {% endif %}
    {% endfor %}
    {% for param in endpoint.parameters %}
    {% if not param.required %}
    {{ param.py_name }}: {{ param.type }} | None = {% if param.default is not none %}{{ param.default | repr }}{% else %}None{% endif %},
    {% endif %}
    {% endfor %}
) -> {% if endpoint.raw_response_type %}{{ endpoint.raw_response_type }}{% elif endpoint.response_schema %}{% if endpoint.is_array_response %}list[{{ endpoint.response_schema }}]{% else %}{{ endpoint.response_schema }}{% endif %}{% else %}dict[str, Any]{% endif %}:
    """{{ endpoint.description }}
    {% if endpoint.parameters %}

    Args:
    {% for param in endpoint.parameters %}
        {{ param.py_name }}: {{ param.description or param.name }}
    {% endfor %}
    {% endif %}
    """
    params: dict[str, str | int | float | bool] = {}
    {% for param in endpoint.parameters %}
    {% if param.required %}
    params["{{ param.name }}"] = {{ param.py_name }}
    {% else %}
    if {{ param.py_name }} is not None:
        params["{{ param.name }}"] = {{ param.py_name }}
    {% endif %}
    {% endfor %}

    return await client.request(
        "{{ endpoint.http_method }}",
        "{{ endpoint.path }}",
        {% if endpoint.requires_signature %}signed=True,{% endif %}
        params=params if params else None,
    )

{% endfor %}
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/generator/test_templates.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add generator/templates/endpoint.py.j2 tests/unit/generator/test_templates.py
git commit -m "feat: add endpoint Jinja2 template with schema imports"
```

---

## Task 12: Implement Emitter

**Files:**
- Modify: `generator/emitter.py`
- Create: `tests/unit/generator/test_emitter.py`

**Design: Schema Import Collection**

The emitter needs to collect all schema types used in endpoint return types and pass them to the template for import generation:

```python
# Collect schema imports
endpoints = [get_klines() -> list[Kline], get_trades() -> list[Trade]]
schema_imports = collect_schema_imports(endpoints)  # ["Kline", "Trade"]

# Pass to template
template.render(endpoints=endpoints, schema_imports=schema_imports, spec_name="spot")
```

**Step 1: Write the failing test**

```python
# tests/unit/generator/test_emitter.py
from pathlib import Path
import tempfile

from generator.models import Schema, Property, Endpoint, Parameter, ParsedSpec


def test_collect_schema_imports():
    """Test collecting schema imports from endpoints."""
    from generator.emitter import collect_schema_imports

    endpoints = [
        Endpoint(
            operation_id="GetKlinesV3",
            method_name="get_klines",
            http_method="GET",
            path="/api/v3/klines",
            parameters=[],
            response_schema="Kline",
            is_array_response=True,
            requires_signature=False,
            description="",
            module="market",
        ),
        Endpoint(
            operation_id="GetTradesV3",
            method_name="get_trades",
            http_method="GET",
            path="/api/v3/trades",
            parameters=[],
            response_schema="Trade",
            is_array_response=True,
            requires_signature=False,
            description="",
            module="market",
        ),
        Endpoint(
            operation_id="GetDepthV3",
            method_name="get_depth",
            http_method="GET",
            path="/api/v3/depth",
            parameters=[],
            response_schema=None,  # Raw type, no schema
            raw_response_type="list[list[str]]",
            is_array_response=True,
            requires_signature=False,
            description="",
            module="market",
        ),
    ]

    imports = collect_schema_imports(endpoints)

    assert "Kline" in imports
    assert "Trade" in imports
    assert len(imports) == 2  # No import for raw_response_type


def test_collect_schema_imports_deduplicates():
    """Test that schema imports are deduplicated."""
    from generator.emitter import collect_schema_imports

    endpoints = [
        Endpoint(
            operation_id="GetOrderV3",
            method_name="get_order",
            http_method="GET",
            path="/api/v3/order",
            parameters=[],
            response_schema="Order",
            is_array_response=False,
            requires_signature=True,
            description="",
            module="trade",
        ),
        Endpoint(
            operation_id="PostOrderV3",
            method_name="create_order",
            http_method="POST",
            path="/api/v3/order",
            parameters=[],
            response_schema="Order",  # Same schema
            is_array_response=False,
            requires_signature=True,
            description="",
            module="trade",
        ),
    ]

    imports = collect_schema_imports(endpoints)

    assert imports == ["Order"]  # Deduplicated


def test_emit_schemas():
    """Test emitting schema file."""
    from generator.emitter import emit_schemas

    schemas = {
        "Order": Schema(
            name="Order",
            original_name="SpotCreateOrderV3Resp",
            properties=[
                Property(name="orderId", py_name="order_id", type="int", required=True),
            ],
            is_array=False,
        )
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "spot.py"
        emit_schemas(schemas, output_path, "spot")

        content = output_path.read_text()
        assert "class Order(BaseStruct):" in content


def test_emit_endpoints():
    """Test emitting endpoint file with schema imports."""
    from generator.emitter import emit_endpoints

    endpoints = [
        Endpoint(
            operation_id="GetKlinesV3",
            method_name="get_klines",
            http_method="GET",
            path="/api/v3/klines",
            parameters=[
                Parameter(name="symbol", py_name="symbol", type="str", required=True, default=None, description=""),
            ],
            response_schema="Kline",
            is_array_response=True,
            requires_signature=False,
            description="Get klines",
            module="market",
        )
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "market.py"
        emit_endpoints(endpoints, output_path, "market", "spot")

        content = output_path.read_text()
        assert "async def get_klines(" in content
        assert "from binance._schemas.spot import Kline" in content


def test_emit_endpoints_with_raw_type():
    """Test emitting endpoint with raw_response_type (no schema import)."""
    from generator.emitter import emit_endpoints

    endpoints = [
        Endpoint(
            operation_id="GetKlinesV3",
            method_name="get_klines",
            http_method="GET",
            path="/api/v3/klines",
            parameters=[],
            response_schema=None,
            raw_response_type="list[list[int | str]]",
            is_array_response=True,
            requires_signature=False,
            description="Get klines",
            module="market",
        )
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "market.py"
        emit_endpoints(endpoints, output_path, "market", "spot")

        content = output_path.read_text()
        assert "-> list[list[int | str]]" in content
        # Should not have empty import
        assert "from binance._schemas.spot import \n" not in content


def test_emit_spec():
    """Test emitting all files for a parsed spec."""
    from generator.emitter import emit_spec

    spec = ParsedSpec(
        name="spot",
        endpoints=[
            Endpoint(
                operation_id="GetKlinesV3",
                method_name="get_klines",
                http_method="GET",
                path="/api/v3/klines",
                parameters=[],
                response_schema="Kline",
                is_array_response=True,
                requires_signature=False,
                description="Get klines",
                module="market",
            )
        ],
        schemas={
            "Kline": Schema(
                name="Kline",
                original_name="GetKlinesV3Resp",
                properties=[],
                is_array=True,
            )
        },
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        api_dir = Path(tmpdir) / "api"
        schemas_dir = Path(tmpdir) / "schemas"

        emit_spec(spec, api_dir, schemas_dir)

        assert (api_dir / "spot" / "market.py").exists()
        assert (schemas_dir / "spot.py").exists()

        # Verify import is in generated file
        market_content = (api_dir / "spot" / "market.py").read_text()
        assert "from binance._schemas.spot import Kline" in market_content
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/generator/test_emitter.py -v`
Expected: FAIL with "cannot import name 'emit_schemas' from 'generator.emitter'"

**Step 3: Implement emitter**

```python
# generator/emitter.py
"""Emit Python code from internal models using templates."""
from pathlib import Path
from collections import defaultdict

from jinja2 import Environment, FileSystemLoader

from generator.models import Schema, Endpoint, ParsedSpec
from generator.config import TEMPLATE_DIR


def get_template_env() -> Environment:
    """Create Jinja2 environment with custom filters."""
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    # Register custom filters - Jinja2 doesn't have repr by default
    env.filters["repr"] = repr
    return env


def collect_schema_imports(endpoints: list[Endpoint]) -> list[str]:
    """Collect unique schema names used in endpoint return types.

    Args:
        endpoints: List of endpoints to scan

    Returns:
        Sorted list of unique schema names to import
    """
    schemas: set[str] = set()
    for endpoint in endpoints:
        if endpoint.response_schema:
            schemas.add(endpoint.response_schema)
    return sorted(schemas)


def emit_schemas(
    schemas: dict[str, Schema],
    output_path: Path,
    module_name: str,
) -> None:
    """Emit schema definitions to a Python file.

    Args:
        schemas: Dict of schema name to Schema
        output_path: Path to write output
        module_name: Module name for header
    """
    env = get_template_env()
    template = env.get_template("schema.py.j2")

    # Sort schemas by name for consistent output
    sorted_schemas = sorted(schemas.values(), key=lambda s: s.name)

    content = template.render(schemas=sorted_schemas, module_name=module_name)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content)


def emit_endpoints(
    endpoints: list[Endpoint],
    output_path: Path,
    module_name: str,
    spec_name: str,
) -> None:
    """Emit endpoint functions to a Python file.

    Args:
        endpoints: List of Endpoint models
        output_path: Path to write output
        module_name: Module name for header (e.g., "market")
        spec_name: Spec name for schema imports (e.g., "spot")
    """
    env = get_template_env()
    template = env.get_template("endpoint.py.j2")

    # Sort endpoints by method name for consistent output
    sorted_endpoints = sorted(endpoints, key=lambda e: e.method_name)

    # Collect schema imports
    schema_imports = collect_schema_imports(sorted_endpoints)

    content = template.render(
        endpoints=sorted_endpoints,
        module_name=module_name,
        spec_name=spec_name,
        schema_imports=schema_imports,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content)


def emit_spec(
    spec: ParsedSpec,
    api_dir: Path,
    schemas_dir: Path,
) -> None:
    """Emit all files for a parsed spec.

    Args:
        spec: Parsed specification
        api_dir: Base directory for API endpoint files
        schemas_dir: Base directory for schema files
    """
    # Group endpoints by module
    endpoints_by_module: dict[str, list[Endpoint]] = defaultdict(list)
    for endpoint in spec.endpoints:
        endpoints_by_module[endpoint.module].append(endpoint)

    # Emit endpoint files per module
    spec_api_dir = api_dir / spec.name
    for module_name, endpoints in endpoints_by_module.items():
        output_path = spec_api_dir / f"{module_name}.py"
        emit_endpoints(endpoints, output_path, module_name, spec.name)

    # Create __init__.py for the spec API directory
    init_path = spec_api_dir / "__init__.py"
    init_content = f'"""Generated {spec.name} API endpoints."""\n'
    for module_name in sorted(endpoints_by_module.keys()):
        init_content += f"from . import {module_name}\n"
    init_path.parent.mkdir(parents=True, exist_ok=True)
    init_path.write_text(init_content)

    # Emit schema file
    schema_path = schemas_dir / f"{spec.name}.py"
    emit_schemas(spec.schemas, schema_path, spec.name)
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/generator/test_emitter.py -v`
Expected: PASS

**Step 5: Run mypy**

Run: `mypy generator/emitter.py --strict`
Expected: Success

**Step 6: Commit**

```bash
git add generator/emitter.py tests/unit/generator/test_emitter.py
git commit -m "feat: implement code emitter with schema imports"
```

---

## Task 13: Implement CLI Main Entry Point

**Files:**
- Modify: `generator/__main__.py`
- Create: `tests/unit/generator/test_main.py`

**Step 1: Write the failing test**

```python
# tests/unit/generator/test_main.py
import subprocess
import sys
from pathlib import Path


def test_generator_cli_help():
    """Test generator CLI shows help."""
    result = subprocess.run(
        [sys.executable, "-m", "generator", "--help"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Generate Binance API client code" in result.stdout


def test_generator_cli_dry_run():
    """Test generator CLI dry run."""
    spec_dir = Path("specs/openapi/spot")
    if not spec_dir.exists():
        import pytest
        pytest.skip("Spec directory not found")

    result = subprocess.run(
        [sys.executable, "-m", "generator", "--dry-run", "--limit", "3"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Would generate" in result.stdout or "Parsed" in result.stdout


def test_generator_cli_verbose():
    """Test generator CLI verbose mode shows errors."""
    spec_dir = Path("specs/openapi/spot")
    if not spec_dir.exists():
        import pytest
        pytest.skip("Spec directory not found")

    result = subprocess.run(
        [sys.executable, "-m", "generator", "--dry-run", "--verbose", "--limit", "5"],
        capture_output=True,
        text=True,
    )

    # Should complete (warnings don't cause failure)
    assert result.returncode in (0, 1)  # 0 if no errors, 1 if errors
    # Verbose mode shows "warnings" or "errors" count
    assert "warnings" in result.stdout or "Done" in result.stdout
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/generator/test_main.py -v`
Expected: FAIL

**Step 3: Implement CLI main**

```python
# generator/__main__.py
"""CLI entry point for generator.

Usage:
    python -m generator              # Generate all APIs
    python -m generator --spot       # Generate only spot API
    python -m generator --dry-run    # Show what would be generated
    python -m generator --limit 10   # Limit endpoints (for testing)
    python -m generator --strict     # Fail on any errors
"""
import argparse
import sys
from pathlib import Path

from generator.config import SPEC_PATHS, OUTPUT_PATHS
from generator.parser import parse_spec_directory, report_parse_result
from generator.emitter import emit_spec


def main() -> int:
    """Run the generator.

    Returns:
        Exit code (0=success, 1=errors)
    """
    parser = argparse.ArgumentParser(
        description="Generate Binance API client code from OpenAPI specs"
    )
    parser.add_argument(
        "--spot", action="store_true",
        help="Generate only spot API"
    )
    parser.add_argument(
        "--futures", action="store_true",
        help="Generate only futures APIs"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would be generated without writing files"
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Limit number of endpoints to parse (for testing)"
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Fail on any parse errors (not just warnings)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Show detailed error/warning messages"
    )

    args = parser.parse_args()

    # Determine which specs to process
    specs_to_process: list[str] = []
    if args.spot:
        specs_to_process = ["spot"]
    elif args.futures:
        specs_to_process = ["umfutures", "cmfutures"]
    else:
        specs_to_process = list(SPEC_PATHS.keys())

    has_errors = False

    for spec_name in specs_to_process:
        spec_dir = SPEC_PATHS.get(spec_name)
        if not spec_dir or not spec_dir.exists():
            print(f"Skipping {spec_name}: spec directory not found")
            continue

        print(f"Parsing {spec_name}...")
        result = parse_spec_directory(spec_dir, limit=args.limit)
        spec = result.spec

        print(f"  Parsed {len(spec.endpoints)} endpoints")
        print(f"  Found {len(spec.schemas)} unique schemas")

        # Report errors/warnings
        if result.errors:
            print(f"  {result.warning_count} warnings, {result.error_count} errors")
            if args.verbose:
                report_parse_result(result)

        # Track if we have errors
        if result.has_errors:
            has_errors = True
            if args.strict:
                print(f"  Stopping due to errors (--strict mode)")
                continue

        # Group endpoints by module
        modules: dict[str, int] = {}
        for endpoint in spec.endpoints:
            modules[endpoint.module] = modules.get(endpoint.module, 0) + 1

        for module, count in sorted(modules.items()):
            print(f"    {module}: {count} endpoints")

        if args.dry_run:
            print(f"  Would generate:")
            print(f"    - binance/api/{spec_name}/*.py")
            print(f"    - binance/_schemas/{spec_name}.py")
        else:
            api_dir = OUTPUT_PATHS["api"]
            schemas_dir = OUTPUT_PATHS["schemas"]

            emit_spec(spec, api_dir, schemas_dir)

            print(f"  Generated:")
            print(f"    - {api_dir}/{spec_name}/")
            print(f"    - {schemas_dir}/{spec_name}.py")

    if has_errors:
        print("\n⚠️  Completed with errors. Use --verbose for details.")
        return 1

    print("\n✓ Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/generator/test_main.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add generator/__main__.py tests/unit/generator/test_main.py
git commit -m "feat: implement generator CLI entry point"
```

---

## Task 14: Integration Test - Generate Spot Market Module

**Files:**
- Create: `tests/integration/generator/test_generate_spot.py`

**Step 1: Write the test**

```python
# tests/integration/generator/test_generate_spot.py
"""Integration test for generating spot market endpoints."""
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_output_dir():
    """Create temporary output directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test_generate_spot_market_endpoints(temp_output_dir: Path):
    """Test generating spot market endpoints produces valid Python."""
    spec_dir = Path("specs/openapi/spot")
    if not spec_dir.exists():
        pytest.skip("Spec directory not found")

    from generator.parser import parse_spec_directory
    from generator.emitter import emit_spec

    # Parse spot specs (limited for speed)
    parsed = parse_spec_directory(spec_dir, limit=20)

    # Filter to just market endpoints for this test
    market_endpoints = [e for e in parsed.endpoints if e.module == "market"]

    assert len(market_endpoints) > 0, "Should have market endpoints"

    # Emit to temp directory
    api_dir = temp_output_dir / "api"
    schemas_dir = temp_output_dir / "schemas"

    emit_spec(parsed, api_dir, schemas_dir)

    # Check files were created
    assert (api_dir / "spot" / "market.py").exists()
    assert (schemas_dir / "spot.py").exists()

    # Verify syntax by importing
    sys.path.insert(0, str(temp_output_dir))

    # Read and compile to check syntax
    market_code = (api_dir / "spot" / "market.py").read_text()
    compile(market_code, "market.py", "exec")

    schema_code = (schemas_dir / "spot.py").read_text()
    compile(schema_code, "spot.py", "exec")


def test_generated_code_type_checks(temp_output_dir: Path):
    """Test that generated code passes mypy."""
    spec_dir = Path("specs/openapi/spot")
    if not spec_dir.exists():
        pytest.skip("Spec directory not found")

    from generator.parser import parse_spec_directory
    from generator.emitter import emit_spec

    # Parse and emit
    parsed = parse_spec_directory(spec_dir, limit=10)

    api_dir = temp_output_dir / "api"
    schemas_dir = temp_output_dir / "schemas"

    emit_spec(parsed, api_dir, schemas_dir)

    # Run mypy on generated files
    result = subprocess.run(
        ["mypy", str(api_dir / "spot"), "--ignore-missing-imports"],
        capture_output=True,
        text=True,
    )

    # Note: We allow some errors since generated code may reference
    # schemas that aren't imported yet
    print(result.stdout)
    print(result.stderr)
```

**Step 2: Create test directory**

```bash
mkdir -p tests/integration/generator
touch tests/integration/__init__.py
touch tests/integration/generator/__init__.py
```

**Step 3: Run integration test**

Run: `pytest tests/integration/generator/test_generate_spot.py -v`
Expected: PASS

**Step 4: Commit**

```bash
git add tests/integration/
git commit -m "test: add integration test for spot market generation"
```

---

## Task 15: Final Verification and Documentation

**Files:**
- Modify: `generator/README.md`

**Step 1: Run full test suite**

Run: `pytest tests/unit/generator/ -v`
Expected: All tests pass

**Step 2: Run mypy on generator**

Run: `mypy generator/ --strict`
Expected: Success

**Step 3: Test full generation (dry run)**

Run: `python -m generator --dry-run`
Expected: Shows parsed endpoints and what would be generated

**Step 4: Create generator README**

```markdown
# Code Generator

Generates typed Python client code from OpenAPI YAML specs.

## Usage

```bash
# Generate all APIs
python -m generator

# Generate only spot API
python -m generator --spot

# Preview what would be generated
python -m generator --dry-run

# Limit endpoints (for testing)
python -m generator --limit 10
```

## Architecture

```
generator/
├── __init__.py       # Package metadata
├── __main__.py       # CLI entry point
├── config.py         # Paths, type mapping, naming rules
├── models.py         # Internal data models (Parameter, Schema, Endpoint)
├── parser.py         # Parse OpenAPI YAML → internal models
├── emitter.py        # Emit internal models → Python code
└── templates/        # Jinja2 templates
    ├── schema.py.j2  # Schema class template
    └── endpoint.py.j2 # Endpoint function template
```

## Spec File Location

Place OpenAPI YAML files in:
- `specs/openapi/spot/` - Spot trading API
- `specs/openapi/umfutures/` - USDT-M Futures API
- `specs/openapi/cmfutures/` - COIN-M Futures API

## Output

Generated files go to:
- `binance/api/{spec}/` - Endpoint modules
- `binance/_schemas/{spec}.py` - Schema definitions
```

**Step 5: Commit**

```bash
git add generator/README.md
git commit -m "docs: add generator README"
```

---

## Summary

After completing all 15 tasks, you will have:

1. **Generator package** (`generator/`) with:
   - Configuration for paths, types, and naming
   - Models for Parameter, Schema, Endpoint, ParsedSpec
   - YAML parser that handles OpenAPI specs
   - Jinja2-based code emitter
   - CLI entry point

2. **Templates** (`generator/templates/`) for:
   - Schema classes (msgspec Structs)
   - Endpoint functions (async methods)

3. **Tests** covering:
   - Unit tests for all components
   - Integration test for end-to-end generation

4. **Generated output** structure:
   ```
   binance/
   ├── api/
   │   └── spot/
   │       ├── __init__.py
   │       ├── general.py
   │       ├── market.py
   │       ├── trade.py
   │       └── account.py
   └── _schemas/
       └── spot.py
   ```

---

## Dependency Graph

```
Task 1 (Dependencies)
    ↓
Task 2 (Package Structure)
    ↓
Task 3 (Config) ─────────────────────┐
    ↓                                │
Task 4 (Models) ←────────────────────┤
    ↓                                │
Task 5 (Parser Basic)                │
    ↓                                │
Task 6 (Parameter Parsing)           │
    ↓                                │
Task 7 (Schema Parsing)              │
    ↓                                │
Task 8 (Endpoint Parsing)            │
    ↓                                │
Task 9 (Directory Parser)            │
    ↓                                │
Task 10 (Schema Template) ←──────────┘
    ↓
Task 11 (Endpoint Template)
    ↓
Task 12 (Emitter) ←── Task 10, 11
    ↓
Task 13 (CLI Main) ←── Task 9, 12
    ↓
Task 14 (Integration Test)
    ↓
Task 15 (Final Verification)
```
