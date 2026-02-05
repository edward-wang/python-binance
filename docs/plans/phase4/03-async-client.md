# Phase 4.3: Extend AsyncClient with Futures Methods

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Extend `binance/client.py` with USDT-M and COIN-M futures methods that return typed schemas.

**Prerequisites:** Tasks 1-8 complete (api/futures_um/, api/futures_cm/, _schemas/futures.py exist)

---

## Task 9: Fix HTTPClient Time Sync for Multiple APIs

**Problem:** HTTPClient._sync_server_time() hardcodes `/api/v3/time` (Spot). Futures clients with `/fapi/` or `/dapi/` base URLs will fail because that endpoint doesn't exist.

**Solution:** Add configurable `time_sync_path` parameter to HTTPClient.

**Files:**
- Modify: `binance/_core/http.py`
- Create: `tests/unit/test_http_time_sync.py`

**Step 1: Write the failing test**

```python
# tests/unit/test_http_time_sync.py
"""Test HTTPClient time sync configuration."""
import pytest


def test_http_client_default_time_sync_path():
    """Test default time sync path is spot endpoint."""
    from binance._core.http import HTTPClient

    client = HTTPClient()
    assert client._time_sync_path == "/api/v3/time"


def test_http_client_custom_time_sync_path():
    """Test custom time sync path for futures."""
    from binance._core.http import HTTPClient

    client = HTTPClient(time_sync_path="/fapi/v1/time")
    assert client._time_sync_path == "/fapi/v1/time"


def test_http_client_disable_time_sync():
    """Test disabling time sync."""
    from binance._core.http import HTTPClient

    client = HTTPClient(time_sync_path=None)
    assert client._time_sync_path is None


def test_context_has_offset_initially_false():
    """Test has_offset returns False before time sync."""
    from binance._core.context import context

    # Reset offset for test
    context._server_time_offset = 0
    assert context.has_offset() is False


def test_context_has_offset_true_after_sync():
    """Test has_offset returns True after offset is set."""
    from binance._core.context import context

    context._server_time_offset = 100  # Simulate time sync
    assert context.has_offset() is True
    context._server_time_offset = 0  # Reset
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/test_http_time_sync.py -v`
Expected: FAIL with "AttributeError: 'HTTPClient' object has no attribute '_time_sync_path'"

**Step 3: Update HTTPClient**

```python
# Modify binance/_core/http.py

class HTTPClient:
    """Async HTTP client with connection pooling and auto-retry."""

    __slots__ = (
        "_api_key",
        "_api_secret",
        "_base_url",
        "_session",
        "_connector",
        "_timeout",
        "_time_sync_path",  # NEW
    )

    def __init__(
        self,
        api_key: str = "",
        api_secret: str = "",
        testnet: bool = False,
        base_url: str | None = None,
        timeout: float = TIMEOUT_DEFAULT,
        time_sync_path: str | None = "/api/v3/time",  # NEW: configurable, None to disable
    ) -> None:
        """Initialize HTTP client.

        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            testnet: Use testnet URLs if True
            base_url: Override base URL
            timeout: Request timeout in seconds
            time_sync_path: Path for time sync endpoint. Use:
                - "/api/v3/time" for Spot (default)
                - "/fapi/v1/time" for USDT-M Futures
                - "/dapi/v1/time" for COIN-M Futures
                - None to disable time sync (share offset from another client)
        """
        self._api_key = api_key
        self._api_secret = api_secret
        self._base_url = base_url or BASE_URLS["spot_testnet" if testnet else "spot"]
        self._session: aiohttp.ClientSession | None = None
        self._connector: aiohttp.TCPConnector | None = None
        self._timeout = aiohttp.ClientTimeout(total=timeout)
        self._time_sync_path = time_sync_path  # NEW

    async def connect(self) -> None:
        """Initialize connection pool and sync server time."""
        self._connector = aiohttp.TCPConnector(
            limit=POOL_CONNECTIONS,
            keepalive_timeout=POOL_KEEPALIVE,
            ttl_dns_cache=DNS_CACHE_TTL,
        )
        self._session = aiohttp.ClientSession(
            connector=self._connector,
            timeout=self._timeout,
            json_serialize=lambda x: orjson.dumps(x).decode(),
        )
        # Conditional time sync - skip if disabled or offset already set
        if self._time_sync_path and not context.has_offset():
            await self._sync_server_time()

    async def _sync_server_time(self) -> None:
        """Fetch server time and update offset."""
        if self._time_sync_path is None:
            return
        data = await self.request("GET", self._time_sync_path, signed=False)
        context.update_offset(data["serverTime"])
```

**Step 4: Update context.py to add has_offset()**

```python
# Add to binance/_core/context.py

class _Context:
    # ... existing code ...

    def has_offset(self) -> bool:
        """Check if time offset has been set."""
        return self._server_time_offset != 0
```

**Step 5: Fix request_raw() to handle TimestampError**

The existing `request_raw()` method doesn't handle `TimestampError` for auto-retry like `request()` does. For signed futures endpoints, timestamp errors would fail without retry.

```python
# Update request_raw() in binance/_core/http.py

    async def request_raw(
        self,
        method: str,
        path: str,
        signed: bool = False,
        params: dict[str, Any] | None = None,
    ) -> bytes:
        """Execute HTTP request and return raw bytes.

        Used by generated code with pre-compiled decoders.
        """
        params = dict(params) if params else {}

        if signed:
            params = sign_request(params, self._api_secret)

        headers = {}
        if self._api_key:
            headers["X-MBX-APIKEY"] = self._api_key

        url = f"{self._base_url}{path}"

        try:
            return await self._do_request_raw(method, url, params, headers)
        except TimestampError:
            # Self-healing: sync time and retry once
            await self._sync_server_time()
            if signed:
                # Re-sign with updated timestamp
                params = {k: v for k, v in params.items() if k not in ("timestamp", "signature")}
                params = sign_request(params, self._api_secret)
            return await self._do_request_raw(method, url, params, headers)

    async def _do_request_raw(
        self,
        method: str,
        url: str,
        params: dict[str, Any],
        headers: dict[str, str],
    ) -> bytes:
        """Execute single HTTP request returning raw bytes."""
        if self._session is None:
            raise RuntimeError("HTTPClient not connected. Call connect() first.")

        try:
            async with self._session.request(
                method,
                url,
                params=params if method == "GET" else None,
                data=params if method != "GET" else None,
                headers=headers,
            ) as response:
                raw = await response.read()

                # Extract metadata and check errors
                meta = APIErrorMeta(
                    used_weight=_parse_int(response.headers.get("X-MBX-USED-WEIGHT-1M")),
                    retry_after=_parse_int(response.headers.get("Retry-After")),
                )

                if response.status >= 400:
                    data = orjson.loads(raw) if raw else {}
                    raise_for_error(response.status, data, meta)

                return raw

        except aiohttp.ClientConnectorError as e:
            raise ConnectionError(str(e), method=method, path=url) from e
        except aiohttp.ServerTimeoutError as e:
            raise TimeoutError(str(e), method=method, path=url) from e
```

**Step 6: Run tests**

Run: `pytest tests/unit/test_http_time_sync.py -v`
Expected: PASS

**Step 7: Commit**

```bash
git add binance/_core/http.py binance/_core/context.py tests/unit/test_http_time_sync.py
git commit -m "feat: add configurable time_sync_path to HTTPClient and fix request_raw retry"
```

---

## Task 10: Add Futures HTTPClient Instances with Lazy Initialization

**Files:**
- Modify: `binance/client.py`
- Create: `tests/unit/test_client_futures.py`

**Step 1: Write the failing test**

```python
# tests/unit/test_client_futures.py
"""Test AsyncClient futures HTTP client support."""
import pytest


def test_async_client_has_futures_properties():
    """Test that client has futures HTTP client properties."""
    from binance.client import AsyncClient

    client = AsyncClient(testnet=True)
    assert hasattr(client, "_http_futures_um")
    assert hasattr(client, "_http_futures_cm")


def test_async_client_futures_lazy_init():
    """Test futures clients are lazily initialized."""
    from binance.client import AsyncClient

    client = AsyncClient(testnet=True)
    # Before accessing, internal storage should be None
    assert client._AsyncClient__http_futures_um is None
    assert client._AsyncClient__http_futures_cm is None


def test_async_client_futures_testnet_urls():
    """Test futures clients use correct testnet URLs."""
    from binance.client import AsyncClient
    from binance._core.config import BASE_URLS

    client = AsyncClient(testnet=True)
    # Access to trigger lazy init
    um_client = client._http_futures_um
    cm_client = client._http_futures_cm

    assert um_client._base_url == BASE_URLS["futures_um_testnet"]
    assert cm_client._base_url == BASE_URLS["futures_cm_testnet"]
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/test_client_futures.py -v`
Expected: FAIL

**Step 3: Update AsyncClient with lazy-initialized futures clients**

```python
# Modify binance/client.py

from binance._core.config import BASE_URLS, get_base_url
from binance._core.http import HTTPClient

# Add futures schema imports
from binance._schemas.futures import (
    FuturesExchangeInfo,
    FuturesKline,
    FuturesOrder,
    FuturesAccount,
    FuturesBalance,
    PositionRisk,
    MarkPrice,
    FundingRate,
    LeverageResult,
    FuturesTicker24h,
    FuturesMyTrade,
    BatchOrderError,
)


class AsyncClient:
    """Async client for Binance API.

    Supports Spot, USDT-M Futures, and COIN-M Futures APIs.
    All methods return typed msgspec schemas.

    Futures clients are lazily initialized on first use to avoid
    unnecessary connections when only using spot API.
    """

    __slots__ = (
        "_http",
        "__http_futures_um",
        "__http_futures_cm",
        "_api_key",
        "_api_secret",
        "_testnet",
        "_timeout",
    )

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
            base_url: Override spot base URL (ignores testnet if set)
            timeout: Request timeout in seconds
        """
        # Store for lazy init of futures clients
        self._api_key = api_key
        self._api_secret = api_secret
        self._testnet = testnet
        self._timeout = timeout

        # Spot API - always initialized
        spot_url = base_url or get_base_url("spot", testnet)
        self._http = HTTPClient(
            api_key=api_key,
            api_secret=api_secret,
            base_url=spot_url,
            timeout=timeout,
            time_sync_path="/api/v3/time",  # Spot time sync
        )

        # Futures clients - lazy initialized
        self.__http_futures_um: HTTPClient | None = None
        self.__http_futures_cm: HTTPClient | None = None

    @property
    def _http_futures_um(self) -> HTTPClient:
        """Get USDT-M futures HTTP client (lazy initialized)."""
        if self.__http_futures_um is None:
            self.__http_futures_um = HTTPClient(
                api_key=self._api_key,
                api_secret=self._api_secret,
                base_url=get_base_url("futures_um", self._testnet),
                timeout=self._timeout,
                time_sync_path=None,  # Share offset from spot client
            )
        return self.__http_futures_um

    @property
    def _http_futures_cm(self) -> HTTPClient:
        """Get COIN-M futures HTTP client (lazy initialized)."""
        if self.__http_futures_cm is None:
            self.__http_futures_cm = HTTPClient(
                api_key=self._api_key,
                api_secret=self._api_secret,
                base_url=get_base_url("futures_cm", self._testnet),
                timeout=self._timeout,
                time_sync_path=None,  # Share offset from spot client
            )
        return self.__http_futures_cm

    async def __aenter__(self) -> "AsyncClient":
        """Async context manager entry."""
        await self._http.connect()
        # Futures clients connect on first use (lazy)
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit."""
        await self.close()

    async def connect(self) -> None:
        """Initialize spot connection pool.

        Futures clients connect lazily on first use.
        """
        await self._http.connect()

    async def close(self) -> None:
        """Close all connection pools."""
        await self._http.close()
        if self.__http_futures_um is not None:
            await self.__http_futures_um.close()
        if self.__http_futures_cm is not None:
            await self.__http_futures_cm.close()

    async def _ensure_futures_um_connected(self) -> HTTPClient:
        """Ensure USDT-M futures client is connected."""
        client = self._http_futures_um
        if client._session is None:
            await client.connect()
        return client

    async def _ensure_futures_cm_connected(self) -> HTTPClient:
        """Ensure COIN-M futures client is connected."""
        client = self._http_futures_cm
        if client._session is None:
            await client.connect()
        return client
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/unit/test_client.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add binance/client.py tests/unit/test_client.py
git commit -m "feat: add futures HTTP client support to AsyncClient"
```

---

## Task 11: Bind USDT-M Futures General and Market Endpoints

**Files:**
- Modify: `binance/client.py`
- Modify: `tests/unit/test_client.py`

**Step 1: Write the failing test**

```python
# Add to tests/unit/test_client.py

def test_async_client_has_futures_um_general_methods():
    """Test that client has USDT-M futures general methods."""
    from binance.client import AsyncClient

    client = AsyncClient()
    assert hasattr(client, "futures_ping")
    assert hasattr(client, "futures_get_server_time")
    assert hasattr(client, "futures_get_exchange_info")


def test_async_client_has_futures_um_market_methods():
    """Test that client has USDT-M futures market methods."""
    from binance.client import AsyncClient

    client = AsyncClient()
    assert hasattr(client, "futures_get_klines")
    assert hasattr(client, "futures_get_order_book")
    assert hasattr(client, "futures_get_mark_price")
    assert hasattr(client, "futures_get_funding_rate")
    assert hasattr(client, "futures_get_ticker_24h")
    assert hasattr(client, "futures_get_ticker_price")
```

**Step 2: Add USDT-M general and market methods**

**Important:** All futures methods MUST use `await self._ensure_futures_um_connected()` to get a connected HTTP client. This enables lazy connection on first use.

```python
# Add to binance/client.py

from binance.api import futures_um, futures_cm
from binance._schemas.spot import ServerTime, OrderBook, Trade, AggTrade, TickerPrice, BookTicker

class AsyncClient:
    # ... existing code ...

    # ============ USDT-M Futures General Endpoints ============

    async def futures_ping(self) -> dict[str, Any]:
        """Test connectivity to USDT-M Futures API.

        Weight: 1

        Returns:
            Empty dict on success
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.general.ping(http)

    async def futures_get_server_time(self) -> ServerTime:
        """Get USDT-M Futures server time.

        Weight: 1

        Returns:
            ServerTime with server_time in milliseconds
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.general.get_server_time(http)

    async def futures_get_exchange_info(self) -> FuturesExchangeInfo:
        """Get USDT-M Futures exchange trading rules.

        Weight: 1

        Returns:
            FuturesExchangeInfo with symbols and rate limits
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.general.get_exchange_info(http)

    # ============ USDT-M Futures Market Data Endpoints ============

    async def futures_get_order_book(
        self,
        symbol: str,
        limit: int = 500,
    ) -> OrderBook:
        """Get USDT-M futures order book depth.

        Weight: 5-20 depending on limit

        Args:
            symbol: Trading pair (e.g., "BTCUSDT")
            limit: Depth limit (5, 10, 20, 50, 100, 500, 1000)

        Returns:
            OrderBook with bids and asks
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.market.get_order_book(http, symbol=symbol, limit=limit)

    async def futures_get_trades(
        self,
        symbol: str,
        limit: int = 500,
    ) -> list[Trade]:
        """Get USDT-M futures recent trades.

        Weight: 5

        Returns:
            List of Trade objects
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.market.get_trades(http, symbol=symbol, limit=limit)

    async def futures_get_agg_trades(
        self,
        symbol: str,
        from_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 500,
    ) -> list[AggTrade]:
        """Get USDT-M futures aggregated trades.

        Weight: 20

        Returns:
            List of AggTrade objects
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.market.get_agg_trades(
            http,
            symbol=symbol,
            from_id=from_id,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    async def futures_get_klines(
        self,
        symbol: str,
        interval: str,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 500,
    ) -> list[FuturesKline]:
        """Get USDT-M futures kline/candlestick bars.

        Weight: 5

        Args:
            symbol: Trading pair (e.g., "BTCUSDT")
            interval: Kline interval (1m, 5m, 15m, 1h, 4h, 1d, etc.)
            start_time: Start time in ms
            end_time: End time in ms
            limit: Number of klines (max 1500)

        Returns:
            List of FuturesKline objects with typed fields
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.market.get_klines(
            http,
            symbol=symbol,
            interval=interval,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    async def futures_get_continuous_klines(
        self,
        pair: str,
        contract_type: str,
        interval: str,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 500,
    ) -> list[FuturesKline]:
        """Get USDT-M continuous contract klines.

        Weight: 5

        Args:
            pair: Trading pair (e.g., "BTCUSDT")
            contract_type: PERPETUAL, CURRENT_QUARTER, NEXT_QUARTER
            interval: Kline interval

        Returns:
            List of FuturesKline objects
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.market.get_continuous_klines(
            http,
            pair=pair,
            contract_type=contract_type,
            interval=interval,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    @overload
    async def futures_get_mark_price(self, symbol: str) -> MarkPrice: ...
    @overload
    async def futures_get_mark_price(self, symbol: None = None) -> list[MarkPrice]: ...

    async def futures_get_mark_price(
        self,
        symbol: str | None = None,
    ) -> MarkPrice | list[MarkPrice]:
        """Get USDT-M futures mark price and funding rate.

        Weight: 1

        Args:
            symbol: Trading pair (returns single) or None (returns all)

        Returns:
            MarkPrice if symbol specified, else list[MarkPrice]
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.market.get_mark_price(http, symbol=symbol)

    async def futures_get_funding_rate(
        self,
        symbol: str,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 100,
    ) -> list[FundingRate]:
        """Get USDT-M futures funding rate history.

        Weight: 1

        Returns:
            List of FundingRate objects
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.market.get_funding_rate(
            http,
            symbol=symbol,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    @overload
    async def futures_get_ticker_24h(self, symbol: str) -> FuturesTicker24h: ...
    @overload
    async def futures_get_ticker_24h(self, symbol: None = None) -> list[FuturesTicker24h]: ...

    async def futures_get_ticker_24h(
        self,
        symbol: str | None = None,
    ) -> FuturesTicker24h | list[FuturesTicker24h]:
        """Get USDT-M futures 24hr ticker.

        Weight: 1-40 depending on parameters

        Returns:
            FuturesTicker24h if symbol specified, else list
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.market.get_ticker_24h(http, symbol=symbol)

    @overload
    async def futures_get_ticker_price(self, symbol: str) -> TickerPrice: ...
    @overload
    async def futures_get_ticker_price(self, symbol: None = None) -> list[TickerPrice]: ...

    async def futures_get_ticker_price(
        self,
        symbol: str | None = None,
    ) -> TickerPrice | list[TickerPrice]:
        """Get USDT-M futures symbol price ticker.

        Weight: 1-2

        Returns:
            TickerPrice if symbol specified, else list
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.market.get_ticker_price(http, symbol=symbol)

    @overload
    async def futures_get_book_ticker(self, symbol: str) -> BookTicker: ...
    @overload
    async def futures_get_book_ticker(self, symbol: None = None) -> list[BookTicker]: ...

    async def futures_get_book_ticker(
        self,
        symbol: str | None = None,
    ) -> BookTicker | list[BookTicker]:
        """Get USDT-M futures best bid/ask price.

        Weight: 1-2

        Returns:
            BookTicker if symbol specified, else list
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.market.get_book_ticker(http, symbol=symbol)
```

**Step 3: Run tests**

Run: `pytest tests/unit/test_client.py -v`
Expected: PASS

**Step 4: Commit**

```bash
git add binance/client.py tests/unit/test_client.py
git commit -m "feat: bind USDT-M futures general and market endpoints"
```

---

## Task 12: Bind USDT-M Futures Trade and Account Endpoints

**Files:**
- Modify: `binance/client.py`
- Modify: `tests/unit/test_client.py`

**Step 1: Write the failing test**

```python
# Add to tests/unit/test_client.py

def test_async_client_has_futures_um_trade_methods():
    """Test that client has USDT-M futures trading methods."""
    from binance.client import AsyncClient

    client = AsyncClient()
    assert hasattr(client, "futures_create_order")
    assert hasattr(client, "futures_create_test_order")
    assert hasattr(client, "futures_get_order")
    assert hasattr(client, "futures_cancel_order")
    assert hasattr(client, "futures_cancel_all_open_orders")
    assert hasattr(client, "futures_get_open_orders")
    assert hasattr(client, "futures_create_batch_orders")


def test_async_client_has_futures_um_account_methods():
    """Test that client has USDT-M futures account methods."""
    from binance.client import AsyncClient

    client = AsyncClient()
    assert hasattr(client, "futures_get_account")
    assert hasattr(client, "futures_get_balance")
    assert hasattr(client, "futures_get_position_risk")
    assert hasattr(client, "futures_set_leverage")
    assert hasattr(client, "futures_set_margin_type")
```

**Step 2: Add USDT-M trade and account methods**

```python
# Add to binance/client.py

class AsyncClient:
    # ... existing code ...

    # ============ USDT-M Futures Trade Endpoints (Signed) ============

    async def futures_create_order(
        self,
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
        """Create a new USDT-M futures order.

        Weight: 1
        Requires: Signature

        Args:
            symbol: Trading pair (e.g., "BTCUSDT")
            side: BUY or SELL
            type: LIMIT, MARKET, STOP, STOP_MARKET, TAKE_PROFIT,
                  TAKE_PROFIT_MARKET, TRAILING_STOP_MARKET
            quantity: Order quantity
            price: Limit price
            time_in_force: GTC, IOC, FOK, GTX
            reduce_only: Reduce position only
            new_client_order_id: Custom order ID for idempotency
            stop_price: Stop price
            position_side: LONG, SHORT, or BOTH (hedge mode)
            close_position: Close all position
            activation_price: For TRAILING_STOP_MARKET
            callback_rate: For TRAILING_STOP_MARKET
            working_type: MARK_PRICE or CONTRACT_PRICE
            price_protect: Price protection
            new_order_resp_type: ACK or RESULT

        Returns:
            FuturesOrder with order details

        Tip:
            Always provide `new_client_order_id` for idempotent order placement.
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.trade.create_order(
            http,
            symbol=symbol,
            side=side,
            type=type,
            quantity=quantity,
            price=price,
            time_in_force=time_in_force,
            reduce_only=reduce_only,
            new_client_order_id=new_client_order_id,
            stop_price=stop_price,
            position_side=position_side,
            close_position=close_position,
            activation_price=activation_price,
            callback_rate=callback_rate,
            working_type=working_type,
            price_protect=price_protect,
            new_order_resp_type=new_order_resp_type,
        )

    async def futures_create_test_order(
        self,
        symbol: str,
        side: str,
        type: str,
        quantity: str | None = None,
        price: str | None = None,
        time_in_force: str | None = None,
    ) -> dict[str, Any]:
        """Test USDT-M futures order creation (no actual order placed).

        Weight: 1
        Requires: Signature

        Returns:
            Empty dict on success
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.trade.create_test_order(
            http,
            symbol=symbol,
            side=side,
            type=type,
            quantity=quantity,
            price=price,
            time_in_force=time_in_force,
        )

    async def futures_get_order(
        self,
        symbol: str,
        order_id: int | None = None,
        orig_client_order_id: str | None = None,
    ) -> FuturesOrder:
        """Query USDT-M futures order status.

        Weight: 1
        Requires: Signature

        Returns:
            FuturesOrder with current status
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.trade.get_order(
            http,
            symbol=symbol,
            order_id=order_id,
            orig_client_order_id=orig_client_order_id,
        )

    async def futures_cancel_order(
        self,
        symbol: str,
        order_id: int | None = None,
        orig_client_order_id: str | None = None,
    ) -> FuturesOrder:
        """Cancel an active USDT-M futures order.

        Weight: 1
        Requires: Signature

        Returns:
            FuturesOrder with canceled status
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.trade.cancel_order(
            http,
            symbol=symbol,
            order_id=order_id,
            orig_client_order_id=orig_client_order_id,
        )

    async def futures_cancel_all_open_orders(
        self,
        symbol: str,
    ) -> dict[str, Any]:
        """Cancel all open USDT-M futures orders on a symbol.

        Weight: 1
        Requires: Signature

        Returns:
            Success response
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.trade.cancel_all_open_orders(http, symbol=symbol)

    async def futures_get_open_orders(
        self,
        symbol: str | None = None,
    ) -> list[FuturesOrder]:
        """Get all open USDT-M futures orders.

        Weight: 1-40 depending on symbol
        Requires: Signature

        Returns:
            List of open FuturesOrder objects
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.trade.get_open_orders(http, symbol=symbol)

    async def futures_get_all_orders(
        self,
        symbol: str,
        order_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 500,
    ) -> list[FuturesOrder]:
        """Get all USDT-M futures orders (active, canceled, filled).

        Weight: 5
        Requires: Signature

        Returns:
            List of FuturesOrder objects
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.trade.get_all_orders(
            http,
            symbol=symbol,
            order_id=order_id,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    async def futures_create_batch_orders(
        self,
        orders: list[dict[str, Any]],
    ) -> list[FuturesOrder | BatchOrderError]:
        """Place multiple USDT-M futures orders in a single request.

        Weight: 5
        Requires: Signature

        Note: Each order in the response can be either a FuturesOrder (success)
        or a BatchOrderError (failure). Check for 'code' attribute to detect errors.

        Args:
            orders: List of order dicts (max 5). Each dict should contain:
                - symbol: Trading pair (required)
                - side: BUY or SELL (required)
                - type: Order type (required)
                - quantity: Order quantity (required for most types)
                - price: Limit price (required for LIMIT orders)
                - positionSide: LONG, SHORT, or BOTH (optional)
                - timeInForce: GTC, IOC, FOK (optional)

        Returns:
            List of FuturesOrder or BatchOrderError for each order

        Example:
            orders = [
                {"symbol": "BTCUSDT", "side": "BUY", "type": "LIMIT",
                 "quantity": "0.001", "price": "30000", "timeInForce": "GTC"},
            ]
            results = await client.futures_create_batch_orders(orders)
            for result in results:
                if hasattr(result, 'code'):  # BatchOrderError
                    print(f"Failed: {result.msg}")
                else:
                    print(f"Order {result.order_id} placed")
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.trade.create_batch_orders(http, orders=orders)

    # ============ USDT-M Futures Account Endpoints (Signed) ============

    async def futures_get_account(self) -> FuturesAccount:
        """Get USDT-M futures account information.

        Weight: 5
        Requires: Signature

        Returns:
            FuturesAccount with balances and positions
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.account.get_account(http)

    async def futures_get_balance(self) -> list[FuturesBalance]:
        """Get USDT-M futures account balance.

        Weight: 5
        Requires: Signature

        Returns:
            List of FuturesBalance objects
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.account.get_balance(http)

    async def futures_get_position_risk(
        self,
        symbol: str | None = None,
    ) -> list[PositionRisk]:
        """Get USDT-M futures position information.

        Weight: 5
        Requires: Signature

        Args:
            symbol: Trading pair (optional, returns all if not specified)

        Returns:
            List of PositionRisk objects
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.account.get_position_risk(http, symbol=symbol)

    async def futures_set_leverage(
        self,
        symbol: str,
        leverage: int,
    ) -> LeverageResult:
        """Change USDT-M futures leverage.

        Weight: 1
        Requires: Signature

        Args:
            symbol: Trading pair
            leverage: Target leverage (1-125)

        Returns:
            LeverageResult with new leverage and max notional
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.account.set_leverage(http, symbol=symbol, leverage=leverage)

    async def futures_set_margin_type(
        self,
        symbol: str,
        margin_type: str,
    ) -> dict[str, Any]:
        """Change USDT-M futures margin type.

        Weight: 1
        Requires: Signature

        Args:
            symbol: Trading pair
            margin_type: ISOLATED or CROSSED

        Returns:
            Success response
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.account.set_margin_type(http, symbol=symbol, margin_type=margin_type)

    async def futures_get_my_trades(
        self,
        symbol: str,
        order_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        from_id: int | None = None,
        limit: int = 500,
    ) -> list[FuturesMyTrade]:
        """Get USDT-M futures trades for account.

        Weight: 5
        Requires: Signature

        Returns:
            List of FuturesMyTrade objects
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.account.get_my_trades(
            http,
            symbol=symbol,
            order_id=order_id,
            start_time=start_time,
            end_time=end_time,
            from_id=from_id,
            limit=limit,
        )
```

**Step 3: Run tests**

Run: `pytest tests/unit/test_client.py -v`
Expected: PASS

**Step 4: Commit**

```bash
git add binance/client.py tests/unit/test_client.py
git commit -m "feat: bind USDT-M futures trade and account endpoints"
```

---

## Task 13: Add COIN-M Futures Methods (Complete)

**Files:**
- Modify: `binance/client.py`
- Modify: `tests/unit/test_client_futures.py`

**Step 1: Write tests for COIN-M futures methods**

```python
# Add to tests/unit/test_client_futures.py

def test_async_client_has_futures_cm_methods():
    """Test that client has COIN-M futures methods."""
    from binance.client import AsyncClient

    client = AsyncClient()
    # General
    assert hasattr(client, "futures_coin_ping")
    assert hasattr(client, "futures_coin_get_server_time")
    assert hasattr(client, "futures_coin_get_exchange_info")
    # Market
    assert hasattr(client, "futures_coin_get_klines")
    assert hasattr(client, "futures_coin_get_order_book")
    assert hasattr(client, "futures_coin_get_mark_price")
    assert hasattr(client, "futures_coin_get_funding_rate")
    assert hasattr(client, "futures_coin_get_ticker_24h")
    assert hasattr(client, "futures_coin_get_ticker_price")
    # Trade
    assert hasattr(client, "futures_coin_create_order")
    assert hasattr(client, "futures_coin_cancel_order")
    assert hasattr(client, "futures_coin_get_order")
    assert hasattr(client, "futures_coin_get_open_orders")
    assert hasattr(client, "futures_coin_create_batch_orders")
    # Account
    assert hasattr(client, "futures_coin_get_account")
    assert hasattr(client, "futures_coin_get_balance")
    assert hasattr(client, "futures_coin_get_position_risk")
    assert hasattr(client, "futures_coin_set_leverage")
```

**Step 2: Add COIN-M methods (complete implementation)**

All COIN-M methods use `await self._ensure_futures_cm_connected()` for lazy connection.

```python
# Add to binance/client.py

class AsyncClient:
    # ... existing code ...

    # ============ COIN-M Futures General Endpoints ============

    async def futures_coin_ping(self) -> dict[str, Any]:
        """Test connectivity to COIN-M Futures API.

        Weight: 1
        """
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.general.ping(http)

    async def futures_coin_get_server_time(self) -> ServerTime:
        """Get COIN-M Futures server time.

        Weight: 1
        """
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.general.get_server_time(http)

    async def futures_coin_get_exchange_info(self) -> FuturesExchangeInfo:
        """Get COIN-M Futures exchange trading rules.

        Weight: 1
        """
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.general.get_exchange_info(http)

    # ============ COIN-M Futures Market Data Endpoints ============

    async def futures_coin_get_order_book(
        self,
        symbol: str,
        limit: int = 500,
    ) -> OrderBook:
        """Get COIN-M futures order book depth."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.market.get_order_book(http, symbol=symbol, limit=limit)

    async def futures_coin_get_trades(
        self,
        symbol: str,
        limit: int = 500,
    ) -> list[Trade]:
        """Get COIN-M futures recent trades."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.market.get_trades(http, symbol=symbol, limit=limit)

    async def futures_coin_get_klines(
        self,
        symbol: str,
        interval: str,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 500,
    ) -> list[FuturesKline]:
        """Get COIN-M futures kline/candlestick bars."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.market.get_klines(
            http,
            symbol=symbol,
            interval=interval,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    @overload
    async def futures_coin_get_mark_price(self, symbol: str) -> MarkPrice: ...
    @overload
    async def futures_coin_get_mark_price(self, symbol: None = None) -> list[MarkPrice]: ...

    async def futures_coin_get_mark_price(
        self,
        symbol: str | None = None,
    ) -> MarkPrice | list[MarkPrice]:
        """Get COIN-M futures mark price and funding rate."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.market.get_mark_price(http, symbol=symbol)

    async def futures_coin_get_funding_rate(
        self,
        symbol: str,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 100,
    ) -> list[FundingRate]:
        """Get COIN-M futures funding rate history."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.market.get_funding_rate(
            http,
            symbol=symbol,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    @overload
    async def futures_coin_get_ticker_24h(self, symbol: str) -> FuturesTicker24h: ...
    @overload
    async def futures_coin_get_ticker_24h(self, symbol: None = None) -> list[FuturesTicker24h]: ...

    async def futures_coin_get_ticker_24h(
        self,
        symbol: str | None = None,
    ) -> FuturesTicker24h | list[FuturesTicker24h]:
        """Get COIN-M futures 24hr ticker."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.market.get_ticker_24h(http, symbol=symbol)

    @overload
    async def futures_coin_get_ticker_price(self, symbol: str) -> TickerPrice: ...
    @overload
    async def futures_coin_get_ticker_price(self, symbol: None = None) -> list[TickerPrice]: ...

    async def futures_coin_get_ticker_price(
        self,
        symbol: str | None = None,
    ) -> TickerPrice | list[TickerPrice]:
        """Get COIN-M futures symbol price ticker."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.market.get_ticker_price(http, symbol=symbol)

    # ============ COIN-M Futures Trade Endpoints (Signed) ============

    async def futures_coin_create_order(
        self,
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
        working_type: str | None = None,
        price_protect: bool | None = None,
        new_order_resp_type: str | None = None,
    ) -> FuturesOrder:
        """Create a new COIN-M futures order.

        Weight: 1
        Requires: Signature
        """
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.trade.create_order(
            http,
            symbol=symbol,
            side=side,
            type=type,
            quantity=quantity,
            price=price,
            time_in_force=time_in_force,
            reduce_only=reduce_only,
            new_client_order_id=new_client_order_id,
            stop_price=stop_price,
            position_side=position_side,
            close_position=close_position,
            working_type=working_type,
            price_protect=price_protect,
            new_order_resp_type=new_order_resp_type,
        )

    async def futures_coin_get_order(
        self,
        symbol: str,
        order_id: int | None = None,
        orig_client_order_id: str | None = None,
    ) -> FuturesOrder:
        """Query COIN-M futures order status."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.trade.get_order(
            http,
            symbol=symbol,
            order_id=order_id,
            orig_client_order_id=orig_client_order_id,
        )

    async def futures_coin_cancel_order(
        self,
        symbol: str,
        order_id: int | None = None,
        orig_client_order_id: str | None = None,
    ) -> FuturesOrder:
        """Cancel an active COIN-M futures order."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.trade.cancel_order(
            http,
            symbol=symbol,
            order_id=order_id,
            orig_client_order_id=orig_client_order_id,
        )

    async def futures_coin_cancel_all_open_orders(
        self,
        symbol: str,
    ) -> dict[str, Any]:
        """Cancel all open COIN-M futures orders on a symbol."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.trade.cancel_all_open_orders(http, symbol=symbol)

    async def futures_coin_get_open_orders(
        self,
        symbol: str | None = None,
    ) -> list[FuturesOrder]:
        """Get all open COIN-M futures orders."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.trade.get_open_orders(http, symbol=symbol)

    async def futures_coin_get_all_orders(
        self,
        symbol: str,
        order_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 500,
    ) -> list[FuturesOrder]:
        """Get all COIN-M futures orders (active, canceled, filled)."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.trade.get_all_orders(
            http,
            symbol=symbol,
            order_id=order_id,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    async def futures_coin_create_batch_orders(
        self,
        orders: list[dict[str, Any]],
    ) -> list[FuturesOrder | BatchOrderError]:
        """Place multiple COIN-M futures orders in a single request.

        Weight: 5
        Requires: Signature

        Args:
            orders: List of order dicts (max 5)

        Returns:
            List of FuturesOrder or BatchOrderError for each order
        """
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.trade.create_batch_orders(http, orders=orders)

    # ============ COIN-M Futures Account Endpoints (Signed) ============

    async def futures_coin_get_account(self) -> FuturesAccount:
        """Get COIN-M futures account information."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.account.get_account(http)

    async def futures_coin_get_balance(self) -> list[FuturesBalance]:
        """Get COIN-M futures account balance."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.account.get_balance(http)

    async def futures_coin_get_position_risk(
        self,
        symbol: str | None = None,
    ) -> list[PositionRisk]:
        """Get COIN-M futures position information."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.account.get_position_risk(http, symbol=symbol)

    async def futures_coin_set_leverage(
        self,
        symbol: str,
        leverage: int,
    ) -> LeverageResult:
        """Change COIN-M futures leverage."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.account.set_leverage(http, symbol=symbol, leverage=leverage)

    async def futures_coin_set_margin_type(
        self,
        symbol: str,
        margin_type: str,
    ) -> dict[str, Any]:
        """Change COIN-M futures margin type."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.account.set_margin_type(http, symbol=symbol, margin_type=margin_type)

    async def futures_coin_get_my_trades(
        self,
        symbol: str,
        order_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        from_id: int | None = None,
        limit: int = 500,
    ) -> list[FuturesMyTrade]:
        """Get COIN-M futures trades for account."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.account.get_my_trades(
            http,
            symbol=symbol,
            order_id=order_id,
            start_time=start_time,
            end_time=end_time,
            from_id=from_id,
            limit=limit,
        )
```

**Step 3: Run tests**

Run: `pytest tests/unit/test_client_futures.py -v`
Expected: PASS

**Step 4: Run mypy**

Run: `mypy binance/client.py --strict`
Expected: Success (or known msgspec-related warnings)

**Step 5: Commit**

```bash
git add binance/client.py tests/unit/test_client_futures.py
git commit -m "feat: add COIN-M futures methods to AsyncClient"
```

---

## Task 14: Add Mock-Based Unit Tests for Futures Methods

**Files:**
- Create: `tests/unit/test_futures_client_mocked.py`

```python
# tests/unit/test_futures_client_mocked.py
"""Unit tests for AsyncClient futures methods with mocked HTTP."""
from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from binance.client import AsyncClient
from binance._schemas.futures import (
    FuturesKline, FuturesOrder, PositionRisk, MarkPrice,
)


@pytest.fixture
def mock_client():
    """Create AsyncClient with mocked HTTP clients."""
    client = AsyncClient(api_key="test", api_secret="test")
    client._http_futures_um = MagicMock()
    client._http_futures_um.request = AsyncMock()
    client._http_futures_um.request_raw = AsyncMock()
    return client


class TestFuturesUMMarket:
    """Test USDT-M futures market endpoints with mocks."""

    @pytest.mark.asyncio
    async def test_futures_get_mark_price_single(self, mock_client):
        """Test single symbol returns MarkPrice."""
        with patch('binance.api.futures_um.market.get_mark_price', new_callable=AsyncMock) as mock:
            mock.return_value = MarkPrice(
                symbol="BTCUSDT",
                mark_price="50000",
                index_price="49995",
                last_funding_rate="0.0001",
                next_funding_time=1700000000000,
                time=1699999999999,
            )
            result = await mock_client.futures_get_mark_price(symbol="BTCUSDT")
            assert isinstance(result, MarkPrice)
            assert result.symbol == "BTCUSDT"


class TestFuturesUMTrade:
    """Test USDT-M futures trade endpoints with mocks."""

    @pytest.mark.asyncio
    async def test_futures_create_order_returns_typed(self, mock_client):
        """Test create_order returns FuturesOrder."""
        with patch('binance.api.futures_um.trade.create_order', new_callable=AsyncMock) as mock:
            mock.return_value = FuturesOrder(
                symbol="BTCUSDT",
                order_id=12345678,
                client_order_id="test",
                price="50000",
                orig_qty="0.001",
                executed_qty="0",
                status="NEW",
                time_in_force="GTC",
                type="LIMIT",
                side="BUY",
            )
            result = await mock_client.futures_create_order(
                symbol="BTCUSDT",
                side="BUY",
                type="LIMIT",
                quantity="0.001",
                price="50000",
                time_in_force="GTC",
            )
            assert isinstance(result, FuturesOrder)
            assert result.order_id == 12345678


class TestFuturesUMAccount:
    """Test USDT-M futures account endpoints with mocks."""

    @pytest.mark.asyncio
    async def test_futures_get_position_risk(self, mock_client):
        """Test get_position_risk returns list of PositionRisk."""
        with patch('binance.api.futures_um.account.get_position_risk', new_callable=AsyncMock) as mock:
            mock.return_value = [
                PositionRisk(
                    symbol="BTCUSDT",
                    position_amt="0.001",
                    entry_price="50000",
                    mark_price="50500",
                    un_realized_profit="0.50",
                    liquidation_price="40000",
                    leverage="20",
                    margin_type="cross",
                    position_side="BOTH",
                )
            ]
            result = await mock_client.futures_get_position_risk()
            assert isinstance(result, list)
            assert len(result) == 1
            assert result[0].symbol == "BTCUSDT"
```

**Step 2: Run mocked tests**

Run: `pytest tests/unit/test_futures_client_mocked.py -v`
Expected: PASS

**Step 3: Commit**

```bash
git add tests/unit/test_futures_client_mocked.py
git commit -m "test: add mock-based unit tests for futures client methods"
```

---

## Next Steps

Continue with [04-integration-testing.md](./04-integration-testing.md) to test against Binance futures testnet.
