"""Test generator parser."""
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

    # Unsigned - no security, no timestamp
    operation = {"parameters": [{"name": "symbol"}]}
    assert is_signed_endpoint(operation) is False

    # Signed with security section (primary indicator)
    operation = {"security": [{"ApiKey": []}]}
    assert is_signed_endpoint(operation) is True

    # Signed with timestamp param (secondary indicator)
    operation = {"parameters": [{"name": "timestamp", "required": True}]}
    assert is_signed_endpoint(operation) is True

    # Signed with requestBody schema (tertiary indicator for POST/PUT)
    operation = {
        "requestBody": {
            "content": {
                "application/x-www-form-urlencoded": {
                    "schema": {"$ref": "#/components/schemas/CreateOrderReq"}
                }
            }
        }
    }
    assert is_signed_endpoint(operation) is True

    # Unsigned timestamp (not required)
    operation = {"parameters": [{"name": "timestamp", "required": False}]}
    assert is_signed_endpoint(operation) is False


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
    """Test parsing enum parameter with Literal type generation."""
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
    # Should generate Literal type
    assert param.literal_type == 'Literal["1m", "5m", "1h", "1d"]'
    assert param.type == param.literal_type


def test_generate_literal_type():
    """Test Literal type generation."""
    from generator.parser import generate_literal_type

    assert generate_literal_type(["BUY", "SELL"]) == 'Literal["BUY", "SELL"]'
    assert generate_literal_type(["1m"]) == 'Literal["1m"]'


def test_parse_parameter_with_array():
    """Test parsing array parameter."""
    from generator.parser import parse_parameter

    param_data = {
        "name": "symbols",
        "in": "query",
        "schema": {
            "type": "array",
            "items": {"type": "string"}
        }
    }

    param = parse_parameter(param_data)

    assert param.type == "list[str]"


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
