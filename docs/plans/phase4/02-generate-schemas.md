# Phase 4.2: Generate Futures API Schemas

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create `binance/_schemas/futures.py` with typed schemas for Futures API responses.

**Prerequisites:** Task 1 complete (config URLs added)

**Note:** Execute this file BEFORE 01-generate-endpoints.md Tasks 5-7, as endpoints import these schemas.

---

## Task 2: Update Spot Schemas for Futures Compatibility

**Files:**
- Modify: `binance/_schemas/spot.py`
- Modify: `tests/unit/schemas/test_spot_schemas.py`

**Context:** Some spot schemas are reused for futures endpoints, but have slight differences:
- `Trade`: Futures doesn't have `isBestMatch` field
- `OrderBook`: Futures has extra `E` (event time) and `T` (transaction time) fields

**Step 1: Write compatibility test**

```python
# Add to tests/unit/schemas/test_spot_schemas.py

def test_trade_without_is_best_match():
    """Test Trade schema works without is_best_match (futures compatibility)."""
    from binance._schemas.spot import Trade
    import msgspec

    # Futures trade response (no isBestMatch)
    data = b'{"id": 123, "price": "50000", "qty": "0.1", "quoteQty": "5000", "time": 1699999999, "isBuyerMaker": true}'
    trade = msgspec.json.decode(data, type=Trade)
    assert trade.id == 123
    assert trade.is_best_match is None


def test_orderbook_with_event_time():
    """Test OrderBook with E and T fields (futures compatibility)."""
    from binance._schemas.spot import OrderBook
    import msgspec

    # Futures orderbook response (has E and T)
    data = b'{"lastUpdateId": 1027024, "E": 1589436922972, "T": 1589436922959, "bids": [["4.00", "10"]], "asks": [["4.01", "5"]]}'
    book = msgspec.json.decode(data, type=OrderBook)
    assert book.last_update_id == 1027024
    assert book.e == 1589436922972
    assert book.t == 1589436922959
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/schemas/test_spot_schemas.py -v -k "without_is_best_match or with_event_time"`
Expected: FAIL

**Step 3: Update spot schemas for compatibility**

```python
# binance/_schemas/spot.py - modify Trade class

class Trade(BaseStruct):
    """Public trade from GET /api/v3/trades.

    Note: is_best_match is optional for futures API compatibility
    (futures /trades endpoint doesn't return this field).
    """

    id: Annotated[int, msgspec.Meta(description="Trade ID")]
    price: Annotated[str, msgspec.Meta(description="Price")]
    qty: Annotated[str, msgspec.Meta(description="Quantity")]
    quote_qty: Annotated[str, msgspec.Meta(description="Quote quantity")]
    time: Annotated[int, msgspec.Meta(description="Trade time")]
    is_buyer_maker: Annotated[bool, msgspec.Meta(description="Buyer is maker")]
    is_best_match: Annotated[bool | None, msgspec.Meta(description="Best match (spot only)")] = None
```

```python
# binance/_schemas/spot.py - modify OrderBook class

class OrderBook(BaseStruct):
    """Order book from GET /api/v3/depth.

    Note: e and t fields are optional - present in futures API responses
    (event time and transaction time).
    """

    last_update_id: Annotated[int, msgspec.Meta(description="Last update ID")]
    bids: Annotated[list[list[str]], msgspec.Meta(description="Bid orders [price, qty]")]
    asks: Annotated[list[list[str]], msgspec.Meta(description="Ask orders [price, qty]")]
    # Futures-only fields (optional for spot compatibility)
    e: Annotated[int | None, msgspec.Meta(description="Event time (futures only)")] = None
    t: Annotated[int | None, msgspec.Meta(description="Transaction time (futures only)")] = None
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/unit/schemas/test_spot_schemas.py -v`
Expected: PASS

**Step 5: Verify existing spot tests still pass**

Run: `pytest tests/ -v -k "spot"`
Expected: All PASS

**Step 6: Commit**

```bash
git add binance/_schemas/spot.py tests/unit/schemas/test_spot_schemas.py
git commit -m "fix: make spot schemas compatible with futures API responses"
```

---

## Task 3: Create Futures Schemas File

**Files:**
- Create: `binance/_schemas/futures.py`
- Create: `tests/unit/schemas/test_futures_schemas.py`

**Step 1: Write the failing test**

```python
# tests/unit/schemas/test_futures_schemas.py
"""Test futures API schemas."""


def test_futures_schemas_importable():
    """Test that futures schemas can be imported."""
    from binance._schemas.futures import (
        FuturesExchangeInfo,
        FuturesKline,
        FuturesOrder,
        FuturesAccount,
        FuturesAsset,
        FuturesBalance,
        AccountPosition,
        PositionRisk,
        MarkPrice,
        FundingRate,
        LeverageResult,
        FuturesTicker24h,
        FuturesMyTrade,
    )
    assert FuturesExchangeInfo is not None
    assert FuturesKline is not None
    assert FuturesOrder is not None
    assert AccountPosition is not None
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit/schemas/test_futures_schemas.py::test_futures_schemas_importable -v`
Expected: FAIL with "No module named 'binance._schemas.futures'"

**Step 3: Create futures schemas**

```python
# binance/_schemas/futures.py
"""Futures API schemas for USDT-M and COIN-M futures.

These schemas are used by api/futures_um/*.py and api/futures_cm/*.py for typed returns.
Uses BaseStruct with rename="camel" for automatic snake_case <-> camelCase.
"""
from typing import Annotated

import msgspec

from binance._schemas.common import BaseStruct


# ============ Exchange Info ============


class FuturesRateLimit(BaseStruct):
    """Rate limit info in futures exchange info."""

    rate_limit_type: Annotated[str, msgspec.Meta(description="Rate limit type")]
    interval: Annotated[str, msgspec.Meta(description="Interval unit")]
    interval_num: Annotated[int, msgspec.Meta(description="Interval count")]
    limit: Annotated[int, msgspec.Meta(description="Request limit")]


class FuturesSymbolFilter(BaseStruct):
    """Symbol trading filter for futures.

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

    # MIN_NOTIONAL
    notional: Annotated[str | None, msgspec.Meta(description="Min notional")] = None

    # PERCENT_PRICE
    multiplier_up: Annotated[str | None, msgspec.Meta(description="Max price multiplier")] = None
    multiplier_down: Annotated[str | None, msgspec.Meta(description="Min price multiplier")] = None
    multiplier_decimal: Annotated[str | None, msgspec.Meta(description="Multiplier decimal")] = None

    # MAX_NUM_ORDERS / MAX_NUM_ALGO_ORDERS
    limit: Annotated[int | None, msgspec.Meta(description="Limit")] = None


class FuturesSymbol(BaseStruct):
    """Symbol info in futures exchange info."""

    symbol: Annotated[str, msgspec.Meta(description="Trading pair")]
    pair: Annotated[str, msgspec.Meta(description="Underlying pair")]
    contract_type: Annotated[str, msgspec.Meta(description="Contract type")]
    delivery_date: Annotated[int, msgspec.Meta(description="Delivery date")]
    onboard_date: Annotated[int, msgspec.Meta(description="Onboard date")]
    status: Annotated[str, msgspec.Meta(description="Symbol status")]
    maint_margin_percent: Annotated[str, msgspec.Meta(description="Maintenance margin percent")]
    required_margin_percent: Annotated[str, msgspec.Meta(description="Required margin percent")]
    base_asset: Annotated[str, msgspec.Meta(description="Base asset")]
    quote_asset: Annotated[str, msgspec.Meta(description="Quote asset")]
    margin_asset: Annotated[str, msgspec.Meta(description="Margin asset")]
    price_precision: Annotated[int, msgspec.Meta(description="Price precision")]
    quantity_precision: Annotated[int, msgspec.Meta(description="Quantity precision")]
    base_asset_precision: Annotated[int, msgspec.Meta(description="Base asset precision")]
    quote_precision: Annotated[int, msgspec.Meta(description="Quote precision")]
    underlying_type: Annotated[str, msgspec.Meta(description="Underlying type")]
    settle_plan: Annotated[int, msgspec.Meta(description="Settle plan")] = 0
    trigger_protect: Annotated[str, msgspec.Meta(description="Trigger protect")] = "0"
    order_types: Annotated[list[str], msgspec.Meta(description="Allowed order types")] = []
    time_in_force: Annotated[list[str], msgspec.Meta(description="Time in force options")] = []
    filters: Annotated[list[FuturesSymbolFilter], msgspec.Meta(description="Trading filters")] = []
    underlying_sub_type: Annotated[list[str], msgspec.Meta(description="Underlying sub type")] = []
    liquidation_fee: Annotated[str, msgspec.Meta(description="Liquidation fee")] = "0"
    market_take_bound: Annotated[str, msgspec.Meta(description="Market take bound")] = "0"


class FuturesExchangeInfo(BaseStruct):
    """Exchange info from GET /fapi/v1/exchangeInfo or /dapi/v1/exchangeInfo."""

    timezone: Annotated[str, msgspec.Meta(description="Server timezone")]
    server_time: Annotated[int, msgspec.Meta(description="Server time")]
    rate_limits: Annotated[list[FuturesRateLimit], msgspec.Meta(description="Rate limits")]
    symbols: Annotated[list[FuturesSymbol], msgspec.Meta(description="Trading symbols")]
    exchange_filters: Annotated[list[dict], msgspec.Meta(description="Exchange filters")] = []
    futures_type: Annotated[str | None, msgspec.Meta(description="Futures type")] = None


# ============ Market Data ============


class FuturesKline(BaseStruct):
    """Typed kline for futures with named fields.

    The API returns raw arrays, converted to typed objects for AI-friendliness.
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
    def from_raw(cls, raw: list[int | str]) -> "FuturesKline":
        """Convert raw kline array to typed FuturesKline.

        Args:
            raw: Raw kline array from API [open_time, open, high, low, close, ...]

        Returns:
            Typed FuturesKline object with named fields
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


class MarkPrice(BaseStruct):
    """Mark price and funding rate from GET /fapi/v1/premiumIndex."""

    symbol: Annotated[str, msgspec.Meta(description="Trading pair")]
    mark_price: Annotated[str, msgspec.Meta(description="Mark price")]
    index_price: Annotated[str, msgspec.Meta(description="Index price")]
    estimated_settle_price: Annotated[str | None, msgspec.Meta(description="Estimated settle price")] = None
    last_funding_rate: Annotated[str, msgspec.Meta(description="Last funding rate")]
    next_funding_time: Annotated[int, msgspec.Meta(description="Next funding time in ms")]
    interest_rate: Annotated[str | None, msgspec.Meta(description="Interest rate")] = None
    time: Annotated[int, msgspec.Meta(description="Update time")]


class FundingRate(BaseStruct):
    """Funding rate history from GET /fapi/v1/fundingRate."""

    symbol: Annotated[str, msgspec.Meta(description="Trading pair")]
    funding_rate: Annotated[str, msgspec.Meta(description="Funding rate")]
    funding_time: Annotated[int, msgspec.Meta(description="Funding time in ms")]
    mark_price: Annotated[str | None, msgspec.Meta(description="Mark price at funding")] = None


class FuturesTicker24h(BaseStruct):
    """24hr ticker for futures from GET /fapi/v1/ticker/24hr."""

    symbol: Annotated[str, msgspec.Meta(description="Trading pair")]
    price_change: Annotated[str, msgspec.Meta(description="Price change")]
    price_change_percent: Annotated[str, msgspec.Meta(description="Price change percent")]
    weighted_avg_price: Annotated[str, msgspec.Meta(description="Weighted average price")]
    last_price: Annotated[str, msgspec.Meta(description="Last price")]
    last_qty: Annotated[str, msgspec.Meta(description="Last quantity")]
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


# ============ Order/Trade ============


class FuturesOrder(BaseStruct):
    """Order response for futures.

    Used for create, query, and cancel order responses.
    """

    symbol: Annotated[str, msgspec.Meta(description="Trading pair")]
    order_id: Annotated[int, msgspec.Meta(description="Order ID")]
    client_order_id: Annotated[str, msgspec.Meta(description="Client order ID")]
    price: Annotated[str, msgspec.Meta(description="Order price")]
    orig_qty: Annotated[str, msgspec.Meta(description="Original quantity")]
    executed_qty: Annotated[str, msgspec.Meta(description="Executed quantity")]
    cum_qty: Annotated[str | None, msgspec.Meta(description="Cumulative quantity")] = None
    cum_quote: Annotated[str | None, msgspec.Meta(description="Cumulative quote")] = None
    status: Annotated[str, msgspec.Meta(description="Order status")]
    time_in_force: Annotated[str, msgspec.Meta(description="Time in force")]
    type: Annotated[str, msgspec.Meta(description="Order type")]
    side: Annotated[str, msgspec.Meta(description="Order side")]
    stop_price: Annotated[str | None, msgspec.Meta(description="Stop price")] = None
    price_protect: Annotated[bool | None, msgspec.Meta(description="Price protection")] = None
    orig_type: Annotated[str | None, msgspec.Meta(description="Original order type")] = None
    position_side: Annotated[str | None, msgspec.Meta(description="Position side")] = None
    close_position: Annotated[bool | None, msgspec.Meta(description="Close position")] = None
    activation_price: Annotated[str | None, msgspec.Meta(description="Activation price")] = None
    callback_rate: Annotated[str | None, msgspec.Meta(description="Callback rate")] = None
    working_type: Annotated[str | None, msgspec.Meta(description="Working type")] = None
    reduce_only: Annotated[bool | None, msgspec.Meta(description="Reduce only")] = None
    avg_price: Annotated[str | None, msgspec.Meta(description="Average fill price")] = None
    update_time: Annotated[int | None, msgspec.Meta(description="Update time")] = None
    time: Annotated[int | None, msgspec.Meta(description="Order time")] = None


class FuturesMyTrade(BaseStruct):
    """User's trade for futures."""

    symbol: Annotated[str, msgspec.Meta(description="Trading pair")]
    id: Annotated[int, msgspec.Meta(description="Trade ID")]
    order_id: Annotated[int, msgspec.Meta(description="Order ID")]
    price: Annotated[str, msgspec.Meta(description="Price")]
    qty: Annotated[str, msgspec.Meta(description="Quantity")]
    quote_qty: Annotated[str, msgspec.Meta(description="Quote quantity")]
    commission: Annotated[str, msgspec.Meta(description="Commission")]
    commission_asset: Annotated[str, msgspec.Meta(description="Commission asset")]
    time: Annotated[int, msgspec.Meta(description="Trade time")]
    buyer: Annotated[bool, msgspec.Meta(description="Is buyer")]
    maker: Annotated[bool, msgspec.Meta(description="Is maker")]
    position_side: Annotated[str | None, msgspec.Meta(description="Position side")] = None
    realized_pnl: Annotated[str | None, msgspec.Meta(description="Realized PnL")] = None


class BatchOrderError(BaseStruct):
    """Error response for a single order in batch orders.

    When an order in a batch fails, the API returns this instead of FuturesOrder.
    """

    code: Annotated[int, msgspec.Meta(description="Error code")]
    msg: Annotated[str, msgspec.Meta(description="Error message")]


# BatchOrderResult is a union - each item in batch response is either order or error
# Use msgspec.Struct with tag for discrimination, or handle manually in decoder
BatchOrderResult = FuturesOrder | BatchOrderError


# ============ Account/Position ============


class FuturesAsset(BaseStruct):
    """Asset in futures account.

    Note: margin_available is USDT-M only (v2 endpoint), COIN-M (v1) doesn't return it.
    """

    asset: Annotated[str, msgspec.Meta(description="Asset name")]
    wallet_balance: Annotated[str, msgspec.Meta(description="Wallet balance")]
    unrealized_profit: Annotated[str, msgspec.Meta(description="Unrealized profit")]
    margin_balance: Annotated[str, msgspec.Meta(description="Margin balance")]
    maint_margin: Annotated[str, msgspec.Meta(description="Maintenance margin")]
    initial_margin: Annotated[str, msgspec.Meta(description="Initial margin")]
    position_initial_margin: Annotated[str, msgspec.Meta(description="Position initial margin")]
    open_order_initial_margin: Annotated[str, msgspec.Meta(description="Open order initial margin")]
    max_withdraw_amount: Annotated[str, msgspec.Meta(description="Max withdraw amount")]
    cross_wallet_balance: Annotated[str | None, msgspec.Meta(description="Cross wallet balance")] = None
    cross_un_pnl: Annotated[str | None, msgspec.Meta(description="Cross unrealized PnL")] = None
    available_balance: Annotated[str | None, msgspec.Meta(description="Available balance")] = None
    margin_available: Annotated[bool | None, msgspec.Meta(description="Margin available (USDT-M only)")] = None
    update_time: Annotated[int | None, msgspec.Meta(description="Update time")] = None


class AccountPosition(BaseStruct):
    """Position in GET /fapi/v2/account response.

    Note: This is different from PositionRisk (GET /fapi/v2/positionRisk).
    Account positions have margin/notional details, while PositionRisk has
    liquidation/mark price details.
    """

    symbol: Annotated[str, msgspec.Meta(description="Trading pair")]
    position_amt: Annotated[str, msgspec.Meta(description="Position amount")]
    entry_price: Annotated[str, msgspec.Meta(description="Entry price")]
    unrealized_profit: Annotated[str, msgspec.Meta(description="Unrealized profit")]
    leverage: Annotated[str, msgspec.Meta(description="Leverage")]
    position_side: Annotated[str, msgspec.Meta(description="Position side")]
    initial_margin: Annotated[str, msgspec.Meta(description="Initial margin")]
    maint_margin: Annotated[str, msgspec.Meta(description="Maintenance margin")]
    position_initial_margin: Annotated[str, msgspec.Meta(description="Position initial margin")]
    open_order_initial_margin: Annotated[str, msgspec.Meta(description="Open order initial margin")]
    isolated: Annotated[bool, msgspec.Meta(description="Is isolated margin")]
    max_notional: Annotated[str | None, msgspec.Meta(description="Max notional")] = None
    bid_notional: Annotated[str | None, msgspec.Meta(description="Bid notional")] = None
    ask_notional: Annotated[str | None, msgspec.Meta(description="Ask notional")] = None
    break_even_price: Annotated[str | None, msgspec.Meta(description="Break even price")] = None
    max_qty: Annotated[str | None, msgspec.Meta(description="Max qty (COIN-M)")] = None
    notional_value: Annotated[str | None, msgspec.Meta(description="Notional value (COIN-M)")] = None
    update_time: Annotated[int | None, msgspec.Meta(description="Update time")] = None


class FuturesAccount(BaseStruct):
    """Futures account information from GET /fapi/v2/account."""

    total_initial_margin: Annotated[str, msgspec.Meta(description="Total initial margin")]
    total_maint_margin: Annotated[str, msgspec.Meta(description="Total maintenance margin")]
    total_wallet_balance: Annotated[str, msgspec.Meta(description="Total wallet balance")]
    total_unrealized_profit: Annotated[str, msgspec.Meta(description="Total unrealized profit")]
    total_margin_balance: Annotated[str, msgspec.Meta(description="Total margin balance")]
    total_position_initial_margin: Annotated[str, msgspec.Meta(description="Total position initial margin")]
    total_open_order_initial_margin: Annotated[str, msgspec.Meta(description="Total open order initial margin")]
    total_cross_wallet_balance: Annotated[str, msgspec.Meta(description="Total cross wallet balance")]
    total_cross_un_pnl: Annotated[str, msgspec.Meta(description="Total cross unrealized PnL")]
    available_balance: Annotated[str, msgspec.Meta(description="Available balance")]
    max_withdraw_amount: Annotated[str, msgspec.Meta(description="Max withdraw amount")]
    assets: Annotated[list[FuturesAsset], msgspec.Meta(description="Asset balances")]
    positions: Annotated[list[AccountPosition], msgspec.Meta(description="Positions")]
    can_trade: Annotated[bool | None, msgspec.Meta(description="Can trade")] = None
    can_deposit: Annotated[bool | None, msgspec.Meta(description="Can deposit")] = None
    can_withdraw: Annotated[bool | None, msgspec.Meta(description="Can withdraw")] = None
    fee_tier: Annotated[int | None, msgspec.Meta(description="Fee tier")] = None
    update_time: Annotated[int | None, msgspec.Meta(description="Update time")] = None


class FuturesBalance(BaseStruct):
    """Futures balance from GET /fapi/v2/balance (USDT-M) or /dapi/v1/balance (COIN-M).

    Note: USDT-M and COIN-M have different field names:
    - USDT-M: maxWithdrawAmount, marginAvailable
    - COIN-M: withdrawAvailable (no marginAvailable)
    """

    account_alias: Annotated[str, msgspec.Meta(description="Account alias")]
    asset: Annotated[str, msgspec.Meta(description="Asset name")]
    balance: Annotated[str, msgspec.Meta(description="Wallet balance")]
    cross_wallet_balance: Annotated[str, msgspec.Meta(description="Cross wallet balance")]
    available_balance: Annotated[str, msgspec.Meta(description="Available balance")]
    cross_un_pnl: Annotated[str | None, msgspec.Meta(description="Cross unrealized PnL")] = None
    # USDT-M only fields
    max_withdraw_amount: Annotated[str | None, msgspec.Meta(description="Max withdraw amount (USDT-M)")] = None
    margin_available: Annotated[bool | None, msgspec.Meta(description="Margin available (USDT-M)")] = None
    # COIN-M only fields
    withdraw_available: Annotated[str | None, msgspec.Meta(description="Withdraw available (COIN-M)")] = None
    update_time: Annotated[int | None, msgspec.Meta(description="Update time")] = None


class PositionRisk(BaseStruct):
    """Position risk from GET /fapi/v2/positionRisk (USDT-M) or /dapi/v1/positionRisk (COIN-M).

    Note: Field `un_realized_profit` uses underscore because the API returns
    `unRealizedProfit` (capital R), unlike `account` endpoint which returns
    `unrealizedProfit` (lowercase r). This is a Binance API inconsistency.

    USDT-M and COIN-M differences:
    - USDT-M: maxNotionalValue, notional, isolatedWallet
    - COIN-M: maxQty (instead of maxNotionalValue)
    """

    symbol: Annotated[str, msgspec.Meta(description="Trading pair")]
    position_amt: Annotated[str, msgspec.Meta(description="Position amount")]
    entry_price: Annotated[str, msgspec.Meta(description="Entry price")]
    break_even_price: Annotated[str | None, msgspec.Meta(description="Break even price")] = None
    mark_price: Annotated[str, msgspec.Meta(description="Mark price")]
    # API returns `unRealizedProfit` (capital R) - different from account endpoint
    un_realized_profit: Annotated[str, msgspec.Meta(description="Unrealized profit")]
    liquidation_price: Annotated[str, msgspec.Meta(description="Liquidation price")]
    leverage: Annotated[str, msgspec.Meta(description="Leverage")]
    margin_type: Annotated[str, msgspec.Meta(description="Margin type")]
    position_side: Annotated[str, msgspec.Meta(description="Position side")]
    isolated_margin: Annotated[str | None, msgspec.Meta(description="Isolated margin")] = None
    is_auto_add_margin: Annotated[str | None, msgspec.Meta(description="Auto add margin")] = None
    # USDT-M only fields
    max_notional_value: Annotated[str | None, msgspec.Meta(description="Max notional value (USDT-M)")] = None
    notional: Annotated[str | None, msgspec.Meta(description="Notional value (USDT-M)")] = None
    isolated_wallet: Annotated[str | None, msgspec.Meta(description="Isolated wallet (USDT-M)")] = None
    # COIN-M only fields
    max_qty: Annotated[str | None, msgspec.Meta(description="Max quantity (COIN-M)")] = None
    update_time: Annotated[int | None, msgspec.Meta(description="Update time")] = None


class LeverageResult(BaseStruct):
    """Result from POST /fapi/v1/leverage (USDT-M) or /dapi/v1/leverage (COIN-M).

    Note: USDT-M returns maxNotionalValue, COIN-M returns maxQty.
    """

    leverage: Annotated[int, msgspec.Meta(description="New leverage")]
    symbol: Annotated[str, msgspec.Meta(description="Trading pair")]
    # USDT-M only
    max_notional_value: Annotated[str | None, msgspec.Meta(description="Max notional value (USDT-M)")] = None
    # COIN-M only
    max_qty: Annotated[str | None, msgspec.Meta(description="Max quantity (COIN-M)")] = None
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/unit/schemas/test_futures_schemas.py -v`
Expected: PASS

**Step 5: Run mypy**

Run: `mypy binance/_schemas/futures.py --strict`
Expected: Success

**Step 6: Commit**

```bash
git add binance/_schemas/futures.py tests/unit/schemas/test_futures_schemas.py
git commit -m "feat: add futures API schemas with typed structs"
```

---

## Task 4: Add Comprehensive Schema Tests

**Files:**
- Modify: `tests/unit/schemas/test_futures_schemas.py`

**Step 1: Add comprehensive schema tests**

```python
# tests/unit/schemas/test_futures_schemas.py (extended)
"""Test futures API schemas including edge cases."""
import msgspec
import pytest

from binance._schemas.futures import (
    FuturesExchangeInfo,
    FuturesSymbol,
    FuturesKline,
    FuturesOrder,
    FuturesAccount,
    FuturesAsset,
    FuturesBalance,
    AccountPosition,
    PositionRisk,
    MarkPrice,
    FundingRate,
    LeverageResult,
    FuturesTicker24h,
    FuturesMyTrade,
)


class TestFuturesKline:
    """Test FuturesKline schema with from_raw() converter."""

    def test_kline_from_raw(self):
        """Test converting raw kline array to typed FuturesKline."""
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
        kline = FuturesKline.from_raw(raw)

        assert kline.open_time == 1699999999999
        assert kline.open == "50000.00"
        assert kline.high == "51000.00"
        assert kline.low == "49000.00"
        assert kline.close == "50500.00"
        assert kline.volume == "100.5"
        assert kline.close_time == 1700000003999
        assert kline.trades == 1500

    def test_kline_is_frozen(self):
        """Test FuturesKline is immutable."""
        kline = FuturesKline.from_raw([0, "1", "2", "3", "4", "5", 0, "6", 0, "7", "8"])
        with pytest.raises(AttributeError):
            kline.close = "9999"


class TestFuturesOrder:
    """Test FuturesOrder schema."""

    def test_decode_new_order(self):
        """Test decoding new order response."""
        data = b'''{
            "symbol": "BTCUSDT",
            "orderId": 12345678,
            "clientOrderId": "test123",
            "price": "50000.00",
            "origQty": "0.001",
            "executedQty": "0.000",
            "status": "NEW",
            "timeInForce": "GTC",
            "type": "LIMIT",
            "side": "BUY",
            "positionSide": "BOTH",
            "updateTime": 1699999999999
        }'''
        order = msgspec.json.decode(data, type=FuturesOrder)
        assert order.symbol == "BTCUSDT"
        assert order.order_id == 12345678
        assert order.status == "NEW"

    def test_decode_filled_order_with_avg_price(self):
        """Test decoding filled order with average price."""
        data = b'''{
            "symbol": "BTCUSDT",
            "orderId": 12345678,
            "clientOrderId": "test123",
            "price": "0",
            "origQty": "0.001",
            "executedQty": "0.001",
            "status": "FILLED",
            "timeInForce": "GTC",
            "type": "MARKET",
            "side": "BUY",
            "avgPrice": "50123.45",
            "updateTime": 1699999999999
        }'''
        order = msgspec.json.decode(data, type=FuturesOrder)
        assert order.status == "FILLED"
        assert order.avg_price == "50123.45"


class TestPositionRisk:
    """Test PositionRisk schema."""

    def test_decode_position(self):
        """Test decoding position risk."""
        data = b'''{
            "symbol": "BTCUSDT",
            "positionAmt": "0.001",
            "entryPrice": "50000.00",
            "markPrice": "50500.00",
            "unRealizedProfit": "0.50",
            "liquidationPrice": "0",
            "leverage": "20",
            "marginType": "cross",
            "positionSide": "BOTH"
        }'''
        position = msgspec.json.decode(data, type=PositionRisk)
        assert position.symbol == "BTCUSDT"
        assert position.position_amt == "0.001"
        assert position.leverage == "20"
        assert position.margin_type == "cross"

    def test_decode_empty_position(self):
        """Test decoding position with zero amount."""
        data = b'''{
            "symbol": "ETHUSDT",
            "positionAmt": "0",
            "entryPrice": "0.00000000",
            "markPrice": "3000.00",
            "unRealizedProfit": "0.00000000",
            "liquidationPrice": "0",
            "leverage": "10",
            "marginType": "cross",
            "positionSide": "BOTH"
        }'''
        position = msgspec.json.decode(data, type=PositionRisk)
        assert position.position_amt == "0"


class TestMarkPrice:
    """Test MarkPrice schema."""

    def test_decode_mark_price(self):
        """Test decoding mark price response."""
        data = b'''{
            "symbol": "BTCUSDT",
            "markPrice": "50000.00000000",
            "indexPrice": "49995.00000000",
            "lastFundingRate": "0.00010000",
            "nextFundingTime": 1700000000000,
            "time": 1699999999999
        }'''
        mark = msgspec.json.decode(data, type=MarkPrice)
        assert mark.symbol == "BTCUSDT"
        assert mark.mark_price == "50000.00000000"
        assert mark.last_funding_rate == "0.00010000"

    def test_decode_mark_price_with_interest_rate(self):
        """Test decoding mark price with interest rate field."""
        data = b'''{
            "symbol": "BTCUSDT",
            "markPrice": "50000.00",
            "indexPrice": "49995.00",
            "estimatedSettlePrice": "50010.00",
            "lastFundingRate": "0.0001",
            "interestRate": "0.0003",
            "nextFundingTime": 1700000000000,
            "time": 1699999999999
        }'''
        mark = msgspec.json.decode(data, type=MarkPrice)
        assert mark.estimated_settle_price == "50010.00"
        assert mark.interest_rate == "0.0003"


class TestFundingRate:
    """Test FundingRate schema."""

    def test_decode_funding_rate(self):
        """Test decoding funding rate history."""
        data = b'''{
            "symbol": "BTCUSDT",
            "fundingRate": "0.00010000",
            "fundingTime": 1699999999999
        }'''
        rate = msgspec.json.decode(data, type=FundingRate)
        assert rate.symbol == "BTCUSDT"
        assert rate.funding_rate == "0.00010000"

    def test_decode_funding_rate_list(self):
        """Test decoding list of funding rates."""
        data = b'''[
            {"symbol": "BTCUSDT", "fundingRate": "0.0001", "fundingTime": 1699999999999},
            {"symbol": "BTCUSDT", "fundingRate": "0.0002", "fundingTime": 1699996399999}
        ]'''
        rates = msgspec.json.decode(data, type=list[FundingRate])
        assert len(rates) == 2
        assert rates[0].funding_rate == "0.0001"


class TestFuturesAccount:
    """Test FuturesAccount schema."""

    def test_decode_account_with_positions(self):
        """Test decoding account with positions."""
        data = b'''{
            "totalInitialMargin": "100.00000000",
            "totalMaintMargin": "50.00000000",
            "totalWalletBalance": "10000.00000000",
            "totalUnrealizedProfit": "50.00000000",
            "totalMarginBalance": "10050.00000000",
            "totalPositionInitialMargin": "100.00000000",
            "totalOpenOrderInitialMargin": "0.00000000",
            "totalCrossWalletBalance": "10000.00000000",
            "totalCrossUnPnl": "50.00000000",
            "availableBalance": "9900.00000000",
            "maxWithdrawAmount": "9900.00000000",
            "assets": [
                {
                    "asset": "USDT",
                    "walletBalance": "10000.00",
                    "unrealizedProfit": "50.00",
                    "marginBalance": "10050.00",
                    "maintMargin": "50.00",
                    "initialMargin": "100.00",
                    "positionInitialMargin": "100.00",
                    "openOrderInitialMargin": "0.00",
                    "maxWithdrawAmount": "9900.00"
                }
            ],
            "positions": [
                {
                    "symbol": "BTCUSDT",
                    "positionAmt": "0.001",
                    "entryPrice": "50000.00",
                    "markPrice": "50050.00",
                    "unrealizedProfit": "0.05",
                    "liquidationPrice": "40000.00",
                    "leverage": "20",
                    "marginType": "cross",
                    "positionSide": "BOTH"
                }
            ]
        }'''
        account = msgspec.json.decode(data, type=FuturesAccount)
        assert account.total_wallet_balance == "10000.00000000"
        assert len(account.assets) == 1
        assert account.assets[0].asset == "USDT"
        assert len(account.positions) == 1
        assert account.positions[0].symbol == "BTCUSDT"


class TestLeverageResult:
    """Test LeverageResult schema."""

    def test_decode_leverage_result(self):
        """Test decoding leverage change result."""
        data = b'''{
            "leverage": 20,
            "maxNotionalValue": "1000000",
            "symbol": "BTCUSDT"
        }'''
        result = msgspec.json.decode(data, type=LeverageResult)
        assert result.leverage == 20
        assert result.max_notional_value == "1000000"
        assert result.symbol == "BTCUSDT"


class TestFuturesExchangeInfo:
    """Test FuturesExchangeInfo schema."""

    def test_decode_exchange_info(self):
        """Test decoding futures exchange info."""
        data = b'''{
            "timezone": "UTC",
            "serverTime": 1699999999999,
            "rateLimits": [
                {"rateLimitType": "REQUEST_WEIGHT", "interval": "MINUTE", "intervalNum": 1, "limit": 2400}
            ],
            "exchangeFilters": [],
            "symbols": [
                {
                    "symbol": "BTCUSDT",
                    "pair": "BTCUSDT",
                    "contractType": "PERPETUAL",
                    "deliveryDate": 4133404800000,
                    "onboardDate": 1569398400000,
                    "status": "TRADING",
                    "maintMarginPercent": "2.5000",
                    "requiredMarginPercent": "5.0000",
                    "baseAsset": "BTC",
                    "quoteAsset": "USDT",
                    "marginAsset": "USDT",
                    "pricePrecision": 2,
                    "quantityPrecision": 3,
                    "baseAssetPrecision": 8,
                    "quotePrecision": 8,
                    "underlyingType": "COIN",
                    "filters": [],
                    "orderTypes": ["LIMIT", "MARKET"],
                    "timeInForce": ["GTC", "IOC"]
                }
            ]
        }'''
        info = msgspec.json.decode(data, type=FuturesExchangeInfo)
        assert info.timezone == "UTC"
        assert len(info.symbols) == 1
        assert info.symbols[0].symbol == "BTCUSDT"
        assert info.symbols[0].contract_type == "PERPETUAL"
```

**Step 2: Run tests**

Run: `pytest tests/unit/schemas/test_futures_schemas.py -v`
Expected: PASS

**Step 3: Commit**

```bash
git add tests/unit/schemas/test_futures_schemas.py
git commit -m "test: add comprehensive futures schema tests"
```

---

## Task 5: Update Schema Exports

**Files:**
- Modify: `binance/_schemas/__init__.py`

**Step 1: Add futures exports**

```python
# binance/_schemas/__init__.py
"""Schemas package - all typed response structs."""
from binance._schemas.common import BaseStruct
from binance._schemas.spot import (
    ServerTime,
    ExchangeInfo,
    # ... existing spot exports
)
from binance._schemas.futures import (
    FuturesExchangeInfo,
    FuturesKline,
    FuturesOrder,
    FuturesAccount,
    FuturesAsset,
    FuturesBalance,
    AccountPosition,
    PositionRisk,
    MarkPrice,
    FundingRate,
    LeverageResult,
    FuturesTicker24h,
    FuturesMyTrade,
    BatchOrderError,
)

__all__ = [
    "BaseStruct",
    # Spot
    "ServerTime",
    "ExchangeInfo",
    # ... existing
    # Futures
    "FuturesExchangeInfo",
    "FuturesKline",
    "FuturesOrder",
    "FuturesAccount",
    "FuturesAsset",
    "FuturesBalance",
    "AccountPosition",
    "PositionRisk",
    "MarkPrice",
    "FundingRate",
    "LeverageResult",
    "FuturesTicker24h",
    "FuturesMyTrade",
    "BatchOrderError",
]
```

**Step 2: Run import test**

Run: `python -c "from binance._schemas.futures import *; print('OK')"`
Expected: OK

**Step 3: Commit**

```bash
git add binance/_schemas/__init__.py
git commit -m "feat: export futures schemas from _schemas package"
```

---

## Next Steps

Continue with [03-async-client.md](./03-async-client.md) to extend AsyncClient with futures methods.
