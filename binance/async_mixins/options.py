"""
AsyncOptionsMixin - Options

This mixin contains all Options related methods.
"""
from typing import Dict, Any, Optional, TYPE_CHECKING

# This mixin depends on request methods provided by AsyncClientCore

if TYPE_CHECKING:
    from ._core_typing import AsyncClientCoreLike as _AsyncClientCoreLike
else:
    class _AsyncClientCoreLike:
        pass


class AsyncOptionsMixin(_AsyncClientCoreLike):
    """
    Options API Mixin
    
    This mixin provides all Options related methods.
    These methods depend on request infrastructure provided by AsyncClientCore or ClientCore.
    """

    async def options_ping(self):
        return await self._request_options_api("get", "ping")


    async def options_time(self):
        return await self._request_options_api("get", "time")


    async def options_info(self):
        return await self._request_options_api("get", "optionInfo")


    async def options_exchange_info(self):
        return await self._request_options_api("get", "exchangeInfo")


    async def options_index_price(self, **params):
        return await self._request_options_api("get", "index", data=params)


    async def options_price(self, **params):
        return await self._request_options_api("get", "ticker", data=params)


    async def options_mark_price(self, **params):
        return await self._request_options_api("get", "mark", data=params)


    async def options_order_book(self, **params):
        return await self._request_options_api("get", "depth", data=params)


    async def options_klines(self, **params):
        return await self._request_options_api("get", "klines", data=params)


    async def options_recent_trades(self, **params):
        return await self._request_options_api("get", "trades", data=params)


    async def options_historical_trades(self, **params):
        return await self._request_options_api("get", "historicalTrades", data=params)

    # Account and trading interface endpoints


    async def options_account_info(self, **params):
        return await self._request_options_api(
            "get", "account", signed=True, data=params
        )


    async def options_funds_transfer(self, **params):
        return await self._request_options_api(
            "post", "transfer", signed=True, data=params
        )


    async def options_positions(self, **params):
        return await self._request_options_api(
            "get", "position", signed=True, data=params
        )


    async def options_bill(self, **params):
        return await self._request_options_api("post", "bill", signed=True, data=params)


    async def options_place_order(self, **params):
        if "clientOrderId" not in params:
            params["clientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return await self._request_options_api(
            "post", "order", signed=True, data=params
        )


    async def options_place_batch_order(self, **params):
        for order in params["batchOrders"]:
            if "newClientOrderId" not in order:
                order["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return await self._request_options_api(
            "post", "batchOrders", signed=True, data=params
        )


    async def options_cancel_order(self, **params):
        return await self._request_options_api(
            "delete", "order", signed=True, data=params
        )


    async def options_cancel_batch_order(self, **params):
        return await self._request_options_api(
            "delete", "batchOrders", signed=True, data=params
        )


    async def options_cancel_all_orders(self, **params):
        return await self._request_options_api(
            "delete", "allOpenOrders", signed=True, data=params
        )


    async def options_query_order(self, **params):
        return await self._request_options_api("get", "order", signed=True, data=params)


    async def options_query_pending_orders(self, **params):
        return await self._request_options_api(
            "get", "openOrders", signed=True, data=params
        )


    async def options_query_order_history(self, **params):
        return await self._request_options_api(
            "get", "historyOrders", signed=True, data=params
        )


    async def options_user_trades(self, **params):
        return await self._request_options_api(
            "get", "userTrades", signed=True, data=params
        )

    # Block Trade Endpoints


    async def options_create_block_trade_order(self, **params):
        return await self._request_options_api(
            "post", "block/order/create", signed=True, data=params
        )


    async def options_cancel_block_trade_order(self, **params):
        return await self._request_options_api(
            "delete", "block/order/create", signed=True, data=params
        )


    async def options_extend_block_trade_order(self, **params):
        return await self._request_options_api(
            "put", "block/order/create", signed=True, data=params
        )


    async def options_get_block_trade_orders(self, **params):
        return await self._request_options_api(
            "get", "block/order/orders", signed=True, data=params
        )


    async def options_accept_block_trade_order(self, **params):
        return await self._request_options_api(
            "post", "block/order/execute", signed=True, data=params
        )


    async def options_get_block_trade_order(self, **params):
        return await self._request_options_api(
            "get", "block/order/execute", signed=True, data=params
        )


    async def options_account_get_block_trades(self, **params):
        return await self._request_options_api(
            "get", "block/user-trades", signed=True, data=params
        )

    # Countdown Cancel All Endpoints


    async def options_v1_get_countdown_cancel_all(self, **params):
        return await self._request_options_api(
            "get", "countdownCancelAll", signed=True, data=params
        )


    async def options_v1_post_countdown_cancel_all(self, **params):
        return await self._request_options_api(
            "post", "countdownCancelAll", signed=True, data=params
        )


    async def options_v1_post_countdown_cancel_all_heart_beat(self, **params):
        return await self._request_options_api(
            "post", "countdownCancelAllHeartBeat", signed=True, data=params
        )

    # Advanced Order Management


    async def options_v1_delete_all_open_orders_by_underlying(self, **params):
        return await self._request_options_api(
            "delete", "allOpenOrdersByUnderlying", signed=True, data=params
        )

    # Account and Margin


    async def options_v1_get_margin_account(self, **params):
        return await self._request_options_api(
            "get", "marginAccount", signed=True, data=params
        )


    async def options_v1_get_exercise_history(self, **params):
        return await self._request_options_api(
            "get", "exerciseHistory", signed=False, data=params
        )

    # Income History


    async def options_v1_get_income_asyn(self, **params):
        return await self._request_options_api(
            "get", "income/asyn", signed=True, data=params
        )


    async def options_v1_get_income_asyn_id(self, **params):
        return await self._request_options_api(
            "get", "income/asyn/id", signed=True, data=params
        )

    # Market Data - Block Trades


    async def options_v1_get_block_trades(self, **params):
        return await self._request_options_api(
            "get", "blockTrades", signed=False, data=params
        )

    # Fiat Endpoints

