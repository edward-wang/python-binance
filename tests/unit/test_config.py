"""Tests for _core/config.py"""
import pytest
from binance._core.config import (
    BASE_URLS,
    RECV_WINDOW_DEFAULT,
    TIMEOUT_DEFAULT,
    POOL_CONNECTIONS,
    POOL_KEEPALIVE,
    DNS_CACHE_TTL,
    get_base_url,
)


def test_base_urls_contains_spot():
    assert "spot" in BASE_URLS
    assert BASE_URLS["spot"] == "https://api.binance.com"


def test_base_urls_contains_spot_testnet():
    assert "spot_testnet" in BASE_URLS
    assert BASE_URLS["spot_testnet"] == "https://testnet.binance.vision"


def test_base_urls_contains_futures():
    assert "futures_um" in BASE_URLS
    assert "futures_cm" in BASE_URLS


def test_default_constants():
    assert RECV_WINDOW_DEFAULT == 5000
    assert TIMEOUT_DEFAULT == 10.0
    assert POOL_CONNECTIONS == 100
    assert POOL_KEEPALIVE == 30
    assert DNS_CACHE_TTL == 300


def test_get_base_url_spot():
    assert get_base_url("spot", testnet=False) == "https://api.binance.com"
    assert get_base_url("spot", testnet=True) == "https://testnet.binance.vision"


def test_get_base_url_futures():
    assert get_base_url("futures_um", testnet=False) == "https://fapi.binance.com"
    assert get_base_url("futures_um", testnet=True) == "https://testnet.binancefuture.com"


def test_get_base_url_invalid():
    with pytest.raises(KeyError):
        get_base_url("invalid", testnet=False)
