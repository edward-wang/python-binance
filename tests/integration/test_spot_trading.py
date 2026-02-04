"""Integration tests for trading endpoints.

CAUTION: These tests create real orders on testnet.
"""
import uuid

import pytest

from binance._schemas.spot import CancelOrderResult, Order, QueryOrder


@pytest.mark.asyncio
class TestTradingEndpoints:
    """Test trading endpoints."""

    async def test_create_test_order(self, authenticated_client):
        """Test creating a test order (no actual execution)."""
        result = await authenticated_client.create_test_order(
            symbol="BTCUSDT",
            side="BUY",
            type="LIMIT",
            quantity="0.001",
            price="20000.00",
            time_in_force="GTC",
        )

        # Test order returns empty dict on success
        assert result == {}

    async def test_create_and_cancel_limit_order(self, authenticated_client):
        """Test creating and canceling a limit order."""
        client_order_id = f"test_{uuid.uuid4().hex[:8]}"

        # Create a low limit buy order (won't fill)
        order = await authenticated_client.create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="LIMIT",
            quantity="0.001",
            price="10000.00",  # Low price, won't fill
            time_in_force="GTC",
            new_client_order_id=client_order_id,
            new_order_resp_type="FULL",
        )

        # Verify typed return
        assert isinstance(order, Order)
        assert order.order_id > 0
        assert order.symbol == "BTCUSDT"
        assert order.side == "BUY"
        assert order.status == "NEW"

        order_id = order.order_id

        # Query the order
        query = await authenticated_client.get_order(
            symbol="BTCUSDT",
            order_id=order_id,
        )

        assert isinstance(query, QueryOrder)
        assert query.order_id == order_id
        assert query.status == "NEW"

        # Cancel the order
        cancel = await authenticated_client.cancel_order(
            symbol="BTCUSDT",
            order_id=order_id,
        )

        assert isinstance(cancel, CancelOrderResult)
        assert cancel.order_id == order_id
        assert cancel.status == "CANCELED"

    async def test_get_order_by_client_id(self, authenticated_client):
        """Test querying order by client order ID."""
        client_order_id = f"test_{uuid.uuid4().hex[:8]}"

        # Create order with custom client ID
        order = await authenticated_client.create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="LIMIT",
            quantity="0.001",
            price="10000.00",
            time_in_force="GTC",
            new_client_order_id=client_order_id,
        )

        # Query by client order ID
        query = await authenticated_client.get_order(
            symbol="BTCUSDT",
            orig_client_order_id=client_order_id,
        )

        assert isinstance(query, QueryOrder)
        assert query.client_order_id == client_order_id

        # Cleanup
        await authenticated_client.cancel_order(
            symbol="BTCUSDT",
            orig_client_order_id=client_order_id,
        )
