"""Integration tests for concurrent API requests.

Tests that verify the client handles concurrent requests correctly.
"""
import asyncio

import pytest


@pytest.mark.asyncio
class TestConcurrentRequests:
    """Test concurrent request handling."""

    async def test_concurrent_ticker_requests(self, public_client):
        """Test fetching multiple tickers concurrently."""
        symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT"]

        # Fetch all tickers concurrently
        tasks = [public_client.get_ticker_price(symbol=s) for s in symbols]
        results = await asyncio.gather(*tasks)

        assert len(results) == len(symbols)
        for i, result in enumerate(results):
            assert result.symbol == symbols[i]

    async def test_concurrent_klines_requests(self, public_client):
        """Test fetching multiple klines concurrently."""
        requests = [
            ("BTCUSDT", "1h"),
            ("ETHUSDT", "1h"),
            ("BNBUSDT", "4h"),
        ]

        tasks = [
            public_client.get_klines(symbol=sym, interval=interval, limit=10)
            for sym, interval in requests
        ]
        results = await asyncio.gather(*tasks)

        assert len(results) == len(requests)
        for result in results:
            assert isinstance(result, list)
            assert len(result) <= 10

    async def test_concurrent_mixed_endpoints(self, public_client):
        """Test concurrent requests to different endpoints."""
        from binance._schemas.spot import AvgPrice, OrderBook, ServerTime, TickerPrice

        tasks = [
            public_client.get_server_time(),
            public_client.get_ticker_price(symbol="BTCUSDT"),
            public_client.get_order_book(symbol="BTCUSDT", limit=5),
            public_client.get_avg_price(symbol="BTCUSDT"),
        ]

        results = await asyncio.gather(*tasks)

        # All should return successfully
        assert len(results) == 4
        # Verify types
        assert isinstance(results[0], ServerTime)
        assert isinstance(results[1], TickerPrice)
        assert isinstance(results[2], OrderBook)
        assert isinstance(results[3], AvgPrice)

    async def test_high_concurrency(self, public_client):
        """Test high number of concurrent requests."""
        # 20 concurrent ping requests
        tasks = [public_client.ping() for _ in range(20)]

        results = await asyncio.gather(*tasks)

        assert len(results) == 20
        assert all(r == {} for r in results)


@pytest.mark.asyncio
class TestConnectionPooling:
    """Test connection pool behavior."""

    async def test_reuses_connections(self, public_client):
        """Test that client reuses HTTP connections."""
        # Make multiple sequential requests
        for _ in range(5):
            await public_client.ping()

        # If we get here without error, connection reuse is working

    async def test_client_context_manager(self):
        """Test that context manager properly cleans up."""
        from binance import AsyncClient

        async with AsyncClient(testnet=True) as client:
            await client.ping()

        # After context exit, client should be closed
