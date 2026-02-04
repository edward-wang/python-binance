"""Test generator emitter."""
from pathlib import Path

import pytest

from generator.models import (
    Schema,
    Property,
    Endpoint,
    Parameter,
    ParsedSpec,
)


def test_create_emitter():
    """Test creating an Emitter instance."""
    from generator.emitter import Emitter

    emitter = Emitter()
    assert emitter is not None


def test_render_schemas():
    """Test rendering schema file."""
    from generator.emitter import Emitter

    emitter = Emitter()

    schemas = {
        "OrderResp": Schema(
            name="Order",
            original_name="OrderResp",
            properties=[
                Property(name="orderId", py_name="order_id", type="int", required=True),
                Property(name="symbol", py_name="symbol", type="str", required=True),
            ],
            is_array=False,
        ),
    }

    output = emitter.render_schemas("Spot", schemas)

    assert "class Order(msgspec.Struct" in output
    assert "order_id: int" in output


def test_render_endpoints():
    """Test rendering endpoint file."""
    from generator.emitter import Emitter

    emitter = Emitter()

    endpoints = [
        Endpoint(
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
        ),
    ]

    schemas = {
        "Kline": Schema(
            name="Kline",
            original_name="KlineResp",
            properties=[],
            is_array=True,
            raw_type="list[list[int | str]]",
        ),
    }

    output = emitter.render_endpoints(
        api_name="Spot",
        module="market",
        endpoints=endpoints,
        schemas=schemas,
    )

    assert "class MarketMixin:" in output
    assert "async def get_klines(" in output


def test_group_endpoints_by_module():
    """Test grouping endpoints by their module."""
    from generator.emitter import Emitter

    emitter = Emitter()

    endpoints = [
        Endpoint(
            operation_id="GetKlines",
            method_name="get_klines",
            http_method="GET",
            path="/api/v3/klines",
            parameters=[],
            response_schema=None,
            is_array_response=False,
            requires_signature=False,
            description="",
            module="market",
        ),
        Endpoint(
            operation_id="CreateOrder",
            method_name="create_order",
            http_method="POST",
            path="/api/v3/order",
            parameters=[],
            response_schema=None,
            is_array_response=False,
            requires_signature=True,
            description="",
            module="trade",
        ),
        Endpoint(
            operation_id="GetDepth",
            method_name="get_depth",
            http_method="GET",
            path="/api/v3/depth",
            parameters=[],
            response_schema=None,
            is_array_response=False,
            requires_signature=False,
            description="",
            module="market",
        ),
    ]

    grouped = emitter.group_by_module(endpoints)

    assert len(grouped["market"]) == 2
    assert len(grouped["trade"]) == 1


def test_emit_to_directory(tmp_path):
    """Test emitting generated code to directory."""
    from generator.emitter import Emitter

    emitter = Emitter()

    spec = ParsedSpec(
        name="spot",
        endpoints=[
            Endpoint(
                operation_id="GetKlines",
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
        ],
        schemas={
            "KlineResp": Schema(
                name="Kline",
                original_name="KlineResp",
                properties=[],
                is_array=True,
                raw_type="list[list[int | str]]",
            ),
        },
    )

    emitter.emit(spec, tmp_path)

    # Check files were created
    assert (tmp_path / "schemas.py").exists()
    assert (tmp_path / "market.py").exists()

    # Check content
    schemas_content = (tmp_path / "schemas.py").read_text()
    assert "Kline = list[list[int | str]]" in schemas_content

    market_content = (tmp_path / "market.py").read_text()
    assert "get_klines" in market_content


def test_detect_literal_types():
    """Test detecting when Literal types are used."""
    from generator.emitter import Emitter

    emitter = Emitter()

    # Has Literal
    endpoints = [
        Endpoint(
            operation_id="CreateOrder",
            method_name="create_order",
            http_method="POST",
            path="/api/v3/order",
            parameters=[
                Parameter(
                    name="side",
                    py_name="side",
                    type='Literal["BUY", "SELL"]',
                    required=True,
                    default=None,
                    description="",
                ),
            ],
            response_schema=None,
            is_array_response=False,
            requires_signature=True,
            description="",
            module="trade",
        ),
    ]

    assert emitter.has_literal_types(endpoints) is True

    # No Literal
    endpoints_no_literal = [
        Endpoint(
            operation_id="GetTime",
            method_name="get_time",
            http_method="GET",
            path="/api/v3/time",
            parameters=[],
            response_schema=None,
            is_array_response=False,
            requires_signature=False,
            description="",
            module="general",
        ),
    ]

    assert emitter.has_literal_types(endpoints_no_literal) is False
