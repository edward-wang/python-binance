"""
AsyncMarginMixin - Margin API

This mixin contains all Margin related methods.
"""
from typing import Dict, Any, Optional, TYPE_CHECKING
from ..client import Client
from ..base_client import BaseClient

# This mixin depends on request methods provided by AsyncClientCore

if TYPE_CHECKING:
    from ._core_typing import AsyncClientCoreLike as _AsyncClientCoreLike
else:
    class _AsyncClientCoreLike:
        pass


class AsyncMarginMixin(_AsyncClientCoreLike):
    """
    Margin API Mixin
    
    This mixin provides all Margin related methods.
    These methods depend on request infrastructure provided by AsyncClientCore.
    """

    async def get_margin_account(self, **params):
        return await self._request_margin_api(
            "get", "margin/account", True, data=params
        )

    get_margin_account.__doc__ = Client.get_margin_account.__doc__


    async def get_isolated_margin_account(self, **params):
        return await self._request_margin_api(
            "get", "margin/isolated/account", True, data=params
        )

    get_isolated_margin_account.__doc__ = Client.get_isolated_margin_account.__doc__


    async def enable_isolated_margin_account(self, **params):
        return await self._request_margin_api(
            "post", "margin/isolated/account", True, data=params
        )

    enable_isolated_margin_account.__doc__ = (
        Client.enable_isolated_margin_account.__doc__
    )


    async def disable_isolated_margin_account(self, **params):
        return await self._request_margin_api(
            "delete", "margin/isolated/account", True, data=params
        )

    disable_isolated_margin_account.__doc__ = (
        Client.disable_isolated_margin_account.__doc__
    )


    async def get_enabled_isolated_margin_account_limit(self, **params):
        return await self._request_margin_api(
            "get", "margin/isolated/accountLimit", True, data=params
        )

    get_enabled_isolated_margin_account_limit.__doc__ = (
        Client.get_enabled_isolated_margin_account_limit.__doc__
    )


    async def get_margin_dustlog(self, **params):
        return await self._request_margin_api(
            "get", "margin/dribblet", True, data=params
        )

    get_margin_dustlog.__doc__ = Client.get_margin_dustlog.__doc__


    async def get_margin_dust_assets(self, **params):
        return await self._request_margin_api("get", "margin/dust", True, data=params)

    get_margin_dust_assets.__doc__ = Client.get_margin_dust_assets.__doc__


    async def transfer_margin_dust(self, **params):
        return await self._request_margin_api("post", "margin/dust", True, data=params)

    transfer_margin_dust.__doc__ = Client.transfer_margin_dust.__doc__


    async def get_cross_margin_collateral_ratio(self, **params):
        return await self._request_margin_api(
            "get", "margin/crossMarginCollateralRatio", True, data=params
        )

    get_cross_margin_collateral_ratio.__doc__ = (
        Client.get_cross_margin_collateral_ratio.__doc__
    )


    async def get_small_liability_exchange_assets(self, **params):
        return await self._request_margin_api(
            "get", "margin/exchange-small-liability", True, data=params
        )

    get_small_liability_exchange_assets.__doc__ = (
        Client.get_small_liability_exchange_assets.__doc__
    )


    async def exchange_small_liability_assets(self, **params):
        return await self._request_margin_api(
            "post", "margin/exchange-small-liability", True, data=params
        )

    exchange_small_liability_assets.__doc__ = (
        Client.exchange_small_liability_assets.__doc__
    )


    async def get_small_liability_exchange_history(self, **params):
        return await self._request_margin_api(
            "get", "margin/exchange-small-liability-history", True, data=params
        )

    get_small_liability_exchange_history.__doc__ = (
        Client.get_small_liability_exchange_history.__doc__
    )


    async def get_future_hourly_interest_rate(self, **params):
        return await self._request_margin_api(
            "get", "margin/next-hourly-interest-rate", True, data=params
        )

    get_future_hourly_interest_rate.__doc__ = (
        Client.get_future_hourly_interest_rate.__doc__
    )


    async def get_margin_capital_flow(self, **params):
        return await self._request_margin_api(
            "get", "margin/capital-flow", True, data=params
        )

    get_margin_capital_flow.__doc__ = Client.get_margin_capital_flow.__doc__


    async def get_margin_delist_schedule(self, **params):
        return await self._request_margin_api(
            "get", "margin/delist-schedule", True, data=params
        )

    get_margin_delist_schedule.__doc__ = Client.get_margin_delist_schedule.__doc__


    async def get_margin_asset(self, **params):
        return await self._request_margin_api("get", "margin/asset", data=params)

    get_margin_asset.__doc__ = Client.get_margin_asset.__doc__


    async def get_margin_symbol(self, **params):
        return await self._request_margin_api("get", "margin/pair", data=params)

    get_margin_symbol.__doc__ = Client.get_margin_symbol.__doc__


    async def get_margin_all_assets(self, **params):
        return await self._request_margin_api("get", "margin/allAssets", data=params)

    get_margin_all_assets.__doc__ = Client.get_margin_all_assets.__doc__


    async def get_margin_all_pairs(self, **params):
        return await self._request_margin_api("get", "margin/allPairs", data=params)

    get_margin_all_pairs.__doc__ = Client.get_margin_all_pairs.__doc__


    async def create_isolated_margin_account(self, **params):
        return await self._request_margin_api(
            "post", "margin/isolated/create", signed=True, data=params
        )

    create_isolated_margin_account.__doc__ = (
        Client.create_isolated_margin_account.__doc__
    )


    async def get_isolated_margin_symbol(self, **params):
        return await self._request_margin_api(
            "get", "margin/isolated/pair", signed=True, data=params
        )

    get_isolated_margin_symbol.__doc__ = Client.get_isolated_margin_symbol.__doc__


    async def get_all_isolated_margin_symbols(self, **params):
        return await self._request_margin_api(
            "get", "margin/isolated/allPairs", signed=True, data=params
        )

    get_all_isolated_margin_symbols.__doc__ = (
        Client.get_all_isolated_margin_symbols.__doc__
    )


    async def get_isolated_margin_fee_data(self, **params):
        return await self._request_margin_api(
            "get", "margin/isolatedMarginData", True, data=params
        )

    get_isolated_margin_fee_data.__doc__ = Client.get_isolated_margin_fee_data.__doc__


    async def get_isolated_margin_tier_data(self, **params):
        return await self._request_margin_api(
            "get", "margin/isolatedMarginTier", True, data=params
        )

    get_isolated_margin_tier_data.__doc__ = Client.get_isolated_margin_tier_data.__doc__


    async def margin_manual_liquidation(self, **params):
        return await self._request_margin_api(
            "get", "margin/manual-liquidation", True, data=params
        )

    margin_manual_liquidation.__doc__ = Client.margin_manual_liquidation.__doc__


    async def get_margin_price_index(self, **params):
        return await self._request_margin_api("get", "margin/priceIndex", data=params)

    get_margin_price_index.__doc__ = Client.get_margin_price_index.__doc__


    async def transfer_margin_to_spot(self, **params):
        params["type"] = 2
        return await self._request_margin_api(
            "post", "margin/transfer", signed=True, data=params
        )

    transfer_margin_to_spot.__doc__ = Client.transfer_margin_to_spot.__doc__


    async def transfer_spot_to_margin(self, **params):
        params["type"] = 1
        return await self._request_margin_api(
            "post", "margin/transfer", signed=True, data=params
        )

    transfer_spot_to_margin.__doc__ = Client.transfer_spot_to_margin.__doc__


    async def transfer_isolated_margin_to_spot(self, **params):
        params["transFrom"] = "ISOLATED_MARGIN"
        params["transTo"] = "SPOT"
        return await self._request_margin_api(
            "post", "margin/isolated/transfer", signed=True, data=params
        )

    transfer_isolated_margin_to_spot.__doc__ = (
        Client.transfer_isolated_margin_to_spot.__doc__
    )


    async def transfer_spot_to_isolated_margin(self, **params):
        params["transFrom"] = "SPOT"
        params["transTo"] = "ISOLATED_MARGIN"
        return await self._request_margin_api(
            "post", "margin/isolated/transfer", signed=True, data=params
        )

    transfer_spot_to_isolated_margin.__doc__ = (
        Client.transfer_spot_to_isolated_margin.__doc__
    )


    async def create_margin_loan(self, **params):
        return await self._request_margin_api(
            "post", "margin/loan", signed=True, data=params
        )

    create_margin_loan.__doc__ = Client.create_margin_loan.__doc__


    async def repay_margin_loan(self, **params):
        return await self._request_margin_api(
            "post", "margin/repay", signed=True, data=params
        )

    repay_margin_loan.__doc__ = Client.repay_margin_loan.__doc__


    async def create_margin_order(self, **params):
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.SPOT_ORDER_PREFIX + self.uuid22()
        return await self._request_margin_api(
            "post", "margin/order", signed=True, data=params
        )

    create_margin_order.__doc__ = Client.create_margin_order.__doc__


    async def cancel_margin_order(self, **params):
        return await self._request_margin_api(
            "delete", "margin/order", signed=True, data=params
        )

    cancel_margin_order.__doc__ = Client.cancel_margin_order.__doc__


    async def cancel_all_open_margin_orders(self, **params):
        return await self._request_margin_api(
            "delete", "margin/openOrders", signed=True, data=params
        )

    cancel_all_open_margin_orders.__doc__ = Client.cancel_all_open_margin_orders.__doc__


    async def set_margin_max_leverage(self, **params):
        return await self._request_margin_api(
            "post", "margin/max-leverage", signed=True, data=params
        )

    set_margin_max_leverage.__doc__ = Client.set_margin_max_leverage.__doc__


    async def get_margin_transfer_history(self, **params):
        return await self._request_margin_api(
            "get", "margin/transfer", signed=True, data=params
        )

    get_margin_transfer_history.__doc__ = Client.get_margin_transfer_history.__doc__


    async def get_margin_loan_details(self, **params):
        return await self._request_margin_api(
            "get", "margin/loan", signed=True, data=params
        )

    get_margin_loan_details.__doc__ = Client.get_margin_loan_details.__doc__


    async def get_margin_repay_details(self, **params):
        return await self._request_margin_api(
            "get", "margin/repay", signed=True, data=params
        )


    async def get_cross_margin_data(self, **params):
        return await self._request_margin_api(
            "get", "margin/crossMarginData", signed=True, data=params
        )


    async def get_margin_interest_history(self, **params):
        return await self._request_margin_api(
            "get", "margin/interestHistory", signed=True, data=params
        )


    async def get_margin_force_liquidation_rec(self, **params):
        return await self._request_margin_api(
            "get", "margin/forceLiquidationRec", signed=True, data=params
        )


    async def get_margin_order(self, **params):
        return await self._request_margin_api(
            "get", "margin/order", signed=True, data=params
        )


    async def get_open_margin_orders(self, **params):
        return await self._request_margin_api(
            "get", "margin/openOrders", signed=True, data=params
        )


    async def get_all_margin_orders(self, **params):
        return await self._request_margin_api(
            "get", "margin/allOrders", signed=True, data=params
        )


    async def get_margin_trades(self, **params):
        return await self._request_margin_api(
            "get", "margin/myTrades", signed=True, data=params
        )


    async def get_max_margin_loan(self, **params):
        return await self._request_margin_api(
            "get", "margin/maxBorrowable", signed=True, data=params
        )


    async def get_max_margin_transfer(self, **params):
        return await self._request_margin_api(
            "get", "margin/maxTransferable", signed=True, data=params
        )

    # Margin OCO


    async def create_margin_oco_order(self, **params):
        return await self._request_margin_api(
            "post", "margin/order/oco", signed=True, data=params
        )


    async def cancel_margin_oco_order(self, **params):
        return await self._request_margin_api(
            "delete", "margin/orderList", signed=True, data=params
        )


    async def get_margin_oco_order(self, **params):
        return await self._request_margin_api(
            "get", "margin/orderList", signed=True, data=params
        )


    async def get_open_margin_oco_orders(self, **params):
        return await self._request_margin_api(
            "get", "margin/openOrderList", signed=True, data=params
        )

    async def margin_next_hourly_interest_rate(self, **params):
        return await self._request_margin_api(
            "get", "margin/next-hourly-interest-rate", signed=True, data=params
        )

    margin_next_hourly_interest_rate.__doc__ = (
        Client.margin_next_hourly_interest_rate.__doc__
    )

    async def margin_interest_history(self, **params):
        return await self._request_margin_api(
            "get", "margin/interestHistory", signed=True, data=params
        )

    margin_interest_history.__doc__ = Client.margin_interest_history.__doc__

    async def margin_borrow_repay(self, **params):
        return await self._request_margin_api(
            "post", "margin/borrow-repay", signed=True, data=params
        )

    margin_borrow_repay.__doc__ = Client.margin_borrow_repay.__doc__

    async def margin_get_borrow_repay_records(self, **params):
        return await self._request_margin_api(
            "get", "margin/borrow-repay", signed=True, data=params
        )

    margin_get_borrow_repay_records.__doc__ = (
        Client.margin_get_borrow_repay_records.__doc__
    )

    async def margin_interest_rate_history(self, **params):
        return await self._request_margin_api(
            "get", "margin/interestRateHistory", signed=True, data=params
        )

    margin_interest_rate_history.__doc__ = Client.margin_interest_rate_history.__doc__

    async def margin_max_borrowable(self, **params):
        return await self._request_margin_api(
            "get", "margin/maxBorrowable", signed=True, data=params
        )

    margin_max_borrowable.__doc__ = Client.margin_max_borrowable.__doc__

    # Cross-margin


    async def margin_stream_get_listen_key(self):
        res = await self._request_margin_api(
            "post", "userDataStream", signed=False, data={}
        )
        return res["listenKey"]


    async def margin_stream_keepalive(self, listenKey):
        params = {"listenKey": listenKey}
        return await self._request_margin_api(
            "put", "userDataStream", signed=False, data=params
        )


    async def margin_stream_close(self, listenKey):
        params = {"listenKey": listenKey}
        return await self._request_margin_api(
            "delete", "userDataStream", signed=False, data=params
        )

        # Isolated margin


    async def isolated_margin_stream_get_listen_key(self, symbol):
        params = {"symbol": symbol}
        res = await self._request_margin_api(
            "post", "userDataStream/isolated", signed=False, data=params
        )
        return res["listenKey"]


    async def isolated_margin_stream_keepalive(self, symbol, listenKey):
        params = {"symbol": symbol, "listenKey": listenKey}
        return await self._request_margin_api(
            "put", "userDataStream/isolated", signed=False, data=params
        )


    async def isolated_margin_stream_close(self, symbol, listenKey):
        params = {"symbol": symbol, "listenKey": listenKey}
        return await self._request_margin_api(
            "delete", "userDataStream/isolated", signed=False, data=params
        )

    async def margin_v1_get_margin_all_order_list(self, **params):
        return await self._request_margin_api(
            "get", "margin/allOrderList", signed=True, data=params, version=1
        )

    margin_v1_get_margin_all_order_list.__doc__ = (
        Client.margin_v1_get_margin_all_order_list.__doc__
    )

    async def margin_v1_get_margin_available_inventory(self, **params):
        return await self._request_margin_api(
            "get", "margin/available-inventory", signed=True, data=params, version=1
        )

    margin_v1_get_margin_available_inventory.__doc__ = (
        Client.margin_v1_get_margin_available_inventory.__doc__
    )

    async def margin_v1_get_margin_isolated_transfer(self, **params):
        return await self._request_margin_api(
            "get", "margin/isolated/transfer", signed=True, data=params, version=1
        )


    async def margin_v1_get_margin_leverage_bracket(self, **params):
        return await self._request_margin_api(
            "get", "margin/leverageBracket", signed=True, data=params, version=1
        )

    margin_v1_get_margin_leverage_bracket.__doc__ = (
        Client.margin_v1_get_margin_leverage_bracket.__doc__
    )

    async def margin_v1_get_margin_rate_limit_order(self, **params):
        return await self._request_margin_api(
            "get", "margin/rateLimit/order", signed=True, data=params, version=1
        )

    margin_v1_get_margin_rate_limit_order.__doc__ = (
        Client.margin_v1_get_margin_rate_limit_order.__doc__
    )

    async def margin_v1_get_margin_trade_coeff(self, **params):
        return await self._request_margin_api(
            "get", "margin/tradeCoeff", signed=True, data=params, version=1
        )

    margin_v1_get_margin_trade_coeff.__doc__ = (
        Client.margin_v1_get_margin_trade_coeff.__doc__
    )

    async def margin_v1_post_margin_manual_liquidation(self, **params):
        return await self._request_margin_api(
            "post", "margin/manual-liquidation", signed=True, data=params, version=1
        )
