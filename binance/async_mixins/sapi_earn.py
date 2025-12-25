"""
AsyncSapiEarnMixin - Earn API (Simple Earn, Lending, Staking)

This mixin contains all Simple Earn, Lending, Staking, ETH Staking, and SOL Staking related methods that use SAPI (Signed API).
"""
from typing import Dict, Any, Optional, TYPE_CHECKING
from ..client import Client

if TYPE_CHECKING:
    from ._core_typing import AsyncClientCoreLike as _AsyncClientCoreLike
else:
    class _AsyncClientCoreLike:
        pass


class AsyncSapiEarnMixin(_AsyncClientCoreLike):
    """
    Earn API Mixin
    
    This mixin provides all Simple Earn, Lending, Staking, ETH Staking, and SOL Staking related methods.
    These methods depend on AsyncClientCore for request infrastructure.
    """

    # Simple Earn Endpoints

    async def get_simple_earn_flexible_product_list(self, **params):
        return await self._request_margin_api(
            "get", "simple-earn/flexible/list", signed=True, data=params
        )

    get_simple_earn_flexible_product_list.__doc__ = (
        Client.get_simple_earn_flexible_product_list.__doc__
    )

    async def get_simple_earn_locked_product_list(self, **params):
        return await self._request_margin_api(
            "get", "simple-earn/locked/list", signed=True, data=params
        )

    get_simple_earn_locked_product_list.__doc__ = (
        Client.get_simple_earn_locked_product_list.__doc__
    )

    async def subscribe_simple_earn_flexible_product(self, **params):
        return await self._request_margin_api(
            "post", "simple-earn/flexible/subscribe", signed=True, data=params
        )

    subscribe_simple_earn_flexible_product.__doc__ = (
        Client.subscribe_simple_earn_flexible_product.__doc__
    )

    async def subscribe_simple_earn_locked_product(self, **params):
        return await self._request_margin_api(
            "post", "simple-earn/locked/subscribe", signed=True, data=params
        )

    subscribe_simple_earn_locked_product.__doc__ = (
        Client.subscribe_simple_earn_locked_product.__doc__
    )

    async def redeem_simple_earn_flexible_product(self, **params):
        return await self._request_margin_api(
            "post", "simple-earn/flexible/redeem", signed=True, data=params
        )

    redeem_simple_earn_flexible_product.__doc__ = (
        Client.redeem_simple_earn_flexible_product.__doc__
    )

    async def redeem_simple_earn_locked_product(self, **params):
        return await self._request_margin_api(
            "post", "simple-earn/locked/redeem", signed=True, data=params
        )

    redeem_simple_earn_locked_product.__doc__ = (
        Client.redeem_simple_earn_locked_product.__doc__
    )

    async def get_simple_earn_flexible_product_position(self, **params):
        return await self._request_margin_api(
            "get", "simple-earn/flexible/position", signed=True, data=params
        )

    get_simple_earn_flexible_product_position.__doc__ = (
        Client.get_simple_earn_flexible_product_position.__doc__
    )

    async def get_simple_earn_locked_product_position(self, **params):
        return await self._request_margin_api(
            "get", "simple-earn/locked/position", signed=True, data=params
        )

    get_simple_earn_locked_product_position.__doc__ = (
        Client.get_simple_earn_locked_product_position.__doc__
    )

    async def get_simple_earn_account(self, **params):
        return await self._request_margin_api(
            "get", "simple-earn/account", signed=True, data=params
        )

    get_simple_earn_account.__doc__ = Client.get_simple_earn_account.__doc__

    # Lending Endpoints

    async def get_fixed_activity_project_list(self, **params):
        return await self._request_margin_api(
            "get", "lending/project/list", signed=True, data=params
        )

    async def change_fixed_activity_to_daily_position(self, **params):
        return await self._request_margin_api(
            "post", "lending/positionChanged", signed=True, data=params
        )

    # Staking Endpoints

    async def get_staking_product_list(self, **params):
        return await self._request_margin_api(
            "get", "staking/productList", signed=True, data=params
        )

    async def purchase_staking_product(self, **params):
        return await self._request_margin_api(
            "post", "staking/purchase", signed=True, data=params
        )

    async def redeem_staking_product(self, **params):
        return await self._request_margin_api(
            "post", "staking/redeem", signed=True, data=params
        )

    async def get_staking_position(self, **params):
        return await self._request_margin_api(
            "get", "staking/position", signed=True, data=params
        )

    async def get_staking_purchase_history(self, **params):
        return await self._request_margin_api(
            "get", "staking/purchaseRecord", signed=True, data=params
        )

    async def set_auto_staking(self, **params):
        return await self._request_margin_api(
            "post", "staking/setAutoStaking", signed=True, data=params
        )

    async def get_personal_left_quota(self, **params):
        return await self._request_margin_api(
            "get", "staking/personalLeftQuota", signed=True, data=params
        )

    # US Staking Endpoints

    async def get_staking_asset_us(self, **params):
        assert self.tld == "us", "Endpoint only available on binance.us"
        return await self._request_margin_api("get", "staking/asset", True, data=params)

    get_staking_asset_us.__doc__ = Client.get_staking_asset_us.__doc__

    async def stake_asset_us(self, **params):
        assert self.tld == "us", "Endpoint only available on binance.us"
        return await self._request_margin_api(
            "post", "staking/stake", True, data=params
        )

    stake_asset_us.__doc__ = Client.stake_asset_us.__doc__

    async def unstake_asset_us(self, **params):
        assert self.tld == "us", "Endpoint only available on binance.us"
        return await self._request_margin_api(
            "post", "staking/unstake", True, data=params
        )

    unstake_asset_us.__doc__ = Client.unstake_asset_us.__doc__

    async def get_staking_balance_us(self, **params):
        assert self.tld == "us", "Endpoint only available on binance.us"
        return await self._request_margin_api(
            "get", "staking/stakingBalance", True, data=params
        )

    get_staking_balance_us.__doc__ = Client.get_staking_balance_us.__doc__

    async def get_staking_history_us(self, **params):
        assert self.tld == "us", "Endpoint only available on binance.us"
        return await self._request_margin_api(
            "get", "staking/history", True, data=params
        )

    get_staking_history_us.__doc__ = Client.get_staking_history_us.__doc__

    async def get_staking_rewards_history_us(self, **params):
        assert self.tld == "us", "Endpoint only available on binance.us"
        return await self._request_margin_api(
            "get", "staking/stakingRewardsHistory", True, data=params
        )

    get_staking_rewards_history_us.__doc__ = (
        Client.get_staking_rewards_history_us.__doc__
    )

    # Versioned Earn Endpoints

    async def margin_v1_get_simple_earn_flexible_history_subscription_record(
        self, **params
    ):
        return await self._request_margin_api(
            "get",
            "simple-earn/flexible/history/subscriptionRecord",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_simple_earn_flexible_history_subscription_record.__doc__ = (
        Client.margin_v1_get_simple_earn_flexible_history_subscription_record.__doc__
    )

    async def margin_v1_post_lending_auto_invest_one_off(self, **params):
        return await self._request_margin_api(
            "post", "lending/auto-invest/one-off", signed=True, data=params, version=1
        )

    margin_v1_post_lending_auto_invest_one_off.__doc__ = (
        Client.margin_v1_post_lending_auto_invest_one_off.__doc__
    )

    async def margin_v1_get_lending_auto_invest_plan_id(self, **params):
        return await self._request_margin_api(
            "get", "lending/auto-invest/plan/id", signed=True, data=params, version=1
        )

    margin_v1_get_lending_auto_invest_plan_id.__doc__ = (
        Client.margin_v1_get_lending_auto_invest_plan_id.__doc__
    )

    async def margin_v1_get_lending_auto_invest_target_asset_list(self, **params):
        return await self._request_margin_api(
            "get",
            "lending/auto-invest/target-asset/list",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_lending_auto_invest_target_asset_list.__doc__ = (
        Client.margin_v1_get_lending_auto_invest_target_asset_list.__doc__
    )

    async def margin_v1_post_sol_staking_sol_redeem(self, **params):
        return await self._request_margin_api(
            "post", "sol-staking/sol/redeem", signed=True, data=params, version=1
        )

    margin_v1_post_sol_staking_sol_redeem.__doc__ = (
        Client.margin_v1_post_sol_staking_sol_redeem.__doc__
    )

    async def margin_v2_get_eth_staking_account(self, **params):
        return await self._request_margin_api(
            "get", "eth-staking/account", signed=True, data=params, version=2
        )

    margin_v2_get_eth_staking_account.__doc__ = (
        Client.margin_v2_get_eth_staking_account.__doc__
    )

    async def margin_v1_post_eth_staking_wbeth_unwrap(self, **params):
        return await self._request_margin_api(
            "post", "eth-staking/wbeth/unwrap", signed=True, data=params, version=1
        )

    margin_v1_post_eth_staking_wbeth_unwrap.__doc__ = (
        Client.margin_v1_post_eth_staking_wbeth_unwrap.__doc__
    )

    async def margin_v1_get_eth_staking_eth_history_staking_history(self, **params):
        return await self._request_margin_api(
            "get",
            "eth-staking/eth/history/stakingHistory",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_eth_staking_eth_history_staking_history.__doc__ = (
        Client.margin_v1_get_eth_staking_eth_history_staking_history.__doc__
    )

    async def margin_v1_get_eth_staking_eth_history_rate_history(self, **params):
        """
        Get WBETH exchange rate history data

        :param params: Query parameters, including:
            - current: Current page, starting from 1
            - size: Page size, maximum 100
            - startTime: Start timestamp (milliseconds)
            - endTime: End timestamp (milliseconds)
        :return: Response containing exchange rate history data
        """
        return await self._request_margin_api(
            "get",
            "eth-staking/eth/history/rateHistory",
            signed=True,
            data=params,
            version=1,
        )

    async def margin_v1_get_staking_staking_record(self, **params):
        return await self._request_margin_api(
            "get", "staking/stakingRecord", signed=True, data=params, version=1
        )

    margin_v1_get_staking_staking_record.__doc__ = (
        Client.margin_v1_get_staking_staking_record.__doc__
    )

    async def margin_v1_get_eth_staking_eth_history_redemption_history(self, **params):
        return await self._request_margin_api(
            "get",
            "eth-staking/eth/history/redemptionHistory",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_eth_staking_eth_history_redemption_history.__doc__ = (
        Client.margin_v1_get_eth_staking_eth_history_redemption_history.__doc__
    )

    async def margin_v1_get_eth_staking_eth_history_wbeth_rewards_history(
        self, **params
    ):
        return await self._request_margin_api(
            "get",
            "eth-staking/eth/history/wbethRewardsHistory",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_eth_staking_eth_history_wbeth_rewards_history.__doc__ = (
        Client.margin_v1_get_eth_staking_eth_history_wbeth_rewards_history.__doc__
    )

    async def margin_v1_get_lending_auto_invest_all_asset(self, **params):
        return await self._request_margin_api(
            "get", "lending/auto-invest/all/asset", signed=True, data=params, version=1
        )

    margin_v1_get_lending_auto_invest_all_asset.__doc__ = (
        Client.margin_v1_get_lending_auto_invest_all_asset.__doc__
    )

    async def margin_v1_get_lending_auto_invest_history_list(self, **params):
        return await self._request_margin_api(
            "get",
            "lending/auto-invest/history/list",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_lending_auto_invest_history_list.__doc__ = (
        Client.margin_v1_get_lending_auto_invest_history_list.__doc__
    )

    async def margin_v1_get_lending_auto_invest_index_info(self, **params):
        return await self._request_margin_api(
            "get", "lending/auto-invest/index/info", signed=True, data=params, version=1
        )

    margin_v1_get_lending_auto_invest_index_info.__doc__ = (
        Client.margin_v1_get_lending_auto_invest_index_info.__doc__
    )

    async def margin_v1_get_lending_auto_invest_index_user_summary(self, **params):
        return await self._request_margin_api(
            "get",
            "lending/auto-invest/index/user-summary",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_lending_auto_invest_index_user_summary.__doc__ = (
        Client.margin_v1_get_lending_auto_invest_index_user_summary.__doc__
    )

    async def margin_v1_get_lending_auto_invest_one_off_status(self, **params):
        return await self._request_margin_api(
            "get",
            "lending/auto-invest/one-off/status",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_lending_auto_invest_one_off_status.__doc__ = (
        Client.margin_v1_get_lending_auto_invest_one_off_status.__doc__
    )

    async def margin_v1_get_lending_auto_invest_plan_list(self, **params):
        return await self._request_margin_api(
            "get", "lending/auto-invest/plan/list", signed=True, data=params, version=1
        )

    margin_v1_get_lending_auto_invest_plan_list.__doc__ = (
        Client.margin_v1_get_lending_auto_invest_plan_list.__doc__
    )

    async def margin_v1_get_lending_auto_invest_rebalance_history(self, **params):
        return await self._request_margin_api(
            "get",
            "lending/auto-invest/rebalance/history",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_lending_auto_invest_rebalance_history.__doc__ = (
        Client.margin_v1_get_lending_auto_invest_rebalance_history.__doc__
    )

    async def margin_v1_get_lending_auto_invest_redeem_history(self, **params):
        return await self._request_margin_api(
            "get",
            "lending/auto-invest/redeem/history",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_lending_auto_invest_redeem_history.__doc__ = (
        Client.margin_v1_get_lending_auto_invest_redeem_history.__doc__
    )

    async def margin_v1_get_lending_auto_invest_source_asset_list(self, **params):
        return await self._request_margin_api(
            "get",
            "lending/auto-invest/source-asset/list",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_lending_auto_invest_source_asset_list.__doc__ = (
        Client.margin_v1_get_lending_auto_invest_source_asset_list.__doc__
    )

    async def margin_v1_get_lending_auto_invest_target_asset_roi_list(self, **params):
        return await self._request_margin_api(
            "get",
            "lending/auto-invest/target-asset/roi/list",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_lending_auto_invest_target_asset_roi_list.__doc__ = (
        Client.margin_v1_get_lending_auto_invest_target_asset_roi_list.__doc__
    )

    async def margin_v1_get_simple_earn_flexible_history_redemption_record(
        self, **params
    ):
        return await self._request_margin_api(
            "get",
            "simple-earn/flexible/history/redemptionRecord",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_simple_earn_flexible_history_redemption_record.__doc__ = (
        Client.margin_v1_get_simple_earn_flexible_history_redemption_record.__doc__
    )

    async def margin_v1_get_simple_earn_locked_history_redemption_record(
        self, **params
    ):
        return await self._request_margin_api(
            "get",
            "simple-earn/locked/history/redemptionRecord",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_simple_earn_locked_history_redemption_record.__doc__ = (
        Client.margin_v1_get_simple_earn_locked_history_redemption_record.__doc__
    )

    async def margin_v1_get_simple_earn_locked_history_subscription_record(
        self, **params
    ):
        return await self._request_margin_api(
            "get",
            "simple-earn/locked/history/subscriptionRecord",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_simple_earn_locked_history_subscription_record.__doc__ = (
        Client.margin_v1_get_simple_earn_locked_history_subscription_record.__doc__
    )

    async def margin_v1_get_sol_staking_account(self, **params):
        return await self._request_margin_api(
            "get", "sol-staking/account", signed=True, data=params, version=1
        )

    margin_v1_get_sol_staking_account.__doc__ = (
        Client.margin_v1_get_sol_staking_account.__doc__
    )

    async def margin_v1_get_sol_staking_sol_history_bnsol_rewards_history(
        self, **params
    ):
        return await self._request_margin_api(
            "get",
            "sol-staking/sol/history/bnsolRewardsHistory",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_sol_staking_sol_history_bnsol_rewards_history.__doc__ = (
        Client.margin_v1_get_sol_staking_sol_history_bnsol_rewards_history.__doc__
    )

    async def margin_v1_get_sol_staking_sol_history_boost_rewards_history(
        self, **params
    ):
        return await self._request_margin_api(
            "get",
            "sol-staking/sol/history/boostRewardsHistory",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_sol_staking_sol_history_boost_rewards_history.__doc__ = (
        Client.margin_v1_get_sol_staking_sol_history_boost_rewards_history.__doc__
    )

    async def margin_v1_get_sol_staking_sol_history_rate_history(self, **params):
        return await self._request_margin_api(
            "get",
            "sol-staking/sol/history/rateHistory",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_sol_staking_sol_history_rate_history.__doc__ = (
        Client.margin_v1_get_sol_staking_sol_history_rate_history.__doc__
    )

    async def margin_v1_get_sol_staking_sol_history_redemption_history(self, **params):
        return await self._request_margin_api(
            "get",
            "sol-staking/sol/history/redemptionHistory",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_sol_staking_sol_history_redemption_history.__doc__ = (
        Client.margin_v1_get_sol_staking_sol_history_redemption_history.__doc__
    )

    async def margin_v1_get_sol_staking_sol_history_staking_history(self, **params):
        return await self._request_margin_api(
            "get",
            "sol-staking/sol/history/stakingHistory",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_sol_staking_sol_history_staking_history.__doc__ = (
        Client.margin_v1_get_sol_staking_sol_history_staking_history.__doc__
    )

    async def margin_v1_get_sol_staking_sol_history_unclaimed_rewards(self, **params):
        return await self._request_margin_api(
            "get",
            "sol-staking/sol/history/unclaimedRewards",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_sol_staking_sol_history_unclaimed_rewards.__doc__ = (
        Client.margin_v1_get_sol_staking_sol_history_unclaimed_rewards.__doc__
    )

    async def margin_v1_get_sol_staking_sol_quota(self, **params):
        return await self._request_margin_api(
            "get", "sol-staking/sol/quota", signed=True, data=params, version=1
        )

    margin_v1_get_sol_staking_sol_quota.__doc__ = (
        Client.margin_v1_get_sol_staking_sol_quota.__doc__
    )

    async def margin_v1_post_eth_staking_eth_redeem(self, **params):
        return await self._request_margin_api(
            "post", "eth-staking/eth/redeem", signed=True, data=params, version=1
        )

    margin_v1_post_eth_staking_eth_redeem.__doc__ = (
        Client.margin_v1_post_eth_staking_eth_redeem.__doc__
    )

    async def margin_v1_post_eth_staking_wbeth_wrap(self, **params):
        return await self._request_margin_api(
            "post", "eth-staking/wbeth/wrap", signed=True, data=params, version=1
        )

    margin_v1_post_eth_staking_wbeth_wrap.__doc__ = (
        Client.margin_v1_post_eth_staking_wbeth_wrap.__doc__
    )

    async def margin_v1_post_lending_auto_invest_plan_add(self, **params):
        return await self._request_margin_api(
            "post", "lending/auto-invest/plan/add", signed=True, data=params, version=1
        )

    margin_v1_post_lending_auto_invest_plan_add.__doc__ = (
        Client.margin_v1_post_lending_auto_invest_plan_add.__doc__
    )

    async def margin_v1_post_lending_auto_invest_plan_edit_status(self, **params):
        return await self._request_margin_api(
            "post",
            "lending/auto-invest/plan/edit-status",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_lending_auto_invest_plan_edit_status.__doc__ = (
        Client.margin_v1_post_lending_auto_invest_plan_edit_status.__doc__
    )

    async def margin_v1_post_lending_auto_invest_redeem(self, **params):
        return await self._request_margin_api(
            "post", "lending/auto-invest/redeem", signed=True, data=params, version=1
        )

    margin_v1_post_lending_auto_invest_redeem.__doc__ = (
        Client.margin_v1_post_lending_auto_invest_redeem.__doc__
    )

    async def margin_v1_post_lending_customized_fixed_purchase(self, **params):
        return await self._request_margin_api(
            "post",
            "lending/customizedFixed/purchase",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_lending_customized_fixed_purchase.__doc__ = (
        Client.margin_v1_post_lending_customized_fixed_purchase.__doc__
    )

    async def margin_v1_post_lending_daily_purchase(self, **params):
        return await self._request_margin_api(
            "post", "lending/daily/purchase", signed=True, data=params, version=1
        )

    margin_v1_post_lending_daily_purchase.__doc__ = (
        Client.margin_v1_post_lending_daily_purchase.__doc__
    )

    async def margin_v1_post_lending_daily_redeem(self, **params):
        return await self._request_margin_api(
            "post", "lending/daily/redeem", signed=True, data=params, version=1
        )

    margin_v1_post_lending_daily_redeem.__doc__ = (
        Client.margin_v1_post_lending_daily_redeem.__doc__
    )

    async def margin_v1_post_simple_earn_locked_set_redeem_option(self, **params):
        return await self._request_margin_api(
            "post",
            "simple-earn/locked/setRedeemOption",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_simple_earn_locked_set_redeem_option.__doc__ = (
        Client.margin_v1_post_simple_earn_locked_set_redeem_option.__doc__
    )

    async def margin_v1_post_sol_staking_sol_claim(self, **params):
        return await self._request_margin_api(
            "post", "sol-staking/sol/claim", signed=True, data=params, version=1
        )

    margin_v1_post_sol_staking_sol_claim.__doc__ = (
        Client.margin_v1_post_sol_staking_sol_claim.__doc__
    )

    async def margin_v1_post_sol_staking_sol_stake(self, **params):
        return await self._request_margin_api(
            "post", "sol-staking/sol/stake", signed=True, data=params, version=1
        )

    margin_v1_post_sol_staking_sol_stake.__doc__ = (
        Client.margin_v1_post_sol_staking_sol_stake.__doc__
    )

    async def margin_v2_post_eth_staking_eth_stake(self, **params):
        return await self._request_margin_api(
            "post", "eth-staking/eth/stake", signed=True, data=params, version=2
        )

    margin_v2_post_eth_staking_eth_stake.__doc__ = (
        Client.margin_v2_post_eth_staking_eth_stake.__doc__
    )
