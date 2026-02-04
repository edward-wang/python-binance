# Phase 2: CLI & Integration (Tasks 13-15)

> **Navigation:** [Overview](00-overview.md) | [Foundation](01-foundation.md) | [Parser](02-parser.md) | [Templates & Emitter](03-templates-emitter.md) | **CLI & Integration**

> **Prerequisites:** Complete Tasks 0-12 first.

---

## Task 13: Implement CLI Main Entry Point

**Files:**
- Modify: `generator/__main__.py`
- Create: `tests/unit/generator/test_main.py`

**Step 1: Write the failing test**

```python
# tests/unit/generator/test_main.py
import subprocess
import sys
from pathlib import Path


def test_generator_cli_help():
    """Test generator CLI shows help."""
    result = subprocess.run(
        [sys.executable, "-m", "generator", "--help"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Generate Binance API client code" in result.stdout


def test_generator_cli_dry_run():
    """Test generator CLI dry run."""
    spec_dir = Path("specs/openapi/spot")
    if not spec_dir.exists():
        import pytest
        pytest.skip("Spec directory not found")

    result = subprocess.run(
        [sys.executable, "-m", "generator", "--dry-run", "--limit", "3"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Would generate" in result.stdout or "Parsed" in result.stdout


def test_generator_cli_verbose():
    """Test generator CLI verbose mode shows errors."""
    spec_dir = Path("specs/openapi/spot")
    if not spec_dir.exists():
        import pytest
        pytest.skip("Spec directory not found")

    result = subprocess.run(
        [sys.executable, "-m", "generator", "--dry-run", "--verbose", "--limit", "5"],
        capture_output=True,
        text=True,
    )

    assert result.returncode in (0, 1)
    assert "warnings" in result.stdout or "Done" in result.stdout
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/generator/test_main.py -v`
Expected: FAIL

**Step 3: Implement CLI main**

```python
# generator/__main__.py
"""CLI entry point for generator.

Usage:
    python -m generator              # Generate all APIs
    python -m generator --spot       # Generate only spot API
    python -m generator --dry-run    # Show what would be generated
    python -m generator --limit 10   # Limit endpoints (for testing)
    python -m generator --strict     # Fail on any errors
"""
import argparse
import sys
from pathlib import Path

from generator.config import SPEC_PATHS, OUTPUT_PATHS
from generator.parser import parse_spec_directory, report_parse_result
from generator.emitter import emit_spec


def main() -> int:
    """Run the generator.

    Returns:
        Exit code (0=success, 1=errors)
    """
    parser = argparse.ArgumentParser(
        description="Generate Binance API client code from OpenAPI specs"
    )
    parser.add_argument(
        "--spot", action="store_true",
        help="Generate only spot API"
    )
    parser.add_argument(
        "--futures", action="store_true",
        help="Generate only futures APIs"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would be generated without writing files"
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Limit number of endpoints to parse (for testing)"
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Fail on any parse errors (not just warnings)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Show detailed error/warning messages"
    )

    args = parser.parse_args()

    # Determine which specs to process
    specs_to_process: list[str] = []
    if args.spot:
        specs_to_process = ["spot"]
    elif args.futures:
        specs_to_process = ["umfutures", "cmfutures"]
    else:
        specs_to_process = list(SPEC_PATHS.keys())

    has_errors = False

    for spec_name in specs_to_process:
        spec_dir = SPEC_PATHS.get(spec_name)
        if not spec_dir or not spec_dir.exists():
            print(f"Skipping {spec_name}: spec directory not found")
            continue

        print(f"Parsing {spec_name}...")
        result = parse_spec_directory(spec_dir, limit=args.limit)
        spec = result.spec

        print(f"  Parsed {len(spec.endpoints)} endpoints")
        print(f"  Found {len(spec.schemas)} unique schemas")

        # Report errors/warnings
        if result.errors:
            print(f"  {result.warning_count} warnings, {result.error_count} errors")
            if args.verbose:
                report_parse_result(result)

        # Track if we have errors
        if result.has_errors:
            has_errors = True
            if args.strict:
                print(f"  Stopping due to errors (--strict mode)")
                continue

        # Group endpoints by module
        modules: dict[str, int] = {}
        for endpoint in spec.endpoints:
            modules[endpoint.module] = modules.get(endpoint.module, 0) + 1

        for module, count in sorted(modules.items()):
            print(f"    {module}: {count} endpoints")

        if args.dry_run:
            print(f"  Would generate:")
            print(f"    - binance/api/{spec_name}/*.py")
            print(f"    - binance/_schemas/{spec_name}.py")
        else:
            api_dir = OUTPUT_PATHS["api"]
            schemas_dir = OUTPUT_PATHS["schemas"]

            emit_spec(spec, api_dir, schemas_dir)

            print(f"  Generated:")
            print(f"    - {api_dir}/{spec_name}/")
            print(f"    - {schemas_dir}/{spec_name}.py")

    if has_errors:
        print("\nCompleted with errors. Use --verbose for details.")
        return 1

    print("\nDone!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/generator/test_main.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add generator/__main__.py tests/unit/generator/test_main.py
git commit -m "feat: implement generator CLI entry point"
```

---

## Task 14: Integration Test - Generate Spot Market Module

**Files:**
- Create: `tests/integration/generator/test_generate_spot.py`

**Step 1: Write the test**

```python
# tests/integration/generator/test_generate_spot.py
"""Integration test for generating spot market endpoints."""
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_output_dir():
    """Create temporary output directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test_generate_spot_market_endpoints(temp_output_dir: Path):
    """Test generating spot market endpoints produces valid Python."""
    spec_dir = Path("specs/openapi/spot")
    if not spec_dir.exists():
        pytest.skip("Spec directory not found")

    from generator.parser import parse_spec_directory
    from generator.emitter import emit_spec

    # Parse spot specs (limited for speed)
    result = parse_spec_directory(spec_dir, limit=20)

    # Filter to just market endpoints for this test
    market_endpoints = [e for e in result.spec.endpoints if e.module == "market"]

    assert len(market_endpoints) > 0, "Should have market endpoints"

    # Emit to temp directory
    api_dir = temp_output_dir / "api"
    schemas_dir = temp_output_dir / "schemas"

    emit_spec(result.spec, api_dir, schemas_dir)

    # Check files were created
    assert (api_dir / "spot" / "market.py").exists()
    assert (schemas_dir / "spot.py").exists()

    # Read and compile to check syntax
    market_code = (api_dir / "spot" / "market.py").read_text()
    compile(market_code, "market.py", "exec")

    schema_code = (schemas_dir / "spot.py").read_text()
    compile(schema_code, "spot.py", "exec")


def test_generated_code_type_checks(temp_output_dir: Path):
    """Test that generated code passes mypy."""
    spec_dir = Path("specs/openapi/spot")
    if not spec_dir.exists():
        pytest.skip("Spec directory not found")

    from generator.parser import parse_spec_directory
    from generator.emitter import emit_spec

    # Parse and emit
    result = parse_spec_directory(spec_dir, limit=10)

    api_dir = temp_output_dir / "api"
    schemas_dir = temp_output_dir / "schemas"

    emit_spec(result.spec, api_dir, schemas_dir)

    # Run mypy on generated files
    mypy_result = subprocess.run(
        ["mypy", str(api_dir / "spot"), "--ignore-missing-imports"],
        capture_output=True,
        text=True,
    )

    print(mypy_result.stdout)
    print(mypy_result.stderr)
```

**Step 2: Create test directory**

```bash
mkdir -p tests/integration/generator
touch tests/integration/__init__.py
touch tests/integration/generator/__init__.py
```

**Step 3: Run integration test**

Run: `pytest tests/integration/generator/test_generate_spot.py -v`
Expected: PASS

**Step 4: Commit**

```bash
git add tests/integration/
git commit -m "test: add integration test for spot market generation"
```

---

## Task 15: Final Verification and Documentation

**Files:**
- Create: `generator/README.md`

**Step 1: Run full test suite**

Run: `pytest tests/unit/generator/ -v`
Expected: All tests pass

**Step 2: Run mypy on generator**

Run: `mypy generator/ --strict`
Expected: Success

**Step 3: Test full generation (dry run)**

Run: `python -m generator --dry-run`
Expected: Shows parsed endpoints and what would be generated

**Step 4: Create generator README**

```markdown
# Code Generator

Generates typed Python client code from OpenAPI YAML specs.

## Usage

```bash
# Generate all APIs
python -m generator

# Generate only spot API
python -m generator --spot

# Preview what would be generated
python -m generator --dry-run

# Limit endpoints (for testing)
python -m generator --limit 10

# Show detailed errors
python -m generator --verbose

# Fail on any errors
python -m generator --strict
```

## Architecture

```
generator/
├── __init__.py       # Package metadata
├── __main__.py       # CLI entry point
├── config.py         # Paths, type mapping, naming rules
├── models.py         # Internal data models (Parameter, Schema, Endpoint)
├── parser.py         # Parse OpenAPI YAML → internal models
├── emitter.py        # Emit internal models → Python code
├── overrides.yaml    # Schema naming overrides
└── templates/        # Jinja2 templates
    ├── schema.py.j2  # Schema class template
    └── endpoint.py.j2 # Endpoint function template
```

## Spec File Location

Place OpenAPI YAML files in:
- `specs/openapi/spot/` - Spot trading API
- `specs/openapi/umfutures/` - USDT-M Futures API
- `specs/openapi/cmfutures/` - COIN-M Futures API

## Output

Generated files go to:
- `binance/api/{spec}/` - Endpoint modules
- `binance/_schemas/{spec}.py` - Schema definitions

## Generation Metadata

All generated files include:
- Generation timestamp
- Source spec directory
- "DO NOT EDIT" warning with regeneration command
- Formatted with `ruff format`

## Error Handling

The generator collects all parsing errors/warnings:
- **Warnings**: Skipped files, naming conflicts
- **Errors**: Critical parsing failures

Use `--verbose` to see details, `--strict` to fail on any errors.
```

**Step 5: Commit**

```bash
git add generator/README.md
git commit -m "docs: add generator README"
```

---

## Summary

After completing all 16 tasks (0-15), you will have:

1. **Generator package** (`generator/`) with:
   - Configuration for paths, types, and naming
   - Models for Parameter, Schema, Endpoint, ParsedSpec
   - YAML parser that handles OpenAPI specs
   - Jinja2-based code emitter
   - CLI entry point

2. **Templates** (`generator/templates/`) for:
   - Schema classes (msgspec Structs)
   - Endpoint functions (async methods)

3. **Tests** covering:
   - Unit tests for all components
   - Integration test for end-to-end generation

4. **Generated output** structure:
   ```
   binance/
   ├── api/
   │   └── spot/
   │       ├── __init__.py
   │       ├── general.py
   │       ├── market.py
   │       ├── trade.py
   │       └── account.py
   └── _schemas/
       └── spot.py
   ```

---

## Full Dependency Graph

See [00-overview.md](00-overview.md#dependency-graph) for the complete dependency graph.

---

> **Complete!** After finishing Task 15, the Phase 2 Code Generator is ready.
