"""Unit tests for market spot endpoints."""
from unittest.mock import AsyncMock, MagicMock

import pytest

from binance.api.spot import market


@pytest.fixture
def mock_http():
    """Create mock HTTPClient."""
    http = MagicMock()
    http.request = AsyncMock()
    http.request_raw = AsyncMock()
    return http


class TestGetOrderBook:
    """Test get_order_book endpoint."""

    @pytest.mark.asyncio
    async def test_returns_typed_order_book(self, mock_http):
        """Test returns OrderBook schema."""
        mock_http.request_raw.return_value = b'''{
            "lastUpdateId": 123456789,
            "bids": [["50000.00", "1.0"]],
            "asks": [["50001.00", "2.0"]]
        }'''

        result = await market.get_order_book(mock_http, symbol="BTCUSDT")

        from binance._schemas.spot import OrderBook

        assert isinstance(result, OrderBook)
        assert result.last_update_id == 123456789

    @pytest.mark.asyncio
    async def test_limit_param_omitted_when_default(self, mock_http):
        """Test limit=100 is not sent (default)."""
        mock_http.request_raw.return_value = b'{"lastUpdateId": 1, "bids": [], "asks": []}'

        await market.get_order_book(mock_http, symbol="BTCUSDT", limit=100)

        call_args = mock_http.request_raw.call_args
        assert "limit" not in call_args[1].get("params", {})

    @pytest.mark.asyncio
    async def test_limit_param_sent_when_non_default(self, mock_http):
        """Test limit is sent when not default."""
        mock_http.request_raw.return_value = b'{"lastUpdateId": 1, "bids": [], "asks": []}'

        await market.get_order_book(mock_http, symbol="BTCUSDT", limit=50)

        call_args = mock_http.request_raw.call_args
        assert call_args[1]["params"]["limit"] == 50


class TestGetTrades:
    """Test get_trades endpoint."""

    @pytest.mark.asyncio
    async def test_returns_list_of_trades(self, mock_http):
        """Test returns list[Trade]."""
        mock_http.request_raw.return_value = b'''[
            {"id": 1, "price": "50000", "qty": "0.1", "quoteQty": "5000", "time": 1699999999999, "isBuyerMaker": true, "isBestMatch": true}
        ]'''

        result = await market.get_trades(mock_http, symbol="BTCUSDT")

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].id == 1


class TestGetKlines:
    """Test get_klines endpoint."""

    @pytest.mark.asyncio
    async def test_returns_typed_klines(self, mock_http):
        """Test returns list[Kline] with typed fields."""
        mock_http.request.return_value = [
            [1699999999999, "50000.00", "51000.00", "49000.00", "50500.00", "100.5", 1700000003999, "5025000.00", 1500, "60.3", "3015000.00", "0"]
        ]

        result = await market.get_klines(mock_http, symbol="BTCUSDT", interval="1h")

        from binance._schemas.spot import Kline

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Kline)
        assert result[0].open == "50000.00"
        assert result[0].close == "50500.00"
        assert result[0].open_time == 1699999999999


class TestGetTickerPrice:
    """Test get_ticker_price endpoint with variant returns."""

    @pytest.mark.asyncio
    async def test_single_symbol_returns_single_object(self, mock_http):
        """Test single symbol returns TickerPrice."""
        mock_http.request_raw.return_value = b'{"symbol": "BTCUSDT", "price": "50000.00"}'

        result = await market.get_ticker_price(mock_http, symbol="BTCUSDT")

        from binance._schemas.spot import TickerPrice

        assert isinstance(result, TickerPrice)
        assert result.symbol == "BTCUSDT"

    @pytest.mark.asyncio
    async def test_no_symbol_returns_list(self, mock_http):
        """Test no symbol returns list[TickerPrice]."""
        mock_http.request_raw.return_value = b'[{"symbol": "BTCUSDT", "price": "50000.00"}]'

        result = await market.get_ticker_price(mock_http)

        assert isinstance(result, list)
