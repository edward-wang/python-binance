# Phase 4.3: Extend AsyncClient with Futures Methods

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Extend `binance/client.py` with USDT-M and COIN-M futures methods that return typed schemas.

**Prerequisites:** Tasks 1-7 complete (api/futures_um/, api/futures_cm/, _schemas/futures.py exist)

---

## Task 8: Add Futures HTTPClient Support

**Files:**
- Modify: `binance/_core/http.py` (if needed)
- Modify: `binance/client.py`
- Modify: `tests/unit/test_client.py`

**Step 1: Write the failing test**

```python
# Add to tests/unit/test_client.py

def test_async_client_has_futures_http():
    """Test that client has futures HTTP clients."""
    from binance.client import AsyncClient

    client = AsyncClient(testnet=True)
    assert hasattr(client, "_http_futures_um")
    assert hasattr(client, "_http_futures_cm")


def test_async_client_futures_testnet_urls():
    """Test futures clients use correct testnet URLs."""
    from binance.client import AsyncClient
    from binance._core.config import FUTURES_UM_TESTNET_URL, FUTURES_CM_TESTNET_URL

    client = AsyncClient(testnet=True)
    # The HTTP clients should be configured with testnet URLs
    # (Implementation detail - may need to check _base_url attribute)
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/test_client.py::test_async_client_has_futures_http -v`
Expected: FAIL

**Step 3: Update AsyncClient to support multiple base URLs**

```python
# Modify binance/client.py

from binance._core.config import (
    BASE_URL,
    TESTNET_URL,
    FUTURES_UM_BASE_URL,
    FUTURES_UM_TESTNET_URL,
    FUTURES_CM_BASE_URL,
    FUTURES_CM_TESTNET_URL,
)
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
)


class AsyncClient:
    """Async client for Binance API.

    Supports Spot, USDT-M Futures, and COIN-M Futures APIs.
    All methods return typed msgspec schemas.
    """

    __slots__ = ("_http", "_http_futures_um", "_http_futures_cm")

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
        # Spot API
        spot_url = base_url or (TESTNET_URL if testnet else BASE_URL)
        self._http = HTTPClient(
            api_key=api_key,
            api_secret=api_secret,
            base_url=spot_url,
            timeout=timeout,
        )

        # USDT-M Futures API
        futures_um_url = FUTURES_UM_TESTNET_URL if testnet else FUTURES_UM_BASE_URL
        self._http_futures_um = HTTPClient(
            api_key=api_key,
            api_secret=api_secret,
            base_url=futures_um_url,
            timeout=timeout,
        )

        # COIN-M Futures API
        futures_cm_url = FUTURES_CM_TESTNET_URL if testnet else FUTURES_CM_BASE_URL
        self._http_futures_cm = HTTPClient(
            api_key=api_key,
            api_secret=api_secret,
            base_url=futures_cm_url,
            timeout=timeout,
        )

    async def __aenter__(self) -> "AsyncClient":
        """Async context manager entry."""
        await self._http.connect()
        await self._http_futures_um.connect()
        await self._http_futures_cm.connect()
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit."""
        await self._http.close()
        await self._http_futures_um.close()
        await self._http_futures_cm.close()

    async def connect(self) -> None:
        """Initialize all connection pools."""
        await self._http.connect()
        await self._http_futures_um.connect()
        await self._http_futures_cm.connect()

    async def close(self) -> None:
        """Close all connection pools."""
        await self._http.close()
        await self._http_futures_um.close()
        await self._http_futures_cm.close()
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

## Task 9: Bind USDT-M Futures General and Market Endpoints

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
        return await futures_um.general.ping(self._http_futures_um)

    async def futures_get_server_time(self) -> ServerTime:
        """Get USDT-M Futures server time.

        Weight: 1

        Returns:
            ServerTime with server_time in milliseconds
        """
        return await futures_um.general.get_server_time(self._http_futures_um)

    async def futures_get_exchange_info(self) -> FuturesExchangeInfo:
        """Get USDT-M Futures exchange trading rules.

        Weight: 1

        Returns:
            FuturesExchangeInfo with symbols and rate limits
        """
        return await futures_um.general.get_exchange_info(self._http_futures_um)

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
        return await futures_um.market.get_order_book(
            self._http_futures_um, symbol=symbol, limit=limit
        )

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
        return await futures_um.market.get_trades(
            self._http_futures_um, symbol=symbol, limit=limit
        )

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
        return await futures_um.market.get_agg_trades(
            self._http_futures_um,
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
        return await futures_um.market.get_klines(
            self._http_futures_um,
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
        return await futures_um.market.get_continuous_klines(
            self._http_futures_um,
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
        return await futures_um.market.get_mark_price(
            self._http_futures_um, symbol=symbol
        )

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
        return await futures_um.market.get_funding_rate(
            self._http_futures_um,
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
        return await futures_um.market.get_ticker_24h(
            self._http_futures_um, symbol=symbol
        )

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
        return await futures_um.market.get_ticker_price(
            self._http_futures_um, symbol=symbol
        )

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
        return await futures_um.market.get_book_ticker(
            self._http_futures_um, symbol=symbol
        )
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

## Task 10: Bind USDT-M Futures Trade and Account Endpoints

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
        return await futures_um.trade.create_order(
            self._http_futures_um,
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
        return await futures_um.trade.create_test_order(
            self._http_futures_um,
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
        return await futures_um.trade.get_order(
            self._http_futures_um,
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
        return await futures_um.trade.cancel_order(
            self._http_futures_um,
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
        return await futures_um.trade.cancel_all_open_orders(
            self._http_futures_um, symbol=symbol
        )

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
        return await futures_um.trade.get_open_orders(
            self._http_futures_um, symbol=symbol
        )

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
        return await futures_um.trade.get_all_orders(
            self._http_futures_um,
            symbol=symbol,
            order_id=order_id,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    # ============ USDT-M Futures Account Endpoints (Signed) ============

    async def futures_get_account(self) -> FuturesAccount:
        """Get USDT-M futures account information.

        Weight: 5
        Requires: Signature

        Returns:
            FuturesAccount with balances and positions
        """
        return await futures_um.account.get_account(self._http_futures_um)

    async def futures_get_balance(self) -> list[FuturesBalance]:
        """Get USDT-M futures account balance.

        Weight: 5
        Requires: Signature

        Returns:
            List of FuturesBalance objects
        """
        return await futures_um.account.get_balance(self._http_futures_um)

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
        return await futures_um.account.get_position_risk(
            self._http_futures_um, symbol=symbol
        )

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
        return await futures_um.account.set_leverage(
            self._http_futures_um, symbol=symbol, leverage=leverage
        )

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
        return await futures_um.account.set_margin_type(
            self._http_futures_um, symbol=symbol, margin_type=margin_type
        )

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
        return await futures_um.account.get_my_trades(
            self._http_futures_um,
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

## Task 11: Add COIN-M Futures Methods (Similar to USDT-M)

**Files:**
- Modify: `binance/client.py`
- Modify: `tests/unit/test_client.py`

**Step 1: Write tests for COIN-M futures methods**

```python
# Add to tests/unit/test_client.py

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
    assert hasattr(client, "futures_coin_get_mark_price")
    # Trade
    assert hasattr(client, "futures_coin_create_order")
    assert hasattr(client, "futures_coin_cancel_order")
    # Account
    assert hasattr(client, "futures_coin_get_account")
    assert hasattr(client, "futures_coin_get_position_risk")
```

**Step 2: Add COIN-M methods (prefix: futures_coin_)**

Add COIN-M methods following the same pattern as USDT-M, but using:
- `self._http_futures_cm` instead of `self._http_futures_um`
- `futures_cm` module instead of `futures_um`
- Method prefix `futures_coin_` instead of `futures_`

```python
# Add to binance/client.py

class AsyncClient:
    # ... existing code ...

    # ============ COIN-M Futures General Endpoints ============

    async def futures_coin_ping(self) -> dict[str, Any]:
        """Test connectivity to COIN-M Futures API."""
        return await futures_cm.general.ping(self._http_futures_cm)

    async def futures_coin_get_server_time(self) -> ServerTime:
        """Get COIN-M Futures server time."""
        return await futures_cm.general.get_server_time(self._http_futures_cm)

    async def futures_coin_get_exchange_info(self) -> FuturesExchangeInfo:
        """Get COIN-M Futures exchange trading rules."""
        return await futures_cm.general.get_exchange_info(self._http_futures_cm)

    # ============ COIN-M Futures Market Data Endpoints ============

    async def futures_coin_get_klines(
        self,
        symbol: str,
        interval: str,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 500,
    ) -> list[FuturesKline]:
        """Get COIN-M futures kline/candlestick bars."""
        return await futures_cm.market.get_klines(
            self._http_futures_cm,
            symbol=symbol,
            interval=interval,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    # ... Add remaining COIN-M methods following the USDT-M pattern ...

    # ============ COIN-M Futures Trade Endpoints ============

    async def futures_coin_create_order(
        self,
        symbol: str,
        side: str,
        type: str,
        quantity: str | None = None,
        price: str | None = None,
        # ... same parameters as USDT-M
    ) -> FuturesOrder:
        """Create a new COIN-M futures order."""
        return await futures_cm.trade.create_order(
            self._http_futures_cm,
            symbol=symbol,
            side=side,
            type=type,
            # ...
        )

    # ============ COIN-M Futures Account Endpoints ============

    async def futures_coin_get_account(self) -> FuturesAccount:
        """Get COIN-M futures account information."""
        return await futures_cm.account.get_account(self._http_futures_cm)

    async def futures_coin_get_position_risk(
        self,
        symbol: str | None = None,
    ) -> list[PositionRisk]:
        """Get COIN-M futures position information."""
        return await futures_cm.account.get_position_risk(
            self._http_futures_cm, symbol=symbol
        )

    async def futures_coin_set_leverage(
        self,
        symbol: str,
        leverage: int,
    ) -> LeverageResult:
        """Change COIN-M futures leverage."""
        return await futures_cm.account.set_leverage(
            self._http_futures_cm, symbol=symbol, leverage=leverage
        )
```

**Step 3: Run tests**

Run: `pytest tests/unit/test_client.py -v`
Expected: PASS

**Step 4: Run mypy**

Run: `mypy binance/client.py --strict`
Expected: Success (or known msgspec-related warnings)

**Step 5: Commit**

```bash
git add binance/client.py tests/unit/test_client.py
git commit -m "feat: add COIN-M futures methods to AsyncClient"
```

---

## Task 11.1: Add Mock-Based Unit Tests for Futures Methods

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
