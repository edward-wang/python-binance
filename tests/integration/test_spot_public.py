"""Integration tests for public Spot API endpoints.

All tests verify typed schema returns, not raw dicts.
"""
import pytest

from binance._schemas.spot import (
    AvgPrice,
    BookTicker,
    ExchangeInfo,
    Kline,
    OrderBook,
    ServerTime,
    Ticker24h,
    TickerPrice,
    Trade,
)


@pytest.mark.asyncio
class TestGeneralEndpoints:
    """Test general public endpoints."""

    async def test_ping(self, public_client):
        """Test ping endpoint returns successfully."""
        result = await public_client.ping()
        assert result == {}

    async def test_get_server_time(self, public_client):
        """Test server time returns typed ServerTime."""
        result = await public_client.get_server_time()

        # Verify typed return
        assert isinstance(result, ServerTime)
        assert result.server_time > 0

    async def test_get_exchange_info(self, public_client):
        """Test exchange info returns typed ExchangeInfo."""
        result = await public_client.get_exchange_info()

        # Verify typed return
        assert isinstance(result, ExchangeInfo)
        assert result.timezone == "UTC"
        assert result.server_time > 0
        assert len(result.symbols) > 0

    async def test_get_exchange_info_single_symbol(self, public_client):
        """Test exchange info for single symbol."""
        result = await public_client.get_exchange_info(symbol="BTCUSDT")

        assert isinstance(result, ExchangeInfo)
        assert len(result.symbols) == 1
        assert result.symbols[0].symbol == "BTCUSDT"


@pytest.mark.asyncio
class TestMarketDataEndpoints:
    """Test market data public endpoints."""

    async def test_get_order_book(self, public_client):
        """Test order book returns typed OrderBook."""
        result = await public_client.get_order_book(symbol="BTCUSDT", limit=5)

        assert isinstance(result, OrderBook)
        assert result.last_update_id > 0
        assert len(result.bids) <= 5
        assert len(result.asks) <= 5

    async def test_get_order_book_structure(self, public_client):
        """Test order book bid/ask structure."""
        result = await public_client.get_order_book(symbol="BTCUSDT", limit=1)

        if result.bids:
            bid = result.bids[0]
            # Verify it's [price, quantity] as strings
            assert len(bid) == 2
            assert isinstance(bid[0], str)
            assert isinstance(bid[1], str)

    async def test_get_trades(self, public_client):
        """Test recent trades returns list of typed Trade."""
        result = await public_client.get_trades(symbol="BTCUSDT", limit=5)

        assert isinstance(result, list)
        assert len(result) <= 5

        if result:
            trade = result[0]
            assert isinstance(trade, Trade)
            assert trade.id > 0
            assert trade.price  # non-empty string
            assert trade.qty

    async def test_get_klines(self, public_client):
        """Test klines returns list of typed Kline."""
        result = await public_client.get_klines(
            symbol="BTCUSDT",
            interval="1h",
            limit=5,
        )

        assert isinstance(result, list)
        assert len(result) <= 5

        if result:
            kline = result[0]
            assert isinstance(kline, Kline)
            assert kline.open_time > 0
            assert kline.open  # non-empty string
            assert kline.close_time > kline.open_time

    async def test_get_avg_price(self, public_client):
        """Test average price returns typed AvgPrice."""
        result = await public_client.get_avg_price(symbol="BTCUSDT")

        assert isinstance(result, AvgPrice)
        assert result.mins >= 0
        assert result.price  # non-empty string

    async def test_get_ticker_price_single(self, public_client):
        """Test price ticker single symbol returns TickerPrice."""
        result = await public_client.get_ticker_price(symbol="BTCUSDT")

        # Single symbol returns single object
        assert isinstance(result, TickerPrice)
        assert result.symbol == "BTCUSDT"
        assert result.price

    async def test_get_ticker_price_all(self, public_client):
        """Test price ticker all symbols returns list[TickerPrice]."""
        result = await public_client.get_ticker_price()

        # No symbol returns list
        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(t, TickerPrice) for t in result)

    async def test_get_ticker_24h_single(self, public_client):
        """Test 24hr ticker single symbol returns Ticker24h."""
        result = await public_client.get_ticker_24h(symbol="BTCUSDT")

        assert isinstance(result, Ticker24h)
        assert result.symbol == "BTCUSDT"
        assert result.price_change
        assert result.price_change_percent
        assert result.volume

    async def test_get_ticker_24h_all(self, public_client):
        """Test 24hr ticker all symbols returns list[Ticker24h]."""
        result = await public_client.get_ticker_24h()

        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(t, Ticker24h) for t in result)

    async def test_get_book_ticker_single(self, public_client):
        """Test book ticker single symbol returns BookTicker."""
        result = await public_client.get_book_ticker(symbol="BTCUSDT")

        assert isinstance(result, BookTicker)
        assert result.symbol == "BTCUSDT"
        assert result.bid_price
        assert result.ask_price

    async def test_get_book_ticker_all(self, public_client):
        """Test book ticker all symbols returns list[BookTicker]."""
        result = await public_client.get_book_ticker()

        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(t, BookTicker) for t in result)
