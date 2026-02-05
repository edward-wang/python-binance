"""Integration tests for concurrent futures API requests."""
import asyncio

import pytest

from binance._schemas.spot import ServerTime, TickerPrice
from binance._schemas.futures import MarkPrice, FuturesKline


@pytest.mark.asyncio
class TestConcurrentFuturesRequests:
    """Test concurrent futures request handling."""

    async def test_concurrent_mark_price_requests(self, futures_public_client):
        """Test fetching multiple mark prices concurrently."""
        symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]

        tasks = [
            futures_public_client.futures_get_mark_price(symbol=s) for s in symbols
        ]
        results = await asyncio.gather(*tasks)

        assert len(results) == len(symbols)
        for i, result in enumerate(results):
            assert isinstance(result, MarkPrice)
            assert result.symbol == symbols[i]

    async def test_concurrent_klines_requests(self, futures_public_client):
        """Test fetching multiple klines concurrently."""
        requests = [
            ("BTCUSDT", "1h"),
            ("ETHUSDT", "1h"),
            ("BNBUSDT", "4h"),
        ]

        tasks = [
            futures_public_client.futures_get_klines(
                symbol=sym, interval=interval, limit=10
            )
            for sym, interval in requests
        ]
        results = await asyncio.gather(*tasks)

        assert len(results) == len(requests)
        for result in results:
            assert isinstance(result, list)
            if result:
                assert isinstance(result[0], FuturesKline)

    async def test_concurrent_mixed_futures_endpoints(self, futures_public_client):
        """Test concurrent requests to different futures endpoints."""
        tasks = [
            futures_public_client.futures_get_server_time(),
            futures_public_client.futures_get_ticker_price(symbol="BTCUSDT"),
            futures_public_client.futures_get_mark_price(symbol="BTCUSDT"),
            futures_public_client.futures_get_order_book(symbol="BTCUSDT", limit=5),
        ]

        results = await asyncio.gather(*tasks)

        assert len(results) == 4
        assert isinstance(results[0], ServerTime)
        assert isinstance(results[1], TickerPrice)
        assert isinstance(results[2], MarkPrice)

    async def test_concurrent_spot_and_futures(self, futures_public_client):
        """Test concurrent requests to both spot and futures APIs."""
        tasks = [
            # Spot
            futures_public_client.get_server_time(),
            futures_public_client.get_ticker_price(symbol="BTCUSDT"),
            # Futures
            futures_public_client.futures_get_server_time(),
            futures_public_client.futures_get_ticker_price(symbol="BTCUSDT"),
        ]

        results = await asyncio.gather(*tasks)

        assert len(results) == 4
        # All should succeed
        assert all(r is not None for r in results)

    async def test_high_concurrency_futures(self, futures_public_client):
        """Test high number of concurrent futures requests."""
        tasks = [futures_public_client.futures_ping() for _ in range(20)]

        results = await asyncio.gather(*tasks)

        assert len(results) == 20
        assert all(r == {} for r in results)
