# Phase 5.1: Type Annotations

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix mypy errors to achieve type-safe core modules.

**Prerequisites:** Phase 4 complete, all unit tests passing

---

## Task 1: Fix exceptions.py Type Annotations

**Files:**
- Modify: `binance/exceptions.py`

**Step 1: Read current file**

```bash
cat binance/exceptions.py
```

**Step 2: Add type annotations to all functions**

The legacy `exceptions.py` has wrapper functions without type annotations. Add them:

```python
# binance/exceptions.py
"""Legacy exception wrappers for backward compatibility.

New code should import from binance._core.exceptions directly.
"""
from __future__ import annotations

from binance._core.exceptions import (
    BinanceAPIError,
    BinanceRequestError,
    BinanceWebSocketError,
    ConnectionError,
    InvalidParameterError,
    InvalidSymbolError,
    NotFoundError,
    OrderError,
    RateLimitError,
    TimeoutError,
    TimestampError,
)

__all__ = [
    "BinanceAPIError",
    "BinanceRequestError",
    "BinanceWebSocketError",
    "ConnectionError",
    "InvalidParameterError",
    "InvalidSymbolError",
    "NotFoundError",
    "OrderError",
    "RateLimitError",
    "TimeoutError",
    "TimestampError",
]


# Legacy factory functions - keep for backward compatibility
def api_error(code: int, message: str) -> BinanceAPIError:
    """Create a BinanceAPIError."""
    return BinanceAPIError(code, message)


def request_error(message: str) -> BinanceRequestError:
    """Create a BinanceRequestError."""
    return BinanceRequestError(message)


def timeout_error(message: str) -> TimeoutError:
    """Create a TimeoutError."""
    return TimeoutError(message)


def connection_error(message: str) -> ConnectionError:
    """Create a ConnectionError."""
    return ConnectionError(message)


def websocket_error(message: str) -> BinanceWebSocketError:
    """Create a BinanceWebSocketError."""
    return BinanceWebSocketError(message)
```

**Step 3: Verify mypy passes**

```bash
python -m mypy binance/exceptions.py --ignore-missing-imports
# Expected: Success: no issues found
```

**Step 4: Run tests**

```bash
python -m pytest tests/unit/ -q -x
# Expected: 289 passed
```

**Step 5: Commit**

```bash
git add binance/exceptions.py
git commit -m "fix: add type annotations to exceptions.py

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 2: Fix helpers.py Type Annotations

**Files:**
- Modify: `binance/helpers.py`

**Step 1: Read current file**

```bash
cat binance/helpers.py
```

**Step 2: Add type annotations**

```python
# binance/helpers.py
"""Helper utilities for the Binance client."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from binance._core.formatters import (
    format_price,
    format_quantity,
    interval_to_ms,
)

__all__ = [
    "format_price",
    "format_quantity",
    "interval_to_ms",
    "date_to_milliseconds",
    "round_step_size",
]


def date_to_milliseconds(date_str: str) -> int:
    """Convert date string to milliseconds timestamp.

    Args:
        date_str: Date in format 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'

    Returns:
        Milliseconds since epoch
    """
    formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return int(dt.timestamp() * 1000)
        except ValueError:
            continue
    raise ValueError(f"Invalid date format: {date_str}")


def round_step_size(
    quantity: float | str,
    step_size: float | str,
) -> str:
    """Round quantity to valid step size.

    Args:
        quantity: The quantity to round
        step_size: The minimum step size (e.g., "0.001")

    Returns:
        Quantity rounded to step size as string
    """
    qty = float(quantity)
    step = float(step_size)

    # Calculate precision from step size
    step_str = f"{step:.10f}".rstrip("0")
    if "." in step_str:
        precision = len(step_str.split(".")[1])
    else:
        precision = 0

    # Round to step
    rounded = round(qty / step) * step
    return f"{rounded:.{precision}f}"
```

**Step 3: Verify mypy passes**

```bash
python -m mypy binance/helpers.py --ignore-missing-imports
# Expected: Success: no issues found
```

**Step 4: Run tests**

```bash
python -m pytest tests/unit/ -q -x
# Expected: 289 passed
```

**Step 5: Commit**

```bash
git add binance/helpers.py
git commit -m "fix: add type annotations to helpers.py

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 3: Add msgspec Type Ignores to Schemas

**Files:**
- Modify: `binance/_schemas/spot.py`
- Modify: `binance/_schemas/futures.py`

**Context:** mypy reports false positives for msgspec frozen inheritance. Add targeted ignores.

**Step 1: Check current errors**

```bash
python -m mypy binance/_schemas/ --ignore-missing-imports 2>&1 | head -20
```

**Step 2: Add module-level type ignore for msgspec**

Add to the top of each schema file (after imports):

```python
# binance/_schemas/spot.py
# ... existing imports ...

# mypy doesn't understand msgspec's frozen inheritance pattern
# type: ignore[misc] for "Cannot inherit non-frozen dataclass from a frozen one"
```

**Alternative approach - use pyproject.toml:**

```toml
# pyproject.toml - add mypy config
[tool.mypy]
ignore_missing_imports = true

[[tool.mypy.overrides]]
module = "binance._schemas.*"
disable_error_code = ["misc"]
```

**Step 3: Verify mypy passes for schemas**

```bash
python -m mypy binance/_schemas/ --ignore-missing-imports
# Expected: Success or only misc errors (which we ignore)
```

**Step 4: Run tests**

```bash
python -m pytest tests/unit/schemas/ -q
# Expected: All schema tests pass
```

**Step 5: Commit**

```bash
git add binance/_schemas/ pyproject.toml
git commit -m "fix: configure mypy to ignore msgspec false positives

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 4: Create mypy Configuration

**Files:**
- Modify: `pyproject.toml`

**Step 1: Read current pyproject.toml**

```bash
cat pyproject.toml
```

**Step 2: Add mypy configuration section**

```toml
# Add to pyproject.toml

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_ignores = true
ignore_missing_imports = true
strict_optional = true

# Core modules - strict typing
[[tool.mypy.overrides]]
module = [
    "binance._core.*",
    "binance._schemas.*",
    "binance.api.*",
    "binance.client",
]
disallow_untyped_defs = true
disallow_incomplete_defs = true

# Legacy modules - relaxed typing
[[tool.mypy.overrides]]
module = [
    "binance.ws.*",
    "binance.base_client",
    "binance.async_client_core",
]
disallow_untyped_defs = false
ignore_errors = true

# msgspec schemas - ignore frozen inheritance false positive
[[tool.mypy.overrides]]
module = "binance._schemas.*"
disable_error_code = ["misc"]
```

**Step 3: Verify mypy passes on core modules**

```bash
python -m mypy binance/_core/ binance/_schemas/ binance/client.py binance/api/
# Expected: Success: no issues found (or only acceptable warnings)
```

**Step 4: Run full test suite**

```bash
python -m pytest tests/unit/ -q
# Expected: 289 passed
```

**Step 5: Commit**

```bash
git add pyproject.toml
git commit -m "chore: add mypy configuration for type checking

- Strict typing for core modules (_core/, _schemas/, api/, client.py)
- Relaxed typing for legacy ws/ modules
- Ignore msgspec frozen inheritance false positives

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Verification

After completing all tasks:

```bash
# Core modules should pass strict mypy
python -m mypy binance/_core/ binance/_schemas/ binance/client.py binance/api/ --ignore-missing-imports

# All tests should still pass
python -m pytest tests/unit/ -q

# Expected output:
# Success: no issues found in X source files
# 289 passed
```
