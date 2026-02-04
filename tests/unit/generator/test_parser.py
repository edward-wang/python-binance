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


def test_parse_schema_object():
    """Test parsing object schema with properties."""
    from generator.parser import parse_schema

    schema_data = {
        "type": "object",
        "properties": {
            "orderId": {"type": "integer", "format": "int64"},
            "symbol": {"type": "string"},
            "status": {"type": "string"}
        },
        "required": ["orderId", "symbol"]
    }

    schema = parse_schema("Order", "GetOrderV3Resp", schema_data)

    assert schema.is_array is False
    assert len(schema.properties) == 3

    # Check properties
    prop_map = {p.name: p for p in schema.properties}
    assert prop_map["orderId"].type == "int"
    assert prop_map["orderId"].required is True
    assert prop_map["status"].required is False


def test_parse_schema_array_of_ref():
    """Test parsing array schema with $ref items."""
    from generator.parser import parse_schema

    schema_data = {
        "type": "array",
        "items": {
            "$ref": "#/components/schemas/TradeItem"
        }
    }

    schema = parse_schema("Trade", "GetTradesV3Resp", schema_data)

    assert schema.is_array is True
    assert schema.item_type == "TradeItem"


def test_get_response_schema_ref_200():
    """Test extracting response schema from 200 response."""
    from generator.parser import get_response_schema_ref

    operation = {
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/OrderResult"}
                    }
                }
            }
        }
    }

    ref = get_response_schema_ref(operation)
    assert ref == "OrderResult"


def test_get_response_schema_ref_default():
    """Test extracting response schema from default response."""
    from generator.parser import get_response_schema_ref

    operation = {
        "responses": {
            "default": {
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/APIResponse"}
                    }
                }
            }
        }
    }

    ref = get_response_schema_ref(operation)
    assert ref == "APIResponse"


def test_get_response_schema_ref_json_charset():
    """Test extracting response schema with charset in content type."""
    from generator.parser import get_response_schema_ref

    operation = {
        "responses": {
            "200": {
                "content": {
                    "application/json;charset=utf-8": {
                        "schema": {"$ref": "#/components/schemas/Result"}
                    }
                }
            }
        }
    }

    ref = get_response_schema_ref(operation)
    assert ref == "Result"


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


def test_parse_endpoint():
    """Test parsing a complete endpoint."""
    from generator.parser import parse_endpoint

    data = {
        "components": {
            "schemas": {
                "GetKlinesResp": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "oneOf": [
                                {"type": "integer"},
                                {"type": "string"}
                            ]
                        }
                    }
                }
            }
        },
        "paths": {
            "/api/v3/klines": {
                "get": {
                    "operationId": "GetKlinesV3",
                    "parameters": [
                        {"name": "symbol", "in": "query", "required": True, "schema": {"type": "string"}},
                        {"name": "interval", "in": "query", "required": True, "schema": {"type": "string"}},
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/GetKlinesResp"}
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
    assert endpoint.path == "/api/v3/klines"
    assert len(endpoint.parameters) == 2
    assert endpoint.requires_signature is False
    assert endpoint.module == "market"


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


def test_parse_spec_directory(tmp_path):
    """Test parsing all YAML files in a spec directory."""
    from generator.parser import parse_spec_directory
    from generator.models import ParseErrorSeverity

    # Create test spec files
    spec1 = tmp_path / "get_klines.yaml"
    spec1.write_text("""
openapi: 3.0.0
paths:
  /api/v3/klines:
    get:
      operationId: GetKlinesV3
      parameters:
        - name: symbol
          in: query
          required: true
          schema:
            type: string
      responses:
        200:
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GetKlinesResp'
components:
  schemas:
    GetKlinesResp:
      type: array
      items:
        type: array
        items:
          type: string
""")

    spec2 = tmp_path / "get_ticker.yaml"
    spec2.write_text("""
openapi: 3.0.0
paths:
  /api/v3/ticker/price:
    get:
      operationId: GetTickerPriceV3
      parameters:
        - name: symbol
          in: query
          schema:
            type: string
      responses:
        200:
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TickerPrice'
components:
  schemas:
    TickerPrice:
      type: object
      properties:
        symbol:
          type: string
        price:
          type: string
""")

    result = parse_spec_directory(tmp_path, "test")

    assert result.spec.name == "test"
    assert len(result.spec.endpoints) == 2
    assert len(result.spec.schemas) >= 2
    assert result.error_count == 0


def test_parse_spec_directory_with_errors(tmp_path):
    """Test directory parsing handles errors gracefully."""
    from generator.parser import parse_spec_directory
    from generator.models import ParseErrorSeverity

    # Valid spec
    valid = tmp_path / "valid.yaml"
    valid.write_text("""
openapi: 3.0.0
paths:
  /api/v3/time:
    get:
      operationId: GetServerTimeV3
      responses:
        200:
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ServerTime'
components:
  schemas:
    ServerTime:
      type: object
      properties:
        serverTime:
          type: integer
""")

    # Invalid spec (missing paths)
    invalid = tmp_path / "invalid.yaml"
    invalid.write_text("""
openapi: 3.0.0
components:
  schemas: {}
""")

    result = parse_spec_directory(tmp_path, "test")

    assert len(result.spec.endpoints) == 1  # Only valid endpoint
    assert result.warning_count >= 1  # At least one warning for invalid file


def test_parse_spec_directory_deduplicates_schemas(tmp_path):
    """Test that schemas are deduplicated across files."""
    from generator.parser import parse_spec_directory

    # Two specs with the same schema name
    spec1 = tmp_path / "spec1.yaml"
    spec1.write_text("""
openapi: 3.0.0
paths:
  /api/v3/trades:
    get:
      operationId: GetTradesV3
      responses:
        200:
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Trade'
components:
  schemas:
    Trade:
      type: object
      properties:
        id:
          type: integer
        price:
          type: string
""")

    spec2 = tmp_path / "spec2.yaml"
    spec2.write_text("""
openapi: 3.0.0
paths:
  /api/v3/myTrades:
    get:
      operationId: GetMyTradesV3
      responses:
        200:
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Trade'
components:
  schemas:
    Trade:
      type: object
      properties:
        id:
          type: integer
        price:
          type: string
""")

    result = parse_spec_directory(tmp_path, "test")

    assert len(result.spec.endpoints) == 2
    # Trade schema should be deduplicated
    trade_schemas = [s for s in result.spec.schemas.values() if "Trade" in s.original_name]
    assert len(trade_schemas) == 1


def test_parse_spec_directory_empty(tmp_path):
    """Test parsing empty directory."""
    from generator.parser import parse_spec_directory

    result = parse_spec_directory(tmp_path, "empty")

    assert result.spec.name == "empty"
    assert len(result.spec.endpoints) == 0
    assert len(result.spec.schemas) == 0
