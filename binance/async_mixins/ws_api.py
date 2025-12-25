"""
AsyncWsApiMixin - WebSocket API

This mixin contains all WebSocket API related methods.
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


class AsyncWsApiMixin(_AsyncClientCoreLike):
    """
    WebSocket API API Mixin
    
    This mixin provides all WebSocket API related methods.
    These methods depend on request infrastructure provided by AsyncClientCore or ClientCore.
    """

    async def ws_create_test_order(self, **params):
        """Test new order creation and signature/recvWindow long. Creates and validates a new order but does not send it into the matching engine.
        https://binance-docs.github.io/apidocs/websocket_api/en/#test-new-order-trade
        :param symbol: required
        :type symbol: str
        :param side: required
        :type side: str
        :param type: required
        :type type: str
        :param timeInForce: required if limit order
        :type timeInForce: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param icebergQty: Used with iceberg orders
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: The number of milliseconds the request is valid for
        :type recvWindow: int
        :returns: WS response
        .. code-block:: python
            {}
        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.SPOT_ORDER_PREFIX + self.uuid22()

        return await self._ws_api_request("order.test", True, params)


    async def ws_create_order(self, **params):
        """Create an order via WebSocket.
        https://binance-docs.github.io/apidocs/websocket_api/en/#place-new-order-trade
        :param id: The request ID to be used. By default uuid22() is used.
        :param symbol: The symbol to create an order for
        :param side: BUY or SELL
        :param type: Order type (e.g., LIMIT, MARKET)
        :param quantity: The amount to buy or sell
        :param kwargs: Additional order parameters
        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.SPOT_ORDER_PREFIX + self.uuid22()

        return await self._ws_api_request("order.place", True, params)


    async def ws_order_limit(self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params):
        """Send in a new limit order
        Any order with an icebergQty MUST have timeInForce set to GTC.
        :param symbol: required
        :type symbol: str
        :param side: required
        :type side: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param timeInForce: default Good till cancelled
        :type timeInForce: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param icebergQty: Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int
        :returns: WS response
        See order endpoint for full response options
        """
        params.update(
            {
                "type": self.ORDER_TYPE_LIMIT,
                "timeInForce": timeInForce,
            }
        )
        return await self.ws_create_order(**params)


    async def ws_order_limit_buy(
        self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params
    ):
        """Send in a new limit buy order
        Any order with an icebergQty MUST have timeInForce set to GTC.
        :param symbol: required
        :type symbol: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param timeInForce: default Good till cancelled
        :type timeInForce: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param stopPrice: Used with stop orders
        :type stopPrice: decimal
        :param icebergQty: Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int
        :returns: WS response
        See order endpoint for full response options
        """
        params.update(
            {
                "side": self.SIDE_BUY,
            }
        )
        return await self.ws_order_limit(timeInForce=timeInForce, **params)

    async def ws_order_limit_sell(
        self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params
    ):
        """Send in a new limit sell order
        Any order with an icebergQty MUST have timeInForce set to GTC.
        :param symbol: required
        :type symbol: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param timeInForce: default Good till cancelled
        :type timeInForce: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param stopPrice: Used with stop orders
        :type stopPrice: decimal
        :param icebergQty: Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int
        :returns: WS response
        See order endpoint for full response options
        """
        params.update({"side": self.SIDE_SELL})
        return await self.ws_order_limit(timeInForce=timeInForce, **params)

    async def ws_order_market(self, **params):
        """Send in a new market order
        :param symbol: required
        :type symbol: str
        :param side: required
        :type side: str
        :param quantity: required
        :type quantity: decimal
        :param quoteOrderQty: amount the user wants to spend (when buying) or receive (when selling)
            of the quote asset
        :type quoteOrderQty: decimal
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int
        :returns: WS response
        See order endpoint for full response options
        """
        params.update({"type": self.ORDER_TYPE_MARKET})
        return await self.ws_create_order(**params)


    async def ws_order_market_buy(self, **params):
        """Send in a new market buy order
        :param symbol: required
        :type symbol: str
        :param quantity: required
        :type quantity: decimal
        :param quoteOrderQty: the amount the user wants to spend of the quote asset
        :type quoteOrderQty: decimal
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int
        :returns: WS response
        See order endpoint for full response options
        """
        params.update({"side": self.SIDE_BUY})
        return await self.ws_order_market(**params)


    async def ws_order_market_sell(self, **params):
        """Send in a new market sell order
        :param symbol: required
        :type symbol: str
        :param quantity: required
        :type quantity: decimal
        :param quoteOrderQty: the amount the user wants to receive of the quote asset
        :type quoteOrderQty: decimal
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int
        :returns: WS response
        See order endpoint for full response options
        """
        params.update({"side": self.SIDE_SELL})
        return await self.ws_order_market(**params)


    async def ws_get_order(self, **params):
        """Check an order's status. Either orderId or origClientOrderId must be sent.
        https://binance-docs.github.io/apidocs/websocket_api/en/#query-order-user_data
        :param symbol: required
        :type symbol: str
        :param orderId: The unique order id
        :type orderId: int
        :param origClientOrderId: optional
        :type origClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int
        """

        return await self._ws_api_request("order.status", True, params)


    async def ws_cancel_order(self, **params):
        return await self._ws_api_request("order.cancel", True, params)


    async def ws_cancel_and_replace_order(self, **params):
        return await self._ws_api_request("order.cancelReplace", True, params)


    async def ws_get_open_orders(self, **params):
        return await self._ws_api_request("openOrders.status", True, params)


    async def ws_cancel_all_open_orders(self, **params):
        return await self._ws_api_request("openOrders.cancelAll", True, params)


    async def ws_create_oco_order(self, **params):
        return await self._ws_api_request("orderList.place.oco", True, params)


    async def ws_create_oto_order(self, **params):
        return await self._ws_api_request("orderList.place.oto", True, params)


    async def ws_create_otoco_order(self, **params):
        return await self._ws_api_request("orderList.place.otoco", True, params)


    async def ws_get_oco_order(self, **params):
        return await self._ws_api_request("orderList.status", True, params)


    async def ws_cancel_oco_order(self, **params):
        return await self._ws_api_request("orderList.cancel", True, params)


    async def ws_get_oco_open_orders(self, **params):
        return await self._ws_api_request("openOrderLists.status", True, params)


    async def ws_create_sor_order(self, **params):
        return await self._ws_api_request("sor.order.place", True, params)


    async def ws_create_test_sor_order(self, **params):
        return await self._ws_api_request("sor.order.test", True, params)


    async def ws_get_account(self, **params):
        return await self._ws_api_request("account.status", True, params)


    async def ws_get_account_rate_limits_orders(self, **params):
        return await self._ws_api_request("account.rateLimits.orders", True, params)


    async def ws_get_all_orders(self, **params):
        return await self._ws_api_request("allOrders", True, params)


    async def ws_get_my_trades(self, **params):
        return await self._ws_api_request("myTrades", True, params)


    async def ws_get_prevented_matches(self, **params):
        return await self._ws_api_request("myPreventedMatches", True, params)


    async def ws_get_allocations(self, **params):
        return await self._ws_api_request("myAllocations", True, params)


    async def ws_get_commission_rates(self, **params):
        return await self._ws_api_request("account.commission", True, params)


    async def ws_get_order_book(self, **params):
        return await self._ws_api_request("depth", False, params)


    async def ws_get_recent_trades(self, **params):
        return await self._ws_api_request("trades.recent", False, params)


    async def ws_get_historical_trades(self, **params):
        return await self._ws_api_request("trades.historical", False, params)


    async def ws_get_aggregate_trades(self, **params):
        return await self._ws_api_request("trades.aggregate", False, params)


    async def ws_get_klines(self, **params):
        return await self._ws_api_request("klines", False, params)


    async def ws_get_uiKlines(self, **params):
        return await self._ws_api_request("uiKlines", False, params)


    async def ws_get_avg_price(self, **params):
        return await self._ws_api_request("avgPrice", False, params)


    async def ws_get_ticker(self, **params):
        return await self._ws_api_request("ticker.24hr", False, params)


    async def ws_get_trading_day_ticker(self, **params):
        return await self._ws_api_request("ticker.tradingDay", False, params)


    async def ws_get_symbol_ticker_window(self, **params):
        return await self._ws_api_request("ticker", False, params)


    async def ws_get_symbol_ticker(self, **params):
        return await self._ws_api_request("ticker.price", False, params)


    async def ws_get_orderbook_ticker(self, **params):
        return await self._ws_api_request("ticker.book", False, params)


    async def ws_ping(self, **params):
        return await self._ws_api_request("ping", False, params)


    async def ws_get_time(self, **params):
        return await self._ws_api_request("time", False, params)


    async def ws_get_exchange_info(self, **params):
        return await self._ws_api_request("exchangeInfo", False, params)


    async def ws_futures_get_order_book(self, **params):
        """
        Get the order book for a symbol
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/websocket-api
        """
        return await self._ws_futures_api_request("depth", False, params)


    async def ws_futures_get_all_tickers(self, **params):
        """
        Latest price for a symbol or symbols
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/websocket-api/Symbol-Price-Ticker
        """
        return await self._ws_futures_api_request("ticker.price", False, params)


    async def ws_futures_get_order_book_ticker(self, **params):
        """
        Best price/qty on the order book for a symbol or symbols.
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/websocket-api/Symbol-Order-Book-Ticker
        """
        return await self._ws_futures_api_request("ticker.book", False, params)


    async def ws_futures_create_order(self, **params):
        """
        Send in a new order
        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/websocket-api
        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return await self._ws_futures_api_request("order.place", True, params)


    async def ws_futures_edit_order(self, **params):
        """
        Edit an order
        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/websocket-api/Modify-Order
        """
        return await self._ws_futures_api_request("order.modify", True, params)


    async def ws_futures_cancel_order(self, **params):
        """
        cancel an order
        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/websocket-api/Cancel-Order
        """
        return await self._ws_futures_api_request("order.cancel", True, params)


    async def ws_futures_get_order(self, **params):
        """
        Get an order
        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/websocket-api/Query-Order
        """
        return await self._ws_futures_api_request("order.status", True, params)


    async def ws_futures_v2_account_position(self, **params):
        """
        Get current position information(only symbol that has position or open orders will be return awaited).
        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/websocket-api/Position-Info-V2
        """
        return await self._ws_futures_api_request("v2/account.position", True, params)


    async def ws_futures_account_position(self, **params):
        """
        Get current position information.
        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/websocket-api/Position-Information
        """
        return await self._ws_futures_api_request("account.position", True, params)


    async def ws_futures_v2_account_balance(self, **params):
        """
        Get current account information.
        https://developers.binance.com/docs/derivatives/usds-margined-futures/account/websocket-api#api-description
        """
        return await self._ws_futures_api_request("v2/account.balance", True, params)


    async def ws_futures_account_balance(self, **params):
        """
        Get current account information.
        https://developers.binance.com/docs/derivatives/usds-margined-futures/account/websocket-api/Futures-Account-Balance
        """
        return await self._ws_futures_api_request("account.balance", True, params)


    async def ws_futures_v2_account_status(self, **params):
        """
        Get current account information. User in single-asset/ multi-assets mode will see different value, see comments in response section for detail.
        https://developers.binance.com/docs/derivatives/usds-margined-futures/account/websocket-api/Account-Information-V2
        """
        return await self._ws_futures_api_request("v2/account.status", True, params)


    async def ws_futures_account_status(self, **params):
        """
        Get current account information. User in single-asset/ multi-assets mode will see different value, see comments in response section for detail.
        https://developers.binance.com/docs/derivatives/usds-margined-futures/account/websocket-api/Account-Information
        """
        return await self._ws_futures_api_request("account.status", True, params)

    ####################################################
    # Gift Card API Endpoints
    ####################################################

