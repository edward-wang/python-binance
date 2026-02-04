"""Emit generated Python code from parsed OpenAPI specs.

Combines parsed data with Jinja2 templates to generate typed Python client code.
"""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from jinja2 import Environment, PackageLoader

from generator.models import Endpoint, ParsedSpec, Schema


class Emitter:
    """Code emitter that renders templates with parsed spec data."""

    def __init__(self) -> None:
        """Initialize the emitter with Jinja2 environment."""
        self.env = Environment(
            loader=PackageLoader("generator", "templates"),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render_schemas(
        self,
        api_name: str,
        schemas: dict[str, Schema],
    ) -> str:
        """Render the schemas module.

        Args:
            api_name: API name (e.g., "Spot", "UMFutures")
            schemas: Dictionary of schema name -> Schema

        Returns:
            Rendered Python code
        """
        template = self.env.get_template("schema.py.j2")

        # Check if any schema has Literal types in properties
        has_literal = any(
            "Literal[" in prop.type
            for schema in schemas.values()
            for prop in schema.properties
        )

        return template.render(
            api_name=api_name,
            schemas=list(schemas.values()),
            has_literal_types=has_literal,
        )

    def render_endpoints(
        self,
        api_name: str,
        module: str,
        endpoints: list[Endpoint],
        schemas: dict[str, Schema],
    ) -> str:
        """Render an endpoint module.

        Args:
            api_name: API name (e.g., "Spot")
            module: Module name (e.g., "market", "trade")
            endpoints: List of endpoints for this module
            schemas: Dictionary of all schemas

        Returns:
            Rendered Python code
        """
        template = self.env.get_template("endpoint.py.j2")

        # Collect schema imports needed
        schema_imports = set()
        for endpoint in endpoints:
            if endpoint.response_schema:
                schema_imports.add(endpoint.response_schema)

        # Determine if Literal types are used
        has_literal = self.has_literal_types(endpoints)

        # Convert module name to class name
        module_class = module.title()
        client_class = f"{api_name}Client"

        return template.render(
            api_name=api_name,
            module=module,
            module_class=module_class,
            client_class=client_class,
            endpoints=endpoints,
            schema_imports=sorted(schema_imports),
            has_literal_types=has_literal,
        )

    def group_by_module(
        self,
        endpoints: list[Endpoint],
    ) -> dict[str, list[Endpoint]]:
        """Group endpoints by their module.

        Args:
            endpoints: List of all endpoints

        Returns:
            Dictionary of module name -> list of endpoints
        """
        grouped: dict[str, list[Endpoint]] = defaultdict(list)
        for endpoint in endpoints:
            grouped[endpoint.module].append(endpoint)
        return dict(grouped)

    def has_literal_types(self, endpoints: list[Endpoint]) -> bool:
        """Check if any endpoint uses Literal types.

        Args:
            endpoints: List of endpoints to check

        Returns:
            True if Literal types are used
        """
        for endpoint in endpoints:
            for param in endpoint.parameters:
                if "Literal[" in param.type:
                    return True
        return False

    def emit(
        self,
        spec: ParsedSpec,
        output_dir: Path,
    ) -> list[Path]:
        """Emit generated code to output directory.

        Args:
            spec: Parsed spec data
            output_dir: Directory to write generated files

        Returns:
            List of generated file paths
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        generated_files: list[Path] = []

        # Convert spec name to API name (e.g., "spot" -> "Spot")
        api_name = spec.name.title()

        # Generate schemas module
        schemas_content = self.render_schemas(api_name, spec.schemas)
        schemas_path = output_dir / "schemas.py"
        schemas_path.write_text(schemas_content)
        generated_files.append(schemas_path)

        # Group endpoints by module and generate each
        grouped = self.group_by_module(spec.endpoints)
        for module, endpoints in grouped.items():
            content = self.render_endpoints(
                api_name=api_name,
                module=module,
                endpoints=endpoints,
                schemas=spec.schemas,
            )
            module_path = output_dir / f"{module}.py"
            module_path.write_text(content)
            generated_files.append(module_path)

        return generated_files
