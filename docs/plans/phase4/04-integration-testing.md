# Phase 4.4: Futures Integration Testing on Binance Testnet

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Verify AsyncClient futures methods work with real Binance Futures API on testnet, including error scenarios.

**Prerequisites:** Tasks 1-11 complete (AsyncClient with all futures methods)

---

## Futures Testnet Setup

Before running integration tests, you need:

1. **Futures Testnet API Keys:** Get from https://testnet.binancefuture.com/
2. **Environment Variables:**
   ```bash
   export BINANCE_FUTURES_TESTNET_API_KEY="your_futures_testnet_api_key"
   export BINANCE_FUTURES_TESTNET_API_SECRET="your_futures_testnet_api_secret"
   ```

**Note:** The futures testnet uses the same URL for both USDT-M and COIN-M: `https://testnet.binancefuture.com`

---

## Task 12: Create Futures Test Fixtures

**Files:**
- Modify: `tests/integration/conftest.py`

**Step 1: Add futures test fixtures**

```python
# tests/integration/conftest.py (add to existing)
"""Shared fixtures for integration tests."""
import os

import pytest
import pytest_asyncio

from binance import AsyncClient


def get_futures_testnet_credentials() -> tuple[str, str]:
    """Get futures testnet API credentials from environment."""
    api_key = os.environ.get("BINANCE_FUTURES_TESTNET_API_KEY", "")
    api_secret = os.environ.get("BINANCE_FUTURES_TESTNET_API_SECRET", "")
    return api_key, api_secret


@pytest.fixture
def has_futures_testnet_credentials() -> bool:
    """Check if futures testnet credentials are available."""
    api_key, api_secret = get_futures_testnet_credentials()
    return bool(api_key and api_secret)


@pytest_asyncio.fixture
async def futures_public_client():
    """Create a client for public futures endpoints (no auth needed)."""
    async with AsyncClient(testnet=True) as client:
        yield client


@pytest_asyncio.fixture
async def futures_authenticated_client(has_futures_testnet_credentials):
    """Create an authenticated client for signed futures endpoints."""
    if not has_futures_testnet_credentials:
        pytest.skip("Futures testnet credentials not available")

    api_key, api_secret = get_futures_testnet_credentials()
    async with AsyncClient(
        api_key=api_key,
        api_secret=api_secret,
        testnet=True,
    ) as client:
        yield client
```

**Step 2: Commit**

```bash
git add tests/integration/conftest.py
git commit -m "test: add futures testnet fixtures"
```

---

## Task 13: Public Futures Endpoint Integration Tests

**Files:**
- Create: `tests/integration/test_futures_public.py`

**Step 1: Write public endpoint tests**

```python
# tests/integration/test_futures_public.py
"""Integration tests for public Futures API endpoints.

All tests verify typed schema returns.
"""
import pytest

from binance._schemas.spot import ServerTime, OrderBook, TickerPrice, BookTicker
from binance._schemas.futures import (
    FuturesExchangeInfo,
    FuturesKline,
    MarkPrice,
    FundingRate,
    FuturesTicker24h,
)


@pytest.mark.asyncio
class TestFuturesUMGeneralEndpoints:
    """Test USDT-M futures general public endpoints."""

    async def test_futures_ping(self, futures_public_client):
        """Test ping endpoint returns successfully."""
        result = await futures_public_client.futures_ping()
        assert result == {}

    async def test_futures_get_server_time(self, futures_public_client):
        """Test server time returns typed ServerTime."""
        result = await futures_public_client.futures_get_server_time()

        assert isinstance(result, ServerTime)
        assert result.server_time > 0

    async def test_futures_get_exchange_info(self, futures_public_client):
        """Test exchange info returns typed FuturesExchangeInfo."""
        result = await futures_public_client.futures_get_exchange_info()

        assert isinstance(result, FuturesExchangeInfo)
        assert result.timezone == "UTC"
        assert result.server_time > 0
        assert len(result.symbols) > 0

    async def test_futures_exchange_info_has_perpetual(self, futures_public_client):
        """Test exchange info includes perpetual contracts."""
        result = await futures_public_client.futures_get_exchange_info()

        perpetual_symbols = [s for s in result.symbols if s.contract_type == "PERPETUAL"]
        assert len(perpetual_symbols) > 0

        # BTCUSDT should be a perpetual
        btc = next((s for s in perpetual_symbols if s.symbol == "BTCUSDT"), None)
        assert btc is not None
        assert btc.base_asset == "BTC"
        assert btc.quote_asset == "USDT"


@pytest.mark.asyncio
class TestFuturesUMMarketDataEndpoints:
    """Test USDT-M futures market data endpoints."""

    async def test_futures_get_order_book(self, futures_public_client):
        """Test order book returns typed OrderBook."""
        result = await futures_public_client.futures_get_order_book(
            symbol="BTCUSDT", limit=5
        )

        assert isinstance(result, OrderBook)
        assert result.last_update_id > 0
        assert len(result.bids) <= 5
        assert len(result.asks) <= 5

    async def test_futures_get_klines(self, futures_public_client):
        """Test klines returns list of typed FuturesKline."""
        result = await futures_public_client.futures_get_klines(
            symbol="BTCUSDT",
            interval="1h",
            limit=5,
        )

        assert isinstance(result, list)
        assert len(result) <= 5

        if result:
            kline = result[0]
            assert isinstance(kline, FuturesKline)
            assert kline.open_time > 0
            assert kline.open  # non-empty string
            assert kline.close_time > kline.open_time

    async def test_futures_get_continuous_klines(self, futures_public_client):
        """Test continuous klines returns list of FuturesKline."""
        result = await futures_public_client.futures_get_continuous_klines(
            pair="BTCUSDT",
            contract_type="PERPETUAL",
            interval="1h",
            limit=5,
        )

        assert isinstance(result, list)
        if result:
            assert isinstance(result[0], FuturesKline)

    async def test_futures_get_mark_price_single(self, futures_public_client):
        """Test mark price single symbol returns MarkPrice."""
        result = await futures_public_client.futures_get_mark_price(symbol="BTCUSDT")

        assert isinstance(result, MarkPrice)
        assert result.symbol == "BTCUSDT"
        assert result.mark_price
        assert result.index_price
        assert result.last_funding_rate

    async def test_futures_get_mark_price_all(self, futures_public_client):
        """Test mark price all symbols returns list[MarkPrice]."""
        result = await futures_public_client.futures_get_mark_price()

        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(m, MarkPrice) for m in result)

    async def test_futures_get_funding_rate(self, futures_public_client):
        """Test funding rate history returns list of FundingRate."""
        result = await futures_public_client.futures_get_funding_rate(
            symbol="BTCUSDT",
            limit=5,
        )

        assert isinstance(result, list)
        if result:
            rate = result[0]
            assert isinstance(rate, FundingRate)
            assert rate.symbol == "BTCUSDT"
            assert rate.funding_rate
            assert rate.funding_time > 0

    async def test_futures_get_ticker_24h_single(self, futures_public_client):
        """Test 24hr ticker single returns FuturesTicker24h."""
        result = await futures_public_client.futures_get_ticker_24h(symbol="BTCUSDT")

        assert isinstance(result, FuturesTicker24h)
        assert result.symbol == "BTCUSDT"
        assert result.price_change
        assert result.volume

    async def test_futures_get_ticker_24h_all(self, futures_public_client):
        """Test 24hr ticker all returns list."""
        result = await futures_public_client.futures_get_ticker_24h()

        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(t, FuturesTicker24h) for t in result)

    async def test_futures_get_ticker_price_single(self, futures_public_client):
        """Test price ticker single returns TickerPrice."""
        result = await futures_public_client.futures_get_ticker_price(symbol="BTCUSDT")

        assert isinstance(result, TickerPrice)
        assert result.symbol == "BTCUSDT"
        assert result.price

    async def test_futures_get_ticker_price_all(self, futures_public_client):
        """Test price ticker all returns list."""
        result = await futures_public_client.futures_get_ticker_price()

        assert isinstance(result, list)
        assert len(result) > 0

    async def test_futures_get_book_ticker_single(self, futures_public_client):
        """Test book ticker single returns BookTicker."""
        result = await futures_public_client.futures_get_book_ticker(symbol="BTCUSDT")

        assert isinstance(result, BookTicker)
        assert result.symbol == "BTCUSDT"
        assert result.bid_price
        assert result.ask_price


@pytest.mark.asyncio
class TestFuturesCMPublicEndpoints:
    """Test COIN-M futures public endpoints."""

    async def test_futures_coin_ping(self, futures_public_client):
        """Test COIN-M ping endpoint."""
        result = await futures_public_client.futures_coin_ping()
        assert result == {}

    async def test_futures_coin_get_exchange_info(self, futures_public_client):
        """Test COIN-M exchange info."""
        result = await futures_public_client.futures_coin_get_exchange_info()

        assert isinstance(result, FuturesExchangeInfo)
        assert len(result.symbols) > 0

    async def test_futures_coin_get_klines(self, futures_public_client):
        """Test COIN-M klines."""
        result = await futures_public_client.futures_coin_get_klines(
            symbol="BTCUSD_PERP",
            interval="1h",
            limit=5,
        )

        assert isinstance(result, list)
        if result:
            assert isinstance(result[0], FuturesKline)
```

**Step 2: Run public endpoint tests**

Run: `pytest tests/integration/test_futures_public.py -v`
Expected: PASS

**Step 3: Commit**

```bash
git add tests/integration/test_futures_public.py
git commit -m "test: add public futures endpoint integration tests"
```

---

## Task 14: Authenticated Futures Endpoint Integration Tests

**Files:**
- Create: `tests/integration/test_futures_account.py`

**Step 1: Write authenticated endpoint tests**

```python
# tests/integration/test_futures_account.py
"""Integration tests for authenticated Futures API endpoints."""
import pytest

from binance._schemas.futures import (
    FuturesAccount,
    FuturesBalance,
    PositionRisk,
    FuturesOrder,
    LeverageResult,
    FuturesMyTrade,
)


@pytest.mark.asyncio
class TestFuturesUMAccountEndpoints:
    """Test USDT-M futures authenticated account endpoints."""

    async def test_futures_get_account(self, futures_authenticated_client):
        """Test account info returns typed FuturesAccount."""
        result = await futures_authenticated_client.futures_get_account()

        assert isinstance(result, FuturesAccount)
        assert result.total_wallet_balance is not None
        assert result.available_balance is not None
        assert isinstance(result.assets, list)
        assert isinstance(result.positions, list)

    async def test_futures_get_balance(self, futures_authenticated_client):
        """Test balance returns list of FuturesBalance."""
        result = await futures_authenticated_client.futures_get_balance()

        assert isinstance(result, list)
        if result:
            balance = result[0]
            assert isinstance(balance, FuturesBalance)
            assert balance.asset
            assert balance.balance is not None

    async def test_futures_get_position_risk(self, futures_authenticated_client):
        """Test position risk returns list of PositionRisk."""
        result = await futures_authenticated_client.futures_get_position_risk()

        assert isinstance(result, list)
        if result:
            position = result[0]
            assert isinstance(position, PositionRisk)
            assert position.symbol
            assert position.leverage

    async def test_futures_get_position_risk_single_symbol(
        self, futures_authenticated_client
    ):
        """Test position risk for single symbol."""
        result = await futures_authenticated_client.futures_get_position_risk(
            symbol="BTCUSDT"
        )

        assert isinstance(result, list)
        # Should return positions for BTCUSDT only
        for position in result:
            assert position.symbol == "BTCUSDT"

    async def test_futures_get_open_orders(self, futures_authenticated_client):
        """Test open orders returns list of FuturesOrder."""
        result = await futures_authenticated_client.futures_get_open_orders(
            symbol="BTCUSDT"
        )

        assert isinstance(result, list)
        # May be empty if no open orders
        if result:
            assert isinstance(result[0], FuturesOrder)

    async def test_futures_get_my_trades(self, futures_authenticated_client):
        """Test my trades returns list of FuturesMyTrade."""
        result = await futures_authenticated_client.futures_get_my_trades(
            symbol="BTCUSDT"
        )

        assert isinstance(result, list)
        # May be empty if no trades
        if result:
            assert isinstance(result[0], FuturesMyTrade)
```

**Step 2: Run authenticated tests**

Run: `pytest tests/integration/test_futures_account.py -v`
Expected: PASS (if credentials configured) or SKIP

**Step 3: Commit**

```bash
git add tests/integration/test_futures_account.py
git commit -m "test: add authenticated futures account integration tests"
```

---

## Task 15: Futures Trading Integration Tests

**Files:**
- Create: `tests/integration/test_futures_trading.py`

**Step 1: Write trading tests**

```python
# tests/integration/test_futures_trading.py
"""Integration tests for futures trading endpoints.

CAUTION: These tests create real orders on futures testnet.
"""
import pytest

from binance._schemas.futures import FuturesOrder, LeverageResult


@pytest.mark.asyncio
class TestFuturesUMTradingEndpoints:
    """Test USDT-M futures trading endpoints."""

    async def test_futures_create_test_order(self, futures_authenticated_client):
        """Test creating a test order (no actual execution)."""
        result = await futures_authenticated_client.futures_create_test_order(
            symbol="BTCUSDT",
            side="BUY",
            type="LIMIT",
            quantity="0.001",
            price="20000.00",
            time_in_force="GTC",
        )

        # Test order returns empty dict on success
        assert result == {}

    async def test_futures_set_leverage(self, futures_authenticated_client):
        """Test setting leverage."""
        result = await futures_authenticated_client.futures_set_leverage(
            symbol="BTCUSDT",
            leverage=10,
        )

        assert isinstance(result, LeverageResult)
        assert result.leverage == 10
        assert result.symbol == "BTCUSDT"
        assert result.max_notional_value

    async def test_futures_create_and_cancel_limit_order(
        self, futures_authenticated_client
    ):
        """Test creating and canceling a limit order."""
        # Create a low limit buy order (won't fill)
        order = await futures_authenticated_client.futures_create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="LIMIT",
            quantity="0.001",
            price="20000.00",  # Low price, won't fill
            time_in_force="GTC",
        )

        # Verify typed return
        assert isinstance(order, FuturesOrder)
        assert order.order_id > 0
        assert order.symbol == "BTCUSDT"
        assert order.side == "BUY"
        assert order.status == "NEW"

        order_id = order.order_id

        # Query the order
        query = await futures_authenticated_client.futures_get_order(
            symbol="BTCUSDT",
            order_id=order_id,
        )

        assert isinstance(query, FuturesOrder)
        assert query.order_id == order_id
        assert query.status == "NEW"

        # Cancel the order
        cancel = await futures_authenticated_client.futures_cancel_order(
            symbol="BTCUSDT",
            order_id=order_id,
        )

        assert isinstance(cancel, FuturesOrder)
        assert cancel.order_id == order_id
        assert cancel.status == "CANCELED"

    async def test_futures_create_market_order(self, futures_authenticated_client):
        """Test creating a market order.

        Note: This will actually execute on futures testnet.
        Make sure your testnet account has USDT balance.
        """
        # Set leverage first to a safe level
        await futures_authenticated_client.futures_set_leverage(
            symbol="BTCUSDT",
            leverage=1,
        )

        # Small market buy order
        order = await futures_authenticated_client.futures_create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="MARKET",
            quantity="0.001",
        )

        assert isinstance(order, FuturesOrder)
        assert order.symbol == "BTCUSDT"
        assert order.side == "BUY"
        assert order.type == "MARKET"
        # Market orders should fill immediately
        assert order.status in ("FILLED", "PARTIALLY_FILLED", "NEW")

        # Close position if opened
        if order.status == "FILLED":
            await futures_authenticated_client.futures_create_order(
                symbol="BTCUSDT",
                side="SELL",
                type="MARKET",
                quantity="0.001",
            )

    async def test_futures_cancel_all_open_orders(self, futures_authenticated_client):
        """Test canceling all open orders."""
        # First create a limit order
        await futures_authenticated_client.futures_create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="LIMIT",
            quantity="0.001",
            price="20000.00",
            time_in_force="GTC",
        )

        # Cancel all
        result = await futures_authenticated_client.futures_cancel_all_open_orders(
            symbol="BTCUSDT"
        )

        # Should return success response
        assert "code" in result or result == {} or "msg" in result


@pytest.mark.asyncio
class TestFuturesUMOrderQueryEndpoints:
    """Test futures order query endpoints."""

    async def test_futures_get_order_by_client_id(self, futures_authenticated_client):
        """Test querying order by client order ID."""
        import uuid

        client_order_id = f"test_{uuid.uuid4().hex[:8]}"

        # Create order with custom client ID
        order = await futures_authenticated_client.futures_create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="LIMIT",
            quantity="0.001",
            price="20000.00",
            time_in_force="GTC",
            new_client_order_id=client_order_id,
        )

        # Query by client order ID
        query = await futures_authenticated_client.futures_get_order(
            symbol="BTCUSDT",
            orig_client_order_id=client_order_id,
        )

        assert isinstance(query, FuturesOrder)
        assert query.client_order_id == client_order_id

        # Cleanup
        await futures_authenticated_client.futures_cancel_order(
            symbol="BTCUSDT",
            orig_client_order_id=client_order_id,
        )

    async def test_futures_get_all_orders(self, futures_authenticated_client):
        """Test getting all orders (active, canceled, filled)."""
        result = await futures_authenticated_client.futures_get_all_orders(
            symbol="BTCUSDT",
            limit=10,
        )

        assert isinstance(result, list)
        if result:
            assert isinstance(result[0], FuturesOrder)
```

**Step 2: Run trading tests (carefully!)**

Run: `pytest tests/integration/test_futures_trading.py -v`
Expected: PASS

**Step 3: Commit**

```bash
git add tests/integration/test_futures_trading.py
git commit -m "test: add futures trading integration tests"
```

---

## Task 16: Error Scenario Tests

**Files:**
- Create: `tests/integration/test_futures_errors.py`

**Step 1: Write error scenario tests**

```python
# tests/integration/test_futures_errors.py
"""Integration tests for Futures API error scenarios."""
import pytest

from binance._core.exceptions import (
    BinanceAPIError,
    InvalidSymbolError,
    InvalidParameterError,
)


@pytest.mark.asyncio
class TestFuturesInvalidSymbolErrors:
    """Test error handling for invalid symbols."""

    async def test_invalid_symbol_raises_error(self, futures_public_client):
        """Test that invalid symbol raises InvalidSymbolError."""
        with pytest.raises((InvalidSymbolError, BinanceAPIError)) as exc_info:
            await futures_public_client.futures_get_order_book(
                symbol="INVALID_SYMBOL"
            )

        # Should get error code -1121 (INVALID_SYMBOL)
        if hasattr(exc_info.value, 'code'):
            assert exc_info.value.code == -1121

    async def test_invalid_symbol_klines(self, futures_public_client):
        """Test invalid symbol in klines endpoint."""
        with pytest.raises((InvalidSymbolError, BinanceAPIError)):
            await futures_public_client.futures_get_klines(
                symbol="NOTREAL", interval="1h"
            )


@pytest.mark.asyncio
class TestFuturesInvalidParameterErrors:
    """Test error handling for invalid parameters."""

    async def test_invalid_interval(self, futures_public_client):
        """Test invalid interval parameter."""
        with pytest.raises((InvalidParameterError, BinanceAPIError)):
            await futures_public_client.futures_get_klines(
                symbol="BTCUSDT", interval="invalid"
            )

    async def test_invalid_leverage(self, futures_authenticated_client):
        """Test invalid leverage value."""
        with pytest.raises(BinanceAPIError):
            await futures_authenticated_client.futures_set_leverage(
                symbol="BTCUSDT",
                leverage=1000,  # Too high
            )


@pytest.mark.asyncio
class TestFuturesAuthenticationErrors:
    """Test error handling for authentication issues."""

    async def test_signed_endpoint_without_auth(self):
        """Test calling signed endpoint without credentials."""
        from binance import AsyncClient

        async with AsyncClient(testnet=True) as client:
            with pytest.raises(BinanceAPIError) as exc_info:
                await client.futures_get_account()

            # Should get authentication error
            assert exc_info.value.code in (-2014, -2015, -1022)


@pytest.mark.asyncio
class TestFuturesOrderErrors:
    """Test error handling for order-related errors."""

    async def test_insufficient_margin(self, futures_authenticated_client):
        """Test order with insufficient margin."""
        with pytest.raises(BinanceAPIError) as exc_info:
            await futures_authenticated_client.futures_create_order(
                symbol="BTCUSDT",
                side="BUY",
                type="MARKET",
                quantity="10000",  # Very large quantity
            )

        # Error code -2019: Margin is insufficient
        # or -4003: Quantity greater than max qty
        assert exc_info.value.code in (-2019, -4003, -1111)

    async def test_cancel_nonexistent_order(self, futures_authenticated_client):
        """Test canceling order that doesn't exist."""
        with pytest.raises(BinanceAPIError) as exc_info:
            await futures_authenticated_client.futures_cancel_order(
                symbol="BTCUSDT",
                order_id=999999999999,
            )

        # Error code -2011: Unknown order
        assert exc_info.value.code == -2011

    async def test_query_nonexistent_order(self, futures_authenticated_client):
        """Test querying order that doesn't exist."""
        with pytest.raises(BinanceAPIError) as exc_info:
            await futures_authenticated_client.futures_get_order(
                symbol="BTCUSDT",
                order_id=999999999999,
            )

        # Error code -2013: Order does not exist
        assert exc_info.value.code == -2013
```

**Step 2: Run error scenario tests**

Run: `pytest tests/integration/test_futures_errors.py -v`
Expected: PASS

**Step 3: Commit**

```bash
git add tests/integration/test_futures_errors.py
git commit -m "test: add futures error scenario integration tests"
```

---

## Task 17: Concurrent Futures Request Tests

**Files:**
- Create: `tests/integration/test_futures_concurrent.py`

**Step 1: Write concurrent request tests**

```python
# tests/integration/test_futures_concurrent.py
"""Integration tests for concurrent futures API requests."""
import asyncio

import pytest

from binance._schemas.spot import ServerTime, TickerPrice
from binance._schemas.futures import MarkPrice, FuturesKline


@pytest.mark.asyncio
class TestConcurrentFuturesRequests:
    """Test concurrent futures request handling."""

    async def test_concurrent_mark_price_requests(self, futures_public_client):
        """Test fetching multiple mark prices concurrently."""
        symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]

        tasks = [
            futures_public_client.futures_get_mark_price(symbol=s)
            for s in symbols
        ]
        results = await asyncio.gather(*tasks)

        assert len(results) == len(symbols)
        for i, result in enumerate(results):
            assert isinstance(result, MarkPrice)
            assert result.symbol == symbols[i]

    async def test_concurrent_klines_requests(self, futures_public_client):
        """Test fetching multiple klines concurrently."""
        requests = [
            ("BTCUSDT", "1h"),
            ("ETHUSDT", "1h"),
            ("BNBUSDT", "4h"),
        ]

        tasks = [
            futures_public_client.futures_get_klines(symbol=sym, interval=interval, limit=10)
            for sym, interval in requests
        ]
        results = await asyncio.gather(*tasks)

        assert len(results) == len(requests)
        for result in results:
            assert isinstance(result, list)
            if result:
                assert isinstance(result[0], FuturesKline)

    async def test_concurrent_mixed_futures_endpoints(self, futures_public_client):
        """Test concurrent requests to different futures endpoints."""
        tasks = [
            futures_public_client.futures_get_server_time(),
            futures_public_client.futures_get_ticker_price(symbol="BTCUSDT"),
            futures_public_client.futures_get_mark_price(symbol="BTCUSDT"),
            futures_public_client.futures_get_order_book(symbol="BTCUSDT", limit=5),
        ]

        results = await asyncio.gather(*tasks)

        assert len(results) == 4
        assert isinstance(results[0], ServerTime)
        assert isinstance(results[1], TickerPrice)
        assert isinstance(results[2], MarkPrice)

    async def test_concurrent_spot_and_futures(self, futures_public_client):
        """Test concurrent requests to both spot and futures APIs."""
        tasks = [
            # Spot
            futures_public_client.get_server_time(),
            futures_public_client.get_ticker_price(symbol="BTCUSDT"),
            # Futures
            futures_public_client.futures_get_server_time(),
            futures_public_client.futures_get_ticker_price(symbol="BTCUSDT"),
        ]

        results = await asyncio.gather(*tasks)

        assert len(results) == 4
        # All should succeed
        assert all(r is not None for r in results)

    async def test_high_concurrency_futures(self, futures_public_client):
        """Test high number of concurrent futures requests."""
        tasks = [
            futures_public_client.futures_ping()
            for _ in range(20)
        ]

        results = await asyncio.gather(*tasks)

        assert len(results) == 20
        assert all(r == {} for r in results)
```

**Step 2: Run concurrent tests**

Run: `pytest tests/integration/test_futures_concurrent.py -v`
Expected: PASS

**Step 3: Commit**

```bash
git add tests/integration/test_futures_concurrent.py
git commit -m "test: add concurrent futures request tests"
```

---

## Task 18: Final Verification

**Step 1: Run all unit tests**

Run: `pytest tests/unit/ -v`
Expected: All tests PASS

**Step 2: Run all integration tests**

Run: `pytest tests/integration/ -v`
Expected: All tests PASS

**Step 3: Run type checking**

Run: `mypy binance/ --strict`
Expected: Success (or known msgspec-related warnings)

**Step 4: Run linting**

Run: `ruff check binance/`
Expected: No errors

**Step 5: Run full test suite**

Run: `pytest tests/ -v --tb=short`
Expected: All tests PASS

**Step 6: Final commit**

```bash
git add .
git commit -m "feat: complete Phase 4 - Futures API implementation"
```

---

## Phase 4 Complete Checklist

### Endpoint Modules
- [ ] `api/futures_um/` modules created (general, market, trade, account)
- [ ] `api/futures_cm/` modules created (general, market, trade, account)
- [ ] All endpoints return typed schemas
- [ ] Pre-compiled decoders used

### Schemas
- [ ] `_schemas/futures.py` created
- [ ] All futures-specific schemas defined
- [ ] FuturesKline.from_raw() converter works

### AsyncClient
- [ ] Futures HTTP clients added (_http_futures_um, _http_futures_cm)
- [ ] USDT-M methods added (futures_*)
- [ ] COIN-M methods added (futures_coin_*)
- [ ] @overload for variant return types

### Unit Tests (Offline)
- [ ] Schema parsing tests pass
- [ ] Mock-based endpoint tests pass
- [ ] Mock-based client tests pass

### Integration Tests (Testnet)
- [ ] Public endpoint tests pass
- [ ] Authenticated endpoint tests pass
- [ ] Trading tests pass
- [ ] Error scenario tests pass
- [ ] Concurrent request tests pass

### Quality
- [ ] mypy passes
- [ ] ruff passes
- [ ] Test coverage > 80%

---

## Test Coverage Summary

| Test Category | File | Tests | Network |
|---------------|------|-------|---------|
| Futures schemas | `tests/unit/schemas/test_futures_schemas.py` | 15+ | No |
| Futures UM endpoints | `tests/unit/api/test_futures_um_*.py` | 20+ | No |
| Client mocks | `tests/unit/test_futures_client_mocked.py` | 10+ | No |
| Public endpoints | `tests/integration/test_futures_public.py` | 20+ | Yes |
| Account endpoints | `tests/integration/test_futures_account.py` | 8+ | Yes |
| Trading endpoints | `tests/integration/test_futures_trading.py` | 8+ | Yes |
| Error scenarios | `tests/integration/test_futures_errors.py` | 8+ | Yes |
| Concurrent requests | `tests/integration/test_futures_concurrent.py` | 5+ | Yes |

**Total: 100+ new tests** for futures API

---

## Next Phase

Phase 5: Testing & Polish - Documentation, benchmarks, and final cleanup.
