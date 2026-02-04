"""Test generator models."""
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


def test_parameter_with_literal_type():
    """Test Parameter with enum literal type."""
    param = Parameter(
        name="interval",
        py_name="interval",
        type='Literal["1m", "5m", "1h", "1d"]',
        required=True,
        default=None,
        description="Kline interval",
        enum=["1m", "5m", "1h", "1d"],
        literal_type='Literal["1m", "5m", "1h", "1d"]',
    )
    assert param.literal_type is not None
    assert "1m" in param.literal_type


def test_endpoint_creation():
    """Test Endpoint dataclass."""
    endpoint = Endpoint(
        operation_id="GetKlinesV3",
        method_name="get_klines",
        http_method="GET",
        path="/api/v3/klines",
        parameters=[
            Parameter(
                name="symbol",
                py_name="symbol",
                type="str",
                required=True,
                default=None,
                description="",
            ),
        ],
        response_schema="Kline",
        is_array_response=True,
        requires_signature=False,
        description="Get kline data",
        module="market",
    )
    assert endpoint.method_name == "get_klines"
    assert endpoint.requires_signature is False
    assert endpoint.weight == 1  # Default weight


def test_endpoint_with_weight():
    """Test Endpoint with rate limit weight."""
    endpoint = Endpoint(
        operation_id="GetKlinesV3",
        method_name="get_klines",
        http_method="GET",
        path="/api/v3/klines",
        parameters=[],
        response_schema="Kline",
        is_array_response=True,
        requires_signature=False,
        description="Get kline data",
        module="market",
        weight=5,
    )
    assert endpoint.weight == 5


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
