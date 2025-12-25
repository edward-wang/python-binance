"""
AsyncFuturesUmMixin - UM Futures (USD-Margined Futures) API

This mixin contains all UM Futures (USD-Margined Futures) related methods.
"""
from ..enums import HistoricalKlinesType
from typing import TYPE_CHECKING
from ..client import Client
from urllib.parse import urlencode, quote
from ..helpers import convert_list_to_json_array

# This mixin depends on request methods provided by AsyncClientCore

if TYPE_CHECKING:
    from ._core_typing import AsyncClientCoreLike as _AsyncClientCoreLike
else:
    class _AsyncClientCoreLike:
        pass


class AsyncFuturesUmMixin(_AsyncClientCoreLike):
    """
    UM Futures (USD-Margined Futures) API Mixin
    
    This mixin provides all UM Futures (USD-Margined Futures) related methods.
    These methods rely on the request infrastructure provided by AsyncClientCore.
    """

    async def futures_ping(self):
        return await self._request_futures_api("get", "ping")


    async def futures_time(self):
        return await self._request_futures_api("get", "time")


    async def futures_exchange_info(self):
        return await self._request_futures_api("get", "exchangeInfo")


    async def futures_order_book(self, **params):
        return await self._request_futures_api("get", "depth", data=params)


    async def futures_recent_trades(self, **params):
        return await self._request_futures_api("get", "trades", data=params)


    async def futures_historical_trades(self, **params):
        return await self._request_futures_api("get", "historicalTrades", data=params)


    async def futures_aggregate_trades(self, **params):
        return await self._request_futures_api("get", "aggTrades", data=params)


    async def futures_klines(self, **params):
        return await self._request_futures_api("get", "klines", data=params)


    async def futures_mark_price_klines(self, **params):
        return await self._request_futures_api("get", "markPriceKlines", data=params)

    futures_mark_price_klines.__doc__ = Client.futures_mark_price_klines.__doc__


    async def futures_index_price_klines(self, **params):
        return await self._request_futures_api("get", "indexPriceKlines", data=params)

    futures_index_price_klines.__doc__ = Client.futures_index_price_klines.__doc__


    async def futures_premium_index_klines(self, **params):
        return await self._request_futures_api("get", "premiumIndexKlines", data=params)

    futures_premium_index_klines.__doc__ = Client.futures_index_price_klines.__doc__


    async def futures_continuous_klines(self, **params):
        return await self._request_futures_api("get", "continuousKlines", data=params)


    async def futures_historical_klines(
        self, symbol: str, interval: str, start_str, end_str=None, limit=None
    ):
        return await self._historical_klines(
            symbol,
            interval,
            start_str,
            end_str=end_str,
            limit=limit,
            klines_type=HistoricalKlinesType.FUTURES,
        )


    async def futures_historical_klines_generator(
        self, symbol, interval, start_str, end_str=None
    ):
        return self._historical_klines_generator(
            symbol,
            interval,
            start_str,
            end_str=end_str,
            klines_type=HistoricalKlinesType.FUTURES,
        )


    async def futures_mark_price(self, **params):
        return await self._request_futures_api("get", "premiumIndex", data=params)


    async def futures_funding_rate(self, **params):
        return await self._request_futures_api("get", "fundingRate", data=params)


    async def futures_top_longshort_account_ratio(self, **params):
        return await self._request_futures_data_api(
            "get", "topLongShortAccountRatio", data=params
        )


    async def futures_top_longshort_position_ratio(self, **params):
        return await self._request_futures_data_api(
            "get", "topLongShortPositionRatio", data=params
        )


    async def futures_global_longshort_ratio(self, **params):
        return await self._request_futures_data_api(
            "get", "globalLongShortAccountRatio", data=params
        )


    async def futures_taker_longshort_ratio(self, **params):
        return await self._request_futures_data_api(
            "get", "takerlongshortRatio", data=params
        )


    async def futures_ticker(self, **params):
        return await self._request_futures_api("get", "ticker/24hr", data=params)


    async def futures_symbol_ticker(self, **params):
        return await self._request_futures_api("get", "ticker/price", data=params)


    async def futures_orderbook_ticker(self, **params):
        return await self._request_futures_api("get", "ticker/bookTicker", data=params)


    async def futures_index_price_constituents(self, **params):
        return await self._request_futures_api("get", "constituents", data=params)

    futures_index_price_constituents.__doc__ = (
        Client.futures_index_price_constituents.__doc__
    )


    async def futures_liquidation_orders(self, **params):
        return await self._request_futures_api(
            "get", "forceOrders", signed=True, data=params
        )


    async def futures_api_trading_status(self, **params):
        return await self._request_futures_api(
            "get", "apiTradingStatus", signed=True, data=params
        )


    async def futures_commission_rate(self, **params):
        return await self._request_futures_api(
            "get", "commissionRate", signed=True, data=params
        )


    async def futures_adl_quantile_estimate(self, **params):
        return await self._request_futures_api(
            "get", "adlQuantile", signed=True, data=params
        )


    async def futures_open_interest(self, **params):
        return await self._request_futures_api("get", "openInterest", data=params)


    async def futures_index_info(self, **params):
        return await self._request_futures_api("get", "indexInfo", data=params)


    async def futures_open_interest_hist(self, **params):
        return await self._request_futures_data_api(
            "get", "openInterestHist", data=params
        )


    async def futures_leverage_bracket(self, **params):
        return await self._request_futures_api(
            "get", "leverageBracket", True, data=params
        )



    async def futures_create_order(self, **params):
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return await self._request_futures_api("post", "order", True, data=params)


    async def futures_limit_order(self, **params):
        """Send in a new futures limit order.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        params["type"] = "LIMIT"
        return await self._request_futures_api("post", "order", True, data=params)


    async def futures_market_order(self, **params):
        """Send in a new futures market order.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        params["type"] = "MARKET"
        return await self._request_futures_api("post", "order", True, data=params)


    async def futures_limit_buy_order(self, **params):
        """Send in a new futures limit buy order.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        params["side"] = "BUY"
        params["type"] = "LIMIT"
        return await self._request_futures_api("post", "order", True, data=params)


    async def futures_limit_sell_order(self, **params):
        """Send in a new futures limit sell order.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        params["side"] = "SELL"
        params["type"] = "LIMIT"
        return await self._request_futures_api("post", "order", True, data=params)


    async def futures_market_buy_order(self, **params):
        """Send in a new futures market buy order.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        params["side"] = "BUY"
        params["type"] = "MARKET"
        return await self._request_futures_api("post", "order", True, data=params)


    async def futures_market_sell_order(self, **params):
        """Send in a new futures market sell order.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        params["side"] = "SELL"
        params["type"] = "MARKET"
        return await self._request_futures_api("post", "order", True, data=params)


    async def futures_modify_order(self, **params):
        """Modify an existing order. Currently only LIMIT order modification is supported.

        https://binance-docs.github.io/apidocs/futures/en/#modify-order-trade

        """
        return await self._request_futures_api("put", "order", True, data=params)


    async def futures_create_test_order(self, **params):
        return await self._request_futures_api("post", "order/test", True, data=params)


    async def futures_place_batch_order(self, **params):
        for order in params["batchOrders"]:
            if "newClientOrderId" not in order:
                order["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
                order = self._order_params(order)
        query_string = urlencode(params).replace("%40", "@").replace("%27", "%22")
        params["batchOrders"] = query_string[12:]

        return await self._request_futures_api(
            "post", "batchOrders", True, data=params, force_params=True
        )


    async def futures_get_order(self, **params):
        return await self._request_futures_api("get", "order", True, data=params)


    async def futures_get_open_orders(self, **params):
        return await self._request_futures_api("get", "openOrders", True, data=params)


    async def futures_get_all_orders(self, **params):
        return await self._request_futures_api("get", "allOrders", True, data=params)


    async def futures_cancel_order(self, **params):
        return await self._request_futures_api("delete", "order", True, data=params)


    async def futures_cancel_all_open_orders(self, **params):
        return await self._request_futures_api(
            "delete", "allOpenOrders", True, data=params
        )


    async def futures_cancel_orders(self, **params):
        if params.get("orderidlist"):
            params["orderidlist"] = quote(
                convert_list_to_json_array(params["orderidlist"])
            )
        if params.get("origclientorderidlist"):
            params["origclientorderidlist"] = quote(
                convert_list_to_json_array(params["origclientorderidlist"])
            )
        return await self._request_futures_api(
            "delete", "batchOrders", True, data=params, force_params=True
        )


    async def futures_countdown_cancel_all(self, **params):
        return await self._request_futures_api(
            "post", "countdownCancelAll", True, data=params
        )


    async def futures_account_balance(self, **params):
        return await self._request_futures_api(
            "get", "balance", True, version=3, data=params
        )


    async def futures_account(self, **params):
        return await self._request_futures_api(
            "get", "account", True, version=2, data=params
        )


    async def futures_change_leverage(self, **params):
        return await self._request_futures_api("post", "leverage", True, data=params)


    async def futures_change_margin_type(self, **params):
        return await self._request_futures_api("post", "marginType", True, data=params)


    async def futures_change_position_margin(self, **params):
        return await self._request_futures_api(
            "post", "positionMargin", True, data=params
        )


    async def futures_position_margin_history(self, **params):
        return await self._request_futures_api(
            "get", "positionMargin/history", True, data=params
        )


    async def futures_position_information(self, **params):
        return await self._request_futures_api(
            "get", "positionRisk", True, version=3, data=params
        )


    async def futures_account_trades(self, **params):
        return await self._request_futures_api("get", "userTrades", True, data=params)


    async def futures_income_history(self, **params):
        return await self._request_futures_api("get", "income", True, data=params)


    async def futures_change_position_mode(self, **params):
        return await self._request_futures_api(
            "post", "positionSide/dual", True, data=params
        )


    async def futures_get_position_mode(self, **params):
        return await self._request_futures_api(
            "get", "positionSide/dual", True, data=params
        )


    async def futures_change_multi_assets_mode(self, multiAssetsMargin: bool):
        params = {"multiAssetsMargin": "true" if multiAssetsMargin else "false"}
        return await self._request_futures_api(
            "post", "multiAssetsMargin", True, data=params
        )


    async def futures_get_multi_assets_mode(self):
        return await self._request_futures_api(
            "get", "multiAssetsMargin", True, data={}
        )


    async def futures_stream_get_listen_key(self):
        res = await self._request_futures_api(
            "post", "listenKey", signed=False, data={}
        )
        return res["listenKey"]


    async def futures_stream_keepalive(self, listenKey):
        params = {"listenKey": listenKey}
        return await self._request_futures_api(
            "put", "listenKey", signed=False, data=params
        )


    async def futures_stream_close(self, listenKey):
        params = {"listenKey": listenKey}
        return await self._request_futures_api(
            "delete", "listenKey", signed=False, data=params
        )

    # new methods

    async def futures_account_config(self, **params):
        return await self._request_futures_api(
            "get", "accountConfig", signed=True, version=1, data=params
        )


    async def futures_symbol_config(self, **params):
        return await self._request_futures_api(
            "get", "symbolConfig", signed=True, version=1, data=params
        )

    # futures_v1 methods

    async def futures_v1_get_order_asyn(self, **params):
        return await self._request_futures_api(
            "get", "order/asyn", signed=True, data=params, version=1
        )

    futures_v1_get_order_asyn.__doc__ = Client.futures_v1_get_order_asyn.__doc__


    async def futures_v1_get_trade_asyn(self, **params):
        return await self._request_futures_api(
            "get", "trade/asyn", signed=True, data=params, version=1
        )

    futures_v1_get_trade_asyn.__doc__ = Client.futures_v1_get_trade_asyn.__doc__


    async def futures_v1_get_funding_info(self, **params):
        return await self._request_futures_api(
            "get", "fundingInfo", signed=False, data=params, version=1
        )

    futures_v1_get_funding_info.__doc__ = Client.futures_v1_get_funding_info.__doc__


    async def futures_v1_get_income_asyn_id(self, **params):
        return await self._request_futures_api(
            "get", "income/asyn/id", signed=True, data=params, version=1
        )

    futures_v1_get_income_asyn_id.__doc__ = Client.futures_v1_get_income_asyn_id.__doc__


    async def futures_v1_get_pm_account_info(self, **params):
        return await self._request_futures_api(
            "get", "pmAccountInfo", signed=True, data=params, version=1
        )

    futures_v1_get_pm_account_info.__doc__ = (
        Client.futures_v1_get_pm_account_info.__doc__
    )


    async def futures_v1_put_batch_order(self, **params):
        return await self._request_futures_api(
            "put", "batchOrder", signed=True, data=params, version=1
        )

    futures_v1_put_batch_order.__doc__ = Client.futures_v1_put_batch_order.__doc__


    async def futures_v1_post_batch_order(self, **params):
        return await self._request_futures_api(
            "post", "batchOrder", signed=True, data=params, version=1
        )

    futures_v1_post_batch_order.__doc__ = Client.futures_v1_post_batch_order.__doc__


    async def futures_v1_get_trade_asyn_id(self, **params):
        return await self._request_futures_api(
            "get", "trade/asyn/id", signed=True, data=params, version=1
        )

    futures_v1_get_trade_asyn_id.__doc__ = Client.futures_v1_get_trade_asyn_id.__doc__


    async def futures_v1_put_batch_orders(self, **params):
        return await self._request_futures_api(
            "put", "batchOrders", signed=True, data=params, version=1
        )

    futures_v1_put_batch_orders.__doc__ = Client.futures_v1_put_batch_orders.__doc__


    async def futures_v1_get_convert_exchange_info(self, **params):
        return await self._request_futures_api(
            "get", "convert/exchangeInfo", signed=False, data=params, version=1
        )

    futures_v1_get_convert_exchange_info.__doc__ = (
        Client.futures_v1_get_convert_exchange_info.__doc__
    )


    async def futures_v1_get_order_amendment(self, **params):
        return await self._request_futures_api(
            "get", "orderAmendment", signed=True, data=params, version=1
        )

    futures_v1_get_order_amendment.__doc__ = (
        Client.futures_v1_get_order_amendment.__doc__
    )


    async def futures_v1_get_income_asyn(self, **params):
        return await self._request_futures_api(
            "get", "income/asyn", signed=True, data=params, version=1
        )

    futures_v1_get_income_asyn.__doc__ = Client.futures_v1_get_income_asyn.__doc__


    async def futures_v1_get_fee_burn(self, **params):
        return await self._request_futures_api(
            "get", "feeBurn", signed=True, data=params, version=1
        )

    futures_v1_get_fee_burn.__doc__ = Client.futures_v1_get_fee_burn.__doc__


    async def futures_v1_get_asset_index(self, **params):
        return await self._request_futures_api(
            "get", "assetIndex", signed=False, data=params, version=1
        )

    futures_v1_get_asset_index.__doc__ = Client.futures_v1_get_asset_index.__doc__


    async def futures_v1_get_rate_limit_order(self, **params):
        return await self._request_futures_api(
            "get", "rateLimit/order", signed=True, data=params, version=1
        )

    futures_v1_get_rate_limit_order.__doc__ = (
        Client.futures_v1_get_rate_limit_order.__doc__
    )


    async def futures_v1_get_open_order(self, **params):
        return await self._request_futures_api(
            "get", "openOrder", signed=True, data=params, version=1
        )

    futures_v1_get_open_order.__doc__ = Client.futures_v1_get_open_order.__doc__


    async def futures_v1_post_fee_burn(self, **params):
        return await self._request_futures_api(
            "post", "feeBurn", signed=True, data=params, version=1
        )

    futures_v1_post_fee_burn.__doc__ = Client.futures_v1_post_fee_burn.__doc__


    async def futures_v1_post_convert_accept_quote(self, **params):
        return await self._request_futures_api(
            "post", "convert/acceptQuote", signed=True, data=params, version=1
        )

    futures_v1_post_convert_accept_quote.__doc__ = (
        Client.futures_v1_post_convert_accept_quote.__doc__
    )


    async def futures_v1_get_order_asyn_id(self, **params):
        return await self._request_futures_api(
            "get", "order/asyn/id", signed=True, data=params, version=1
        )

    futures_v1_get_order_asyn_id.__doc__ = Client.futures_v1_get_order_asyn_id.__doc__


    async def futures_v1_post_convert_get_quote(self, **params):
        return await self._request_futures_api(
            "post", "convert/getQuote", signed=True, data=params, version=1
        )

    futures_v1_post_convert_get_quote.__doc__ = (
        Client.futures_v1_post_convert_get_quote.__doc__
    )


    async def futures_v1_delete_batch_order(self, **params):
        return await self._request_futures_api(
            "delete", "batchOrder", signed=True, data=params, version=1
        )

    futures_v1_delete_batch_order.__doc__ = Client.futures_v1_delete_batch_order.__doc__


    async def futures_v1_get_convert_order_status(self, **params):
        return await self._request_futures_api(
            "get", "convert/orderStatus", signed=True, data=params, version=1
        )

    futures_v1_get_convert_order_status.__doc__ = (
        Client.futures_v1_get_convert_order_status.__doc__
    )

    
