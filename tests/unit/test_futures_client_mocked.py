"""Unit tests for AsyncClient futures methods with mocked HTTP."""
from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from binance.client import AsyncClient
from binance._schemas.futures import (
    FuturesKline,
    FuturesOrder,
    PositionRisk,
    MarkPrice,
    FuturesAccount,
    FuturesBalance,
    LeverageResult,
)


@pytest.fixture
def mock_client():
    """Create AsyncClient with mocked HTTP clients."""
    client = AsyncClient(api_key="test", api_secret="test")

    # Mock the futures HTTP clients with _session set (simulates connected)
    mock_um = MagicMock()
    mock_um._session = MagicMock()  # Simulate connected
    mock_um.request = AsyncMock()
    mock_um.request_raw = AsyncMock()
    client._AsyncClient__http_futures_um = mock_um

    mock_cm = MagicMock()
    mock_cm._session = MagicMock()  # Simulate connected
    mock_cm.request = AsyncMock()
    mock_cm.request_raw = AsyncMock()
    client._AsyncClient__http_futures_cm = mock_cm

    return client


class TestFuturesUMMarket:
    """Test USDT-M futures market endpoints with mocks."""

    @pytest.mark.asyncio
    async def test_futures_get_mark_price_single(self, mock_client):
        """Test single symbol returns MarkPrice."""
        with patch(
            "binance.api.futures_um.market.get_mark_price", new_callable=AsyncMock
        ) as mock:
            mock.return_value = MarkPrice(
                symbol="BTCUSDT",
                mark_price="50000",
                index_price="49995",
                last_funding_rate="0.0001",
                next_funding_time=1700000000000,
                time=1699999999999,
            )
            result = await mock_client.futures_get_mark_price(symbol="BTCUSDT")
            assert isinstance(result, MarkPrice)
            assert result.symbol == "BTCUSDT"

    @pytest.mark.asyncio
    async def test_futures_get_klines(self, mock_client):
        """Test get_klines returns list of FuturesKline."""
        with patch(
            "binance.api.futures_um.market.get_klines", new_callable=AsyncMock
        ) as mock:
            mock.return_value = [
                FuturesKline(
                    open_time=1699999999999,
                    open="50000",
                    high="51000",
                    low="49000",
                    close="50500",
                    volume="100",
                    close_time=1700000003999,
                    quote_volume="5000",
                    trades=100,
                    taker_buy_base="60",
                    taker_buy_quote="3000",
                )
            ]
            result = await mock_client.futures_get_klines(
                symbol="BTCUSDT", interval="1h"
            )
            assert isinstance(result, list)
            assert len(result) == 1
            assert isinstance(result[0], FuturesKline)
            assert result[0].close == "50500"


class TestFuturesUMTrade:
    """Test USDT-M futures trade endpoints with mocks."""

    @pytest.mark.asyncio
    async def test_futures_create_order_returns_typed(self, mock_client):
        """Test create_order returns FuturesOrder."""
        with patch(
            "binance.api.futures_um.trade.create_order", new_callable=AsyncMock
        ) as mock:
            mock.return_value = FuturesOrder(
                symbol="BTCUSDT",
                order_id=12345678,
                client_order_id="test",
                price="50000",
                orig_qty="0.001",
                executed_qty="0",
                status="NEW",
                time_in_force="GTC",
                type="LIMIT",
                side="BUY",
            )
            result = await mock_client.futures_create_order(
                symbol="BTCUSDT",
                side="BUY",
                type="LIMIT",
                quantity="0.001",
                price="50000",
                time_in_force="GTC",
            )
            assert isinstance(result, FuturesOrder)
            assert result.order_id == 12345678

    @pytest.mark.asyncio
    async def test_futures_cancel_order(self, mock_client):
        """Test cancel_order returns FuturesOrder."""
        with patch(
            "binance.api.futures_um.trade.cancel_order", new_callable=AsyncMock
        ) as mock:
            mock.return_value = FuturesOrder(
                symbol="BTCUSDT",
                order_id=12345678,
                client_order_id="test",
                price="50000",
                orig_qty="0.001",
                executed_qty="0",
                status="CANCELED",
                time_in_force="GTC",
                type="LIMIT",
                side="BUY",
            )
            result = await mock_client.futures_cancel_order(
                symbol="BTCUSDT", order_id=12345678
            )
            assert isinstance(result, FuturesOrder)
            assert result.status == "CANCELED"


class TestFuturesUMAccount:
    """Test USDT-M futures account endpoints with mocks."""

    @pytest.mark.asyncio
    async def test_futures_get_position_risk(self, mock_client):
        """Test get_position_risk returns list of PositionRisk."""
        with patch(
            "binance.api.futures_um.account.get_position_risk", new_callable=AsyncMock
        ) as mock:
            mock.return_value = [
                PositionRisk(
                    symbol="BTCUSDT",
                    position_amt="0.001",
                    entry_price="50000",
                    mark_price="50500",
                    un_realized_profit="0.50",
                    liquidation_price="40000",
                    leverage="20",
                    margin_type="cross",
                    position_side="BOTH",
                )
            ]
            result = await mock_client.futures_get_position_risk()
            assert isinstance(result, list)
            assert len(result) == 1
            assert result[0].symbol == "BTCUSDT"

    @pytest.mark.asyncio
    async def test_futures_get_account(self, mock_client):
        """Test get_account returns FuturesAccount."""
        with patch(
            "binance.api.futures_um.account.get_account", new_callable=AsyncMock
        ) as mock:
            mock.return_value = FuturesAccount(
                total_initial_margin="1000",
                total_maint_margin="500",
                total_wallet_balance="10000",
                total_unrealized_profit="100",
                total_margin_balance="10100",
                total_position_initial_margin="1000",
                total_open_order_initial_margin="0",
                total_cross_wallet_balance="9000",
                total_cross_un_pnl="50",
                available_balance="9000",
                max_withdraw_amount="9000",
                assets=[],
                positions=[],
            )
            result = await mock_client.futures_get_account()
            assert isinstance(result, FuturesAccount)
            assert result.total_wallet_balance == "10000"

    @pytest.mark.asyncio
    async def test_futures_set_leverage(self, mock_client):
        """Test set_leverage returns LeverageResult."""
        with patch(
            "binance.api.futures_um.account.set_leverage", new_callable=AsyncMock
        ) as mock:
            mock.return_value = LeverageResult(
                symbol="BTCUSDT",
                leverage=20,
                max_notional_value="10000000",
            )
            result = await mock_client.futures_set_leverage(
                symbol="BTCUSDT", leverage=20
            )
            assert isinstance(result, LeverageResult)
            assert result.leverage == 20


class TestFuturesCMMarket:
    """Test COIN-M futures market endpoints with mocks."""

    @pytest.mark.asyncio
    async def test_futures_coin_get_mark_price_single(self, mock_client):
        """Test single symbol returns MarkPrice."""
        with patch(
            "binance.api.futures_cm.market.get_mark_price", new_callable=AsyncMock
        ) as mock:
            mock.return_value = MarkPrice(
                symbol="BTCUSD_PERP",
                mark_price="50000",
                index_price="49995",
                last_funding_rate="0.0001",
                next_funding_time=1700000000000,
                time=1699999999999,
            )
            result = await mock_client.futures_coin_get_mark_price(symbol="BTCUSD_PERP")
            assert isinstance(result, MarkPrice)
            assert result.symbol == "BTCUSD_PERP"


class TestFuturesCMTrade:
    """Test COIN-M futures trade endpoints with mocks."""

    @pytest.mark.asyncio
    async def test_futures_coin_create_order(self, mock_client):
        """Test create_order returns FuturesOrder."""
        with patch(
            "binance.api.futures_cm.trade.create_order", new_callable=AsyncMock
        ) as mock:
            mock.return_value = FuturesOrder(
                symbol="BTCUSD_PERP",
                order_id=12345678,
                client_order_id="test",
                price="50000",
                orig_qty="1",
                executed_qty="0",
                status="NEW",
                time_in_force="GTC",
                type="LIMIT",
                side="BUY",
            )
            result = await mock_client.futures_coin_create_order(
                symbol="BTCUSD_PERP",
                side="BUY",
                type="LIMIT",
                quantity="1",
                price="50000",
                time_in_force="GTC",
            )
            assert isinstance(result, FuturesOrder)
            assert result.order_id == 12345678


class TestFuturesCMAccount:
    """Test COIN-M futures account endpoints with mocks."""

    @pytest.mark.asyncio
    async def test_futures_coin_get_balance(self, mock_client):
        """Test get_balance returns list of FuturesBalance."""
        with patch(
            "binance.api.futures_cm.account.get_balance", new_callable=AsyncMock
        ) as mock:
            mock.return_value = [
                FuturesBalance(
                    account_alias="FuturesMain",
                    asset="BTC",
                    balance="1.5",
                    cross_wallet_balance="1.5",
                    cross_un_pnl="0.01",
                    available_balance="1.4",
                    max_withdraw_amount="1.4",
                )
            ]
            result = await mock_client.futures_coin_get_balance()
            assert isinstance(result, list)
            assert len(result) == 1
            assert result[0].asset == "BTC"
