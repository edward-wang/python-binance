"""Spot API schemas - Generated from OpenAPI specs.

These schemas are used by api/spot/*.py for typed returns.
Uses BaseStruct with rename="camel" for automatic snake_case ↔ camelCase.
"""
from typing import Annotated

import msgspec

from binance._schemas.common import BaseStruct


# ============ Server/Exchange Info ============


class ServerTime(BaseStruct):
    """Server time from GET /api/v3/time."""

    server_time: Annotated[int, msgspec.Meta(description="Server time in milliseconds")]


class RateLimit(BaseStruct):
    """Rate limit info in exchange info."""

    rate_limit_type: Annotated[str, msgspec.Meta(description="Rate limit type")]
    interval: Annotated[str, msgspec.Meta(description="Interval unit")]
    interval_num: Annotated[int, msgspec.Meta(description="Interval count")]
    limit: Annotated[int, msgspec.Meta(description="Request limit")]


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


class Symbol(BaseStruct):
    """Symbol info in exchange info."""

    symbol: Annotated[str, msgspec.Meta(description="Trading pair")]
    status: Annotated[str, msgspec.Meta(description="Symbol status")]
    base_asset: Annotated[str, msgspec.Meta(description="Base asset")]
    base_asset_precision: Annotated[int, msgspec.Meta(description="Base asset precision")]
    quote_asset: Annotated[str, msgspec.Meta(description="Quote asset")]
    quote_precision: Annotated[int, msgspec.Meta(description="Quote precision")]
    quote_asset_precision: Annotated[int, msgspec.Meta(description="Quote asset precision")]
    order_types: Annotated[list[str], msgspec.Meta(description="Allowed order types")]
    iceberg_allowed: Annotated[bool, msgspec.Meta(description="Iceberg orders allowed")]
    oco_allowed: Annotated[bool, msgspec.Meta(description="OCO orders allowed")]
    quote_order_qty_market_allowed: Annotated[bool, msgspec.Meta(description="Quote qty market orders")]
    allow_trailing_stop: Annotated[bool, msgspec.Meta(description="Trailing stop allowed")]
    is_spot_trading_allowed: Annotated[bool, msgspec.Meta(description="Spot trading allowed")]
    is_margin_trading_allowed: Annotated[bool, msgspec.Meta(description="Margin trading allowed")]
    filters: Annotated[list[SymbolFilter], msgspec.Meta(description="Trading filters")]
    permissions: Annotated[list[str], msgspec.Meta(description="Permissions")]


class ExchangeInfo(BaseStruct):
    """Exchange info from GET /api/v3/exchangeInfo."""

    timezone: Annotated[str, msgspec.Meta(description="Server timezone")]
    server_time: Annotated[int, msgspec.Meta(description="Server time")]
    rate_limits: Annotated[list[RateLimit], msgspec.Meta(description="Rate limits")]
    symbols: Annotated[list[Symbol], msgspec.Meta(description="Trading symbols")]


# ============ Market Data ============


class OrderBook(BaseStruct):
    """Order book from GET /api/v3/depth."""

    last_update_id: Annotated[int, msgspec.Meta(description="Last update ID")]
    bids: Annotated[list[list[str]], msgspec.Meta(description="Bid orders [price, qty]")]
    asks: Annotated[list[list[str]], msgspec.Meta(description="Ask orders [price, qty]")]


class Trade(BaseStruct):
    """Public trade from GET /api/v3/trades."""

    id: Annotated[int, msgspec.Meta(description="Trade ID")]
    price: Annotated[str, msgspec.Meta(description="Price")]
    qty: Annotated[str, msgspec.Meta(description="Quantity")]
    quote_qty: Annotated[str, msgspec.Meta(description="Quote quantity")]
    time: Annotated[int, msgspec.Meta(description="Trade time")]
    is_buyer_maker: Annotated[bool, msgspec.Meta(description="Buyer is maker")]
    is_best_match: Annotated[bool, msgspec.Meta(description="Best match")]


class AggTrade(BaseStruct):
    """Aggregated trade from GET /api/v3/aggTrades."""

    a: Annotated[int, msgspec.Meta(description="Aggregate trade ID")]
    p: Annotated[str, msgspec.Meta(description="Price")]
    q: Annotated[str, msgspec.Meta(description="Quantity")]
    f: Annotated[int, msgspec.Meta(description="First trade ID")]
    l: Annotated[int, msgspec.Meta(description="Last trade ID")]  # noqa: E741
    T: Annotated[int, msgspec.Meta(description="Trade time")]  # noqa: N815
    m: Annotated[bool, msgspec.Meta(description="Buyer is maker")]
    M: Annotated[bool, msgspec.Meta(description="Best match")]  # noqa: N815


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


class AvgPrice(BaseStruct):
    """Average price from GET /api/v3/avgPrice."""

    mins: Annotated[int, msgspec.Meta(description="Price avg interval")]
    price: Annotated[str, msgspec.Meta(description="Average price")]


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


class BookTicker(BaseStruct):
    """Best price/qty from GET /api/v3/ticker/bookTicker."""

    symbol: Annotated[str, msgspec.Meta(description="Trading pair")]
    bid_price: Annotated[str, msgspec.Meta(description="Best bid price")]
    bid_qty: Annotated[str, msgspec.Meta(description="Best bid quantity")]
    ask_price: Annotated[str, msgspec.Meta(description="Best ask price")]
    ask_qty: Annotated[str, msgspec.Meta(description="Best ask quantity")]


# ============ Order/Trade ============


class OrderFill(BaseStruct):
    """Individual fill in FULL order response."""

    price: Annotated[str, msgspec.Meta(description="Fill price")]
    qty: Annotated[str, msgspec.Meta(description="Fill quantity")]
    commission: Annotated[str, msgspec.Meta(description="Commission")]
    commission_asset: Annotated[str, msgspec.Meta(description="Commission asset")]
    trade_id: Annotated[int, msgspec.Meta(description="Trade ID")]


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
    fills: Annotated[list[OrderFill] | None, msgspec.Meta(description="Fill details")] = None


class QueryOrder(BaseStruct):
    """Order from GET /api/v3/order (query order status)."""

    symbol: Annotated[str, msgspec.Meta(description="Trading pair")]
    order_id: Annotated[int, msgspec.Meta(description="Order ID")]
    order_list_id: Annotated[int, msgspec.Meta(description="Order list ID")]
    client_order_id: Annotated[str, msgspec.Meta(description="Client order ID")]
    price: Annotated[str, msgspec.Meta(description="Price")]
    orig_qty: Annotated[str, msgspec.Meta(description="Original quantity")]
    executed_qty: Annotated[str, msgspec.Meta(description="Executed quantity")]
    cummulative_quote_qty: Annotated[str, msgspec.Meta(description="Cumulative quote qty")]
    status: Annotated[str, msgspec.Meta(description="Order status")]
    time_in_force: Annotated[str, msgspec.Meta(description="Time in force")]
    type: Annotated[str, msgspec.Meta(description="Order type")]
    side: Annotated[str, msgspec.Meta(description="Order side")]
    stop_price: Annotated[str | None, msgspec.Meta(description="Stop price")] = None
    iceberg_qty: Annotated[str | None, msgspec.Meta(description="Iceberg quantity")] = None
    time: Annotated[int | None, msgspec.Meta(description="Order time")] = None
    update_time: Annotated[int | None, msgspec.Meta(description="Update time")] = None
    is_working: Annotated[bool | None, msgspec.Meta(description="Is working")] = None
    orig_quote_order_qty: Annotated[str | None, msgspec.Meta(description="Original quote qty")] = None


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


# ============ Account ============


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


class MyTrade(BaseStruct):
    """User's trade from GET /api/v3/myTrades."""

    symbol: Annotated[str, msgspec.Meta(description="Trading pair")]
    id: Annotated[int, msgspec.Meta(description="Trade ID")]
    order_id: Annotated[int, msgspec.Meta(description="Order ID")]
    order_list_id: Annotated[int, msgspec.Meta(description="Order list ID")]
    price: Annotated[str, msgspec.Meta(description="Price")]
    qty: Annotated[str, msgspec.Meta(description="Quantity")]
    quote_qty: Annotated[str, msgspec.Meta(description="Quote quantity")]
    commission: Annotated[str, msgspec.Meta(description="Commission")]
    commission_asset: Annotated[str, msgspec.Meta(description="Commission asset")]
    time: Annotated[int, msgspec.Meta(description="Trade time")]
    is_buyer: Annotated[bool, msgspec.Meta(description="Is buyer")]
    is_maker: Annotated[bool, msgspec.Meta(description="Is maker")]
    is_best_match: Annotated[bool, msgspec.Meta(description="Best match")]
