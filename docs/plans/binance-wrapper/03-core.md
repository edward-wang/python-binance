# Section 3: Core Infrastructure (`_core/`)

Hand-written foundation that generated code depends on.

## Module Overview

| Module | Purpose | Lines |
|--------|---------|-------|
| `config.py` | URLs, constants | ~100 |
| `context.py` | Time offset, global state | ~80 |
| `auth.py` | HMAC/RSA/Ed25519 signatures | ~150 |
| `http.py` | aiohttp client + connection pool | ~250 |
| `exceptions.py` | Exception hierarchy | ~250 |
| `decoders.py` | Pre-compiled msgspec decoders | ~50 |
| `formatters.py` | Price/quantity formatting | ~50 |

## `_core/config.py`

```python
"""URLs and constants for Binance API."""

# Base URLs
BASE_URLS = {
    "spot": "https://api.binance.com",
    "spot_testnet": "https://testnet.binance.vision",
    "futures_um": "https://fapi.binance.com",
    "futures_um_testnet": "https://testnet.binancefuture.com",
    "futures_cm": "https://dapi.binance.com",
    "futures_cm_testnet": "https://testnet.binancefuture.com",
}

# Default settings
RECV_WINDOW_DEFAULT = 5000
TIMEOUT_DEFAULT = 10.0

# Connection pool settings
POOL_CONNECTIONS = 100
POOL_KEEPALIVE = 30
DNS_CACHE_TTL = 300
```

## `_core/context.py`

Global engine context for cross-cutting concerns.

```python
"""Global engine context for cross-cutting concerns.

Manages:
- Server time offset (critical for signed requests)
- Future: rate limit state, connection pool references
"""
import time

class EngineContext:
    """Global context for the Binance client engine."""
    __slots__ = ("time_offset", "_last_sync")

    def __init__(self):
        # Server time - local time (milliseconds)
        self.time_offset: int = 0
        self._last_sync: float = 0.0

    def get_timestamp(self) -> int:
        """Get calibrated timestamp in milliseconds.

        All signed requests should use this instead of time.time().
        """
        return int(time.time() * 1000) + self.time_offset

    def update_offset(self, server_time: int) -> None:
        """Update time offset based on server response.

        Args:
            server_time: Server time in milliseconds (from /api/v3/time)
        """
        local_time = int(time.time() * 1000)
        self.time_offset = server_time - local_time
        self._last_sync = time.time()

    def needs_sync(self, interval: float = 3600.0) -> bool:
        """Check if time offset needs re-sync.

        Args:
            interval: Sync interval in seconds (default: 1 hour)
        """
        return time.time() - self._last_sync > interval

# Global singleton
context = EngineContext()
```

## `_core/auth.py`

Signature generation using context for timestamp.

```python
"""Signature generation for Binance API authentication."""
import hmac
import hashlib
from urllib.parse import urlencode
from binance._core.context import context

def sign_request(params: dict, secret: str) -> dict:
    """Add timestamp and signature to request params.

    Args:
        params: Request parameters
        secret: API secret key

    Returns:
        Parameters with timestamp and signature added
    """
    params["timestamp"] = context.get_timestamp()

    query_string = urlencode(sorted(params.items()))
    signature = hmac.new(
        secret.encode("utf-8"),
        query_string.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    params["signature"] = signature
    return params

# RSA and Ed25519 signing functions...
```

## `_core/http.py`

High-performance async HTTP client with:
- Connection pooling
- orjson for JSON
- Auto time sync on -1021 error
- Rate limit header extraction

```python
"""High-performance async HTTP client."""
import aiohttp
import orjson
from binance._core.config import BASE_URLS, POOL_CONNECTIONS, POOL_KEEPALIVE
from binance._core.context import context
from binance._core.auth import sign_request
from binance._core.exceptions import raise_for_error, TimestampError, APIErrorMeta

class HTTPClient:
    """Async HTTP client with connection pooling and auto-retry."""

    __slots__ = ("_api_key", "_api_secret", "_base_url", "_session", "_connector")

    def __init__(
        self,
        api_key: str = "",
        api_secret: str = "",
        testnet: bool = False,
        base_url: str | None = None,
    ):
        self._api_key = api_key
        self._api_secret = api_secret
        self._base_url = base_url or BASE_URLS["spot_testnet" if testnet else "spot"]
        self._session: aiohttp.ClientSession | None = None
        self._connector: aiohttp.TCPConnector | None = None

    async def connect(self) -> None:
        """Initialize connection pool and sync server time."""
        self._connector = aiohttp.TCPConnector(
            limit=POOL_CONNECTIONS,
            keepalive_timeout=POOL_KEEPALIVE,
            ttl_dns_cache=300,
        )
        self._session = aiohttp.ClientSession(
            connector=self._connector,
            json_serialize=lambda x: orjson.dumps(x).decode(),
        )
        # Initial time sync
        await self._sync_server_time()

    async def close(self) -> None:
        """Close connection pool."""
        if self._session:
            await self._session.close()
        if self._connector:
            await self._connector.close()

    async def _sync_server_time(self) -> None:
        """Fetch server time and update offset."""
        data = await self._request("GET", "/api/v3/time", signed=False)
        context.update_offset(data["serverTime"])

    async def _request(
        self,
        method: str,
        path: str,
        signed: bool = False,
        params: dict | None = None,
        **kwargs,
    ) -> dict:
        """Execute HTTP request with error handling."""
        params = params or {}

        if signed:
            params = sign_request(params, self._api_secret)

        headers = {}
        if self._api_key:
            headers["X-MBX-APIKEY"] = self._api_key

        url = f"{self._base_url}{path}"

        try:
            return await self._do_request(method, url, params, headers)
        except TimestampError:
            # Self-healing: sync time and retry once
            await self._sync_server_time()
            if signed:
                params = sign_request(params, self._api_secret)
            return await self._do_request(method, url, params, headers)

    async def _do_request(
        self,
        method: str,
        url: str,
        params: dict,
        headers: dict,
    ) -> dict:
        """Execute single HTTP request."""
        async with self._session.request(
            method,
            url,
            params=params if method == "GET" else None,
            data=params if method != "GET" else None,
            headers=headers,
        ) as response:
            raw = await response.read()
            data = orjson.loads(raw) if raw else {}

            # Extract rate limit metadata
            meta = APIErrorMeta(
                used_weight=_parse_int(response.headers.get("X-MBX-USED-WEIGHT-1M")),
                retry_after=_parse_int(response.headers.get("Retry-After")),
            )

            # Check for errors
            if response.status >= 400 or "code" in data:
                raise_for_error(response.status, data, meta)

            return data

def _parse_int(value: str | None) -> int | None:
    """Parse integer from header value."""
    return int(value) if value else None
```

## `_core/decoders.py`

Pre-compiled msgspec decoders for hot paths.

```python
"""Pre-compiled msgspec decoders for high-frequency endpoints."""
import msgspec
from typing import TypeVar

T = TypeVar("T")

# Decoder cache
_DECODERS: dict[type, msgspec.json.Decoder] = {}

def get_decoder(schema_type: type[T]) -> msgspec.json.Decoder[T]:
    """Get or create a pre-compiled decoder for the given type.

    Pre-compiled decoders skip type introspection on each call,
    providing 20-30% faster decoding for repeated use.
    """
    if schema_type not in _DECODERS:
        _DECODERS[schema_type] = msgspec.json.Decoder(schema_type)
    return _DECODERS[schema_type]
```

## `_core/formatters.py`

Price and quantity formatting for order submission.

```python
"""Price and quantity formatting for order submission.

All calculations use float for HFT performance.
Only format to string at the final order submission step.
"""

def format_price(value: float, tick_size: float) -> str:
    """Format price to match exchange tick size.

    Example:
        format_price(50000.123456, 0.01) → "50000.12"
    """
    precision = _get_precision(tick_size)
    return f"{value:.{precision}f}"

def format_quantity(value: float, step_size: float) -> str:
    """Format quantity to match exchange step size.

    Example:
        format_quantity(1.23456789, 0.001) → "1.234"
    """
    precision = _get_precision(step_size)
    return f"{value:.{precision}f}"

def _get_precision(step: float) -> int:
    """Get decimal precision from step size."""
    s = f"{step:.10f}".rstrip('0')
    if '.' in s:
        return len(s.split('.')[1])
    return 0
```
