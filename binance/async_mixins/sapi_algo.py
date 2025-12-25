"""
AsyncSapiAlgoMixin - Algo Trading API

This mixin contains all Algo Trading related methods that use SAPI (Signed API).
"""
from typing import Dict, Any, Optional, TYPE_CHECKING
from ..client import Client

if TYPE_CHECKING:
    from ._core_typing import AsyncClientCoreLike as _AsyncClientCoreLike
else:
    class _AsyncClientCoreLike:
        pass


class AsyncSapiAlgoMixin(_AsyncClientCoreLike):
    """
    Algo Trading API Mixin
    
    This mixin provides all Algo Trading related methods.
    These methods depend on AsyncClientCore for request infrastructure.
    """

    # Algo Spot Endpoints

    async def margin_v1_get_algo_spot_historical_orders(self, **params):
        return await self._request_margin_api(
            "get", "algo/spot/historicalOrders", signed=True, data=params, version=1
        )

    margin_v1_get_algo_spot_historical_orders.__doc__ = (
        Client.margin_v1_get_algo_spot_historical_orders.__doc__
    )

    async def margin_v1_get_algo_spot_open_orders(self, **params):
        return await self._request_margin_api(
            "get", "algo/spot/openOrders", signed=True, data=params, version=1
        )

    margin_v1_get_algo_spot_open_orders.__doc__ = (
        Client.margin_v1_get_algo_spot_open_orders.__doc__
    )

    async def margin_v1_get_algo_spot_sub_orders(self, **params):
        return await self._request_margin_api(
            "get", "algo/spot/subOrders", signed=True, data=params, version=1
        )

    margin_v1_get_algo_spot_sub_orders.__doc__ = (
        Client.margin_v1_get_algo_spot_sub_orders.__doc__
    )

    async def margin_v1_delete_algo_spot_order(self, **params):
        return await self._request_margin_api(
            "delete", "algo/spot/order", signed=True, data=params, version=1
        )

    margin_v1_delete_algo_spot_order.__doc__ = (
        Client.margin_v1_delete_algo_spot_order.__doc__
    )

    async def margin_v1_post_algo_spot_new_order_twap(self, **params):
        return await self._request_margin_api(
            "post", "algo/spot/newOrderTwap", signed=True, data=params, version=1
        )

    margin_v1_post_algo_spot_new_order_twap.__doc__ = (
        Client.margin_v1_post_algo_spot_new_order_twap.__doc__
    )

    # Algo Futures Endpoints

    async def margin_v1_post_algo_futures_new_order_twap(self, **params):
        return await self._request_margin_api(
            "post", "algo/futures/newOrderTwap", signed=True, data=params, version=1
        )

    margin_v1_post_algo_futures_new_order_twap.__doc__ = (
        Client.margin_v1_post_algo_futures_new_order_twap.__doc__
    )

    async def margin_v1_post_algo_futures_new_order_vp(self, **params):
        return await self._request_margin_api(
            "post", "algo/futures/newOrderVp", signed=True, data=params, version=1
        )

    margin_v1_post_algo_futures_new_order_vp.__doc__ = (
        Client.margin_v1_post_algo_futures_new_order_vp.__doc__
    )

