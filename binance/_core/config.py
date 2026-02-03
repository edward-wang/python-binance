"""URLs and constants for Binance API.

All configuration values are module-level constants for performance.
No runtime configuration - use environment variables or constructor params.
"""
from typing import Literal

# ============ Base URLs ============

BASE_URLS: dict[str, str] = {
    # Spot
    "spot": "https://api.binance.com",
    "spot_testnet": "https://testnet.binance.vision",
    # Futures USDT-Margined
    "futures_um": "https://fapi.binance.com",
    "futures_um_testnet": "https://testnet.binancefuture.com",
    # Futures COIN-Margined
    "futures_cm": "https://dapi.binance.com",
    "futures_cm_testnet": "https://testnet.binancefuture.com",
}

# ============ Request Defaults ============

RECV_WINDOW_DEFAULT: int = 5000  # milliseconds
TIMEOUT_DEFAULT: float = 10.0  # seconds

# ============ Connection Pool Settings ============

POOL_CONNECTIONS: int = 100  # max concurrent connections
POOL_KEEPALIVE: int = 30  # keepalive timeout in seconds
DNS_CACHE_TTL: int = 300  # DNS cache TTL in seconds

# ============ API Types ============

ApiType = Literal["spot", "futures_um", "futures_cm"]


def get_base_url(api_type: ApiType, testnet: bool = False) -> str:
    """Get base URL for the specified API type.

    Args:
        api_type: One of "spot", "futures_um", "futures_cm"
        testnet: Use testnet URL if True

    Returns:
        Base URL string

    Raises:
        KeyError: If api_type is invalid
    """
    key = f"{api_type}_testnet" if testnet else api_type
    return BASE_URLS[key]
