# Phase 2: Code Generator - Overview

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a code generator that parses OpenAPI YAML specs and outputs typed Python client code.

**Architecture:** The generator reads individual endpoint YAML files from `specs/openapi/`, parses them into an internal model (dataclasses), then uses Jinja2 templates to emit Python code. Schema deduplication ensures shared types are generated once.

**Tech Stack:** PyYAML (parsing), Jinja2 (templating), pathlib (file handling), dataclasses (internal model)

---

## Plan Files

| File | Tasks | Description |
|------|-------|-------------|
| [01-foundation.md](01-foundation.md) | 0-4 | Spec analysis, dependencies, package structure, config, models |
| [02-parser.md](02-parser.md) | 5-9 | YAML parsing, parameters, schemas, endpoints, directory parser |
| [03-templates-emitter.md](03-templates-emitter.md) | 10-12 | Jinja2 templates and code emitter |
| [04-cli-integration.md](04-cli-integration.md) | 13-15 | CLI, integration tests, final verification |

---

## Spec File Format Summary

Each endpoint file (e.g., `specs/openapi/spot/get_api_v3_klines.yaml`) contains:
- `components.schemas` - Request/response schema definitions
- `components.securitySchemes` - API key definition (if authenticated)
- `paths.{path}.{method}` - Endpoint definition with parameters, requestBody, responses, security

**Key patterns to handle:**
1. **Public endpoints** - No `security` section (e.g., `/api/v3/time`, `/api/v3/klines`)
2. **Signed endpoints** - Has `security` + `timestamp` parameter (e.g., `/api/v3/account`, `/api/v3/order`)
3. **Response types** - Object (`$ref`), array (`items.$ref`), raw array (`items.oneOf`)
4. **Parameters** - Query params with `required`, `default`, `type`, `format`, `enum`

---

## Dependency Graph

```
Task 0 (Spec Analysis) ──────────────┐ ← Do this first to understand patterns
    ↓                                │
Task 1 (Dependencies)                │
    ↓                                │
Task 2 (Package Structure)           │
    ↓                                │
Task 3 (Config) ─────────────────────┤
    ↓                                │
Task 4 (Models) ←────────────────────┤ ← Informed by Task 0 findings
    ↓                                │
Task 5 (Parser Basic)                │
    ↓                                │
Task 6 (Parameter Parsing)           │
    ↓                                │
Task 7 (Schema Parsing)              │
    ↓                                │
Task 8 (Endpoint Parsing)            │
    ↓                                │
Task 9 (Directory Parser)            │
    ↓                                │
Task 10 (Schema Template) ←──────────┘
    ↓
Task 11 (Endpoint Template)
    ↓
Task 12 (Emitter) ←── Task 10, 11, includes ruff formatting
    ↓
Task 13 (CLI Main) ←── Task 9, 12
    ↓
Task 14 (Integration Test)
    ↓
Task 15 (Final Verification)
```

---

## Generation Metadata

All generated files include:
- Generation timestamp (consistent across files in same run)
- Source spec directory path
- "DO NOT EDIT" warning with regeneration command
- Formatted with `ruff format` for consistent style

---

## Cross-References

When a task references another task's output:
- Models defined in Task 4 → see [01-foundation.md#task-4](01-foundation.md#task-4-implement-generator-models)
- Config functions → see [01-foundation.md#task-3](01-foundation.md#task-3-implement-generator-config)
- Parser functions → see [02-parser.md](02-parser.md)
- Templates → see [03-templates-emitter.md](03-templates-emitter.md)
