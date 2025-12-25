"""
AsyncSapiAccountSecurityMixin - Account & Security API

This mixin contains all System and Account security related methods that use SAPI (Signed API).
"""
from typing import Dict, Any, Optional, TYPE_CHECKING
from ..client import Client

if TYPE_CHECKING:
    from ._core_typing import AsyncClientCoreLike as _AsyncClientCoreLike
else:
    class _AsyncClientCoreLike:
        pass


class AsyncSapiAccountSecurityMixin(_AsyncClientCoreLike):
    """
    Account & Security API Mixin
    
    This mixin provides all System and Account security related methods.
    These methods depend on AsyncClientCore for request infrastructure.
    """

    async def margin_v1_post_account_api_restrictions_ip_restriction_ip_list(
        self, **params
    ):
        return await self._request_margin_api(
            "post",
            "account/apiRestrictions/ipRestriction/ipList",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_account_api_restrictions_ip_restriction_ip_list.__doc__ = (
        Client.margin_v1_post_account_api_restrictions_ip_restriction_ip_list.__doc__
    )

    async def margin_v1_delete_account_api_restrictions_ip_restriction_ip_list(
        self, **params
    ):
        return await self._request_margin_api(
            "delete",
            "account/apiRestrictions/ipRestriction/ipList",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_delete_account_api_restrictions_ip_restriction_ip_list.__doc__ = (
        Client.margin_v1_delete_account_api_restrictions_ip_restriction_ip_list.__doc__
    )

    async def margin_v1_get_account_api_restrictions_ip_restriction(self, **params):
        return await self._request_margin_api(
            "get",
            "account/apiRestrictions/ipRestriction",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_account_api_restrictions_ip_restriction.__doc__ = (
        Client.margin_v1_get_account_api_restrictions_ip_restriction.__doc__
    )

    async def margin_v1_get_account_info(self, **params):
        return await self._request_margin_api(
            "get", "account/info", signed=True, data=params, version=1
        )

    margin_v1_get_account_info.__doc__ = Client.margin_v1_get_account_info.__doc__

    async def margin_v1_post_account_api_restrictions_ip_restriction(self, **params):
        return await self._request_margin_api(
            "post",
            "account/apiRestrictions/ipRestriction",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_account_api_restrictions_ip_restriction.__doc__ = (
        Client.margin_v1_post_account_api_restrictions_ip_restriction.__doc__
    )

    async def margin_v1_post_account_disable_fast_withdraw_switch(self, **params):
        return await self._request_margin_api(
            "post",
            "account/disableFastWithdrawSwitch",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_account_disable_fast_withdraw_switch.__doc__ = (
        Client.margin_v1_post_account_disable_fast_withdraw_switch.__doc__
    )

    async def margin_v1_post_account_enable_fast_withdraw_switch(self, **params):
        return await self._request_margin_api(
            "post",
            "account/enableFastWithdrawSwitch",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_account_enable_fast_withdraw_switch.__doc__ = (
        Client.margin_v1_post_account_enable_fast_withdraw_switch.__doc__
    )
