"""Integration tests for public Futures API endpoints.

All tests verify typed schema returns.
"""
import pytest

from binance._schemas.spot import ServerTime, OrderBook, TickerPrice, BookTicker
from binance._schemas.futures import (
    FuturesExchangeInfo,
    FuturesKline,
    MarkPrice,
    FundingRate,
    FuturesTicker24h,
)


@pytest.mark.asyncio
class TestFuturesUMGeneralEndpoints:
    """Test USDT-M futures general public endpoints."""

    async def test_futures_ping(self, futures_public_client):
        """Test ping endpoint returns successfully."""
        result = await futures_public_client.futures_ping()
        assert result == {}

    async def test_futures_get_server_time(self, futures_public_client):
        """Test server time returns typed ServerTime."""
        result = await futures_public_client.futures_get_server_time()

        assert isinstance(result, ServerTime)
        assert result.server_time > 0

    async def test_futures_get_exchange_info(self, futures_public_client):
        """Test exchange info returns typed FuturesExchangeInfo."""
        result = await futures_public_client.futures_get_exchange_info()

        assert isinstance(result, FuturesExchangeInfo)
        assert result.timezone == "UTC"
        assert result.server_time > 0
        assert len(result.symbols) > 0

    async def test_futures_exchange_info_has_perpetual(self, futures_public_client):
        """Test exchange info includes perpetual contracts."""
        result = await futures_public_client.futures_get_exchange_info()

        perpetual_symbols = [
            s for s in result.symbols if s.contract_type == "PERPETUAL"
        ]
        assert len(perpetual_symbols) > 0

        # BTCUSDT should be a perpetual
        btc = next((s for s in perpetual_symbols if s.symbol == "BTCUSDT"), None)
        assert btc is not None
        assert btc.base_asset == "BTC"
        assert btc.quote_asset == "USDT"


@pytest.mark.asyncio
class TestFuturesUMMarketDataEndpoints:
    """Test USDT-M futures market data endpoints."""

    async def test_futures_get_order_book(self, futures_public_client):
        """Test order book returns typed OrderBook."""
        result = await futures_public_client.futures_get_order_book(
            symbol="BTCUSDT", limit=5
        )

        assert isinstance(result, OrderBook)
        assert result.last_update_id > 0
        assert len(result.bids) <= 5
        assert len(result.asks) <= 5

    async def test_futures_get_klines(self, futures_public_client):
        """Test klines returns list of typed FuturesKline."""
        result = await futures_public_client.futures_get_klines(
            symbol="BTCUSDT",
            interval="1h",
            limit=5,
        )

        assert isinstance(result, list)
        assert len(result) <= 5

        if result:
            kline = result[0]
            assert isinstance(kline, FuturesKline)
            assert kline.open_time > 0
            assert kline.open  # non-empty string
            assert kline.close_time > kline.open_time

    async def test_futures_get_continuous_klines(self, futures_public_client):
        """Test continuous klines returns list of FuturesKline."""
        result = await futures_public_client.futures_get_continuous_klines(
            pair="BTCUSDT",
            contract_type="PERPETUAL",
            interval="1h",
            limit=5,
        )

        assert isinstance(result, list)
        if result:
            assert isinstance(result[0], FuturesKline)

    async def test_futures_get_mark_price_single(self, futures_public_client):
        """Test mark price single symbol returns MarkPrice."""
        result = await futures_public_client.futures_get_mark_price(symbol="BTCUSDT")

        assert isinstance(result, MarkPrice)
        assert result.symbol == "BTCUSDT"
        assert result.mark_price
        assert result.index_price
        assert result.last_funding_rate

    async def test_futures_get_mark_price_all(self, futures_public_client):
        """Test mark price all symbols returns list[MarkPrice]."""
        result = await futures_public_client.futures_get_mark_price()

        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(m, MarkPrice) for m in result)

    async def test_futures_get_funding_rate(self, futures_public_client):
        """Test funding rate history returns list of FundingRate."""
        result = await futures_public_client.futures_get_funding_rate(
            symbol="BTCUSDT",
            limit=5,
        )

        assert isinstance(result, list)
        if result:
            rate = result[0]
            assert isinstance(rate, FundingRate)
            assert rate.symbol == "BTCUSDT"
            assert rate.funding_rate
            assert rate.funding_time > 0

    async def test_futures_get_ticker_24h_single(self, futures_public_client):
        """Test 24hr ticker single returns FuturesTicker24h."""
        result = await futures_public_client.futures_get_ticker_24h(symbol="BTCUSDT")

        assert isinstance(result, FuturesTicker24h)
        assert result.symbol == "BTCUSDT"
        assert result.price_change
        assert result.volume

    async def test_futures_get_ticker_24h_all(self, futures_public_client):
        """Test 24hr ticker all returns list."""
        result = await futures_public_client.futures_get_ticker_24h()

        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(t, FuturesTicker24h) for t in result)

    async def test_futures_get_ticker_price_single(self, futures_public_client):
        """Test price ticker single returns TickerPrice."""
        result = await futures_public_client.futures_get_ticker_price(symbol="BTCUSDT")

        assert isinstance(result, TickerPrice)
        assert result.symbol == "BTCUSDT"
        assert result.price

    async def test_futures_get_ticker_price_all(self, futures_public_client):
        """Test price ticker all returns list."""
        result = await futures_public_client.futures_get_ticker_price()

        assert isinstance(result, list)
        assert len(result) > 0

    async def test_futures_get_book_ticker_single(self, futures_public_client):
        """Test book ticker single returns BookTicker."""
        result = await futures_public_client.futures_get_book_ticker(symbol="BTCUSDT")

        assert isinstance(result, BookTicker)
        assert result.symbol == "BTCUSDT"
        assert result.bid_price
        assert result.ask_price


@pytest.mark.asyncio
class TestFuturesCMPublicEndpoints:
    """Test COIN-M futures public endpoints."""

    async def test_futures_coin_ping(self, futures_public_client):
        """Test COIN-M ping endpoint."""
        result = await futures_public_client.futures_coin_ping()
        assert result == {}

    async def test_futures_coin_get_exchange_info(self, futures_public_client):
        """Test COIN-M exchange info."""
        result = await futures_public_client.futures_coin_get_exchange_info()

        assert isinstance(result, FuturesExchangeInfo)
        assert len(result.symbols) > 0

    async def test_futures_coin_get_klines(self, futures_public_client):
        """Test COIN-M klines."""
        result = await futures_public_client.futures_coin_get_klines(
            symbol="BTCUSD_PERP",
            interval="1h",
            limit=5,
        )

        assert isinstance(result, list)
        if result:
            assert isinstance(result[0], FuturesKline)
