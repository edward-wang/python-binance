"""
AsyncSapiDciMixin - DCI (Dual Currency Investment) API

This mixin contains all DCI related methods that use SAPI (Signed API).
"""
from typing import Dict, Any, Optional, TYPE_CHECKING
from ..client import Client

if TYPE_CHECKING:
    from ._core_typing import AsyncClientCoreLike as _AsyncClientCoreLike
else:
    class _AsyncClientCoreLike:
        pass


class AsyncSapiDciMixin(_AsyncClientCoreLike):
    """
    DCI (Dual Currency Investment) API Mixin
    
    This mixin provides all DCI related methods.
    These methods depend on AsyncClientCore for request infrastructure.
    """

    async def margin_v1_get_dci_product_accounts(self, **params):
        return await self._request_margin_api(
            "get", "dci/product/accounts", signed=True, data=params, version=1
        )

    margin_v1_get_dci_product_accounts.__doc__ = (
        Client.margin_v1_get_dci_product_accounts.__doc__
    )

    async def margin_v1_get_dci_product_list(self, **params):
        return await self._request_margin_api(
            "get", "dci/product/list", signed=True, data=params, version=1
        )

    margin_v1_get_dci_product_list.__doc__ = (
        Client.margin_v1_get_dci_product_list.__doc__
    )

    async def margin_v1_get_dci_product_positions(self, **params):
        return await self._request_margin_api(
            "get", "dci/product/positions", signed=True, data=params, version=1
        )

    margin_v1_get_dci_product_positions.__doc__ = (
        Client.margin_v1_get_dci_product_positions.__doc__
    )

    async def margin_v1_post_dci_product_auto_compound_edit_status(self, **params):
        return await self._request_margin_api(
            "post",
            "dci/product/auto_compound/edit-status",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_dci_product_auto_compound_edit_status.__doc__ = (
        Client.margin_v1_post_dci_product_auto_compound_edit_status.__doc__
    )

    async def margin_v1_post_dci_product_subscribe(self, **params):
        return await self._request_margin_api(
            "post", "dci/product/subscribe", signed=True, data=params, version=1
        )

    margin_v1_post_dci_product_subscribe.__doc__ = (
        Client.margin_v1_post_dci_product_subscribe.__doc__
    )

