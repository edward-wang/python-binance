"""Test generator templates."""
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

from generator.models import Schema, Property


@pytest.fixture
def jinja_env():
    """Create Jinja2 environment with templates."""
    templates_dir = Path(__file__).parent.parent.parent.parent / "generator" / "templates"
    return Environment(
        loader=FileSystemLoader(templates_dir),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def test_schema_template_basic(jinja_env):
    """Test generating a basic schema class."""
    template = jinja_env.get_template("schema.py.j2")

    schema = Schema(
        name="Order",
        original_name="GetOrderV3Resp",
        properties=[
            Property(name="orderId", py_name="order_id", type="int", required=True),
            Property(name="symbol", py_name="symbol", type="str", required=True),
            Property(name="status", py_name="status", type="str", required=False),
        ],
        is_array=False,
    )

    output = template.render(
        api_name="Spot",
        schemas=[schema],
        has_literal_types=False,
    )

    assert "class Order(msgspec.Struct, rename=\"camel\"):" in output
    assert "order_id: int" in output
    assert "symbol: str" in output
    assert "status: str | None = None" in output


def test_schema_template_raw_type(jinja_env):
    """Test generating schema with raw array type (klines)."""
    template = jinja_env.get_template("schema.py.j2")

    schema = Schema(
        name="Kline",
        original_name="GetKlinesV3Resp",
        properties=[],
        is_array=True,
        raw_type="list[list[int | str]]",
    )

    output = template.render(
        api_name="Spot",
        schemas=[schema],
        has_literal_types=False,
    )

    assert "Kline = list[list[int | str]]" in output


def test_schema_template_with_literal(jinja_env):
    """Test that Literal import is included when needed."""
    template = jinja_env.get_template("schema.py.j2")

    schema = Schema(
        name="OrderSide",
        original_name="OrderSide",
        properties=[
            Property(
                name="side",
                py_name="side",
                type='Literal["BUY", "SELL"]',
                required=True,
            ),
        ],
        is_array=False,
    )

    output = template.render(
        api_name="Spot",
        schemas=[schema],
        has_literal_types=True,
    )

    assert "from typing import Literal" in output


def test_schema_template_empty_schema(jinja_env):
    """Test generating empty schema fallback."""
    template = jinja_env.get_template("schema.py.j2")

    schema = Schema(
        name="EmptyResponse",
        original_name="EmptyResp",
        properties=[],
        is_array=False,
    )

    output = template.render(
        api_name="Spot",
        schemas=[schema],
        has_literal_types=False,
    )

    assert "EmptyResponse = dict[str, Any]" in output


def test_schema_template_module_header(jinja_env):
    """Test that generated file has proper header."""
    template = jinja_env.get_template("schema.py.j2")

    output = template.render(
        api_name="Spot",
        schemas=[],
        has_literal_types=False,
    )

    assert '"""Generated Spot API response schemas.' in output
    assert "import msgspec" in output


# ============ Endpoint Template Tests ============

from generator.models import Endpoint, Parameter


def test_endpoint_template_unsigned(jinja_env):
    """Test generating unsigned endpoint method."""
    template = jinja_env.get_template("endpoint.py.j2")

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
                description="Trading pair",
            ),
            Parameter(
                name="interval",
                py_name="interval",
                type="str",
                required=True,
                default=None,
                description="Kline interval",
            ),
            Parameter(
                name="limit",
                py_name="limit",
                type="int",
                required=False,
                default=500,
                description="Max results",
            ),
        ],
        response_schema="Kline",
        is_array_response=True,
        requires_signature=False,
        description="Get kline/candlestick data",
        module="market",
        weight=1,
    )

    output = template.render(
        api_name="Spot",
        module="market",
        module_class="Market",
        client_class="SpotClient",
        endpoints=[endpoint],
        schema_imports=["Kline"],
        has_literal_types=False,
    )

    assert "async def get_klines(" in output
    assert "symbol: str," in output
    assert "interval: str," in output
    assert "limit: int = 500," in output
    assert "_request(" in output  # Unsigned uses _request
    assert "_request_signed(" not in output
    assert '"/api/v3/klines"' in output


def test_endpoint_template_signed(jinja_env):
    """Test generating signed endpoint method."""
    template = jinja_env.get_template("endpoint.py.j2")

    endpoint = Endpoint(
        operation_id="CreateOrderV3",
        method_name="create_order",
        http_method="POST",
        path="/api/v3/order",
        parameters=[
            Parameter(
                name="symbol",
                py_name="symbol",
                type="str",
                required=True,
                default=None,
                description="Trading pair",
            ),
            Parameter(
                name="side",
                py_name="side",
                type='Literal["BUY", "SELL"]',
                required=True,
                default=None,
                description="Order side",
            ),
        ],
        response_schema="Order",
        is_array_response=False,
        requires_signature=True,
        description="Create new order",
        module="trade",
        weight=1,
    )

    output = template.render(
        api_name="Spot",
        module="trade",
        module_class="Trade",
        client_class="SpotClient",
        endpoints=[endpoint],
        schema_imports=["Order"],
        has_literal_types=True,
    )

    assert "async def create_order(" in output
    assert "_request_signed(" in output  # Signed uses _request_signed
    assert 'Literal["BUY", "SELL"]' in output


def test_endpoint_template_optional_params(jinja_env):
    """Test that optional parameters are handled correctly."""
    template = jinja_env.get_template("endpoint.py.j2")

    endpoint = Endpoint(
        operation_id="GetTickerV3",
        method_name="get_ticker",
        http_method="GET",
        path="/api/v3/ticker",
        parameters=[
            Parameter(
                name="symbol",
                py_name="symbol",
                type="str",
                required=False,
                default=None,
                description="Optional symbol",
            ),
        ],
        response_schema="Ticker",
        is_array_response=False,
        requires_signature=False,
        description="Get ticker",
        module="market",
        weight=1,
    )

    output = template.render(
        api_name="Spot",
        module="market",
        module_class="Market",
        client_class="SpotClient",
        endpoints=[endpoint],
        schema_imports=["Ticker"],
        has_literal_types=False,
    )

    assert "symbol: str | None = None," in output
    assert 'if symbol is not None:' in output


def test_endpoint_template_weight_docstring(jinja_env):
    """Test that weight is included in docstring."""
    template = jinja_env.get_template("endpoint.py.j2")

    endpoint = Endpoint(
        operation_id="GetDepthV3",
        method_name="get_depth",
        http_method="GET",
        path="/api/v3/depth",
        parameters=[],
        response_schema="OrderBook",
        is_array_response=False,
        requires_signature=False,
        description="Get order book",
        module="market",
        weight=5,
    )

    output = template.render(
        api_name="Spot",
        module="market",
        module_class="Market",
        client_class="SpotClient",
        endpoints=[endpoint],
        schema_imports=["OrderBook"],
        has_literal_types=False,
    )

    assert "Weight: 5" in output
