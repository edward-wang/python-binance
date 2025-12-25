"""
AsyncFuturesCmMixin - CM Futures (Coin-Margined Futures) API

This mixin contains all CM Futures (Coin-Margined Futures) related methods.
"""
from typing import TYPE_CHECKING
from urllib.parse import urlencode, quote
from ..client import Client
from ..helpers import convert_list_to_json_array

# This mixin depends on the request methods provided by AsyncClientCore

if TYPE_CHECKING:
    from ._core_typing import AsyncClientCoreLike as _AsyncClientCoreLike
else:
    class _AsyncClientCoreLike:
        pass


class AsyncFuturesCmMixin(_AsyncClientCoreLike):
    """
    CM Futures (Coin-Margined Futures) API Mixin
    
    This mixin provides all CM Futures (Coin-Margined Futures) related methods.
    These methods depend on the request infrastructure provided by AsyncClientCore.
    """

    async def futures_coin_ping(self):
        return await self._request_futures_coin_api("get", "ping")


    async def futures_coin_time(self):
        return await self._request_futures_coin_api("get", "time")


    async def futures_coin_exchange_info(self):
        return await self._request_futures_coin_api("get", "exchangeInfo")


    async def futures_coin_order_book(self, **params):
        return await self._request_futures_coin_api("get", "depth", data=params)


    async def futures_coin_recent_trades(self, **params):
        return await self._request_futures_coin_api("get", "trades", data=params)


    async def futures_coin_historical_trades(self, **params):
        return await self._request_futures_coin_api(
            "get", "historicalTrades", data=params
        )


    async def futures_coin_aggregate_trades(self, **params):
        return await self._request_futures_coin_api("get", "aggTrades", data=params)


    async def futures_coin_klines(self, **params):
        return await self._request_futures_coin_api("get", "klines", data=params)


    async def futures_coin_continous_klines(self, **params):
        return await self._request_futures_coin_api(
            "get", "continuousKlines", data=params
        )


    async def futures_coin_index_price_klines(self, **params):
        return await self._request_futures_coin_api(
            "get", "indexPriceKlines", data=params
        )


    async def futures_coin_mark_price_klines(self, **params):
        return await self._request_futures_coin_api(
            "get", "markPriceKlines", data=params
        )

    futures_coin_mark_price_klines.__doc__ = Client.futures_mark_price_klines.__doc__


    async def futures_coin_premium_index_klines(self, **params):
        return await self._request_futures_coin_api(
            "get", "premiumIndexKlines", data=params
        )

    futures_coin_premium_index_klines.__doc__ = (
        Client.futures_premium_index_klines.__doc__
    )


    async def futures_coin_mark_price(self, **params):
        return await self._request_futures_coin_api("get", "premiumIndex", data=params)


    async def futures_coin_funding_rate(self, **params):
        return await self._request_futures_coin_api("get", "fundingRate", data=params)


    async def futures_coin_ticker(self, **params):
        return await self._request_futures_coin_api("get", "ticker/24hr", data=params)


    async def futures_coin_symbol_ticker(self, **params):
        return await self._request_futures_coin_api("get", "ticker/price", data=params)


    async def futures_coin_orderbook_ticker(self, **params):
        return await self._request_futures_coin_api(
            "get", "ticker/bookTicker", data=params
        )


    async def futures_coin_index_price_constituents(self, **params):
        return await self._request_futures_coin_api("get", "constituents", data=params)

    futures_coin_index_price_constituents.__doc__ = (
        Client.futures_coin_index_price_constituents.__doc__
    )


    async def futures_coin_liquidation_orders(self, **params):
        return await self._request_futures_coin_api(
            "get", "forceOrders", signed=True, data=params
        )


    async def futures_coin_open_interest(self, **params):
        return await self._request_futures_coin_api("get", "openInterest", data=params)


    async def futures_coin_open_interest_hist(self, **params):
        return await self._request_futures_coin_data_api(
            "get", "openInterestHist", data=params
        )


    async def futures_coin_leverage_bracket(self, **params):
        return await self._request_futures_coin_api(
            "get", "leverageBracket", version=2, signed=True, data=params
        )


    async def futures_coin_create_order(self, **params):
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return await self._request_futures_coin_api("post", "order", True, data=params)


    async def futures_coin_place_batch_order(self, **params):
        for order in params["batchOrders"]:
            if "newClientOrderId" not in order:
                order["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        query_string = urlencode(params)
        query_string = query_string.replace("%27", "%22")
        params["batchOrders"] = query_string[12:]

        return await self._request_futures_coin_api(
            "post", "batchOrders", True, data=params
        )


    async def futures_coin_get_order(self, **params):
        return await self._request_futures_coin_api("get", "order", True, data=params)


    async def futures_coin_get_open_orders(self, **params):
        return await self._request_futures_coin_api(
            "get", "openOrders", True, data=params
        )


    async def futures_coin_get_all_orders(self, **params):
        return await self._request_futures_coin_api(
            "get", "allOrders", signed=True, data=params
        )


    async def futures_coin_cancel_order(self, **params):
        return await self._request_futures_coin_api(
            "delete", "order", signed=True, data=params
        )


    async def futures_coin_cancel_all_open_orders(self, **params):
        return await self._request_futures_coin_api(
            "delete", "allOpenOrders", signed=True, data=params, force_params=True
        )


    async def futures_coin_cancel_orders(self, **params):
        if params.get("orderidlist"):
            params["orderidlist"] = quote(
                convert_list_to_json_array(params["orderidlist"])
            )
        if params.get("origclientorderidlist"):
            params["origclientorderidlist"] = quote(
                convert_list_to_json_array(params["origclientorderidlist"])
            )
        return await self._request_futures_coin_api(
            "delete", "batchOrders", True, data=params
        )


    async def futures_coin_account_balance(self, **params):
        return await self._request_futures_coin_api(
            "get", "balance", signed=True, data=params
        )


    async def futures_coin_account(self, **params):
        return await self._request_futures_coin_api(
            "get", "account", signed=True, data=params
        )


    async def futures_coin_change_leverage(self, **params):
        return await self._request_futures_coin_api(
            "post", "leverage", signed=True, data=params
        )


    async def futures_coin_change_margin_type(self, **params):
        return await self._request_futures_coin_api(
            "post", "marginType", signed=True, data=params
        )


    async def futures_coin_change_position_margin(self, **params):
        return await self._request_futures_coin_api(
            "post", "positionMargin", True, data=params
        )


    async def futures_coin_position_margin_history(self, **params):
        return await self._request_futures_coin_api(
            "get", "positionMargin/history", True, data=params
        )


    async def futures_coin_position_information(self, **params):
        return await self._request_futures_coin_api(
            "get", "positionRisk", True, data=params
        )


    async def futures_coin_account_trades(self, **params):
        return await self._request_futures_coin_api(
            "get", "userTrades", True, data=params
        )


    async def futures_coin_income_history(self, **params):
        return await self._request_futures_coin_api("get", "income", True, data=params)


    async def futures_coin_change_position_mode(self, **params):
        return await self._request_futures_coin_api(
            "post", "positionSide/dual", True, data=params
        )


    async def futures_coin_get_position_mode(self, **params):
        return await self._request_futures_coin_api(
            "get", "positionSide/dual", True, data=params
        )


    async def futures_coin_stream_get_listen_key(self):
        res = await self._request_futures_coin_api(
            "post", "listenKey", signed=False, data={}
        )
        return res["listenKey"]


    async def futures_coin_stream_keepalive(self, listenKey):
        params = {"listenKey": listenKey}
        return await self._request_futures_coin_api(
            "put", "listenKey", signed=False, data=params
        )


    async def futures_coin_account_order_history_download(self, **params):
        return await self._request_futures_coin_api(
            "get", "order/asyn", True, data=params
        )

    futures_coin_account_order_history_download.__doc__ = (
        Client.futures_coin_account_order_history_download.__doc__
    )


    async def futures_coin_account_order_history_download_link(self, **params):
        return await self._request_futures_coin_api(
            "get", "order/asyn/id", True, data=params
        )

    futures_coin_account_order_history_download_link.__doc__ = (
        Client.futures_coin_accout_order_history_download_link.__doc__
    )


    async def futures_coin_account_trade_history_download(self, **params):
        return await self._request_futures_coin_api(
            "get", "trade/asyn", True, data=params
        )

    futures_coin_account_trade_history_download.__doc__ = (
        Client.futures_coin_account_trade_history_download.__doc__
    )


    async def futures_coin_account_trade_history_download_link(self, **params):
        return await self._request_futures_coin_api(
            "get", "trade/asyn/id", True, data=params
        )

    futures_coin_account_trade_history_download_link.__doc__ = (
        Client.futures_coin_account_trade_history_download_link.__doc__
    )


    async def futures_coin_stream_close(self, listenKey):
        params = {"listenKey": listenKey}
        return await self._request_futures_coin_api(
            "delete", "listenKey", signed=False, data=params
        )

    async def futures_coin_v1_get_income_asyn_id(self, **params):
        return await self._request_futures_coin_api(
            "get", "income/asyn/id", signed=True, data=params, version=1
        )

    futures_coin_v1_get_income_asyn_id.__doc__ = (
        Client.futures_coin_v1_get_income_asyn_id.__doc__
    )

    async def futures_coin_v1_get_order_amendment(self, **params):
        return await self._request_futures_coin_api(
            "get", "orderAmendment", signed=True, data=params, version=1
        )

    futures_coin_v1_get_order_amendment.__doc__ = (
        Client.futures_coin_v1_get_order_amendment.__doc__
    )

    async def futures_coin_v1_get_pm_account_info(self, **params):
        return await self._request_futures_coin_api(
            "get", "pmAccountInfo", signed=True, data=params, version=1
        )

    futures_coin_v1_get_pm_account_info.__doc__ = (
        Client.futures_coin_v1_get_pm_account_info.__doc__
    )

    async def futures_coin_v1_get_funding_info(self, **params):
        return await self._request_futures_coin_api(
            "get", "fundingInfo", signed=False, data=params, version=1
        )

    futures_coin_v1_get_funding_info.__doc__ = (
        Client.futures_coin_v1_get_funding_info.__doc__
    )

    async def futures_coin_v1_get_adl_quantile(self, **params):
        return await self._request_futures_coin_api(
            "get", "adlQuantile", signed=True, data=params, version=1
        )

    futures_coin_v1_get_adl_quantile.__doc__ = (
        Client.futures_coin_v1_get_adl_quantile.__doc__
    )

    async def futures_coin_v1_get_income_asyn(self, **params):
        return await self._request_futures_coin_api(
            "get", "income/asyn", signed=True, data=params, version=1
        )

    futures_coin_v1_get_income_asyn.__doc__ = (
        Client.futures_coin_v1_get_income_asyn.__doc__
    )

    async def futures_coin_v1_get_commission_rate(self, **params):
        return await self._request_futures_coin_api(
            "get", "commissionRate", signed=True, data=params, version=1
        )

    futures_coin_v1_get_commission_rate.__doc__ = (
        Client.futures_coin_v1_get_commission_rate.__doc__
    )

    async def futures_coin_v1_put_batch_orders(self, **params):
        return await self._request_futures_coin_api(
            "put", "batchOrders", signed=True, data=params, version=1
        )

    futures_coin_v1_put_batch_orders.__doc__ = (
        Client.futures_coin_v1_put_batch_orders.__doc__
    )

    async def futures_coin_v1_put_order(self, **params):
        return await self._request_futures_coin_api(
            "put", "order", signed=True, data=params, version=1
        )

    futures_coin_v1_put_order.__doc__ = Client.futures_coin_v1_put_order.__doc__

