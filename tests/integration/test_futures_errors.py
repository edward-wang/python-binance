"""Integration tests for Futures API error scenarios."""
import pytest

from binance._core.exceptions import (
    BinanceAPIError,
    InvalidSymbolError,
    InvalidParameterError,
)


@pytest.mark.asyncio
class TestFuturesInvalidSymbolErrors:
    """Test error handling for invalid symbols."""

    async def test_invalid_symbol_raises_error(self, futures_public_client):
        """Test that invalid symbol raises InvalidSymbolError."""
        with pytest.raises((InvalidSymbolError, BinanceAPIError)) as exc_info:
            await futures_public_client.futures_get_order_book(symbol="INVALID_SYMBOL")

        # Should get error code -1121 (INVALID_SYMBOL)
        if hasattr(exc_info.value, "code"):
            assert exc_info.value.code == -1121

    async def test_invalid_symbol_klines(self, futures_public_client):
        """Test invalid symbol in klines endpoint."""
        with pytest.raises((InvalidSymbolError, BinanceAPIError)):
            await futures_public_client.futures_get_klines(
                symbol="NOTREAL", interval="1h"
            )


@pytest.mark.asyncio
class TestFuturesInvalidParameterErrors:
    """Test error handling for invalid parameters."""

    async def test_invalid_interval(self, futures_public_client):
        """Test invalid interval parameter."""
        with pytest.raises((InvalidParameterError, BinanceAPIError)):
            await futures_public_client.futures_get_klines(
                symbol="BTCUSDT", interval="invalid"
            )

    async def test_invalid_leverage(self, futures_authenticated_client):
        """Test invalid leverage value."""
        with pytest.raises(BinanceAPIError):
            await futures_authenticated_client.futures_set_leverage(
                symbol="BTCUSDT",
                leverage=1000,  # Too high
            )


@pytest.mark.asyncio
class TestFuturesAuthenticationErrors:
    """Test error handling for authentication issues."""

    async def test_signed_endpoint_without_auth(self):
        """Test calling signed endpoint without credentials."""
        from binance import AsyncClient

        async with AsyncClient(testnet=True) as client:
            with pytest.raises(BinanceAPIError) as exc_info:
                await client.futures_get_account()

            # Should get authentication error
            assert exc_info.value.code in (-2014, -2015, -1022)


@pytest.mark.asyncio
class TestFuturesOrderErrors:
    """Test error handling for order-related errors."""

    async def test_insufficient_margin(self, futures_authenticated_client):
        """Test order with insufficient margin."""
        with pytest.raises(BinanceAPIError) as exc_info:
            await futures_authenticated_client.futures_create_order(
                symbol="BTCUSDT",
                side="BUY",
                type="MARKET",
                quantity="10000",  # Very large quantity
            )

        # Error code -2019: Margin is insufficient
        # or -4003: Quantity greater than max qty
        assert exc_info.value.code in (-2019, -4003, -1111)

    async def test_cancel_nonexistent_order(self, futures_authenticated_client):
        """Test canceling order that doesn't exist."""
        with pytest.raises(BinanceAPIError) as exc_info:
            await futures_authenticated_client.futures_cancel_order(
                symbol="BTCUSDT",
                order_id=999999999999,
            )

        # Error code -2011: Unknown order
        assert exc_info.value.code == -2011

    async def test_query_nonexistent_order(self, futures_authenticated_client):
        """Test querying order that doesn't exist."""
        with pytest.raises(BinanceAPIError) as exc_info:
            await futures_authenticated_client.futures_get_order(
                symbol="BTCUSDT",
                order_id=999999999999,
            )

        # Error code -2013: Order does not exist
        assert exc_info.value.code == -2013
