"""
AsyncSapiPayMixin - Pay API

This mixin contains all Pay related methods that use SAPI (Signed API).
"""
from typing import Dict, Any, Optional, TYPE_CHECKING
from ..client import Client

if TYPE_CHECKING:
    from ._core_typing import AsyncClientCoreLike as _AsyncClientCoreLike
else:
    class _AsyncClientCoreLike:
        pass


class AsyncSapiPayMixin(_AsyncClientCoreLike):
    """
    Pay API Mixin
    
    This mixin provides all Pay related methods.
    These methods depend on AsyncClientCore for request infrastructure.
    """

    # Pay Endpoints

    async def get_pay_trade_history(self, **params):
        return await self._request_margin_api(
            "get", "pay/transactions", signed=True, data=params
        )

    get_pay_trade_history.__doc__ = Client.get_pay_trade_history.__doc__

