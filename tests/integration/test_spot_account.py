"""Integration tests for authenticated Spot API endpoints.

Requires testnet credentials in environment:
  BINANCE_TESTNET_API_KEY
  BINANCE_TESTNET_API_SECRET
"""
import pytest

from binance._schemas.spot import Account, Balance, MyTrade, QueryOrder


@pytest.mark.asyncio
class TestAccountEndpoints:
    """Test authenticated account endpoints."""

    async def test_get_account(self, authenticated_client):
        """Test account info returns typed Account."""
        result = await authenticated_client.get_account()

        assert isinstance(result, Account)
        assert result.maker_commission >= 0
        assert result.taker_commission >= 0
        assert isinstance(result.can_trade, bool)
        assert isinstance(result.balances, list)

    async def test_get_account_has_balances(self, authenticated_client):
        """Test account balances are typed Balance objects."""
        result = await authenticated_client.get_account()

        assert len(result.balances) > 0

        # Check balance structure
        balance = result.balances[0]
        assert isinstance(balance, Balance)
        assert balance.asset  # non-empty string
        assert balance.free is not None
        assert balance.locked is not None

    async def test_get_my_trades(self, authenticated_client):
        """Test my trades returns list of typed MyTrade."""
        result = await authenticated_client.get_my_trades(symbol="BTCUSDT")

        assert isinstance(result, list)
        # May be empty if no trades on testnet
        if result:
            assert isinstance(result[0], MyTrade)

    async def test_get_open_orders(self, authenticated_client):
        """Test open orders returns list of typed QueryOrder."""
        result = await authenticated_client.get_open_orders(symbol="BTCUSDT")

        assert isinstance(result, list)
        # May be empty if no open orders
        if result:
            assert isinstance(result[0], QueryOrder)

    async def test_get_open_orders_all(self, authenticated_client):
        """Test open orders for all symbols."""
        result = await authenticated_client.get_open_orders()

        assert isinstance(result, list)
