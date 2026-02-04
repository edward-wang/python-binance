"""Unit tests for general spot endpoints."""
from unittest.mock import AsyncMock, MagicMock

import pytest

from binance.api.spot import general


@pytest.fixture
def mock_http():
    """Create mock HTTPClient."""
    http = MagicMock()
    http.request = AsyncMock()
    http.request_raw = AsyncMock()
    return http


class TestPing:
    """Test ping endpoint."""

    @pytest.mark.asyncio
    async def test_ping_calls_correct_endpoint(self, mock_http):
        """Test ping makes correct request."""
        mock_http.request.return_value = {}

        result = await general.ping(mock_http)

        mock_http.request.assert_called_once_with("GET", "/api/v3/ping")
        assert result == {}


class TestGetServerTime:
    """Test get_server_time endpoint."""

    @pytest.mark.asyncio
    async def test_returns_typed_server_time(self, mock_http):
        """Test returns ServerTime schema."""
        mock_http.request_raw.return_value = b'{"serverTime": 1699999999999}'

        result = await general.get_server_time(mock_http)

        from binance._schemas.spot import ServerTime

        assert isinstance(result, ServerTime)
        assert result.server_time == 1699999999999


class TestGetExchangeInfo:
    """Test get_exchange_info endpoint."""

    @pytest.mark.asyncio
    async def test_with_symbol_param(self, mock_http):
        """Test symbol parameter is passed correctly."""
        mock_http.request_raw.return_value = b'{"timezone": "UTC", "serverTime": 1, "rateLimits": [], "symbols": []}'

        await general.get_exchange_info(mock_http, symbol="BTCUSDT")

        mock_http.request_raw.assert_called_once()
        call_args = mock_http.request_raw.call_args
        assert call_args[1]["params"]["symbol"] == "BTCUSDT"

    @pytest.mark.asyncio
    async def test_without_params(self, mock_http):
        """Test no params when none specified."""
        mock_http.request_raw.return_value = b'{"timezone": "UTC", "serverTime": 1, "rateLimits": [], "symbols": []}'

        await general.get_exchange_info(mock_http)

        call_args = mock_http.request_raw.call_args
        assert call_args[1].get("params", {}) == {}
