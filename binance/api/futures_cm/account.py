"""COIN-M Futures Account API endpoints."""
from typing import Any

import msgspec

from binance._core.http import HTTPClient
from binance._schemas.futures import (
    FuturesAccount,
    FuturesBalance,
    FuturesMyTrade,
    LeverageResult,
    PositionRisk,
)

# Pre-compiled decoders
_account_decoder = msgspec.json.Decoder(FuturesAccount)
_balance_list_decoder = msgspec.json.Decoder(list[FuturesBalance])
_position_list_decoder = msgspec.json.Decoder(list[PositionRisk])
_leverage_decoder = msgspec.json.Decoder(LeverageResult)
_trade_list_decoder = msgspec.json.Decoder(list[FuturesMyTrade])


async def get_account(http: HTTPClient) -> FuturesAccount:
    """Get current account information.

    Weight: 5
    Requires: Signature

    Note: COIN-M uses /dapi/v1/account (not v2 like USDT-M)

    Returns:
        FuturesAccount with balances and positions
    """
    raw = await http.request_raw("GET", "/dapi/v1/account", signed=True)
    return _account_decoder.decode(raw)


async def get_balance(http: HTTPClient) -> list[FuturesBalance]:
    """Get futures account balance.

    Weight: 5
    Requires: Signature

    Note: COIN-M returns withdrawAvailable instead of maxWithdrawAmount

    Returns:
        List of FuturesBalance objects
    """
    raw = await http.request_raw("GET", "/dapi/v1/balance", signed=True)
    return _balance_list_decoder.decode(raw)


async def get_position_risk(
    http: HTTPClient,
    symbol: str | None = None,
    pair: str | None = None,
) -> list[PositionRisk]:
    """Get current position information.

    Weight: 5
    Requires: Signature

    Args:
        symbol: Trading pair (e.g., "BTCUSD_PERP")
        pair: Underlying pair (e.g., "BTCUSD") - returns all symbols for pair

    Returns:
        List of PositionRisk objects
    """
    params: dict[str, Any] = {}
    if symbol is not None:
        params["symbol"] = symbol
    if pair is not None:
        params["pair"] = pair

    raw = await http.request_raw("GET", "/dapi/v1/positionRisk", signed=True, params=params)
    return _position_list_decoder.decode(raw)


async def set_leverage(
    http: HTTPClient,
    symbol: str,
    leverage: int,
) -> LeverageResult:
    """Change user's initial leverage.

    Weight: 1
    Requires: Signature

    Note: COIN-M returns maxQty instead of maxNotionalValue

    Args:
        symbol: Trading pair
        leverage: Target leverage (1-125)

    Returns:
        LeverageResult with new leverage and max qty
    """
    params: dict[str, Any] = {
        "symbol": symbol,
        "leverage": leverage,
    }
    raw = await http.request_raw("POST", "/dapi/v1/leverage", signed=True, params=params)
    return _leverage_decoder.decode(raw)


async def set_margin_type(
    http: HTTPClient,
    symbol: str,
    margin_type: str,
) -> dict[str, Any]:
    """Change margin type (ISOLATED/CROSSED).

    Weight: 1
    Requires: Signature

    Args:
        symbol: Trading pair
        margin_type: ISOLATED or CROSSED

    Returns:
        Success response
    """
    params: dict[str, Any] = {
        "symbol": symbol,
        "marginType": margin_type,
    }
    return await http.request("POST", "/dapi/v1/marginType", signed=True, params=params)


async def get_my_trades(
    http: HTTPClient,
    symbol: str | None = None,
    pair: str | None = None,
    order_id: int | None = None,
    start_time: int | None = None,
    end_time: int | None = None,
    from_id: int | None = None,
    limit: int = 500,
) -> list[FuturesMyTrade]:
    """Get trades for a specific account and symbol.

    Weight: 5
    Requires: Signature

    Note: COIN-M supports both symbol and pair parameters

    Args:
        symbol: Trading pair (e.g., "BTCUSD_PERP")
        pair: Underlying pair (e.g., "BTCUSD") - returns trades for all symbols

    Returns:
        List of FuturesMyTrade objects
    """
    params: dict[str, Any] = {}
    if symbol is not None:
        params["symbol"] = symbol
    if pair is not None:
        params["pair"] = pair
    if order_id is not None:
        params["orderId"] = order_id
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if from_id is not None:
        params["fromId"] = from_id
    if limit != 500:
        params["limit"] = limit

    raw = await http.request_raw("GET", "/dapi/v1/userTrades", signed=True, params=params)
    return _trade_list_decoder.decode(raw)
