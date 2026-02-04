"""Parse OpenAPI YAML files into internal models.

Handles the individual endpoint YAML files in specs/openapi/{api}/*.yaml
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def parse_yaml_file(file_path: Path) -> dict[str, Any]:
    """Parse a single YAML file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def extract_path_and_method(
    data: dict[str, Any],
) -> tuple[str, str, dict[str, Any]]:
    """Extract the endpoint path, HTTP method, and operation from spec data."""
    paths = data.get("paths", {})
    if not paths:
        raise ValueError("No paths found in spec")

    path = next(iter(paths.keys()))
    methods = paths[path]
    method = next(iter(methods.keys()))
    operation = methods[method]

    return path, method.upper(), operation


def is_signed_endpoint(operation: dict[str, Any]) -> bool:
    """Determine if endpoint requires signature.

    Detection priority:
    1. Primary: 'security' section present (OpenAPI standard)
    2. Secondary: Required 'timestamp' parameter (Binance convention)
    3. Tertiary: POST/PUT with requestBody schema (likely signed)
    """
    # Primary: Check security section (most reliable)
    if "security" in operation:
        return True

    # Secondary: Check for timestamp in query parameters
    for param in operation.get("parameters", []):
        if param.get("name") == "timestamp" and param.get("required"):
            return True

    # Tertiary: Check for requestBody with schema (POST/PUT endpoints)
    # These typically require signature in Binance API
    request_body = operation.get("requestBody", {})
    if request_body:
        content = request_body.get("content", {})
        for content_type, media in content.items():
            if media.get("schema"):
                return True

    return False
