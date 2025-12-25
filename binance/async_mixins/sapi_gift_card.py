"""
AsyncSapiGiftCardMixin - Gift Card API

This mixin contains all Gift Card related methods that use SAPI (Signed API).
"""
from typing import Dict, Any, Optional, TYPE_CHECKING
from ..client import Client

if TYPE_CHECKING:
    from ._core_typing import AsyncClientCoreLike as _AsyncClientCoreLike
else:
    class _AsyncClientCoreLike:
        pass


class AsyncSapiGiftCardMixin(_AsyncClientCoreLike):
    """
    Gift Card API Mixin
    
    This mixin provides all Gift Card related methods.
    These methods depend on AsyncClientCore for request infrastructure.
    """

    async def gift_card_fetch_token_limit(self, **params):
        return await self._request_margin_api(
            "get", "giftcard/buyCode/token-limit", signed=True, data=params
        )

    gift_card_fetch_token_limit.__doc__ = Client.gift_card_fetch_token_limit.__doc__

    async def gift_card_fetch_rsa_public_key(self, **params):
        return await self._request_margin_api(
            "get", "giftcard/cryptography/rsa-public-key", signed=True, data=params
        )

    gift_card_fetch_rsa_public_key.__doc__ = (
        Client.gift_card_fetch_rsa_public_key.__doc__
    )

    async def gift_card_verify(self, **params):
        return await self._request_margin_api(
            "get", "giftcard/verify", signed=True, data=params
        )

    gift_card_verify.__doc__ = Client.gift_card_verify.__doc__

    async def gift_card_redeem(self, **params):
        return await self._request_margin_api(
            "post", "giftcard/redeemCode", signed=True, data=params
        )

    gift_card_redeem.__doc__ = Client.gift_card_redeem.__doc__

    async def gift_card_create(self, **params):
        return await self._request_margin_api(
            "post", "giftcard/createCode", signed=True, data=params
        )

    gift_card_create.__doc__ = Client.gift_card_create.__doc__

    async def gift_card_create_dual_token(self, **params):
        return await self._request_margin_api(
            "post", "giftcard/buyCode", signed=True, data=params
        )

    gift_card_create_dual_token.__doc__ = Client.gift_card_create_dual_token.__doc__

