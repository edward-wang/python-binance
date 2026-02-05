"""Shared fixtures for integration tests."""
import os

import pytest
import pytest_asyncio

from binance import AsyncClient


def get_testnet_credentials() -> tuple[str, str]:
    """Get testnet API credentials from environment."""
    api_key = os.environ.get("BINANCE_TESTNET_API_KEY", "")
    api_secret = os.environ.get("BINANCE_TESTNET_API_SECRET", "")
    return api_key, api_secret


@pytest.fixture
def has_testnet_credentials() -> bool:
    """Check if testnet credentials are available."""
    api_key, api_secret = get_testnet_credentials()
    return bool(api_key and api_secret)


@pytest_asyncio.fixture
async def public_client():
    """Create a client for public endpoints (no auth needed)."""
    async with AsyncClient(testnet=True) as client:
        yield client


@pytest_asyncio.fixture
async def authenticated_client(has_testnet_credentials):
    """Create an authenticated client for signed endpoints."""
    if not has_testnet_credentials:
        pytest.skip("Testnet credentials not available")

    api_key, api_secret = get_testnet_credentials()
    async with AsyncClient(
        api_key=api_key,
        api_secret=api_secret,
        testnet=True,
    ) as client:
        yield client


# ============ Futures Testnet Fixtures ============


def get_futures_testnet_credentials() -> tuple[str, str]:
    """Get futures testnet API credentials from environment."""
    api_key = os.environ.get("BINANCE_FUTURES_TESTNET_API_KEY", "")
    api_secret = os.environ.get("BINANCE_FUTURES_TESTNET_API_SECRET", "")
    return api_key, api_secret


@pytest.fixture
def has_futures_testnet_credentials() -> bool:
    """Check if futures testnet credentials are available."""
    api_key, api_secret = get_futures_testnet_credentials()
    return bool(api_key and api_secret)


@pytest_asyncio.fixture
async def futures_public_client():
    """Create a client for public futures endpoints (no auth needed)."""
    async with AsyncClient(testnet=True) as client:
        yield client


@pytest_asyncio.fixture
async def futures_authenticated_client(has_futures_testnet_credentials):
    """Create an authenticated client for signed futures endpoints."""
    if not has_futures_testnet_credentials:
        pytest.skip("Futures testnet credentials not available")

    api_key, api_secret = get_futures_testnet_credentials()
    async with AsyncClient(
        api_key=api_key,
        api_secret=api_secret,
        testnet=True,
    ) as client:
        yield client
