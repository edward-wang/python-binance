# Phase 3.1: Generate Spot API Endpoints

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Run the generator to produce `binance/api/spot/` modules from OpenAPI specs.

**Prerequisites:** Phase 2 generator complete, specs in `specs/openapi/spot/`

---

## Task 1: Verify Generator and Specs

**Files:**
- Check: `generator/__main__.py`
- Check: `specs/openapi/spot/*.yaml`

**Step 1: Verify generator runs**

Run: `python -m generator --help`
Expected: Help output showing available commands

**Step 2: Check spec files exist**

Run: `ls specs/openapi/spot/get_api_v3_klines.yaml specs/openapi/spot/post_api_v3_order.yaml`
Expected: Files exist

**Step 3: Count spec files**

Run: `ls specs/openapi/spot/*.yaml | wc -l`
Expected: ~300+ files (we'll filter to core ~50 for MVP)

**Step 4: Commit (if any fixes needed)**

If generator needed fixes, commit them:
```bash
git add generator/
git commit -m "fix: generator adjustments for phase 3"
```

---

## Task 2: Create API Package Structure

**Files:**
- Create: `binance/api/__init__.py`
- Create: `binance/api/spot/__init__.py`
- Create: `tests/unit/api/__init__.py`
- Create: `tests/unit/api/test_spot_imports.py`

**Step 1: Write the failing test**

```python
# tests/unit/api/__init__.py
# (empty file)
```

```python
# tests/unit/api/test_spot_imports.py
"""Test that spot API package structure exists."""


def test_api_package_importable():
    """Test that api package exists."""
    import binance.api
    assert binance.api.__name__ == "binance.api"


def test_spot_package_importable():
    """Test that spot package exists."""
    import binance.api.spot
    assert binance.api.spot.__name__ == "binance.api.spot"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/api/test_spot_imports.py -v`
Expected: FAIL with "No module named 'binance.api'"

**Step 3: Create package structure**

```python
# binance/api/__init__.py
"""Generated API modules for Binance endpoints.

Each subpackage (spot, futures_um, etc.) contains endpoint methods
grouped by functionality (general, market, trade, account).
"""
```

```python
# binance/api/spot/__init__.py
"""Spot API endpoints.

Modules:
- general: ping, time, exchange_info
- market: klines, depth, trades, ticker
- trade: orders, cancel
- account: account info, my_trades
"""
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/unit/api/test_spot_imports.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add binance/api/ tests/unit/api/
git commit -m "feat: create api package structure for spot endpoints"
```

---

## Task 3: Run Generator for Spot Endpoints

**Files:**
- Run: `python -m generator spot`
- Check: `binance/api/spot/general.py`
- Check: `binance/api/spot/market.py`
- Check: `binance/api/spot/trade.py`
- Check: `binance/api/spot/account.py`

**Step 1: Run generator for spot API**

Run: `python -m generator spot`
Expected output:
```
Parsing specs/openapi/spot...
  ✓ Parsed 50 endpoint files
Generating binance/api/spot/...
  ✓ binance/api/spot/general.py (3 endpoints)
  ✓ binance/api/spot/market.py (8 endpoints)
  ✓ binance/api/spot/trade.py (6 endpoints)
  ✓ binance/api/spot/account.py (3 endpoints)
Done!
```

**Step 2: Verify generated files exist**

Run: `ls -la binance/api/spot/`
Expected: `__init__.py`, `general.py`, `market.py`, `trade.py`, `account.py`

**Step 3: Check syntax validity**

Run: `python -c "from binance.api.spot import general, market, trade, account"`
Expected: No errors

**Step 4: Review generated general.py**

Read `binance/api/spot/general.py` and verify it looks like:

```python
"""Spot General API endpoints.

Generated from OpenAPI specs. Do not edit manually.
"""
from typing import Any
from binance._core.http import HTTPClient


async def ping(http: HTTPClient) -> dict[str, Any]:
    """Test connectivity to the Rest API.

    Weight: 1

    Returns:
        Empty dict on success
    """
    return await http.request("GET", "/api/v3/ping")


async def get_server_time(http: HTTPClient) -> dict[str, Any]:
    """Test connectivity and get current server time.

    Weight: 1

    Returns:
        Server time in milliseconds
    """
    return await http.request("GET", "/api/v3/time")


async def get_exchange_info(
    http: HTTPClient,
    symbol: str | None = None,
    symbols: list[str] | None = None,
    permissions: list[str] | None = None,
) -> dict[str, Any]:
    """Get current exchange trading rules and symbol information.

    Weight: 20

    Args:
        symbol: Trading pair (e.g., "BTCUSDT")
        symbols: List of trading pairs
        permissions: Filter by permissions

    Returns:
        Exchange information including trading rules
    """
    params: dict[str, Any] = {}
    if symbol is not None:
        params["symbol"] = symbol
    if symbols is not None:
        params["symbols"] = symbols
    if permissions is not None:
        params["permissions"] = permissions
    return await http.request("GET", "/api/v3/exchangeInfo", params=params)
```

**Step 5: Review generated market.py**

Verify `binance/api/spot/market.py` has klines, depth, etc. with proper type hints.

**Step 6: Review generated trade.py**

Verify `binance/api/spot/trade.py` has create_order with `signed=True`.

Example expected pattern:
```python
async def create_order(
    http: HTTPClient,
    symbol: str,
    side: str,
    type: str,
    quantity: str | None = None,
    price: str | None = None,
    time_in_force: str | None = None,
    # ... more params
) -> dict[str, Any]:
    """Create a new order.

    Weight: 1

    Args:
        symbol: Trading pair
        side: BUY or SELL
        type: Order type (LIMIT, MARKET, etc.)
        ...

    Returns:
        Order response
    """
    params: dict[str, Any] = {
        "symbol": symbol,
        "side": side,
        "type": type,
    }
    if quantity is not None:
        params["quantity"] = quantity
    # ... build params
    return await http.request("POST", "/api/v3/order", signed=True, params=params)
```

**Step 7: Run mypy**

Run: `mypy binance/api/spot/ --strict`
Expected: Success (or minor issues to fix)

**Step 8: Fix any generator issues**

If generated code has issues, fix in generator and re-run:
```bash
# Fix generator
# Re-run: python -m generator spot
```

**Step 9: Commit generated code**

```bash
git add binance/api/spot/
git commit -m "feat: generate spot API endpoints from OpenAPI specs"
```

---

## Task 3.1: Manual Review and Fixes

**Purpose:** Generator output may need manual tweaks for edge cases.

**Step 1: Check klines endpoint**

The klines endpoint returns `list[list[int | str]]`, not a typed struct.
Verify `market.py` handles this:

```python
async def get_klines(
    http: HTTPClient,
    symbol: str,
    interval: str,
    start_time: int | None = None,
    end_time: int | None = None,
    limit: int = 500,
) -> list[list[int | str]]:
    """Get Kline/candlestick bars for a symbol.

    Weight: 2

    Args:
        symbol: Trading pair (e.g., "BTCUSDT")
        interval: Kline interval (e.g., "1h", "1d")
        start_time: Start time in milliseconds
        end_time: End time in milliseconds
        limit: Number of results (default 500, max 1000)

    Returns:
        List of klines, each kline is [open_time, open, high, low, close, volume, ...]
    """
    params: dict[str, Any] = {
        "symbol": symbol,
        "interval": interval,
    }
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if limit != 500:
        params["limit"] = limit
    return await http.request("GET", "/api/v3/klines", params=params)
```

**Step 2: Check depth endpoint**

Verify depth returns proper structure:

```python
async def get_order_book(
    http: HTTPClient,
    symbol: str,
    limit: int = 100,
) -> dict[str, Any]:
    """Get order book depth.

    Weight: 5-50 depending on limit

    Args:
        symbol: Trading pair
        limit: Depth limit (5, 10, 20, 50, 100, 500, 1000, 5000)

    Returns:
        Order book with bids and asks
    """
    params: dict[str, Any] = {
        "symbol": symbol,
    }
    if limit != 100:
        params["limit"] = limit
    return await http.request("GET", "/api/v3/depth", params=params)
```

**Step 3: Check signed endpoints have `signed=True`**

Verify all endpoints in `trade.py` and `account.py` use `signed=True`:

```python
# In trade.py
return await http.request("POST", "/api/v3/order", signed=True, params=params)

# In account.py
return await http.request("GET", "/api/v3/account", signed=True, params=params)
```

**Step 4: If manual fixes needed, apply and commit**

```bash
git add binance/api/spot/
git commit -m "fix: manual adjustments to generated spot endpoints"
```

---

## Next Steps

Continue with [02-generate-schemas.md](./02-generate-schemas.md) to generate typed response schemas.
