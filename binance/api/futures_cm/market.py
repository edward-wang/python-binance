"""COIN-M Futures Market Data API endpoints."""
from typing import Any

import msgspec

from binance._core.http import HTTPClient
from binance._schemas.spot import OrderBook, Trade, AggTrade, TickerPrice, BookTicker
from binance._schemas.futures import (
    FuturesKline,
    MarkPrice,
    FundingRate,
    FuturesTicker24h,
)

# Pre-compiled decoders
_order_book_decoder = msgspec.json.Decoder(OrderBook)
_trade_list_decoder = msgspec.json.Decoder(list[Trade])
_agg_trade_list_decoder = msgspec.json.Decoder(list[AggTrade])
_mark_price_decoder = msgspec.json.Decoder(MarkPrice)
_mark_price_list_decoder = msgspec.json.Decoder(list[MarkPrice])
_funding_rate_decoder = msgspec.json.Decoder(list[FundingRate])
_ticker_24h_decoder = msgspec.json.Decoder(FuturesTicker24h)
_ticker_24h_list_decoder = msgspec.json.Decoder(list[FuturesTicker24h])
_ticker_price_decoder = msgspec.json.Decoder(TickerPrice)
_ticker_price_list_decoder = msgspec.json.Decoder(list[TickerPrice])
_book_ticker_decoder = msgspec.json.Decoder(BookTicker)
_book_ticker_list_decoder = msgspec.json.Decoder(list[BookTicker])


async def get_order_book(
    http: HTTPClient,
    symbol: str,
    limit: int = 500,
) -> OrderBook:
    """Get order book depth.

    Weight: 5-20 depending on limit

    Args:
        symbol: Trading pair (e.g., "BTCUSD_PERP")
        limit: Depth limit (5, 10, 20, 50, 100, 500, 1000)

    Returns:
        OrderBook with bids and asks
    """
    params: dict[str, Any] = {"symbol": symbol}
    if limit != 500:
        params["limit"] = limit
    raw = await http.request_raw("GET", "/dapi/v1/depth", params=params)
    return _order_book_decoder.decode(raw)


async def get_trades(
    http: HTTPClient,
    symbol: str,
    limit: int = 500,
) -> list[Trade]:
    """Get recent trades.

    Weight: 5

    Args:
        symbol: Trading pair
        limit: Number of trades (max 1000)

    Returns:
        List of Trade objects
    """
    params: dict[str, Any] = {"symbol": symbol}
    if limit != 500:
        params["limit"] = limit
    raw = await http.request_raw("GET", "/dapi/v1/trades", params=params)
    return _trade_list_decoder.decode(raw)


async def get_agg_trades(
    http: HTTPClient,
    symbol: str,
    from_id: int | None = None,
    start_time: int | None = None,
    end_time: int | None = None,
    limit: int = 500,
) -> list[AggTrade]:
    """Get aggregated trades.

    Weight: 20

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
    raw = await http.request_raw("GET", "/dapi/v1/aggTrades", params=params)
    return _agg_trade_list_decoder.decode(raw)


async def get_klines(
    http: HTTPClient,
    symbol: str,
    interval: str,
    start_time: int | None = None,
    end_time: int | None = None,
    limit: int = 500,
) -> list[FuturesKline]:
    """Get kline/candlestick bars.

    Weight: 5

    Args:
        symbol: Trading pair (e.g., "BTCUSD_PERP")
        interval: Kline interval (1m, 5m, 15m, 1h, 4h, 1d, etc.)
        start_time: Start time in milliseconds
        end_time: End time in milliseconds
        limit: Number of klines (max 1500)

    Returns:
        List of FuturesKline objects with typed fields
    """
    params: dict[str, Any] = {"symbol": symbol, "interval": interval}
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if limit != 500:
        params["limit"] = limit
    raw = await http.request("GET", "/dapi/v1/klines", params=params)
    return [FuturesKline.from_raw(k) for k in raw]


async def get_continuous_klines(
    http: HTTPClient,
    pair: str,
    contract_type: str,
    interval: str,
    start_time: int | None = None,
    end_time: int | None = None,
    limit: int = 500,
) -> list[FuturesKline]:
    """Get continuous contract klines.

    Weight: 5

    Args:
        pair: Trading pair (e.g., "BTCUSD")
        contract_type: PERPETUAL, CURRENT_QUARTER, NEXT_QUARTER
        interval: Kline interval

    Returns:
        List of FuturesKline objects
    """
    params: dict[str, Any] = {
        "pair": pair,
        "contractType": contract_type,
        "interval": interval,
    }
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if limit != 500:
        params["limit"] = limit
    raw = await http.request("GET", "/dapi/v1/continuousKlines", params=params)
    return [FuturesKline.from_raw(k) for k in raw]


async def get_mark_price(
    http: HTTPClient,
    symbol: str | None = None,
) -> MarkPrice | list[MarkPrice]:
    """Get mark price and funding rate.

    Weight: 1

    Args:
        symbol: Trading pair (returns single) or None (returns all)

    Returns:
        MarkPrice if symbol specified, else list[MarkPrice]
    """
    params: dict[str, Any] = {}
    if symbol is not None:
        params["symbol"] = symbol
    raw = await http.request_raw("GET", "/dapi/v1/premiumIndex", params=params)
    if symbol is not None:
        return _mark_price_decoder.decode(raw)
    return _mark_price_list_decoder.decode(raw)


async def get_funding_rate(
    http: HTTPClient,
    symbol: str,
    start_time: int | None = None,
    end_time: int | None = None,
    limit: int = 100,
) -> list[FundingRate]:
    """Get funding rate history.

    Weight: 1

    Args:
        symbol: Trading pair
        start_time: Start time in ms
        end_time: End time in ms
        limit: Number of results (max 1000)

    Returns:
        List of FundingRate objects
    """
    params: dict[str, Any] = {"symbol": symbol}
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if limit != 100:
        params["limit"] = limit
    raw = await http.request_raw("GET", "/dapi/v1/fundingRate", params=params)
    return _funding_rate_decoder.decode(raw)


async def get_ticker_24h(
    http: HTTPClient,
    symbol: str | None = None,
) -> FuturesTicker24h | list[FuturesTicker24h]:
    """Get 24hr ticker price change statistics.

    Weight: 1-40 depending on parameters

    Returns:
        FuturesTicker24h if symbol specified, else list[FuturesTicker24h]
    """
    params: dict[str, Any] = {}
    if symbol is not None:
        params["symbol"] = symbol
    raw = await http.request_raw("GET", "/dapi/v1/ticker/24hr", params=params)
    if symbol is not None:
        return _ticker_24h_decoder.decode(raw)
    return _ticker_24h_list_decoder.decode(raw)


async def get_ticker_price(
    http: HTTPClient,
    symbol: str | None = None,
) -> TickerPrice | list[TickerPrice]:
    """Get symbol price ticker.

    Weight: 1-2

    Returns:
        TickerPrice if symbol specified, else list[TickerPrice]
    """
    params: dict[str, Any] = {}
    if symbol is not None:
        params["symbol"] = symbol
    raw = await http.request_raw("GET", "/dapi/v1/ticker/price", params=params)
    if symbol is not None:
        return _ticker_price_decoder.decode(raw)
    return _ticker_price_list_decoder.decode(raw)


async def get_book_ticker(
    http: HTTPClient,
    symbol: str | None = None,
) -> BookTicker | list[BookTicker]:
    """Get best bid/ask price.

    Weight: 1-2

    Returns:
        BookTicker if symbol specified, else list[BookTicker]
    """
    params: dict[str, Any] = {}
    if symbol is not None:
        params["symbol"] = symbol
    raw = await http.request_raw("GET", "/dapi/v1/ticker/bookTicker", params=params)
    if symbol is not None:
        return _book_ticker_decoder.decode(raw)
    return _book_ticker_list_decoder.decode(raw)
