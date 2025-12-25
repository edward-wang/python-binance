"""
AsyncSapiConvertMixin - Convert API

This mixin contains all Convert related methods that use SAPI (Signed API).
"""
from typing import Dict, Any, Optional, TYPE_CHECKING
from ..client import Client

if TYPE_CHECKING:
    from ._core_typing import AsyncClientCoreLike as _AsyncClientCoreLike
else:
    class _AsyncClientCoreLike:
        pass


class AsyncSapiConvertMixin(_AsyncClientCoreLike):
    """
    Convert API Mixin
    
    This mixin provides all Convert related methods.
    These methods depend on AsyncClientCore for request infrastructure.
    """

    # Convert Endpoints

    async def get_convert_trade_history(self, **params):
        return await self._request_margin_api(
            "get", "convert/tradeFlow", signed=True, data=params
        )

    get_convert_trade_history.__doc__ = Client.get_convert_trade_history.__doc__

    async def convert_request_quote(self, **params):
        return await self._request_margin_api(
            "post", "convert/getQuote", signed=True, data=params
        )

    convert_request_quote.__doc__ = Client.convert_request_quote.__doc__

    async def convert_accept_quote(self, **params):
        return await self._request_margin_api(
            "post", "convert/acceptQuote", signed=True, data=params
        )

    convert_accept_quote.__doc__ = Client.convert_accept_quote.__doc__

    # Versioned Convert Endpoints

    async def margin_v1_get_convert_order_status(self, **params):
        return await self._request_margin_api(
            "get", "convert/orderStatus", signed=True, data=params, version=1
        )

    margin_v1_get_convert_order_status.__doc__ = (
        Client.margin_v1_get_convert_order_status.__doc__
    )

    async def margin_v1_post_convert_limit_cancel_order(self, **params):
        return await self._request_margin_api(
            "post", "convert/limit/cancelOrder", signed=True, data=params, version=1
        )

    margin_v1_post_convert_limit_cancel_order.__doc__ = (
        Client.margin_v1_post_convert_limit_cancel_order.__doc__
    )

    async def margin_v1_get_convert_asset_info(self, **params):
        return await self._request_margin_api(
            "get", "convert/assetInfo", signed=True, data=params, version=1
        )

    margin_v1_get_convert_asset_info.__doc__ = (
        Client.margin_v1_get_convert_asset_info.__doc__
    )

    async def margin_v1_get_convert_exchange_info(self, **params):
        return await self._request_margin_api(
            "get", "convert/exchangeInfo", signed=False, data=params, version=1
        )

    margin_v1_get_convert_exchange_info.__doc__ = (
        Client.margin_v1_get_convert_exchange_info.__doc__
    )

    async def margin_v1_get_convert_limit_query_open_orders(self, **params):
        return await self._request_margin_api(
            "get", "convert/limit/queryOpenOrders", signed=True, data=params, version=1
        )

    margin_v1_get_convert_limit_query_open_orders.__doc__ = (
        Client.margin_v1_get_convert_limit_query_open_orders.__doc__
    )

    async def margin_v1_post_convert_limit_place_order(self, **params):
        return await self._request_margin_api(
            "post", "convert/limit/placeOrder", signed=True, data=params, version=1
        )

    margin_v1_post_convert_limit_place_order.__doc__ = (
        Client.margin_v1_post_convert_limit_place_order.__doc__
    )
