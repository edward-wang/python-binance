"""
AsyncClient Core - 核心请求基础设施模块

此模块包含 AsyncClient 的核心请求能力:
- Session 管理
- HTTP 请求处理
- 响应处理
- 各 API 端点的 URI 构造方法
"""
import asyncio
from pathlib import Path
from typing import Any, Dict, Optional, Union
from urllib.parse import urlencode
import time
import aiohttp
import yarl

from binance.exceptions import (
    BinanceAPIException,
    BinanceRequestException,
)
from binance.helpers import get_loop
from .base_client import BaseClient
from .client import Client


class AsyncClientCore(BaseClient):
    """AsyncClient 的核心请求基础设施"""

    # Contract attributes: initialized by the concrete client (e.g. AsyncClient).
    # They are declared here so type checkers can validate usage in this core.
    loop: Optional[asyncio.AbstractEventLoop]
    https_proxy: Optional[str]
    _session_params: Dict[str, Any]

    def _init_session(self) -> aiohttp.ClientSession:
        loop = getattr(self, "loop", None) or get_loop()
        session_params: Dict[str, Any] = getattr(self, "_session_params", None) or {}
        session = aiohttp.ClientSession(
            loop=loop, headers=self._get_headers(), **session_params
        )
        return session

    async def close_connection(self):
        if self.session:
            assert self.session
            await self.session.close()
        if self.ws_api:
            await self.ws_api.close()
            self._ws_api = None

    async def _request(
        self, method, uri: str, signed: bool, force_params: bool = False, **kwargs
    ):
        # this check needs to be done before __get_request_kwargs to avoid
        # polluting the signature
        headers = {}
        if method.upper() in ["POST", "PUT", "DELETE"]:
            headers.update({"Content-Type": "application/x-www-form-urlencoded"})

        if "data" in kwargs:
            for key in kwargs["data"]:
                if key == "headers":
                    headers.update(kwargs["data"][key])
                    del kwargs["data"][key]
                    break

        kwargs = self._get_request_kwargs(method, signed, force_params, **kwargs)

        if method == "get":
            # url encode the query string
            if "params" in kwargs:
                uri = f"{uri}?{kwargs['params']}"
                kwargs.pop("params")

        data = kwargs.get("data")
        if data is not None:
            del kwargs["data"]

        if (
            signed and self.PRIVATE_KEY and data
        ):  # handle issues with signing using eddsa/rsa and POST requests
            dict_data = Client.convert_to_dict(data)
            signature = dict_data["signature"] if "signature" in dict_data else None
            if signature:
                del dict_data["signature"]
            url_encoded_data = urlencode(dict_data)
            data = f"{url_encoded_data}&signature={signature}"

        # Remove proxies from kwargs since aiohttp uses 'proxy' parameter instead
        kwargs.pop("proxies", None)

        async with getattr(self.session, method)(
            yarl.URL(uri, encoded=True),
            proxy=getattr(self, "https_proxy", None),
            headers=headers,
            data=data,
            **kwargs,
        ) as response:
            self.response = response
            return await self._handle_response(response)

    async def _handle_response(self, response: aiohttp.ClientResponse):
        """Internal helper for handling API responses from the Binance server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """
        if not str(response.status).startswith("2"):
            raise BinanceAPIException(response, response.status, await response.text())

        text = await response.text()
        if text == "":
            return {}

        try:
            return await response.json()
        except ValueError:
            txt = await response.text()
            raise BinanceRequestException(f"Invalid Response: {txt}")

    async def _request_api(
        self,
        method,
        path,
        signed=False,
        version=BaseClient.PUBLIC_API_VERSION,
        **kwargs,
    ):
        uri = self._create_api_uri(path, signed, version)
        force_params = kwargs.pop("force_params", False)
        return await self._request(method, uri, signed, force_params, **kwargs)

    async def _request_futures_api(
        self, method, path, signed=False, version=1, **kwargs
    ) -> Dict:
        version = self._get_version(version, **kwargs)
        uri = self._create_futures_api_uri(path, version=version)
        force_params = kwargs.pop("force_params", False)
        return await self._request(method, uri, signed, force_params, **kwargs)

    async def _request_futures_data_api(
        self, method, path, signed=False, **kwargs
    ) -> Dict:
        uri = self._create_futures_data_api_uri(path)
        force_params = kwargs.pop("force_params", True)
        return await self._request(method, uri, signed, force_params, **kwargs)

    async def _request_futures_coin_api(
        self, method, path, signed=False, version=1, **kwargs
    ) -> Dict:
        version = self._get_version(version, **kwargs)
        uri = self._create_futures_coin_api_url(path, version=version)
        force_params = kwargs.pop("force_params", False)
        return await self._request(method, uri, signed, force_params, **kwargs)

    async def _request_futures_coin_data_api(
        self, method, path, signed=False, version=1, **kwargs
    ) -> Dict:
        version = self._get_version(version, **kwargs)
        uri = self._create_futures_coin_data_api_url(path, version=version)

        force_params = kwargs.pop("force_params", True)
        return await self._request(method, uri, signed, force_params, **kwargs)

    async def _request_options_api(self, method, path, signed=False, **kwargs) -> Dict:
        uri = self._create_options_api_uri(path)
        force_params = kwargs.pop("force_params", True)

        return await self._request(method, uri, signed, force_params, **kwargs)

    async def _request_margin_api(
        self, method, path, signed=False, version=1, **kwargs
    ) -> Dict:
        version = self._get_version(version, **kwargs)
        uri = self._create_margin_api_uri(path, version)

        force_params = kwargs.pop("force_params", False)
        return await self._request(method, uri, signed, force_params, **kwargs)

    async def _request_papi_api(
        self, method, path, signed=False, version=1, **kwargs
    ) -> Dict:
        version = self._get_version(version, **kwargs)
        uri = self._create_papi_api_uri(path, version)

        force_params = kwargs.pop("force_params", False)
        return await self._request(method, uri, signed, force_params, **kwargs)

    async def _request_website(self, method, path, signed=False, **kwargs) -> Dict:
        uri = self._create_website_uri(path)
        return await self._request(method, uri, signed, **kwargs)

    async def _get(
        self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs
    ):
        return await self._request_api("get", path, signed, version, **kwargs)

    async def _post(
        self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs
    ) -> Dict:
        return await self._request_api("post", path, signed, version, **kwargs)

    async def _put(
        self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs
    ) -> Dict:
        return await self._request_api("put", path, signed, version, **kwargs)

    async def _delete(
        self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs
    ) -> Dict:
        return await self._request_api("delete", path, signed, version, **kwargs)

