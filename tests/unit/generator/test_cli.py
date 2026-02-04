"""Test generator CLI."""
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from generator.__main__ import main, generate_api
from generator.models import (
    ParsedSpec,
    ParseResult,
    ParseError,
    ParseErrorSeverity,
)


def test_main_no_args(capsys):
    """Test CLI with no arguments shows help."""
    with patch("sys.argv", ["generator"]):
        exit_code = main()
        assert exit_code == 1


def test_main_help(capsys):
    """Test CLI --help flag."""
    with patch("sys.argv", ["generator", "--help"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0


def test_generate_api_unknown_spec(capsys):
    """Test generating unknown spec name."""
    result = generate_api("unknown", Path("/tmp/output"))
    assert result is False

    captured = capsys.readouterr()
    assert "Unknown spec" in captured.err


def test_generate_api_missing_directory(tmp_path, capsys):
    """Test generating with missing spec directory."""
    # Patch SPEC_PATHS to point to non-existent directory
    fake_paths = {"test": tmp_path / "nonexistent"}

    with patch("generator.__main__.SPEC_PATHS", fake_paths):
        result = generate_api("test", tmp_path / "output")
        assert result is False

    captured = capsys.readouterr()
    assert "not found" in captured.err


def test_generate_api_success(tmp_path, capsys):
    """Test successful generation."""
    # Create a minimal spec file
    spec_dir = tmp_path / "specs"
    spec_dir.mkdir()

    spec_file = spec_dir / "test_endpoint.yaml"
    spec_file.write_text("""
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

    output_dir = tmp_path / "output"
    fake_paths = {"test": spec_dir}

    with patch("generator.__main__.SPEC_PATHS", fake_paths):
        result = generate_api("test", output_dir)

    assert result is True
    assert (output_dir / "schemas.py").exists()

    captured = capsys.readouterr()
    assert "Parsed 1 endpoints" in captured.out
    assert "Generated" in captured.out


def test_generate_api_with_warnings(tmp_path, capsys):
    """Test generation with parse warnings."""
    spec_dir = tmp_path / "specs"
    spec_dir.mkdir()

    # Valid spec
    valid_spec = spec_dir / "valid.yaml"
    valid_spec.write_text("""
openapi: 3.0.0
paths:
  /api/v3/time:
    get:
      operationId: GetTimeV3
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
components:
  schemas: {}
""")

    # Invalid spec (missing paths)
    invalid_spec = spec_dir / "invalid.yaml"
    invalid_spec.write_text("""
openapi: 3.0.0
components:
  schemas: {}
""")

    output_dir = tmp_path / "output"
    fake_paths = {"test": spec_dir}

    with patch("generator.__main__.SPEC_PATHS", fake_paths):
        result = generate_api("test", output_dir)

    assert result is True
    captured = capsys.readouterr()
    assert "WARNING" in captured.err


def test_main_single_spec(tmp_path):
    """Test main() with single spec argument."""
    spec_dir = tmp_path / "specs"
    spec_dir.mkdir()

    spec_file = spec_dir / "endpoint.yaml"
    spec_file.write_text("""
openapi: 3.0.0
paths:
  /api/v3/ping:
    get:
      operationId: PingV3
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
components:
  schemas: {}
""")

    output_dir = tmp_path / "output"
    fake_paths = {"spot": spec_dir}

    with patch("generator.__main__.SPEC_PATHS", fake_paths):
        with patch("sys.argv", ["generator", "spot", "--output", str(output_dir)]):
            exit_code = main()

    assert exit_code == 0
    assert output_dir.exists()


def test_main_all_specs(tmp_path):
    """Test main() with --all flag."""
    # Create spec directories
    for api in ["spot", "umfutures"]:
        spec_dir = tmp_path / "specs" / api
        spec_dir.mkdir(parents=True)
        spec_file = spec_dir / "endpoint.yaml"
        spec_file.write_text(f"""
openapi: 3.0.0
paths:
  /api/v3/ping:
    get:
      operationId: Ping{api.title()}V3
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
components:
  schemas: {{}}
""")

    output_dir = tmp_path / "output"
    fake_paths = {
        "spot": tmp_path / "specs" / "spot",
        "umfutures": tmp_path / "specs" / "umfutures",
    }

    with patch("generator.__main__.SPEC_PATHS", fake_paths):
        with patch("sys.argv", ["generator", "--all", "--output", str(output_dir)]):
            exit_code = main()

    assert exit_code == 0
    assert (output_dir / "spot").exists()
    assert (output_dir / "umfutures").exists()
