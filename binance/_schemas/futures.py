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
    last_funding_rate: Annotated[str, msgspec.Meta(description="Last funding rate")]
    next_funding_time: Annotated[int, msgspec.Meta(description="Next funding time in ms")]
    time: Annotated[int, msgspec.Meta(description="Update time")]
    # Optional fields
    estimated_settle_price: Annotated[str | None, msgspec.Meta(description="Estimated settle price")] = None
    interest_rate: Annotated[str | None, msgspec.Meta(description="Interest rate")] = None


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

    # Required fields
    symbol: Annotated[str, msgspec.Meta(description="Trading pair")]
    order_id: Annotated[int, msgspec.Meta(description="Order ID")]
    client_order_id: Annotated[str, msgspec.Meta(description="Client order ID")]
    price: Annotated[str, msgspec.Meta(description="Order price")]
    orig_qty: Annotated[str, msgspec.Meta(description="Original quantity")]
    executed_qty: Annotated[str, msgspec.Meta(description="Executed quantity")]
    status: Annotated[str, msgspec.Meta(description="Order status")]
    time_in_force: Annotated[str, msgspec.Meta(description="Time in force")]
    type: Annotated[str, msgspec.Meta(description="Order type")]
    side: Annotated[str, msgspec.Meta(description="Order side")]
    # Optional fields
    cum_qty: Annotated[str | None, msgspec.Meta(description="Cumulative quantity")] = None
    cum_quote: Annotated[str | None, msgspec.Meta(description="Cumulative quote")] = None
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

    # Required fields
    symbol: Annotated[str, msgspec.Meta(description="Trading pair")]
    position_amt: Annotated[str, msgspec.Meta(description="Position amount")]
    entry_price: Annotated[str, msgspec.Meta(description="Entry price")]
    mark_price: Annotated[str, msgspec.Meta(description="Mark price")]
    # API returns `unRealizedProfit` (capital R) - different from account endpoint
    un_realized_profit: Annotated[str, msgspec.Meta(description="Unrealized profit")]
    liquidation_price: Annotated[str, msgspec.Meta(description="Liquidation price")]
    leverage: Annotated[str, msgspec.Meta(description="Leverage")]
    margin_type: Annotated[str, msgspec.Meta(description="Margin type")]
    position_side: Annotated[str, msgspec.Meta(description="Position side")]
    # Optional fields
    break_even_price: Annotated[str | None, msgspec.Meta(description="Break even price")] = None
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
