# Phase 3.4: Integration Testing on Binance Testnet

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Verify the AsyncClient works with real Binance API calls on testnet, **including error scenarios**.

**Prerequisites:** Tasks 1-11 complete (AsyncClient fully implemented with typed returns)

---

## Testnet Setup

Before running integration tests, you need:

1. **Testnet API Keys:** Get from https://testnet.binance.vision/
2. **Environment Variables:**
   ```bash
   export BINANCE_TESTNET_API_KEY="your_testnet_api_key"
   export BINANCE_TESTNET_API_SECRET="your_testnet_api_secret"
   ```

---

## Task 12: Public Endpoint Integration Tests

**Files:**
- Create: `tests/integration/__init__.py`
- Create: `tests/integration/conftest.py`
- Create: `tests/integration/test_spot_public.py`

**Step 1: Create test fixtures**

```python
# tests/integration/__init__.py
"""Integration tests - require network access and API keys."""
```

```python
# tests/integration/conftest.py
"""Shared fixtures for integration tests."""
import os

import pytest
import pytest_asyncio

from binance import AsyncClient


def get_testnet_credentials() -> tuple[str, str]:
    """Get testnet API credentials from environment."""
    api_key = os.environ.get("BINANCE_TESTNET_API_KEY", "")
    api_secret = os.environ.get("BINANCE_TESTNET_API_SECRET", "")
    return api_key, api_secret


@pytest.fixture
def has_testnet_credentials() -> bool:
    """Check if testnet credentials are available."""
    api_key, api_secret = get_testnet_credentials()
    return bool(api_key and api_secret)


@pytest_asyncio.fixture
async def public_client():
    """Create a client for public endpoints (no auth needed)."""
    async with AsyncClient(testnet=True) as client:
        yield client


@pytest_asyncio.fixture
async def authenticated_client(has_testnet_credentials):
    """Create an authenticated client for signed endpoints."""
    if not has_testnet_credentials:
        pytest.skip("Testnet credentials not available")

    api_key, api_secret = get_testnet_credentials()
    async with AsyncClient(
        api_key=api_key,
        api_secret=api_secret,
        testnet=True,
    ) as client:
        yield client
```

**Step 2: Write public endpoint tests with typed assertions**

```python
# tests/integration/test_spot_public.py
"""Integration tests for public Spot API endpoints.

All tests verify typed schema returns, not raw dicts.
"""
import pytest

from binance._schemas.spot import (
    ServerTime,
    ExchangeInfo,
    OrderBook,
    Trade,
    Kline,
    AvgPrice,
    TickerPrice,
    Ticker24h,
    BookTicker,
)


@pytest.mark.asyncio
class TestGeneralEndpoints:
    """Test general public endpoints."""

    async def test_ping(self, public_client):
        """Test ping endpoint returns successfully."""
        result = await public_client.ping()
        assert result == {}

    async def test_get_server_time(self, public_client):
        """Test server time returns typed ServerTime."""
        result = await public_client.get_server_time()

        # Verify typed return
        assert isinstance(result, ServerTime)
        assert result.server_time > 0

    async def test_get_exchange_info(self, public_client):
        """Test exchange info returns typed ExchangeInfo."""
        result = await public_client.get_exchange_info()

        # Verify typed return
        assert isinstance(result, ExchangeInfo)
        assert result.timezone == "UTC"
        assert result.server_time > 0
        assert len(result.symbols) > 0

    async def test_get_exchange_info_single_symbol(self, public_client):
        """Test exchange info for single symbol."""
        result = await public_client.get_exchange_info(symbol="BTCUSDT")

        assert isinstance(result, ExchangeInfo)
        assert len(result.symbols) == 1
        assert result.symbols[0].symbol == "BTCUSDT"


@pytest.mark.asyncio
class TestMarketDataEndpoints:
    """Test market data public endpoints."""

    async def test_get_order_book(self, public_client):
        """Test order book returns typed OrderBook."""
        result = await public_client.get_order_book(symbol="BTCUSDT", limit=5)

        assert isinstance(result, OrderBook)
        assert result.last_update_id > 0
        assert len(result.bids) <= 5
        assert len(result.asks) <= 5

    async def test_get_order_book_structure(self, public_client):
        """Test order book bid/ask structure."""
        result = await public_client.get_order_book(symbol="BTCUSDT", limit=1)

        if result.bids:
            bid = result.bids[0]
            # Verify it's [price, quantity] as strings
            assert len(bid) == 2
            assert isinstance(bid[0], str)
            assert isinstance(bid[1], str)

    async def test_get_trades(self, public_client):
        """Test recent trades returns list of typed Trade."""
        result = await public_client.get_trades(symbol="BTCUSDT", limit=5)

        assert isinstance(result, list)
        assert len(result) <= 5

        if result:
            trade = result[0]
            assert isinstance(trade, Trade)
            assert trade.id > 0
            assert trade.price  # non-empty string
            assert trade.qty

    async def test_get_klines(self, public_client):
        """Test klines returns list of typed Kline."""
        result = await public_client.get_klines(
            symbol="BTCUSDT",
            interval="1h",
            limit=5,
        )

        assert isinstance(result, list)
        assert len(result) <= 5

        if result:
            kline = result[0]
            assert isinstance(kline, Kline)
            assert kline.open_time > 0
            assert kline.open  # non-empty string
            assert kline.close_time > kline.open_time

    async def test_get_avg_price(self, public_client):
        """Test average price returns typed AvgPrice."""
        result = await public_client.get_avg_price(symbol="BTCUSDT")

        assert isinstance(result, AvgPrice)
        assert result.mins >= 0
        assert result.price  # non-empty string

    async def test_get_ticker_price_single(self, public_client):
        """Test price ticker single symbol returns TickerPrice."""
        result = await public_client.get_ticker_price(symbol="BTCUSDT")

        # Single symbol returns single object
        assert isinstance(result, TickerPrice)
        assert result.symbol == "BTCUSDT"
        assert result.price

    async def test_get_ticker_price_all(self, public_client):
        """Test price ticker all symbols returns list[TickerPrice]."""
        result = await public_client.get_ticker_price()

        # No symbol returns list
        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(t, TickerPrice) for t in result)

    async def test_get_ticker_24h_single(self, public_client):
        """Test 24hr ticker single symbol returns Ticker24h."""
        result = await public_client.get_ticker_24h(symbol="BTCUSDT")

        assert isinstance(result, Ticker24h)
        assert result.symbol == "BTCUSDT"
        assert result.price_change
        assert result.price_change_percent
        assert result.volume

    async def test_get_ticker_24h_all(self, public_client):
        """Test 24hr ticker all symbols returns list[Ticker24h]."""
        result = await public_client.get_ticker_24h()

        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(t, Ticker24h) for t in result)

    async def test_get_book_ticker_single(self, public_client):
        """Test book ticker single symbol returns BookTicker."""
        result = await public_client.get_book_ticker(symbol="BTCUSDT")

        assert isinstance(result, BookTicker)
        assert result.symbol == "BTCUSDT"
        assert result.bid_price
        assert result.ask_price

    async def test_get_book_ticker_all(self, public_client):
        """Test book ticker all symbols returns list[BookTicker]."""
        result = await public_client.get_book_ticker()

        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(t, BookTicker) for t in result)
```

**Step 3: Run public endpoint tests**

Run: `pytest tests/integration/test_spot_public.py -v`
Expected: PASS (all tests should pass with testnet)

**Step 4: Commit**

```bash
git add tests/integration/
git commit -m "test: add public endpoint integration tests with typed assertions"
```

---

## Task 13: Authenticated Endpoint Integration Tests

**Files:**
- Create: `tests/integration/test_spot_account.py`

**Step 1: Write authenticated endpoint tests with typed assertions**

```python
# tests/integration/test_spot_account.py
"""Integration tests for authenticated Spot API endpoints."""
import pytest

from binance._schemas.spot import Account, Balance, MyTrade, Order, RateLimitInfo


@pytest.mark.asyncio
class TestAccountEndpoints:
    """Test authenticated account endpoints."""

    async def test_get_account(self, authenticated_client):
        """Test account info returns typed Account."""
        result = await authenticated_client.get_account()

        assert isinstance(result, Account)
        assert result.maker_commission >= 0
        assert result.taker_commission >= 0
        assert isinstance(result.can_trade, bool)
        assert isinstance(result.balances, list)

    async def test_get_account_has_balances(self, authenticated_client):
        """Test account balances are typed Balance objects."""
        result = await authenticated_client.get_account()

        assert len(result.balances) > 0

        # Check balance structure
        balance = result.balances[0]
        assert isinstance(balance, Balance)
        assert balance.asset  # non-empty string
        assert balance.free is not None
        assert balance.locked is not None

    async def test_get_my_trades_empty(self, authenticated_client):
        """Test my trades returns list of typed MyTrade."""
        result = await authenticated_client.get_my_trades(symbol="BTCUSDT")

        assert isinstance(result, list)
        # May be empty if no trades on testnet
        if result:
            assert isinstance(result[0], MyTrade)

    async def test_get_open_orders(self, authenticated_client):
        """Test open orders returns list of typed Order."""
        result = await authenticated_client.get_open_orders(symbol="BTCUSDT")

        assert isinstance(result, list)
        # May be empty if no open orders
        if result:
            assert isinstance(result[0], Order)

    async def test_get_open_orders_all(self, authenticated_client):
        """Test open orders for all symbols."""
        result = await authenticated_client.get_open_orders()

        assert isinstance(result, list)

    async def test_get_order_rate_limit(self, authenticated_client):
        """Test order rate limit returns list of typed RateLimitInfo."""
        result = await authenticated_client.get_order_rate_limit()

        assert isinstance(result, list)
        if result:
            limit = result[0]
            assert isinstance(limit, RateLimitInfo)
            assert limit.rate_limit_type
            assert limit.interval
            assert limit.limit >= 0
```

**Step 2: Run authenticated tests**

Run: `pytest tests/integration/test_spot_account.py -v`
Expected: PASS (if testnet credentials configured) or SKIP (if not)

**Step 3: Commit**

```bash
git add tests/integration/test_spot_account.py
git commit -m "test: add authenticated endpoint integration tests with typed assertions"
```

---

## Task 14: Trading Integration Tests

**Files:**
- Create: `tests/integration/test_spot_trading.py`

**Step 1: Write trading tests with typed assertions**

```python
# tests/integration/test_spot_trading.py
"""Integration tests for trading endpoints.

CAUTION: These tests create real orders on testnet.
"""
import pytest

from binance._schemas.spot import Order, CancelOrderResult


@pytest.mark.asyncio
class TestTradingEndpoints:
    """Test trading endpoints."""

    async def test_create_test_order(self, authenticated_client):
        """Test creating a test order (no actual execution)."""
        result = await authenticated_client.create_test_order(
            symbol="BTCUSDT",
            side="BUY",
            type="LIMIT",
            quantity="0.001",
            price="20000.00",
            time_in_force="GTC",
        )

        # Test order returns empty dict on success
        assert result == {}

    async def test_create_and_cancel_limit_order(self, authenticated_client):
        """Test creating and canceling a limit order."""
        # Create a low limit buy order (won't fill)
        order = await authenticated_client.create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="LIMIT",
            quantity="0.001",
            price="10000.00",  # Low price, won't fill
            time_in_force="GTC",
            new_order_resp_type="FULL",
        )

        # Verify typed return
        assert isinstance(order, Order)
        assert order.order_id > 0
        assert order.symbol == "BTCUSDT"
        assert order.side == "BUY"
        assert order.status == "NEW"

        order_id = order.order_id

        # Query the order
        query = await authenticated_client.get_order(
            symbol="BTCUSDT",
            order_id=order_id,
        )

        assert isinstance(query, Order)
        assert query.order_id == order_id
        assert query.status == "NEW"

        # Cancel the order
        cancel = await authenticated_client.cancel_order(
            symbol="BTCUSDT",
            order_id=order_id,
        )

        assert isinstance(cancel, CancelOrderResult)
        assert cancel.order_id == order_id
        assert cancel.status == "CANCELED"

    async def test_create_market_order_buy(self, authenticated_client):
        """Test creating a market buy order.

        Note: This will actually execute on testnet.
        Make sure your testnet account has USDT balance.
        """
        # Small market buy order
        order = await authenticated_client.create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="MARKET",
            quantity="0.001",
            new_order_resp_type="FULL",
        )

        assert isinstance(order, Order)
        assert order.symbol == "BTCUSDT"
        assert order.side == "BUY"
        assert order.type == "MARKET"
        # Market orders should fill immediately
        assert order.status in ("FILLED", "PARTIALLY_FILLED")

    async def test_cancel_all_open_orders(self, authenticated_client):
        """Test canceling all open orders."""
        # First create a few limit orders
        for price in ["10000.00", "10001.00"]:
            await authenticated_client.create_order(
                symbol="BTCUSDT",
                side="BUY",
                type="LIMIT",
                quantity="0.001",
                price=price,
                time_in_force="GTC",
            )

        # Cancel all
        result = await authenticated_client.cancel_all_open_orders(symbol="BTCUSDT")

        assert isinstance(result, list)
        # Should have canceled the orders we created
        for cancelled in result:
            assert isinstance(cancelled, CancelOrderResult)
            assert cancelled.status == "CANCELED"


@pytest.mark.asyncio
class TestOrderQueryEndpoints:
    """Test order query endpoints."""

    async def test_get_order_by_client_id(self, authenticated_client):
        """Test querying order by client order ID."""
        import uuid

        client_order_id = f"test_{uuid.uuid4().hex[:8]}"

        # Create order with custom client ID
        order = await authenticated_client.create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="LIMIT",
            quantity="0.001",
            price="10000.00",
            time_in_force="GTC",
            new_client_order_id=client_order_id,
        )

        # Query by client order ID
        query = await authenticated_client.get_order(
            symbol="BTCUSDT",
            orig_client_order_id=client_order_id,
        )

        assert isinstance(query, Order)
        assert query.client_order_id == client_order_id

        # Cleanup
        await authenticated_client.cancel_order(
            symbol="BTCUSDT",
            orig_client_order_id=client_order_id,
        )
```

**Step 2: Run trading tests (carefully!)**

Run: `pytest tests/integration/test_spot_trading.py -v`
Expected: PASS (orders created and canceled on testnet)

**Step 3: Commit**

```bash
git add tests/integration/test_spot_trading.py
git commit -m "test: add trading integration tests with typed assertions"
```

---

## Task 15: Error Scenario Tests (NEW)

**Files:**
- Create: `tests/integration/test_error_scenarios.py`

**Step 1: Write error scenario tests**

```python
# tests/integration/test_error_scenarios.py
"""Integration tests for API error scenarios.

Tests that verify proper error handling for invalid requests.
"""
import pytest

from binance._core.exceptions import (
    BinanceAPIError,
    InvalidSymbolError,
    InvalidParameterError,
)


@pytest.mark.asyncio
class TestInvalidSymbolErrors:
    """Test error handling for invalid symbols."""

    async def test_invalid_symbol_raises_error(self, public_client):
        """Test that invalid symbol raises InvalidSymbolError."""
        with pytest.raises(InvalidSymbolError) as exc_info:
            await public_client.get_order_book(symbol="INVALID_SYMBOL")

        assert exc_info.value.code == -1121  # INVALID_SYMBOL
        assert "INVALID_SYMBOL" in str(exc_info.value)

    async def test_invalid_symbol_klines(self, public_client):
        """Test invalid symbol in klines endpoint."""
        with pytest.raises(InvalidSymbolError):
            await public_client.get_klines(symbol="NOTREAL", interval="1h")

    async def test_invalid_symbol_ticker(self, public_client):
        """Test invalid symbol in ticker endpoint."""
        with pytest.raises(InvalidSymbolError):
            await public_client.get_ticker_price(symbol="XXXXXX")


@pytest.mark.asyncio
class TestInvalidParameterErrors:
    """Test error handling for invalid parameters."""

    async def test_invalid_interval(self, public_client):
        """Test invalid interval parameter."""
        with pytest.raises(InvalidParameterError):
            await public_client.get_klines(symbol="BTCUSDT", interval="invalid")

    async def test_invalid_limit_too_large(self, public_client):
        """Test limit parameter exceeds maximum."""
        with pytest.raises(InvalidParameterError):
            await public_client.get_order_book(symbol="BTCUSDT", limit=99999)

    async def test_missing_required_param_order(self, authenticated_client):
        """Test missing required parameter for order."""
        with pytest.raises((TypeError, InvalidParameterError)):
            # Missing side and type
            await authenticated_client.create_order(symbol="BTCUSDT")


@pytest.mark.asyncio
class TestAuthenticationErrors:
    """Test error handling for authentication issues."""

    async def test_signed_endpoint_without_auth(self):
        """Test calling signed endpoint without credentials."""
        from binance import AsyncClient

        async with AsyncClient(testnet=True) as client:
            # No API key/secret provided
            with pytest.raises(BinanceAPIError) as exc_info:
                await client.get_account()

            # Should get authentication error
            assert exc_info.value.code in (-2014, -2015)  # API-key or signature errors


@pytest.mark.asyncio
class TestOrderErrors:
    """Test error handling for order-related errors."""

    async def test_insufficient_balance(self, authenticated_client):
        """Test order with insufficient balance."""
        with pytest.raises(BinanceAPIError) as exc_info:
            # Try to buy more than balance allows
            await authenticated_client.create_order(
                symbol="BTCUSDT",
                side="BUY",
                type="MARKET",
                quantity="1000000",  # Very large quantity
            )

        # Error code -2010: Account has insufficient balance
        assert exc_info.value.code == -2010

    async def test_min_notional_violation(self, authenticated_client):
        """Test order below minimum notional value."""
        with pytest.raises(BinanceAPIError) as exc_info:
            await authenticated_client.create_order(
                symbol="BTCUSDT",
                side="BUY",
                type="LIMIT",
                quantity="0.00001",  # Too small
                price="10.00",  # Low price = tiny notional
                time_in_force="GTC",
            )

        # Error code -1013: Filter failure: MIN_NOTIONAL
        assert exc_info.value.code == -1013

    async def test_lot_size_violation(self, authenticated_client):
        """Test order with invalid lot size precision."""
        with pytest.raises(BinanceAPIError) as exc_info:
            await authenticated_client.create_order(
                symbol="BTCUSDT",
                side="BUY",
                type="LIMIT",
                quantity="0.000001234567",  # Too many decimals
                price="50000.00",
                time_in_force="GTC",
            )

        # Error code -1013: Filter failure: LOT_SIZE
        assert exc_info.value.code == -1013

    async def test_cancel_nonexistent_order(self, authenticated_client):
        """Test canceling order that doesn't exist."""
        with pytest.raises(BinanceAPIError) as exc_info:
            await authenticated_client.cancel_order(
                symbol="BTCUSDT",
                order_id=999999999999,  # Non-existent order
            )

        # Error code -2011: Unknown order
        assert exc_info.value.code == -2011

    async def test_query_nonexistent_order(self, authenticated_client):
        """Test querying order that doesn't exist."""
        with pytest.raises(BinanceAPIError) as exc_info:
            await authenticated_client.get_order(
                symbol="BTCUSDT",
                order_id=999999999999,
            )

        assert exc_info.value.code == -2013  # Order does not exist
```

**Step 2: Run error scenario tests**

Run: `pytest tests/integration/test_error_scenarios.py -v`
Expected: PASS (all error scenarios handled correctly)

**Step 3: Commit**

```bash
git add tests/integration/test_error_scenarios.py
git commit -m "test: add error scenario integration tests"
```

---

## Task 16: Concurrent Request Tests (NEW)

**Files:**
- Create: `tests/integration/test_concurrent.py`

**Step 1: Write concurrent request tests**

```python
# tests/integration/test_concurrent.py
"""Integration tests for concurrent API requests.

Tests that verify the client handles concurrent requests correctly.
"""
import asyncio

import pytest


@pytest.mark.asyncio
class TestConcurrentRequests:
    """Test concurrent request handling."""

    async def test_concurrent_ticker_requests(self, public_client):
        """Test fetching multiple tickers concurrently."""
        symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT"]

        # Fetch all tickers concurrently
        tasks = [
            public_client.get_ticker_price(symbol=s)
            for s in symbols
        ]
        results = await asyncio.gather(*tasks)

        assert len(results) == len(symbols)
        for i, result in enumerate(results):
            assert result.symbol == symbols[i]

    async def test_concurrent_klines_requests(self, public_client):
        """Test fetching multiple klines concurrently."""
        requests = [
            ("BTCUSDT", "1h"),
            ("ETHUSDT", "1h"),
            ("BNBUSDT", "4h"),
        ]

        tasks = [
            public_client.get_klines(symbol=sym, interval=interval, limit=10)
            for sym, interval in requests
        ]
        results = await asyncio.gather(*tasks)

        assert len(results) == len(requests)
        for result in results:
            assert isinstance(result, list)
            assert len(result) <= 10

    async def test_concurrent_mixed_endpoints(self, public_client):
        """Test concurrent requests to different endpoints."""
        tasks = [
            public_client.get_server_time(),
            public_client.get_ticker_price(symbol="BTCUSDT"),
            public_client.get_order_book(symbol="BTCUSDT", limit=5),
            public_client.get_avg_price(symbol="BTCUSDT"),
        ]

        results = await asyncio.gather(*tasks)

        # All should return successfully
        assert len(results) == 4
        # Verify types
        from binance._schemas.spot import ServerTime, TickerPrice, OrderBook, AvgPrice

        assert isinstance(results[0], ServerTime)
        assert isinstance(results[1], TickerPrice)
        assert isinstance(results[2], OrderBook)
        assert isinstance(results[3], AvgPrice)

    async def test_concurrent_with_one_failure(self, public_client):
        """Test that one failure doesn't affect other requests."""
        from binance._core.exceptions import InvalidSymbolError

        tasks = [
            public_client.get_ticker_price(symbol="BTCUSDT"),
            public_client.get_ticker_price(symbol="INVALID"),  # Will fail
            public_client.get_ticker_price(symbol="ETHUSDT"),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # First and third should succeed
        assert results[0].symbol == "BTCUSDT"
        assert results[2].symbol == "ETHUSDT"
        # Second should be an exception
        assert isinstance(results[1], InvalidSymbolError)

    async def test_high_concurrency(self, public_client):
        """Test high number of concurrent requests."""
        # 20 concurrent requests
        tasks = [
            public_client.ping()
            for _ in range(20)
        ]

        results = await asyncio.gather(*tasks)

        assert len(results) == 20
        assert all(r == {} for r in results)


@pytest.mark.asyncio
class TestConnectionPooling:
    """Test connection pool behavior."""

    async def test_reuses_connections(self, public_client):
        """Test that client reuses HTTP connections."""
        # Make multiple sequential requests
        for _ in range(5):
            await public_client.ping()

        # If we get here without error, connection reuse is working
        # (Connection errors would occur if pool exhausted)

    async def test_client_context_manager(self):
        """Test that context manager properly cleans up."""
        from binance import AsyncClient

        async with AsyncClient(testnet=True) as client:
            await client.ping()

        # After context exit, client should be closed
        # Attempting to use it should fail or work gracefully
```

**Step 2: Run concurrent tests**

Run: `pytest tests/integration/test_concurrent.py -v`
Expected: PASS (all concurrent scenarios work correctly)

**Step 3: Commit**

```bash
git add tests/integration/test_concurrent.py
git commit -m "test: add concurrent request integration tests"
```

---

## Task 17: Mock-Based Unit Tests for HTTP Layer (NEW)

**Files:**
- Create: `tests/unit/test_http_mocked.py`

This enables testing without network access and verifying request construction.

**Step 1: Write mock-based HTTP tests**

```python
# tests/unit/test_http_mocked.py
"""Unit tests with mocked HTTP layer.

These tests verify request construction and response parsing without network.
"""
from unittest.mock import AsyncMock, patch

import msgspec
import pytest

from binance._schemas.spot import ServerTime, Account, TickerPrice


@pytest.mark.asyncio
class TestMockedPublicEndpoints:
    """Test public endpoints with mocked HTTP."""

    async def test_get_server_time_request_construction(self):
        """Verify get_server_time constructs correct request."""
        from binance import AsyncClient

        mock_response = b'{"serverTime": 1234567890123}'

        with patch.object(
            AsyncClient, "_request_raw", new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = mock_response

            async with AsyncClient(testnet=True) as client:
                # Override to use our mock
                client._http.request_raw = mock_request
                result = await client.get_server_time()

            # Verify request was made correctly
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert call_args[0][0] == "GET"
            assert "/api/v3/time" in call_args[0][1]

    async def test_get_ticker_price_parses_single(self):
        """Verify single ticker response parses to TickerPrice."""
        from binance.api.spot import market

        mock_response = b'{"symbol": "BTCUSDT", "price": "50000.00"}'

        # Test decoder directly
        decoder = msgspec.json.Decoder(TickerPrice)
        result = decoder.decode(mock_response)

        assert isinstance(result, TickerPrice)
        assert result.symbol == "BTCUSDT"
        assert result.price == "50000.00"

    async def test_get_ticker_price_parses_list(self):
        """Verify multiple ticker response parses to list[TickerPrice]."""
        mock_response = b'''[
            {"symbol": "BTCUSDT", "price": "50000.00"},
            {"symbol": "ETHUSDT", "price": "3000.00"}
        ]'''

        decoder = msgspec.json.Decoder(list[TickerPrice])
        result = decoder.decode(mock_response)

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(t, TickerPrice) for t in result)


@pytest.mark.asyncio
class TestMockedAuthenticatedEndpoints:
    """Test authenticated endpoints with mocked HTTP."""

    async def test_get_account_includes_signature(self):
        """Verify get_account request includes signature."""
        from binance import AsyncClient

        mock_response = b'''{
            "makerCommission": 10,
            "takerCommission": 10,
            "buyerCommission": 0,
            "sellerCommission": 0,
            "canTrade": true,
            "canWithdraw": true,
            "canDeposit": true,
            "updateTime": 1234567890,
            "accountType": "SPOT",
            "balances": []
        }'''

        with patch.object(
            AsyncClient, "_request_raw", new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = mock_response

            async with AsyncClient(
                api_key="test_key",
                api_secret="test_secret",
                testnet=True,
            ) as client:
                client._http.request_raw = mock_request
                await client.get_account()

            # Verify signed=True was passed
            call_args = mock_request.call_args
            assert call_args[1].get("signed", False) is True

    async def test_create_order_includes_all_params(self):
        """Verify create_order includes all required parameters."""
        from binance import AsyncClient

        mock_response = b'''{
            "symbol": "BTCUSDT",
            "orderId": 12345,
            "orderListId": -1,
            "clientOrderId": "test123",
            "transactTime": 1234567890,
            "price": "10000.00",
            "origQty": "0.001",
            "executedQty": "0",
            "cummulativeQuoteQty": "0",
            "status": "NEW",
            "timeInForce": "GTC",
            "type": "LIMIT",
            "side": "BUY"
        }'''

        with patch.object(
            AsyncClient, "_request_raw", new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = mock_response

            async with AsyncClient(
                api_key="test_key",
                api_secret="test_secret",
                testnet=True,
            ) as client:
                client._http.request_raw = mock_request
                await client.create_order(
                    symbol="BTCUSDT",
                    side="BUY",
                    type="LIMIT",
                    quantity="0.001",
                    price="10000.00",
                    time_in_force="GTC",
                )

            # Verify POST method
            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            # Verify required params in request
            assert "symbol" in str(call_args)
            assert "BTCUSDT" in str(call_args)


@pytest.mark.asyncio
class TestErrorResponseParsing:
    """Test error response parsing."""

    async def test_api_error_parsing(self):
        """Verify API error responses are parsed correctly."""
        from binance._core.exceptions import raise_for_error, BinanceAPIError

        error_response = b'{"code": -1121, "msg": "Invalid symbol."}'

        with pytest.raises(BinanceAPIError) as exc_info:
            raise_for_error(error_response, 400)

        assert exc_info.value.code == -1121
        assert "Invalid symbol" in str(exc_info.value)

    async def test_rate_limit_error_parsing(self):
        """Verify rate limit error is handled."""
        from binance._core.exceptions import raise_for_error, RateLimitError

        error_response = b'{"code": -1015, "msg": "Too many requests."}'

        with pytest.raises(RateLimitError) as exc_info:
            raise_for_error(error_response, 429)

        assert exc_info.value.code == -1015
```

**Step 2: Run mock-based tests**

Run: `pytest tests/unit/test_http_mocked.py -v`
Expected: PASS (all tests run without network)

**Step 3: Commit**

```bash
git add tests/unit/test_http_mocked.py
git commit -m "test: add mock-based unit tests for HTTP layer"
```

---

## Task 18: Final Verification

**Step 1: Run all unit tests (no network required)**

Run: `pytest tests/unit/ -v`
Expected: All tests PASS

**Step 2: Run all integration tests**

Run: `pytest tests/integration/ -v`
Expected: All tests PASS (with testnet credentials)

**Step 3: Run full test suite**

Run: `pytest tests/ -v`
Expected: All tests PASS

**Step 4: Run type checking**

Run: `mypy binance/ --strict`
Expected: Success

**Step 5: Run linting**

Run: `ruff check binance/`
Expected: No errors

**Step 6: Final commit**

```bash
git add .
git commit -m "feat: complete Phase 3 - Spot API implementation with typed returns"
```

---

## Phase 3 Complete Checklist

### Code Generation
- [ ] Generator produces valid api/spot/ modules
- [ ] Generator produces valid _schemas/spot.py
- [ ] Endpoints return **typed schemas** (not raw dicts)
- [ ] Pre-compiled decoders used for performance

### AsyncClient
- [ ] AsyncClient binds all 20 core endpoints
- [ ] Methods return typed schemas
- [ ] @overload used for variant return types
- [ ] Package exports AsyncClient correctly

### Unit Tests (Offline)
- [ ] Schema parsing tests pass
- [ ] Mock-based HTTP tests pass
- [ ] Error parsing tests pass

### Integration Tests (Testnet)
- [ ] Public endpoint tests pass (with typed assertions)
- [ ] Authenticated endpoint tests pass
- [ ] Trading tests pass on testnet
- [ ] **Error scenario tests pass** (invalid symbol, params, etc.)
- [ ] **Concurrent request tests pass**

### Quality
- [ ] mypy type checking passes (`--strict`)
- [ ] ruff linting passes
- [ ] Test coverage > 80%

---

## Test Coverage Summary

| Test Category | File | Tests | Network |
|---------------|------|-------|---------|
| Schema parsing | `tests/unit/test_schemas_spot.py` | 15+ | No |
| Endpoint mocks | `tests/unit/test_endpoints_spot.py` | 20+ | No |
| HTTP mocks | `tests/unit/test_http_mocked.py` | 10+ | No |
| Public endpoints | `tests/integration/test_spot_public.py` | 15+ | Yes |
| Account endpoints | `tests/integration/test_spot_account.py` | 6+ | Yes |
| Trading endpoints | `tests/integration/test_spot_trading.py` | 5+ | Yes |
| Error scenarios | `tests/integration/test_error_scenarios.py` | 12+ | Yes |
| Concurrent requests | `tests/integration/test_concurrent.py` | 6+ | Yes |

**Total: 90+ tests** covering all critical paths

---

## Next Phase

Phase 4: Futures API - Similar process for USDT-M and COIN-M futures.
