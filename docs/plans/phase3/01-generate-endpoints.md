# Phase 3.1: Generate Spot API Endpoints

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Run the generator to produce `binance/api/spot/` modules with **typed returns**.

**Prerequisites:** Phase 2 generator complete, specs in `specs/openapi/spot/`

---

## Task 1: Verify Generator Output Quality

**Purpose:** Ensure generator produces valid, usable code before proceeding.

**Files:**
- Check: `generator/__main__.py`
- Check: `specs/openapi/spot/*.yaml`

**Step 1: Run generator on a single file to verify output**

```bash
# Generate just one endpoint to verify quality
python -c "
from generator.parser import parse_yaml_file, extract_path_and_method, parse_endpoint
from generator.emitter import render_endpoint
from pathlib import Path

spec = parse_yaml_file(Path('specs/openapi/spot/get_api_v3_time.yaml'))
path, method, operation = extract_path_and_method(spec)
endpoint = parse_endpoint(path, method, operation, spec.get('components', {}))
code = render_endpoint(endpoint)
print(code)
"
```

Expected output should include:
- Proper imports
- Async function definition
- Type hints
- Docstring with weight

**Step 2: Verify output compiles**

```bash
python -c "
from generator.parser import parse_yaml_file, extract_path_and_method, parse_endpoint
from generator.emitter import render_endpoint
from pathlib import Path

spec = parse_yaml_file(Path('specs/openapi/spot/get_api_v3_time.yaml'))
path, method, operation = extract_path_and_method(spec)
endpoint = parse_endpoint(path, method, operation, spec.get('components', {}))
code = render_endpoint(endpoint)

# Verify it compiles
compile(code, '<generated>', 'exec')
print('✓ Generated code compiles')
"
```

**Step 3: Count spec files**

Run: `ls specs/openapi/spot/get_api_v3*.yaml specs/openapi/spot/post_api_v3*.yaml specs/openapi/spot/delete_api_v3*.yaml | wc -l`
Expected: ~30 core API v3 files

**Step 4: Document any generator fixes needed**

If generator output has issues, note them for fixing:
```bash
# Example issues to check:
# - Missing imports
# - Wrong parameter names
# - Missing signed=True for authenticated endpoints
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

All methods return typed msgspec schemas, not raw dicts.
"""
```

```python
# binance/api/spot/__init__.py
"""Spot API endpoints with typed returns.

Modules:
- general: ping, get_server_time, get_exchange_info
- market: get_klines, get_order_book, get_trades, get_ticker_*
- trade: create_order, cancel_order, get_order
- account: get_account, get_my_trades

All methods return msgspec schema types for type safety.
"""
from binance.api.spot import general, market, trade, account

__all__ = ["general", "market", "trade", "account"]
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

## Task 3: Run Generator for Spot Endpoints (Typed Returns)

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
  ✓ Parsed 20 endpoint files
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

**Step 4: Review generated general.py for typed returns**

The generated code should use typed returns:

```python
# binance/api/spot/general.py
"""Spot General API endpoints.

Generated from OpenAPI specs. Do not edit manually.
"""
from typing import Any

import msgspec

from binance._core.http import HTTPClient
from binance._schemas.spot import ServerTime, ExchangeInfo

# Pre-compiled decoders for performance
_server_time_decoder = msgspec.json.Decoder(ServerTime)
_exchange_info_decoder = msgspec.json.Decoder(ExchangeInfo)


async def ping(http: HTTPClient) -> dict[str, Any]:
    """Test connectivity to the Rest API.

    Weight: 1

    Returns:
        Empty dict on success
    """
    return await http.request("GET", "/api/v3/ping")


async def get_server_time(http: HTTPClient) -> ServerTime:
    """Test connectivity and get current server time.

    Weight: 1

    Returns:
        ServerTime with server_time field in milliseconds
    """
    raw = await http.request_raw("GET", "/api/v3/time")
    return _server_time_decoder.decode(raw)


async def get_exchange_info(
    http: HTTPClient,
    symbol: str | None = None,
    symbols: list[str] | None = None,
    permissions: list[str] | None = None,
) -> ExchangeInfo:
    """Get current exchange trading rules and symbol information.

    Weight: 20

    Args:
        symbol: Trading pair (e.g., "BTCUSDT")
        symbols: List of trading pairs
        permissions: Filter by permissions

    Returns:
        ExchangeInfo with symbols and rate limits
    """
    params: dict[str, Any] = {}
    if symbol is not None:
        params["symbol"] = symbol
    if symbols is not None:
        params["symbols"] = symbols
    if permissions is not None:
        params["permissions"] = permissions
    raw = await http.request_raw("GET", "/api/v3/exchangeInfo", params=params)
    return _exchange_info_decoder.decode(raw)
```

**Step 5: Review generated market.py for typed returns**

```python
# binance/api/spot/market.py (key patterns)
from binance._schemas.spot import (
    OrderBook, Trade, AggTrade, AvgPrice, Kline,
    Ticker24h, TickerPrice, BookTicker,
)

_order_book_decoder = msgspec.json.Decoder(OrderBook)
_trade_list_decoder = msgspec.json.Decoder(list[Trade])
_ticker_price_decoder = msgspec.json.Decoder(TickerPrice)
_ticker_price_list_decoder = msgspec.json.Decoder(list[TickerPrice])


async def get_order_book(
    http: HTTPClient,
    symbol: str,
    limit: int = 100,
) -> OrderBook:
    """Get order book depth."""
    params: dict[str, Any] = {"symbol": symbol}
    if limit != 100:
        params["limit"] = limit
    raw = await http.request_raw("GET", "/api/v3/depth", params=params)
    return _order_book_decoder.decode(raw)


async def get_trades(
    http: HTTPClient,
    symbol: str,
    limit: int = 500,
) -> list[Trade]:
    """Get recent trades."""
    params: dict[str, Any] = {"symbol": symbol}
    if limit != 500:
        params["limit"] = limit
    raw = await http.request_raw("GET", "/api/v3/trades", params=params)
    return _trade_list_decoder.decode(raw)


# For klines - convert raw arrays to typed Kline objects
async def get_klines(
    http: HTTPClient,
    symbol: str,
    interval: str,
    start_time: int | None = None,
    end_time: int | None = None,
    limit: int = 500,
) -> list[Kline]:
    """Get Kline/candlestick bars for a symbol.

    Returns typed Kline objects with named fields for AI-friendliness.

    Args:
        symbol: Trading pair (e.g., "BTCUSDT")
        interval: Kline interval (1m, 5m, 15m, 1h, 4h, 1d, etc.)
        start_time: Start time in milliseconds
        end_time: End time in milliseconds
        limit: Number of klines (max 1000, default 500)

    Returns:
        List of Kline objects with open, high, low, close, volume, etc.
    """
    params: dict[str, Any] = {"symbol": symbol, "interval": interval}
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if limit != 500:
        params["limit"] = limit
    raw = await http.request("GET", "/api/v3/klines", params=params)
    return [Kline.from_raw(k) for k in raw]


# For ticker endpoints with single/multiple return types
async def get_ticker_price(
    http: HTTPClient,
    symbol: str | None = None,
    symbols: list[str] | None = None,
) -> TickerPrice | list[TickerPrice]:
    """Get symbol price ticker.

    Returns single TickerPrice if symbol specified, else list.
    """
    params: dict[str, Any] = {}
    if symbol is not None:
        params["symbol"] = symbol
    if symbols is not None:
        params["symbols"] = symbols

    raw = await http.request_raw("GET", "/api/v3/ticker/price", params=params)

    # Single symbol returns object, multiple returns array
    if symbol is not None:
        return _ticker_price_decoder.decode(raw)
    return _ticker_price_list_decoder.decode(raw)
```

**Step 6: Review generated trade.py for signed endpoints**

```python
# binance/api/spot/trade.py (key patterns)
from binance._schemas.spot import Order, CancelOrderResult

_order_decoder = msgspec.json.Decoder(Order)
_cancel_result_decoder = msgspec.json.Decoder(CancelOrderResult)


async def create_order(
    http: HTTPClient,
    symbol: str,
    side: str,
    type: str,
    quantity: str | None = None,
    price: str | None = None,
    time_in_force: str | None = None,
    new_client_order_id: str | None = None,
    # ... more params
) -> Order:
    """Create a new order.

    Weight: 1
    Requires: Signature (signed=True)

    Tip: Always provide `new_client_order_id` for idempotent order placement.
    If a network error occurs, you can safely retry with the same client ID -
    Binance will reject duplicates, preventing accidental double orders.
    """
    params: dict[str, Any] = {
        "symbol": symbol,
        "side": side,
        "type": type,
    }
    if quantity is not None:
        params["quantity"] = quantity
    if price is not None:
        params["price"] = price
    if time_in_force is not None:
        params["timeInForce"] = time_in_force
    # ... more params

    raw = await http.request_raw("POST", "/api/v3/order", signed=True, params=params)
    return _order_decoder.decode(raw)
```

**Step 7: Run mypy**

Run: `mypy binance/api/spot/ --strict`
Expected: Success (or minor issues to fix)

**Step 8: Commit generated code**

```bash
git add binance/api/spot/
git commit -m "feat: generate spot API endpoints with typed returns"
```

---

## Task 4: Manual Review and Fixes

**Purpose:** Generator output may need manual tweaks for edge cases.

**Step 1: Verify all signed endpoints have `signed=True`**

```bash
# Check trade.py - all should have signed=True
grep -n "signed=True" binance/api/spot/trade.py

# Check account.py - all should have signed=True
grep -n "signed=True" binance/api/spot/account.py
```

**Step 2: Verify decoders are defined for all return types**

```bash
# Check that all decoder variables are defined before use
grep -E "^_.*_decoder = " binance/api/spot/*.py
```

**Step 3: Check parameter name mapping (snake_case to camelCase)**

Verify parameters are correctly mapped:
```python
# In function signature: start_time (snake_case)
# In params dict: "startTime" (camelCase for API)
if start_time is not None:
    params["startTime"] = start_time  # ✓ Correct
```

**Step 4: Add Kline schema with from_raw() converter**

Klines come from the API as raw arrays. For AI-friendliness, we convert them to typed objects.

```python
# In binance/_schemas/spot.py
class Kline(BaseStruct):
    """Typed kline with named fields for AI-friendly access.

    The API returns raw arrays, but we convert them to typed objects
    so users can access fields by name (kline.close) instead of index (kline[4]).
    """
    open_time: int
    open: str
    high: str
    low: str
    close: str
    volume: str
    close_time: int
    quote_volume: str
    trades: int
    taker_buy_base: str
    taker_buy_quote: str

    @classmethod
    def from_raw(cls, raw: list[int | str]) -> "Kline":
        """Convert raw kline array to typed Kline."""
        return cls(
            open_time=int(raw[0]),
            open=str(raw[1]),
            high=str(raw[2]),
            low=str(raw[3]),
            close=str(raw[4]),
            volume=str(raw[5]),
            close_time=int(raw[6]),
            quote_volume=str(raw[7]),
            trades=int(raw[8]),
            taker_buy_base=str(raw[9]),
            taker_buy_quote=str(raw[10]),
        )
```

**Step 5: If manual fixes needed, apply and commit**

```bash
git add binance/api/spot/
git commit -m "fix: manual adjustments to generated spot endpoints"
```

---

## Task 4.1: Add Unit Tests for Generated Endpoints

**Files:**
- Create: `tests/unit/api/test_spot_general.py`
- Create: `tests/unit/api/test_spot_market.py`

**Purpose:** Test generated code without network access using mocks.

**Step 1: Write unit tests for general endpoints**

```python
# tests/unit/api/test_spot_general.py
"""Unit tests for general spot endpoints."""
from unittest.mock import AsyncMock, MagicMock
import pytest

from binance.api.spot import general


@pytest.fixture
def mock_http():
    """Create mock HTTPClient."""
    http = MagicMock()
    http.request = AsyncMock()
    http.request_raw = AsyncMock()
    return http


class TestPing:
    """Test ping endpoint."""

    @pytest.mark.asyncio
    async def test_ping_calls_correct_endpoint(self, mock_http):
        """Test ping makes correct request."""
        mock_http.request.return_value = {}

        result = await general.ping(mock_http)

        mock_http.request.assert_called_once_with("GET", "/api/v3/ping")
        assert result == {}


class TestGetServerTime:
    """Test get_server_time endpoint."""

    @pytest.mark.asyncio
    async def test_returns_typed_server_time(self, mock_http):
        """Test returns ServerTime schema."""
        mock_http.request_raw.return_value = b'{"serverTime": 1699999999999}'

        result = await general.get_server_time(mock_http)

        from binance._schemas.spot import ServerTime
        assert isinstance(result, ServerTime)
        assert result.server_time == 1699999999999


class TestGetExchangeInfo:
    """Test get_exchange_info endpoint."""

    @pytest.mark.asyncio
    async def test_with_symbol_param(self, mock_http):
        """Test symbol parameter is passed correctly."""
        mock_http.request_raw.return_value = b'{"timezone": "UTC", "serverTime": 1, "rateLimits": [], "symbols": []}'

        await general.get_exchange_info(mock_http, symbol="BTCUSDT")

        mock_http.request_raw.assert_called_once()
        call_args = mock_http.request_raw.call_args
        assert call_args[1]["params"]["symbol"] == "BTCUSDT"

    @pytest.mark.asyncio
    async def test_without_params(self, mock_http):
        """Test no params when none specified."""
        mock_http.request_raw.return_value = b'{"timezone": "UTC", "serverTime": 1, "rateLimits": [], "symbols": []}'

        await general.get_exchange_info(mock_http)

        call_args = mock_http.request_raw.call_args
        assert call_args[1].get("params", {}) == {}
```

**Step 2: Write unit tests for market endpoints**

```python
# tests/unit/api/test_spot_market.py
"""Unit tests for market spot endpoints."""
from unittest.mock import AsyncMock, MagicMock
import pytest

from binance.api.spot import market


@pytest.fixture
def mock_http():
    """Create mock HTTPClient."""
    http = MagicMock()
    http.request = AsyncMock()
    http.request_raw = AsyncMock()
    return http


class TestGetOrderBook:
    """Test get_order_book endpoint."""

    @pytest.mark.asyncio
    async def test_returns_typed_order_book(self, mock_http):
        """Test returns OrderBook schema."""
        mock_http.request_raw.return_value = b'''{
            "lastUpdateId": 123456789,
            "bids": [["50000.00", "1.0"]],
            "asks": [["50001.00", "2.0"]]
        }'''

        result = await market.get_order_book(mock_http, symbol="BTCUSDT")

        from binance._schemas.spot import OrderBook
        assert isinstance(result, OrderBook)
        assert result.last_update_id == 123456789

    @pytest.mark.asyncio
    async def test_limit_param_omitted_when_default(self, mock_http):
        """Test limit=100 is not sent (default)."""
        mock_http.request_raw.return_value = b'{"lastUpdateId": 1, "bids": [], "asks": []}'

        await market.get_order_book(mock_http, symbol="BTCUSDT", limit=100)

        call_args = mock_http.request_raw.call_args
        assert "limit" not in call_args[1].get("params", {})

    @pytest.mark.asyncio
    async def test_limit_param_sent_when_non_default(self, mock_http):
        """Test limit is sent when not default."""
        mock_http.request_raw.return_value = b'{"lastUpdateId": 1, "bids": [], "asks": []}'

        await market.get_order_book(mock_http, symbol="BTCUSDT", limit=50)

        call_args = mock_http.request_raw.call_args
        assert call_args[1]["params"]["limit"] == 50


class TestGetTrades:
    """Test get_trades endpoint."""

    @pytest.mark.asyncio
    async def test_returns_list_of_trades(self, mock_http):
        """Test returns list[Trade]."""
        mock_http.request_raw.return_value = b'''[
            {"id": 1, "price": "50000", "qty": "0.1", "quoteQty": "5000", "time": 1699999999999, "isBuyerMaker": true, "isBestMatch": true}
        ]'''

        result = await market.get_trades(mock_http, symbol="BTCUSDT")

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].id == 1


class TestGetTickerPrice:
    """Test get_ticker_price endpoint with variant returns."""

    @pytest.mark.asyncio
    async def test_single_symbol_returns_single_object(self, mock_http):
        """Test single symbol returns TickerPrice."""
        mock_http.request_raw.return_value = b'{"symbol": "BTCUSDT", "price": "50000.00"}'

        result = await market.get_ticker_price(mock_http, symbol="BTCUSDT")

        from binance._schemas.spot import TickerPrice
        assert isinstance(result, TickerPrice)
        assert result.symbol == "BTCUSDT"

    @pytest.mark.asyncio
    async def test_no_symbol_returns_list(self, mock_http):
        """Test no symbol returns list[TickerPrice]."""
        mock_http.request_raw.return_value = b'[{"symbol": "BTCUSDT", "price": "50000.00"}]'

        result = await market.get_ticker_price(mock_http)

        assert isinstance(result, list)
```

**Step 3: Run unit tests**

Run: `pytest tests/unit/api/ -v`
Expected: PASS

**Step 4: Commit tests**

```bash
git add tests/unit/api/
git commit -m "test: add unit tests for generated spot endpoints"
```

---

## Next Steps

Continue with [02-generate-schemas.md](./02-generate-schemas.md) to generate typed response schemas.
