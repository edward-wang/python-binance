# Phase 3.2: Generate Spot API Schemas

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Generate msgspec schemas for Spot API responses in `binance/_schemas/spot.py`.

**Prerequisites:** Task 1-3 complete (api/spot/ modules exist)

---

## Task 4: Run Generator for Schemas

**Files:**
- Run: `python -m generator spot --schemas`
- Check: `binance/_schemas/spot.py`

**Step 1: Run generator for schemas**

Run: `python -m generator spot --schemas`
Expected output:
```
Parsing schemas from specs/openapi/spot...
  ✓ Parsed 45 schema definitions
Generating binance/_schemas/spot.py...
  ✓ binance/_schemas/spot.py (45 schemas)
Done!
```

**Step 2: Verify schema file exists**

Run: `ls -la binance/_schemas/spot.py`
Expected: File exists

**Step 3: Check syntax validity**

Run: `python -c "from binance._schemas.spot import *"`
Expected: No errors

**Step 4: Run mypy**

Run: `mypy binance/_schemas/spot.py --strict`
Expected: Success

**Step 5: Commit generated schemas**

```bash
git add binance/_schemas/spot.py
git commit -m "feat: generate spot API schemas from OpenAPI specs"
```

---

## Task 5: Review and Fix Generated Schemas

**Files:**
- Review: `binance/_schemas/spot.py`
- Modify if needed

**Step 1: Verify BaseStruct import**

Check the file imports correctly:

```python
# binance/_schemas/spot.py
"""Spot API schemas - Generated from OpenAPI specs.

Do not edit manually. Re-generate with: python -m generator spot --schemas
"""
from typing import Annotated

import msgspec

from binance._schemas.common import BaseStruct
```

**Step 2: Verify Order response schema**

Check for proper Order schema:

```python
class Order(BaseStruct):
    """Order response from POST /api/v3/order."""

    symbol: Annotated[str, msgspec.Meta(description="Trading pair")]
    order_id: Annotated[int, msgspec.Meta(description="Order ID")]
    order_list_id: Annotated[int, msgspec.Meta(description="Order list ID, -1 if not part of list")]
    client_order_id: Annotated[str, msgspec.Meta(description="Client order ID")]
    transact_time: Annotated[int, msgspec.Meta(description="Transaction time in ms")]
    price: Annotated[str, msgspec.Meta(description="Order price")]
    orig_qty: Annotated[str, msgspec.Meta(description="Original quantity")]
    executed_qty: Annotated[str, msgspec.Meta(description="Executed quantity")]
    cummulative_quote_qty: Annotated[str, msgspec.Meta(description="Cumulative quote quantity")]
    status: Annotated[str, msgspec.Meta(description="Order status")]
    time_in_force: Annotated[str, msgspec.Meta(description="Time in force")]
    type: Annotated[str, msgspec.Meta(description="Order type")]
    side: Annotated[str, msgspec.Meta(description="Order side")]
```

**Step 3: Verify Account schema**

Check for proper Account schema with nested balances:

```python
class Balance(BaseStruct):
    """Asset balance in account."""

    asset: Annotated[str, msgspec.Meta(description="Asset symbol")]
    free: Annotated[str, msgspec.Meta(description="Available balance")]
    locked: Annotated[str, msgspec.Meta(description="Locked balance")]


class Account(BaseStruct):
    """Account information from GET /api/v3/account."""

    maker_commission: Annotated[int, msgspec.Meta(description="Maker commission rate")]
    taker_commission: Annotated[int, msgspec.Meta(description="Taker commission rate")]
    buyer_commission: Annotated[int, msgspec.Meta(description="Buyer commission rate")]
    seller_commission: Annotated[int, msgspec.Meta(description="Seller commission rate")]
    can_trade: Annotated[bool, msgspec.Meta(description="Can trade")]
    can_withdraw: Annotated[bool, msgspec.Meta(description="Can withdraw")]
    can_deposit: Annotated[bool, msgspec.Meta(description="Can deposit")]
    update_time: Annotated[int, msgspec.Meta(description="Last update time")]
    account_type: Annotated[str, msgspec.Meta(description="Account type")]
    balances: Annotated[list[Balance], msgspec.Meta(description="Asset balances")]
```

**Step 4: Verify ExchangeInfo schema**

Check for proper nested structure:

```python
class RateLimit(BaseStruct):
    """Rate limit rule."""

    rate_limit_type: Annotated[str, msgspec.Meta(description="Rate limit type")]
    interval: Annotated[str, msgspec.Meta(description="Interval")]
    interval_num: Annotated[int, msgspec.Meta(description="Interval number")]
    limit: Annotated[int, msgspec.Meta(description="Limit value")]


class SymbolFilter(BaseStruct):
    """Symbol trading filter."""

    filter_type: Annotated[str, msgspec.Meta(description="Filter type")]
    # Filter-specific fields vary, use optional
    min_price: Annotated[str | None, msgspec.Meta(description="Min price")] = None
    max_price: Annotated[str | None, msgspec.Meta(description="Max price")] = None
    tick_size: Annotated[str | None, msgspec.Meta(description="Tick size")] = None
    min_qty: Annotated[str | None, msgspec.Meta(description="Min quantity")] = None
    max_qty: Annotated[str | None, msgspec.Meta(description="Max quantity")] = None
    step_size: Annotated[str | None, msgspec.Meta(description="Step size")] = None
    # ... more filter fields


class Symbol(BaseStruct):
    """Trading symbol information."""

    symbol: Annotated[str, msgspec.Meta(description="Symbol name")]
    status: Annotated[str, msgspec.Meta(description="Trading status")]
    base_asset: Annotated[str, msgspec.Meta(description="Base asset")]
    base_asset_precision: Annotated[int, msgspec.Meta(description="Base asset precision")]
    quote_asset: Annotated[str, msgspec.Meta(description="Quote asset")]
    quote_precision: Annotated[int, msgspec.Meta(description="Quote precision")]
    order_types: Annotated[list[str], msgspec.Meta(description="Allowed order types")]
    iceberg_allowed: Annotated[bool, msgspec.Meta(description="Iceberg orders allowed")]
    filters: Annotated[list[SymbolFilter], msgspec.Meta(description="Trading filters")]


class ExchangeInfo(BaseStruct):
    """Exchange information from GET /api/v3/exchangeInfo."""

    timezone: Annotated[str, msgspec.Meta(description="Server timezone")]
    server_time: Annotated[int, msgspec.Meta(description="Server time in ms")]
    rate_limits: Annotated[list[RateLimit], msgspec.Meta(description="Rate limit rules")]
    symbols: Annotated[list[Symbol], msgspec.Meta(description="Trading symbols")]
```

**Step 5: Verify Trade schema**

```python
class Trade(BaseStruct):
    """Trade from GET /api/v3/trades."""

    id: Annotated[int, msgspec.Meta(description="Trade ID")]
    price: Annotated[str, msgspec.Meta(description="Trade price")]
    qty: Annotated[str, msgspec.Meta(description="Trade quantity")]
    quote_qty: Annotated[str, msgspec.Meta(description="Quote quantity")]
    time: Annotated[int, msgspec.Meta(description="Trade time")]
    is_buyer_maker: Annotated[bool, msgspec.Meta(description="Was buyer the maker")]
    is_best_match: Annotated[bool, msgspec.Meta(description="Was this the best match")]


class MyTrade(BaseStruct):
    """User trade from GET /api/v3/myTrades."""

    symbol: Annotated[str, msgspec.Meta(description="Trading pair")]
    id: Annotated[int, msgspec.Meta(description="Trade ID")]
    order_id: Annotated[int, msgspec.Meta(description="Order ID")]
    price: Annotated[str, msgspec.Meta(description="Trade price")]
    qty: Annotated[str, msgspec.Meta(description="Trade quantity")]
    quote_qty: Annotated[str, msgspec.Meta(description="Quote quantity")]
    commission: Annotated[str, msgspec.Meta(description="Commission")]
    commission_asset: Annotated[str, msgspec.Meta(description="Commission asset")]
    time: Annotated[int, msgspec.Meta(description="Trade time")]
    is_buyer: Annotated[bool, msgspec.Meta(description="Was buyer")]
    is_maker: Annotated[bool, msgspec.Meta(description="Was maker")]
```

**Step 6: Verify OrderBook schema**

```python
class OrderBook(BaseStruct):
    """Order book from GET /api/v3/depth."""

    last_update_id: Annotated[int, msgspec.Meta(description="Last update ID")]
    bids: Annotated[list[list[str]], msgspec.Meta(description="Bid levels [price, qty]")]
    asks: Annotated[list[list[str]], msgspec.Meta(description="Ask levels [price, qty]")]
```

**Step 7: Verify Ticker schemas**

```python
class TickerPrice(BaseStruct):
    """Price ticker from GET /api/v3/ticker/price."""

    symbol: Annotated[str, msgspec.Meta(description="Trading pair")]
    price: Annotated[str, msgspec.Meta(description="Current price")]


class Ticker24h(BaseStruct):
    """24hr ticker from GET /api/v3/ticker/24hr."""

    symbol: Annotated[str, msgspec.Meta(description="Trading pair")]
    price_change: Annotated[str, msgspec.Meta(description="Price change")]
    price_change_percent: Annotated[str, msgspec.Meta(description="Price change percent")]
    weighted_avg_price: Annotated[str, msgspec.Meta(description="Weighted average price")]
    prev_close_price: Annotated[str, msgspec.Meta(description="Previous close price")]
    last_price: Annotated[str, msgspec.Meta(description="Last price")]
    bid_price: Annotated[str, msgspec.Meta(description="Best bid price")]
    ask_price: Annotated[str, msgspec.Meta(description="Best ask price")]
    open_price: Annotated[str, msgspec.Meta(description="Open price")]
    high_price: Annotated[str, msgspec.Meta(description="High price")]
    low_price: Annotated[str, msgspec.Meta(description="Low price")]
    volume: Annotated[str, msgspec.Meta(description="Base asset volume")]
    quote_volume: Annotated[str, msgspec.Meta(description="Quote asset volume")]
    open_time: Annotated[int, msgspec.Meta(description="Open time")]
    close_time: Annotated[int, msgspec.Meta(description="Close time")]
    first_id: Annotated[int, msgspec.Meta(description="First trade ID")]
    last_id: Annotated[int, msgspec.Meta(description="Last trade ID")]
    count: Annotated[int, msgspec.Meta(description="Number of trades")]


class BookTicker(BaseStruct):
    """Book ticker from GET /api/v3/ticker/bookTicker."""

    symbol: Annotated[str, msgspec.Meta(description="Trading pair")]
    bid_price: Annotated[str, msgspec.Meta(description="Best bid price")]
    bid_qty: Annotated[str, msgspec.Meta(description="Best bid quantity")]
    ask_price: Annotated[str, msgspec.Meta(description="Best ask price")]
    ask_qty: Annotated[str, msgspec.Meta(description="Best ask quantity")]
```

**Step 8: Fix any issues and commit**

If manual fixes needed:
```bash
git add binance/_schemas/spot.py
git commit -m "fix: manual adjustments to generated spot schemas"
```

---

## Task 6: Create Schema Tests

**Files:**
- Create: `tests/unit/schemas/test_spot_schemas.py`

**Step 1: Write schema tests**

```python
# tests/unit/schemas/test_spot_schemas.py
"""Test spot API schemas."""
import msgspec
import pytest

from binance._schemas.spot import (
    Order,
    Account,
    Balance,
    Trade,
    MyTrade,
    OrderBook,
    TickerPrice,
    Ticker24h,
    BookTicker,
    ExchangeInfo,
    Symbol,
    RateLimit,
)


class TestOrderSchema:
    """Test Order schema."""

    def test_decode_order_response(self):
        """Test decoding order response JSON."""
        json_data = b'''{
            "symbol": "BTCUSDT",
            "orderId": 123456,
            "orderListId": -1,
            "clientOrderId": "test123",
            "transactTime": 1699999999999,
            "price": "50000.00",
            "origQty": "0.001",
            "executedQty": "0.001",
            "cummulativeQuoteQty": "50.00",
            "status": "FILLED",
            "timeInForce": "GTC",
            "type": "LIMIT",
            "side": "BUY"
        }'''

        order = msgspec.json.decode(json_data, type=Order)

        assert order.symbol == "BTCUSDT"
        assert order.order_id == 123456
        assert order.status == "FILLED"
        assert order.side == "BUY"

    def test_order_is_frozen(self):
        """Test Order is immutable."""
        order = Order(
            symbol="BTCUSDT",
            order_id=123,
            order_list_id=-1,
            client_order_id="test",
            transact_time=1699999999999,
            price="50000.00",
            orig_qty="0.001",
            executed_qty="0.001",
            cummulative_quote_qty="50.00",
            status="NEW",
            time_in_force="GTC",
            type="LIMIT",
            side="BUY",
        )

        with pytest.raises(AttributeError):
            order.status = "FILLED"  # Should fail - frozen


class TestAccountSchema:
    """Test Account schema."""

    def test_decode_account_response(self):
        """Test decoding account response with nested balances."""
        json_data = b'''{
            "makerCommission": 10,
            "takerCommission": 10,
            "buyerCommission": 0,
            "sellerCommission": 0,
            "canTrade": true,
            "canWithdraw": true,
            "canDeposit": true,
            "updateTime": 1699999999999,
            "accountType": "SPOT",
            "balances": [
                {"asset": "BTC", "free": "1.0", "locked": "0.0"},
                {"asset": "USDT", "free": "10000.0", "locked": "0.0"}
            ]
        }'''

        account = msgspec.json.decode(json_data, type=Account)

        assert account.can_trade is True
        assert account.account_type == "SPOT"
        assert len(account.balances) == 2
        assert account.balances[0].asset == "BTC"
        assert account.balances[0].free == "1.0"


class TestTradeSchema:
    """Test Trade schema."""

    def test_decode_trade(self):
        """Test decoding public trade."""
        json_data = b'''{
            "id": 123456,
            "price": "50000.00",
            "qty": "0.001",
            "quoteQty": "50.00",
            "time": 1699999999999,
            "isBuyerMaker": true,
            "isBestMatch": true
        }'''

        trade = msgspec.json.decode(json_data, type=Trade)

        assert trade.id == 123456
        assert trade.price == "50000.00"
        assert trade.is_buyer_maker is True


class TestOrderBookSchema:
    """Test OrderBook schema."""

    def test_decode_order_book(self):
        """Test decoding order book."""
        json_data = b'''{
            "lastUpdateId": 123456789,
            "bids": [["50000.00", "1.0"], ["49999.00", "2.0"]],
            "asks": [["50001.00", "1.5"], ["50002.00", "3.0"]]
        }'''

        book = msgspec.json.decode(json_data, type=OrderBook)

        assert book.last_update_id == 123456789
        assert len(book.bids) == 2
        assert book.bids[0] == ["50000.00", "1.0"]
        assert len(book.asks) == 2


class TestTickerSchemas:
    """Test ticker schemas."""

    def test_decode_ticker_price(self):
        """Test decoding price ticker."""
        json_data = b'{"symbol": "BTCUSDT", "price": "50000.00"}'

        ticker = msgspec.json.decode(json_data, type=TickerPrice)

        assert ticker.symbol == "BTCUSDT"
        assert ticker.price == "50000.00"

    def test_decode_book_ticker(self):
        """Test decoding book ticker."""
        json_data = b'''{
            "symbol": "BTCUSDT",
            "bidPrice": "50000.00",
            "bidQty": "1.0",
            "askPrice": "50001.00",
            "askQty": "2.0"
        }'''

        ticker = msgspec.json.decode(json_data, type=BookTicker)

        assert ticker.symbol == "BTCUSDT"
        assert ticker.bid_price == "50000.00"
        assert ticker.ask_price == "50001.00"
```

**Step 2: Run tests**

Run: `pytest tests/unit/schemas/test_spot_schemas.py -v`
Expected: PASS

**Step 3: Run mypy on tests**

Run: `mypy tests/unit/schemas/test_spot_schemas.py`
Expected: Success

**Step 4: Commit tests**

```bash
git add tests/unit/schemas/
git commit -m "test: add spot schema unit tests"
```

---

## Next Steps

Continue with [03-async-client.md](./03-async-client.md) to create the AsyncClient entry point.
