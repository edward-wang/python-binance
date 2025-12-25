"""
AsyncSapiWalletCapitalMixin - Wallet & Capital API

This mixin contains all Asset, Capital, Spot delist schedule, and BNB burn related methods that use SAPI (Signed API).
"""
from typing import Dict, Any, Optional, TYPE_CHECKING
from ..client import Client

if TYPE_CHECKING:
    from ._core_typing import AsyncClientCoreLike as _AsyncClientCoreLike
else:
    class _AsyncClientCoreLike:
        pass


class AsyncSapiWalletCapitalMixin(_AsyncClientCoreLike):
    """
    Wallet & Capital API Mixin
    
    This mixin provides all Asset, Capital, Spot delist schedule, and BNB burn related methods.
    These methods depend on AsyncClientCore for request infrastructure.
    """

    async def get_all_coins_info(self, **params):
        return await self._request_margin_api(
            "get", "capital/config/getall", True, data=params
        )

    async def get_account_snapshot(self, **params):
        return await self._request_margin_api(
            "get", "accountSnapshot", True, data=params
        )

    async def disable_fast_withdraw_switch(self, **params):
        return await self._request_margin_api(
            "post", "disableFastWithdrawSwitch", True, data=params
        )

    async def enable_fast_withdraw_switch(self, **params):
        return await self._request_margin_api(
            "post", "enableFastWithdrawSwitch", True, data=params
        )

    async def new_transfer_history(self, **params):
        return await self._request_margin_api(
            "get", "asset/transfer", True, data=params
        )


    async def funding_wallet(self, **params):
        return await self._request_margin_api(
            "post", "asset/get-funding-asset", True, data=params
        )


    async def get_user_asset(self, **params):
        return await self._request_margin_api(
            "post", "asset/getUserAsset", True, data=params, version=3
        )


    async def universal_transfer(self, **params):
        return await self._request_margin_api(
            "post", "asset/transfer", signed=True, data=params
        )

    async def get_dust_assets(self, **params):
        return await self._request_margin_api(
            "post", "asset/dust-btc", True, data=params
        )

    get_dust_assets.__doc__ = Client.get_dust_assets.__doc__

    async def get_dust_log(self, **params):
        return await self._request_margin_api(
            "get", "asset/dribblet", True, data=params
        )

    get_dust_log.__doc__ = Client.get_dust_log.__doc__

    async def transfer_dust(self, **params):
        return await self._request_margin_api("post", "asset/dust", True, data=params)

    transfer_dust.__doc__ = Client.transfer_dust.__doc__

    async def get_asset_dividend_history(self, **params):
        return await self._request_margin_api(
            "get", "asset/assetDividend", True, data=params
        )

    get_asset_dividend_history.__doc__ = Client.get_asset_dividend_history.__doc__

    async def make_universal_transfer(self, **params):
        return await self._request_margin_api(
            "post", "asset/transfer", signed=True, data=params
        )

    make_universal_transfer.__doc__ = Client.make_universal_transfer.__doc__

    async def query_universal_transfer_history(self, **params):
        return await self._request_margin_api(
            "get", "asset/transfer", signed=True, data=params
        )

    query_universal_transfer_history.__doc__ = (
        Client.query_universal_transfer_history.__doc__
    )

    async def get_trade_fee(self, **params):
        if self.tld == "us":
            endpoint = "asset/query/trading-fee"
        else:
            endpoint = "asset/tradeFee"
        return await self._request_margin_api("get", endpoint, True, data=params)

    get_trade_fee.__doc__ = Client.get_trade_fee.__doc__

    async def get_asset_details(self, **params):
        return await self._request_margin_api(
            "get", "asset/assetDetail", True, data=params
        )

    get_asset_details.__doc__ = Client.get_asset_details.__doc__

    async def get_spot_delist_schedule(self, **params):
        return await self._request_margin_api(
            "get", "/spot/delist-schedule", signed=True, data=params
        )

    async def withdraw(self, **params):
        # force a name for the withdrawal if one not set
        if "coin" in params and "name" not in params:
            params["name"] = params["coin"]
        return await self._request_margin_api(
            "post", "capital/withdraw/apply", True, data=params
        )

    withdraw.__doc__ = Client.withdraw.__doc__

    async def get_deposit_history(self, **params):
        return await self._request_margin_api(
            "get", "capital/deposit/hisrec", True, data=params
        )

    get_deposit_history.__doc__ = Client.get_deposit_history.__doc__

    async def get_withdraw_history(self, **params):
        return await self._request_margin_api(
            "get", "capital/withdraw/history", True, data=params
        )

    get_withdraw_history.__doc__ = Client.get_withdraw_history.__doc__

    async def get_withdraw_history_id(self, withdraw_id, **params):
        result = await self.get_withdraw_history(**params)

        for entry in result:
            if isinstance(entry, dict) and entry.get("id") == withdraw_id:
                return entry

        raise Exception("There is no entry with withdraw id", result)

    get_withdraw_history_id.__doc__ = Client.get_withdraw_history_id.__doc__

    async def get_deposit_address(
        self, coin: str, network: Optional[str] = None, **params
    ):
        params["coin"] = coin
        if network:
            params["network"] = network
        return await self._request_margin_api(
            "get", "capital/deposit/address", True, data=params
        )

    get_deposit_address.__doc__ = Client.get_deposit_address.__doc__

    async def toggle_bnb_burn_spot_margin(self, **params):
        return await self._request_margin_api(
            "post", "bnbBurn", signed=True, data=params
        )

    toggle_bnb_burn_spot_margin.__doc__ = Client.toggle_bnb_burn_spot_margin.__doc__

    async def get_bnb_burn_spot_margin(self, **params):
        return await self._request_margin_api(
            "get", "bnbBurn", signed=True, data=params
        )

    get_bnb_burn_spot_margin.__doc__ = Client.get_bnb_burn_spot_margin.__doc__

    async def margin_v1_get_asset_custody_transfer_history(self, **params):
        return await self._request_margin_api(
            "get", "asset/custody/transfer-history", signed=True, data=params, version=1
        )

    margin_v1_get_asset_custody_transfer_history.__doc__ = (
        Client.margin_v1_get_asset_custody_transfer_history.__doc__
    )

    async def margin_v1_get_capital_deposit_address_list(self, **params):
        return await self._request_margin_api(
            "get", "capital/deposit/address/list", signed=True, data=params, version=1
        )

    margin_v1_get_capital_deposit_address_list.__doc__ = (
        Client.margin_v1_get_capital_deposit_address_list.__doc__
    )

    async def margin_v1_get_asset_ledger_transfer_cloud_mining_query_by_page(
        self, **params
    ):
        return await self._request_margin_api(
            "get",
            "asset/ledger-transfer/cloud-mining/queryByPage",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_asset_ledger_transfer_cloud_mining_query_by_page.__doc__ = (
        Client.margin_v1_get_asset_ledger_transfer_cloud_mining_query_by_page.__doc__
    )

    async def margin_v1_get_asset_wallet_balance(self, **params):
        return await self._request_margin_api(
            "get", "asset/wallet/balance", signed=True, data=params, version=1
        )

    margin_v1_get_asset_wallet_balance.__doc__ = (
        Client.margin_v1_get_asset_wallet_balance.__doc__
    )

    async def margin_v1_get_capital_contract_convertible_coins(self, **params):
        return await self._request_margin_api(
            "get",
            "capital/contract/convertible-coins",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_get_capital_contract_convertible_coins.__doc__ = (
        Client.margin_v1_get_capital_contract_convertible_coins.__doc__
    )

    async def margin_v1_get_spot_delist_schedule(self, **params):
        return await self._request_margin_api(
            "get", "spot/delist-schedule", signed=True, data=params, version=1
        )

    margin_v1_get_spot_delist_schedule.__doc__ = (
        Client.margin_v1_get_spot_delist_schedule.__doc__
    )

    async def margin_v1_post_asset_convert_transfer(self, **params):
        return await self._request_margin_api(
            "post", "asset/convert-transfer", signed=True, data=params, version=1
        )

    margin_v1_post_asset_convert_transfer.__doc__ = (
        Client.margin_v1_post_asset_convert_transfer.__doc__
    )

    async def margin_v1_post_asset_convert_transfer_query_by_page(self, **params):
        return await self._request_margin_api(
            "post",
            "asset/convert-transfer/queryByPage",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_asset_convert_transfer_query_by_page.__doc__ = (
        Client.margin_v1_post_asset_convert_transfer_query_by_page.__doc__
    )

    async def margin_v1_post_capital_contract_convertible_coins(self, **params):
        return await self._request_margin_api(
            "post",
            "capital/contract/convertible-coins",
            signed=True,
            data=params,
            version=1,
        )

    margin_v1_post_capital_contract_convertible_coins.__doc__ = (
        Client.margin_v1_post_capital_contract_convertible_coins.__doc__
    )

    async def margin_v1_post_capital_deposit_credit_apply(self, **params):
        return await self._request_margin_api(
            "post", "capital/deposit/credit-apply", signed=True, data=params, version=1
        )

    margin_v1_post_capital_deposit_credit_apply.__doc__ = (
        Client.margin_v1_post_capital_deposit_credit_apply.__doc__
    )


    async def get_system_status(self):
        return await self._request_margin_api("get", "system/status")

    get_system_status.__doc__ = Client.get_system_status.__doc__


    async def get_account_status(self, **params):
        return await self._request_margin_api(
            "get", "account/status", True, data=params
        )

    get_account_status.__doc__ = Client.get_account_status.__doc__


    async def get_account_api_trading_status(self, **params):
        return await self._request_margin_api(
            "get", "account/apiTradingStatus", True, data=params
        )

    get_account_api_trading_status.__doc__ = (
        Client.get_account_api_trading_status.__doc__
    )


    async def get_account_api_permissions(self, **params):
        return await self._request_margin_api(
            "get", "account/apiRestrictions", True, data=params
        )

    get_account_api_permissions.__doc__ = Client.get_account_api_permissions.__doc__

