"""Code generator for Binance API client.

Reads OpenAPI YAML specs and generates typed Python code.

Usage:
    python -m generator spot --output generated/spot
    python -m generator --all --output generated

Components:
    - parser: Parse OpenAPI YAML specs into internal models
    - emitter: Render templates to generate Python code
    - config: Configuration and naming rules
    - models: Data models for parsed specs
"""
from generator.config import (
    SPEC_PATHS,
    OUTPUT_PATHS,
    to_snake_case,
    to_class_name,
    to_method_name,
)
from generator.models import (
    Parameter,
    Property,
    Schema,
    Endpoint,
    ParsedSpec,
    ParseResult,
    ParseError,
    ParseErrorSeverity,
)
from generator.parser import (
    parse_yaml_file,
    parse_endpoint,
    parse_endpoint_file,
    parse_spec_directory,
)
from generator.emitter import Emitter

__version__ = "0.1.0"

__all__ = [
    # Config
    "SPEC_PATHS",
    "OUTPUT_PATHS",
    "to_snake_case",
    "to_class_name",
    "to_method_name",
    # Models
    "Parameter",
    "Property",
    "Schema",
    "Endpoint",
    "ParsedSpec",
    "ParseResult",
    "ParseError",
    "ParseErrorSeverity",
    # Parser
    "parse_yaml_file",
    "parse_endpoint",
    "parse_endpoint_file",
    "parse_spec_directory",
    # Emitter
    "Emitter",
]
