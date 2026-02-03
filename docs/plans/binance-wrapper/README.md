# Binance Python Wrapper - Design Document

## Overview

This document describes the architecture and implementation plan for a high-performance, AI-friendly Binance Python wrapper.

**Created:** 2026-02-03
**Status:** Design Complete, Ready for Implementation

## Design Principles

| Principle | Implementation |
|-----------|----------------|
| **Spec-driven** | Generate wrapper from OpenXAPI specs |
| **Async-only** | No sync API - simplifies codebase |
| **Ultra-low latency** | msgspec, orjson, uvloop, float for calculations |
| **Atomic files** | Every module < 300 lines |
| **AI-friendly** | Annotated descriptions for both humans and LLMs |

## Performance Stack

| Component | Choice |
|-----------|--------|
| Event loop | uvloop |
| HTTP client | aiohttp + connection pooling |
| JSON | orjson |
| Data models | msgspec |
| Numeric types | float (format to str at order time) |

## Document Structure

| Document | Description |
|----------|-------------|
| [01-overview.md](./01-overview.md) | Project goals, principles, constraints |
| [02-architecture.md](./02-architecture.md) | Directory structure, module organization |
| [03-core.md](./03-core.md) | Core infrastructure (_core/) |
| [04-generator.md](./04-generator.md) | Code generation system |
| [05-schemas.md](./05-schemas.md) | msgspec schemas and patterns |
| [06-exceptions.md](./06-exceptions.md) | Exception hierarchy and error handling |
| [07-phases.md](./07-phases.md) | Implementation roadmap |
| [08-future.md](./08-future.md) | Future work and optimizations |

## Quick Links

- **Start implementation:** [07-phases.md](./07-phases.md)
- **Core design:** [03-core.md](./03-core.md)
- **Schema patterns:** [05-schemas.md](./05-schemas.md)
- **WebSocket optimization:** [08-future.md](./08-future.md)

## Implementation Status

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 1 | Not Started | Foundation (_core/) |
| Phase 2 | Not Started | Code Generator |
| Phase 3 | Not Started | Spot API |
| Phase 4 | Not Started | Futures API |
| Phase 5 | Not Started | Testing & Polish |
