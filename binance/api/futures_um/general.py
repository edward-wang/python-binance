"""USDT-M Futures General API endpoints."""
from typing import Any

import msgspec

from binance._core.http import HTTPClient
from binance._schemas.spot import ServerTime  # Reuse ServerTime schema
from binance._schemas.futures import FuturesExchangeInfo

# Pre-compiled decoders
_server_time_decoder = msgspec.json.Decoder(ServerTime)
_exchange_info_decoder = msgspec.json.Decoder(FuturesExchangeInfo)


async def ping(http: HTTPClient) -> dict[str, Any]:
    """Test connectivity to the Futures API.

    Weight: 1

    Returns:
        Empty dict on success
    """
    return await http.request("GET", "/fapi/v1/ping")


async def get_server_time(http: HTTPClient) -> ServerTime:
    """Get current server time.

    Weight: 1

    Returns:
        ServerTime with server_time in milliseconds
    """
    raw = await http.request_raw("GET", "/fapi/v1/time")
    return _server_time_decoder.decode(raw)


async def get_exchange_info(http: HTTPClient) -> FuturesExchangeInfo:
    """Get current exchange trading rules and symbol information.

    Weight: 1

    Returns:
        FuturesExchangeInfo with symbols and rate limits
    """
    raw = await http.request_raw("GET", "/fapi/v1/exchangeInfo")
    return _exchange_info_decoder.decode(raw)
