# Phase 3.4: Integration Testing on Binance Testnet

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Verify the AsyncClient works with real Binance API calls on testnet.

**Prerequisites:** Tasks 1-9 complete (AsyncClient fully implemented)

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

## Task 10: Public Endpoint Integration Tests

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

**Step 2: Write public endpoint tests**

```python
# tests/integration/test_spot_public.py
"""Integration tests for public Spot API endpoints."""
import pytest


@pytest.mark.asyncio
class TestGeneralEndpoints:
    """Test general public endpoints."""

    async def test_ping(self, public_client):
        """Test ping endpoint returns successfully."""
        result = await public_client.ping()
        assert result == {}

    async def test_get_server_time(self, public_client):
        """Test server time endpoint returns valid timestamp."""
        result = await public_client.get_server_time()

        assert "serverTime" in result
        assert isinstance(result["serverTime"], int)
        assert result["serverTime"] > 0

    async def test_get_exchange_info(self, public_client):
        """Test exchange info endpoint returns valid data."""
        result = await public_client.get_exchange_info()

        assert "timezone" in result
        assert "serverTime" in result
        assert "symbols" in result
        assert len(result["symbols"]) > 0

    async def test_get_exchange_info_single_symbol(self, public_client):
        """Test exchange info for single symbol."""
        result = await public_client.get_exchange_info(symbol="BTCUSDT")

        assert "symbols" in result
        assert len(result["symbols"]) == 1
        assert result["symbols"][0]["symbol"] == "BTCUSDT"


@pytest.mark.asyncio
class TestMarketDataEndpoints:
    """Test market data public endpoints."""

    async def test_get_order_book(self, public_client):
        """Test order book returns bids and asks."""
        result = await public_client.get_order_book(symbol="BTCUSDT", limit=5)

        assert "lastUpdateId" in result
        assert "bids" in result
        assert "asks" in result
        assert len(result["bids"]) <= 5
        assert len(result["asks"]) <= 5

    async def test_get_order_book_structure(self, public_client):
        """Test order book data structure."""
        result = await public_client.get_order_book(symbol="BTCUSDT", limit=1)

        if result["bids"]:
            bid = result["bids"][0]
            assert len(bid) == 2  # [price, quantity]
            assert isinstance(bid[0], str)  # price as string
            assert isinstance(bid[1], str)  # quantity as string

    async def test_get_trades(self, public_client):
        """Test recent trades returns list."""
        result = await public_client.get_trades(symbol="BTCUSDT", limit=5)

        assert isinstance(result, list)
        assert len(result) <= 5

        if result:
            trade = result[0]
            assert "id" in trade
            assert "price" in trade
            assert "qty" in trade
            assert "time" in trade

    async def test_get_klines(self, public_client):
        """Test klines returns candlestick data."""
        result = await public_client.get_klines(
            symbol="BTCUSDT",
            interval="1h",
            limit=5,
        )

        assert isinstance(result, list)
        assert len(result) <= 5

        if result:
            kline = result[0]
            assert len(kline) >= 11  # Standard kline has 12 elements
            # [open_time, open, high, low, close, volume, close_time, ...]
            assert isinstance(kline[0], int)  # open_time
            assert isinstance(kline[1], str)  # open price

    async def test_get_avg_price(self, public_client):
        """Test average price returns valid data."""
        result = await public_client.get_avg_price(symbol="BTCUSDT")

        assert "mins" in result
        assert "price" in result
        assert isinstance(result["price"], str)

    async def test_get_ticker_price(self, public_client):
        """Test price ticker returns valid data."""
        result = await public_client.get_ticker_price(symbol="BTCUSDT")

        assert "symbol" in result
        assert result["symbol"] == "BTCUSDT"
        assert "price" in result
        assert isinstance(result["price"], str)

    async def test_get_ticker_price_all(self, public_client):
        """Test price ticker for all symbols."""
        result = await public_client.get_ticker_price()

        assert isinstance(result, list)
        assert len(result) > 0

    async def test_get_ticker_24h(self, public_client):
        """Test 24hr ticker returns valid data."""
        result = await public_client.get_ticker_24h(symbol="BTCUSDT")

        assert "symbol" in result
        assert "priceChange" in result
        assert "priceChangePercent" in result
        assert "volume" in result

    async def test_get_book_ticker(self, public_client):
        """Test book ticker returns best bid/ask."""
        result = await public_client.get_book_ticker(symbol="BTCUSDT")

        assert "symbol" in result
        assert "bidPrice" in result
        assert "bidQty" in result
        assert "askPrice" in result
        assert "askQty" in result
```

**Step 3: Run public endpoint tests**

Run: `pytest tests/integration/test_spot_public.py -v`
Expected: PASS (all tests should pass with testnet)

**Step 4: Commit**

```bash
git add tests/integration/
git commit -m "test: add public endpoint integration tests"
```

---

## Task 11: Authenticated Endpoint Integration Tests

**Files:**
- Create: `tests/integration/test_spot_account.py`

**Step 1: Write authenticated endpoint tests**

```python
# tests/integration/test_spot_account.py
"""Integration tests for authenticated Spot API endpoints."""
import pytest


@pytest.mark.asyncio
class TestAccountEndpoints:
    """Test authenticated account endpoints."""

    async def test_get_account(self, authenticated_client):
        """Test account info returns valid data."""
        result = await authenticated_client.get_account()

        assert "makerCommission" in result
        assert "takerCommission" in result
        assert "canTrade" in result
        assert "balances" in result
        assert isinstance(result["balances"], list)

    async def test_get_account_has_balances(self, authenticated_client):
        """Test account has balance structure."""
        result = await authenticated_client.get_account()

        balances = result["balances"]
        assert len(balances) > 0

        # Check balance structure
        balance = balances[0]
        assert "asset" in balance
        assert "free" in balance
        assert "locked" in balance

    async def test_get_my_trades_empty(self, authenticated_client):
        """Test my trades returns list (may be empty on testnet)."""
        result = await authenticated_client.get_my_trades(symbol="BTCUSDT")

        assert isinstance(result, list)
        # May be empty if no trades on testnet

    async def test_get_open_orders(self, authenticated_client):
        """Test open orders returns list."""
        result = await authenticated_client.get_open_orders(symbol="BTCUSDT")

        assert isinstance(result, list)
        # May be empty if no open orders

    async def test_get_open_orders_all(self, authenticated_client):
        """Test open orders for all symbols."""
        result = await authenticated_client.get_open_orders()

        assert isinstance(result, list)

    async def test_get_order_rate_limit(self, authenticated_client):
        """Test order rate limit returns usage info."""
        result = await authenticated_client.get_order_rate_limit()

        assert isinstance(result, list)
        if result:
            limit = result[0]
            assert "rateLimitType" in limit
            assert "interval" in limit
            assert "limit" in limit
```

**Step 2: Run authenticated tests**

Run: `pytest tests/integration/test_spot_account.py -v`
Expected: PASS (if testnet credentials configured) or SKIP (if not)

**Step 3: Commit**

```bash
git add tests/integration/test_spot_account.py
git commit -m "test: add authenticated endpoint integration tests"
```

---

## Task 12: Trading Integration Tests

**Files:**
- Create: `tests/integration/test_spot_trading.py`

**Step 1: Write trading tests**

```python
# tests/integration/test_spot_trading.py
"""Integration tests for trading endpoints.

CAUTION: These tests create real orders on testnet.
"""
import pytest


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

        assert "orderId" in order
        assert "symbol" in order
        assert order["symbol"] == "BTCUSDT"
        assert order["side"] == "BUY"
        assert order["status"] == "NEW"

        order_id = order["orderId"]

        # Query the order
        query = await authenticated_client.get_order(
            symbol="BTCUSDT",
            order_id=order_id,
        )

        assert query["orderId"] == order_id
        assert query["status"] == "NEW"

        # Cancel the order
        cancel = await authenticated_client.cancel_order(
            symbol="BTCUSDT",
            order_id=order_id,
        )

        assert cancel["orderId"] == order_id
        assert cancel["status"] == "CANCELED"

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

        assert "orderId" in order
        assert order["symbol"] == "BTCUSDT"
        assert order["side"] == "BUY"
        assert order["type"] == "MARKET"
        # Market orders should fill immediately
        assert order["status"] in ("FILLED", "PARTIALLY_FILLED")

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
            assert cancelled["status"] == "CANCELED"


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

        assert query["clientOrderId"] == client_order_id

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
git commit -m "test: add trading integration tests for testnet"
```

---

## Task 12.1: Final Verification

**Step 1: Run all integration tests**

Run: `pytest tests/integration/ -v`
Expected: All tests PASS

**Step 2: Run full test suite**

Run: `pytest tests/ -v`
Expected: All tests PASS

**Step 3: Run type checking**

Run: `mypy binance/ --strict`
Expected: Success

**Step 4: Run linting**

Run: `ruff check binance/`
Expected: No errors

**Step 5: Final commit**

```bash
git add .
git commit -m "feat: complete Phase 3 - Spot API implementation"
```

---

## Phase 3 Complete Checklist

- [ ] Generator produces valid api/spot/ modules
- [ ] Generator produces valid _schemas/spot.py
- [ ] AsyncClient binds all 20 core endpoints
- [ ] Package exports AsyncClient correctly
- [ ] Public endpoint tests pass
- [ ] Authenticated endpoint tests pass
- [ ] Trading tests pass on testnet
- [ ] mypy type checking passes
- [ ] ruff linting passes

---

## Next Phase

Phase 4: Futures API - Similar process for USDT-M and COIN-M futures.
