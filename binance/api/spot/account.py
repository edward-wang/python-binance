"""Spot Account API endpoints.

Generated from OpenAPI specs. Do not edit manually.
"""
from typing import Any

import msgspec

from binance._core.http import HTTPClient
from binance._schemas.spot import Account, MyTrade

# Pre-compiled decoders for performance
_account_decoder = msgspec.json.Decoder(Account)
_my_trade_list_decoder = msgspec.json.Decoder(list[MyTrade])


async def get_account(http: HTTPClient) -> Account:
    """Get current account information.

    Weight: 20
    Requires: Signature (signed=True)

    Returns:
        Account with balances and permissions
    """
    raw = await http.request_raw("GET", "/api/v3/account", signed=True)
    return _account_decoder.decode(raw)


async def get_my_trades(
    http: HTTPClient,
    symbol: str,
    order_id: int | None = None,
    start_time: int | None = None,
    end_time: int | None = None,
    from_id: int | None = None,
    limit: int = 500,
) -> list[MyTrade]:
    """Get trades for a specific account and symbol.

    Weight: 20
    Requires: Signature (signed=True)

    Args:
        symbol: Trading pair
        order_id: Only trades for this order
        start_time: Start time in milliseconds
        end_time: End time in milliseconds
        from_id: Trade ID to start from
        limit: Max results (default 500, max 1000)

    Returns:
        List of MyTrade
    """
    params: dict[str, Any] = {"symbol": symbol}
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

    raw = await http.request_raw("GET", "/api/v3/myTrades", signed=True, params=params)
    return _my_trade_list_decoder.decode(raw)
