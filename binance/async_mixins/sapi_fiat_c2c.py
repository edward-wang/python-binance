"""
AsyncSapiFiatC2cMixin - Fiat & C2C API

This mixin contains all Fiat and C2C related methods that use SAPI (Signed API).
"""
from typing import Dict, Any, Optional, TYPE_CHECKING
from ..client import Client

if TYPE_CHECKING:
    from ._core_typing import AsyncClientCoreLike as _AsyncClientCoreLike
else:
    class _AsyncClientCoreLike:
        pass


class AsyncSapiFiatC2cMixin(_AsyncClientCoreLike):
    """
    Fiat & C2C API Mixin
    
    This mixin provides all Fiat and C2C related methods.
    These methods depend on AsyncClientCore for request infrastructure.
    """

    # Fiat Endpoints

    async def get_fiat_deposit_withdraw_history(self, **params):
        return await self._request_margin_api(
            "get", "fiat/orders", signed=True, data=params
        )

    async def get_fiat_payments_history(self, **params):
        return await self._request_margin_api(
            "get", "fiat/payments", signed=True, data=params
        )

    # C2C Endpoints

    async def get_c2c_trade_history(self, **params):
        return await self._request_margin_api(
            "get", "c2c/orderMatch/listUserOrderHistory", signed=True, data=params
        )

