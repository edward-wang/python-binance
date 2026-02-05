"""Unit tests for USDT-M futures market endpoints."""
from unittest.mock import AsyncMock, MagicMock

import pytest

from binance.api.futures_um import market


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
        mock_http.request_raw.return_value = b'{"lastUpdateId": 123, "bids": [["50000", "1"]], "asks": [["50001", "2"]]}'

        result = await market.get_order_book(mock_http, symbol="BTCUSDT")

        from binance._schemas.spot import OrderBook

        assert isinstance(result, OrderBook)
        assert result.last_update_id == 123

    @pytest.mark.asyncio
    async def test_passes_limit_param(self, mock_http):
        """Test limit parameter is passed."""
        mock_http.request_raw.return_value = b'{"lastUpdateId": 1, "bids": [], "asks": []}'

        await market.get_order_book(mock_http, symbol="BTCUSDT", limit=100)

        mock_http.request_raw.assert_called_once_with(
            "GET", "/fapi/v1/depth", params={"symbol": "BTCUSDT", "limit": 100}
        )


class TestGetKlines:
    """Test get_klines endpoint."""

    @pytest.mark.asyncio
    async def test_returns_typed_klines(self, mock_http):
        """Test returns list of FuturesKline."""
        mock_http.request.return_value = [
            [
                1699999999999,
                "50000",
                "51000",
                "49000",
                "50500",
                "100",
                1700000003999,
                "5000",
                100,
                "60",
                "3000",
            ]
        ]

        result = await market.get_klines(mock_http, symbol="BTCUSDT", interval="1h")

        from binance._schemas.futures import FuturesKline

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], FuturesKline)
        assert result[0].open == "50000"
        assert result[0].close == "50500"

    @pytest.mark.asyncio
    async def test_passes_time_params(self, mock_http):
        """Test start/end time parameters."""
        mock_http.request.return_value = []

        await market.get_klines(
            mock_http,
            symbol="BTCUSDT",
            interval="1h",
            start_time=1699999000000,
            end_time=1700000000000,
            limit=100,
        )

        mock_http.request.assert_called_once_with(
            "GET",
            "/fapi/v1/klines",
            params={
                "symbol": "BTCUSDT",
                "interval": "1h",
                "startTime": 1699999000000,
                "endTime": 1700000000000,
                "limit": 100,
            },
        )


class TestGetMarkPrice:
    """Test get_mark_price endpoint."""

    @pytest.mark.asyncio
    async def test_single_symbol_returns_single(self, mock_http):
        """Test single symbol returns MarkPrice."""
        mock_http.request_raw.return_value = b'{"symbol": "BTCUSDT", "markPrice": "50000", "indexPrice": "49995", "lastFundingRate": "0.0001", "nextFundingTime": 1700000000000, "time": 1699999999999}'

        result = await market.get_mark_price(mock_http, symbol="BTCUSDT")

        from binance._schemas.futures import MarkPrice

        assert isinstance(result, MarkPrice)
        assert result.symbol == "BTCUSDT"
        assert result.mark_price == "50000"

    @pytest.mark.asyncio
    async def test_no_symbol_returns_list(self, mock_http):
        """Test no symbol returns list."""
        mock_http.request_raw.return_value = b'[{"symbol": "BTCUSDT", "markPrice": "50000", "indexPrice": "49995", "lastFundingRate": "0.0001", "nextFundingTime": 1700000000000, "time": 1699999999999}]'

        result = await market.get_mark_price(mock_http)

        assert isinstance(result, list)
        assert len(result) == 1


class TestGetFundingRate:
    """Test get_funding_rate endpoint."""

    @pytest.mark.asyncio
    async def test_returns_funding_rate_list(self, mock_http):
        """Test returns list of FundingRate."""
        mock_http.request_raw.return_value = b'[{"symbol": "BTCUSDT", "fundingRate": "0.0001", "fundingTime": 1699999999999}]'

        result = await market.get_funding_rate(mock_http, symbol="BTCUSDT")

        from binance._schemas.futures import FundingRate

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], FundingRate)
        assert result[0].funding_rate == "0.0001"


class TestGetTicker24h:
    """Test get_ticker_24h endpoint."""

    @pytest.mark.asyncio
    async def test_single_symbol_returns_single(self, mock_http):
        """Test single symbol returns FuturesTicker24h."""
        mock_http.request_raw.return_value = b'{"symbol": "BTCUSDT", "priceChange": "500", "priceChangePercent": "1", "weightedAvgPrice": "50000", "lastPrice": "50500", "lastQty": "0.1", "openPrice": "50000", "highPrice": "51000", "lowPrice": "49500", "volume": "10000", "quoteVolume": "500000000", "openTime": 1699913599999, "closeTime": 1699999999999, "firstId": 1, "lastId": 100, "count": 100}'

        result = await market.get_ticker_24h(mock_http, symbol="BTCUSDT")

        from binance._schemas.futures import FuturesTicker24h

        assert isinstance(result, FuturesTicker24h)
        assert result.symbol == "BTCUSDT"


class TestGetTrades:
    """Test get_trades endpoint."""

    @pytest.mark.asyncio
    async def test_returns_trade_list(self, mock_http):
        """Test returns list of Trade."""
        mock_http.request_raw.return_value = b'[{"id": 123, "price": "50000", "qty": "0.1", "quoteQty": "5000", "time": 1699999999999, "isBuyerMaker": true}]'

        result = await market.get_trades(mock_http, symbol="BTCUSDT")

        from binance._schemas.spot import Trade

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Trade)


class TestGetBookTicker:
    """Test get_book_ticker endpoint."""

    @pytest.mark.asyncio
    async def test_single_symbol_returns_single(self, mock_http):
        """Test single symbol returns BookTicker."""
        mock_http.request_raw.return_value = b'{"symbol": "BTCUSDT", "bidPrice": "50000", "bidQty": "1", "askPrice": "50001", "askQty": "2"}'

        result = await market.get_book_ticker(mock_http, symbol="BTCUSDT")

        from binance._schemas.spot import BookTicker

        assert isinstance(result, BookTicker)
        assert result.bid_price == "50000"
