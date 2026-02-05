"""Schema definitions for Binance API.

This package contains msgspec Struct definitions:
- common: Base class, Literals, Constants (hand-written)
- spot: Spot API schemas (generated)
- futures: Futures API schemas (generated)
"""
from binance._schemas.common import BaseStruct
from binance._schemas.spot import (
    ServerTime,
    RateLimit,
    SymbolFilter,
    Symbol,
    ExchangeInfo,
    OrderBook,
    Trade,
    AggTrade,
    Kline,
    AvgPrice,
    TickerPrice,
    Ticker24h,
    BookTicker,
    OrderFill,
    Order,
    QueryOrder,
    CancelOrderResult,
    Balance,
    Account,
    MyTrade,
)
from binance._schemas.futures import (
    FuturesExchangeInfo,
    FuturesSymbol,
    FuturesSymbolFilter,
    FuturesRateLimit,
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
    # Common
    "BaseStruct",
    # Spot
    "ServerTime",
    "RateLimit",
    "SymbolFilter",
    "Symbol",
    "ExchangeInfo",
    "OrderBook",
    "Trade",
    "AggTrade",
    "Kline",
    "AvgPrice",
    "TickerPrice",
    "Ticker24h",
    "BookTicker",
    "OrderFill",
    "Order",
    "QueryOrder",
    "CancelOrderResult",
    "Balance",
    "Account",
    "MyTrade",
    # Futures
    "FuturesExchangeInfo",
    "FuturesSymbol",
    "FuturesSymbolFilter",
    "FuturesRateLimit",
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
