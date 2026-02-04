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
