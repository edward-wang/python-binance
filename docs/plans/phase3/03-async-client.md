# Phase 3.3: Create AsyncClient Entry Point

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create `binance/client.py` with `AsyncClient` that binds generated endpoint methods.

**Prerequisites:** Tasks 1-6 complete (api/spot/ and _schemas/spot.py exist)

---

## Task 7: Create AsyncClient Skeleton

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

This thin wrapper binds generated endpoint methods from api/spot/ modules
to provide a clean interface for users.

Usage:
    async with AsyncClient(api_key="...", api_secret="...") as client:
        # Market data (public)
        klines = await client.get_klines(symbol="BTCUSDT", interval="1h")

        # Account data (signed)
        account = await client.get_account()

        # Trading (signed)
        order = await client.create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="MARKET",
            quantity="0.001",
        )
"""
from typing import Any

from binance._core.http import HTTPClient


class AsyncClient:
    """Async client for Binance Spot API.

    All methods are async and must be awaited.
    Use as async context manager for automatic connection handling.
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

## Task 8: Bind General Endpoints

**Files:**
- Modify: `binance/client.py`
- Modify: `tests/unit/test_client.py`

**Step 1: Write the failing test**

```python
# Add to tests/unit/test_client.py

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
    assert callable(client.get_server_time)


def test_async_client_has_get_exchange_info():
    """Test that client has get_exchange_info method."""
    from binance.client import AsyncClient

    client = AsyncClient()
    assert hasattr(client, "get_exchange_info")
    assert callable(client.get_exchange_info)
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/test_client.py::test_async_client_has_ping -v`
Expected: FAIL with "assert hasattr(client, 'ping')"

**Step 3: Add general endpoint methods**

```python
# Add to binance/client.py after the class definition

from binance.api.spot import general


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

    async def get_server_time(self) -> dict[str, Any]:
        """Test connectivity and get current server time.

        Weight: 1

        Returns:
            Server time in milliseconds
        """
        return await general.get_server_time(self._http)

    async def get_exchange_info(
        self,
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
git commit -m "feat: bind general endpoints to AsyncClient"
```

---

## Task 9: Bind Market, Trade, and Account Endpoints

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
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/test_client.py::test_async_client_has_market_methods -v`
Expected: FAIL

**Step 3: Add all endpoint imports and method bindings**

```python
# binance/client.py
"""AsyncClient - Main entry point for Binance API."""
from typing import Any

from binance._core.http import HTTPClient
from binance.api.spot import general, market, trade, account


class AsyncClient:
    """Async client for Binance Spot API."""

    __slots__ = ("_http",)

    def __init__(
        self,
        api_key: str = "",
        api_secret: str = "",
        testnet: bool = False,
        base_url: str | None = None,
        timeout: float = 10.0,
    ) -> None:
        """Initialize AsyncClient."""
        self._http = HTTPClient(
            api_key=api_key,
            api_secret=api_secret,
            testnet=testnet,
            base_url=base_url,
            timeout=timeout,
        )

    async def __aenter__(self) -> "AsyncClient":
        await self._http.connect()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self._http.close()

    async def connect(self) -> None:
        """Initialize connection pool."""
        await self._http.connect()

    async def close(self) -> None:
        """Close connection pool."""
        await self._http.close()

    # ============ General Endpoints ============

    async def ping(self) -> dict[str, Any]:
        """Test connectivity to the Rest API. Weight: 1"""
        return await general.ping(self._http)

    async def get_server_time(self) -> dict[str, Any]:
        """Get current server time. Weight: 1"""
        return await general.get_server_time(self._http)

    async def get_exchange_info(
        self,
        symbol: str | None = None,
        symbols: list[str] | None = None,
        permissions: list[str] | None = None,
    ) -> dict[str, Any]:
        """Get exchange trading rules and symbol information. Weight: 20"""
        return await general.get_exchange_info(
            self._http, symbol=symbol, symbols=symbols, permissions=permissions
        )

    # ============ Market Data Endpoints ============

    async def get_order_book(
        self,
        symbol: str,
        limit: int = 100,
    ) -> dict[str, Any]:
        """Get order book depth. Weight: 5-50 depending on limit."""
        return await market.get_order_book(self._http, symbol=symbol, limit=limit)

    async def get_trades(
        self,
        symbol: str,
        limit: int = 500,
    ) -> list[dict[str, Any]]:
        """Get recent trades. Weight: 10"""
        return await market.get_trades(self._http, symbol=symbol, limit=limit)

    async def get_agg_trades(
        self,
        symbol: str,
        from_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 500,
    ) -> list[dict[str, Any]]:
        """Get aggregated trades. Weight: 2"""
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
    ) -> list[list[Any]]:
        """Get kline/candlestick bars. Weight: 2"""
        return await market.get_klines(
            self._http,
            symbol=symbol,
            interval=interval,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    async def get_avg_price(self, symbol: str) -> dict[str, Any]:
        """Get current average price. Weight: 2"""
        return await market.get_avg_price(self._http, symbol=symbol)

    async def get_ticker_24h(
        self,
        symbol: str | None = None,
        symbols: list[str] | None = None,
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Get 24hr ticker price change statistics. Weight: 1-80"""
        return await market.get_ticker_24h(
            self._http, symbol=symbol, symbols=symbols
        )

    async def get_ticker_price(
        self,
        symbol: str | None = None,
        symbols: list[str] | None = None,
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Get symbol price ticker. Weight: 1-4"""
        return await market.get_ticker_price(
            self._http, symbol=symbol, symbols=symbols
        )

    async def get_book_ticker(
        self,
        symbol: str | None = None,
        symbols: list[str] | None = None,
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Get best bid/ask price. Weight: 1-4"""
        return await market.get_book_ticker(
            self._http, symbol=symbol, symbols=symbols
        )

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
    ) -> dict[str, Any]:
        """Create a new order. Weight: 1"""
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
        """Test new order creation (no actual order placed). Weight: 1"""
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
    ) -> dict[str, Any]:
        """Query order status. Weight: 4"""
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
    ) -> dict[str, Any]:
        """Cancel an active order. Weight: 1"""
        return await trade.cancel_order(
            self._http,
            symbol=symbol,
            order_id=order_id,
            orig_client_order_id=orig_client_order_id,
        )

    async def get_open_orders(
        self,
        symbol: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get all open orders. Weight: 6 or 80"""
        return await trade.get_open_orders(self._http, symbol=symbol)

    async def cancel_all_open_orders(
        self,
        symbol: str,
    ) -> list[dict[str, Any]]:
        """Cancel all open orders on a symbol. Weight: 1"""
        return await trade.cancel_all_open_orders(self._http, symbol=symbol)

    # ============ Account Endpoints (Signed) ============

    async def get_account(self) -> dict[str, Any]:
        """Get current account information. Weight: 20"""
        return await account.get_account(self._http)

    async def get_my_trades(
        self,
        symbol: str,
        order_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        from_id: int | None = None,
        limit: int = 500,
    ) -> list[dict[str, Any]]:
        """Get trades for a specific account and symbol. Weight: 20"""
        return await account.get_my_trades(
            self._http,
            symbol=symbol,
            order_id=order_id,
            start_time=start_time,
            end_time=end_time,
            from_id=from_id,
            limit=limit,
        )

    async def get_order_rate_limit(self) -> list[dict[str, Any]]:
        """Get current order count usage. Weight: 40"""
        return await account.get_order_rate_limit(self._http)
```

**Step 4: Run tests**

Run: `pytest tests/unit/test_client.py -v`
Expected: PASS

**Step 5: Run mypy**

Run: `mypy binance/client.py --strict`
Expected: Success

**Step 6: Commit**

```bash
git add binance/client.py tests/unit/test_client.py
git commit -m "feat: bind all spot endpoints to AsyncClient"
```

---

## Task 9.1: Update Package Exports

**Files:**
- Modify: `binance/__init__.py`

**Step 1: Write test**

```python
# Add to tests/unit/test_client.py

def test_async_client_importable_from_package():
    """Test that AsyncClient can be imported from binance package."""
    from binance import AsyncClient
    assert AsyncClient is not None
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/test_client.py::test_async_client_importable_from_package -v`
Expected: FAIL

**Step 3: Update binance/__init__.py**

```python
# binance/__init__.py
"""Binance API Python Wrapper.

High-performance async client for Binance REST API.

Usage:
    from binance import AsyncClient

    async with AsyncClient(api_key="...", api_secret="...") as client:
        # Get market data
        klines = await client.get_klines(symbol="BTCUSDT", interval="1h")

        # Place order
        order = await client.create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="MARKET",
            quantity="0.001",
        )
"""
from binance.client import AsyncClient

__all__ = ["AsyncClient"]
__version__ = "0.1.0"
```

**Step 4: Run tests**

Run: `pytest tests/unit/test_client.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add binance/__init__.py tests/unit/test_client.py
git commit -m "feat: export AsyncClient from binance package"
```

---

## Next Steps

Continue with [04-integration-testing.md](./04-integration-testing.md) to test against Binance testnet.
