"""
AsyncSapiSubAccountBrokerMixin - Sub Account & Broker API

This mixin contains all Sub Account, Broker, and Managed Sub Account related methods that use SAPI (Signed API).
"""
from typing import Dict, Any, Optional, TYPE_CHECKING
from ..client import Client

if TYPE_CHECKING:
    from ._core_typing import AsyncClientCoreLike as _AsyncClientCoreLike
else:
    class _AsyncClientCoreLike:
        pass


class AsyncSapiSubAccountBrokerMixin(_AsyncClientCoreLike):
    """
    Sub Account & Broker API Mixin
    
    This mixin provides all Sub Account, Broker, and Managed Sub Account related methods.
    These methods depend on AsyncClientCore for request infrastructure.
    """

    # Sub Accounts

    async def get_sub_account_list(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/list", True, data=params
        )

    async def get_sub_account_transfer_history(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/sub/transfer/history", True, data=params
        )

    async def get_sub_account_futures_transfer_history(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/futures/internalTransfer", True, data=params
        )

    async def create_sub_account_futures_transfer(self, **params):
        return await self._request_margin_api(
            "post", "sub-account/futures/internalTransfer", True, data=params
        )

    async def get_sub_account_assets(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/assets", True, data=params, version=4
        )

    async def query_subaccount_spot_summary(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/spotSummary", True, data=params
        )

    async def get_subaccount_deposit_address(self, **params):
        return await self._request_margin_api(
            "get", "capital/deposit/subAddress", True, data=params
        )

    async def get_subaccount_deposit_history(self, **params):
        return await self._request_margin_api(
            "get", "capital/deposit/subHisrec", True, data=params
        )

    async def get_subaccount_futures_margin_status(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/status", True, data=params
        )

    async def enable_subaccount_margin(self, **params):
        return await self._request_margin_api(
            "post", "sub-account/margin/enable", True, data=params
        )

    async def get_subaccount_margin_details(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/margin/account", True, data=params
        )

    async def get_subaccount_margin_summary(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/margin/accountSummary", True, data=params
        )

    async def enable_subaccount_futures(self, **params):
        return await self._request_margin_api(
            "post", "sub-account/futures/enable", True, data=params
        )

    async def get_subaccount_futures_details(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/futures/account", True, data=params, version=2
        )

    async def get_subaccount_futures_summary(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/futures/accountSummary", True, data=params, version=2
        )

    async def get_subaccount_futures_positionrisk(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/futures/positionRisk", True, data=params, version=2
        )

    async def make_subaccount_futures_transfer(self, **params):
        return await self._request_margin_api(
            "post", "sub-account/futures/transfer", True, data=params
        )

    async def make_subaccount_margin_transfer(self, **params):
        return await self._request_margin_api(
            "post", "sub-account/margin/transfer", True, data=params
        )

    async def make_subaccount_to_subaccount_transfer(self, **params):
        return await self._request_margin_api(
            "post", "sub-account/transfer/subToSub", True, data=params
        )

    async def make_subaccount_to_master_transfer(self, **params):
        return await self._request_margin_api(
            "post", "sub-account/transfer/subToMaster", True, data=params
        )

    async def get_subaccount_transfer_history(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/transfer/subUserHistory", True, data=params
        )

    async def make_subaccount_universal_transfer(self, **params):
        return await self._request_margin_api(
            "post", "sub-account/universalTransfer", True, data=params
        )

    async def get_universal_transfer_history(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/universalTransfer", True, data=params
        )

    # Versioned Sub Account Endpoints

    async def margin_v1_post_sub_account_eoptions_enable(self, **params):
        return await self._request_margin_api(
            "post", "sub-account/eoptions/enable", signed=True, data=params, version=1
        )

    margin_v1_post_sub_account_eoptions_enable.__doc__ = (
        Client.margin_v1_post_sub_account_eoptions_enable.__doc__
    )

    # Broker Endpoints

    async def margin_v1_post_broker_sub_account_api_commission_coin_futures(
        self, **params
    ):
        return await self._request_margin_api(
            "post",
            "broker/subAccountApi/commission/coinFutures",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_broker_sub_account_api_commission_coin_futures.__doc__ = (
        Client.margin_v1_post_broker_sub_account_api_commission_coin_futures.__doc__
    )

    async def margin_v1_post_broker_sub_account_blvt(self, **params):
        return await self._request_margin_api(
            "post", "broker/subAccount/blvt", signed=True, data=params, version=1
        )

    margin_v1_post_broker_sub_account_blvt.__doc__ = (
        Client.margin_v1_post_broker_sub_account_blvt.__doc__
    )

    async def margin_v1_post_broker_sub_account_api_permission(self, **params):
        return await self._request_margin_api(
            "post",
            "broker/subAccountApi/permission",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_broker_sub_account_api_permission.__doc__ = (
        Client.margin_v1_post_broker_sub_account_api_permission.__doc__
    )

    async def margin_v1_post_broker_sub_account_api(self, **params):
        return await self._request_margin_api(
            "post", "broker/subAccountApi", signed=True, data=params, version=1
        )

    margin_v1_post_broker_sub_account_api.__doc__ = (
        Client.margin_v1_post_broker_sub_account_api.__doc__
    )

    async def margin_v1_get_broker_sub_account(self, **params):
        return await self._request_margin_api(
            "get", "broker/subAccount", signed=True, data=params, version=1
        )

    margin_v1_get_broker_sub_account.__doc__ = (
        Client.margin_v1_get_broker_sub_account.__doc__
    )

    async def margin_v1_get_broker_sub_account_api_ip_restriction(self, **params):
        return await self._request_margin_api(
            "get",
            "broker/subAccountApi/ipRestriction",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_broker_sub_account_api_ip_restriction.__doc__ = (
        Client.margin_v1_get_broker_sub_account_api_ip_restriction.__doc__
    )

    async def margin_v1_post_broker_sub_account_bnb_burn_margin_interest(
        self, **params
    ):
        return await self._request_margin_api(
            "post",
            "broker/subAccount/bnbBurn/marginInterest",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_broker_sub_account_bnb_burn_margin_interest.__doc__ = (
        Client.margin_v1_post_broker_sub_account_bnb_burn_margin_interest.__doc__
    )

    async def margin_v1_get_broker_transfer_futures(self, **params):
        return await self._request_margin_api(
            "get", "broker/transfer/futures", signed=True, data=params, version=1
        )

    margin_v1_get_broker_transfer_futures.__doc__ = (
        Client.margin_v1_get_broker_transfer_futures.__doc__
    )

    async def margin_v1_get_broker_rebate_recent_record(self, **params):
        return await self._request_margin_api(
            "get", "broker/rebate/recentRecord", signed=True, data=params, version=1
        )

    margin_v1_get_broker_rebate_recent_record.__doc__ = (
        Client.margin_v1_get_broker_rebate_recent_record.__doc__
    )

    # Managed Sub Account Endpoints

    async def margin_v1_get_managed_subaccount_query_trans_log_for_investor(
        self, **params
    ):
        return await self._request_margin_api(
            "get",
            "managed-subaccount/queryTransLogForInvestor",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_managed_subaccount_query_trans_log_for_investor.__doc__ = (
        Client.margin_v1_get_managed_subaccount_query_trans_log_for_investor.__doc__
    )

    async def margin_v1_delete_broker_sub_account_api(self, **params):
        return await self._request_margin_api(
            "delete", "broker/subAccountApi", signed=True, data=params, version=1
        )

    margin_v1_delete_broker_sub_account_api.__doc__ = (
        Client.margin_v1_delete_broker_sub_account_api.__doc__
    )

    async def margin_v1_delete_broker_sub_account_api_ip_restriction_ip_list(
        self, **params
    ):
        return await self._request_margin_api(
            "delete",
            "broker/subAccountApi/ipRestriction/ipList",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_delete_broker_sub_account_api_ip_restriction_ip_list.__doc__ = (
        Client.margin_v1_delete_broker_sub_account_api_ip_restriction_ip_list.__doc__
    )


    async def margin_v1_delete_sub_account_sub_account_api_ip_restriction_ip_list(
        self, **params
    ):
        return await self._request_margin_api(
            "delete",
            "sub-account/subAccountApi/ipRestriction/ipList",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_delete_sub_account_sub_account_api_ip_restriction_ip_list.__doc__ = (
        Client.margin_v1_delete_sub_account_sub_account_api_ip_restriction_ip_list.__doc__
    )

    async def margin_v1_get_broker_rebate_futures_recent_record(self, **params):
        return await self._request_margin_api(
            "get",
            "broker/rebate/futures/recentRecord",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_broker_rebate_futures_recent_record.__doc__ = (
        Client.margin_v1_get_broker_rebate_futures_recent_record.__doc__
    )

    async def margin_v1_get_broker_rebate_historical_record(self, **params):
        return await self._request_margin_api(
            "get", "broker/rebate/historicalRecord", signed=True, data=params, version=1
        )

    margin_v1_get_broker_rebate_historical_record.__doc__ = (
        Client.margin_v1_get_broker_rebate_historical_record.__doc__
    )

    async def margin_v1_get_broker_sub_account_api(self, **params):
        return await self._request_margin_api(
            "get", "broker/subAccountApi", signed=True, data=params, version=1
        )

    margin_v1_get_broker_sub_account_api.__doc__ = (
        Client.margin_v1_get_broker_sub_account_api.__doc__
    )

    async def margin_v1_get_broker_sub_account_api_commission_coin_futures(
        self, **params
    ):
        return await self._request_margin_api(
            "get",
            "broker/subAccountApi/commission/coinFutures",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_broker_sub_account_api_commission_coin_futures.__doc__ = (
        Client.margin_v1_get_broker_sub_account_api_commission_coin_futures.__doc__
    )

    async def margin_v1_get_broker_sub_account_api_commission_futures(self, **params):
        return await self._request_margin_api(
            "get",
            "broker/subAccountApi/commission/futures",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_broker_sub_account_api_commission_futures.__doc__ = (
        Client.margin_v1_get_broker_sub_account_api_commission_futures.__doc__
    )

    async def margin_v1_get_broker_sub_account_bnb_burn_status(self, **params):
        return await self._request_margin_api(
            "get",
            "broker/subAccount/bnbBurn/status",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_broker_sub_account_bnb_burn_status.__doc__ = (
        Client.margin_v1_get_broker_sub_account_bnb_burn_status.__doc__
    )

    async def margin_v1_get_broker_sub_account_deposit_hist(self, **params):
        return await self._request_margin_api(
            "get", "broker/subAccount/depositHist", signed=True, data=params, version=1
        )

    margin_v1_get_broker_sub_account_deposit_hist.__doc__ = (
        Client.margin_v1_get_broker_sub_account_deposit_hist.__doc__
    )

    async def margin_v1_get_broker_sub_account_futures_summary(self, **params):
        return await self._request_margin_api(
            "get",
            "broker/subAccount/futuresSummary",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_broker_sub_account_futures_summary.__doc__ = (
        Client.margin_v1_get_broker_sub_account_futures_summary.__doc__
    )

    async def margin_v1_get_broker_sub_account_margin_summary(self, **params):
        return await self._request_margin_api(
            "get",
            "broker/subAccount/marginSummary",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_broker_sub_account_margin_summary.__doc__ = (
        Client.margin_v1_get_broker_sub_account_margin_summary.__doc__
    )

    async def margin_v1_get_broker_sub_account_spot_summary(self, **params):
        return await self._request_margin_api(
            "get", "broker/subAccount/spotSummary", signed=True, data=params, version=1
        )

    margin_v1_get_broker_sub_account_spot_summary.__doc__ = (
        Client.margin_v1_get_broker_sub_account_spot_summary.__doc__
    )

    async def margin_v1_get_broker_transfer(self, **params):
        return await self._request_margin_api(
            "get", "broker/transfer", signed=True, data=params, version=1
        )

    margin_v1_get_broker_transfer.__doc__ = Client.margin_v1_get_broker_transfer.__doc__

    async def margin_v1_get_broker_universal_transfer(self, **params):
        return await self._request_margin_api(
            "get", "broker/universalTransfer", signed=True, data=params, version=1
        )

    margin_v1_get_broker_universal_transfer.__doc__ = (
        Client.margin_v1_get_broker_universal_transfer.__doc__
    )

    async def margin_v1_get_managed_subaccount_account_snapshot(self, **params):
        return await self._request_margin_api(
            "get",
            "managed-subaccount/accountSnapshot",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_managed_subaccount_account_snapshot.__doc__ = (
        Client.margin_v1_get_managed_subaccount_account_snapshot.__doc__
    )

    async def margin_v1_get_managed_subaccount_asset(self, **params):
        return await self._request_margin_api(
            "get", "managed-subaccount/asset", signed=True, data=params, version=1
        )

    margin_v1_get_managed_subaccount_asset.__doc__ = (
        Client.margin_v1_get_managed_subaccount_asset.__doc__
    )

    async def margin_v1_get_managed_subaccount_deposit_address(self, **params):
        return await self._request_margin_api(
            "get",
            "managed-subaccount/deposit/address",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_managed_subaccount_deposit_address.__doc__ = (
        Client.margin_v1_get_managed_subaccount_deposit_address.__doc__
    )

    async def margin_v1_get_managed_subaccount_fetch_future_asset(self, **params):
        return await self._request_margin_api(
            "get",
            "managed-subaccount/fetch-future-asset",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_managed_subaccount_fetch_future_asset.__doc__ = (
        Client.margin_v1_get_managed_subaccount_fetch_future_asset.__doc__
    )

    async def margin_v1_get_managed_subaccount_info(self, **params):
        return await self._request_margin_api(
            "get", "managed-subaccount/info", signed=True, data=params, version=1
        )

    margin_v1_get_managed_subaccount_info.__doc__ = (
        Client.margin_v1_get_managed_subaccount_info.__doc__
    )

    async def margin_v1_get_managed_subaccount_margin_asset(self, **params):
        return await self._request_margin_api(
            "get", "managed-subaccount/marginAsset", signed=True, data=params, version=1
        )

    margin_v1_get_managed_subaccount_margin_asset.__doc__ = (
        Client.margin_v1_get_managed_subaccount_margin_asset.__doc__
    )

    async def margin_v1_get_managed_subaccount_query_trans_log(self, **params):
        return await self._request_margin_api(
            "get",
            "managed-subaccount/query-trans-log",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_managed_subaccount_query_trans_log.__doc__ = (
        Client.margin_v1_get_managed_subaccount_query_trans_log.__doc__
    )

    async def margin_v1_get_sub_account_sub_account_api_ip_restriction(self, **params):
        return await self._request_margin_api(
            "get",
            "sub-account/subAccountApi/ipRestriction",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_sub_account_sub_account_api_ip_restriction.__doc__ = (
        Client.margin_v1_get_sub_account_sub_account_api_ip_restriction.__doc__
    )

    async def margin_v1_get_sub_account_transaction_statistics(self, **params):
        return await self._request_margin_api(
            "get",
            "sub-account/transaction-statistics",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_sub_account_transaction_statistics.__doc__ = (
        Client.margin_v1_get_sub_account_transaction_statistics.__doc__
    )

    async def margin_v1_post_broker_sub_account(self, **params):
        return await self._request_margin_api(
            "post", "broker/subAccount", signed=True, data=params, version=1
        )

    margin_v1_post_broker_sub_account.__doc__ = (
        Client.margin_v1_post_broker_sub_account.__doc__
    )

    async def margin_v1_post_broker_sub_account_api_commission(self, **params):
        return await self._request_margin_api(
            "post",
            "broker/subAccountApi/commission",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_broker_sub_account_api_commission.__doc__ = (
        Client.margin_v1_post_broker_sub_account_api_commission.__doc__
    )

    async def margin_v1_post_broker_sub_account_api_commission_futures(self, **params):
        return await self._request_margin_api(
            "post",
            "broker/subAccountApi/commission/futures",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_broker_sub_account_api_commission_futures.__doc__ = (
        Client.margin_v1_post_broker_sub_account_api_commission_futures.__doc__
    )

    async def margin_v1_post_broker_sub_account_api_ip_restriction(self, **params):
        return await self._request_margin_api(
            "post",
            "broker/subAccountApi/ipRestriction",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_broker_sub_account_api_ip_restriction.__doc__ = (
        Client.margin_v1_post_broker_sub_account_api_ip_restriction.__doc__
    )

    async def margin_v1_post_broker_sub_account_bnb_burn_spot(self, **params):
        return await self._request_margin_api(
            "post",
            "broker/subAccount/bnbBurn/spot",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_broker_sub_account_bnb_burn_spot.__doc__ = (
        Client.margin_v1_post_broker_sub_account_bnb_burn_spot.__doc__
    )

    async def margin_v1_post_broker_transfer(self, **params):
        return await self._request_margin_api(
            "post", "broker/transfer", signed=True, data=params, version=1
        )

    margin_v1_post_broker_transfer.__doc__ = (
        Client.margin_v1_post_broker_transfer.__doc__
    )

    async def margin_v1_post_broker_transfer_futures(self, **params):
        return await self._request_margin_api(
            "post", "broker/transfer/futures", signed=True, data=params, version=1
        )

    margin_v1_post_broker_transfer_futures.__doc__ = (
        Client.margin_v1_post_broker_transfer_futures.__doc__
    )

    async def margin_v1_post_broker_universal_transfer(self, **params):
        return await self._request_margin_api(
            "post", "broker/universalTransfer", signed=True, data=params, version=1
        )

    margin_v1_post_broker_universal_transfer.__doc__ = (
        Client.margin_v1_post_broker_universal_transfer.__doc__
    )

    async def margin_v1_post_managed_subaccount_deposit(self, **params):
        return await self._request_margin_api(
            "post", "managed-subaccount/deposit", signed=True, data=params, version=1
        )

    margin_v1_post_managed_subaccount_deposit.__doc__ = (
        Client.margin_v1_post_managed_subaccount_deposit.__doc__
    )

    async def margin_v1_post_managed_subaccount_withdraw(self, **params):
        return await self._request_margin_api(
            "post", "managed-subaccount/withdraw", signed=True, data=params, version=1
        )

    margin_v1_post_managed_subaccount_withdraw.__doc__ = (
        Client.margin_v1_post_managed_subaccount_withdraw.__doc__
    )

    async def margin_v1_post_sub_account_blvt_enable(self, **params):
        return await self._request_margin_api(
            "post", "sub-account/blvt/enable", signed=True, data=params, version=1
        )

    margin_v1_post_sub_account_blvt_enable.__doc__ = (
        Client.margin_v1_post_sub_account_blvt_enable.__doc__
    )

    async def margin_v1_post_sub_account_sub_account_api_ip_restriction(self, **params):
        return await self._request_margin_api(
            "post",
            "sub-account/subAccountApi/ipRestriction",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_sub_account_sub_account_api_ip_restriction.__doc__ = (
        Client.margin_v1_post_sub_account_sub_account_api_ip_restriction.__doc__
    )

    async def margin_v1_post_sub_account_virtual_sub_account(self, **params):
        return await self._request_margin_api(
            "post", "sub-account/virtualSubAccount", signed=True, data=params, version=1
        )

    margin_v1_post_sub_account_virtual_sub_account.__doc__ = (
        Client.margin_v1_post_sub_account_virtual_sub_account.__doc__
    )

    async def margin_v2_get_broker_sub_account_futures_summary(self, **params):
        return await self._request_margin_api(
            "get",
            "broker/subAccount/futuresSummary",
            signed=True,
            data=params,
            version=2,
        )

    margin_v2_get_broker_sub_account_futures_summary.__doc__ = (
        Client.margin_v2_get_broker_sub_account_futures_summary.__doc__
    )

    async def margin_v2_post_broker_sub_account_api_ip_restriction(self, **params):
        return await self._request_margin_api(
            "post",
            "broker/subAccountApi/ipRestriction",
            signed=True,
            data=params,
            version=2,
        )

    margin_v2_post_broker_sub_account_api_ip_restriction.__doc__ = (
        Client.margin_v2_post_broker_sub_account_api_ip_restriction.__doc__
    )

    async def margin_v2_post_sub_account_sub_account_api_ip_restriction(self, **params):
        return await self._request_margin_api(
            "post",
            "sub-account/subAccountApi/ipRestriction",
            signed=True,
            data=params,
            version=2,
        )

    margin_v2_post_sub_account_sub_account_api_ip_restriction.__doc__ = (
        Client.margin_v2_post_sub_account_sub_account_api_ip_restriction.__doc__
    )

    async def margin_v3_get_broker_sub_account_futures_summary(self, **params):
        return await self._request_margin_api(
            "get",
            "broker/subAccount/futuresSummary",
            signed=True,
            data=params,
            version=3,
        )

    margin_v3_get_broker_sub_account_futures_summary.__doc__ = (
        Client.margin_v3_get_broker_sub_account_futures_summary.__doc__
    )

    async def margin_v1_get_managed_subaccount_query_trans_log_for_trade_parent(
        self, **params
    ):
        return await self._request_margin_api(
            "get",
            "managed-subaccount/queryTransLogForTradeParent",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_managed_subaccount_query_trans_log_for_trade_parent.__doc__ = (
        Client.margin_v1_get_managed_subaccount_query_trans_log_for_trade_parent.__doc__
    )

    async def margin_v1_post_broker_sub_account_api_ip_restriction_ip_list(
        self, **params
    ):
        return await self._request_margin_api(
            "post",
            "broker/subAccountApi/ipRestriction/ipList",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_broker_sub_account_api_ip_restriction_ip_list.__doc__ = (
        Client.margin_v1_post_broker_sub_account_api_ip_restriction_ip_list.__doc__
    )

    async def margin_v1_post_broker_sub_account_api_permission_universal_transfer(
        self, **params
    ):
        return await self._request_margin_api(
            "post",
            "broker/subAccountApi/permission/universalTransfer",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_broker_sub_account_api_permission_universal_transfer.__doc__ = (
        Client.margin_v1_post_broker_sub_account_api_permission_universal_transfer.__doc__
    )

    async def margin_v1_post_broker_sub_account_api_permission_vanilla_options(
        self, **params
    ):
        return await self._request_margin_api(
            "post",
            "broker/subAccountApi/permission/vanillaOptions",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_broker_sub_account_api_permission_vanilla_options.__doc__ = (
        Client.margin_v1_post_broker_sub_account_api_permission_vanilla_options.__doc__
    )

    async def margin_v1_post_sub_account_sub_account_api_ip_restriction_ip_list(
        self, **params
    ):
        return await self._request_margin_api(
            "post",
            "sub-account/subAccountApi/ipRestriction/ipList",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_sub_account_sub_account_api_ip_restriction_ip_list.__doc__ = (
        Client.margin_v1_post_sub_account_sub_account_api_ip_restriction_ip_list.__doc__
    )
