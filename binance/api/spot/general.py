"""Spot General API endpoints.

Generated from OpenAPI specs. Do not edit manually.
"""
from typing import Any

import msgspec

from binance._core.http import HTTPClient
from binance._schemas.spot import ExchangeInfo, ServerTime

# Pre-compiled decoders for performance
_server_time_decoder = msgspec.json.Decoder(ServerTime)
_exchange_info_decoder = msgspec.json.Decoder(ExchangeInfo)


async def ping(http: HTTPClient) -> dict[str, Any]:
    """Test connectivity to the Rest API.

    Weight: 1

    Returns:
        Empty dict on success
    """
    return await http.request("GET", "/api/v3/ping")


async def get_server_time(http: HTTPClient) -> ServerTime:
    """Test connectivity and get current server time.

    Weight: 1

    Returns:
        ServerTime with server_time field in milliseconds
    """
    raw = await http.request_raw("GET", "/api/v3/time")
    return _server_time_decoder.decode(raw)


async def get_exchange_info(
    http: HTTPClient,
    symbol: str | None = None,
    symbols: list[str] | None = None,
    permissions: list[str] | None = None,
) -> ExchangeInfo:
    """Get current exchange trading rules and symbol information.

    Weight: 20

    Args:
        symbol: Trading pair (e.g., "BTCUSDT")
        symbols: List of trading pairs
        permissions: Filter by permissions

    Returns:
        ExchangeInfo with symbols and rate limits
    """
    params: dict[str, Any] = {}
    if symbol is not None:
        params["symbol"] = symbol
    if symbols is not None:
        params["symbols"] = symbols
    if permissions is not None:
        params["permissions"] = permissions
    raw = await http.request_raw("GET", "/api/v3/exchangeInfo", params=params)
    return _exchange_info_decoder.decode(raw)
