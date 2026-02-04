"""Generator configuration and naming rules."""
from __future__ import annotations

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
    2. Strip response/request suffixes (Resp, Response, Request)
    3. Strip version suffix (V3, V1, etc.)
    4. Strip prefixes (Spot, Futures, Get, Post, Delete, Put)
    5. Check semantic_renames override
    6. Convert plural to singular
    7. Fallback to original if result is empty

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

    # Step 2: Strip response/request suffixes FIRST
    name = RESP_SUFFIXES.sub("", schema_name)
    name = REQ_SUFFIXES.sub("", name)

    # Step 3: Strip version suffix (now at end after Resp removed)
    name = VERSION_SUFFIXES.sub("", name)

    # Step 4: Strip common prefixes
    name = PREFIX_PATTERNS.sub("", name)

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


def detect_method_collisions(
    operation_ids: list[str],
    module: str,
) -> dict[str, list[str]]:
    """Detect when multiple operations map to the same method name within a module.

    Args:
        operation_ids: List of operationIds for endpoints in the same module
        module: Module name (for context in error messages)

    Returns:
        Dict of method_name -> list of operation_ids that conflict
    """
    mappings: dict[str, list[str]] = {}
    for op_id in operation_ids:
        method_name = to_method_name(op_id)
        mappings.setdefault(method_name, []).append(op_id)

    return {name: ops for name, ops in mappings.items() if len(ops) > 1}


def resolve_method_collision(
    operation_id: str,
    existing_methods: set[str],
) -> str:
    """Resolve method name collision by appending version or suffix.

    Args:
        operation_id: Original operationId
        existing_methods: Set of method names already used in this module

    Returns:
        Unique method name
    """
    base_name = to_method_name(operation_id)

    if base_name not in existing_methods:
        return base_name

    # Try appending version from operationId (e.g., get_klines_v3)
    version_match = re.search(r"V(\d+)", operation_id)
    if version_match:
        versioned_name = f"{base_name}_v{version_match.group(1)}"
        if versioned_name not in existing_methods:
            return versioned_name

    # Fallback: append incrementing suffix
    suffix = 2
    while f"{base_name}_{suffix}" in existing_methods:
        suffix += 1
    return f"{base_name}_{suffix}"


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

# Default module inference based on path keywords
MODULE_KEYWORDS: dict[str, str] = {
    "trade": "trade",
    "order": "trade",
    "account": "account",
    "balance": "account",
    "asset": "account",
    "ticker": "market",
    "price": "market",
    "depth": "market",
    "kline": "market",
    "candle": "market",
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

    # Infer module from path keywords (for new/unknown endpoints)
    path_lower = path.lower()
    for keyword, module in MODULE_KEYWORDS.items():
        if keyword in path_lower:
            return module

    # Default to 'general' for core API, 'other' for sapi
    if "/sapi/" in path:
        return "other"

    return "general"
