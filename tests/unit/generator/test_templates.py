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
