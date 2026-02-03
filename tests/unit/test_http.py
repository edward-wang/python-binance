"""Tests for _core/http.py"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from binance._core.http import HTTPClient, _parse_int


class TestParseInt:
    def test_parse_valid_int(self):
        assert _parse_int("123") == 123

    def test_parse_none(self):
        assert _parse_int(None) is None

    def test_parse_empty_string(self):
        assert _parse_int("") is None


class TestHTTPClientInit:
    def test_default_values(self):
        client = HTTPClient()
        assert client._api_key == ""
        assert client._api_secret == ""
        assert "api.binance.com" in client._base_url

    def test_testnet_url(self):
        client = HTTPClient(testnet=True)
        assert "testnet" in client._base_url

    def test_custom_base_url(self):
        client = HTTPClient(base_url="https://custom.api.com")
        assert client._base_url == "https://custom.api.com"

    def test_api_credentials(self):
        client = HTTPClient(api_key="key123", api_secret="secret456")
        assert client._api_key == "key123"
        assert client._api_secret == "secret456"


class TestHTTPClientConnection:
    @pytest.mark.asyncio
    async def test_connect_creates_session(self):
        client = HTTPClient()
        with patch.object(HTTPClient, "_sync_server_time", new_callable=AsyncMock):
            await client.connect()
            assert client._session is not None
            assert client._connector is not None
            await client.close()

    @pytest.mark.asyncio
    async def test_close_cleans_up(self):
        client = HTTPClient()
        with patch.object(HTTPClient, "_sync_server_time", new_callable=AsyncMock):
            await client.connect()
            session = client._session
            connector = client._connector
            await client.close()
            assert session.closed
            assert connector.closed


class TestHTTPClientRequest:
    @pytest.mark.asyncio
    async def test_request_adds_api_key_header(self):
        client = HTTPClient(api_key="test_key")
        client._session = MagicMock()

        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.read = AsyncMock(return_value=b'{"result": "ok"}')
        mock_response.headers = {}
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock()

        client._session.request = MagicMock(return_value=mock_response)

        await client._do_request("GET", "https://api.binance.com/test", {}, {"X-MBX-APIKEY": "test_key"})

        call_args = client._session.request.call_args
        assert call_args[1]["headers"]["X-MBX-APIKEY"] == "test_key"
