"""
AsyncSapiLocalentityMixin - Local Entity Compliance API

This mixin contains all Local Entity compliance related methods that use SAPI (Signed API).
"""
from typing import Dict, Any, Optional, TYPE_CHECKING
from ..client import Client

if TYPE_CHECKING:
    from ._core_typing import AsyncClientCoreLike as _AsyncClientCoreLike
else:
    class _AsyncClientCoreLike:
        pass


class AsyncSapiLocalentityMixin(_AsyncClientCoreLike):
    """
    Local Entity Compliance API Mixin
    
    This mixin provides all Local Entity compliance related methods.
    These methods depend on AsyncClientCore for request infrastructure.
    """

    # Local Entity methods will be added here
    pass


    async def margin_v1_get_localentity_deposit_history(self, **params):
        return await self._request_margin_api(
            "get", "localentity/deposit/history", signed=True, data=params, version=1
        )

    margin_v1_get_localentity_deposit_history.__doc__ = (
        Client.margin_v1_get_localentity_deposit_history.__doc__
    )

    async def margin_v1_get_localentity_vasp(self, **params):
        return await self._request_margin_api(
            "get", "localentity/vasp", signed=True, data=params, version=1
        )

    margin_v1_get_localentity_vasp.__doc__ = (
        Client.margin_v1_get_localentity_vasp.__doc__
    )

    async def margin_v1_get_localentity_withdraw_history(self, **params):
        return await self._request_margin_api(
            "get", "localentity/withdraw/history", signed=True, data=params, version=1
        )

    margin_v1_get_localentity_withdraw_history.__doc__ = (
        Client.margin_v1_get_localentity_withdraw_history.__doc__
    )

    async def margin_v1_post_localentity_withdraw_apply(self, **params):
        return await self._request_margin_api(
            "post", "localentity/withdraw/apply", signed=True, data=params, version=1
        )

    margin_v1_post_localentity_withdraw_apply.__doc__ = (
        Client.margin_v1_post_localentity_withdraw_apply.__doc__
    )

    async def margin_v1_put_localentity_deposit_provide_info(self, **params):
        return await self._request_margin_api(
            "put",
            "localentity/deposit/provide-info",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_put_localentity_deposit_provide_info.__doc__ = (
        Client.margin_v1_put_localentity_deposit_provide_info.__doc__
    )

    async def margin_v2_get_localentity_withdraw_history(self, **params):
        return await self._request_margin_api(
            "get", "localentity/withdraw/history", signed=True, data=params, version=2
        )

    margin_v2_get_localentity_withdraw_history.__doc__ = (
        Client.margin_v2_get_localentity_withdraw_history.__doc__
    )
