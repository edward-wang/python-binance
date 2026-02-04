"""CLI entry point for generator.

Usage:
    python -m generator spot --output generated/spot
    python -m generator umfutures --output generated/umfutures
    python -m generator --all --output generated
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from generator.config import SPEC_PATHS, OUTPUT_PATHS, detect_naming_conflicts, to_class_name
from generator.parser import parse_spec_directory
from generator.emitter import Emitter
from generator.models import ParseErrorSeverity


def generate_api(spec_name: str, output_dir: Path) -> bool:
    """Generate API code for a single spec.

    Args:
        spec_name: Name of the spec (spot, umfutures, cmfutures)
        output_dir: Directory to write generated files

    Returns:
        True if successful, False if errors occurred
    """
    spec_dir = SPEC_PATHS.get(spec_name)
    if not spec_dir:
        print(f"Error: Unknown spec '{spec_name}'", file=sys.stderr)
        print(f"Available: {', '.join(SPEC_PATHS.keys())}", file=sys.stderr)
        return False

    if not spec_dir.exists():
        print(f"Error: Spec directory not found: {spec_dir}", file=sys.stderr)
        return False

    print(f"Parsing {spec_name} specs from {spec_dir}...")
    result = parse_spec_directory(spec_dir, spec_name)

    # Report warnings
    for error in result.errors:
        severity = "WARNING" if error.severity == ParseErrorSeverity.WARNING else "ERROR"
        file_name = error.file.name if error.file else "unknown"
        print(f"  {severity}: {file_name}: {error.message}", file=sys.stderr)

    if result.has_errors:
        print(f"Error: Failed to parse {spec_name} specs", file=sys.stderr)
        return False

    print(f"  Parsed {len(result.spec.endpoints)} endpoints, {len(result.spec.schemas)} schemas")
    if result.warning_count > 0:
        print(f"  {result.warning_count} warnings (skipped files)")

    # Check for schema naming conflicts
    schema_mappings = {
        name: to_class_name(name) for name in result.spec.schemas.keys()
    }
    conflicts = detect_naming_conflicts(schema_mappings)
    if conflicts:
        print(f"  WARNING: {len(conflicts)} naming conflicts detected:", file=sys.stderr)
        for clean_name, originals in sorted(conflicts.items())[:5]:
            print(f"    {clean_name}: {originals}", file=sys.stderr)
        if len(conflicts) > 5:
            print(f"    ... and {len(conflicts) - 5} more", file=sys.stderr)

    # Emit generated code
    print(f"Generating code to {output_dir}...")
    emitter = Emitter()
    generated = emitter.emit(result.spec, output_dir)

    print(f"  Generated {len(generated)} files:")
    for path in generated:
        print(f"    - {path.name}")

    return True


def main() -> int:
    """Run the generator.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(
        description="Generate Python API client from OpenAPI specs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python -m generator spot --output generated/spot
    python -m generator umfutures --output generated/umfutures
    python -m generator --all --output generated
        """,
    )

    parser.add_argument(
        "spec",
        nargs="?",
        choices=list(SPEC_PATHS.keys()),
        help="Spec to generate (spot, umfutures, cmfutures)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate all specs",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=OUTPUT_PATHS.get("api", Path("generated")),
        help="Output directory",
    )

    args = parser.parse_args()

    if args.all:
        # Generate all specs
        success = True
        for spec_name in SPEC_PATHS:
            output_dir = args.output / spec_name
            if not generate_api(spec_name, output_dir):
                success = False
        return 0 if success else 1

    if not args.spec:
        parser.print_help()
        return 1

    # Generate single spec
    if generate_api(args.spec, args.output):
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
