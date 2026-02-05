"""Test HTTPClient time sync configuration."""
import pytest


def test_http_client_default_time_sync_path():
    """Test default time sync path is spot endpoint."""
    from binance._core.http import HTTPClient

    client = HTTPClient()
    assert client._time_sync_path == "/api/v3/time"


def test_http_client_custom_time_sync_path():
    """Test custom time sync path for futures."""
    from binance._core.http import HTTPClient

    client = HTTPClient(time_sync_path="/fapi/v1/time")
    assert client._time_sync_path == "/fapi/v1/time"


def test_http_client_disable_time_sync():
    """Test disabling time sync."""
    from binance._core.http import HTTPClient

    client = HTTPClient(time_sync_path=None)
    assert client._time_sync_path is None


def test_context_has_offset_initially_false():
    """Test has_offset returns False before time sync."""
    from binance._core.context import context

    # Reset offset for test
    original_offset = context.time_offset
    context.time_offset = 0
    try:
        assert context.has_offset() is False
    finally:
        context.time_offset = original_offset


def test_context_has_offset_true_after_sync():
    """Test has_offset returns True after offset is set."""
    from binance._core.context import context

    # Set a non-zero offset to simulate time sync
    original_offset = context.time_offset
    context.time_offset = 100
    try:
        assert context.has_offset() is True
    finally:
        context.time_offset = original_offset
