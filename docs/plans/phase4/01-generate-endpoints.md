# Phase 4.1: Generate Futures API Endpoints

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create `binance/api/futures_um/` and `binance/api/futures_cm/` modules with typed returns.

**Prerequisites:** Phase 3 complete, futures specs in `specs/openapi/umfutures/` and `specs/openapi/cmfutures/`

**⚠️ Execution Order:**
1. Execute **Task 1** (config URLs) from this file
2. Execute **Tasks 2-5** from `02-generate-schemas.md` (schemas must exist first)
3. Return here for **Tasks 6-8** (endpoint modules)

---

## Task 1: Add Futures Base URLs to Config

**Files:**
- Modify: `binance/_core/config.py`
- Create: `tests/unit/test_futures_config.py`

**Step 1: Write the failing test**

```python
# tests/unit/test_futures_config.py
"""Test futures configuration."""


def test_futures_um_urls_defined():
    """Test USDT-M futures URLs are defined."""
    from binance._core.config import FUTURES_UM_BASE_URL, FUTURES_UM_TESTNET_URL

    assert FUTURES_UM_BASE_URL == "https://fapi.binance.com"
    assert FUTURES_UM_TESTNET_URL == "https://testnet.binancefuture.com"


def test_futures_cm_urls_defined():
    """Test COIN-M futures URLs are defined."""
    from binance._core.config import FUTURES_CM_BASE_URL, FUTURES_CM_TESTNET_URL

    assert FUTURES_CM_BASE_URL == "https://dapi.binance.com"
    assert FUTURES_CM_TESTNET_URL == "https://testnet.binancefuture.com"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/test_futures_config.py -v`
Expected: FAIL with "cannot import name 'FUTURES_UM_BASE_URL'"

**Step 3: Add futures URLs to config**

```python
# Add to binance/_core/config.py

# Futures USDT-Margined (UM) URLs
FUTURES_UM_BASE_URL = "https://fapi.binance.com"
FUTURES_UM_TESTNET_URL = "https://testnet.binancefuture.com"

# Futures COIN-Margined (CM) URLs
FUTURES_CM_BASE_URL = "https://dapi.binance.com"
FUTURES_CM_TESTNET_URL = "https://testnet.binancefuture.com"
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/unit/test_futures_config.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add binance/_core/config.py tests/unit/test_futures_config.py
git commit -m "feat: add futures API base URLs to config"
```

---

## Task 6: Create USDT-M Futures Package Structure

**Files:**
- Create: `binance/api/futures_um/__init__.py`
- Create: `binance/api/futures_um/general.py`
- Create: `binance/api/futures_um/market.py`
- Create: `binance/api/futures_um/trade.py`
- Create: `binance/api/futures_um/account.py`
- Create: `tests/unit/api/test_futures_um_imports.py`

**Step 1: Write the failing test**

```python
# tests/unit/api/test_futures_um_imports.py
"""Test USDT-M futures API package structure."""


def test_futures_um_package_importable():
    """Test that futures_um package exists."""
    import binance.api.futures_um
    assert binance.api.futures_um.__name__ == "binance.api.futures_um"


def test_futures_um_modules_importable():
    """Test that futures_um modules exist."""
    from binance.api.futures_um import general, market, trade, account
    assert general is not None
    assert market is not None
    assert trade is not None
    assert account is not None
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/api/test_futures_um_imports.py -v`
Expected: FAIL with "No module named 'binance.api.futures_um'"

**Step 3: Create package structure**

```python
# binance/api/futures_um/__init__.py
"""USDT-Margined (UM) Futures API endpoints with typed returns.

Modules:
- general: ping, get_server_time, get_exchange_info
- market: get_klines, get_order_book, get_mark_price, get_funding_rate
- trade: create_order, cancel_order, get_order, get_open_orders
- account: get_account, get_balance, get_position_risk, set_leverage

All methods return msgspec schema types for type safety.
Base URL: https://fapi.binance.com (production) / https://testnet.binancefuture.com (testnet)
"""
from binance.api.futures_um import general, market, trade, account

__all__ = ["general", "market", "trade", "account"]
```

```python
# binance/api/futures_um/general.py
"""USDT-M Futures General API endpoints."""
from typing import Any

import msgspec

from binance._core.http import HTTPClient
from binance._schemas.spot import ServerTime  # Reuse ServerTime schema
from binance._schemas.futures import FuturesExchangeInfo

# Pre-compiled decoders
_server_time_decoder = msgspec.json.Decoder(ServerTime)
_exchange_info_decoder = msgspec.json.Decoder(FuturesExchangeInfo)


async def ping(http: HTTPClient) -> dict[str, Any]:
    """Test connectivity to the Futures API.

    Weight: 1

    Returns:
        Empty dict on success
    """
    return await http.request("GET", "/fapi/v1/ping")


async def get_server_time(http: HTTPClient) -> ServerTime:
    """Get current server time.

    Weight: 1

    Returns:
        ServerTime with server_time in milliseconds
    """
    raw = await http.request_raw("GET", "/fapi/v1/time")
    return _server_time_decoder.decode(raw)


async def get_exchange_info(http: HTTPClient) -> FuturesExchangeInfo:
    """Get current exchange trading rules and symbol information.

    Weight: 1

    Returns:
        FuturesExchangeInfo with symbols and rate limits
    """
    raw = await http.request_raw("GET", "/fapi/v1/exchangeInfo")
    return _exchange_info_decoder.decode(raw)
```

```python
# binance/api/futures_um/market.py
"""USDT-M Futures Market Data API endpoints."""
from typing import Any

import msgspec

from binance._core.http import HTTPClient
from binance._schemas.spot import OrderBook, Trade, AggTrade, TickerPrice, BookTicker
from binance._schemas.futures import (
    FuturesKline,
    MarkPrice,
    FundingRate,
    FuturesTicker24h,
)

# Pre-compiled decoders
_order_book_decoder = msgspec.json.Decoder(OrderBook)
_trade_list_decoder = msgspec.json.Decoder(list[Trade])
_agg_trade_list_decoder = msgspec.json.Decoder(list[AggTrade])
_mark_price_decoder = msgspec.json.Decoder(MarkPrice)
_mark_price_list_decoder = msgspec.json.Decoder(list[MarkPrice])
_funding_rate_decoder = msgspec.json.Decoder(list[FundingRate])
_ticker_24h_decoder = msgspec.json.Decoder(FuturesTicker24h)
_ticker_24h_list_decoder = msgspec.json.Decoder(list[FuturesTicker24h])
_ticker_price_decoder = msgspec.json.Decoder(TickerPrice)
_ticker_price_list_decoder = msgspec.json.Decoder(list[TickerPrice])
_book_ticker_decoder = msgspec.json.Decoder(BookTicker)
_book_ticker_list_decoder = msgspec.json.Decoder(list[BookTicker])


async def get_order_book(
    http: HTTPClient,
    symbol: str,
    limit: int = 500,
) -> OrderBook:
    """Get order book depth.

    Weight: 5-20 depending on limit

    Args:
        symbol: Trading pair (e.g., "BTCUSDT")
        limit: Depth limit (5, 10, 20, 50, 100, 500, 1000)

    Returns:
        OrderBook with bids and asks
    """
    params: dict[str, Any] = {"symbol": symbol}
    if limit != 500:
        params["limit"] = limit
    raw = await http.request_raw("GET", "/fapi/v1/depth", params=params)
    return _order_book_decoder.decode(raw)


async def get_trades(
    http: HTTPClient,
    symbol: str,
    limit: int = 500,
) -> list[Trade]:
    """Get recent trades.

    Weight: 5

    Args:
        symbol: Trading pair
        limit: Number of trades (max 1000)

    Returns:
        List of Trade objects
    """
    params: dict[str, Any] = {"symbol": symbol}
    if limit != 500:
        params["limit"] = limit
    raw = await http.request_raw("GET", "/fapi/v1/trades", params=params)
    return _trade_list_decoder.decode(raw)


async def get_agg_trades(
    http: HTTPClient,
    symbol: str,
    from_id: int | None = None,
    start_time: int | None = None,
    end_time: int | None = None,
    limit: int = 500,
) -> list[AggTrade]:
    """Get aggregated trades.

    Weight: 20

    Returns:
        List of AggTrade objects
    """
    params: dict[str, Any] = {"symbol": symbol}
    if from_id is not None:
        params["fromId"] = from_id
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if limit != 500:
        params["limit"] = limit
    raw = await http.request_raw("GET", "/fapi/v1/aggTrades", params=params)
    return _agg_trade_list_decoder.decode(raw)


async def get_klines(
    http: HTTPClient,
    symbol: str,
    interval: str,
    start_time: int | None = None,
    end_time: int | None = None,
    limit: int = 500,
) -> list[FuturesKline]:
    """Get kline/candlestick bars.

    Weight: 5

    Args:
        symbol: Trading pair (e.g., "BTCUSDT")
        interval: Kline interval (1m, 5m, 15m, 1h, 4h, 1d, etc.)
        start_time: Start time in milliseconds
        end_time: End time in milliseconds
        limit: Number of klines (max 1500)

    Returns:
        List of FuturesKline objects with typed fields
    """
    params: dict[str, Any] = {"symbol": symbol, "interval": interval}
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if limit != 500:
        params["limit"] = limit
    raw = await http.request("GET", "/fapi/v1/klines", params=params)
    return [FuturesKline.from_raw(k) for k in raw]


async def get_continuous_klines(
    http: HTTPClient,
    pair: str,
    contract_type: str,
    interval: str,
    start_time: int | None = None,
    end_time: int | None = None,
    limit: int = 500,
) -> list[FuturesKline]:
    """Get continuous contract klines.

    Weight: 5

    Args:
        pair: Trading pair (e.g., "BTCUSDT")
        contract_type: PERPETUAL, CURRENT_QUARTER, NEXT_QUARTER
        interval: Kline interval

    Returns:
        List of FuturesKline objects
    """
    params: dict[str, Any] = {
        "pair": pair,
        "contractType": contract_type,
        "interval": interval,
    }
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if limit != 500:
        params["limit"] = limit
    raw = await http.request("GET", "/fapi/v1/continuousKlines", params=params)
    return [FuturesKline.from_raw(k) for k in raw]


async def get_mark_price(
    http: HTTPClient,
    symbol: str | None = None,
) -> MarkPrice | list[MarkPrice]:
    """Get mark price and funding rate.

    Weight: 1

    Args:
        symbol: Trading pair (returns single) or None (returns all)

    Returns:
        MarkPrice if symbol specified, else list[MarkPrice]
    """
    params: dict[str, Any] = {}
    if symbol is not None:
        params["symbol"] = symbol
    raw = await http.request_raw("GET", "/fapi/v1/premiumIndex", params=params)
    if symbol is not None:
        return _mark_price_decoder.decode(raw)
    return _mark_price_list_decoder.decode(raw)


async def get_funding_rate(
    http: HTTPClient,
    symbol: str,
    start_time: int | None = None,
    end_time: int | None = None,
    limit: int = 100,
) -> list[FundingRate]:
    """Get funding rate history.

    Weight: 1

    Args:
        symbol: Trading pair
        start_time: Start time in ms
        end_time: End time in ms
        limit: Number of results (max 1000)

    Returns:
        List of FundingRate objects
    """
    params: dict[str, Any] = {"symbol": symbol}
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if limit != 100:
        params["limit"] = limit
    raw = await http.request_raw("GET", "/fapi/v1/fundingRate", params=params)
    return _funding_rate_decoder.decode(raw)


async def get_ticker_24h(
    http: HTTPClient,
    symbol: str | None = None,
) -> FuturesTicker24h | list[FuturesTicker24h]:
    """Get 24hr ticker price change statistics.

    Weight: 1-40 depending on parameters

    Returns:
        FuturesTicker24h if symbol specified, else list[FuturesTicker24h]
    """
    params: dict[str, Any] = {}
    if symbol is not None:
        params["symbol"] = symbol
    raw = await http.request_raw("GET", "/fapi/v1/ticker/24hr", params=params)
    if symbol is not None:
        return _ticker_24h_decoder.decode(raw)
    return _ticker_24h_list_decoder.decode(raw)


async def get_ticker_price(
    http: HTTPClient,
    symbol: str | None = None,
) -> TickerPrice | list[TickerPrice]:
    """Get symbol price ticker.

    Weight: 1-2

    Returns:
        TickerPrice if symbol specified, else list[TickerPrice]
    """
    params: dict[str, Any] = {}
    if symbol is not None:
        params["symbol"] = symbol
    raw = await http.request_raw("GET", "/fapi/v1/ticker/price", params=params)
    if symbol is not None:
        return _ticker_price_decoder.decode(raw)
    return _ticker_price_list_decoder.decode(raw)


async def get_book_ticker(
    http: HTTPClient,
    symbol: str | None = None,
) -> BookTicker | list[BookTicker]:
    """Get best bid/ask price.

    Weight: 1-2

    Returns:
        BookTicker if symbol specified, else list[BookTicker]
    """
    params: dict[str, Any] = {}
    if symbol is not None:
        params["symbol"] = symbol
    raw = await http.request_raw("GET", "/fapi/v1/ticker/bookTicker", params=params)
    if symbol is not None:
        return _book_ticker_decoder.decode(raw)
    return _book_ticker_list_decoder.decode(raw)
```

```python
# binance/api/futures_um/trade.py
"""USDT-M Futures Trade API endpoints."""
from typing import Any

import msgspec

from binance._core.http import HTTPClient
from binance._schemas.futures import FuturesOrder, BatchOrderError

# Pre-compiled decoders
_order_decoder = msgspec.json.Decoder(FuturesOrder)
_order_list_decoder = msgspec.json.Decoder(list[FuturesOrder])
_batch_order_decoder = msgspec.json.Decoder(list[FuturesOrder | BatchOrderError])


async def create_order(
    http: HTTPClient,
    symbol: str,
    side: str,
    type: str,
    quantity: str | None = None,
    price: str | None = None,
    time_in_force: str | None = None,
    reduce_only: bool | None = None,
    new_client_order_id: str | None = None,
    stop_price: str | None = None,
    position_side: str | None = None,
    close_position: bool | None = None,
    activation_price: str | None = None,
    callback_rate: str | None = None,
    working_type: str | None = None,
    price_protect: bool | None = None,
    new_order_resp_type: str | None = None,
) -> FuturesOrder:
    """Create a new futures order.

    Weight: 1
    Requires: Signature

    Args:
        symbol: Trading pair (e.g., "BTCUSDT")
        side: BUY or SELL
        type: LIMIT, MARKET, STOP, STOP_MARKET, TAKE_PROFIT, TAKE_PROFIT_MARKET,
              TRAILING_STOP_MARKET
        quantity: Order quantity
        price: Limit price (required for LIMIT orders)
        time_in_force: GTC, IOC, FOK, GTX
        reduce_only: Reduce position only (cannot be sent with closePosition)
        new_client_order_id: Custom order ID for idempotency
        stop_price: Stop price for STOP/TAKE_PROFIT orders
        position_side: LONG, SHORT, or BOTH (for hedge mode)
        close_position: Close all position (for STOP orders)
        activation_price: Activation price for TRAILING_STOP_MARKET
        callback_rate: Callback rate for TRAILING_STOP_MARKET
        working_type: MARK_PRICE or CONTRACT_PRICE
        price_protect: Price protection
        new_order_resp_type: ACK or RESULT

    Returns:
        FuturesOrder with order details

    Tip:
        Always provide `new_client_order_id` for idempotent order placement.
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
    if reduce_only is not None:
        params["reduceOnly"] = str(reduce_only).lower()
    if new_client_order_id is not None:
        params["newClientOrderId"] = new_client_order_id
    if stop_price is not None:
        params["stopPrice"] = stop_price
    if position_side is not None:
        params["positionSide"] = position_side
    if close_position is not None:
        params["closePosition"] = str(close_position).lower()
    if activation_price is not None:
        params["activationPrice"] = activation_price
    if callback_rate is not None:
        params["callbackRate"] = callback_rate
    if working_type is not None:
        params["workingType"] = working_type
    if price_protect is not None:
        params["priceProtect"] = str(price_protect).lower()
    if new_order_resp_type is not None:
        params["newOrderRespType"] = new_order_resp_type

    raw = await http.request_raw("POST", "/fapi/v1/order", signed=True, params=params)
    return _order_decoder.decode(raw)


async def create_test_order(
    http: HTTPClient,
    symbol: str,
    side: str,
    type: str,
    quantity: str | None = None,
    price: str | None = None,
    time_in_force: str | None = None,
) -> dict[str, Any]:
    """Test new order creation (no actual order placed).

    Weight: 1
    Requires: Signature

    Returns:
        Empty dict on success
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

    return await http.request("POST", "/fapi/v1/order/test", signed=True, params=params)


async def get_order(
    http: HTTPClient,
    symbol: str,
    order_id: int | None = None,
    orig_client_order_id: str | None = None,
) -> FuturesOrder:
    """Query order status.

    Weight: 1
    Requires: Signature

    Args:
        symbol: Trading pair
        order_id: Order ID (use this or orig_client_order_id)
        orig_client_order_id: Client order ID

    Returns:
        FuturesOrder with current status
    """
    params: dict[str, Any] = {"symbol": symbol}
    if order_id is not None:
        params["orderId"] = order_id
    if orig_client_order_id is not None:
        params["origClientOrderId"] = orig_client_order_id

    raw = await http.request_raw("GET", "/fapi/v1/order", signed=True, params=params)
    return _order_decoder.decode(raw)


async def cancel_order(
    http: HTTPClient,
    symbol: str,
    order_id: int | None = None,
    orig_client_order_id: str | None = None,
) -> FuturesOrder:
    """Cancel an active order.

    Weight: 1
    Requires: Signature

    Returns:
        FuturesOrder with canceled status
    """
    params: dict[str, Any] = {"symbol": symbol}
    if order_id is not None:
        params["orderId"] = order_id
    if orig_client_order_id is not None:
        params["origClientOrderId"] = orig_client_order_id

    raw = await http.request_raw("DELETE", "/fapi/v1/order", signed=True, params=params)
    return _order_decoder.decode(raw)


async def cancel_all_open_orders(
    http: HTTPClient,
    symbol: str,
) -> dict[str, Any]:
    """Cancel all open orders on a symbol.

    Weight: 1
    Requires: Signature

    Returns:
        Success response
    """
    params: dict[str, Any] = {"symbol": symbol}
    return await http.request("DELETE", "/fapi/v1/allOpenOrders", signed=True, params=params)


async def get_open_orders(
    http: HTTPClient,
    symbol: str | None = None,
) -> list[FuturesOrder]:
    """Get all open orders.

    Weight: 1-40 depending on symbol
    Requires: Signature

    Returns:
        List of open FuturesOrder objects
    """
    params: dict[str, Any] = {}
    if symbol is not None:
        params["symbol"] = symbol

    raw = await http.request_raw("GET", "/fapi/v1/openOrders", signed=True, params=params)
    return _order_list_decoder.decode(raw)


async def get_all_orders(
    http: HTTPClient,
    symbol: str,
    order_id: int | None = None,
    start_time: int | None = None,
    end_time: int | None = None,
    limit: int = 500,
) -> list[FuturesOrder]:
    """Get all account orders (active, canceled, filled).

    Weight: 5
    Requires: Signature

    Returns:
        List of FuturesOrder objects
    """
    params: dict[str, Any] = {"symbol": symbol}
    if order_id is not None:
        params["orderId"] = order_id
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if limit != 500:
        params["limit"] = limit

    raw = await http.request_raw("GET", "/fapi/v1/allOrders", signed=True, params=params)
    return _order_list_decoder.decode(raw)


async def create_batch_orders(
    http: HTTPClient,
    orders: list[dict[str, Any]],
) -> list[FuturesOrder | BatchOrderError]:
    """Place multiple orders in a single request.

    Weight: 5
    Requires: Signature

    Note: Each order in the response can be either a FuturesOrder (success)
    or a BatchOrderError (failure). Check for 'code' field to detect errors.

    Args:
        orders: List of order dicts (max 5). Each dict should contain:
            - symbol: Trading pair (required)
            - side: BUY or SELL (required)
            - type: Order type (required)
            - quantity: Order quantity (required for most types)
            - price: Limit price (required for LIMIT orders)
            - positionSide: LONG, SHORT, or BOTH (optional)
            - timeInForce: GTC, IOC, FOK (optional)
            - reduceOnly: true/false (optional)
            - stopPrice: Stop price (for STOP orders)

    Returns:
        List of FuturesOrder or BatchOrderError for each order

    Example:
        orders = [
            {"symbol": "BTCUSDT", "side": "BUY", "type": "LIMIT",
             "quantity": "0.001", "price": "30000", "timeInForce": "GTC"},
            {"symbol": "BTCUSDT", "side": "SELL", "type": "LIMIT",
             "quantity": "0.001", "price": "35000", "timeInForce": "GTC"},
        ]
        results = await create_batch_orders(http, orders)
        for result in results:
            if isinstance(result, BatchOrderError):
                print(f"Order failed: {result.code} - {result.msg}")
            else:
                print(f"Order placed: {result.order_id}")
    """
    import orjson

    # Binance requires batchOrders as a JSON string, not a list
    params: dict[str, Any] = {
        "batchOrders": orjson.dumps(orders).decode(),
    }
    raw = await http.request_raw("POST", "/fapi/v1/batchOrders", signed=True, params=params)
    return _batch_order_decoder.decode(raw)
```

```python
# binance/api/futures_um/account.py
"""USDT-M Futures Account API endpoints."""
from typing import Any

import msgspec

from binance._core.http import HTTPClient
from binance._schemas.futures import (
    FuturesAccount,
    FuturesBalance,
    PositionRisk,
    LeverageResult,
    FuturesMyTrade,
)

# Pre-compiled decoders
_account_decoder = msgspec.json.Decoder(FuturesAccount)
_balance_list_decoder = msgspec.json.Decoder(list[FuturesBalance])
_position_list_decoder = msgspec.json.Decoder(list[PositionRisk])
_leverage_decoder = msgspec.json.Decoder(LeverageResult)
_trade_list_decoder = msgspec.json.Decoder(list[FuturesMyTrade])


async def get_account(http: HTTPClient) -> FuturesAccount:
    """Get current account information.

    Weight: 5
    Requires: Signature

    Returns:
        FuturesAccount with balances and positions
    """
    raw = await http.request_raw("GET", "/fapi/v2/account", signed=True)
    return _account_decoder.decode(raw)


async def get_balance(http: HTTPClient) -> list[FuturesBalance]:
    """Get futures account balance.

    Weight: 5
    Requires: Signature

    Returns:
        List of FuturesBalance objects
    """
    raw = await http.request_raw("GET", "/fapi/v2/balance", signed=True)
    return _balance_list_decoder.decode(raw)


async def get_position_risk(
    http: HTTPClient,
    symbol: str | None = None,
) -> list[PositionRisk]:
    """Get current position information.

    Weight: 5
    Requires: Signature

    Args:
        symbol: Trading pair (optional, returns all if not specified)

    Returns:
        List of PositionRisk objects
    """
    params: dict[str, Any] = {}
    if symbol is not None:
        params["symbol"] = symbol

    raw = await http.request_raw("GET", "/fapi/v2/positionRisk", signed=True, params=params)
    return _position_list_decoder.decode(raw)


async def set_leverage(
    http: HTTPClient,
    symbol: str,
    leverage: int,
) -> LeverageResult:
    """Change user's initial leverage.

    Weight: 1
    Requires: Signature

    Args:
        symbol: Trading pair
        leverage: Target leverage (1-125)

    Returns:
        LeverageResult with new leverage and max notional
    """
    params: dict[str, Any] = {
        "symbol": symbol,
        "leverage": leverage,
    }
    raw = await http.request_raw("POST", "/fapi/v1/leverage", signed=True, params=params)
    return _leverage_decoder.decode(raw)


async def set_margin_type(
    http: HTTPClient,
    symbol: str,
    margin_type: str,
) -> dict[str, Any]:
    """Change margin type (ISOLATED/CROSSED).

    Weight: 1
    Requires: Signature

    Args:
        symbol: Trading pair
        margin_type: ISOLATED or CROSSED

    Returns:
        Success response
    """
    params: dict[str, Any] = {
        "symbol": symbol,
        "marginType": margin_type,
    }
    return await http.request("POST", "/fapi/v1/marginType", signed=True, params=params)


async def get_my_trades(
    http: HTTPClient,
    symbol: str,
    order_id: int | None = None,
    start_time: int | None = None,
    end_time: int | None = None,
    from_id: int | None = None,
    limit: int = 500,
) -> list[FuturesMyTrade]:
    """Get trades for a specific account and symbol.

    Weight: 5
    Requires: Signature

    Returns:
        List of FuturesMyTrade objects
    """
    params: dict[str, Any] = {"symbol": symbol}
    if order_id is not None:
        params["orderId"] = order_id
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if from_id is not None:
        params["fromId"] = from_id
    if limit != 500:
        params["limit"] = limit

    raw = await http.request_raw("GET", "/fapi/v1/userTrades", signed=True, params=params)
    return _trade_list_decoder.decode(raw)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/unit/api/test_futures_um_imports.py -v`
Expected: PASS (after creating schemas in Task 5)

**Step 5: Commit**

```bash
git add binance/api/futures_um/ tests/unit/api/test_futures_um_imports.py
git commit -m "feat: create USDT-M futures endpoint modules with typed returns"
```

---

## Task 7: Create COIN-M Futures Package Structure

**Files:**
- Create: `binance/api/futures_cm/__init__.py`
- Create: `binance/api/futures_cm/general.py`
- Create: `binance/api/futures_cm/market.py`
- Create: `binance/api/futures_cm/trade.py`
- Create: `binance/api/futures_cm/account.py`
- Create: `tests/unit/api/test_futures_cm_imports.py`

**Step 1: Write the failing test**

```python
# tests/unit/api/test_futures_cm_imports.py
"""Test COIN-M futures API package structure."""


def test_futures_cm_package_importable():
    """Test that futures_cm package exists."""
    import binance.api.futures_cm
    assert binance.api.futures_cm.__name__ == "binance.api.futures_cm"


def test_futures_cm_modules_importable():
    """Test that futures_cm modules exist."""
    from binance.api.futures_cm import general, market, trade, account
    assert general is not None
    assert market is not None
    assert trade is not None
    assert account is not None
```

**Step 2: Create COIN-M package (similar to USDT-M but with /dapi/ paths)**

```python
# binance/api/futures_cm/__init__.py
"""COIN-Margined (CM) Futures API endpoints with typed returns.

Modules:
- general: ping, get_server_time, get_exchange_info
- market: get_klines, get_order_book, get_mark_price, get_funding_rate
- trade: create_order, cancel_order, get_order, get_open_orders
- account: get_account, get_balance, get_position_risk, set_leverage

All methods return msgspec schema types for type safety.
Base URL: https://dapi.binance.com (production) / https://testnet.binancefuture.com (testnet)
"""
from binance.api.futures_cm import general, market, trade, account

__all__ = ["general", "market", "trade", "account"]
```

**Step 3: Copy and modify USDT-M modules for COIN-M**

Key differences:
- Change `/fapi/v1/` to `/dapi/v1/`
- Change `/fapi/v2/` to `/dapi/v1/` (COIN-M uses v1 for account endpoints)

```python
# binance/api/futures_cm/general.py
# Same as futures_um/general.py but with /dapi/v1/ paths
async def ping(http: HTTPClient) -> dict[str, Any]:
    return await http.request("GET", "/dapi/v1/ping")

async def get_server_time(http: HTTPClient) -> ServerTime:
    raw = await http.request_raw("GET", "/dapi/v1/time")
    return _server_time_decoder.decode(raw)
# ... etc
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/unit/api/test_futures_cm_imports.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add binance/api/futures_cm/ tests/unit/api/test_futures_cm_imports.py
git commit -m "feat: create COIN-M futures endpoint modules with typed returns"
```

---

## Task 8: Add Unit Tests for Futures Endpoints

**Files:**
- Create: `tests/unit/api/test_futures_um_general.py`
- Create: `tests/unit/api/test_futures_um_market.py`

**Step 1: Write unit tests with mocks**

```python
# tests/unit/api/test_futures_um_general.py
"""Unit tests for USDT-M futures general endpoints."""
from unittest.mock import AsyncMock, MagicMock
import pytest

from binance.api.futures_um import general


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

        mock_http.request.assert_called_once_with("GET", "/fapi/v1/ping")
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
    async def test_calls_correct_endpoint(self, mock_http):
        """Test calls /fapi/v1/exchangeInfo."""
        mock_http.request_raw.return_value = b'{"timezone": "UTC", "serverTime": 1, "rateLimits": [], "symbols": [], "exchangeFilters": []}'

        await general.get_exchange_info(mock_http)

        mock_http.request_raw.assert_called_once_with("GET", "/fapi/v1/exchangeInfo")
```

```python
# tests/unit/api/test_futures_um_market.py
"""Unit tests for USDT-M futures market endpoints."""
from unittest.mock import AsyncMock, MagicMock
import pytest

from binance.api.futures_um import market


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
        mock_http.request_raw.return_value = b'{"lastUpdateId": 123, "bids": [["50000", "1"]], "asks": [["50001", "2"]]}'

        result = await market.get_order_book(mock_http, symbol="BTCUSDT")

        from binance._schemas.spot import OrderBook
        assert isinstance(result, OrderBook)
        assert result.last_update_id == 123


class TestGetKlines:
    """Test get_klines endpoint."""

    @pytest.mark.asyncio
    async def test_returns_typed_klines(self, mock_http):
        """Test returns list of FuturesKline."""
        mock_http.request.return_value = [
            [1699999999999, "50000", "51000", "49000", "50500", "100", 1700000003999, "5000", 100, "60", "3000", "0"]
        ]

        result = await market.get_klines(mock_http, symbol="BTCUSDT", interval="1h")

        from binance._schemas.futures import FuturesKline
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], FuturesKline)


class TestGetMarkPrice:
    """Test get_mark_price endpoint."""

    @pytest.mark.asyncio
    async def test_single_symbol_returns_single(self, mock_http):
        """Test single symbol returns MarkPrice."""
        mock_http.request_raw.return_value = b'{"symbol": "BTCUSDT", "markPrice": "50000", "indexPrice": "49995", "lastFundingRate": "0.0001", "nextFundingTime": 1700000000000, "time": 1699999999999}'

        result = await market.get_mark_price(mock_http, symbol="BTCUSDT")

        from binance._schemas.futures import MarkPrice
        assert isinstance(result, MarkPrice)
        assert result.symbol == "BTCUSDT"

    @pytest.mark.asyncio
    async def test_no_symbol_returns_list(self, mock_http):
        """Test no symbol returns list."""
        mock_http.request_raw.return_value = b'[{"symbol": "BTCUSDT", "markPrice": "50000", "indexPrice": "49995", "lastFundingRate": "0.0001", "nextFundingTime": 1700000000000, "time": 1699999999999}]'

        result = await market.get_mark_price(mock_http)

        assert isinstance(result, list)
```

**Step 2: Run tests**

Run: `pytest tests/unit/api/test_futures_um_*.py -v`
Expected: PASS

**Step 3: Commit**

```bash
git add tests/unit/api/test_futures_um_*.py
git commit -m "test: add unit tests for USDT-M futures endpoints"
```

---

## Next Steps

Continue with [02-generate-schemas.md](./02-generate-schemas.md) to create futures-specific schemas.
