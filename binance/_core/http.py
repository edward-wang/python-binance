"""High-performance async HTTP client.

Features:
- Connection pooling with aiohttp
- orjson for fast JSON parsing
- Auto time sync on -1021 error
- Rate limit header extraction
"""
import aiohttp
import orjson
from typing import Any

from binance._core.config import (
    BASE_URLS,
    POOL_CONNECTIONS,
    POOL_KEEPALIVE,
    DNS_CACHE_TTL,
    TIMEOUT_DEFAULT,
)
from binance._core.context import context
from binance._core.auth import sign_request
from binance._core.exceptions import (
    APIErrorMeta,
    TimestampError,
    raise_for_error,
    ConnectionError,
    TimeoutError,
)


def _parse_int(value: str | None) -> int | None:
    """Parse integer from header value."""
    if value:
        return int(value)
    return None


class HTTPClient:
    """Async HTTP client with connection pooling and auto-retry.

    Usage:
        client = HTTPClient(api_key="...", api_secret="...")
        await client.connect()
        try:
            data = await client.request("GET", "/api/v3/time")
        finally:
            await client.close()

    Or with async context manager:
        async with HTTPClient(...) as client:
            data = await client.request("GET", "/api/v3/time")
    """

    __slots__ = (
        "_api_key",
        "_api_secret",
        "_base_url",
        "_session",
        "_connector",
        "_timeout",
        "_time_sync_path",
    )

    def __init__(
        self,
        api_key: str = "",
        api_secret: str = "",
        testnet: bool = False,
        base_url: str | None = None,
        timeout: float = TIMEOUT_DEFAULT,
        time_sync_path: str | None = "/api/v3/time",
    ) -> None:
        """Initialize HTTP client.

        Args:
            api_key: Binance API key (for authenticated endpoints)
            api_secret: Binance API secret (for signed endpoints)
            testnet: Use testnet URLs if True
            base_url: Override base URL (ignores testnet if set)
            timeout: Request timeout in seconds
            time_sync_path: Path for time sync endpoint. Use:
                - "/api/v3/time" for Spot (default)
                - "/fapi/v1/time" for USDT-M Futures
                - "/dapi/v1/time" for COIN-M Futures
                - None to disable time sync (share offset from another client)
        """
        self._api_key = api_key
        self._api_secret = api_secret
        self._base_url = base_url or BASE_URLS["spot_testnet" if testnet else "spot"]
        self._session: aiohttp.ClientSession | None = None
        self._connector: aiohttp.TCPConnector | None = None
        self._timeout = aiohttp.ClientTimeout(total=timeout)
        self._time_sync_path = time_sync_path

    async def connect(self) -> None:
        """Initialize connection pool and sync server time."""
        self._connector = aiohttp.TCPConnector(
            limit=POOL_CONNECTIONS,
            keepalive_timeout=POOL_KEEPALIVE,
            ttl_dns_cache=DNS_CACHE_TTL,
        )
        self._session = aiohttp.ClientSession(
            connector=self._connector,
            timeout=self._timeout,
            json_serialize=lambda x: orjson.dumps(x).decode(),
        )
        # Conditional time sync - skip if disabled or offset already set
        if self._time_sync_path and not context.has_offset():
            await self._sync_server_time()

    async def close(self) -> None:
        """Close connection pool."""
        if self._session:
            await self._session.close()
        if self._connector:
            await self._connector.close()

    async def __aenter__(self) -> "HTTPClient":
        await self.connect()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    async def _sync_server_time(self) -> None:
        """Fetch server time and update offset."""
        if self._time_sync_path is None:
            return
        data = await self.request("GET", self._time_sync_path, signed=False)
        context.update_offset(data["serverTime"])

    async def request(
        self,
        method: str,
        path: str,
        signed: bool = False,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Execute HTTP request with error handling.

        Args:
            method: HTTP method (GET, POST, DELETE)
            path: API endpoint path
            signed: Whether to sign the request
            params: Request parameters

        Returns:
            Parsed JSON response

        Raises:
            BinanceAPIError: On API error response
            BinanceNetworkError: On connection/timeout errors
        """
        params = dict(params) if params else {}

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
                # Re-sign with updated timestamp
                params = {k: v for k, v in params.items() if k not in ("timestamp", "signature")}
                params = sign_request(params, self._api_secret)
            return await self._do_request(method, url, params, headers)

    async def _do_request(
        self,
        method: str,
        url: str,
        params: dict[str, Any],
        headers: dict[str, str],
    ) -> dict[str, Any]:
        """Execute single HTTP request.

        Args:
            method: HTTP method
            url: Full URL
            params: Request parameters
            headers: Request headers

        Returns:
            Parsed JSON response
        """
        if self._session is None:
            raise RuntimeError("HTTPClient not connected. Call connect() first.")

        try:
            async with self._session.request(
                method,
                url,
                params=params if method == "GET" else None,
                data=params if method != "GET" else None,
                headers=headers,
            ) as response:
                raw = await response.read()
                data: dict[str, Any] = orjson.loads(raw) if raw else {}

                # Extract rate limit metadata from headers
                meta = APIErrorMeta(
                    used_weight=_parse_int(response.headers.get("X-MBX-USED-WEIGHT-1M")),
                    used_weight_1m=_parse_int(response.headers.get("X-MBX-USED-WEIGHT-1M")),
                    retry_after=_parse_int(response.headers.get("Retry-After")),
                )

                # Check for errors
                if response.status >= 400 or "code" in data:
                    raise_for_error(response.status, data, meta)

                return data

        except aiohttp.ClientConnectorError as e:
            raise ConnectionError(str(e), method=method, path=url) from e
        except aiohttp.ServerTimeoutError as e:
            raise TimeoutError(str(e), method=method, path=url) from e

    async def request_raw(
        self,
        method: str,
        path: str,
        signed: bool = False,
        params: dict[str, Any] | None = None,
    ) -> bytes:
        """Execute HTTP request and return raw bytes.

        Used by generated code with pre-compiled decoders.

        Args:
            method: HTTP method
            path: API endpoint path
            signed: Whether to sign the request
            params: Request parameters

        Returns:
            Raw response bytes
        """
        params = dict(params) if params else {}

        if signed:
            params = sign_request(params, self._api_secret)

        headers = {}
        if self._api_key:
            headers["X-MBX-APIKEY"] = self._api_key

        url = f"{self._base_url}{path}"

        try:
            return await self._do_request_raw(method, url, params, headers)
        except TimestampError:
            # Self-healing: sync time and retry once
            await self._sync_server_time()
            if signed:
                # Re-sign with updated timestamp
                params = {k: v for k, v in params.items() if k not in ("timestamp", "signature")}
                params = sign_request(params, self._api_secret)
            return await self._do_request_raw(method, url, params, headers)

    async def _do_request_raw(
        self,
        method: str,
        url: str,
        params: dict[str, Any],
        headers: dict[str, str],
    ) -> bytes:
        """Execute single HTTP request returning raw bytes."""
        if self._session is None:
            raise RuntimeError("HTTPClient not connected. Call connect() first.")

        try:
            async with self._session.request(
                method,
                url,
                params=params if method == "GET" else None,
                data=params if method != "GET" else None,
                headers=headers,
            ) as response:
                raw = await response.read()

                # Extract metadata and check errors
                meta = APIErrorMeta(
                    used_weight=_parse_int(response.headers.get("X-MBX-USED-WEIGHT-1M")),
                    retry_after=_parse_int(response.headers.get("Retry-After")),
                )

                if response.status >= 400:
                    data = orjson.loads(raw) if raw else {}
                    raise_for_error(response.status, data, meta)

                return raw

        except aiohttp.ClientConnectorError as e:
            raise ConnectionError(str(e), method=method, path=url) from e
        except aiohttp.ServerTimeoutError as e:
            raise TimeoutError(str(e), method=method, path=url) from e
