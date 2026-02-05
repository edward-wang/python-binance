"""Integration tests for authenticated Futures API endpoints."""
import pytest

from binance._schemas.futures import (
    FuturesAccount,
    FuturesBalance,
    PositionRisk,
    FuturesOrder,
    LeverageResult,
    FuturesMyTrade,
)


@pytest.mark.asyncio
class TestFuturesUMAccountEndpoints:
    """Test USDT-M futures authenticated account endpoints."""

    async def test_futures_get_account(self, futures_authenticated_client):
        """Test account info returns typed FuturesAccount."""
        result = await futures_authenticated_client.futures_get_account()

        assert isinstance(result, FuturesAccount)
        assert result.total_wallet_balance is not None
        assert result.available_balance is not None
        assert isinstance(result.assets, list)
        assert isinstance(result.positions, list)

    async def test_futures_get_balance(self, futures_authenticated_client):
        """Test balance returns list of FuturesBalance."""
        result = await futures_authenticated_client.futures_get_balance()

        assert isinstance(result, list)
        if result:
            balance = result[0]
            assert isinstance(balance, FuturesBalance)
            assert balance.asset
            assert balance.balance is not None

    async def test_futures_get_position_risk(self, futures_authenticated_client):
        """Test position risk returns list of PositionRisk."""
        result = await futures_authenticated_client.futures_get_position_risk()

        assert isinstance(result, list)
        if result:
            position = result[0]
            assert isinstance(position, PositionRisk)
            assert position.symbol
            assert position.leverage

    async def test_futures_get_position_risk_single_symbol(
        self, futures_authenticated_client
    ):
        """Test position risk for single symbol."""
        result = await futures_authenticated_client.futures_get_position_risk(
            symbol="BTCUSDT"
        )

        assert isinstance(result, list)
        # Should return positions for BTCUSDT only
        for position in result:
            assert position.symbol == "BTCUSDT"

    async def test_futures_get_open_orders(self, futures_authenticated_client):
        """Test open orders returns list of FuturesOrder."""
        result = await futures_authenticated_client.futures_get_open_orders(
            symbol="BTCUSDT"
        )

        assert isinstance(result, list)
        # May be empty if no open orders
        if result:
            assert isinstance(result[0], FuturesOrder)

    async def test_futures_get_my_trades(self, futures_authenticated_client):
        """Test my trades returns list of FuturesMyTrade."""
        result = await futures_authenticated_client.futures_get_my_trades(
            symbol="BTCUSDT"
        )

        assert isinstance(result, list)
        # May be empty if no trades
        if result:
            assert isinstance(result[0], FuturesMyTrade)
