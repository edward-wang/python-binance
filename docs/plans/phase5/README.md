# Phase 5: Testing & Polish

This directory contains the implementation plan for making the Binance Python wrapper production-ready.

## Quick Start

```bash
# Start implementation
# REQUIRED SUB-SKILL: Use superpowers:executing-plans

# Read the overview first
cat docs/plans/phase5/00-overview.md

# Then execute tasks in order (1-15)
```

## Plan Files

| File | Description | Tasks |
|------|-------------|-------|
| [00-overview.md](./00-overview.md) | Prerequisites, goals, verification milestones | - |
| [01-type-annotations.md](./01-type-annotations.md) | Fix mypy errors, add type hints | 1-4 |
| [02-documentation.md](./02-documentation.md) | README.md, examples, CHANGELOG | 5-8 |
| [03-benchmarks.md](./03-benchmarks.md) | Performance verification | 9-11 |
| [04-cleanup.md](./04-cleanup.md) | Remove legacy files, update exports | 12-15 |

## Summary

**Goal:** Production-ready quality

**Tasks:**
1. Fix type annotations (mypy passes)
2. Create documentation (README + examples)
3. Add benchmarks (verify performance)
4. Clean up legacy code (remove unused files)

## Prerequisites

Before starting Phase 5:

1. **Phase 4 complete:** Futures API working
2. **Unit tests passing:** 289 tests
3. **Ruff clean:** No linting errors

## Current Status

```bash
# Check mypy errors
python -m mypy binance/ --ignore-missing-imports 2>&1 | grep -c error
# Currently: ~174 errors (mostly legacy modules)

# After Phase 5:
# Core modules: 0 errors
# Legacy ws/: Ignored
```

## Estimated Scope

- **15 tasks** across 4 plan files
- **~500 lines** of new code (types, docs, benchmarks)
- **~750 lines** removed (legacy files)
- **3 new files** (README.md, CHANGELOG.md, examples/)

## Verification Milestones

| Milestone | Command |
|-----------|---------|
| Types pass | `mypy binance/_core/ binance/_schemas/` |
| Tests pass | `pytest tests/unit/ -q` |
| Lint passes | `ruff check binance/` |
| Benchmarks run | `pytest tests/benchmarks/ -v` |
| Import works | `from binance import AsyncClient` |
