# Phase 1: Foundation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the hand-written `_core/` infrastructure that generated code depends on.

**Architecture:** Create modular core modules (config, context, auth, http, exceptions, decoders, formatters) plus common schemas. Each module is self-contained, <300 lines, with clear dependencies. TDD approach with pytest-asyncio for async code.

**Tech Stack:** Python 3.11+, msgspec, orjson, aiohttp, uvloop, pytest, pytest-asyncio

---

## Prerequisites

Before starting, ensure dependencies are installed:

```bash
pip install msgspec orjson aiohttp uvloop pytest pytest-asyncio
```

---

## Task 1: Update Project Dependencies

**Requires:** None (independent task)

**Files:**
- Modify: `pyproject.toml`
- Modify: `requirements.txt`

**Step 1: Update pyproject.toml**

Replace contents of `pyproject.toml`:

```toml
[project]
name = "binance-wrapper"
version = "2.0.0-dev"
description = "High-performance async Python wrapper for Binance API"
readme = "README.rst"
license = {text = "MIT"}
requires-python = ">=3.11"
authors = [
    {name = "Sam McHardy"},
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "aiohttp>=3.9",
    "msgspec>=0.18",
    "orjson>=3.9",
    "uvloop>=0.19; sys_platform != 'win32'",
    "pycryptodome>=3.15",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "pytest-timeout>=2.2",
    "ruff>=0.2",
    "mypy>=1.8",
]

[tool.ruff]
preview = true
target-version = "py311"
lint.select = ["E", "F", "I", "N", "W"]
lint.ignore = ["E501"]

[tool.pytest.ini_options]
timeout = 90
timeout_method = "thread"
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"

[tool.mypy]
python_version = "3.11"
strict = true
```

**Step 2: Update requirements.txt**

Replace contents of `requirements.txt`:

```
aiohttp>=3.9
msgspec>=0.18
orjson>=3.9
uvloop>=0.19; sys_platform != 'win32'
pycryptodome>=3.15
```

**Step 3: Commit**

```bash
git add pyproject.toml requirements.txt
git commit -m "build: update dependencies for new architecture

- Add msgspec, orjson, uvloop for performance
- Require Python 3.11+
- Configure pytest-asyncio auto mode
- Add mypy strict mode"
```

---

## Task 2: Create _core Package Structure

**Requires:** Task 1 (dependencies installed)

**Files:**
- Create: `binance/_core/__init__.py`
- Create: `binance/_schemas/__init__.py`

**Step 1: Create _core package**

Create `binance/_core/__init__.py`:

```python
"""Core infrastructure for Binance API client.

This package contains hand-written modules that generated code depends on:
- config: URLs and constants
- context: Global engine state (time offset)
- auth: Request signing (HMAC/RSA/Ed25519)
- http: Async HTTP client with connection pooling
- exceptions: Exception hierarchy with error code mapping
- decoders: Pre-compiled msgspec decoders
- formatters: Price/quantity formatting
"""
```

**Step 2: Create _schemas package**

Create `binance/_schemas/__init__.py`:

```python
"""Schema definitions for Binance API.

This package contains msgspec Struct definitions:
- common: Base class, Literals, Constants (hand-written)
- spot: Spot API schemas (generated)
- futures: Futures API schemas (generated)
"""
```

**Step 3: Commit**

```bash
git add binance/_core/__init__.py binance/_schemas/__init__.py
git commit -m "feat: create _core and _schemas package structure"
```

---

## Task 3: Implement _core/config.py

**Requires:** Task 2 (package structure exists)

**Files:**
- Create: `binance/_core/config.py`
- Create: `tests/unit/__init__.py`
- Create: `tests/unit/test_config.py`

**Step 1: Write the failing test**

Create `tests/unit/__init__.py` (empty file):

```python
"""Unit tests for binance._core modules."""
```

Create `tests/unit/test_config.py`:

```python
"""Tests for _core/config.py"""
import pytest
from binance._core.config import (
    BASE_URLS,
    RECV_WINDOW_DEFAULT,
    TIMEOUT_DEFAULT,
    POOL_CONNECTIONS,
    POOL_KEEPALIVE,
    DNS_CACHE_TTL,
    get_base_url,
)


def test_base_urls_contains_spot():
    assert "spot" in BASE_URLS
    assert BASE_URLS["spot"] == "https://api.binance.com"


def test_base_urls_contains_spot_testnet():
    assert "spot_testnet" in BASE_URLS
    assert BASE_URLS["spot_testnet"] == "https://testnet.binance.vision"


def test_base_urls_contains_futures():
    assert "futures_um" in BASE_URLS
    assert "futures_cm" in BASE_URLS


def test_default_constants():
    assert RECV_WINDOW_DEFAULT == 5000
    assert TIMEOUT_DEFAULT == 10.0
    assert POOL_CONNECTIONS == 100
    assert POOL_KEEPALIVE == 30
    assert DNS_CACHE_TTL == 300


def test_get_base_url_spot():
    assert get_base_url("spot", testnet=False) == "https://api.binance.com"
    assert get_base_url("spot", testnet=True) == "https://testnet.binance.vision"


def test_get_base_url_futures():
    assert get_base_url("futures_um", testnet=False) == "https://fapi.binance.com"
    assert get_base_url("futures_um", testnet=True) == "https://testnet.binancefuture.com"


def test_get_base_url_invalid():
    with pytest.raises(KeyError):
        get_base_url("invalid", testnet=False)
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/unit/test_config.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'binance._core.config'`

**Step 3: Write the implementation**

Create `binance/_core/config.py`:

```python
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
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/unit/test_config.py -v
```

Expected: All tests PASS

**Step 5: Commit**

```bash
git add binance/_core/config.py tests/unit/__init__.py tests/unit/test_config.py
git commit -m "feat(_core): add config module with URLs and constants"
```

---

## Task 4: Implement _core/context.py

**Requires:** Task 2 (package structure exists)

**Files:**
- Create: `binance/_core/context.py`
- Create: `tests/unit/test_context.py`

**Step 1: Write the failing test**

Create `tests/unit/test_context.py`:

```python
"""Tests for _core/context.py"""
import time
import pytest
from binance._core.context import EngineContext, context


def test_engine_context_initial_state():
    ctx = EngineContext()
    assert ctx.time_offset == 0
    assert ctx._last_sync == 0.0


def test_get_timestamp_without_offset():
    ctx = EngineContext()
    before = int(time.time() * 1000)
    ts = ctx.get_timestamp()
    after = int(time.time() * 1000)
    assert before <= ts <= after


def test_get_timestamp_with_offset():
    ctx = EngineContext()
    ctx.time_offset = 1000  # 1 second ahead
    before = int(time.time() * 1000) + 1000
    ts = ctx.get_timestamp()
    after = int(time.time() * 1000) + 1000
    assert before <= ts <= after


def test_update_offset():
    ctx = EngineContext()
    # Simulate server time 500ms ahead
    server_time = int(time.time() * 1000) + 500
    ctx.update_offset(server_time)
    # Offset should be approximately 500ms
    assert 400 <= ctx.time_offset <= 600
    assert ctx._last_sync > 0


def test_needs_sync_initially():
    ctx = EngineContext()
    assert ctx.needs_sync(interval=3600.0) is True


def test_needs_sync_after_update():
    ctx = EngineContext()
    ctx.update_offset(int(time.time() * 1000))
    assert ctx.needs_sync(interval=3600.0) is False


def test_needs_sync_after_interval():
    ctx = EngineContext()
    ctx._last_sync = time.time() - 3700  # 1h 1m 40s ago
    assert ctx.needs_sync(interval=3600.0) is True


def test_global_context_singleton():
    # Global context should be an EngineContext instance
    assert isinstance(context, EngineContext)
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/unit/test_context.py -v
```

Expected: FAIL with `ModuleNotFoundError`

**Step 3: Write the implementation**

Create `binance/_core/context.py`:

```python
"""Global engine context for cross-cutting concerns.

Manages:
- Server time offset (critical for signed requests)
- Future: rate limit state, connection pool references

The global `context` singleton should be used throughout the client
to ensure consistent timestamp calculation across all requests.
"""
import time


class EngineContext:
    """Global context for the Binance client engine.

    Attributes:
        time_offset: Server time minus local time in milliseconds.
                    Added to local time when generating request timestamps.
        _last_sync: Unix timestamp of last time sync.
    """

    __slots__ = ("time_offset", "_last_sync")

    def __init__(self) -> None:
        self.time_offset: int = 0
        self._last_sync: float = 0.0

    def get_timestamp(self) -> int:
        """Get calibrated timestamp in milliseconds.

        All signed requests should use this instead of time.time().
        The offset compensates for clock drift between client and server.

        Returns:
            Current time in milliseconds, adjusted by server offset.
        """
        return int(time.time() * 1000) + self.time_offset

    def update_offset(self, server_time: int) -> None:
        """Update time offset based on server response.

        Should be called:
        - On client initialization
        - After receiving -1021 TimestampError
        - Periodically (e.g., every hour)

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

        Returns:
            True if last sync was longer ago than interval.
        """
        return time.time() - self._last_sync > interval


# Global singleton - used by auth.py and http.py
context = EngineContext()
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/unit/test_context.py -v
```

Expected: All tests PASS

**Step 5: Commit**

```bash
git add binance/_core/context.py tests/unit/test_context.py
git commit -m "feat(_core): add context module with time offset management"
```

---

## Task 5: Implement _core/exceptions.py

**Requires:** Task 2 (package structure exists)

**Files:**
- Create: `binance/_core/exceptions.py`
- Create: `tests/unit/test_exceptions.py`

**Step 1: Write the failing test**

Create `tests/unit/test_exceptions.py`:

```python
"""Tests for _core/exceptions.py"""
import pytest
from binance._core.exceptions import (
    APIErrorMeta,
    BinanceError,
    BinanceNetworkError,
    BinanceAPIError,
    RateLimitError,
    IPBannedError,
    ServerMaintenanceError,
    TimestampError,
    AuthenticationError,
    InvalidAPIKeyError,
    InvalidSignatureError,
    OrderError,
    InsufficientBalanceError,
    OrderNotFoundError,
    ConnectionError,
    TimeoutError,
    ERROR_CODE_MAP,
    HTTP_STATUS_MAP,
    raise_for_error,
    is_retryable,
    get_retry_delay,
)


class TestAPIErrorMeta:
    def test_default_values(self):
        meta = APIErrorMeta()
        assert meta.used_weight is None
        assert meta.retry_after is None

    def test_with_values(self):
        meta = APIErrorMeta(used_weight=100, retry_after=60)
        assert meta.used_weight == 100
        assert meta.retry_after == 60


class TestBinanceNetworkError:
    def test_maybe_executed_for_order_post(self):
        err = BinanceNetworkError("timeout", method="POST", path="/api/v3/order")
        assert err.maybe_executed is True

    def test_maybe_executed_for_get(self):
        err = BinanceNetworkError("timeout", method="GET", path="/api/v3/order")
        assert err.maybe_executed is False

    def test_repr_with_maybe_executed(self):
        err = BinanceNetworkError("timeout", method="POST", path="/api/v3/order")
        assert "MAYBE_EXECUTED=True" in repr(err)


class TestBinanceAPIError:
    def test_message_format(self):
        err = BinanceAPIError(code=-1000, message="Test error")
        assert str(err) == "[-1000] Test error"

    def test_repr_with_meta(self):
        meta = APIErrorMeta(used_weight=100, retry_after=60)
        err = BinanceAPIError(code=-1000, message="Test", meta=meta)
        assert "weight=100" in repr(err)
        assert "retry_after=60s" in repr(err)


class TestRateLimitError:
    def test_is_order_limit_true(self):
        err = RateLimitError(code=-1015, message="Too many orders")
        assert err.is_order_limit is True

    def test_is_order_limit_false(self):
        err = RateLimitError(code=-1003, message="Too many requests")
        assert err.is_order_limit is False


class TestErrorCodeMap:
    def test_timestamp_error_mapped(self):
        assert ERROR_CODE_MAP[-1021] == TimestampError

    def test_rate_limit_errors_mapped(self):
        assert ERROR_CODE_MAP[-1003] == RateLimitError
        assert ERROR_CODE_MAP[-1015] == RateLimitError

    def test_auth_errors_mapped(self):
        assert ERROR_CODE_MAP[-2014] == InvalidAPIKeyError
        assert ERROR_CODE_MAP[-2015] == InvalidSignatureError


class TestHTTPStatusMap:
    def test_429_maps_to_rate_limit(self):
        assert HTTP_STATUS_MAP[429] == RateLimitError

    def test_418_maps_to_ip_banned(self):
        assert HTTP_STATUS_MAP[418] == IPBannedError

    def test_503_maps_to_maintenance(self):
        assert HTTP_STATUS_MAP[503] == ServerMaintenanceError


class TestRaiseForError:
    def test_raises_for_http_418(self):
        with pytest.raises(IPBannedError):
            raise_for_error(418, {}, APIErrorMeta())

    def test_raises_for_error_code(self):
        with pytest.raises(TimestampError):
            raise_for_error(400, {"code": -1021, "msg": "Timestamp error"}, APIErrorMeta())

    def test_raises_generic_for_unknown_code(self):
        with pytest.raises(BinanceAPIError):
            raise_for_error(400, {"code": -9999, "msg": "Unknown"}, APIErrorMeta())

    def test_no_raise_for_success(self):
        # Should not raise for 200 with no error code
        raise_for_error(200, {"result": "ok"}, APIErrorMeta())


class TestIsRetryable:
    def test_network_error_retryable(self):
        err = ConnectionError("failed", method="GET", path="/api/v3/time")
        assert is_retryable(err) is True

    def test_network_error_not_retryable_if_maybe_executed(self):
        err = TimeoutError("timeout", method="POST", path="/api/v3/order")
        assert is_retryable(err) is False

    def test_rate_limit_retryable(self):
        err = RateLimitError(code=-1003, message="Too many requests")
        assert is_retryable(err) is True

    def test_auth_error_not_retryable(self):
        err = InvalidAPIKeyError(code=-2014, message="Invalid API key")
        assert is_retryable(err) is False

    def test_order_error_not_retryable(self):
        err = InsufficientBalanceError(code=-2010, message="No balance")
        assert is_retryable(err) is False


class TestGetRetryDelay:
    def test_rate_limit_with_retry_after(self):
        meta = APIErrorMeta(retry_after=30)
        err = RateLimitError(code=-1003, message="", meta=meta)
        assert get_retry_delay(err) == 30.0

    def test_ip_banned(self):
        err = IPBannedError(code=418, message="")
        assert get_retry_delay(err) == 120.0

    def test_maintenance(self):
        err = ServerMaintenanceError(code=503, message="")
        assert get_retry_delay(err) == 300.0

    def test_network_error(self):
        err = ConnectionError("failed", method="GET", path="/test")
        assert get_retry_delay(err) == 1.0
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/unit/test_exceptions.py -v
```

Expected: FAIL with `ModuleNotFoundError`

**Step 3: Write the implementation**

Create `binance/_core/exceptions.py`:

```python
"""Exception hierarchy for Binance API errors.

Design goals:
- Semantic errors: Specific exception per error type
- Retryable vs fatal: Clear distinction for middleware
- Metadata preservation: Rate limit info, retry-after available
- Self-healing: Auto-retry on timestamp errors
- Fast: msgspec structs for metadata
"""
import msgspec


# ============ Error Metadata ============


class APIErrorMeta(msgspec.Struct, frozen=True):
    """Metadata extracted from error response headers."""

    used_weight: int | None = None
    used_weight_1m: int | None = None
    retry_after: int | None = None
    server_time: int | None = None


# ============ Base Exceptions ============


class BinanceError(Exception):
    """Base exception for all Binance errors."""

    pass


class BinanceNetworkError(BinanceError):
    """Network-level errors (connection, timeout).

    CRITICAL: For POST requests (orders), timeout does NOT mean failure.
    The order may have been executed. Always check order status.
    """

    __slots__ = ("maybe_executed", "method", "path")

    def __init__(self, message: str, method: str = "GET", path: str = "") -> None:
        self.method = method
        self.path = path
        self.maybe_executed = method in ("POST", "DELETE") and "order" in path.lower()
        super().__init__(message)

    def __repr__(self) -> str:
        if self.maybe_executed:
            return f"<{self.__class__.__name__}(method={self.method}, path={self.path}, MAYBE_EXECUTED=True)>"
        return f"<{self.__class__.__name__}(method={self.method}, path={self.path})>"


class ConnectionError(BinanceNetworkError):
    """Failed to connect to Binance."""

    pass


class TimeoutError(BinanceNetworkError):
    """Request timed out - order state unknown if POST."""

    pass


# ============ API Errors ============


class BinanceAPIError(BinanceError):
    """API returned an error response."""

    __slots__ = ("code", "message", "meta")

    def __init__(
        self, code: int, message: str, meta: APIErrorMeta | None = None
    ) -> None:
        self.code = code
        self.message = message
        self.meta = meta or APIErrorMeta()
        super().__init__(f"[{code}] {message}")

    def __repr__(self) -> str:
        """Enhanced repr for logging/debugging."""
        parts = [f"code={self.code}"]
        if self.meta.used_weight:
            parts.append(f"weight={self.meta.used_weight}")
        if self.meta.retry_after:
            parts.append(f"retry_after={self.meta.retry_after}s")
        return f"<{self.__class__.__name__}({', '.join(parts)})>"


# ============ Rate Limiting ============


class RateLimitError(BinanceAPIError):
    """HTTP 429 or error code -1003, -1015.

    Two types:
    - Request weight limit (-1003): Too many requests, retry soon
    - Order rate limit (-1015): Too many orders, more serious
    """

    @property
    def retry_after(self) -> int | None:
        return self.meta.retry_after

    @property
    def used_weight(self) -> int | None:
        return self.meta.used_weight

    @property
    def is_order_limit(self) -> bool:
        """True if this is order frequency limit (-1015)."""
        return self.code == -1015


class IPBannedError(BinanceAPIError):
    """HTTP 418 - IP auto-banned for repeated violations."""

    pass


class ServerMaintenanceError(BinanceAPIError):
    """HTTP 503 - Binance under maintenance."""

    pass


class TimestampError(BinanceAPIError):
    """Error code -1021 - Timestamp outside recvWindow.

    Auto-handled by HTTPClient with time re-sync.
    """

    pass


# ============ Authentication ============


class AuthenticationError(BinanceAPIError):
    """Authentication failed - DO NOT RETRY."""

    pass


class InvalidAPIKeyError(AuthenticationError):
    """Error code -2014 - API key format invalid."""

    pass


class InvalidSignatureError(AuthenticationError):
    """Error code -2015 - Signature verification failed."""

    pass


# ============ Order Errors ============


class OrderError(BinanceAPIError):
    """Order-related errors."""

    pass


class InsufficientBalanceError(OrderError):
    """Error code -2010 - Not enough balance."""

    pass


class OrderNotFoundError(OrderError):
    """Error code -2013 - Order does not exist."""

    pass


class OrderWouldTriggerError(OrderError):
    """Error code -2021 - Stop order would trigger immediately."""

    pass


class InvalidQuantityError(OrderError):
    """Error code -1013 - Invalid quantity."""

    pass


# ============ Invalid Request ============


class InvalidRequestError(BinanceAPIError):
    """Invalid request parameters."""

    pass


class InvalidSymbolError(InvalidRequestError):
    """Error code -1121 - Symbol not found."""

    pass


class InvalidParameterError(InvalidRequestError):
    """Error code -1102 - Mandatory parameter missing."""

    pass


# ============ Error Code Mapping ============


ERROR_CODE_MAP: dict[int, type[BinanceAPIError]] = {
    # Rate limiting
    -1003: RateLimitError,
    -1015: RateLimitError,
    # Timestamp
    -1021: TimestampError,
    # Authentication
    -2014: InvalidAPIKeyError,
    -2015: InvalidSignatureError,
    # Orders
    -2010: InsufficientBalanceError,
    -2013: OrderNotFoundError,
    -2021: OrderWouldTriggerError,
    -1013: InvalidQuantityError,
    # Invalid request
    -1121: InvalidSymbolError,
    -1102: InvalidParameterError,
}

HTTP_STATUS_MAP: dict[int, type[BinanceAPIError]] = {
    418: IPBannedError,
    429: RateLimitError,
    503: ServerMaintenanceError,
}


def raise_for_error(
    status_code: int,
    response_data: dict,
    meta: APIErrorMeta,
) -> None:
    """Raise appropriate exception based on status code and error response.

    Args:
        status_code: HTTP status code
        response_data: Parsed JSON response body
        meta: Error metadata from headers

    Raises:
        BinanceAPIError: Or appropriate subclass based on error code
    """
    if status_code in HTTP_STATUS_MAP:
        exc_class = HTTP_STATUS_MAP[status_code]
        raise exc_class(code=status_code, message=f"HTTP {status_code}", meta=meta)

    if "code" in response_data:
        code = response_data["code"]
        message = response_data.get("msg", "Unknown error")
        exc_class = ERROR_CODE_MAP.get(code, BinanceAPIError)
        raise exc_class(code=code, message=message, meta=meta)


# ============ Retry Helpers ============


def is_retryable(error: BinanceError) -> bool:
    """Check if error is safe to retry.

    Args:
        error: The exception to check

    Returns:
        True if the request can be safely retried
    """
    if isinstance(error, BinanceNetworkError):
        if error.maybe_executed:
            return False  # Must verify order state, not retry
        return True
    if isinstance(error, (RateLimitError, ServerMaintenanceError)):
        return True
    if isinstance(error, AuthenticationError):
        return False
    if isinstance(error, OrderError):
        return False
    return False


def get_retry_delay(error: BinanceError) -> float:
    """Get recommended retry delay in seconds.

    Args:
        error: The exception to get delay for

    Returns:
        Recommended delay in seconds before retrying
    """
    if isinstance(error, RateLimitError) and error.retry_after:
        return float(error.retry_after)
    if isinstance(error, IPBannedError):
        return 120.0  # 2 minutes
    if isinstance(error, ServerMaintenanceError):
        return 300.0  # 5 minutes
    if isinstance(error, BinanceNetworkError):
        return 1.0
    return 0.0
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/unit/test_exceptions.py -v
```

Expected: All tests PASS

**Step 5: Commit**

```bash
git add binance/_core/exceptions.py tests/unit/test_exceptions.py
git commit -m "feat(_core): add exception hierarchy with error code mapping"
```

---

## Task 6: Implement _core/formatters.py

**Requires:** Task 2 (package structure exists)

**Files:**
- Create: `binance/_core/formatters.py`
- Create: `tests/unit/test_formatters.py`

**Step 1: Write the failing test**

Create `tests/unit/test_formatters.py`:

```python
"""Tests for _core/formatters.py"""
import pytest
from binance._core.formatters import format_price, format_quantity, _get_precision


class TestGetPrecision:
    def test_precision_0_01(self):
        assert _get_precision(0.01) == 2

    def test_precision_0_001(self):
        assert _get_precision(0.001) == 3

    def test_precision_0_00001(self):
        assert _get_precision(0.00001) == 5

    def test_precision_1(self):
        assert _get_precision(1.0) == 0

    def test_precision_10(self):
        assert _get_precision(10.0) == 0


class TestFormatPrice:
    def test_format_price_2_decimals(self):
        assert format_price(50000.123456, 0.01) == "50000.12"

    def test_format_price_no_decimals(self):
        assert format_price(50000.99, 1.0) == "50001"

    def test_format_price_rounds_down(self):
        # Python's default rounding, not truncation
        assert format_price(50000.125, 0.01) == "50000.12"

    def test_format_price_rounds_up(self):
        assert format_price(50000.126, 0.01) == "50000.13"


class TestFormatQuantity:
    def test_format_quantity_3_decimals(self):
        assert format_quantity(1.23456789, 0.001) == "1.235"

    def test_format_quantity_5_decimals(self):
        assert format_quantity(0.00123456, 0.00001) == "0.00123"

    def test_format_quantity_no_decimals(self):
        assert format_quantity(100.5, 1.0) == "100"
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/unit/test_formatters.py -v
```

Expected: FAIL with `ModuleNotFoundError`

**Step 3: Write the implementation**

Create `binance/_core/formatters.py`:

```python
"""Price and quantity formatting for order submission.

All calculations use float for HFT performance.
Only format to string at the final order submission step.

Example:
    # Strategy calculation (all float, fast)
    current_price = kline.close  # float
    target_price = current_price * 1.001  # float

    # Only at order submission (format once)
    price_str = format_price(target_price, tick_size=0.01)
    qty_str = format_quantity(0.001234, step_size=0.00001)
"""


def format_price(value: float, tick_size: float) -> str:
    """Format price to match exchange tick size.

    Args:
        value: Price as float
        tick_size: Minimum price increment (e.g., 0.01 for BTCUSDT)

    Returns:
        Price formatted as string with correct precision

    Example:
        format_price(50000.123456, 0.01) → "50000.12"
    """
    precision = _get_precision(tick_size)
    return f"{value:.{precision}f}"


def format_quantity(value: float, step_size: float) -> str:
    """Format quantity to match exchange step size.

    Args:
        value: Quantity as float
        step_size: Minimum quantity increment (e.g., 0.001 for BTCUSDT)

    Returns:
        Quantity formatted as string with correct precision

    Example:
        format_quantity(1.23456789, 0.001) → "1.235"
    """
    precision = _get_precision(step_size)
    return f"{value:.{precision}f}"


def _get_precision(step: float) -> int:
    """Get decimal precision from step size.

    Args:
        step: Step size (tick_size or step_size)

    Returns:
        Number of decimal places
    """
    s = f"{step:.10f}".rstrip("0")
    if "." in s:
        return len(s.split(".")[1])
    return 0
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/unit/test_formatters.py -v
```

Expected: All tests PASS

**Step 5: Commit**

```bash
git add binance/_core/formatters.py tests/unit/test_formatters.py
git commit -m "feat(_core): add formatters for price/quantity string conversion"
```

---

## Task 7: Implement _core/decoders.py

**Requires:** Task 2 (package structure exists)

**Files:**
- Create: `binance/_core/decoders.py`
- Create: `tests/unit/test_decoders.py`

**Step 1: Write the failing test**

Create `tests/unit/test_decoders.py`:

```python
"""Tests for _core/decoders.py"""
import msgspec
import pytest
from binance._core.decoders import get_decoder, clear_decoder_cache


class SimpleStruct(msgspec.Struct):
    name: str
    value: int


class TestGetDecoder:
    def test_returns_decoder(self):
        decoder = get_decoder(SimpleStruct)
        assert isinstance(decoder, msgspec.json.Decoder)

    def test_decoder_can_decode(self):
        decoder = get_decoder(SimpleStruct)
        result = decoder.decode(b'{"name": "test", "value": 42}')
        assert result.name == "test"
        assert result.value == 42

    def test_caches_decoder(self):
        decoder1 = get_decoder(SimpleStruct)
        decoder2 = get_decoder(SimpleStruct)
        assert decoder1 is decoder2

    def test_different_types_different_decoders(self):
        class OtherStruct(msgspec.Struct):
            data: str

        decoder1 = get_decoder(SimpleStruct)
        decoder2 = get_decoder(OtherStruct)
        assert decoder1 is not decoder2

    def test_list_type(self):
        decoder = get_decoder(list[SimpleStruct])
        result = decoder.decode(b'[{"name": "a", "value": 1}, {"name": "b", "value": 2}]')
        assert len(result) == 2
        assert result[0].name == "a"


class TestClearDecoderCache:
    def test_clear_cache(self):
        decoder1 = get_decoder(SimpleStruct)
        clear_decoder_cache()
        decoder2 = get_decoder(SimpleStruct)
        # After clearing, should create new decoder
        assert decoder1 is not decoder2
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/unit/test_decoders.py -v
```

Expected: FAIL with `ModuleNotFoundError`

**Step 3: Write the implementation**

Create `binance/_core/decoders.py`:

```python
"""Pre-compiled msgspec decoders for high-frequency endpoints.

Pre-compiled decoders skip type introspection on each call,
providing 20-30% faster decoding for repeated use.

Usage:
    from binance._core.decoders import get_decoder
    from binance._schemas.spot import Kline

    # Get cached decoder (created on first call)
    decoder = get_decoder(list[Kline])

    # Use in hot path
    klines = decoder.decode(raw_bytes)
"""
import msgspec
from typing import TypeVar

T = TypeVar("T")

# Decoder cache - maps type to pre-compiled decoder
_DECODERS: dict[type, msgspec.json.Decoder] = {}


def get_decoder(schema_type: type[T]) -> msgspec.json.Decoder[T]:
    """Get or create a pre-compiled decoder for the given type.

    The decoder is cached after first creation, so subsequent calls
    with the same type return the same decoder instance.

    Args:
        schema_type: The type to decode into (e.g., Kline, list[Kline])

    Returns:
        A msgspec JSON decoder for the specified type
    """
    if schema_type not in _DECODERS:
        _DECODERS[schema_type] = msgspec.json.Decoder(schema_type)
    return _DECODERS[schema_type]


def clear_decoder_cache() -> None:
    """Clear the decoder cache.

    Primarily useful for testing. In production, decoders should
    remain cached for the lifetime of the application.
    """
    _DECODERS.clear()
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/unit/test_decoders.py -v
```

Expected: All tests PASS

**Step 5: Commit**

```bash
git add binance/_core/decoders.py tests/unit/test_decoders.py
git commit -m "feat(_core): add pre-compiled msgspec decoder cache"
```

---

## Task 8: Implement _core/auth.py

**Requires:** Task 4 (imports `binance._core.context`)

**Files:**
- Create: `binance/_core/auth.py`
- Create: `tests/unit/test_auth.py`

**Step 1: Write the failing test**

Create `tests/unit/test_auth.py`:

```python
"""Tests for _core/auth.py"""
import pytest
from unittest.mock import patch
from binance._core.auth import sign_request, generate_signature


class TestGenerateSignature:
    def test_generates_hex_signature(self):
        params = {"symbol": "BTCUSDT", "side": "BUY", "timestamp": 1234567890}
        secret = "test_secret"
        sig = generate_signature(params, secret)
        # Signature should be 64 character hex string
        assert len(sig) == 64
        assert all(c in "0123456789abcdef" for c in sig)

    def test_same_params_same_signature(self):
        params = {"symbol": "BTCUSDT", "timestamp": 1234567890}
        secret = "test_secret"
        sig1 = generate_signature(params, secret)
        sig2 = generate_signature(params, secret)
        assert sig1 == sig2

    def test_different_params_different_signature(self):
        secret = "test_secret"
        sig1 = generate_signature({"symbol": "BTCUSDT", "timestamp": 1}, secret)
        sig2 = generate_signature({"symbol": "ETHUSDT", "timestamp": 1}, secret)
        assert sig1 != sig2

    def test_params_sorted_for_consistency(self):
        secret = "test_secret"
        # Same params in different order should produce same signature
        sig1 = generate_signature({"b": "2", "a": "1"}, secret)
        sig2 = generate_signature({"a": "1", "b": "2"}, secret)
        assert sig1 == sig2


class TestSignRequest:
    @patch("binance._core.auth.context")
    def test_adds_timestamp(self, mock_context):
        mock_context.get_timestamp.return_value = 1234567890000
        params = {"symbol": "BTCUSDT"}
        secret = "test_secret"

        result = sign_request(params.copy(), secret)

        assert "timestamp" in result
        assert result["timestamp"] == 1234567890000

    @patch("binance._core.auth.context")
    def test_adds_signature(self, mock_context):
        mock_context.get_timestamp.return_value = 1234567890000
        params = {"symbol": "BTCUSDT"}
        secret = "test_secret"

        result = sign_request(params.copy(), secret)

        assert "signature" in result
        assert len(result["signature"]) == 64

    @patch("binance._core.auth.context")
    def test_preserves_original_params(self, mock_context):
        mock_context.get_timestamp.return_value = 1234567890000
        params = {"symbol": "BTCUSDT", "side": "BUY"}
        secret = "test_secret"

        result = sign_request(params.copy(), secret)

        assert result["symbol"] == "BTCUSDT"
        assert result["side"] == "BUY"

    @patch("binance._core.auth.context")
    def test_uses_existing_timestamp_if_provided(self, mock_context):
        mock_context.get_timestamp.return_value = 9999999999999
        params = {"symbol": "BTCUSDT", "timestamp": 1234567890000}
        secret = "test_secret"

        result = sign_request(params.copy(), secret)

        # Should use provided timestamp, not context
        assert result["timestamp"] == 1234567890000
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/unit/test_auth.py -v
```

Expected: FAIL with `ModuleNotFoundError`

**Step 3: Write the implementation**

Create `binance/_core/auth.py`:

```python
"""Signature generation for Binance API authentication.

Supports HMAC-SHA256 signing. RSA and Ed25519 can be added later.

All signed requests require:
- timestamp: Server-calibrated timestamp in milliseconds
- signature: HMAC-SHA256 of query string using API secret
"""
import hmac
import hashlib
from urllib.parse import urlencode

from binance._core.context import context


def generate_signature(params: dict, secret: str) -> str:
    """Generate HMAC-SHA256 signature for request parameters.

    Args:
        params: Request parameters (will be sorted)
        secret: API secret key

    Returns:
        Hex-encoded signature string (64 characters)
    """
    # Sort params for consistent signature
    query_string = urlencode(sorted(params.items()))
    signature = hmac.new(
        secret.encode("utf-8"),
        query_string.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return signature


def sign_request(params: dict, secret: str) -> dict:
    """Add timestamp and signature to request params.

    Uses the global context for calibrated timestamp unless
    timestamp is already provided in params.

    Args:
        params: Request parameters (modified in place)
        secret: API secret key

    Returns:
        Parameters with timestamp and signature added
    """
    # Add timestamp if not already present
    if "timestamp" not in params:
        params["timestamp"] = context.get_timestamp()

    # Generate and add signature
    params["signature"] = generate_signature(params, secret)

    return params
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/unit/test_auth.py -v
```

Expected: All tests PASS

**Step 5: Commit**

```bash
git add binance/_core/auth.py tests/unit/test_auth.py
git commit -m "feat(_core): add HMAC-SHA256 request signing"
```

---

## Task 9: Implement _schemas/common.py

**Requires:** Task 2 (package structure exists)

**Files:**
- Create: `binance/_schemas/common.py`
- Create: `tests/unit/test_schemas_common.py`

**Step 1: Write the failing test**

Create `tests/unit/test_schemas_common.py`:

```python
"""Tests for _schemas/common.py"""
import msgspec
import pytest
from binance._schemas.common import (
    BaseStruct,
    OrderSide,
    ORDER_SIDE_BUY,
    ORDER_SIDE_SELL,
    OrderType,
    ORDER_TYPE_LIMIT,
    ORDER_TYPE_MARKET,
    TimeInForce,
    TIME_IN_FORCE_GTC,
    Interval,
    INTERVAL_1H,
    INTERVAL_1D,
)


class TestBaseStruct:
    def test_rename_camel(self):
        """Test snake_case to camelCase conversion"""

        class TestStruct(BaseStruct):
            open_time: int
            close_time: int

        # Encode should produce camelCase
        obj = TestStruct(open_time=1, close_time=2)
        encoded = msgspec.json.encode(obj)
        assert b"openTime" in encoded
        assert b"closeTime" in encoded
        assert b"open_time" not in encoded

    def test_decode_from_camel(self):
        """Test decoding camelCase to snake_case"""

        class TestStruct(BaseStruct):
            open_time: int
            close_time: int

        data = b'{"openTime": 1, "closeTime": 2}'
        obj = msgspec.json.decode(data, type=TestStruct)
        assert obj.open_time == 1
        assert obj.close_time == 2

    def test_frozen(self):
        """Test immutability"""

        class TestStruct(BaseStruct):
            value: int

        obj = TestStruct(value=1)
        with pytest.raises(AttributeError):
            obj.value = 2

    def test_omit_defaults(self):
        """Test that None/default fields are omitted"""

        class TestStruct(BaseStruct):
            required: str
            optional: str | None = None

        obj = TestStruct(required="test")
        encoded = msgspec.json.encode(obj)
        assert b"optional" not in encoded


class TestOrderSide:
    def test_buy_constant(self):
        assert ORDER_SIDE_BUY == "BUY"

    def test_sell_constant(self):
        assert ORDER_SIDE_SELL == "SELL"

    def test_type_annotation(self):
        # Should accept valid values
        side: OrderSide = "BUY"
        assert side == "BUY"


class TestOrderType:
    def test_limit_constant(self):
        assert ORDER_TYPE_LIMIT == "LIMIT"

    def test_market_constant(self):
        assert ORDER_TYPE_MARKET == "MARKET"


class TestTimeInForce:
    def test_gtc_constant(self):
        assert TIME_IN_FORCE_GTC == "GTC"


class TestInterval:
    def test_1h_constant(self):
        assert INTERVAL_1H == "1h"

    def test_1d_constant(self):
        assert INTERVAL_1D == "1d"
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/unit/test_schemas_common.py -v
```

Expected: FAIL with `ModuleNotFoundError`

**Step 3: Write the implementation**

Create `binance/_schemas/common.py`:

```python
"""Common types shared across all APIs.

This module defines:
- BaseStruct: Base class for all msgspec schemas
- Literal types: Type-safe enums without enum overhead
- Constants: Named values for Literals

Design decisions:
- Literal + Constants pattern for type safety AND performance
- rename="camel" for automatic snake_case ↔ camelCase
- frozen=True for immutability and hashability
- omit_defaults=True for smaller payloads
"""
import msgspec
from typing import Literal


# ============ Base Class ============


class BaseStruct(msgspec.Struct, rename="camel", frozen=True, omit_defaults=True):
    """Base class for all schemas.

    Features:
    - rename="camel": auto-convert snake_case ↔ camelCase
    - frozen=True: immutable, hashable, thread-safe
    - omit_defaults=True: skip None/default fields in serialization
    """

    pass


# ============ Order Side ============

OrderSide = Literal["BUY", "SELL"]

ORDER_SIDE_BUY: OrderSide = "BUY"
ORDER_SIDE_SELL: OrderSide = "SELL"


# ============ Order Type ============

OrderType = Literal[
    "LIMIT",
    "MARKET",
    "STOP_LOSS",
    "STOP_LOSS_LIMIT",
    "TAKE_PROFIT",
    "TAKE_PROFIT_LIMIT",
    "LIMIT_MAKER",
]

ORDER_TYPE_LIMIT: OrderType = "LIMIT"
ORDER_TYPE_MARKET: OrderType = "MARKET"
ORDER_TYPE_STOP_LOSS: OrderType = "STOP_LOSS"
ORDER_TYPE_STOP_LOSS_LIMIT: OrderType = "STOP_LOSS_LIMIT"
ORDER_TYPE_TAKE_PROFIT: OrderType = "TAKE_PROFIT"
ORDER_TYPE_TAKE_PROFIT_LIMIT: OrderType = "TAKE_PROFIT_LIMIT"
ORDER_TYPE_LIMIT_MAKER: OrderType = "LIMIT_MAKER"


# ============ Time In Force ============

TimeInForce = Literal["GTC", "IOC", "FOK"]

TIME_IN_FORCE_GTC: TimeInForce = "GTC"
TIME_IN_FORCE_IOC: TimeInForce = "IOC"
TIME_IN_FORCE_FOK: TimeInForce = "FOK"


# ============ Order Status ============

OrderStatus = Literal[
    "NEW",
    "PARTIALLY_FILLED",
    "FILLED",
    "CANCELED",
    "PENDING_CANCEL",
    "REJECTED",
    "EXPIRED",
]

ORDER_STATUS_NEW: OrderStatus = "NEW"
ORDER_STATUS_PARTIALLY_FILLED: OrderStatus = "PARTIALLY_FILLED"
ORDER_STATUS_FILLED: OrderStatus = "FILLED"
ORDER_STATUS_CANCELED: OrderStatus = "CANCELED"
ORDER_STATUS_REJECTED: OrderStatus = "REJECTED"
ORDER_STATUS_EXPIRED: OrderStatus = "EXPIRED"


# ============ Kline Interval ============

Interval = Literal[
    "1s",
    "1m",
    "3m",
    "5m",
    "15m",
    "30m",
    "1h",
    "2h",
    "4h",
    "6h",
    "8h",
    "12h",
    "1d",
    "3d",
    "1w",
    "1M",
]

INTERVAL_1S: Interval = "1s"
INTERVAL_1M: Interval = "1m"
INTERVAL_3M: Interval = "3m"
INTERVAL_5M: Interval = "5m"
INTERVAL_15M: Interval = "15m"
INTERVAL_30M: Interval = "30m"
INTERVAL_1H: Interval = "1h"
INTERVAL_2H: Interval = "2h"
INTERVAL_4H: Interval = "4h"
INTERVAL_6H: Interval = "6h"
INTERVAL_8H: Interval = "8h"
INTERVAL_12H: Interval = "12h"
INTERVAL_1D: Interval = "1d"
INTERVAL_3D: Interval = "3d"
INTERVAL_1W: Interval = "1w"
INTERVAL_1MONTH: Interval = "1M"
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/unit/test_schemas_common.py -v
```

Expected: All tests PASS

**Step 5: Commit**

```bash
git add binance/_schemas/common.py tests/unit/test_schemas_common.py
git commit -m "feat(_schemas): add common types with Literal + Constants pattern"
```

---

## Task 10: Implement _core/http.py

**Requires:** Tasks 3, 4, 5, 8 (imports config, context, auth, exceptions)

**Files:**
- Create: `binance/_core/http.py`
- Create: `tests/unit/test_http.py`

**Step 1: Write the failing test**

Create `tests/unit/test_http.py`:

```python
"""Tests for _core/http.py"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from binance._core.http import HTTPClient, _parse_int


class TestParseInt:
    def test_parse_valid_int(self):
        assert _parse_int("123") == 123

    def test_parse_none(self):
        assert _parse_int(None) is None

    def test_parse_empty_string(self):
        assert _parse_int("") is None


class TestHTTPClientInit:
    def test_default_values(self):
        client = HTTPClient()
        assert client._api_key == ""
        assert client._api_secret == ""
        assert "api.binance.com" in client._base_url

    def test_testnet_url(self):
        client = HTTPClient(testnet=True)
        assert "testnet" in client._base_url

    def test_custom_base_url(self):
        client = HTTPClient(base_url="https://custom.api.com")
        assert client._base_url == "https://custom.api.com"

    def test_api_credentials(self):
        client = HTTPClient(api_key="key123", api_secret="secret456")
        assert client._api_key == "key123"
        assert client._api_secret == "secret456"


class TestHTTPClientConnection:
    @pytest.mark.asyncio
    async def test_connect_creates_session(self):
        client = HTTPClient()
        with patch.object(client, "_sync_server_time", new_callable=AsyncMock):
            await client.connect()
            assert client._session is not None
            assert client._connector is not None
            await client.close()

    @pytest.mark.asyncio
    async def test_close_cleans_up(self):
        client = HTTPClient()
        with patch.object(client, "_sync_server_time", new_callable=AsyncMock):
            await client.connect()
            session = client._session
            connector = client._connector
            await client.close()
            assert session.closed
            assert connector.closed


class TestHTTPClientRequest:
    @pytest.mark.asyncio
    async def test_request_adds_api_key_header(self):
        client = HTTPClient(api_key="test_key")
        client._session = MagicMock()

        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.read = AsyncMock(return_value=b'{"result": "ok"}')
        mock_response.headers = {}
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock()

        client._session.request = MagicMock(return_value=mock_response)

        await client._do_request("GET", "https://api.binance.com/test", {}, {"X-MBX-APIKEY": "test_key"})

        call_args = client._session.request.call_args
        assert call_args[1]["headers"]["X-MBX-APIKEY"] == "test_key"
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/unit/test_http.py -v
```

Expected: FAIL with `ModuleNotFoundError`

**Step 3: Write the implementation**

Create `binance/_core/http.py`:

```python
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
    )

    def __init__(
        self,
        api_key: str = "",
        api_secret: str = "",
        testnet: bool = False,
        base_url: str | None = None,
        timeout: float = TIMEOUT_DEFAULT,
    ) -> None:
        """Initialize HTTP client.

        Args:
            api_key: Binance API key (for authenticated endpoints)
            api_secret: Binance API secret (for signed endpoints)
            testnet: Use testnet URLs if True
            base_url: Override base URL (ignores testnet if set)
            timeout: Request timeout in seconds
        """
        self._api_key = api_key
        self._api_secret = api_secret
        self._base_url = base_url or BASE_URLS["spot_testnet" if testnet else "spot"]
        self._session: aiohttp.ClientSession | None = None
        self._connector: aiohttp.TCPConnector | None = None
        self._timeout = aiohttp.ClientTimeout(total=timeout)

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
        # Initial time sync
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
        data = await self.request("GET", "/api/v3/time", signed=False)
        context.update_offset(data["serverTime"])

    async def request(
        self,
        method: str,
        path: str,
        signed: bool = False,
        params: dict | None = None,
    ) -> dict:
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
        params: dict,
        headers: dict,
    ) -> dict:
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
                data = orjson.loads(raw) if raw else {}

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
        params: dict | None = None,
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

        if self._session is None:
            raise RuntimeError("HTTPClient not connected. Call connect() first.")

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
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/unit/test_http.py -v
```

Expected: All tests PASS

**Step 5: Commit**

```bash
git add binance/_core/http.py tests/unit/test_http.py
git commit -m "feat(_core): add async HTTP client with connection pooling"
```

---

## Task 11: Run All Tests and Verify

**Requires:** Tasks 1-10 (all modules implemented)

**Step 1: Run full test suite**

```bash
pytest tests/unit/ -v
```

Expected: All tests PASS

**Step 2: Type check**

```bash
mypy binance/_core binance/_schemas --strict
```

Expected: No errors (or only minor ones to fix)

**Step 3: Final commit**

```bash
git add -A
git commit -m "test: verify Phase 1 foundation complete

All _core modules implemented:
- config.py: URLs and constants
- context.py: Time offset management
- exceptions.py: Exception hierarchy
- formatters.py: Price/quantity formatting
- decoders.py: Pre-compiled msgspec decoders
- auth.py: HMAC-SHA256 signing
- http.py: Async HTTP client

All _schemas modules implemented:
- common.py: BaseStruct, Literals, Constants"
```

---

## Verification Checklist

After completing all tasks, verify:

- [ ] `binance/_core/__init__.py` exists
- [ ] `binance/_core/config.py` exists with `get_base_url()`
- [ ] `binance/_core/context.py` exists with `context` singleton
- [ ] `binance/_core/exceptions.py` exists with full hierarchy
- [ ] `binance/_core/formatters.py` exists with `format_price()`, `format_quantity()`
- [ ] `binance/_core/decoders.py` exists with `get_decoder()`
- [ ] `binance/_core/auth.py` exists with `sign_request()`
- [ ] `binance/_core/http.py` exists with `HTTPClient`
- [ ] `binance/_schemas/__init__.py` exists
- [ ] `binance/_schemas/common.py` exists with `BaseStruct` and all Literals
- [ ] All unit tests pass: `pytest tests/unit/ -v`
- [ ] Type check passes: `mypy binance/_core binance/_schemas`

---

## Summary

| Task | Module | Tests | Requires |
|------|--------|-------|----------|
| 1 | pyproject.toml, requirements.txt | - | None |
| 2 | _core/__init__.py, _schemas/__init__.py | - | Task 1 |
| 3 | _core/config.py | test_config.py | Task 2 |
| 4 | _core/context.py | test_context.py | Task 2 |
| 5 | _core/exceptions.py | test_exceptions.py | Task 2 |
| 6 | _core/formatters.py | test_formatters.py | Task 2 |
| 7 | _core/decoders.py | test_decoders.py | Task 2 |
| 8 | _core/auth.py | test_auth.py | Task 4 |
| 9 | _schemas/common.py | test_schemas_common.py | Task 2 |
| 10 | _core/http.py | test_http.py | Tasks 3,4,5,8 |
| 11 | Verification | All tests | Tasks 1-10 |

## Dependency Graph

```
Task 1 (dependencies)
    │
    ▼
Task 2 (package structure)
    │
    ├──► Task 3 (config) ─────────────────┐
    │                                      │
    ├──► Task 4 (context) ──► Task 8 (auth)┼──► Task 10 (http) ──► Task 11 (verify)
    │                                      │
    ├──► Task 5 (exceptions) ─────────────┤
    │                                      │
    ├──► Task 6 (formatters)               │
    │                                      │
    ├──► Task 7 (decoders)                 │
    │                                      │
    └──► Task 9 (schemas/common)           │
```

**Parallelizable:** Tasks 3, 4, 5, 6, 7, 9 can run in parallel after Task 2.
**Sequential:** Task 8 requires Task 4. Task 10 requires Tasks 3, 4, 5, 8.

**Total: 11 tasks, ~1,080 lines of implementation code, ~500 lines of tests**
