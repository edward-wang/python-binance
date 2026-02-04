"""Test AsyncClient entry point."""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from binance.client import AsyncClient


class TestAsyncClientInit:
    """Test AsyncClient initialization."""

    def test_async_client_importable(self):
        """Test that AsyncClient can be imported."""
        assert AsyncClient is not None

    def test_async_client_init(self):
        """Test AsyncClient initialization."""
        client = AsyncClient(
            api_key="test_key",
            api_secret="test_secret",
            testnet=True,
        )
        assert client is not None

    def test_async_client_has_http_attribute(self):
        """Test that client has _http attribute."""
        client = AsyncClient()
        assert hasattr(client, "_http")

    def test_async_client_has_general_methods(self):
        """Test that client has general methods."""
        client = AsyncClient()
        assert hasattr(client, "ping")
        assert hasattr(client, "get_server_time")
        assert hasattr(client, "get_exchange_info")

    def test_async_client_has_market_methods(self):
        """Test that client has market data methods."""
        client = AsyncClient()
        assert hasattr(client, "get_klines")
        assert hasattr(client, "get_order_book")
        assert hasattr(client, "get_trades")
        assert hasattr(client, "get_ticker_price")
        assert hasattr(client, "get_ticker_24h")
        assert hasattr(client, "get_book_ticker")
        assert hasattr(client, "get_avg_price")
        assert hasattr(client, "get_agg_trades")

    def test_async_client_has_trade_methods(self):
        """Test that client has trading methods."""
        client = AsyncClient()
        assert hasattr(client, "create_order")
        assert hasattr(client, "create_test_order")
        assert hasattr(client, "get_order")
        assert hasattr(client, "cancel_order")
        assert hasattr(client, "get_open_orders")
        assert hasattr(client, "get_all_orders")

    def test_async_client_has_account_methods(self):
        """Test that client has account methods."""
        client = AsyncClient()
        assert hasattr(client, "get_account")
        assert hasattr(client, "get_my_trades")


class TestAsyncClientImports:
    """Test package imports."""

    def test_async_client_importable_from_package(self):
        """Test that AsyncClient can be imported from binance package."""
        from binance import AsyncClient as AC

        assert AC is not None


@pytest.fixture
def mock_client():
    """Create AsyncClient with mocked HTTP."""
    client = AsyncClient(api_key="test", api_secret="test")
    client._http = MagicMock()
    client._http.request = AsyncMock()
    client._http.request_raw = AsyncMock()
    return client


class TestGeneralEndpoints:
    """Test general endpoints with mocks."""

    @pytest.mark.asyncio
    async def test_ping_returns_empty_dict(self, mock_client):
        """Test ping returns empty dict."""
        with patch("binance.api.spot.general.ping", new_callable=AsyncMock) as mock:
            mock.return_value = {}
            result = await mock_client.ping()
            assert result == {}

    @pytest.mark.asyncio
    async def test_get_server_time_returns_typed(self, mock_client):
        """Test get_server_time returns ServerTime."""
        from binance._schemas.spot import ServerTime

        with patch(
            "binance.api.spot.general.get_server_time", new_callable=AsyncMock
        ) as mock:
            mock.return_value = ServerTime(server_time=1699999999999)
            result = await mock_client.get_server_time()
            assert isinstance(result, ServerTime)
            assert result.server_time == 1699999999999


class TestMarketEndpoints:
    """Test market endpoints with mocks."""

    @pytest.mark.asyncio
    async def test_get_order_book_returns_typed(self, mock_client):
        """Test get_order_book returns OrderBook."""
        from binance._schemas.spot import OrderBook

        with patch(
            "binance.api.spot.market.get_order_book", new_callable=AsyncMock
        ) as mock:
            mock.return_value = OrderBook(
                last_update_id=123,
                bids=[["50000", "1"]],
                asks=[["50001", "2"]],
            )
            result = await mock_client.get_order_book(symbol="BTCUSDT")
            assert isinstance(result, OrderBook)
            assert result.last_update_id == 123

    @pytest.mark.asyncio
    async def test_get_klines_returns_typed(self, mock_client):
        """Test get_klines returns list[Kline]."""
        from binance._schemas.spot import Kline

        with patch(
            "binance.api.spot.market.get_klines", new_callable=AsyncMock
        ) as mock:
            mock.return_value = [
                Kline.from_raw(
                    [1699999999999, "50000", "51000", "49000", "50500", "100", 1700000003999, "5000", 100, "60", "3000"]
                )
            ]
            result = await mock_client.get_klines(symbol="BTCUSDT", interval="1h")
            assert isinstance(result, list)
            assert isinstance(result[0], Kline)
            assert result[0].close == "50500"

    @pytest.mark.asyncio
    async def test_get_ticker_price_single_returns_single(self, mock_client):
        """Test single symbol returns TickerPrice."""
        from binance._schemas.spot import TickerPrice

        with patch(
            "binance.api.spot.market.get_ticker_price", new_callable=AsyncMock
        ) as mock:
            mock.return_value = TickerPrice(symbol="BTCUSDT", price="50000")
            result = await mock_client.get_ticker_price(symbol="BTCUSDT")
            assert isinstance(result, TickerPrice)

    @pytest.mark.asyncio
    async def test_get_ticker_price_no_symbol_returns_list(self, mock_client):
        """Test no symbol returns list."""
        from binance._schemas.spot import TickerPrice

        with patch(
            "binance.api.spot.market.get_ticker_price", new_callable=AsyncMock
        ) as mock:
            mock.return_value = [
                TickerPrice(symbol="BTCUSDT", price="50000"),
                TickerPrice(symbol="ETHUSDT", price="3000"),
            ]
            result = await mock_client.get_ticker_price()
            assert isinstance(result, list)
            assert len(result) == 2


class TestTradeEndpoints:
    """Test trade endpoints with mocks."""

    @pytest.mark.asyncio
    async def test_create_order_returns_typed(self, mock_client):
        """Test create_order returns Order."""
        from binance._schemas.spot import Order

        with patch(
            "binance.api.spot.trade.create_order", new_callable=AsyncMock
        ) as mock:
            mock.return_value = Order(
                symbol="BTCUSDT",
                order_id=123456,
                order_list_id=-1,
                client_order_id="test",
                transact_time=1699999999999,
                status="FILLED",
            )
            result = await mock_client.create_order(
                symbol="BTCUSDT",
                side="BUY",
                type="MARKET",
                quantity="0.001",
            )
            assert isinstance(result, Order)
            assert result.order_id == 123456


class TestAccountEndpoints:
    """Test account endpoints with mocks."""

    @pytest.mark.asyncio
    async def test_get_account_returns_typed(self, mock_client):
        """Test get_account returns Account."""
        from binance._schemas.spot import Account, Balance

        with patch(
            "binance.api.spot.account.get_account", new_callable=AsyncMock
        ) as mock:
            mock.return_value = Account(
                maker_commission=10,
                taker_commission=10,
                buyer_commission=0,
                seller_commission=0,
                can_trade=True,
                can_withdraw=True,
                can_deposit=True,
                update_time=1699999999999,
                account_type="SPOT",
                balances=[Balance(asset="BTC", free="1.0", locked="0.0")],
                permissions=["SPOT"],
            )
            result = await mock_client.get_account()
            assert isinstance(result, Account)
            assert result.balances[0].asset == "BTC"
