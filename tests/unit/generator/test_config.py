"""Test generator configuration."""
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
    assert to_class_name("GetBalancesV3Resp") == "Balance"  # plural -> singular
    assert to_class_name("GetServerTimeV3Resp") == "ServerTime"  # no change needed
    assert to_class_name("GetAccountV3Resp") == "Account"

    # Handles various prefixes
    assert to_class_name("SpotCreateOrderV3Resp") == "CreateOrder"  # keeps verb
    # Note: PostOrderV3Resp is in conflict_resolutions, so test a different one
    assert to_class_name("DeleteOrderV3Resp") == "Order"  # strips Delete


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


def test_get_module_for_path_exact_match():
    """Test module lookup for exact path match."""
    from generator.config import get_module_for_path

    assert get_module_for_path("/api/v3/klines") == "market"
    assert get_module_for_path("/api/v3/order") == "trade"
    assert get_module_for_path("/api/v3/account") == "account"


def test_get_module_for_path_prefix_match():
    """Test module lookup for prefix match."""
    from generator.config import get_module_for_path

    # These start with known prefixes
    assert get_module_for_path("/api/v3/ticker/24hr") == "market"
    assert get_module_for_path("/api/v3/order/test") == "trade"


def test_get_module_for_path_keyword_inference():
    """Test module inference from path keywords (for unknown paths)."""
    from generator.config import get_module_for_path

    # New paths not in PATH_TO_MODULE but containing keywords
    assert get_module_for_path("/api/v4/newTicker") == "market"
    assert get_module_for_path("/api/v4/userBalance") == "account"
    assert get_module_for_path("/api/v4/cancelOrder") == "trade"


def test_get_module_for_path_defaults():
    """Test default module assignment."""
    from generator.config import get_module_for_path

    # sapi endpoints default to 'other'
    assert get_module_for_path("/sapi/v1/something") == "other"

    # Unknown core API endpoints default to 'general'
    assert get_module_for_path("/api/v5/unknown") == "general"


def test_detect_method_collisions():
    """Test detecting method name collisions."""
    from generator.config import detect_method_collisions

    # No collision
    ops = ["GetKlinesV3", "GetTradesV3", "GetDepthV3"]
    collisions = detect_method_collisions(ops, "market")
    assert len(collisions) == 0

    # Collision: GetKlinesV3 and GetKlinesV4 both map to get_klines
    ops = ["GetKlinesV3", "GetKlinesV4", "GetTradesV3"]
    collisions = detect_method_collisions(ops, "market")
    assert "get_klines" in collisions
    assert set(collisions["get_klines"]) == {"GetKlinesV3", "GetKlinesV4"}


def test_resolve_method_collision():
    """Test resolving method name collisions."""
    from generator.config import resolve_method_collision

    existing = {"get_klines"}

    # First collision: use version suffix
    name = resolve_method_collision("GetKlinesV4", existing)
    assert name == "get_klines_v4"

    # Add v4 to existing
    existing.add("get_klines_v4")

    # Third version collision: use numeric suffix when version taken
    name = resolve_method_collision("GetKlinesV5", existing)
    assert name == "get_klines_v5"

    # Add v5 to existing, then try another v5
    existing.add("get_klines_v5")
    existing.add("get_klines")  # ensure base is taken

    # When both base and version suffix taken, use numeric suffix
    name = resolve_method_collision("GetKlinesV5", existing)
    assert name == "get_klines_2"
