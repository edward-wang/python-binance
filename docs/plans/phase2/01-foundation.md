# Phase 2: Foundation (Tasks 0-4)

> **Navigation:** [Overview](00-overview.md) | **Foundation** | [Parser](02-parser.md) | [Templates & Emitter](03-templates-emitter.md) | [CLI & Integration](04-cli-integration.md)

---

## Task 0: Analyze Real Spec Files - Pattern Catalog

**Files:**
- Create: `docs/specs-analysis.md`

**Purpose:** Before writing parser code, analyze real spec files to discover all patterns.
This prevents mid-implementation surprises and ensures the parser design is complete.

**Step 1: Analyze sample spec files**

Examine at least 10 diverse spec files to catalog patterns:

```bash
# List all spot spec files
ls specs/openapi/spot/*.yaml | head -20

# Examine specific files for different patterns
cat specs/openapi/spot/get_api_v3_time.yaml      # Simple public endpoint
cat specs/openapi/spot/get_api_v3_klines.yaml    # Raw array response (oneOf)
cat specs/openapi/spot/get_api_v3_account.yaml   # Signed endpoint
cat specs/openapi/spot/get_api_v3_depth.yaml     # Nested array response
cat specs/openapi/spot/post_api_v3_order.yaml    # POST with requestBody
```

**Step 2: Document discovered patterns**

Create `docs/specs-analysis.md` with findings:

```markdown
# OpenAPI Spec Analysis

## Response Type Patterns

### 1. Object Response ($ref)
Example: `get_api_v3_account.yaml`
```yaml
responses:
  "200":
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/GetAccountV3Resp'
```
Parser action: Extract schema name from $ref, generate typed return.

### 2. Array of Objects (items.$ref)
Example: `get_api_v3_trades.yaml`
```yaml
schema:
  items:
    $ref: '#/components/schemas/GetTradesV3RespItem'
  type: array
```
Parser action: Extract item type, generate `list[ItemType]` return.

### 3. Raw Array (items.oneOf)
Example: `get_api_v3_klines.yaml`
```yaml
schema:
  items:
    items:
      oneOf:
        - type: integer
          format: int64
        - type: string
    type: array
  type: array
```
Parser action: Recursively resolve to `list[list[int | str]]`.

### 4. Inline Object (no $ref)
Example: Some error responses
```yaml
schema:
  properties:
    code:
      type: integer
    msg:
      type: string
  type: object
```
Parser action: Generate inline schema or skip (for errors).

## Parameter Patterns

### 1. Required Query Parameter
```yaml
- in: query
  name: symbol
  required: true
  schema:
    type: string
```

### 2. Optional with Default
```yaml
- in: query
  name: limit
  schema:
    default: 500
    maximum: 1000
    type: integer
```

### 3. Enum Parameter
```yaml
- in: query
  name: side
  required: true
  schema:
    enum: [BUY, SELL]
    type: string
```

### 4. requestBody (POST/PUT)
```yaml
requestBody:
  content:
    application/x-www-form-urlencoded:
      schema:
        $ref: '#/components/schemas/PostOrderV3Req'
```

## Security Patterns

### 1. Public Endpoint (no security)
No `security` section in operation.

### 2. API Key Required
```yaml
security:
  - ApiKey: []
```

### 3. Signed (timestamp required)
Has `security` AND `timestamp` parameter with `required: true`.

## Schema Patterns

### 1. Flat Object
```yaml
properties:
  price:
    type: string
  qty:
    type: string
type: object
```

### 2. Nested Object
```yaml
properties:
  commissionRates:
    properties:
      maker:
        type: string
    type: object
type: object
```

### 3. Array Property
```yaml
properties:
  balances:
    items:
      properties:
        asset:
          type: string
      type: object
    type: array
```

## Edge Cases Found

1. [ ] Empty description fields
2. [ ] Missing type (defaults to object)
3. [ ] format: int64 on integers
4. [ ] Multiple $ref to same schema from different endpoints
5. [ ] Schemas with same structure but different names
```

**Step 3: Verify pattern coverage**

Check that all documented patterns are covered by the parser design:

| Pattern | Covered in Task |
|---------|-----------------|
| Object response ($ref) | Task 7 |
| Array response (items.$ref) | Task 7 |
| Raw array (oneOf) | Task 7 (resolve_type) |
| Required params | Task 6 |
| Optional with default | Task 6 |
| Enum params | Task 6 |
| requestBody params | Task 8 |
| Public endpoints | Task 8 |
| Signed endpoints | Task 8 |
| Nested objects | Task 7 |

**Step 4: Commit**

```bash
git add docs/specs-analysis.md
git commit -m "docs: analyze spec files and catalog patterns for parser design"
```

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
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path


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

> **Next:** Continue with [02-parser.md](02-parser.md) for Tasks 5-9 (Parser Implementation)
