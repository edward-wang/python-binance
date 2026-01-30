"""
Client Core - 核心请求基础设施模块

此模块包含 Client 的核心请求能力:
- Session 管理
- HTTP 请求处理
- 响应处理
- 各 API 端点的 URI 构造方法
"""
from pathlib import Path
from typing import Any, Dict, Optional, Union
from urllib.parse import urlencode
import requests

from binance.exceptions import (
    BinanceAPIException,
    BinanceRequestException,
)
from .base_client import BaseClient


class ClientCore(BaseClient):
    """Client 的核心请求基础设施"""

    def _init_session(self) -> requests.Session:
        headers = self._get_headers()

        session = requests.session()
        session.headers.update(headers)
        return session

    def _request(
        self, method, uri: str, signed: bool, force_params: bool = False, **kwargs
    ):
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

        data = kwargs.get("data")
        if data is not None:
            del kwargs["data"]

        if signed and self.PRIVATE_KEY and data:  # handle issues with signing using eddsa/rsa and POST requests
            dict_data = ClientCore.convert_to_dict(data)
            signature = dict_data["signature"] if "signature" in dict_data else None
            if signature:
                del dict_data["signature"]
            url_encoded_data = urlencode(dict_data)
            data = f"{url_encoded_data}&signature={signature}"

        self.response = getattr(self.session, method)(uri, headers=headers, data=data, **kwargs)
        return self._handle_response(self.response)

    @staticmethod
    def _handle_response(response: requests.Response):
        """Internal helper for handling API responses from the Binance server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """
        if not (200 <= response.status_code < 300):
            raise BinanceAPIException(response, response.status_code, response.text)

        if response.text == "":
            return {}

        try:
            return response.json()
        except ValueError:
            raise BinanceRequestException("Invalid Response: %s" % response.text)

    def _request_api(
        self,
        method,
        path: str,
        signed: bool = False,
        version=BaseClient.PUBLIC_API_VERSION,
        **kwargs,
    ):
        uri = self._create_api_uri(path, signed, version)
        return self._request(method, uri, signed, **kwargs)

    def _request_futures_api(
        self, method, path, signed=False, version: int = 1, **kwargs
    ) -> Dict:
        version = self._get_version(version, **kwargs)
        uri = self._create_futures_api_uri(path, version)
        force_params = kwargs.pop("force_params", False)

        return self._request(method, uri, signed, force_params, **kwargs)

    def _request_futures_data_api(self, method, path, signed=False, **kwargs) -> Dict:
        uri = self._create_futures_data_api_uri(path)

        force_params = kwargs.pop("force_params", True)
        return self._request(method, uri, signed, force_params, **kwargs)

    def _request_futures_coin_api(
        self, method, path, signed=False, version=1, **kwargs
    ) -> Dict:
        version = self._get_version(version, **kwargs)
        uri = self._create_futures_coin_api_url(path, version=version)

        force_params = kwargs.pop("force_params", False)
        return self._request(method, uri, signed, force_params, **kwargs)

    def _request_futures_coin_data_api(
        self, method, path, signed=False, version=1, **kwargs
    ) -> Dict:
        version = self._get_version(version, **kwargs)
        uri = self._create_futures_coin_data_api_url(path, version=version)

        force_params = kwargs.pop("force_params", True)
        return self._request(method, uri, signed, force_params, **kwargs)

    def _request_options_api(self, method, path, signed=False, **kwargs) -> Dict:
        """
        https://developers.binance.com/docs/derivatives/option/market-data
        """
        uri = self._create_options_api_uri(path)

        force_params = kwargs.pop("force_params", True)
        return self._request(method, uri, signed, force_params, **kwargs)

    def _request_margin_api(
        self, method, path, signed=False, version=1, **kwargs
    ) -> Dict:
        version = self._get_version(version, **kwargs)
        uri = self._create_margin_api_uri(path, version)

        force_params = kwargs.pop("force_params", False)
        return self._request(method, uri, signed, force_params, **kwargs)

    def _request_papi_api(
        self, method, path, signed=False, version=1, **kwargs
    ) -> Dict:
        version = self._get_version(version, **kwargs)
        uri = self._create_papi_api_uri(path, version)
        force_params = kwargs.pop("force_params", False)
        return self._request(method, uri, signed, force_params, **kwargs)

    def _request_website(self, method, path, signed=False, **kwargs) -> Dict:
        uri = self._create_website_uri(path)
        return self._request(method, uri, signed, **kwargs)

    def _get(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs):
        return self._request_api("get", path, signed, version, **kwargs)

    def _post(
        self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs
    ) -> Dict:
        return self._request_api("post", path, signed, version, **kwargs)

    def _put(
        self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs
    ) -> Dict:
        return self._request_api("put", path, signed, version, **kwargs)

    def _delete(
        self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs
    ) -> Dict:
        return self._request_api("delete", path, signed, version, **kwargs)

