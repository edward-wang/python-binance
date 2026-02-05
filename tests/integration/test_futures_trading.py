"""Integration tests for futures trading endpoints.

CAUTION: These tests create real orders on futures testnet.
"""
import pytest

from binance._schemas.futures import FuturesOrder, LeverageResult


@pytest.mark.asyncio
class TestFuturesUMTradingEndpoints:
    """Test USDT-M futures trading endpoints."""

    async def test_futures_create_test_order(self, futures_authenticated_client):
        """Test creating a test order (no actual execution)."""
        result = await futures_authenticated_client.futures_create_test_order(
            symbol="BTCUSDT",
            side="BUY",
            type="LIMIT",
            quantity="0.001",
            price="20000.00",
            time_in_force="GTC",
        )

        # Test order returns empty dict on success
        assert result == {}

    async def test_futures_set_leverage(self, futures_authenticated_client):
        """Test setting leverage."""
        result = await futures_authenticated_client.futures_set_leverage(
            symbol="BTCUSDT",
            leverage=10,
        )

        assert isinstance(result, LeverageResult)
        assert result.leverage == 10
        assert result.symbol == "BTCUSDT"
        assert result.max_notional_value

    async def test_futures_create_and_cancel_limit_order(
        self, futures_authenticated_client
    ):
        """Test creating and canceling a limit order."""
        # Create a low limit buy order (won't fill)
        order = await futures_authenticated_client.futures_create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="LIMIT",
            quantity="0.001",
            price="20000.00",  # Low price, won't fill
            time_in_force="GTC",
        )

        # Verify typed return
        assert isinstance(order, FuturesOrder)
        assert order.order_id > 0
        assert order.symbol == "BTCUSDT"
        assert order.side == "BUY"
        assert order.status == "NEW"

        order_id = order.order_id

        # Query the order
        query = await futures_authenticated_client.futures_get_order(
            symbol="BTCUSDT",
            order_id=order_id,
        )

        assert isinstance(query, FuturesOrder)
        assert query.order_id == order_id
        assert query.status == "NEW"

        # Cancel the order
        cancel = await futures_authenticated_client.futures_cancel_order(
            symbol="BTCUSDT",
            order_id=order_id,
        )

        assert isinstance(cancel, FuturesOrder)
        assert cancel.order_id == order_id
        assert cancel.status == "CANCELED"

    async def test_futures_create_market_order(self, futures_authenticated_client):
        """Test creating a market order.

        Note: This will actually execute on futures testnet.
        Make sure your testnet account has USDT balance.
        """
        # Set leverage first to a safe level
        await futures_authenticated_client.futures_set_leverage(
            symbol="BTCUSDT",
            leverage=1,
        )

        # Small market buy order
        order = await futures_authenticated_client.futures_create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="MARKET",
            quantity="0.001",
        )

        assert isinstance(order, FuturesOrder)
        assert order.symbol == "BTCUSDT"
        assert order.side == "BUY"
        assert order.type == "MARKET"
        # Market orders should fill immediately
        assert order.status in ("FILLED", "PARTIALLY_FILLED", "NEW")

        # Close position if opened
        if order.status == "FILLED":
            await futures_authenticated_client.futures_create_order(
                symbol="BTCUSDT",
                side="SELL",
                type="MARKET",
                quantity="0.001",
            )

    async def test_futures_cancel_all_open_orders(self, futures_authenticated_client):
        """Test canceling all open orders."""
        # First create a limit order
        await futures_authenticated_client.futures_create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="LIMIT",
            quantity="0.001",
            price="20000.00",
            time_in_force="GTC",
        )

        # Cancel all
        result = await futures_authenticated_client.futures_cancel_all_open_orders(
            symbol="BTCUSDT"
        )

        # Should return success response
        assert "code" in result or result == {} or "msg" in result


@pytest.mark.asyncio
class TestFuturesUMOrderQueryEndpoints:
    """Test futures order query endpoints."""

    async def test_futures_get_order_by_client_id(self, futures_authenticated_client):
        """Test querying order by client order ID."""
        import uuid

        client_order_id = f"test_{uuid.uuid4().hex[:8]}"

        # Create order with custom client ID
        order = await futures_authenticated_client.futures_create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="LIMIT",
            quantity="0.001",
            price="20000.00",
            time_in_force="GTC",
            new_client_order_id=client_order_id,
        )

        # Query by client order ID
        query = await futures_authenticated_client.futures_get_order(
            symbol="BTCUSDT",
            orig_client_order_id=client_order_id,
        )

        assert isinstance(query, FuturesOrder)
        assert query.client_order_id == client_order_id

        # Cleanup
        await futures_authenticated_client.futures_cancel_order(
            symbol="BTCUSDT",
            orig_client_order_id=client_order_id,
        )

    async def test_futures_get_all_orders(self, futures_authenticated_client):
        """Test getting all orders (active, canceled, filled)."""
        result = await futures_authenticated_client.futures_get_all_orders(
            symbol="BTCUSDT",
            limit=10,
        )

        assert isinstance(result, list)
        if result:
            assert isinstance(result[0], FuturesOrder)
