"""Exception hierarchy for Binance API errors.

Design goals:
- Semantic errors: Specific exception per error type
- Retryable vs fatal: Clear distinction for middleware
- Metadata preservation: Rate limit info, retry-after available
- Self-healing: Auto-retry on timestamp errors
- Fast: msgspec structs for metadata
"""
from typing import Any

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
    response_data: dict[str, Any],
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
        code = int(response_data["code"])
        message = str(response_data.get("msg", "Unknown error"))
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
