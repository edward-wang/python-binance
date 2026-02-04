"""Spot Market Data API endpoints.

Generated from OpenAPI specs. Do not edit manually.
"""
from typing import Any

import msgspec

from binance._core.http import HTTPClient
from binance._schemas.spot import (
    AggTrade,
    AvgPrice,
    BookTicker,
    Kline,
    OrderBook,
    Ticker24h,
    TickerPrice,
    Trade,
)

# Pre-compiled decoders for performance
_order_book_decoder = msgspec.json.Decoder(OrderBook)
_trade_list_decoder = msgspec.json.Decoder(list[Trade])
_agg_trade_list_decoder = msgspec.json.Decoder(list[AggTrade])
_avg_price_decoder = msgspec.json.Decoder(AvgPrice)
_ticker_24h_decoder = msgspec.json.Decoder(Ticker24h)
_ticker_24h_list_decoder = msgspec.json.Decoder(list[Ticker24h])
_ticker_price_decoder = msgspec.json.Decoder(TickerPrice)
_ticker_price_list_decoder = msgspec.json.Decoder(list[TickerPrice])
_book_ticker_decoder = msgspec.json.Decoder(BookTicker)
_book_ticker_list_decoder = msgspec.json.Decoder(list[BookTicker])


async def get_order_book(
    http: HTTPClient,
    symbol: str,
    limit: int = 100,
) -> OrderBook:
    """Get order book depth.

    Weight: Adjusted based on limit (5-50: 5, 100: 10, 500: 50, 1000: 100, 5000: 500)

    Args:
        symbol: Trading pair (e.g., "BTCUSDT")
        limit: Depth limit (default 100, max 5000)

    Returns:
        OrderBook with bids and asks
    """
    params: dict[str, Any] = {"symbol": symbol}
    if limit != 100:
        params["limit"] = limit
    raw = await http.request_raw("GET", "/api/v3/depth", params=params)
    return _order_book_decoder.decode(raw)


async def get_trades(
    http: HTTPClient,
    symbol: str,
    limit: int = 500,
) -> list[Trade]:
    """Get recent trades.

    Weight: 10

    Args:
        symbol: Trading pair
        limit: Number of trades (default 500, max 1000)

    Returns:
        List of Trade objects
    """
    params: dict[str, Any] = {"symbol": symbol}
    if limit != 500:
        params["limit"] = limit
    raw = await http.request_raw("GET", "/api/v3/trades", params=params)
    return _trade_list_decoder.decode(raw)


async def get_agg_trades(
    http: HTTPClient,
    symbol: str,
    from_id: int | None = None,
    start_time: int | None = None,
    end_time: int | None = None,
    limit: int = 500,
) -> list[AggTrade]:
    """Get compressed, aggregate trades.

    Weight: 2

    Args:
        symbol: Trading pair
        from_id: Trade ID to get aggregate trades from
        start_time: Start time in milliseconds
        end_time: End time in milliseconds
        limit: Number of trades (default 500, max 1000)

    Returns:
        List of AggTrade objects
    """
    params: dict[str, Any] = {"symbol": symbol}
    if from_id is not None:
        params["fromId"] = from_id
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if limit != 500:
        params["limit"] = limit
    raw = await http.request_raw("GET", "/api/v3/aggTrades", params=params)
    return _agg_trade_list_decoder.decode(raw)


async def get_klines(
    http: HTTPClient,
    symbol: str,
    interval: str,
    start_time: int | None = None,
    end_time: int | None = None,
    limit: int = 500,
) -> list[Kline]:
    """Get Kline/candlestick bars for a symbol.

    Returns typed Kline objects with named fields for AI-friendliness.

    Weight: 2

    Args:
        symbol: Trading pair (e.g., "BTCUSDT")
        interval: Kline interval (1m, 5m, 15m, 1h, 4h, 1d, etc.)
        start_time: Start time in milliseconds
        end_time: End time in milliseconds
        limit: Number of klines (max 1000, default 500)

    Returns:
        List of Kline objects with open, high, low, close, volume, etc.
    """
    params: dict[str, Any] = {"symbol": symbol, "interval": interval}
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if limit != 500:
        params["limit"] = limit
    raw = await http.request("GET", "/api/v3/klines", params=params)
    return [Kline.from_raw(k) for k in raw]


async def get_avg_price(http: HTTPClient, symbol: str) -> AvgPrice:
    """Get current average price for a symbol.

    Weight: 2

    Args:
        symbol: Trading pair

    Returns:
        AvgPrice with mins (interval) and price
    """
    params: dict[str, Any] = {"symbol": symbol}
    raw = await http.request_raw("GET", "/api/v3/avgPrice", params=params)
    return _avg_price_decoder.decode(raw)


async def get_ticker_24h(
    http: HTTPClient,
    symbol: str | None = None,
    symbols: list[str] | None = None,
) -> Ticker24h | list[Ticker24h]:
    """Get 24hr ticker price change statistics.

    Weight: 2 for single symbol, 80 for all symbols

    Args:
        symbol: Single trading pair
        symbols: Multiple trading pairs

    Returns:
        Single Ticker24h if symbol specified, else list
    """
    params: dict[str, Any] = {}
    if symbol is not None:
        params["symbol"] = symbol
    if symbols is not None:
        params["symbols"] = symbols

    raw = await http.request_raw("GET", "/api/v3/ticker/24hr", params=params)

    if symbol is not None:
        return _ticker_24h_decoder.decode(raw)
    return _ticker_24h_list_decoder.decode(raw)


async def get_ticker_price(
    http: HTTPClient,
    symbol: str | None = None,
    symbols: list[str] | None = None,
) -> TickerPrice | list[TickerPrice]:
    """Get symbol price ticker.

    Weight: 2 for single, 4 for all

    Args:
        symbol: Single trading pair
        symbols: Multiple trading pairs

    Returns:
        Single TickerPrice if symbol specified, else list
    """
    params: dict[str, Any] = {}
    if symbol is not None:
        params["symbol"] = symbol
    if symbols is not None:
        params["symbols"] = symbols

    raw = await http.request_raw("GET", "/api/v3/ticker/price", params=params)

    if symbol is not None:
        return _ticker_price_decoder.decode(raw)
    return _ticker_price_list_decoder.decode(raw)


async def get_book_ticker(
    http: HTTPClient,
    symbol: str | None = None,
    symbols: list[str] | None = None,
) -> BookTicker | list[BookTicker]:
    """Get best price/qty on the order book.

    Weight: 2 for single, 4 for all

    Args:
        symbol: Single trading pair
        symbols: Multiple trading pairs

    Returns:
        Single BookTicker if symbol specified, else list
    """
    params: dict[str, Any] = {}
    if symbol is not None:
        params["symbol"] = symbol
    if symbols is not None:
        params["symbols"] = symbols

    raw = await http.request_raw("GET", "/api/v3/ticker/bookTicker", params=params)

    if symbol is not None:
        return _book_ticker_decoder.decode(raw)
    return _book_ticker_list_decoder.decode(raw)
