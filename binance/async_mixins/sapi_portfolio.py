"""
AsyncSapiPortfolioMixin - Portfolio Margin API

This mixin contains all Portfolio Margin related methods that use SAPI (Signed API).
"""
from typing import Dict, Any, Optional, TYPE_CHECKING
from ..client import Client

if TYPE_CHECKING:
    from ._core_typing import AsyncClientCoreLike as _AsyncClientCoreLike
else:
    class _AsyncClientCoreLike:
        pass


class AsyncSapiPortfolioMixin(_AsyncClientCoreLike):
    """
    Portfolio Margin API Mixin
    
    This mixin provides all Portfolio Margin related methods.
    These methods depend on AsyncClientCore for request infrastructure.
    """

    async def margin_v1_get_portfolio_balance(self, **params):
        return await self._request_margin_api(
            "get", "portfolio/balance", signed=True, data=params, version=1
        )

    margin_v1_get_portfolio_balance.__doc__ = (
        Client.margin_v1_get_portfolio_balance.__doc__
    )

    async def margin_v1_post_portfolio_mint(self, **params):
        return await self._request_margin_api(
            "post", "portfolio/mint", signed=True, data=params, version=1
        )

    margin_v1_post_portfolio_mint.__doc__ = Client.margin_v1_post_portfolio_mint.__doc__

    async def margin_v1_post_portfolio_redeem(self, **params):
        return await self._request_margin_api(
            "post", "portfolio/redeem", signed=True, data=params, version=1
        )

    margin_v1_post_portfolio_redeem.__doc__ = (
        Client.margin_v1_post_portfolio_redeem.__doc__
    )

    async def margin_v1_post_portfolio_repay_futures_switch(self, **params):
        return await self._request_margin_api(
            "post",
            "portfolio/repay-futures-switch",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_portfolio_repay_futures_switch.__doc__ = (
        Client.margin_v1_post_portfolio_repay_futures_switch.__doc__
    )

    async def margin_v2_get_portfolio_account(self, **params):
        return await self._request_margin_api(
            "get", "portfolio/account", signed=True, data=params, version=2
        )

    margin_v2_get_portfolio_account.__doc__ = (
        Client.margin_v2_get_portfolio_account.__doc__
    )

    async def margin_v2_get_portfolio_collateral_rate(self, **params):
        return await self._request_margin_api(
            "get", "portfolio/collateralRate", signed=True, data=params, version=2
        )

    margin_v2_get_portfolio_collateral_rate.__doc__ = (
        Client.margin_v2_get_portfolio_collateral_rate.__doc__
    )

