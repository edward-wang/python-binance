# Section 1: Project Overview & Goals

## Mission

Build an AI-friendly, ultra-low latency Binance Python wrapper, generated from OpenXAPI specs.

## Core Principles

| Principle | Implementation |
|-----------|----------------|
| **Spec-driven** | Generate wrapper from OpenXAPI specs (single source of truth) |
| **Async-only** | No sync API - simplifies codebase by 50% |
| **Declarative endpoints** | Endpoint definitions → method generation |
| **Schema-driven** | msgspec models for input validation and output parsing |
| **Atomic files** | Every module < 300 lines (fits AI context) |
| **Ultra-low latency** | Optimized for high-frequency trading |

## Performance Stack

| Component | Choice | Why |
|-----------|--------|-----|
| **Event loop** | uvloop | 2-4x faster than asyncio |
| **HTTP client** | aiohttp + connection pooling | Proven, fast, reuse connections |
| **JSON** | orjson | 3-10x faster than stdlib json |
| **Data models** | msgspec | 2-5x faster than Pydantic, low memory |
| **Timestamps** | int (milliseconds) | Zero parsing overhead |
| **Classes** | `__slots__` | Reduced memory, faster attribute access |
| **Numeric types** | float (format to str at order time) | Hardware accelerated math |

## Approach

| Step | Description |
|------|-------------|
| 1. Get specs | Download OpenXAPI spec files (one-time) |
| 2. Build generator | Python script that reads specs → outputs wrapper |
| 3. Generate code | Run generator to create `api/` and `_schemas/` |
| 4. Hand-write core | Auth, HTTP, exceptions (reuse existing logic, optimize) |
| 5. Manual maintenance | Update manually when Binance changes (rare) |

## Scope

### In Scope (MVP)

- REST API wrapper (generated from specs)
- Code generator from OpenXAPI specs
- `_core/` infrastructure (auth, http, exceptions, context)
- msgspec schemas with Annotated descriptions
- Exception hierarchy with error code mapping
- Time synchronization (server time offset)

### Out of Scope (Future Work)

| Feature | Priority | Notes |
|---------|----------|-------|
| WebSocket optimization | P0 | Tagged Unions, zero-copy buffers |
| Rate limiter middleware | P1 | Multi-level warnings |
| Margin API | P1 | Cross/isolated margin |
| `.pyi` stub generation | P2 | Enhanced IDE support |
| AI tool schema export | P2 | OpenAI/Claude function calling |
| Options API | P3 | On demand |
| Protocol interfaces | P3 | For testing/mocking |

## Constraints

- Solo developer
- MVP-first (no over-engineering)
- Zero backward compatibility concerns (no existing users)
- Binance API changes infrequently (manual updates acceptable)

## Non-Goals

- Migrating from existing 17K-line client.py
- Sync client support
- Continuous automation pipeline (Go program, GitHub Actions)
- WebSocket refactoring in MVP (keep existing `ws/` as-is)
