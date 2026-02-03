"""Binance Python Wrapper

High-performance, async-only Python wrapper for Binance API.
"""

__version__ = "2.0.0-dev"

# WebSocket components (preserved)
from binance.ws.depthcache import (
    DepthCacheManager,
    OptionsDepthCacheManager,
    ThreadedDepthCacheManager,
    FuturesDepthCacheManager,
)
from binance.ws.streams import (
    BinanceSocketManager,
    ThreadedWebsocketManager,
    BinanceSocketType,
)
from binance.ws.keepalive_websocket import KeepAliveWebsocket
from binance.ws.reconnecting_websocket import ReconnectingWebsocket
from binance.ws.constants import *  # noqa

# Exceptions and enums
from binance.exceptions import *  # noqa
from binance.enums import *  # noqa

__all__ = [
    # WebSocket
    "DepthCacheManager",
    "OptionsDepthCacheManager",
    "ThreadedDepthCacheManager",
    "FuturesDepthCacheManager",
    "BinanceSocketManager",
    "ThreadedWebsocketManager",
    "BinanceSocketType",
    "KeepAliveWebsocket",
    "ReconnectingWebsocket",
]
