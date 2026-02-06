# Phase 5: Testing & Polish Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Production-ready quality - fix type errors, add documentation, verify performance, and clean up legacy code.

**Architecture:** Add type annotations to legacy modules, create comprehensive README with usage examples, benchmark critical paths, and remove deprecated files while preserving backward compatibility exports.

**Tech Stack:** mypy for type checking, pytest-benchmark for performance tests, existing msgspec/aiohttp stack

---

## Prerequisites

Before starting Phase 5, **verify** each prerequisite:

### 1. Phase 4 Complete: Futures API Working

```bash
# Verify Futures API imports and works
python -c "
from binance import AsyncClient
from binance._schemas.futures import FuturesOrder, PositionRisk, MarkPrice
print('✓ Phase 4 Futures API verified')
"
```

### 2. All Unit Tests Pass

```bash
# Verify unit tests pass
python -m pytest tests/unit/ -q
# Expected: 289 passed
```

### 3. Ruff Linting Clean

```bash
# Verify ruff passes on new code
python -m ruff check binance/_core/ binance/_schemas/ binance/api/ binance/client.py
# Expected: All checks passed!
```

**If any prerequisite fails, fix it before proceeding.**

---

## Phase 5 File Structure

| File | Tasks | Description |
|------|-------|-------------|
| [01-type-annotations.md](./01-type-annotations.md) | 1-4 | Fix mypy errors in legacy modules |
| [02-documentation.md](./02-documentation.md) | 5-8 | Create README.md and API examples |
| [03-benchmarks.md](./03-benchmarks.md) | 9-11 | Performance verification |
| [04-cleanup.md](./04-cleanup.md) | 12-15 | Remove legacy files, update exports |

---

## Key Design Decisions

### 1. Type Annotation Strategy

**Scope:** Only add annotations to files we actively maintain. Legacy websocket code gets minimal fixes.

```python
# Priority 1: New _core/ modules (already typed)
# Priority 2: client.py, exceptions.py (need annotations)
# Priority 3: Legacy ws/ modules (minimal fixes, add # type: ignore where needed)
```

### 2. Documentation Approach

Create single comprehensive README.md with:
- Installation
- Quick start (5-line example)
- Common patterns (spot, futures)
- Error handling
- Configuration options

### 3. Benchmark Targets

| Operation | Target | Measurement |
|-----------|--------|-------------|
| Schema decode | < 1μs per object | pytest-benchmark |
| HTTP request overhead | < 1ms | End-to-end timing |
| Concurrent requests | Linear scaling | asyncio.gather |

### 4. Cleanup Strategy

**Remove:** Files that duplicate functionality now in `_core/`
**Keep:** Backward-compatible re-exports in `binance/__init__.py`

```python
# binance/__init__.py - Keep exports for backward compatibility
from binance.client import AsyncClient
from binance._core.exceptions import BinanceAPIError  # Re-export
```

---

## Target Output

### Type Checking

```bash
# Target: mypy passes on core modules
python -m mypy binance/_core/ binance/_schemas/ binance/client.py --ignore-missing-imports
# Expected: Success: no issues found
```

### Documentation

```
README.md              # New: Comprehensive usage guide
docs/
├── plans/            # Existing plans
└── api/              # Optional: Generated API docs
```

### Benchmarks

```
tests/benchmarks/
├── __init__.py
├── test_schema_decode.py
└── test_http_overhead.py
```

### Cleanup Result

```
binance/
├── __init__.py           # Updated exports
├── client.py             # Main entry point
├── exceptions.py         # Type-annotated
├── _core/                # Fully typed
├── _schemas/             # Fully typed
├── api/                  # Fully typed
└── ws/                   # Minimal type fixes
```

**Files to Remove:**
- `binance/base_client.py` (logic in _core/)
- `binance/async_client_core.py` (logic in _core/)
- `binance/enums.py` (replaced by Literals in _schemas/)

---

## Verification Milestones

| Milestone | Verification |
|-----------|--------------|
| Prerequisites pass | All 3 prerequisite checks pass |
| Core modules typed | `mypy binance/_core/ binance/_schemas/` passes |
| Client typed | `mypy binance/client.py` passes |
| README complete | README.md with install + quick start + examples |
| Benchmarks pass | Schema decode < 1μs, HTTP overhead < 1ms |
| Cleanup complete | Old files removed, imports still work |
| All tests pass | `pytest tests/unit/ tests/integration/` |

---

## Current Error Summary

```
mypy binance/ --ignore-missing-imports
# 174 [no-untyped-def]  - Functions missing type annotations
#  69 [no-untyped-call] - Calls to untyped functions
#  65 [type-arg]        - Missing type arguments
#  37 [misc]            - msgspec frozen inheritance (can ignore)
```

**Strategy:**
1. Fix `binance/exceptions.py` (17 errors)
2. Fix `binance/client.py` method signatures
3. Add `# type: ignore[misc]` for msgspec false positives
4. Use `--ignore-missing-imports` for third-party libs

---

## Start Implementation

**First**, run the prerequisite verification commands above.

**Then**, begin with [01-type-annotations.md](./01-type-annotations.md).
