# Phase 5.4: Cleanup

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Remove legacy files, update exports, verify backward compatibility.

**Prerequisites:** Tasks 1-11 complete (type annotations, docs, and benchmarks done)

---

## Task 12: Audit Legacy Files

**Files:**
- Read and analyze: `binance/base_client.py`
- Read and analyze: `binance/async_client_core.py`
- Read and analyze: `binance/enums.py`

**Step 1: Check what legacy files exist**

```bash
ls -la binance/*.py
wc -l binance/base_client.py binance/async_client_core.py binance/enums.py 2>/dev/null
```

**Step 2: Check what imports from legacy files**

```bash
# Check if anything imports from these files
grep -r "from binance.base_client" binance/ tests/ --include="*.py" || echo "No imports"
grep -r "from binance.async_client_core" binance/ tests/ --include="*.py" || echo "No imports"
grep -r "from binance.enums" binance/ tests/ --include="*.py" || echo "No imports"
```

**Step 3: Document findings**

Create a list of:
1. Files that can be safely deleted (nothing imports them)
2. Files that need re-exports preserved
3. Files that have active imports

**Step 4: Commit audit results as comment**

No commit for this task - just documentation for next steps.

---

## Task 13: Remove Legacy Files

**Files:**
- Delete: `binance/base_client.py` (if unused)
- Delete: `binance/async_client_core.py` (if unused)
- Delete: `binance/enums.py` (if unused)

**Step 1: Verify no active imports**

```bash
# Double-check nothing uses these
python -c "
from binance import AsyncClient
# If this works, we don't need base_client
print('✓ AsyncClient imports without base_client')
"
```

**Step 2: Remove unused legacy files**

```bash
# Only remove files confirmed unused in Task 12
git rm binance/base_client.py
git rm binance/async_client_core.py
git rm binance/enums.py
```

**Step 3: Run tests to verify nothing broke**

```bash
python -m pytest tests/unit/ -q -x
# Expected: 289 passed
```

**Step 4: Commit**

```bash
git commit -m "chore: remove legacy files

Removed:
- binance/base_client.py (logic moved to _core/)
- binance/async_client_core.py (logic moved to _core/)
- binance/enums.py (replaced by Literals in _schemas/)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 14: Update Package Exports

**Files:**
- Modify: `binance/__init__.py`

**Step 1: Read current __init__.py**

```bash
cat binance/__init__.py
```

**Step 2: Update exports for clean public API**

```python
# binance/__init__.py
"""Binance Python Wrapper - High-performance async client.

Quick Start:
    >>> from binance import AsyncClient
    >>> async with AsyncClient() as client:
    ...     ticker = await client.get_ticker_price(symbol="BTCUSDT")
    ...     print(ticker.price)
"""
from binance.client import AsyncClient

# Re-export common exceptions for convenience
from binance._core.exceptions import (
    BinanceAPIError,
    BinanceRequestError,
    ConnectionError,
    InvalidParameterError,
    InvalidSymbolError,
    NotFoundError,
    OrderError,
    RateLimitError,
    TimeoutError,
    TimestampError,
)

__version__ = "2.0.0"

__all__ = [
    # Main client
    "AsyncClient",
    # Exceptions
    "BinanceAPIError",
    "BinanceRequestError",
    "ConnectionError",
    "InvalidParameterError",
    "InvalidSymbolError",
    "NotFoundError",
    "OrderError",
    "RateLimitError",
    "TimeoutError",
    "TimestampError",
    # Version
    "__version__",
]
```

**Step 3: Verify imports work**

```bash
python -c "
from binance import AsyncClient, BinanceAPIError, __version__
print(f'Version: {__version__}')
print(f'AsyncClient: {AsyncClient}')
print(f'BinanceAPIError: {BinanceAPIError}')
print('✓ All exports work')
"
```

**Step 4: Run tests**

```bash
python -m pytest tests/unit/ -q -x
# Expected: 289 passed
```

**Step 5: Commit**

```bash
git add binance/__init__.py
git commit -m "chore: update package exports

- Clean public API with AsyncClient + exceptions
- Add __version__ = '2.0.0'
- Add module docstring with quick start

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 15: Final Verification

**Files:**
- No modifications - verification only

**Step 1: Run full test suite**

```bash
python -m pytest tests/unit/ -v
# Expected: 289 passed
```

**Step 2: Run mypy on core modules**

```bash
python -m mypy binance/_core/ binance/_schemas/ binance/client.py binance/api/ --ignore-missing-imports
# Expected: Success: no issues found
```

**Step 3: Run ruff linting**

```bash
python -m ruff check binance/
# Expected: All checks passed!
```

**Step 4: Verify imports and quick start**

```bash
python -c "
import asyncio
from binance import AsyncClient

async def test():
    async with AsyncClient(testnet=True) as client:
        ticker = await client.get_ticker_price(symbol='BTCUSDT')
        print(f'BTC: {ticker.price}')

        mark = await client.futures_get_mark_price(symbol='BTCUSDT')
        print(f'Futures mark: {mark.mark_price}')
    print('✓ Quick start works')

asyncio.run(test())
"
```

**Step 5: Check package structure**

```bash
# Final structure check
find binance -name "*.py" -type f | head -30
```

**Expected final structure:**

```
binance/
├── __init__.py           # Clean exports
├── client.py             # AsyncClient entry point
├── exceptions.py         # Backward-compat re-exports
├── helpers.py            # Utility functions
├── _core/
│   ├── __init__.py
│   ├── auth.py
│   ├── config.py
│   ├── context.py
│   ├── decoders.py
│   ├── exceptions.py
│   ├── formatters.py
│   └── http.py
├── _schemas/
│   ├── __init__.py
│   ├── common.py
│   ├── spot.py
│   └── futures.py
├── api/
│   ├── spot/
│   ├── futures_um/
│   └── futures_cm/
└── ws/                   # Legacy websocket (kept for now)
```

**Step 6: Create final summary commit**

```bash
git add -A
git status
# If there are any uncommitted changes, commit them

git log --oneline -10
# Review recent commits
```

---

## Verification Summary

| Check | Command | Expected |
|-------|---------|----------|
| Unit tests | `pytest tests/unit/ -q` | 289 passed |
| Type check | `mypy binance/_core/ binance/_schemas/` | Success |
| Lint | `ruff check binance/` | All passed |
| Import | `from binance import AsyncClient` | Works |
| Quick start | Run async example | Prints BTC price |

---

## Phase 5 Complete Checklist

- [ ] Task 1: exceptions.py typed
- [ ] Task 2: helpers.py typed
- [ ] Task 3: Schema type ignores added
- [ ] Task 4: mypy config in pyproject.toml
- [ ] Task 5: README.md created
- [ ] Task 6: Examples directory created
- [ ] Task 7: Package metadata updated
- [ ] Task 8: CHANGELOG.md created
- [ ] Task 9: Benchmark infrastructure
- [ ] Task 10: Schema decode benchmarks
- [ ] Task 11: HTTP performance benchmarks
- [ ] Task 12: Legacy file audit
- [ ] Task 13: Legacy files removed
- [ ] Task 14: Package exports updated
- [ ] Task 15: Final verification passed

---

## Next Steps After Phase 5

With Phase 5 complete, the wrapper is production-ready. Future work (from `docs/plans/binance-wrapper/08-future.md`):

| Priority | Feature | Description |
|----------|---------|-------------|
| **P0** | WebSocket Optimization | Zero-copy buffers, tagged unions |
| **P1** | Rate Limiter | Multi-level throttling |
| **P1** | Margin API | Cross/isolated margin |
| **P2** | AI Tool Export | OpenAI/Claude function calling |
| **P2** | .pyi Stubs | Enhanced IDE support |
