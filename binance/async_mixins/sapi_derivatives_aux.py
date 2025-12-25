"""
AsyncSapiDerivativesAuxMixin - Derivatives Auxiliary API

This mixin contains all Derivatives auxiliary methods (futures transfer, futures data) that use SAPI (Signed API).
"""
from typing import Dict, Any, Optional, TYPE_CHECKING
from ..client import Client

if TYPE_CHECKING:
    from ._core_typing import AsyncClientCoreLike as _AsyncClientCoreLike
else:
    class _AsyncClientCoreLike:
        pass


class AsyncSapiDerivativesAuxMixin(_AsyncClientCoreLike):
    """
    Derivatives Auxiliary API Mixin
    
    This mixin provides all Derivatives auxiliary methods (futures transfer, futures data).
    These methods depend on AsyncClientCore for request infrastructure.
    """

    async def futures_account_transfer(self, **params):
        return await self._request_margin_api(
            "post", "futures/transfer", True, data=params
        )

    async def transfer_history(self, **params):
        return await self._request_margin_api(
            "get", "futures/transfer", True, data=params
        )

    async def futures_historical_data_link(self, **params):
        return await self._request_margin_api(
            "get", "futures/data/histDataLink", signed=True, data=params
        )

    futures_historical_data_link.__doc__ = Client.futures_historical_data_link.__doc__

    async def margin_v1_get_copy_trading_futures_lead_symbol(self, **params):
        return await self._request_margin_api(
            "get", "copyTrading/futures/leadSymbol", signed=True, data=params, version=1
        )

    margin_v1_get_copy_trading_futures_lead_symbol.__doc__ = (
        Client.margin_v1_get_copy_trading_futures_lead_symbol.__doc__
    )

    async def margin_v1_get_copy_trading_futures_user_status(self, **params):
        return await self._request_margin_api(
            "get", "copyTrading/futures/userStatus", signed=True, data=params, version=1
        )

    margin_v1_get_copy_trading_futures_user_status.__doc__ = (
        Client.margin_v1_get_copy_trading_futures_user_status.__doc__
    )

