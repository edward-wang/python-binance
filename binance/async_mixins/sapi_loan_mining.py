"""
AsyncSapiLoanMiningMixin - Loan & Mining API

This mixin contains all Loan and Mining related methods that use SAPI (Signed API).
"""
from typing import Dict, Any, Optional, TYPE_CHECKING
from ..client import Client

if TYPE_CHECKING:
    from ._core_typing import AsyncClientCoreLike as _AsyncClientCoreLike
else:
    class _AsyncClientCoreLike:
        pass


class AsyncSapiLoanMiningMixin(_AsyncClientCoreLike):
    """
    Loan & Mining API Mixin
    
    This mixin provides all Loan and Mining related methods.
    These methods depend on AsyncClientCore for request infrastructure.
    """

    # Loan Endpoints

    async def futures_loan_borrow_history(self, **params):
        return await self._request_margin_api(
            "get", "futures/loan/borrow/history", True, data=params
        )

    async def futures_loan_repay_history(self, **params):
        return await self._request_margin_api(
            "get", "futures/loan/repay/history", True, data=params
        )

    async def futures_loan_wallet(self, **params):
        return await self._request_margin_api(
            "get", "futures/loan/wallet", True, data=params, version=2
        )

    async def futures_cross_collateral_adjust_history(self, **params):
        return await self._request_margin_api(
            "get", "futures/loan/adjustCollateral/history", True, data=params
        )

    async def futures_cross_collateral_liquidation_history(self, **params):
        return await self._request_margin_api(
            "get", "futures/loan/liquidationHistory", True, data=params
        )

    async def futures_loan_interest_history(self, **params):
        return await self._request_margin_api(
            "get", "futures/loan/interestHistory", True, data=params
        )

    # Versioned Loan Endpoints

    async def margin_v1_get_loan_vip_ongoing_orders(self, **params):
        return await self._request_margin_api(
            "get", "loan/vip/ongoing/orders", signed=True, data=params, version=1
        )

    margin_v1_get_loan_vip_ongoing_orders.__doc__ = (
        Client.margin_v1_get_loan_vip_ongoing_orders.__doc__
    )

    async def margin_v1_get_loan_income(self, **params):
        return await self._request_margin_api(
            "get", "loan/income", signed=True, data=params, version=1
        )

    margin_v1_get_loan_income.__doc__ = Client.margin_v1_get_loan_income.__doc__

    async def margin_v1_get_loan_vip_request_interest_rate(self, **params):
        return await self._request_margin_api(
            "get", "loan/vip/request/interestRate", signed=True, data=params, version=1
        )

    margin_v1_get_loan_vip_request_interest_rate.__doc__ = (
        Client.margin_v1_get_loan_vip_request_interest_rate.__doc__
    )

    async def margin_v1_get_loan_vip_collateral_account(self, **params):
        return await self._request_margin_api(
            "get", "loan/vip/collateral/account", signed=True, data=params, version=1
        )

    margin_v1_get_loan_vip_collateral_account.__doc__ = (
        Client.margin_v1_get_loan_vip_collateral_account.__doc__
    )

    async def margin_v1_post_loan_adjust_ltv(self, **params):
        return await self._request_margin_api(
            "post", "loan/adjust/ltv", signed=True, data=params, version=1
        )

    margin_v1_post_loan_adjust_ltv.__doc__ = (
        Client.margin_v1_post_loan_adjust_ltv.__doc__
    )

    async def margin_v1_post_loan_repay(self, **params):
        return await self._request_margin_api(
            "post", "loan/repay", signed=True, data=params, version=1
        )

    margin_v1_post_loan_repay.__doc__ = Client.margin_v1_post_loan_repay.__doc__

    async def margin_v1_get_loan_loanable_data(self, **params):
        return await self._request_margin_api(
            "get", "loan/loanable/data", signed=True, data=params, version=1
        )

    margin_v1_get_loan_loanable_data.__doc__ = (
        Client.margin_v1_get_loan_loanable_data.__doc__
    )

    async def margin_v2_get_loan_flexible_repay_rate(self, **params):
        return await self._request_margin_api(
            "get", "loan/flexible/repay/rate", signed=True, data=params, version=2
        )

    margin_v2_get_loan_flexible_repay_rate.__doc__ = (
        Client.margin_v2_get_loan_flexible_repay_rate.__doc__
    )

    async def margin_v2_post_loan_flexible_repay(self, **params):
        return await self._request_margin_api(
            "post", "loan/flexible/repay", signed=True, data=params, version=2
        )

    margin_v2_post_loan_flexible_repay.__doc__ = (
        Client.margin_v2_post_loan_flexible_repay.__doc__
    )

    async def margin_v2_get_loan_flexible_loanable_data(self, **params):
        return await self._request_margin_api(
            "get", "loan/flexible/loanable/data", signed=True, data=params, version=2
        )

    margin_v2_get_loan_flexible_loanable_data.__doc__ = (
        Client.margin_v2_get_loan_flexible_loanable_data.__doc__
    )

    async def margin_v2_post_loan_flexible_adjust_ltv(self, **params):
        return await self._request_margin_api(
            "post", "loan/flexible/adjust/ltv", signed=True, data=params, version=2
        )

    margin_v2_post_loan_flexible_adjust_ltv.__doc__ = (
        Client.margin_v2_post_loan_flexible_adjust_ltv.__doc__
    )

    # Mining Endpoints

    async def margin_v1_get_mining_payment_other(self, **params):
        return await self._request_margin_api(
            "get", "mining/payment/other", signed=True, data=params, version=1
        )

    margin_v1_get_mining_payment_other.__doc__ = (
        Client.margin_v1_get_mining_payment_other.__doc__
    )

    async def margin_v1_get_mining_statistics_user_status(self, **params):
        return await self._request_margin_api(
            "get", "mining/statistics/user/status", signed=True, data=params, version=1
        )

    margin_v1_get_mining_statistics_user_status.__doc__ = (
        Client.margin_v1_get_mining_statistics_user_status.__doc__
    )

    async def margin_v1_get_mining_hash_transfer_config_details_list(self, **params):
        return await self._request_margin_api(
            "get",
            "mining/hash-transfer/config/details/list",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_mining_hash_transfer_config_details_list.__doc__ = (
        Client.margin_v1_get_mining_hash_transfer_config_details_list.__doc__
    )

    async def margin_v1_get_mining_hash_transfer_profit_details(self, **params):
        return await self._request_margin_api(
            "get",
            "mining/hash-transfer/profit/details",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_mining_hash_transfer_profit_details.__doc__ = (
        Client.margin_v1_get_mining_hash_transfer_profit_details.__doc__
    )

    async def margin_v1_get_loan_borrow_history(self, **params):
        return await self._request_margin_api(
            "get", "loan/borrow/history", signed=True, data=params, version=1
        )

    margin_v1_get_loan_borrow_history.__doc__ = (
        Client.margin_v1_get_loan_borrow_history.__doc__
    )

    async def margin_v1_get_loan_collateral_data(self, **params):
        return await self._request_margin_api(
            "get", "loan/collateral/data", signed=True, data=params, version=1
        )

    margin_v1_get_loan_collateral_data.__doc__ = (
        Client.margin_v1_get_loan_collateral_data.__doc__
    )

    async def margin_v1_get_loan_ltv_adjustment_history(self, **params):
        return await self._request_margin_api(
            "get", "loan/ltv/adjustment/history", signed=True, data=params, version=1
        )

    margin_v1_get_loan_ltv_adjustment_history.__doc__ = (
        Client.margin_v1_get_loan_ltv_adjustment_history.__doc__
    )

    async def margin_v1_get_loan_ongoing_orders(self, **params):
        return await self._request_margin_api(
            "get", "loan/ongoing/orders", signed=True, data=params, version=1
        )

    margin_v1_get_loan_ongoing_orders.__doc__ = (
        Client.margin_v1_get_loan_ongoing_orders.__doc__
    )

    async def margin_v1_get_loan_repay_collateral_rate(self, **params):
        return await self._request_margin_api(
            "get", "loan/repay/collateral/rate", signed=True, data=params, version=1
        )

    margin_v1_get_loan_repay_collateral_rate.__doc__ = (
        Client.margin_v1_get_loan_repay_collateral_rate.__doc__
    )

    async def margin_v1_get_loan_repay_history(self, **params):
        return await self._request_margin_api(
            "get", "loan/repay/history", signed=True, data=params, version=1
        )

    margin_v1_get_loan_repay_history.__doc__ = (
        Client.margin_v1_get_loan_repay_history.__doc__
    )

    async def margin_v1_get_loan_vip_loanable_data(self, **params):
        return await self._request_margin_api(
            "get", "loan/vip/loanable/data", signed=True, data=params, version=1
        )

    margin_v1_get_loan_vip_loanable_data.__doc__ = (
        Client.margin_v1_get_loan_vip_loanable_data.__doc__
    )

    async def margin_v1_get_loan_vip_repay_history(self, **params):
        return await self._request_margin_api(
            "get", "loan/vip/repay/history", signed=True, data=params, version=1
        )

    margin_v1_get_loan_vip_repay_history.__doc__ = (
        Client.margin_v1_get_loan_vip_repay_history.__doc__
    )

    async def margin_v1_get_mining_payment_list(self, **params):
        return await self._request_margin_api(
            "get", "mining/payment/list", signed=True, data=params, version=1
        )

    margin_v1_get_mining_payment_list.__doc__ = (
        Client.margin_v1_get_mining_payment_list.__doc__
    )

    async def margin_v1_get_mining_payment_uid(self, **params):
        return await self._request_margin_api(
            "get", "mining/payment/uid", signed=True, data=params, version=1
        )

    margin_v1_get_mining_payment_uid.__doc__ = (
        Client.margin_v1_get_mining_payment_uid.__doc__
    )

    async def margin_v1_get_mining_pub_algo_list(self, **params):
        return await self._request_margin_api(
            "get", "mining/pub/algoList", signed=True, data=params, version=1
        )

    margin_v1_get_mining_pub_algo_list.__doc__ = (
        Client.margin_v1_get_mining_pub_algo_list.__doc__
    )

    async def margin_v1_get_mining_pub_coin_list(self, **params):
        return await self._request_margin_api(
            "get", "mining/pub/coinList", signed=True, data=params, version=1
        )

    margin_v1_get_mining_pub_coin_list.__doc__ = (
        Client.margin_v1_get_mining_pub_coin_list.__doc__
    )

    async def margin_v1_get_mining_statistics_user_list(self, **params):
        return await self._request_margin_api(
            "get", "mining/statistics/user/list", signed=True, data=params, version=1
        )

    margin_v1_get_mining_statistics_user_list.__doc__ = (
        Client.margin_v1_get_mining_statistics_user_list.__doc__
    )

    async def margin_v1_get_mining_worker_detail(self, **params):
        return await self._request_margin_api(
            "get", "mining/worker/detail", signed=True, data=params, version=1
        )

    margin_v1_get_mining_worker_detail.__doc__ = (
        Client.margin_v1_get_mining_worker_detail.__doc__
    )

    async def margin_v1_get_mining_worker_list(self, **params):
        return await self._request_margin_api(
            "get", "mining/worker/list", signed=True, data=params, version=1
        )

    margin_v1_get_mining_worker_list.__doc__ = (
        Client.margin_v1_get_mining_worker_list.__doc__
    )

    async def margin_v1_post_loan_borrow(self, **params):
        return await self._request_margin_api(
            "post", "loan/borrow", signed=True, data=params, version=1
        )

    margin_v1_post_loan_borrow.__doc__ = Client.margin_v1_post_loan_borrow.__doc__

    async def margin_v1_post_loan_customize_margin_call(self, **params):
        return await self._request_margin_api(
            "post", "loan/customize/margin_call", signed=True, data=params, version=1
        )

    margin_v1_post_loan_customize_margin_call.__doc__ = (
        Client.margin_v1_post_loan_customize_margin_call.__doc__
    )

    async def margin_v1_post_loan_flexible_repay_history(self, **params):
        return await self._request_margin_api(
            "post", "loan/flexible/repay/history", signed=True, data=params, version=1
        )

    margin_v1_post_loan_flexible_repay_history.__doc__ = (
        Client.margin_v1_post_loan_flexible_repay_history.__doc__
    )

    async def margin_v1_post_loan_vip_borrow(self, **params):
        return await self._request_margin_api(
            "post", "loan/vip/borrow", signed=True, data=params, version=1
        )

    margin_v1_post_loan_vip_borrow.__doc__ = (
        Client.margin_v1_post_loan_vip_borrow.__doc__
    )

    async def margin_v1_post_loan_vip_renew(self, **params):
        return await self._request_margin_api(
            "post", "loan/vip/renew", signed=True, data=params, version=1
        )

    margin_v1_post_loan_vip_renew.__doc__ = Client.margin_v1_post_loan_vip_renew.__doc__

    async def margin_v1_post_loan_vip_repay(self, **params):
        return await self._request_margin_api(
            "post", "loan/vip/repay", signed=True, data=params, version=1
        )

    margin_v1_post_loan_vip_repay.__doc__ = Client.margin_v1_post_loan_vip_repay.__doc__

    async def margin_v1_post_mining_hash_transfer_config(self, **params):
        return await self._request_margin_api(
            "post", "mining/hash-transfer/config", signed=True, data=params, version=1
        )

    margin_v1_post_mining_hash_transfer_config.__doc__ = (
        Client.margin_v1_post_mining_hash_transfer_config.__doc__
    )

    async def margin_v1_post_mining_hash_transfer_config_cancel(self, **params):
        return await self._request_margin_api(
            "post",
            "mining/hash-transfer/config/cancel",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_mining_hash_transfer_config_cancel.__doc__ = (
        Client.margin_v1_post_mining_hash_transfer_config_cancel.__doc__
    )

    async def margin_v2_get_loan_flexible_borrow_history(self, **params):
        return await self._request_margin_api(
            "get", "loan/flexible/borrow/history", signed=True, data=params, version=2
        )

    margin_v2_get_loan_flexible_borrow_history.__doc__ = (
        Client.margin_v2_get_loan_flexible_borrow_history.__doc__
    )

    async def margin_v2_get_loan_flexible_collateral_data(self, **params):
        return await self._request_margin_api(
            "get", "loan/flexible/collateral/data", signed=True, data=params, version=2
        )

    margin_v2_get_loan_flexible_collateral_data.__doc__ = (
        Client.margin_v2_get_loan_flexible_collateral_data.__doc__
    )

    async def margin_v2_get_loan_flexible_ltv_adjustment_history(self, **params):
        return await self._request_margin_api(
            "get",
            "loan/flexible/ltv/adjustment/history",
            signed=True,
            data=params,
            version=2,
        )

    margin_v2_get_loan_flexible_ltv_adjustment_history.__doc__ = (
        Client.margin_v2_get_loan_flexible_ltv_adjustment_history.__doc__
    )

    async def margin_v2_get_loan_flexible_ongoing_orders(self, **params):
        return await self._request_margin_api(
            "get", "loan/flexible/ongoing/orders", signed=True, data=params, version=2
        )

    margin_v2_get_loan_flexible_ongoing_orders.__doc__ = (
        Client.margin_v2_get_loan_flexible_ongoing_orders.__doc__
    )

    async def margin_v2_get_loan_flexible_repay_history(self, **params):
        return await self._request_margin_api(
            "get", "loan/flexible/repay/history", signed=True, data=params, version=2
        )

    margin_v2_get_loan_flexible_repay_history.__doc__ = (
        Client.margin_v2_get_loan_flexible_repay_history.__doc__
    )

    async def margin_v2_post_loan_flexible_borrow(self, **params):
        return await self._request_margin_api(
            "post", "loan/flexible/borrow", signed=True, data=params, version=2
        )

    margin_v2_post_loan_flexible_borrow.__doc__ = (
        Client.margin_v2_post_loan_flexible_borrow.__doc__
    )
