# Phase 3.3: Create AsyncClient Entry Point

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create `binance/client.py` with `AsyncClient` that returns **typed schemas**.

**Prerequisites:** Tasks 1-7 complete (api/spot/ and _schemas/spot.py exist)

---

## Task 8: Create AsyncClient Skeleton

**Files:**
- Create: `binance/client.py`
- Create: `tests/unit/test_client.py`

**Step 1: Write the failing test**

```python
# tests/unit/test_client.py
"""Test AsyncClient entry point."""
import pytest


def test_async_client_importable():
    """Test that AsyncClient can be imported."""
    from binance.client import AsyncClient
    assert AsyncClient is not None


def test_async_client_init():
    """Test AsyncClient initialization."""
    from binance.client import AsyncClient

    client = AsyncClient(
        api_key="test_key",
        api_secret="test_secret",
        testnet=True,
    )

    assert client is not None


def test_async_client_has_http_attribute():
    """Test that client has _http attribute."""
    from binance.client import AsyncClient

    client = AsyncClient()
    assert hasattr(client, "_http")
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/test_client.py -v`
Expected: FAIL with "No module named 'binance.client'"

**Step 3: Create AsyncClient skeleton**

```python
# binance/client.py
"""AsyncClient - Main entry point for Binance API.

This thin wrapper provides typed method signatures for all endpoints.
All methods return msgspec schema types (not raw dicts).

Usage:
    async with AsyncClient(api_key="...", api_secret="...") as client:
        # Market data (public) - returns typed schemas
        klines = await client.get_klines(symbol="BTCUSDT", interval="1h")

        # Account data (signed) - returns Account schema
        account = await client.get_account()
        print(account.balances[0].asset)  # IDE autocomplete works!

        # Trading (signed) - returns Order schema
        order = await client.create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="MARKET",
            quantity="0.001",
        )
        print(order.order_id)  # Typed access
"""
from typing import Any, overload

from binance._core.http import HTTPClient
from binance._schemas.spot import (
    ServerTime,
    ExchangeInfo,
    OrderBook,
    Trade,
    AggTrade,
    Kline,
    AvgPrice,
    Ticker24h,
    TickerPrice,
    BookTicker,
    Order,
    CancelOrderResult,
    Account,
    MyTrade,
    RateLimitInfo,
)


class AsyncClient:
    """Async client for Binance Spot API.

    All methods are async and must be awaited.
    Use as async context manager for automatic connection handling.

    All endpoint methods return typed msgspec schemas for type safety.
    """

    __slots__ = ("_http",)

    def __init__(
        self,
        api_key: str = "",
        api_secret: str = "",
        testnet: bool = False,
        base_url: str | None = None,
        timeout: float = 10.0,
    ) -> None:
        """Initialize AsyncClient.

        Args:
            api_key: Binance API key (required for authenticated endpoints)
            api_secret: Binance API secret (required for signed endpoints)
            testnet: Use testnet URLs if True
            base_url: Override base URL (ignores testnet if set)
            timeout: Request timeout in seconds
        """
        self._http = HTTPClient(
            api_key=api_key,
            api_secret=api_secret,
            testnet=testnet,
            base_url=base_url,
            timeout=timeout,
        )

    async def __aenter__(self) -> "AsyncClient":
        """Async context manager entry."""
        await self._http.connect()
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit."""
        await self._http.close()

    async def connect(self) -> None:
        """Initialize connection pool.

        Called automatically when using `async with AsyncClient()`.
        Call manually if not using context manager.
        """
        await self._http.connect()

    async def close(self) -> None:
        """Close connection pool.

        Called automatically when using `async with AsyncClient()`.
        Call manually if not using context manager.
        """
        await self._http.close()
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/unit/test_client.py -v`
Expected: PASS

**Step 5: Run mypy**

Run: `mypy binance/client.py --strict`
Expected: Success

**Step 6: Commit skeleton**

```bash
git add binance/client.py tests/unit/test_client.py
git commit -m "feat: create AsyncClient skeleton"
```

---

## Task 9: Bind General Endpoints (Typed Returns)

**Files:**
- Modify: `binance/client.py`
- Modify: `tests/unit/test_client.py`

**Step 1: Write the failing test**

```python
# Add to tests/unit/test_client.py
from unittest.mock import AsyncMock, MagicMock, patch


def test_async_client_has_ping():
    """Test that client has ping method."""
    from binance.client import AsyncClient
    client = AsyncClient()
    assert hasattr(client, "ping")
    assert callable(client.ping)


def test_async_client_has_get_server_time():
    """Test that client has get_server_time method."""
    from binance.client import AsyncClient
    client = AsyncClient()
    assert hasattr(client, "get_server_time")


def test_async_client_has_get_exchange_info():
    """Test that client has get_exchange_info method."""
    from binance.client import AsyncClient
    client = AsyncClient()
    assert hasattr(client, "get_exchange_info")


@pytest.mark.asyncio
async def test_get_server_time_returns_typed():
    """Test get_server_time returns ServerTime schema."""
    from binance.client import AsyncClient
    from binance._schemas.spot import ServerTime

    with patch.object(AsyncClient, '_http') as mock_http:
        mock_http.request_raw = AsyncMock(return_value=b'{"serverTime": 123}')

        client = AsyncClient()
        client._http = mock_http

        # Import the actual function
        from binance.api.spot import general
        with patch.object(general, 'get_server_time', new_callable=AsyncMock) as mock_func:
            mock_func.return_value = ServerTime(server_time=123)

            result = await client.get_server_time()

            assert isinstance(result, ServerTime)
            assert result.server_time == 123
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/test_client.py::test_async_client_has_ping -v`
Expected: FAIL

**Step 3: Add general endpoint methods**

```python
# Add to binance/client.py

from binance.api.spot import general, market, trade, account


class AsyncClient:
    # ... existing code ...

    # ============ General Endpoints ============

    async def ping(self) -> dict[str, Any]:
        """Test connectivity to the Rest API.

        Weight: 1

        Returns:
            Empty dict on success
        """
        return await general.ping(self._http)

    async def get_server_time(self) -> ServerTime:
        """Test connectivity and get current server time.

        Weight: 1

        Returns:
            ServerTime with server_time in milliseconds
        """
        return await general.get_server_time(self._http)

    async def get_exchange_info(
        self,
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
        return await general.get_exchange_info(
            self._http,
            symbol=symbol,
            symbols=symbols,
            permissions=permissions,
        )
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/unit/test_client.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add binance/client.py tests/unit/test_client.py
git commit -m "feat: bind general endpoints to AsyncClient with typed returns"
```

---

## Task 10: Bind Market Endpoints with Overloads

**Files:**
- Modify: `binance/client.py`
- Modify: `tests/unit/test_client.py`

**Step 1: Write tests for market endpoints**

```python
# Add to tests/unit/test_client.py

def test_async_client_has_market_methods():
    """Test that client has market data methods."""
    from binance.client import AsyncClient

    client = AsyncClient()
    assert hasattr(client, "get_klines")
    assert hasattr(client, "get_order_book")
    assert hasattr(client, "get_trades")
    assert hasattr(client, "get_ticker_price")
    assert hasattr(client, "get_ticker_24h")
    assert hasattr(client, "get_book_ticker")
    assert hasattr(client, "get_avg_price")
    assert hasattr(client, "get_agg_trades")
```

**Step 2: Add market endpoint methods with @overload for variant returns**

```python
# Add to binance/client.py

class AsyncClient:
    # ... existing code ...

    # ============ Market Data Endpoints ============

    async def get_order_book(
        self,
        symbol: str,
        limit: int = 100,
    ) -> OrderBook:
        """Get order book depth.

        Weight: 5-50 depending on limit

        Args:
            symbol: Trading pair
            limit: Depth limit (5, 10, 20, 50, 100, 500, 1000, 5000)

        Returns:
            OrderBook with bids and asks
        """
        return await market.get_order_book(self._http, symbol=symbol, limit=limit)

    async def get_trades(
        self,
        symbol: str,
        limit: int = 500,
    ) -> list[Trade]:
        """Get recent trades.

        Weight: 10

        Args:
            symbol: Trading pair
            limit: Number of trades (max 1000)

        Returns:
            List of Trade objects
        """
        return await market.get_trades(self._http, symbol=symbol, limit=limit)

    async def get_agg_trades(
        self,
        symbol: str,
        from_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 500,
    ) -> list[AggTrade]:
        """Get aggregated trades.

        Weight: 2

        Returns:
            List of AggTrade objects
        """
        return await market.get_agg_trades(
            self._http,
            symbol=symbol,
            from_id=from_id,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    async def get_klines(
        self,
        symbol: str,
        interval: str,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 500,
    ) -> list[Kline]:
        """Get kline/candlestick bars.

        Weight: 2

        Args:
            symbol: Trading pair (e.g., "BTCUSDT")
            interval: Kline interval (1m, 5m, 15m, 1h, 4h, 1d, etc.)
            start_time: Start time in ms
            end_time: End time in ms
            limit: Number of klines (max 1000)

        Returns:
            List of Kline objects with typed fields (open, high, low, close, volume, etc.)
        """
        return await market.get_klines(
            self._http,
            symbol=symbol,
            interval=interval,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    async def get_avg_price(self, symbol: str) -> AvgPrice:
        """Get current average price.

        Weight: 2

        Returns:
            AvgPrice with mins and price
        """
        return await market.get_avg_price(self._http, symbol=symbol)

    # Ticker endpoints with overloads for type safety
    @overload
    async def get_ticker_24h(self, symbol: str) -> Ticker24h: ...
    @overload
    async def get_ticker_24h(self, symbol: None = None, symbols: list[str] | None = None) -> list[Ticker24h]: ...

    async def get_ticker_24h(
        self,
        symbol: str | None = None,
        symbols: list[str] | None = None,
    ) -> Ticker24h | list[Ticker24h]:
        """Get 24hr ticker price change statistics.

        Weight: 1-80 depending on parameters

        Args:
            symbol: Single trading pair (returns Ticker24h)
            symbols: Multiple trading pairs (returns list[Ticker24h])

        Returns:
            Ticker24h if symbol specified, else list[Ticker24h]
        """
        return await market.get_ticker_24h(self._http, symbol=symbol, symbols=symbols)

    @overload
    async def get_ticker_price(self, symbol: str) -> TickerPrice: ...
    @overload
    async def get_ticker_price(self, symbol: None = None, symbols: list[str] | None = None) -> list[TickerPrice]: ...

    async def get_ticker_price(
        self,
        symbol: str | None = None,
        symbols: list[str] | None = None,
    ) -> TickerPrice | list[TickerPrice]:
        """Get symbol price ticker.

        Weight: 1-4

        Returns:
            TickerPrice if symbol specified, else list[TickerPrice]
        """
        return await market.get_ticker_price(self._http, symbol=symbol, symbols=symbols)

    @overload
    async def get_book_ticker(self, symbol: str) -> BookTicker: ...
    @overload
    async def get_book_ticker(self, symbol: None = None, symbols: list[str] | None = None) -> list[BookTicker]: ...

    async def get_book_ticker(
        self,
        symbol: str | None = None,
        symbols: list[str] | None = None,
    ) -> BookTicker | list[BookTicker]:
        """Get best bid/ask price.

        Weight: 1-4

        Returns:
            BookTicker if symbol specified, else list[BookTicker]
        """
        return await market.get_book_ticker(self._http, symbol=symbol, symbols=symbols)
```

**Step 3: Run tests**

Run: `pytest tests/unit/test_client.py -v`
Expected: PASS

**Step 4: Commit**

```bash
git add binance/client.py tests/unit/test_client.py
git commit -m "feat: bind market endpoints with typed returns and overloads"
```

---

## Task 11: Bind Trade and Account Endpoints

**Files:**
- Modify: `binance/client.py`
- Modify: `tests/unit/test_client.py`

**Step 1: Write tests for trade/account endpoints**

```python
# Add to tests/unit/test_client.py

def test_async_client_has_trade_methods():
    """Test that client has trading methods."""
    from binance.client import AsyncClient

    client = AsyncClient()
    assert hasattr(client, "create_order")
    assert hasattr(client, "create_test_order")
    assert hasattr(client, "get_order")
    assert hasattr(client, "cancel_order")
    assert hasattr(client, "get_open_orders")
    assert hasattr(client, "cancel_all_open_orders")


def test_async_client_has_account_methods():
    """Test that client has account methods."""
    from binance.client import AsyncClient

    client = AsyncClient()
    assert hasattr(client, "get_account")
    assert hasattr(client, "get_my_trades")
    assert hasattr(client, "get_order_rate_limit")
```

**Step 2: Add trade and account endpoints**

```python
# Add to binance/client.py

class AsyncClient:
    # ... existing code ...

    # ============ Trade Endpoints (Signed) ============

    async def create_order(
        self,
        symbol: str,
        side: str,
        type: str,
        quantity: str | None = None,
        quote_order_qty: str | None = None,
        price: str | None = None,
        time_in_force: str | None = None,
        new_client_order_id: str | None = None,
        stop_price: str | None = None,
        iceberg_qty: str | None = None,
        new_order_resp_type: str | None = None,
    ) -> Order:
        """Create a new order.

        Weight: 1
        Requires: Signature

        Args:
            symbol: Trading pair
            side: BUY or SELL
            type: Order type (LIMIT, MARKET, STOP_LOSS, etc.)
            quantity: Order quantity
            quote_order_qty: Quote quantity (for MARKET orders)
            price: Limit price
            time_in_force: GTC, IOC, FOK
            new_client_order_id: Custom order ID for idempotency
            stop_price: Stop price for STOP_LOSS orders
            iceberg_qty: Iceberg quantity
            new_order_resp_type: ACK, RESULT, or FULL

        Returns:
            Order with order_id, status, fills, etc.

        Tip:
            Always provide `new_client_order_id` for idempotent order placement.
            If a network error occurs, you can safely retry with the same client ID -
            Binance will reject duplicates, preventing accidental double orders.
        """
        return await trade.create_order(
            self._http,
            symbol=symbol,
            side=side,
            type=type,
            quantity=quantity,
            quote_order_qty=quote_order_qty,
            price=price,
            time_in_force=time_in_force,
            new_client_order_id=new_client_order_id,
            stop_price=stop_price,
            iceberg_qty=iceberg_qty,
            new_order_resp_type=new_order_resp_type,
        )

    async def create_test_order(
        self,
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
        return await trade.create_test_order(
            self._http,
            symbol=symbol,
            side=side,
            type=type,
            quantity=quantity,
            price=price,
            time_in_force=time_in_force,
        )

    async def get_order(
        self,
        symbol: str,
        order_id: int | None = None,
        orig_client_order_id: str | None = None,
    ) -> Order:
        """Query order status.

        Weight: 4
        Requires: Signature

        Args:
            symbol: Trading pair
            order_id: Order ID (use this or orig_client_order_id)
            orig_client_order_id: Client order ID

        Returns:
            Order with current status
        """
        return await trade.get_order(
            self._http,
            symbol=symbol,
            order_id=order_id,
            orig_client_order_id=orig_client_order_id,
        )

    async def cancel_order(
        self,
        symbol: str,
        order_id: int | None = None,
        orig_client_order_id: str | None = None,
    ) -> CancelOrderResult:
        """Cancel an active order.

        Weight: 1
        Requires: Signature

        Returns:
            CancelOrderResult with final status
        """
        return await trade.cancel_order(
            self._http,
            symbol=symbol,
            order_id=order_id,
            orig_client_order_id=orig_client_order_id,
        )

    async def get_open_orders(
        self,
        symbol: str | None = None,
    ) -> list[Order]:
        """Get all open orders.

        Weight: 6 (with symbol) or 80 (without)
        Requires: Signature

        Returns:
            List of open Order objects
        """
        return await trade.get_open_orders(self._http, symbol=symbol)

    async def cancel_all_open_orders(
        self,
        symbol: str,
    ) -> list[CancelOrderResult]:
        """Cancel all open orders on a symbol.

        Weight: 1
        Requires: Signature

        Returns:
            List of CancelOrderResult for each canceled order
        """
        return await trade.cancel_all_open_orders(self._http, symbol=symbol)

    # ============ Account Endpoints (Signed) ============

    async def get_account(self) -> Account:
        """Get current account information.

        Weight: 20
        Requires: Signature

        Returns:
            Account with balances and permissions
        """
        return await account.get_account(self._http)

    async def get_my_trades(
        self,
        symbol: str,
        order_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        from_id: int | None = None,
        limit: int = 500,
    ) -> list[MyTrade]:
        """Get trades for a specific account and symbol.

        Weight: 20
        Requires: Signature

        Returns:
            List of MyTrade objects
        """
        return await account.get_my_trades(
            self._http,
            symbol=symbol,
            order_id=order_id,
            start_time=start_time,
            end_time=end_time,
            from_id=from_id,
            limit=limit,
        )

    async def get_order_rate_limit(self) -> list[RateLimitInfo]:
        """Get current order count usage.

        Weight: 40
        Requires: Signature

        Returns:
            List of RateLimitInfo with current usage
        """
        return await account.get_order_rate_limit(self._http)
```

**Step 3: Run tests**

Run: `pytest tests/unit/test_client.py -v`
Expected: PASS

**Step 4: Run mypy**

Run: `mypy binance/client.py --strict`
Expected: Success

**Step 5: Commit**

```bash
git add binance/client.py tests/unit/test_client.py
git commit -m "feat: bind trade and account endpoints with typed returns"
```

---

## Task 11.1: Update Package Exports

**Files:**
- Modify: `binance/__init__.py`

**Step 1: Write test**

```python
# Add to tests/unit/test_client.py

def test_async_client_importable_from_package():
    """Test that AsyncClient can be imported from binance package."""
    from binance import AsyncClient
    assert AsyncClient is not None


def test_schemas_exported():
    """Test that key schemas are exported."""
    from binance import AsyncClient
    from binance._schemas.spot import Order, Account, TickerPrice
    # These should be importable
    assert Order is not None
    assert Account is not None
```

**Step 2: Update binance/__init__.py**

```python
# binance/__init__.py
"""Binance API Python Wrapper.

High-performance async client for Binance REST API with typed returns.

Usage:
    from binance import AsyncClient

    async with AsyncClient(api_key="...", api_secret="...") as client:
        # Get market data - returns typed schemas
        ticker = await client.get_ticker_price(symbol="BTCUSDT")
        print(ticker.price)  # IDE autocomplete works!

        # Get account info
        account = await client.get_account()
        for balance in account.balances:
            if float(balance.free) > 0:
                print(f"{balance.asset}: {balance.free}")

        # Place order
        order = await client.create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="MARKET",
            quantity="0.001",
        )
        print(f"Order {order.order_id} status: {order.status}")
"""
from binance.client import AsyncClient

__all__ = ["AsyncClient"]
__version__ = "2.0.0"
```

**Step 3: Run tests**

Run: `pytest tests/unit/test_client.py -v`
Expected: PASS

**Step 4: Commit**

```bash
git add binance/__init__.py tests/unit/test_client.py
git commit -m "feat: export AsyncClient from binance package"
```

---

## Task 11.2: Add Mock-Based Unit Tests

**Files:**
- Create: `tests/unit/test_client_mocked.py`

**Purpose:** Full coverage with mocked HTTP layer (no network required).

```python
# tests/unit/test_client_mocked.py
"""Unit tests for AsyncClient with mocked HTTP layer."""
from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from binance.client import AsyncClient
from binance._schemas.spot import (
    ServerTime, Order, Account, TickerPrice, OrderBook,
)


@pytest.fixture
def mock_client():
    """Create AsyncClient with mocked HTTP."""
    client = AsyncClient(api_key="test", api_secret="test")
    client._http = MagicMock()
    client._http.request = AsyncMock()
    client._http.request_raw = AsyncMock()
    return client


class TestGeneralEndpoints:
    """Test general endpoints with mocks."""

    @pytest.mark.asyncio
    async def test_ping_returns_empty_dict(self, mock_client):
        """Test ping returns empty dict."""
        mock_client._http.request.return_value = {}

        with patch('binance.api.spot.general.ping', new_callable=AsyncMock) as mock:
            mock.return_value = {}
            result = await mock_client.ping()
            assert result == {}

    @pytest.mark.asyncio
    async def test_get_server_time_returns_typed(self, mock_client):
        """Test get_server_time returns ServerTime."""
        with patch('binance.api.spot.general.get_server_time', new_callable=AsyncMock) as mock:
            mock.return_value = ServerTime(server_time=1699999999999)
            result = await mock_client.get_server_time()
            assert isinstance(result, ServerTime)
            assert result.server_time == 1699999999999


class TestMarketEndpoints:
    """Test market endpoints with mocks."""

    @pytest.mark.asyncio
    async def test_get_order_book_returns_typed(self, mock_client):
        """Test get_order_book returns OrderBook."""
        with patch('binance.api.spot.market.get_order_book', new_callable=AsyncMock) as mock:
            mock.return_value = OrderBook(
                last_update_id=123,
                bids=[["50000", "1"]],
                asks=[["50001", "2"]],
            )
            result = await mock_client.get_order_book(symbol="BTCUSDT")
            assert isinstance(result, OrderBook)
            assert result.last_update_id == 123

    @pytest.mark.asyncio
    async def test_get_ticker_price_single_returns_single(self, mock_client):
        """Test single symbol returns TickerPrice."""
        with patch('binance.api.spot.market.get_ticker_price', new_callable=AsyncMock) as mock:
            mock.return_value = TickerPrice(symbol="BTCUSDT", price="50000")
            result = await mock_client.get_ticker_price(symbol="BTCUSDT")
            assert isinstance(result, TickerPrice)

    @pytest.mark.asyncio
    async def test_get_ticker_price_no_symbol_returns_list(self, mock_client):
        """Test no symbol returns list."""
        with patch('binance.api.spot.market.get_ticker_price', new_callable=AsyncMock) as mock:
            mock.return_value = [
                TickerPrice(symbol="BTCUSDT", price="50000"),
                TickerPrice(symbol="ETHUSDT", price="3000"),
            ]
            result = await mock_client.get_ticker_price()
            assert isinstance(result, list)
            assert len(result) == 2


class TestTradeEndpoints:
    """Test trade endpoints with mocks."""

    @pytest.mark.asyncio
    async def test_create_order_returns_typed(self, mock_client):
        """Test create_order returns Order."""
        with patch('binance.api.spot.trade.create_order', new_callable=AsyncMock) as mock:
            mock.return_value = Order(
                symbol="BTCUSDT",
                order_id=123456,
                order_list_id=-1,
                client_order_id="test",
                transact_time=1699999999999,
                status="FILLED",
            )
            result = await mock_client.create_order(
                symbol="BTCUSDT",
                side="BUY",
                type="MARKET",
                quantity="0.001",
            )
            assert isinstance(result, Order)
            assert result.order_id == 123456


class TestAccountEndpoints:
    """Test account endpoints with mocks."""

    @pytest.mark.asyncio
    async def test_get_account_returns_typed(self, mock_client):
        """Test get_account returns Account."""
        with patch('binance.api.spot.account.get_account', new_callable=AsyncMock) as mock:
            from binance._schemas.spot import Balance
            mock.return_value = Account(
                maker_commission=10,
                taker_commission=10,
                buyer_commission=0,
                seller_commission=0,
                can_trade=True,
                can_withdraw=True,
                can_deposit=True,
                update_time=1699999999999,
                account_type="SPOT",
                balances=[Balance(asset="BTC", free="1.0", locked="0.0")],
                permissions=["SPOT"],
            )
            result = await mock_client.get_account()
            assert isinstance(result, Account)
            assert result.balances[0].asset == "BTC"
```

**Step 2: Run mocked tests**

Run: `pytest tests/unit/test_client_mocked.py -v`
Expected: PASS

**Step 3: Commit**

```bash
git add tests/unit/test_client_mocked.py
git commit -m "test: add mock-based unit tests for AsyncClient"
```

---

## Next Steps

Continue with [04-integration-testing.md](./04-integration-testing.md) to test against Binance testnet.
