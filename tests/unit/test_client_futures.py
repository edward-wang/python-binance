"""Test AsyncClient futures HTTP client support."""
import pytest


def test_async_client_has_futures_properties():
    """Test that client has futures HTTP client properties."""
    from binance.client import AsyncClient

    client = AsyncClient(testnet=True)
    assert hasattr(client, "_http_futures_um")
    assert hasattr(client, "_http_futures_cm")


def test_async_client_futures_lazy_init():
    """Test futures clients are lazily initialized."""
    from binance.client import AsyncClient

    client = AsyncClient(testnet=True)
    # Before accessing, internal storage should be None
    assert client._AsyncClient__http_futures_um is None
    assert client._AsyncClient__http_futures_cm is None


def test_async_client_futures_testnet_urls():
    """Test futures clients use correct testnet URLs."""
    from binance.client import AsyncClient
    from binance._core.config import BASE_URLS

    client = AsyncClient(testnet=True)
    # Access to trigger lazy init
    um_client = client._http_futures_um
    cm_client = client._http_futures_cm

    assert um_client._base_url == BASE_URLS["futures_um_testnet"]
    assert cm_client._base_url == BASE_URLS["futures_cm_testnet"]


def test_async_client_futures_production_urls():
    """Test futures clients use correct production URLs."""
    from binance.client import AsyncClient
    from binance._core.config import BASE_URLS

    client = AsyncClient(testnet=False)
    # Access to trigger lazy init
    um_client = client._http_futures_um
    cm_client = client._http_futures_cm

    assert um_client._base_url == BASE_URLS["futures_um"]
    assert cm_client._base_url == BASE_URLS["futures_cm"]


def test_async_client_futures_share_credentials():
    """Test futures clients share API credentials."""
    from binance.client import AsyncClient

    client = AsyncClient(api_key="test_key", api_secret="test_secret", testnet=True)
    um_client = client._http_futures_um
    cm_client = client._http_futures_cm

    assert um_client._api_key == "test_key"
    assert um_client._api_secret == "test_secret"
    assert cm_client._api_key == "test_key"
    assert cm_client._api_secret == "test_secret"


def test_async_client_futures_disable_time_sync():
    """Test futures clients have time sync disabled (share offset from spot)."""
    from binance.client import AsyncClient

    client = AsyncClient(testnet=True)
    um_client = client._http_futures_um
    cm_client = client._http_futures_cm

    # Futures clients should have time sync disabled to share offset from spot
    assert um_client._time_sync_path is None
    assert cm_client._time_sync_path is None


# ============ Task 11: USDT-M Futures General and Market Methods ============


def test_async_client_has_futures_um_general_methods():
    """Test that client has USDT-M futures general methods."""
    from binance.client import AsyncClient

    client = AsyncClient()
    assert hasattr(client, "futures_ping")
    assert hasattr(client, "futures_get_server_time")
    assert hasattr(client, "futures_get_exchange_info")


def test_async_client_has_futures_um_market_methods():
    """Test that client has USDT-M futures market methods."""
    from binance.client import AsyncClient

    client = AsyncClient()
    assert hasattr(client, "futures_get_klines")
    assert hasattr(client, "futures_get_order_book")
    assert hasattr(client, "futures_get_mark_price")
    assert hasattr(client, "futures_get_funding_rate")
    assert hasattr(client, "futures_get_ticker_24h")
    assert hasattr(client, "futures_get_ticker_price")


# ============ Task 12: USDT-M Futures Trade and Account Methods ============


def test_async_client_has_futures_um_trade_methods():
    """Test that client has USDT-M futures trading methods."""
    from binance.client import AsyncClient

    client = AsyncClient()
    assert hasattr(client, "futures_create_order")
    assert hasattr(client, "futures_create_test_order")
    assert hasattr(client, "futures_get_order")
    assert hasattr(client, "futures_cancel_order")
    assert hasattr(client, "futures_cancel_all_open_orders")
    assert hasattr(client, "futures_get_open_orders")
    assert hasattr(client, "futures_create_batch_orders")


def test_async_client_has_futures_um_account_methods():
    """Test that client has USDT-M futures account methods."""
    from binance.client import AsyncClient

    client = AsyncClient()
    assert hasattr(client, "futures_get_account")
    assert hasattr(client, "futures_get_balance")
    assert hasattr(client, "futures_get_position_risk")
    assert hasattr(client, "futures_set_leverage")
    assert hasattr(client, "futures_set_margin_type")
