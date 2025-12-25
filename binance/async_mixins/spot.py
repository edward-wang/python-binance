"""
AsyncSpotMixin - Spot API

This mixin contains all Spot related methods.
"""
import time
import asyncio
from ..enums import HistoricalKlinesType
from typing import Dict, Any, Optional, List, TYPE_CHECKING
from ..client import Client
from ..base_client import BaseClient
from ..helpers import convert_ts_str, interval_to_milliseconds
from ..exceptions import NotImplementedException

# This mixin depends on request methods provided by AsyncClientCore

if TYPE_CHECKING:
    from ._core_typing import AsyncClientCoreLike as _AsyncClientCoreLike
else:
    class _AsyncClientCoreLike:
        pass


class AsyncSpotMixin(_AsyncClientCoreLike):
    """
    Spot API Mixin
    
    This mixin provides all Spot related methods.
    These methods depend on request infrastructure provided by AsyncClientCore.
    """

    async def cancel_all_open_orders(self, **params):
        return await self._delete("openOrders", True, data=params)

    async def cancel_replace_order(self, **params):
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.SPOT_ORDER_PREFIX + self.uuid22()
        return await self._post("order/cancelReplace", signed=True, data=params)

    cancel_replace_order.__doc__ = Client.cancel_replace_order.__doc__

    async def create_oco_order(self, **params):
        if "listClientOrderId" not in params:
            params["listClientOrderId"] = self.SPOT_ORDER_PREFIX + self.uuid22()
        return await self._post("orderList/oco", True, data=params)

    async def get_products(self) -> Dict:
        products = await self._request_website(
            "get",
            "bapi/asset/v2/public/asset-service/product/get-products?includeEtf=true",
        )
        return products

    get_products.__doc__ = Client.get_products.__doc__


    async def get_exchange_info(self) -> Dict:
        return await self._get("exchangeInfo")

    get_exchange_info.__doc__ = Client.get_exchange_info.__doc__


    async def get_symbol_info(self, symbol) -> Optional[Dict]:
        res = await self.get_exchange_info()

        for item in res["symbols"]:
            if item["symbol"] == symbol.upper():
                return item

        return None

    get_symbol_info.__doc__ = Client.get_symbol_info.__doc__

    # General Endpoints


    async def ping(self) -> Dict:
        return await self._get("ping")

    ping.__doc__ = Client.ping.__doc__


    async def get_server_time(self) -> Dict:
        return await self._get("time")

    get_server_time.__doc__ = Client.get_server_time.__doc__

    # Market Data Endpoints


    async def get_all_tickers(
        self, symbol: Optional[str] = None
    ) -> List[Dict[str, str]]:
        params = {}
        if symbol:
            params["symbol"] = symbol
        response = await self._get("ticker/price", data=params)
        if isinstance(response, list) and all(
            isinstance(item, dict) for item in response
        ):
            return response
        raise TypeError("Expected a list of dictionaries")

    get_all_tickers.__doc__ = Client.get_all_tickers.__doc__


    async def get_orderbook_tickers(self, **params) -> Dict:
        data = {}
        if "symbol" in params:
            data["symbol"] = params["symbol"]
        elif "symbols" in params:
            data["symbols"] = params["symbols"]
        return await self._get("ticker/bookTicker", data=data)

    get_orderbook_tickers.__doc__ = Client.get_orderbook_tickers.__doc__


    async def get_order_book(self, **params) -> Dict:
        return await self._get("depth", data=params)

    get_order_book.__doc__ = Client.get_order_book.__doc__


    async def get_recent_trades(self, **params) -> Dict:
        return await self._get("trades", data=params)

    get_recent_trades.__doc__ = Client.get_recent_trades.__doc__


    async def get_historical_trades(self, **params) -> Dict:
        return await self._get("historicalTrades", data=params)

    get_historical_trades.__doc__ = Client.get_historical_trades.__doc__


    async def get_aggregate_trades(self, **params) -> Dict:
        return await self._get("aggTrades", data=params)

    get_aggregate_trades.__doc__ = Client.get_aggregate_trades.__doc__


    async def aggregate_trade_iter(self, symbol, start_str=None, last_id=None):
        if start_str is not None and last_id is not None:
            raise ValueError(
                "start_time and last_id may not be simultaneously specified."
            )

        # If there's no last_id, get one.
        if last_id is None:
            # Without a last_id, we actually need the first trade.  Normally,
            # we'd get rid of it. See the next loop.
            if start_str is None:
                trades = await self.get_aggregate_trades(symbol=symbol, fromId=0)
            else:
                # The difference between startTime and endTime should be less
                # or equal than an hour and the result set should contain at
                # least one trade.
                start_ts = convert_ts_str(start_str)
                # If the resulting set is empty (i.e. no trades in that interval)
                # then we just move forward hour by hour until we find at least one
                # trade or reach present moment
                while True:
                    end_ts = start_ts + (60 * 60 * 1000)
                    trades = await self.get_aggregate_trades(
                        symbol=symbol, startTime=start_ts, endTime=end_ts
                    )
                    if len(trades) > 0:
                        break
                    # If we reach present moment and find no trades then there is
                    # nothing to iterate, so we're done
                    if end_ts > int(time.time() * 1000):
                        return
                    start_ts = end_ts
            for t in trades:
                yield t
            last_id = trades[-1][self.AGG_ID]

        while True:
            # There is no need to wait between queries, to avoid hitting the
            # rate limit. We're using blocking IO, and as long as we're the
            # only thread running calls like this, Binance will automatically
            # add the right delay time on their end, forcing us to wait for
            # data. That really simplifies this function's job. Binance is
            # fucking awesome.
            trades = await self.get_aggregate_trades(symbol=symbol, fromId=last_id)
            # fromId=n returns a set starting with id n, but we already have
            # that one. So get rid of the first item in the result set.
            trades = trades[1:]
            if len(trades) == 0:
                return
            for t in trades:
                yield t
            last_id = trades[-1][self.AGG_ID]

    aggregate_trade_iter.__doc__ = Client.aggregate_trade_iter.__doc__


    async def get_ui_klines(self, **params) -> Dict:
        return await self._get("uiKlines", data=params)

    get_ui_klines.__doc__ = Client.get_ui_klines.__doc__


    async def get_klines(self, **params) -> Dict:
        return await self._get("klines", data=params)

    get_klines.__doc__ = Client.get_klines.__doc__


    async def _klines(
        self, klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT, **params
    ) -> Dict:
        if "endTime" in params and not params["endTime"]:
            del params["endTime"]
        if HistoricalKlinesType.SPOT == klines_type:
            return await self.get_klines(**params)
        elif HistoricalKlinesType.FUTURES == klines_type:
            return await self.futures_klines(**params)
        elif HistoricalKlinesType.FUTURES_COIN == klines_type:
            return await self.futures_coin_klines(**params)
        elif HistoricalKlinesType.FUTURES_MARK_PRICE == klines_type:
            return await self.futures_mark_price_klines(**params)
        elif HistoricalKlinesType.FUTURES_INDEX_PRICE == klines_type:
            return await self.futures_index_price_klines(**params)
        elif HistoricalKlinesType.FUTURES_COIN_MARK_PRICE == klines_type:
            return await self.futures_coin_mark_price_klines(**params)
        elif HistoricalKlinesType.FUTURES_COIN_INDEX_PRICE == klines_type:
            return await self.futures_coin_index_price_klines(**params)
        else:
            raise NotImplementedException(klines_type)

    _klines.__doc__ = Client._klines.__doc__


    async def _get_earliest_valid_timestamp(
        self,
        symbol,
        interval,
        klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT,
    ):
        kline = await self._klines(
            klines_type=klines_type,
            symbol=symbol,
            interval=interval,
            limit=1,
            startTime=0,
            endTime=int(time.time() * 1000),
        )
        return kline[0][0]

    _get_earliest_valid_timestamp.__doc__ = Client._get_earliest_valid_timestamp.__doc__


    async def get_historical_klines(
        self,
        symbol,
        interval,
        start_str=None,
        end_str=None,
        limit=None,
        klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT,
    ):
        return await self._historical_klines(
            symbol,
            interval,
            start_str,
            end_str=end_str,
            limit=limit,
            klines_type=klines_type,
        )

    get_historical_klines.__doc__ = Client.get_historical_klines.__doc__


    async def _historical_klines(
        self,
        symbol,
        interval,
        start_str=None,
        end_str=None,
        limit=None,
        klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT,
    ):
        initial_limit_set = True
        if limit is None:
            limit = 1000
            initial_limit_set = False

        # init our list
        output_data = []

        # convert interval to useful value in seconds
        timeframe = interval_to_milliseconds(interval)

        # establish first available start timestamp
        start_ts = convert_ts_str(start_str)
        if start_ts is not None:
            first_valid_ts = await self._get_earliest_valid_timestamp(
                symbol, interval, klines_type
            )
            start_ts = max(start_ts, first_valid_ts)

        # if an end time was passed convert it
        end_ts = convert_ts_str(end_str)
        if end_ts and start_ts and end_ts <= start_ts:
            return output_data

        idx = 0
        while True:
            # fetch the klines from start_ts up to max 500 entries or the end_ts if set
            temp_data = await self._klines(
                klines_type=klines_type,
                symbol=symbol,
                interval=interval,
                limit=limit,
                startTime=start_ts,
                endTime=end_ts,
            )

            # append this loops data to our output data
            if temp_data:
                output_data += temp_data

            # check if output_data is greater than limit and truncate if needed and break loop
            if initial_limit_set and len(output_data) > limit:
                output_data = output_data[:limit]
                break

            # handle the case where exactly the limit amount of data was returned last loop
            # or check if we received less than the required limit and exit the loop
            if not len(temp_data) or len(temp_data) < limit:
                # exit the while loop
                break

            # set our start timestamp using the last value in the array
            # and increment next call by our timeframe
            start_ts = temp_data[-1][0] + timeframe

            # exit loop if we reached end_ts before reaching <limit> klines
            if end_ts and start_ts >= end_ts:
                break

            # sleep after every 3rd call to be kind to the API
            idx += 1
            if idx % 3 == 0:
                await asyncio.sleep(1)

        return output_data

    _historical_klines.__doc__ = Client._historical_klines.__doc__


    async def get_historical_klines_generator(
        self,
        symbol,
        interval,
        start_str=None,
        end_str=None,
        limit=1000,
        klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT,
    ):
        return self._historical_klines_generator(
            symbol,
            interval,
            start_str,
            end_str=end_str,
            limit=limit,
            klines_type=klines_type,
        )

    get_historical_klines_generator.__doc__ = (
        Client.get_historical_klines_generator.__doc__
    )


    async def _historical_klines_generator(
        self,
        symbol,
        interval,
        start_str=None,
        end_str=None,
        limit=1000,
        klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT,
    ):
        # convert interval to useful value in seconds
        timeframe = interval_to_milliseconds(interval)

        # if a start time was passed convert it
        start_ts = convert_ts_str(start_str)

        # establish first available start timestamp
        if start_ts is not None:
            first_valid_ts = await self._get_earliest_valid_timestamp(
                symbol, interval, klines_type
            )
            start_ts = max(start_ts, first_valid_ts)

        # if an end time was passed convert it
        end_ts = convert_ts_str(end_str)
        if end_ts and start_ts and end_ts <= start_ts:
            return

        idx = 0
        while True:
            # fetch the klines from start_ts up to max 500 entries or the end_ts if set
            output_data = await self._klines(
                klines_type=klines_type,
                symbol=symbol,
                interval=interval,
                limit=limit,
                startTime=start_ts,
                endTime=end_ts,
            )

            # yield data
            if output_data:
                for o in output_data:
                    yield o

            # handle the case where exactly the limit amount of data was returned last loop
            # check if we received less than the required limit and exit the loop
            if not len(output_data) or len(output_data) < limit:
                # exit the while loop
                break

            # increment next call by our timeframe
            start_ts = output_data[-1][0] + timeframe

            # exit loop if we reached end_ts before reaching <limit> klines
            if end_ts and start_ts >= end_ts:
                break

            # sleep after every 3rd call to be kind to the API
            idx += 1
            if idx % 3 == 0:
                await asyncio.sleep(1)

    _historical_klines_generator.__doc__ = Client._historical_klines_generator.__doc__


    async def get_avg_price(self, **params):
        return await self._get("avgPrice", data=params)

    get_avg_price.__doc__ = Client.get_avg_price.__doc__


    async def get_ticker(self, **params):
        return await self._get("ticker/24hr", data=params)

    get_ticker.__doc__ = Client.get_ticker.__doc__


    async def get_symbol_ticker(self, **params):
        return await self._get("ticker/price", data=params)

    get_symbol_ticker.__doc__ = Client.get_symbol_ticker.__doc__


    async def get_symbol_ticker_window(self, **params):
        return await self._get("ticker", data=params)

    get_symbol_ticker_window.__doc__ = Client.get_symbol_ticker_window.__doc__


    async def get_orderbook_ticker(self, **params):
        return await self._get("ticker/bookTicker", data=params)

    get_orderbook_ticker.__doc__ = Client.get_orderbook_ticker.__doc__

    # Account Endpoints


    async def create_order(self, **params):
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.SPOT_ORDER_PREFIX + self.uuid22()
        return await self._post("order", True, data=params)

    create_order.__doc__ = Client.create_order.__doc__


    async def order_limit(self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params):
        params.update({"type": self.ORDER_TYPE_LIMIT, "timeInForce": timeInForce})
        return await self.create_order(**params)

    order_limit.__doc__ = Client.order_limit.__doc__


    async def order_limit_buy(self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params):
        params.update(
            {
                "side": self.SIDE_BUY,
            }
        )
        return await self.order_limit(timeInForce=timeInForce, **params)

    order_limit_buy.__doc__ = Client.order_limit_buy.__doc__


    async def order_limit_sell(
        self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params
    ):
        params.update({"side": self.SIDE_SELL})
        return await self.order_limit(timeInForce=timeInForce, **params)

    order_limit_sell.__doc__ = Client.order_limit_sell.__doc__


    async def order_market(self, **params):
        params.update({"type": self.ORDER_TYPE_MARKET})
        return await self.create_order(**params)

    order_market.__doc__ = Client.order_market.__doc__


    async def order_market_buy(self, **params):
        params.update({"side": self.SIDE_BUY})
        return await self.order_market(**params)

    order_market_buy.__doc__ = Client.order_market_buy.__doc__


    async def order_market_sell(self, **params):
        params.update({"side": self.SIDE_SELL})
        return await self.order_market(**params)

    order_market_sell.__doc__ = Client.order_market_sell.__doc__


    async def order_oco_buy(self, **params):
        params.update({"side": self.SIDE_BUY})
        return await self.create_oco_order(**params)

    order_oco_buy.__doc__ = Client.order_oco_buy.__doc__


    async def order_oco_sell(self, **params):
        params.update({"side": self.SIDE_SELL})
        return await self.create_oco_order(**params)

    order_oco_sell.__doc__ = Client.order_oco_sell.__doc__


    async def create_test_order(self, **params):
        return await self._post("order/test", True, data=params)

    create_test_order.__doc__ = Client.create_test_order.__doc__


    async def get_order(self, **params):
        return await self._get("order", True, data=params)

    get_order.__doc__ = Client.get_order.__doc__


    async def get_all_orders(self, **params):
        return await self._get("allOrders", True, data=params)

    get_all_orders.__doc__ = Client.get_all_orders.__doc__


    async def cancel_order(self, **params):
        return await self._delete("order", True, data=params)

    cancel_order.__doc__ = Client.cancel_order.__doc__


    async def get_open_orders(self, **params):
        return await self._get("openOrders", True, data=params)

    get_open_orders.__doc__ = Client.get_open_orders.__doc__


    async def get_open_oco_orders(self, **params):
        return await self._get("openOrderList", True, data=params)

    get_open_oco_orders.__doc__ = Client.get_open_oco_orders.__doc__

    # User Stream Endpoints

    async def get_account(self, **params):
        return await self._get("account", True, data=params)

    get_account.__doc__ = Client.get_account.__doc__


    async def get_asset_balance(self, asset=None, **params):
        res = await self.get_account(**params)
        # find asset balance in list of balances
        if "balances" in res:
            if asset:
                for bal in res["balances"]:
                    if bal["asset"].lower() == asset.lower():
                        return bal
            else:
                return res["balances"]
        return None

    get_asset_balance.__doc__ = Client.get_asset_balance.__doc__


    async def get_my_trades(self, **params):
        return await self._get("myTrades", True, data=params)

    get_my_trades.__doc__ = Client.get_my_trades.__doc__


    async def get_current_order_count(self, **params):
        return await self._get("rateLimit/order", True, data=params)

    get_current_order_count.__doc__ = Client.get_current_order_count.__doc__


    async def get_prevented_matches(self, **params):
        return await self._get("myPreventedMatches", True, data=params)

    get_prevented_matches.__doc__ = Client.get_prevented_matches.__doc__


    async def get_allocations(self, **params):
        return await self._get("myAllocations", True, data=params)

    get_allocations.__doc__ = Client.get_allocations.__doc__

    # User Stream Endpoints


    async def stream_get_listen_key(self):
        res = await self._post("userDataStream", False, data={})
        return res["listenKey"]

    stream_get_listen_key.__doc__ = Client.stream_get_listen_key.__doc__


    async def stream_keepalive(self, listenKey):
        params = {"listenKey": listenKey}
        return await self._put("userDataStream", False, data=params)

    stream_keepalive.__doc__ = Client.stream_keepalive.__doc__


    async def stream_close(self, listenKey):
        params = {"listenKey": listenKey}
        return await self._delete("userDataStream", False, data=params)

    stream_close.__doc__ = Client.stream_close.__doc__

    async def v3_delete_open_orders(self, **params):
        return await self._request_api(
            "delete", "openOrders", signed=True, data=params, version="v3"
        )

    v3_delete_open_orders.__doc__ = Client.v3_delete_open_orders.__doc__

    async def v3_delete_order(self, **params):
        return await self._request_api(
            "delete", "order", signed=True, data=params, version="v3"
        )

    v3_delete_order.__doc__ = Client.v3_delete_order.__doc__

    async def v3_delete_order_list(self, **params):
        return await self._request_api(
            "delete", "orderList", signed=True, data=params, version="v3"
        )

    v3_delete_order_list.__doc__ = Client.v3_delete_order_list.__doc__

    async def v3_delete_user_data_stream(self, **params):
        return await self._request_api(
            "delete", "userDataStream", signed=True, data=params, version="v3"
        )

    v3_delete_user_data_stream.__doc__ = Client.v3_delete_user_data_stream.__doc__

    async def v3_get_account(self, **params):
        return await self._request_api(
            "get", "account", signed=True, data=params, version="v3"
        )

    v3_get_account.__doc__ = Client.v3_get_account.__doc__

    async def v3_get_account_commission(self, **params):
        return await self._request_api(
            "get", "account/commission", signed=True, data=params, version="v3"
        )

    v3_get_account_commission.__doc__ = Client.v3_get_account_commission.__doc__

    async def v3_get_all_order_list(self, **params):
        return await self._request_api(
            "get", "allOrderList", signed=True, data=params, version="v3"
        )

    v3_get_all_order_list.__doc__ = Client.v3_get_all_order_list.__doc__

    async def v3_get_all_orders(self, **params):
        return await self._request_api(
            "get", "allOrders", signed=True, data=params, version="v3"
        )

    v3_get_all_orders.__doc__ = Client.v3_get_all_orders.__doc__

    async def v3_get_my_allocations(self, **params):
        return await self._request_api(
            "get", "myAllocations", signed=True, data=params, version="v3"
        )

    v3_get_my_allocations.__doc__ = Client.v3_get_my_allocations.__doc__

    async def v3_get_my_prevented_matches(self, **params):
        return await self._request_api(
            "get", "myPreventedMatches", signed=True, data=params, version="v3"
        )

    v3_get_my_prevented_matches.__doc__ = Client.v3_get_my_prevented_matches.__doc__

    async def v3_get_my_trades(self, **params):
        return await self._request_api(
            "get", "myTrades", signed=True, data=params, version="v3"
        )

    v3_get_my_trades.__doc__ = Client.v3_get_my_trades.__doc__

    async def v3_get_open_order_list(self, **params):
        return await self._request_api(
            "get", "openOrderList", signed=True, data=params, version="v3"
        )

    v3_get_open_order_list.__doc__ = Client.v3_get_open_order_list.__doc__

    async def v3_get_open_orders(self, **params):
        return await self._request_api(
            "get", "openOrders", signed=True, data=params, version="v3"
        )

    v3_get_open_orders.__doc__ = Client.v3_get_open_orders.__doc__

    async def v3_get_order(self, **params):
        return await self._request_api(
            "get", "order", signed=True, data=params, version="v3"
        )

    v3_get_order.__doc__ = Client.v3_get_order.__doc__

    async def v3_get_order_list(self, **params):
        return await self._request_api(
            "get", "orderList", signed=True, data=params, version="v3"
        )

    v3_get_order_list.__doc__ = Client.v3_get_order_list.__doc__

    async def v3_get_rate_limit_order(self, **params):
        return await self._request_api(
            "get", "rateLimit/order", signed=True, data=params, version="v3"
        )

    v3_get_rate_limit_order.__doc__ = Client.v3_get_rate_limit_order.__doc__

    async def v3_get_ticker_trading_day(self, **params):
        return await self._request_api(
            "get", "ticker/tradingDay", signed=False, data=params, version="v3"
        )

    v3_get_ticker_trading_day.__doc__ = Client.v3_get_ticker_trading_day.__doc__

    async def v3_post_cancel_replace(self, **params):
        return await self._request_api(
            "post", "cancelReplace", signed=True, data=params, version="v3"
        )

    v3_post_cancel_replace.__doc__ = Client.v3_post_cancel_replace.__doc__

    async def v3_post_order(self, **params):
        return await self._request_api(
            "post", "order", signed=True, data=params, version="v3"
        )

    v3_post_order.__doc__ = Client.v3_post_order.__doc__

    async def v3_post_order_cancel_replace(self, **params):
        return await self._request_api(
            "post", "order/cancelReplace", signed=True, data=params, version="v3"
        )

    v3_post_order_cancel_replace.__doc__ = Client.v3_post_order_cancel_replace.__doc__

    async def v3_post_order_list_oco(self, **params):
        return await self._request_api(
            "post", "orderList/oco", signed=True, data=params, version="v3"
        )

    v3_post_order_list_oco.__doc__ = Client.v3_post_order_list_oco.__doc__

    async def v3_post_order_list_oto(self, **params):
        return await self._request_api(
            "post", "orderList/oto", signed=True, data=params, version="v3"
        )

    v3_post_order_list_oto.__doc__ = Client.v3_post_order_list_oto.__doc__

    async def v3_post_order_list_otoco(self, **params):
        return await self._request_api(
            "post", "orderList/otoco", signed=True, data=params, version="v3"
        )

    v3_post_order_list_otoco.__doc__ = Client.v3_post_order_list_otoco.__doc__

    async def v3_post_order_test(self, **params):
        return await self._request_api(
            "post", "order/test", signed=True, data=params, version="v3"
        )

    v3_post_order_test.__doc__ = Client.v3_post_order_test.__doc__

    async def v3_post_sor_order(self, **params):
        return await self._request_api(
            "post", "sor/order", signed=True, data=params, version="v3"
        )

    v3_post_sor_order.__doc__ = Client.v3_post_sor_order.__doc__

    async def v3_post_sor_order_test(self, **params):
        return await self._request_api(
            "post", "sor/order/test", signed=True, data=params, version="v3"
        )

    v3_post_sor_order_test.__doc__ = Client.v3_post_sor_order_test.__doc__

    async def v3_post_user_data_stream(self, **params):
        return await self._request_api(
            "post", "userDataStream", signed=True, data=params, version="v3"
        )

    v3_post_user_data_stream.__doc__ = Client.v3_post_user_data_stream.__doc__

    async def v3_put_user_data_stream(self, **params):
        return await self._request_api(
            "put", "userDataStream", signed=True, data=params, version="v3"
        )

    v3_put_user_data_stream.__doc__ = Client.v3_put_user_data_stream.__doc__

    
