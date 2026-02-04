"""Integration tests for the generator.

These tests run the generator against actual spec files to verify
end-to-end functionality.
"""
from pathlib import Path
import subprocess
import sys

import pytest


@pytest.fixture
def output_dir(tmp_path):
    """Create a temporary output directory."""
    return tmp_path / "generated"


def test_generate_spot_api(output_dir):
    """Test generating the full spot API."""
    result = subprocess.run(
        [sys.executable, "-m", "generator", "spot", "--output", str(output_dir)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"Generator failed: {result.stderr}"
    assert "Parsed" in result.stdout
    assert "Generated" in result.stdout

    # Verify files were created
    assert (output_dir / "schemas.py").exists()
    assert (output_dir / "market.py").exists()
    assert (output_dir / "trade.py").exists()
    assert (output_dir / "account.py").exists()


def test_generated_code_is_valid_python(output_dir):
    """Test that all generated files are valid Python."""
    # Generate first
    subprocess.run(
        [sys.executable, "-m", "generator", "spot", "--output", str(output_dir)],
        capture_output=True,
    )

    # Compile each file
    for py_file in output_dir.glob("*.py"):
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(py_file)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"{py_file.name} is not valid Python: {result.stderr}"


def test_generated_schemas_importable(output_dir):
    """Test that generated schemas can be imported."""
    subprocess.run(
        [sys.executable, "-m", "generator", "spot", "--output", str(output_dir)],
        capture_output=True,
    )

    # Add output_dir to path and try to import
    init_file = output_dir / "__init__.py"
    init_file.write_text("")

    # Try importing the schemas module
    result = subprocess.run(
        [sys.executable, "-c", f"import sys; sys.path.insert(0, '{output_dir.parent}'); from {output_dir.name}.schemas import *"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Failed to import schemas: {result.stderr}"


def test_generate_all_apis(output_dir):
    """Test generating all APIs with --all flag."""
    result = subprocess.run(
        [sys.executable, "-m", "generator", "--all", "--output", str(output_dir)],
        capture_output=True,
        text=True,
    )

    # Should succeed (or skip missing futures specs)
    # We just check that it doesn't crash
    assert "Parsing" in result.stdout


def test_endpoint_count():
    """Test that we parse the expected number of spot endpoints."""
    from generator.config import SPEC_PATHS
    from generator.parser import parse_spec_directory

    spot_dir = SPEC_PATHS.get("spot")
    if not spot_dir or not spot_dir.exists():
        pytest.skip("Spot specs not found")

    result = parse_spec_directory(spot_dir, "spot")

    # We expect around 380+ endpoints for spot
    assert len(result.spec.endpoints) >= 350, f"Only {len(result.spec.endpoints)} endpoints found"

    # We expect schemas
    assert len(result.spec.schemas) >= 100, f"Only {len(result.spec.schemas)} schemas found"

    # There should be minimal errors
    assert result.error_count == 0, f"Found {result.error_count} errors"
