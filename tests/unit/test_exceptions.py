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
