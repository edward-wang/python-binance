# Phase 3.2: Generate Spot API Schemas

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Generate msgspec schemas for Spot API responses in `binance/_schemas/spot.py` with comprehensive tests.

**Prerequisites:** Task 1-4 complete (api/spot/ modules exist)

---

## Task 5: Run Generator for Schemas

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

## Task 6: Review and Fix Generated Schemas

**Files:**
- Review: `binance/_schemas/spot.py`
- Modify if needed

**Step 1: Verify BaseStruct import and file header**

```python
# binance/_schemas/spot.py
"""Spot API schemas - Generated from OpenAPI specs.

Do not edit manually. Re-generate with: python -m generator spot --schemas

These schemas are used by api/spot/*.py for typed returns.
"""
from typing import Annotated

import msgspec

from binance._schemas.common import BaseStruct
```

**Step 2: Verify ServerTime schema**

```python
class ServerTime(BaseStruct):
    """Server time from GET /api/v3/time."""

    server_time: Annotated[int, msgspec.Meta(description="Server time in milliseconds")]
```

**Step 3: Verify Order response schema (multiple variations)**

```python
class Order(BaseStruct):
    """Order response from POST /api/v3/order.

    Note: Fields vary based on newOrderRespType (ACK, RESULT, FULL).
    Using optional fields to handle all cases.
    """

    symbol: Annotated[str, msgspec.Meta(description="Trading pair")]
    order_id: Annotated[int, msgspec.Meta(description="Order ID")]
    order_list_id: Annotated[int, msgspec.Meta(description="Order list ID, -1 if not part of list")]
    client_order_id: Annotated[str, msgspec.Meta(description="Client order ID")]
    transact_time: Annotated[int, msgspec.Meta(description="Transaction time in ms")]

    # RESULT and FULL response fields (optional for ACK)
    price: Annotated[str | None, msgspec.Meta(description="Order price")] = None
    orig_qty: Annotated[str | None, msgspec.Meta(description="Original quantity")] = None
    executed_qty: Annotated[str | None, msgspec.Meta(description="Executed quantity")] = None
    cummulative_quote_qty: Annotated[str | None, msgspec.Meta(description="Cumulative quote quantity")] = None
    status: Annotated[str | None, msgspec.Meta(description="Order status")] = None
    time_in_force: Annotated[str | None, msgspec.Meta(description="Time in force")] = None
    type: Annotated[str | None, msgspec.Meta(description="Order type")] = None
    side: Annotated[str | None, msgspec.Meta(description="Order side")] = None

    # FULL response only
    fills: Annotated[list["OrderFill"] | None, msgspec.Meta(description="Fill details")] = None


class OrderFill(BaseStruct):
    """Individual fill in FULL order response."""

    price: Annotated[str, msgspec.Meta(description="Fill price")]
    qty: Annotated[str, msgspec.Meta(description="Fill quantity")]
    commission: Annotated[str, msgspec.Meta(description="Commission")]
    commission_asset: Annotated[str, msgspec.Meta(description="Commission asset")]
    trade_id: Annotated[int, msgspec.Meta(description="Trade ID")]
```

**Step 4: Verify CancelOrderResult schema**

```python
class CancelOrderResult(BaseStruct):
    """Result from DELETE /api/v3/order."""

    symbol: Annotated[str, msgspec.Meta(description="Trading pair")]
    orig_client_order_id: Annotated[str, msgspec.Meta(description="Original client order ID")]
    order_id: Annotated[int, msgspec.Meta(description="Order ID")]
    order_list_id: Annotated[int, msgspec.Meta(description="Order list ID")]
    client_order_id: Annotated[str, msgspec.Meta(description="New client order ID")]
    price: Annotated[str, msgspec.Meta(description="Price")]
    orig_qty: Annotated[str, msgspec.Meta(description="Original quantity")]
    executed_qty: Annotated[str, msgspec.Meta(description="Executed quantity")]
    cummulative_quote_qty: Annotated[str, msgspec.Meta(description="Cumulative quote qty")]
    status: Annotated[str, msgspec.Meta(description="Order status")]
    time_in_force: Annotated[str, msgspec.Meta(description="Time in force")]
    type: Annotated[str, msgspec.Meta(description="Order type")]
    side: Annotated[str, msgspec.Meta(description="Order side")]
```

**Step 5: Verify Account schema with nested balances**

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
    permissions: Annotated[list[str], msgspec.Meta(description="Account permissions")]
```

**Step 6: Verify SymbolFilter with all filter types**

```python
class SymbolFilter(BaseStruct):
    """Symbol trading filter.

    Different filter types have different fields.
    All specific fields are optional.
    """

    filter_type: Annotated[str, msgspec.Meta(description="Filter type")]

    # PRICE_FILTER
    min_price: Annotated[str | None, msgspec.Meta(description="Min price")] = None
    max_price: Annotated[str | None, msgspec.Meta(description="Max price")] = None
    tick_size: Annotated[str | None, msgspec.Meta(description="Tick size")] = None

    # LOT_SIZE / MARKET_LOT_SIZE
    min_qty: Annotated[str | None, msgspec.Meta(description="Min quantity")] = None
    max_qty: Annotated[str | None, msgspec.Meta(description="Max quantity")] = None
    step_size: Annotated[str | None, msgspec.Meta(description="Step size")] = None

    # MIN_NOTIONAL / NOTIONAL
    min_notional: Annotated[str | None, msgspec.Meta(description="Min notional")] = None
    max_notional: Annotated[str | None, msgspec.Meta(description="Max notional")] = None
    apply_to_market: Annotated[bool | None, msgspec.Meta(description="Apply to market orders")] = None
    avg_price_mins: Annotated[int | None, msgspec.Meta(description="Avg price window")] = None

    # ICEBERG_PARTS
    limit: Annotated[int | None, msgspec.Meta(description="Limit")] = None

    # MAX_NUM_ORDERS / MAX_NUM_ALGO_ORDERS
    max_num_orders: Annotated[int | None, msgspec.Meta(description="Max orders")] = None
    max_num_algo_orders: Annotated[int | None, msgspec.Meta(description="Max algo orders")] = None

    # PERCENT_PRICE
    multiplier_up: Annotated[str | None, msgspec.Meta(description="Max price multiplier")] = None
    multiplier_down: Annotated[str | None, msgspec.Meta(description="Min price multiplier")] = None

    # TRAILING_DELTA
    min_trailing_above_delta: Annotated[int | None, msgspec.Meta(description="Min trailing delta")] = None
    max_trailing_above_delta: Annotated[int | None, msgspec.Meta(description="Max trailing delta")] = None
    min_trailing_below_delta: Annotated[int | None, msgspec.Meta(description="Min trailing below")] = None
    max_trailing_below_delta: Annotated[int | None, msgspec.Meta(description="Max trailing below")] = None
```

**Step 7: Verify Kline schema with from_raw() converter**

```python
class Kline(BaseStruct):
    """Typed kline with named fields for AI-friendly access.

    The API returns raw arrays, but we convert them to typed objects
    so users can access fields by name (kline.close) instead of index (kline[4]).
    """

    open_time: Annotated[int, msgspec.Meta(description="Kline open time in ms")]
    open: Annotated[str, msgspec.Meta(description="Open price")]
    high: Annotated[str, msgspec.Meta(description="High price")]
    low: Annotated[str, msgspec.Meta(description="Low price")]
    close: Annotated[str, msgspec.Meta(description="Close price")]
    volume: Annotated[str, msgspec.Meta(description="Base asset volume")]
    close_time: Annotated[int, msgspec.Meta(description="Kline close time in ms")]
    quote_volume: Annotated[str, msgspec.Meta(description="Quote asset volume")]
    trades: Annotated[int, msgspec.Meta(description="Number of trades")]
    taker_buy_base: Annotated[str, msgspec.Meta(description="Taker buy base volume")]
    taker_buy_quote: Annotated[str, msgspec.Meta(description="Taker buy quote volume")]

    @classmethod
    def from_raw(cls, raw: list[int | str]) -> "Kline":
        """Convert raw kline array to typed Kline.

        Args:
            raw: Raw kline array from API [open_time, open, high, low, close, ...]

        Returns:
            Typed Kline object with named fields
        """
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

**Step 8: Verify Ticker schemas**

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
    last_qty: Annotated[str, msgspec.Meta(description="Last quantity")]
    bid_price: Annotated[str, msgspec.Meta(description="Best bid price")]
    bid_qty: Annotated[str, msgspec.Meta(description="Best bid quantity")]
    ask_price: Annotated[str, msgspec.Meta(description="Best ask price")]
    ask_qty: Annotated[str, msgspec.Meta(description="Best ask quantity")]
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
```

**Step 9: Fix any issues and commit**

```bash
git add binance/_schemas/spot.py
git commit -m "fix: manual adjustments to generated spot schemas"
```

---

## Task 7: Create Comprehensive Schema Tests

**Files:**
- Create: `tests/unit/schemas/test_spot_schemas.py`

**Step 1: Write schema tests with edge cases**

```python
# tests/unit/schemas/test_spot_schemas.py
"""Test spot API schemas including edge cases."""
import msgspec
import pytest

from binance._schemas.spot import (
    ServerTime,
    Order,
    OrderFill,
    CancelOrderResult,
    Account,
    Balance,
    Trade,
    MyTrade,
    OrderBook,
    Kline,
    TickerPrice,
    Ticker24h,
    BookTicker,
    ExchangeInfo,
    Symbol,
    SymbolFilter,
    RateLimit,
    AvgPrice,
    AggTrade,
)


class TestServerTime:
    """Test ServerTime schema."""

    def test_decode_server_time(self):
        """Test basic decoding."""
        data = b'{"serverTime": 1699999999999}'
        result = msgspec.json.decode(data, type=ServerTime)
        assert result.server_time == 1699999999999

    def test_frozen_immutable(self):
        """Test schema is frozen."""
        st = ServerTime(server_time=123)
        with pytest.raises(AttributeError):
            st.server_time = 456


class TestOrder:
    """Test Order schema with response variations."""

    def test_decode_ack_response(self):
        """Test ACK response (minimal fields)."""
        data = b'''{
            "symbol": "BTCUSDT",
            "orderId": 123456,
            "orderListId": -1,
            "clientOrderId": "test123",
            "transactTime": 1699999999999
        }'''
        order = msgspec.json.decode(data, type=Order)
        assert order.symbol == "BTCUSDT"
        assert order.order_id == 123456
        assert order.price is None  # Not in ACK

    def test_decode_result_response(self):
        """Test RESULT response (includes status)."""
        data = b'''{
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
        order = msgspec.json.decode(data, type=Order)
        assert order.status == "FILLED"
        assert order.price == "50000.00"

    def test_decode_full_response_with_fills(self):
        """Test FULL response (includes fills)."""
        data = b'''{
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
            "type": "MARKET",
            "side": "BUY",
            "fills": [
                {"price": "50000.00", "qty": "0.001", "commission": "0.00001", "commissionAsset": "BTC", "tradeId": 789}
            ]
        }'''
        order = msgspec.json.decode(data, type=Order)
        assert order.fills is not None
        assert len(order.fills) == 1
        assert order.fills[0].trade_id == 789


class TestAccount:
    """Test Account schema."""

    def test_decode_account_with_balances(self):
        """Test decoding with nested balances."""
        data = b'''{
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
            ],
            "permissions": ["SPOT"]
        }'''
        account = msgspec.json.decode(data, type=Account)
        assert account.account_type == "SPOT"
        assert len(account.balances) == 2
        assert account.balances[0].asset == "BTC"

    def test_empty_balances(self):
        """Test with empty balances array."""
        data = b'''{
            "makerCommission": 10,
            "takerCommission": 10,
            "buyerCommission": 0,
            "sellerCommission": 0,
            "canTrade": true,
            "canWithdraw": true,
            "canDeposit": true,
            "updateTime": 1699999999999,
            "accountType": "SPOT",
            "balances": [],
            "permissions": []
        }'''
        account = msgspec.json.decode(data, type=Account)
        assert account.balances == []


class TestSymbolFilter:
    """Test SymbolFilter with different filter types."""

    def test_price_filter(self):
        """Test PRICE_FILTER type."""
        data = b'''{
            "filterType": "PRICE_FILTER",
            "minPrice": "0.01",
            "maxPrice": "1000000.0",
            "tickSize": "0.01"
        }'''
        f = msgspec.json.decode(data, type=SymbolFilter)
        assert f.filter_type == "PRICE_FILTER"
        assert f.min_price == "0.01"
        assert f.tick_size == "0.01"

    def test_lot_size_filter(self):
        """Test LOT_SIZE type."""
        data = b'''{
            "filterType": "LOT_SIZE",
            "minQty": "0.00001",
            "maxQty": "9000.0",
            "stepSize": "0.00001"
        }'''
        f = msgspec.json.decode(data, type=SymbolFilter)
        assert f.filter_type == "LOT_SIZE"
        assert f.step_size == "0.00001"

    def test_min_notional_filter(self):
        """Test MIN_NOTIONAL type."""
        data = b'''{
            "filterType": "MIN_NOTIONAL",
            "minNotional": "10.0",
            "applyToMarket": true,
            "avgPriceMins": 5
        }'''
        f = msgspec.json.decode(data, type=SymbolFilter)
        assert f.min_notional == "10.0"
        assert f.apply_to_market is True

    def test_unknown_fields_ignored(self):
        """Test unknown fields are silently ignored (msgspec default)."""
        data = b'''{
            "filterType": "UNKNOWN_FILTER",
            "unknownField": "value"
        }'''
        f = msgspec.json.decode(data, type=SymbolFilter)
        assert f.filter_type == "UNKNOWN_FILTER"


class TestOrderBook:
    """Test OrderBook schema."""

    def test_decode_order_book(self):
        """Test decoding order book."""
        data = b'''{
            "lastUpdateId": 123456789,
            "bids": [["50000.00", "1.0"], ["49999.00", "2.0"]],
            "asks": [["50001.00", "1.5"], ["50002.00", "3.0"]]
        }'''
        book = msgspec.json.decode(data, type=OrderBook)
        assert book.last_update_id == 123456789
        assert len(book.bids) == 2
        assert book.bids[0] == ["50000.00", "1.0"]

    def test_empty_order_book(self):
        """Test empty bids/asks (illiquid market)."""
        data = b'{"lastUpdateId": 1, "bids": [], "asks": []}'
        book = msgspec.json.decode(data, type=OrderBook)
        assert book.bids == []
        assert book.asks == []


class TestKline:
    """Test Kline schema with from_raw() converter."""

    def test_kline_from_raw(self):
        """Test converting raw kline array to typed Kline."""
        raw = [
            1699999999999,  # open_time
            "50000.00",     # open
            "51000.00",     # high
            "49000.00",     # low
            "50500.00",     # close
            "100.5",        # volume
            1700000003999,  # close_time
            "5025000.00",   # quote_volume
            1500,           # trades
            "60.3",         # taker_buy_base
            "3015000.00",   # taker_buy_quote
        ]
        kline = Kline.from_raw(raw)

        assert kline.open_time == 1699999999999
        assert kline.open == "50000.00"
        assert kline.high == "51000.00"
        assert kline.low == "49000.00"
        assert kline.close == "50500.00"
        assert kline.volume == "100.5"
        assert kline.close_time == 1700000003999
        assert kline.trades == 1500

    def test_kline_is_frozen(self):
        """Test Kline is immutable."""
        kline = Kline.from_raw([0, "1", "2", "3", "4", "5", 0, "6", 0, "7", "8"])
        with pytest.raises(AttributeError):
            kline.close = "9999"

    def test_kline_list_conversion(self):
        """Test converting list of raw klines."""
        raw_klines = [
            [1699999999999, "50000", "51000", "49000", "50500", "100", 1700000003999, "5000", 100, "60", "3000"],
            [1700000003999, "50500", "52000", "50000", "51500", "150", 1700000007999, "7500", 200, "90", "4500"],
        ]
        klines = [Kline.from_raw(k) for k in raw_klines]

        assert len(klines) == 2
        assert klines[0].close == "50500"
        assert klines[1].close == "51500"


class TestTickerVariants:
    """Test ticker schemas."""

    def test_ticker_price(self):
        """Test TickerPrice decoding."""
        data = b'{"symbol": "BTCUSDT", "price": "50000.00"}'
        ticker = msgspec.json.decode(data, type=TickerPrice)
        assert ticker.symbol == "BTCUSDT"
        assert ticker.price == "50000.00"

    def test_ticker_price_list(self):
        """Test list of TickerPrice."""
        data = b'[{"symbol": "BTCUSDT", "price": "50000"}, {"symbol": "ETHUSDT", "price": "3000"}]'
        tickers = msgspec.json.decode(data, type=list[TickerPrice])
        assert len(tickers) == 2

    def test_book_ticker(self):
        """Test BookTicker decoding."""
        data = b'''{
            "symbol": "BTCUSDT",
            "bidPrice": "50000.00",
            "bidQty": "1.0",
            "askPrice": "50001.00",
            "askQty": "2.0"
        }'''
        ticker = msgspec.json.decode(data, type=BookTicker)
        assert ticker.bid_price == "50000.00"


class TestTrade:
    """Test Trade schemas."""

    def test_public_trade(self):
        """Test public Trade decoding."""
        data = b'''{
            "id": 123456,
            "price": "50000.00",
            "qty": "0.001",
            "quoteQty": "50.00",
            "time": 1699999999999,
            "isBuyerMaker": true,
            "isBestMatch": true
        }'''
        trade = msgspec.json.decode(data, type=Trade)
        assert trade.id == 123456
        assert trade.is_buyer_maker is True

    def test_my_trade(self):
        """Test MyTrade (user's trade) decoding."""
        data = b'''{
            "symbol": "BTCUSDT",
            "id": 123456,
            "orderId": 789,
            "price": "50000.00",
            "qty": "0.001",
            "quoteQty": "50.00",
            "commission": "0.00001",
            "commissionAsset": "BTC",
            "time": 1699999999999,
            "isBuyer": true,
            "isMaker": false
        }'''
        trade = msgspec.json.decode(data, type=MyTrade)
        assert trade.order_id == 789
        assert trade.commission_asset == "BTC"


class TestDecoderPerformance:
    """Test pre-compiled decoders."""

    def test_precompiled_decoder_works(self):
        """Test that pre-compiled decoders work correctly."""
        decoder = msgspec.json.Decoder(Account)
        data = b'''{
            "makerCommission": 10, "takerCommission": 10,
            "buyerCommission": 0, "sellerCommission": 0,
            "canTrade": true, "canWithdraw": true, "canDeposit": true,
            "updateTime": 1, "accountType": "SPOT",
            "balances": [], "permissions": []
        }'''

        # Decode multiple times with same decoder
        for _ in range(100):
            result = decoder.decode(data)
            assert result.account_type == "SPOT"
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
git commit -m "test: add comprehensive spot schema unit tests"
```

---

## Next Steps

Continue with [03-async-client.md](./03-async-client.md) to create the AsyncClient entry point.
