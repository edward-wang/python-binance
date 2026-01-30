"""
WsApiMixin - WebSocket API

此 mixin 包含所有 WebSocket API 相关的方法。
"""
from typing import Dict, Any, Optional
from ..base_client import BaseClient

# 此 mixin 依赖 ClientCore 提供的请求方法


class WsApiMixin:
    """
    WebSocket API API Mixin
    
    此 mixin 提供所有 WebSocket API 相关的方法。
    这些方法依赖 AsyncClientCore 或 ClientCore 提供的请求基础设施。
    """

    def ws_create_test_order(self, **params):
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

        return self._ws_api_request_sync("order.test", True, params)


    def ws_create_order(self, **params):
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

        return self._ws_api_request_sync("order.place", True, params)


    def ws_order_limit(self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params):
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
        params.update({
            "type": self.ORDER_TYPE_LIMIT,
            "timeInForce": timeInForce,
        })
        return self.ws_create_order(**params)


    def ws_order_limit_buy(self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params):
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
        :param icebergQty: Used with iceberg orders
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int
        :returns: WS response
        See order endpoint for full response options
        """
        params.update({
            "side": self.SIDE_BUY,
        })
        return self.ws_order_limit(timeInForce=timeInForce, **params)


    def ws_order_limit_sell(self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params):
        """Send in a new limit sell order
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
        :param icebergQty: Used with iceberg orders
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int
        :returns: WS response
        See order endpoint for full response options
        """
        params.update({"side": self.SIDE_SELL})
        return self.ws_order_limit(timeInForce=timeInForce, **params)


    def ws_order_market(self, **params):
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
        return self.ws_create_order(**params)


    def ws_order_market_buy(self, **params):
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
        return self.ws_order_market(**params)


    def ws_order_market_sell(self, **params):
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
        return self.ws_order_market(**params)


    def ws_get_order(self, **params):
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
        return self._ws_api_request_sync("order.status", True, params)


    def ws_cancel_order(self, **params):
        """Cancel an active order.
        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#cancel-order-trade

        :param symbol: required - Trading symbol, e.g. 'BTCUSDT'
        :type symbol: str
        :param orderId: optional - The unique order id
        :type orderId: int
        :param origClientOrderId: optional - The original client order id
        :type origClientOrderId: str
        :param newClientOrderId: optional - Used to uniquely identify this cancel. Automatically generated if not sent
        :type newClientOrderId: str
        :param cancelRestrictions: optional - ONLY_NEW - Cancel will succeed if the order status is NEW. ONLY_PARTIALLY_FILLED - Cancel will succeed if order status is PARTIALLY_FILLED.
        :type cancelRestrictions: str
        :param recvWindow: optional - The number of milliseconds the request is valid for
        :type recvWindow: int

        Either orderId or origClientOrderId must be sent.

        Weight: 1

        Returns:
        .. code-block:: python
            {
                "id": "5633b6a2-90a9-4192-83e7-925c90b6a2fd",
                "method": "order.cancel",
                "params": {
                    "symbol": "BTCUSDT",
                    "origClientOrderId": "4d96324ff9d44481926157",
                    "apiKey": "vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A",
                    "signature": "33d5b721f278ae17a52f004a82a6f68a70c68e7dd6776ed0be77a455ab855282",
                    "timestamp": 1660801715830
                }
            }
        """
        return self._ws_api_request_sync("order.cancel", True, params)


    def ws_cancel_and_replace_order(self, **params):
        """Cancels an existing order and places a new order on the same symbol.
        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#cancel-and-replace-order-trade

        :param symbol: required - Trading symbol, e.g. 'BTCUSDT'
        :type symbol: str
        :param cancelReplaceMode: required - The mode of cancel-replace: STOP_ON_FAILURE - If the cancel request fails, new order placement will not be attempted. ALLOW_FAILURE - New order placement will be attempted even if cancel request fails
        :type cancelReplaceMode: str
        :param cancelOrderId: optional - The order ID to cancel
        :type cancelOrderId: int
        :param cancelOrigClientOrderId: optional - The original client order ID to cancel
        :type cancelOrigClientOrderId: str
        :param cancelNewClientOrderId: optional - Used to uniquely identify this cancel. Automatically generated if not sent
        :type cancelNewClientOrderId: str
        :param side: required - BUY or SELL
        :type side: str
        :param type: required - Order type, e.g. LIMIT, MARKET
        :type type: str
        :param timeInForce: optional - GTC, IOC, FOK
        :type timeInForce: str
        :param price: optional - Order price
        :type price: str
        :param quantity: optional - Order quantity
        :type quantity: str
        :param quoteOrderQty: optional - Quote quantity
        :type quoteOrderQty: str
        :param newClientOrderId: optional - Used to uniquely identify this new order
        :type newClientOrderId: str
        :param newOrderRespType: optional - ACK, RESULT, or FULL
        :type newOrderRespType: str
        :param stopPrice: optional - Used with STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, and TAKE_PROFIT_LIMIT orders
        :type stopPrice: str
        :param trailingDelta: optional - Used with TAKE_PROFIT, TAKE_PROFIT_LIMIT, STOP_LOSS, STOP_LOSS_LIMIT orders
        :type trailingDelta: int
        :param icebergQty: optional - Used with iceberg orders
        :type icebergQty: str
        :param strategyId: optional - Arbitrary numeric value identifying the order within an order strategy
        :type strategyId: int
        :param strategyType: optional - Arbitrary numeric value identifying the order strategy
        :type strategyType: int
        :param selfTradePreventionMode: optional - The allowed enums is dependent on what is configured on the symbol
        :type selfTradePreventionMode: str
        :param cancelRestrictions: optional - ONLY_NEW - Cancel will succeed if order status is NEW. ONLY_PARTIALLY_FILLED - Cancel will succeed if order status is PARTIALLY_FILLED
        :type cancelRestrictions: str
        :param recvWindow: optional - The number of milliseconds the request is valid for
        :type recvWindow: int

        Either cancelOrderId or cancelOrigClientOrderId must be provided.
        Price is required for LIMIT orders.
        Either quantity or quoteOrderQty must be provided.

        Weight: 1

        Returns:
        .. code-block:: python
           {
                "id": "99de6b92-0eda-4154-9c8d-a51d93c6f92e",
                "status": 200,
                "result": {
                    "cancelResult": "SUCCESS",
                    "newOrderResult": "SUCCESS",
                    "cancelResponse": {
                        "symbol": "BTCUSDT",
                        "origClientOrderId": "4d96324ff9d44481926157",
                        "orderId": 12569099453,
                        "orderListId": -1,
                        "clientOrderId": "91fe37ce9e69c90d6358c0",
                        "price": "23416.10000000",
                        "origQty": "0.00847000",
                        "executedQty": "0.00001000",
                        "cummulativeQuoteQty": "0.23416100",
                        "status": "CANCELED",
                        "timeInForce": "GTC",
                        "type": "LIMIT",
                        "side": "SELL",
                        "selfTradePreventionMode": "NONE"
                    },
                    "newOrderResponse": {
                        "symbol": "BTCUSDT",
                        "orderId": 12569099454,
                        "orderListId": -1,
                        "clientOrderId": "bX5wROblo6YeDwa9iTLeyY",
                        "transactTime": 1660801715639
                    }
                }
            }
        """
        return self._ws_api_request_sync("order.cancelReplace", True, params)


    def ws_get_open_orders(self, **params):
        """Get all open orders on a symbol or all symbols.
        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#current-open-orders-user_data

        :param symbol: optional - Symbol to get open orders for
        :type symbol: str
        :param recvWindow: optional - The value cannot be greater than 60000
        :type recvWindow: int

        :returns: API response

        Response format:
        [
            {
                "symbol": "BTCUSDT",
                "orderId": 12569099453,
                "orderListId": -1,
                "clientOrderId": "4d96324ff9d44481926157",
                "price": "23416.10000000",
                "origQty": "0.00847000",
                "executedQty": "0.00720000",
                "cummulativeQuoteQty": "168.59532000",
                "status": "PARTIALLY_FILLED",
                "timeInForce": "GTC",
                "type": "LIMIT",
                "side": "SELL",
                "stopPrice": "0.00000000",
                "icebergQty": "0.00000000",
                "time": 1660801715639,
                "updateTime": 1660801717945,
                "isWorking": true,
                "workingTime": 1660801715639,
                "origQuoteOrderQty": "0.00000000",
                "selfTradePreventionMode": "NONE"
            }
        ]

        Weight: Adjusted based on parameters:
        - With symbol: 6
        - Without symbol: 12
        """
        return self._ws_api_request_sync("openOrders.status", True, params)


    def ws_cancel_all_open_orders(self, **params):
        """Cancel all open orders on a symbol or all symbols.
        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#cancel-open-orders-trade

        :param symbol: optional - Symbol to cancel orders for
        :type symbol: str
        :param recvWindow: optional - The value cannot be greater than 60000
        :type recvWindow: int

        :returns: Websocket message

        Response format:
        [
            {
                "symbol": "BTCUSDT",
                "origClientOrderId": "4d96324ff9d44481926157",
                "orderId": 12569099453,
                "orderListId": -1,
                "clientOrderId": "91fe37ce9e69c90d6358c0",
                "price": "23416.10000000",
                "origQty": "0.00847000",
                "executedQty": "0.00847000",
                "cummulativeQuoteQty": "198.33521500",
                "status": "CANCELED",
                "timeInForce": "GTC",
                "type": "LIMIT",
                "side": "SELL",
                "stopPrice": "0.00000000",
                "trailingDelta": 0,
                "trailingTime": -1,
                "icebergQty": "0.00000000",
                "strategyId": 37463720,
                "strategyType": 1000000,
                "selfTradePreventionMode": "NONE"
            }
        ]

        Weight: 1
        """
        return self._ws_api_request_sync("openOrders.cancelAll", True, params)


    def ws_create_oco_order(self, **params):
        """Create a new OCO (One-Cancels-the-Other) order.
        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#place-new-order-list---oco-trade

        :param symbol: required - Trading symbol
        :type symbol: str
        :param side: required - BUY or SELL
        :type side: str
        :param quantity: required - Order quantity
        :type quantity: decimal
        :param price: required - Order price for limit leg
        :type price: decimal
        :param stopPrice: required - Stop trigger price for stop leg
        :type stopPrice: decimal
        :param stopLimitPrice: optional - Stop limit price for stop leg
        :type stopLimitPrice: decimal
        :param stopLimitTimeInForce: optional - Time in force for stop leg
        :type stopLimitTimeInForce: str
        :param listClientOrderId: optional - Unique ID for the entire orderList
        :type listClientOrderId: str
        :param limitClientOrderId: optional - Unique ID for the limit order
        :type limitClientOrderId: str
        :param stopClientOrderId: optional - Unique ID for the stop order
        :type stopClientOrderId: str
        :param limitStrategyId: optional - Arbitrary numeric value identifying the limit order within an order strategy
        :type limitStrategyId: int
        :param limitStrategyType: optional - Arbitrary numeric value identifying the limit order strategy
        :type limitStrategyType: int
        :param stopStrategyId: optional - Arbitrary numeric value identifying the stop order within an order strategy
        :type stopStrategyId: int
        :param stopStrategyType: optional - Arbitrary numeric value identifying the stop order strategy
        :type stopStrategyType: int
        :param limitIcebergQty: optional - Iceberg quantity for the limit leg
        :type limitIcebergQty: decimal
        :param stopIcebergQty: optional - Iceberg quantity for the stop leg
        :type stopIcebergQty: decimal
        :param recvWindow: optional - The value cannot be greater than 60000
        :type recvWindow: int

        :returns: Websocket message

        Response format:
        .. code-block:: python
            {
                "id": "56374a46-3261-486b-a211-99ed972eb648",
                "status": 200,
                "result":
                {
                    "orderListId": 2,
                    "contingencyType": "OCO",
                    "listStatusType": "EXEC_STARTED",
                    "listOrderStatus": "EXECUTING",
                    "listClientOrderId": "cKPMnDCbcLQILtDYM4f4fX",
                    "transactionTime": 1711062760648,
                    "symbol": "LTCBNB",
                    "orders":
                    [
                    {
                        "symbol": "LTCBNB",
                        "orderId": 2,
                        "clientOrderId": "0m6I4wfxvTUrOBSMUl0OPU"
                    },
                    {
                        "symbol": "LTCBNB",
                        "orderId": 3,
                        "clientOrderId": "Z2IMlR79XNY5LU0tOxrWyW"
                    }
                    ],
                    "orderReports":
                    [
                    {
                        "symbol": "LTCBNB",
                        "orderId": 2,
                        "orderListId": 2,
                        "clientOrderId": "0m6I4wfxvTUrOBSMUl0OPU",
                        "transactTime": 1711062760648,
                        "price": "1.50000000",
                        "origQty": "1.000000",
                        "executedQty": "0.000000",
                        "origQuoteOrderQty": "0.000000",
                        "cummulativeQuoteQty": "0.00000000",
                        "status": "NEW",
                        "timeInForce": "GTC",
                        "type": "STOP_LOSS_LIMIT",
                        "side": "BUY",
                        "stopPrice": "1.50000001",
                        "workingTime": -1,
                        "selfTradePreventionMode": "NONE"
                    },
                    {
                        "symbol": "LTCBNB",
                        "orderId": 3,
                        "orderListId": 2,
                        "clientOrderId": "Z2IMlR79XNY5LU0tOxrWyW",
                        "transactTime": 1711062760648,
                        "price": "1.49999999",
                        "origQty": "1.000000",
                        "executedQty": "0.000000",
                        "origQuoteOrderQty": "0.000000",
                        "cummulativeQuoteQty": "0.00000000",
                        "status": "NEW",
                        "timeInForce": "GTC",
                        "type": "LIMIT_MAKER",
                        "side": "BUY",
                        "workingTime": 1711062760648,
                        "selfTradePreventionMode": "NONE"
                    }
                    ]
                },
                "rateLimits":
                [
                    {
                    "rateLimitType": "ORDERS",
                    "interval": "SECOND",
                    "intervalNum": 10,
                    "limit": 50,
                    "count": 2
                    },
                    {
                    "rateLimitType": "ORDERS",
                    "interval": "DAY",
                    "intervalNum": 1,
                    "limit": 160000,
                    "count": 2
                    },
                    {
                    "rateLimitType": "REQUEST_WEIGHT",
                    "interval": "MINUTE",
                    "intervalNum": 1,
                    "limit": 6000,
                    "count": 1
                    }
                ]
            }

        Weight: 2
        """
        return self._ws_api_request_sync("orderList.place.oco", True, params)


    def ws_create_oto_order(self, **params):
        """Create a new OTO (One-Triggers-Other) order list.
        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#place-new-order-list---oto-trade

        An OTO order list consists of two orders:
        1. Primary order that must be filled first
        2. Secondary order that is placed only after the primary order is filled

        :param symbol: required - Trading symbol
        :type symbol: str
        :param orders: required - Array of order objects containing:
            [
                {  # Primary order
                    "type": required - Order type (e.g. LIMIT, MARKET),
                    "side": required - BUY or SELL,
                    "price": required for LIMIT orders,
                    "quantity": required - Order quantity,
                    "timeInForce": required for LIMIT orders,
                    "icebergQty": optional,
                    "strategyId": optional,
                    "strategyType": optional,
                    "selfTradePreventionMode": optional
                },
                {  # Secondary order - same parameters as primary
                    ...
                }
            ]
        :type orders: list
        :param listClientOrderId: optional - Unique ID for the entire order list
        :type listClientOrderId: str
        :param limitClientOrderId: optional - Client order ID for the LIMIT leg
        :type limitClientOrderId: str
        :param limitStrategyId: optional - Strategy ID for the LIMIT leg
        :type limitStrategyId: int
        :param limitStrategyType: optional - Strategy type for the LIMIT leg
        :type limitStrategyType: int
        :param stopClientOrderId: optional - Client order ID for the STOP_LOSS/STOP_LOSS_LIMIT leg
        :type stopClientOrderId: str
        :param stopStrategyId: optional - Strategy ID for the STOP_LOSS/STOP_LOSS_LIMIT leg
        :type stopStrategyId: int
        :param stopStrategyType: optional - Strategy type for the STOP_LOSS/STOP_LOSS_LIMIT leg
        :type stopStrategyType: int
        :param newOrderRespType: optional - Set the response JSON
        :type newOrderRespType: str

        Response example:
        .. code-block:: python
            {
                "id": "c5899911-d3f4-47ae-8835-97da553d27d0",
                "status": 200,
                "result": {
                    "orderListId": 1,
                    "contingencyType": "OTO",
                    "listStatusType": "EXEC_STARTED",
                    "listOrderStatus": "EXECUTING",
                    "listClientOrderId": "C3wyRVh3aqKyI2RpBZYmFz",
                    "transactionTime": 1669632210676,
                    "symbol": "BTCUSDT",
                    "orders": [
                        {
                            "symbol": "BTCUSDT",
                            "orderId": 12569099453,
                            "clientOrderId": "bX5wROblo6YeDwa9iTLeyY"
                        },
                        {
                            "symbol": "BTCUSDT",
                            "orderId": 12569099454,
                            "clientOrderId": "Tnu2IP0J5Y4mxw3IxZYeFi"
                        }
                    ],
                    "orderReports": [
                        {
                            "symbol": "BTCUSDT",
                            "orderId": 12569099453,
                            "orderListId": 1,
                            "clientOrderId": "bX5wROblo6YeDwa9iTLeyY",
                            "transactTime": 1669632210676,
                            "price": "23416.10000000",
                            "origQty": "0.00847000",
                            "executedQty": "0.00847000",
                            "cummulativeQuoteQty": "198.33521500",
                            "status": "FILLED",
                            "timeInForce": "GTC",
                            "type": "LIMIT",
                            "side": "SELL",
                            "stopPrice": "0.00000000",
                            "workingTime": 1669632210676,
                            "selfTradePreventionMode": "NONE"
                        },
                        {
                            "symbol": "BTCUSDT",
                            "orderId": 12569099454,
                            "orderListId": 1,
                            "clientOrderId": "Tnu2IP0J5Y4mxw3IxZYeFi",
                            "transactTime": 1669632210676,
                            "price": "0.00000000",
                            "origQty": "0.00847000",
                            "executedQty": "0.00000000",
                            "cummulativeQuoteQty": "0.00000000",
                            "status": "NEW",
                            "timeInForce": "GTC",
                            "type": "MARKET",
                            "side": "BUY",
                            "stopPrice": "0.00000000",
                            "workingTime": -1,
                            "selfTradePreventionMode": "NONE"
                        }
                    ]
                },
                "rateLimits": [
                    {
                        "rateLimitType": "ORDERS",
                        "interval": "SECOND",
                        "intervalNum": 10,
                        "limit": 50,
                        "count": 1
                    },
                    {
                        "rateLimitType": "ORDERS",
                        "interval": "DAY",
                        "intervalNum": 1,
                        "limit": 160000,
                        "count": 1
                    },
                    {
                        "rateLimitType": "REQUEST_WEIGHT",
                        "interval": "MINUTE",
                        "intervalNum": 1,
                        "limit": 6000,
                        "count": 1
                    }
                ]
            }

        Weight: 1
        """
        return self._ws_api_request_sync("orderList.place.oto", True, params)


    def ws_create_otoco_order(self, **params):
        """

        Returns: Websocket message
        .. code-block:: python
            {
                "id": "1712544408508",
                "status": 200,
                "result": {
                    "orderListId": 629,
                    "contingencyType": "OTO",
                    "listStatusType": "EXEC_STARTED",
                    "listOrderStatus": "EXECUTING",
                    "listClientOrderId": "GaeJHjZPasPItFj4x7Mqm6",
                    "transactionTime": 1712544408537,
                    "symbol": "1712544378871",
                    "orders": [
                    {
                        "symbol": "1712544378871",
                        "orderId": 23,
                        "clientOrderId": "OVQOpKwfmPCfaBTD0n7e7H"
                    },
                    {
                        "symbol": "1712544378871",
                        "orderId": 24,
                        "clientOrderId": "YcCPKCDMQIjNvLtNswt82X"
                    },
                    {
                        "symbol": "1712544378871",
                        "orderId": 25,
                        "clientOrderId": "ilpIoShcFZ1ZGgSASKxMPt"
                    }
                    ],
                    "orderReports": [
                    {
                        "symbol": "LTCBNB",
                        "orderId": 23,
                        "orderListId": 629,
                        "clientOrderId": "OVQOpKwfmPCfaBTD0n7e7H",
                        "transactTime": 1712544408537,
                        "price": "1.500000",
                        "origQty": "1.000000",
                        "executedQty": "0.000000",
                        "origQuoteOrderQty": "0.000000",
                        "cummulativeQuoteQty": "0.000000",
                        "status": "NEW",
                        "timeInForce": "GTC",
                        "type": "LIMIT",
                        "side": "BUY",
                        "workingTime": 1712544408537,
                        "selfTradePreventionMode": "NONE"
                    },
                    {
                        "symbol": "LTCBNB",
                        "orderId": 24,
                        "orderListId": 629,
                        "clientOrderId": "YcCPKCDMQIjNvLtNswt82X",
                        "transactTime": 1712544408537,
                        "price": "0.000000",
                        "origQty": "5.000000",
                        "executedQty": "0.000000",
                        "origQuoteOrderQty": "0.000000",
                        "cummulativeQuoteQty": "0.000000",
                        "status": "PENDING_NEW",
                        "timeInForce": "GTC",
                        "type": "STOP_LOSS",
                        "side": "SELL",
                        "stopPrice": "0.500000",
                        "workingTime": -1,
                        "selfTradePreventionMode": "NONE"
                    },
                    {
                        "symbol": "LTCBNB",
                        "orderId": 25,
                        "orderListId": 629,
                        "clientOrderId": "ilpIoShcFZ1ZGgSASKxMPt",
                        "transactTime": 1712544408537,
                        "price": "5.000000",
                        "origQty": "5.000000",
                        "executedQty": "0.000000",
                        "origQuoteOrderQty": "0.000000",
                        "cummulativeQuoteQty": "0.000000",
                        "status": "PENDING_NEW",
                        "timeInForce": "GTC",
                        "type": "LIMIT_MAKER",
                        "side": "SELL",
                        "workingTime": -1,
                        "selfTradePreventionMode": "NONE"
                    }
                    ]
                },
                "rateLimits": [
                    {
                    "rateLimitType": "ORDERS",
                    "interval": "MINUTE",
                    "intervalNum": 1,
                    "limit": 10000000,
                    "count": 18
                    },
                    {
                    "rateLimitType": "REQUEST_WEIGHT",
                    "interval": "MINUTE",
                    "intervalNum": 1,
                    "limit": 1000,
                    "count": 65
                    }
                ]
        }

        Weight: 1
        """
        return self._ws_api_request_sync("orderList.place.otoco", True, params)


    def ws_get_oco_order(self, **params):
        """Query information about a specific OCO order list.

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#query-order-list-user_data

        :param orderListId: int - The identifier for the OCO order list (optional)
        :param origClientOrderId: str - The client-specified OCO order list ID (optional)

        :returns: API response containing OCO order list information including:
        .. code-block:: python
            {
                "id": "b53fd5ff-82c7-4a04-bd64-5f9dc42c2100",
                "status": 200,
                "result": {
                    "orderListId": 1274512,
                    "contingencyType": "OCO",
                    "listStatusType": "EXEC_STARTED",
                    "listOrderStatus": "EXECUTING",
                    "listClientOrderId": "08985fedd9ea2cf6b28996",
                    "transactionTime": 1660801713793,
                    "symbol": "BTCUSDT",
                    "orders": [
                    {
                        "symbol": "BTCUSDT",
                        "orderId": 12569138901,
                        "clientOrderId": "BqtFCj5odMoWtSqGk2X9tU"
                    },
                    {
                        "symbol": "BTCUSDT",
                        "orderId": 12569138902,
                        "clientOrderId": "jLnZpj5enfMXTuhKB1d0us"
                    }
                    ]
                },
                "rateLimits": [
                    {
                    "rateLimitType": "REQUEST_WEIGHT",
                    "interval": "MINUTE",
                    "intervalNum": 1,
                    "limit": 6000,
                    "count": 4
                    }
                ]
            }

        Notes:
            - Either orderListId or origClientOrderId must be provided
            - Weight: 4
            - Data Source: Database

        """
        return self._ws_api_request_sync("orderList.status", True, params)


    def ws_cancel_oco_order(self, **params):
        """Cancel an OCO (One-Cancels-the-Other) order list.

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#cancel-order-list-trade

        :param symbol: required - Trading symbol
        :type symbol: str
        :param orderListId: optional - The ID of the OCO order list to cancel
        :type orderListId: int
        :param listClientOrderId: optional - The client-specified ID of the OCO order list
        :type listClientOrderId: str
        :param newClientOrderId: optional - Client ID to identify the cancel request
        :type newClientOrderId: str
        :param apiKey: required - Your API key
        :type apiKey: str
        :param recvWindow: optional - Number of milliseconds the request is valid for
        :type recvWindow: int
        :param signature: required - HMAC SHA256 signature
        :type signature: str
        :param timestamp: required - Current timestamp in milliseconds
        :type timestamp: int

        **Notes**:
            - Either orderListId or listClientOrderId must be provided
            - newClientOrderId will be auto-generated if not provided

        Response example:
        .. code-block:: python
            {
                "id": "c5899911-d3f4-47ae-8835-97da553d27d0",
                "status": 200,
                "result": {
                    "orderListId": 1274512,
                    "contingencyType": "OCO",
                    "listStatusType": "ALL_DONE",
                    "listOrderStatus": "ALL_DONE",
                    "listClientOrderId": "6023531d7edaad348f5aff",
                    "transactionTime": 1660801720215,
                    "symbol": "BTCUSDT",
                    "orders": [
                        {
                            "symbol": "BTCUSDT",
                            "orderId": 12569138901,
                            "clientOrderId": "BqtFCj5odMoWtSqGk2X9tU"
                        },
                        {
                            "symbol": "BTCUSDT",
                            "orderId": 12569138902,
                            "clientOrderId": "jLnZpj5enfMXTuhKB1d0us"
                        }
                    ],
                    "orderReports": [
                        {
                            "symbol": "BTCUSDT",
                            "orderId": 12569138901,
                            "orderListId": 1274512,
                            "clientOrderId": "BqtFCj5odMoWtSqGk2X9tU",
                            "transactTime": 1660801720215,
                            "price": "23416.10000000",
                            "origQty": "0.00847000",
                            "executedQty": "0.00000000",
                            "cummulativeQuoteQty": "0.00000000",
                            "status": "CANCELED",
                            "timeInForce": "GTC",
                            "type": "STOP_LOSS_LIMIT",
                            "side": "SELL",
                            "stopPrice": "23416.10000000",
                            "selfTradePreventionMode": "NONE"
                        },
                        {
                            "symbol": "BTCUSDT",
                            "orderId": 12569138902,
                            "orderListId": 1274512,
                            "clientOrderId": "jLnZpj5enfMXTuhKB1d0us",
                            "transactTime": 1660801720215,
                            "price": "23416.10000000",
                            "origQty": "0.00847000",
                            "executedQty": "0.00000000",
                            "cummulativeQuoteQty": "0.00000000",
                            "status": "CANCELED",
                            "timeInForce": "GTC",
                            "type": "LIMIT_MAKER",
                            "side": "SELL",
                            "selfTradePreventionMode": "NONE"
                        }
                    ]
                },
                "rateLimits": [
                    {
                        "rateLimitType": "REQUEST_WEIGHT",
                        "interval": "MINUTE",
                        "intervalNum": 1,
                        "limit": 6000,
                        "count": 1
                    }
                ]
            }

        """
        return self._ws_api_request_sync("orderList.cancel", True, params)


    def ws_get_oco_open_orders(self, **params):
        """Query current open OCO (One-Cancels-the-Other) order lists.

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#current-open-order-lists-user_data

        :param recvWindow: optional - Number of milliseconds after timestamp the request is valid for. Default 5000, max 60000
        :type recvWindow: int
        :param apiKey: required - Your API key
        :type apiKey: str
        :param signature: required - HMAC SHA256 signature
        :type signature: str
        :param timestamp: required - Current timestamp in milliseconds
        :type timestamp: int

        :returns: API response in JSON format with open OCO orders

            {
                "id": "c5899911-d3f5-47b3-9b67-4c1342f2a7e1",
                "status": 200,
                "result": [
                    {
                        "orderListId": 1274512,
                        "contingencyType": "OCO",
                        "listStatusType": "EXEC_STARTED",
                        "listOrderStatus": "EXECUTING",
                        "listClientOrderId": "08985fedd9ea2cf6b28996",
                        "transactionTime": 1660801713793,
                        "symbol": "BTCUSDT",
                        "orders": [
                            {
                                "symbol": "BTCUSDT",
                                "orderId": 12569138901,
                                "clientOrderId": "BqtFCj5odMoWtSqGk2X9tU"
                            },
                            {
                                "symbol": "BTCUSDT",
                                "orderId": 12569138902,
                                "clientOrderId": "jLnZpj5enfMXTuhKB1d0us"
                            }
                        ]
                    }
                ],
                "rateLimits": [
                    {
                        "rateLimitType": "REQUEST_WEIGHT",
                        "interval": "MINUTE",
                        "intervalNum": 1,
                        "limit": 6000,
                        "count": 10
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        Weight: 10
        Data Source: Memory
        """
        return self._ws_api_request_sync("openOrderLists.status", True, params)


    def ws_create_sor_order(self, **params):
        """Place a new order using Smart Order Routing (SOR).

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#place-new-order-using-sor-trade

        :param symbol: required - Trading symbol, e.g. BTCUSDT
        :type symbol: str
        :param side: required - Order side: BUY or SELL
        :type side: str
        :param type: required - Order type: LIMIT or MARKET
        :type type: str
        :param quantity: required - Order quantity
        :type quantity: float
        :param timeInForce: required for LIMIT orders - Time in force: GTC, IOC, FOK
        :type timeInForce: str
        :param price: required for LIMIT orders - Order price
        :type price: float
        :param newClientOrderId: optional - Unique order ID. Automatically generated if not sent
        :type newClientOrderId: str
        :param newOrderRespType: optional - Response format: ACK, RESULT, FULL. MARKET and LIMIT orders use FULL by default
        :type newOrderRespType: str
        :param strategyId: optional - Arbitrary numeric value identifying the order within an order strategy
        :type strategyId: int
        :param strategyType: optional - Arbitrary numeric value identifying the order strategy. Values < 1000000 are reserved
        :type strategyType: int
        :param selfTradePreventionMode: optional - Supported values depend on exchange configuration: EXPIRE_TAKER, EXPIRE_MAKER, EXPIRE_BOTH, NONE
        :type selfTradePreventionMode: str
        :param recvWindow: optional - Number of milliseconds after timestamp the request is valid for. Default 5000, max 60000
        :type recvWindow: int

        :returns: Websocket message

        .. code-block:: python
            {
                "id": "3a4437e2-41a3-4c19-897c-9cadc5dce8b6",
                "status": 200,
                "result": [
                    {
                        "symbol": "BTCUSDT",
                        "orderId": 2,
                        "orderListId": -1,
                        "clientOrderId": "sBI1KM6nNtOfj5tccZSKly",
                        "transactTime": 1689149087774,
                        "price": "31000.00000000",
                        "origQty": "0.50000000",
                        "executedQty": "0.50000000",
                        "cummulativeQuoteQty": "14000.00000000",
                        "status": "FILLED",
                        "timeInForce": "GTC",
                        "type": "LIMIT",
                        "side": "BUY",
                        "workingTime": 1689149087774,
                        "fills": [
                            {
                                "matchType": "ONE_PARTY_TRADE_REPORT",
                                "price": "28000.00000000",
                                "qty": "0.50000000",
                                "commission": "0.00000000",
                                "commissionAsset": "BTC",
                                "tradeId": -1,
                                "allocId": 0
                            }
                        ],
                        "workingFloor": "SOR",
                        "selfTradePreventionMode": "NONE",
                        "usedSor": true
                    }
                ],
                "rateLimits": [
                    {
                        "rateLimitType": "REQUEST_WEIGHT",
                        "interval": "MINUTE",
                        "intervalNum": 1,
                        "limit": 6000,
                        "count": 1
                    }
                ]
            }

        Notes:
            - SOR only supports LIMIT and MARKET orders
            - quoteOrderQty is not supported
            - Weight: 1
            - Data Source: Matching Engine
        """
        return self._ws_api_request_sync("sor.order.place", True, params)


    def ws_create_test_sor_order(self, **params):
        """Test new order creation using Smart Order Routing (SOR).
        Creates and validates a new order but does not send it into the matching engine.

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#test-new-order-using-sor-trade

        :param symbol: required - Trading symbol, e.g. BTCUSDT
        :type symbol: str
        :param side: required - Order side: BUY or SELL
        :type side: str
        :param type: required - Order type: LIMIT or MARKET
        :type type: str
        :param quantity: required - Order quantity
        :type quantity: float
        :param timeInForce: required for LIMIT orders - Time in force: GTC, IOC, FOK
        :type timeInForce: str
        :param price: required for LIMIT orders - Order price
        :type price: float
        :param newClientOrderId: optional - Unique order ID. Generated automatically if not sent
        :type newClientOrderId: str
        :param strategyId: optional - Arbitrary numeric value identifying the order within an order strategy
        :type strategyId: int
        :param strategyType: optional - Arbitrary numeric value identifying the order strategy. Values < 1000000 are reserved
        :type strategyType: int
        :param selfTradePreventionMode: optional - EXPIRE_TAKER, EXPIRE_MAKER, EXPIRE_BOTH, NONE
        :type selfTradePreventionMode: str
        :param computeCommissionRates: optional - Calculate commission rates. Default: False
        :type computeCommissionRates: bool

        :returns: Websocket message

        Without computeCommissionRates:

        .. code-block:: python

            {
                "id": "3a4437e2-41a3-4c19-897c-9cadc5dce8b6",
                "status": 200,
                "result": {},
                "rateLimits": [
                    {
                        "rateLimitType": "REQUEST_WEIGHT",
                        "interval": "MINUTE",
                        "intervalNum": 1,
                        "limit": 6000,
                        "count": 1
                    }
                ]
            }

        With computeCommissionRates:

        .. code-block:: python

            {
                "id": "3a4437e2-41a3-4c19-897c-9cadc5dce8b6",
                "status": 200,
                "result": {
                    "standardCommissionForOrder": {
                        "maker": "0.00000112",
                        "taker": "0.00000114"
                    },
                    "taxCommissionForOrder": {
                        "maker": "0.00000112",
                        "taker": "0.00000114"
                    },
                    "discount": {
                        "enabledForAccount": true,
                        "enabledForSymbol": true,
                        "discountAsset": "BNB",
                        "discount": "0.25"
                    }
                },
                "rateLimits": [...]
            }

        Notes:
            - SOR only supports LIMIT and MARKET orders
            - quoteOrderQty is not supported
            - Weight: 1 (without computeCommissionRates), 20 (with computeCommissionRates)
            - Data Source: Memory
        """
        return self._ws_api_request_sync("sor.order.test", True, params)


    def ws_get_account(self, **params):
        """Get current account information.

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#account-information-user_data

        :param omitZeroBalances: optional - When set to true, emits only the non-zero balances of an account. Default: false
        :type omitZeroBalances: bool
        :param recvWindow: optional - The value cannot be greater than 60000
        :type recvWindow: int

        :returns: Websocket message

        .. code-block:: python

            {
                "makerCommission": 15,
                "takerCommission": 15,
                "buyerCommission": 0,
                "sellerCommission": 0,
                "canTrade": true,
                "canWithdraw": true,
                "canDeposit": true,
                "commissionRates": {
                    "maker": "0.00150000",
                    "taker": "0.00150000",
                    "buyer": "0.00000000",
                    "seller": "0.00000000"
                },
                "brokered": false,
                "requireSelfTradePrevention": false,
                "preventSor": false,
                "updateTime": 1660801833000,
                "accountType": "SPOT",
                "balances": [
                    {
                        "asset": "BNB",
                        "free": "0.00000000",
                        "locked": "0.00000000"
                    },
                    {
                        "asset": "BTC",
                        "free": "1.34471120",
                        "locked": "0.08600000"
                    }
                ],
                "permissions": [
                    "SPOT"
                ],
                "uid": 354937868
            }

        Notes:
            - Weight: 20
            - Data Source: Memory => Database
        """
        return self._ws_api_request_sync("account.status", True, params)


    def ws_get_account_rate_limits_orders(self, **params):
        """Query your current unfilled order count for all intervals.

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#account-unfilled-order-count-user_data

        :param recvWindow: optional - The value cannot be greater than 60000
        :type recvWindow: int

        :returns: Websocket response

        .. code-block:: python

            {
                "result": [
                    {
                        "rateLimitType": "ORDERS",
                        "interval": "SECOND",
                        "intervalNum": 10,
                        "limit": 50,
                        "count": 0
                    },
                    {
                        "rateLimitType": "ORDERS",
                        "interval": "DAY",
                        "intervalNum": 1,
                        "limit": 160000,
                        "count": 0
                    }
                ],
                "id": "d3783d8d-f8d1-4d2c-b8a0-b7596af5a664"
            }

        :raises: BinanceRequestException, BinanceAPIException

        Notes:
            - Weight: 40
            - Data Source: Memory
        """
        return self._ws_api_request_sync("account.rateLimits.orders", True, params)


    def ws_get_all_orders(self, **params):
        """Query information about all your orders – active, canceled, filled – filtered by time range.

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#account-order-history-user_data

        :param symbol: STRING - Required
        :type symbol: str
        :param orderId: optional - Order ID to begin at
        :type orderId: int
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param limit: optional - Default 500; max 1000
        :type limit: int
        :param recvWindow: optional - The value cannot be greater than 60000
        :type recvWindow: int

        :returns: Websocket response

        .. code-block:: python

            {
                "id": "734235c2-13d2-4574-be68-723e818c08f3",
                "status": 200,
                "result": [
                    {
                        "symbol": "BTCUSDT",
                        "orderId": 12569099453,
                        "orderListId": -1,
                        "clientOrderId": "4d96324ff9d44481926157",
                        "price": "23416.10000000",
                        "origQty": "0.00847000",
                        "executedQty": "0.00847000",
                        "cummulativeQuoteQty": "198.33521500",
                        "status": "FILLED",
                        "timeInForce": "GTC",
                        "type": "LIMIT",
                        "side": "SELL",
                        "stopPrice": "0.00000000",
                        "icebergQty": "0.00000000",
                        "time": 1660801715639,
                        "updateTime": 1660801717945,
                        "isWorking": true,
                        "workingTime": 1660801715639,
                        "origQuoteOrderQty": "0.00000000",
                        "selfTradePreventionMode": "NONE",
                        "preventedMatchId": 0,            // Only appears if order expired due to STP
                        "preventedQuantity": "1.200000"   // Only appears if order expired due to STP
                    }
                ]
            }

        Notes:
            - Weight: 20
            - Data Source: Database
            - If startTime and/or endTime are specified, orderId is ignored
            - Orders are filtered by time of the last execution status update
            - If orderId is specified, return orders with order ID >= orderId
            - If no condition is specified, the most recent orders are returned
            - For some historical orders the cummulativeQuoteQty response field may be negative
            - The time between startTime and endTime can't be longer than 24 hours
        """
        return self._ws_api_request_sync("allOrders", True, params)


    def ws_get_my_trades(self, **params):
        """Query information about your trades, filtered by time range.

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#account-trade-history-user_data

        :param symbol: STRING - Required
        :type symbol: str
        :param orderId: optional - Get trades for a specific order
        :type orderId: int
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param fromId: optional - Trade ID to fetch from
        :type fromId: int
        :param limit: optional - Default 500; max 1000
        :type limit: int
        :param recvWindow: optional - The value cannot be greater than 60000
        :type recvWindow: int

        :returns: Websocket response

            .. code-block:: python

                [
                    {
                        "symbol": "BTCUSDT",
                        "id": 1650422481,
                        "orderId": 12569099453,
                        "orderListId": -1,
                        "price": "23416.10000000",
                        "qty": "0.00635000",
                        "quoteQty": "148.69223500",
                        "commission": "0.00000000",
                        "commissionAsset": "BNB",
                        "time": 1660801715793,
                        "isBuyer": false,
                        "isMaker": true,
                        "isBestMatch": true
                    }
                ]

        Notes:
            - Weight: 20
            - Data Source: Memory => Database
            - If fromId is specified, return trades with trade ID >= fromId
            - If startTime and/or endTime are specified, trades are filtered by execution time (time)
            - fromId cannot be used together with startTime and endTime
            - If orderId is specified, only trades related to that order are returned
            - startTime and endTime cannot be used together with orderId
            - If no condition is specified, the most recent trades are returned
            - The time between startTime and endTime can't be longer than 24 hours
        """
        return self._ws_api_request_sync("myTrades", True, params)


    def ws_get_prevented_matches(self, **params):
        """Displays the list of orders that were expired due to STP (Self-Trade Prevention).

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#account-prevented-matches-user_data

        :param symbol: STRING - Required
        :type symbol: str
        :param preventedMatchId: optional - Get specific prevented match by ID
        :type preventedMatchId: int
        :param orderId: optional - Get prevented matches for specific order
        :type orderId: int
        :param fromPreventedMatchId: optional - Get prevented matches from this ID
        :type fromPreventedMatchId: int
        :param limit: optional - Default 500; max 1000
        :type limit: int
        :param recvWindow: optional - The value cannot be greater than 60000
        :type recvWindow: int

        :returns: Websocket response

        .. code-block:: python
            {
                "symbol": "BTCUSDT",            # Trading pair
                "preventedMatchId": 1,          # Unique ID for prevented match
                "takerOrderId": 5,              # Order ID of the taker order
                "makerSymbol": "BTCUSDT",       # Symbol of maker order
                "makerOrderId": 3,              # Order ID of maker order
                "tradeGroupId": 1,              # Trade group ID
                "selfTradePreventionMode": "EXPIRE_MAKER", # STP mode used
                "price": "1.100000",            # Price level where match was prevented
                "makerPreventedQuantity": "1.300000", # Quantity that was prevented
                "transactTime": 1669101687094   # Time of prevention
            }

        Supported parameter combinations:
            - symbol + preventedMatchId
            - symbol + orderId
            - symbol + orderId + fromPreventedMatchId (limit defaults to 500)
            - symbol + orderId + fromPreventedMatchId + limit

        Weight:
            - 2 if symbol is invalid
            - 2 when querying by preventedMatchId
            - 20 when querying by orderId

        Data Source: Database
        """
        return self._ws_api_request_sync("myPreventedMatches", True, params)


    def ws_get_allocations(self, **params):
        """Get information about orders that were expired due to STP (Self-Trade Prevention).

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#account-prevented-matches-user_data

        :param symbol: STRING - Required - Trading symbol
        :type symbol: str
        :param preventedMatchId: LONG - Optional - Get specific prevented match by ID
        :type preventedMatchId: int
        :param orderId: LONG - Optional - Get prevented matches for specific order
        :type orderId: int
        :param fromPreventedMatchId: LONG - Optional - Get prevented matches from this ID
        :type fromPreventedMatchId: int
        :param limit: INT - Optional - Default 500; max 1000
        :type limit: int
        :param recvWindow: LONG - Optional - The value cannot be greater than 60000
        :type recvWindow: int
        :param timestamp: LONG - Required
        :type timestamp: int

        :returns: API response

        .. code-block:: python
            {
                "symbol": "BTCUSDT",
                "preventedMatchId": 1,
                "takerOrderId": 5,
                "makerSymbol": "BTCUSDT",
                "makerOrderId": 3,
                "tradeGroupId": 1,
                "selfTradePreventionMode": "EXPIRE_MAKER",
                "price": "1.100000",
                "makerPreventedQuantity": "1.300000",
                "transactTime": 1669101687094
            }

        Supported parameter combinations:
            - symbol + preventedMatchId
            - symbol + orderId
            - symbol + orderId + fromPreventedMatchId (limit defaults to 500)
            - symbol + orderId + fromPreventedMatchId + limit

        Weight:
            - 2 if symbol is invalid
            - 2 when querying by preventedMatchId
            - 20 when querying by orderId

        Data Source: Database
        """
        return self._ws_api_request_sync("myAllocations", True, params)


    def ws_get_commission_rates(self, **params):
        """Get current account commission rates for a symbol.

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#account-commission-rates-user_data

        :param symbol: STRING - Required - Trading symbol
        :type symbol: str
        :param recvWindow: LONG - Optional - The value cannot be greater than 60000
        :type recvWindow: int

        :returns: API response dict with commission rates:

            {
                "symbol": "BTCUSDT",
                "standardCommission": {           # Standard commission rates on trades
                    "maker": "0.00000010",
                    "taker": "0.00000020",
                    "buyer": "0.00000030",
                    "seller": "0.00000040"
                },
                "taxCommission": {               # Tax commission rates on trades
                    "maker": "0.00000112",
                    "taker": "0.00000114",
                    "buyer": "0.00000118",
                    "seller": "0.00000116"
                },
                "discount": {                    # Discount on standard commissions when paying in BNB
                    "enabledForAccount": true,
                    "enabledForSymbol": true,
                    "discountAsset": "BNB",
                    "discount": "0.75000000"     # Standard commission reduction rate when paying in BNB
                }
            }

        :raises: BinanceRequestException, BinanceAPIException

        Weight: 20

        Data Source: Database
        """
        return self._ws_api_request_sync("account.commission", True, params)


    def ws_get_order_book(self, **params):
        """Get current order book for a symbol.

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#order-book

        Note that this request returns limited market depth. If you need to continuously monitor
        order book updates, consider using WebSocket Streams:
        - <symbol>@depth<levels>
        - <symbol>@depth

        You can use `depth` request together with `<symbol>@depth` streams to maintain a local order book.

        :param symbol: STRING - Required - Trading symbol
        :type symbol: str
        :param limit: INT - Optional - Default 100; max 5000
        :type limit: int

        :returns: Websocket message

            {
                "lastUpdateId": 2731179239,
                "bids": [                // Bid levels sorted from highest to lowest price
                    [
                        "0.01379900",   // Price level
                        "3.43200000"    // Quantity
                    ],
                    ...
                ],
                "asks": [                // Ask levels sorted from lowest to highest price
                    [
                        "0.01380000",   // Price level
                        "5.91700000"    // Quantity
                    ],
                    ...
                ]
            }

        Weight: Adjusted based on limit:
            - 1-100: 5
            - 101-500: 25
            - 501-1000: 50
            - 1001-5000: 250

        Data Source: Memory
        """
        return self._ws_api_request_sync("depth", False, params)


    def ws_get_recent_trades(self, **params):
        """Get recent trades for a symbol.

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#recent-trades

        If you need access to real-time trading activity, please consider using WebSocket Streams:
        - <symbol>@trade

        :param symbol: STRING - Required - Trading symbol
        :type symbol: str
        :param limit: INT - Optional - Default 500; max 1000
        :type limit: int

        :returns: API response

        .. code-block:: python
            {
                "id": "409a20bd-253d-41db-a6dd-687862a5882f",
                "status": 200,
                "result": [
                    {
                        "id": 194686783,              # Trade ID
                        "price": "0.01361000",        # Price
                        "qty": "0.01400000",          # Quantity
                        "quoteQty": "0.00019054",     # Quote quantity
                        "time": 1660009530807,        # Trade time
                        "isBuyerMaker": true,         # Was the buyer the maker?
                        "isBestMatch": true           # Was this the best price match?
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        Weight: 25
        Data Source: Memory
        """
        return self._ws_api_request_sync("trades.recent", False, params)


    def ws_get_historical_trades(self, **params):
        """Get historical trades.

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#historical-trades

        :param symbol: STRING - Required - Trading symbol
        :type symbol: str
        :param fromId: INT - Optional - Trade ID to begin at
        :type fromId: int
        :param limit: INT - Optional - Default 500; max 1000
        :type limit: int

        :returns: Websocket message

        .. code-block:: python

            {
                "id": "cffc9c7d-4efc-4ce0-b587-6b87448f052a",
                "result": [
                    {
                        "id": 0,                      # Trade ID
                        "price": "0.00005000",        # Price
                        "qty": "40.00000000",         # Quantity
                        "quoteQty": "0.00200000",     # Quote quantity
                        "time": 1500004800376,        # Trade time
                        "isBuyerMaker": true,         # Was the buyer the maker?
                        "isBestMatch": true           # Was this the best price match?
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        Notes:
            - If fromId is not specified, the most recent trades are returned

        Weight: 25
        Data Source: Database
        """
        return self._ws_api_request_sync("trades.historical", False, params)


    def ws_get_aggregate_trades(self, **params):
        """Get aggregate trades.

        An aggregate trade represents one or more individual trades that fill at the same time,
        from the same taker order, with the same price.

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#aggregate-trades

        :param symbol: STRING - Required - Trading symbol
        :type symbol: str
        :param fromId: INT - Optional - Aggregate trade ID to begin at
        :type fromId: int
        :param startTime: INT - Optional - Start time in milliseconds
        :type startTime: int
        :param endTime: INT - Optional - End time in milliseconds
        :type endTime: int
        :param limit: INT - Optional - Default 500; max 1000
        :type limit: int

        :returns: API response

        .. code-block:: python

            {
                "id": "...",
                "status": 200,
                "result": [
                    {
                        "a": 50000000,        # Aggregate trade ID
                        "p": "0.00274100",    # Price
                        "q": "57.19000000",   # Quantity
                        "f": 59120167,        # First trade ID
                        "l": 59120170,        # Last trade ID
                        "T": 1565877971222,   # Timestamp
                        "m": true,            # Was the buyer the maker?
                        "M": true             # Was the trade the best price match?
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        Notes:
            - If fromId is specified, return aggtrades with aggregate trade ID >= fromId.
            Use fromId and limit to page through all aggtrades.
            - If startTime and/or endTime are specified, aggtrades are filtered by execution time (T).
            fromId cannot be used together with startTime and endTime.
            - If no condition is specified, the most recent aggregate trades are returned.
            - For real-time updates, consider using WebSocket Streams: <symbol>@aggTrade
            - For historical data, consider using data.binance.vision

        Weight: 2
        Data Source: Database
        """
        return self._ws_api_request_sync("trades.aggregate", False, params)


    def ws_get_klines(self, **params):
        """Get klines (candlestick bars).

        Klines are uniquely identified by their open & close time.

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#klines

        :param symbol: STRING - Required - Trading symbol
        :type symbol: str
        :param interval: ENUM - Required - Kline interval
        :type interval: str
        :param startTime: INT - Optional - Start time in milliseconds
        :type startTime: int
        :param endTime: INT - Optional - End time in milliseconds
        :type endTime: int
        :param timeZone: STRING - Optional - Default: 0 (UTC)
        :type timeZone: str
        :param limit: INT - Optional - Default 500; max 1000
        :type limit: int

        Supported kline intervals:
            - seconds: 1s
            - minutes: 1m, 3m, 5m, 15m, 30m
            - hours: 1h, 2h, 4h, 6h, 8h, 12h
            - days: 1d, 3d
            - weeks: 1w
            - months: 1M

        Notes:
            - If startTime/endTime not specified, returns most recent klines
            - Supported timeZone values:
                - Hours and minutes (e.g. "-1:00", "05:45")
                - Only hours (e.g. "0", "8", "4")
                - Accepted range is strictly [-12:00 to +14:00] inclusive
            - If timeZone provided, kline intervals interpreted in that timezone instead of UTC
            - startTime and endTime always interpreted in UTC, regardless of timeZone
            - For real-time updates, consider using WebSocket Streams: <symbol>@kline_<interval>
            - For historical data, consider using data.binance.vision

        Weight: 2
        Data Source: Database

        :returns: API response

        .. code-block:: python

            {
                "id": "1dbbeb56-8eea-466a-8f6e-86bdcfa2fc0b",
                "status": 200,
                "result": [
                    [
                        1655971200000,      # Kline open time
                        "0.01086000",       # Open price
                        "0.01086600",       # High price
                        "0.01083600",       # Low price
                        "0.01083800",       # Close price
                        "2290.53800000",    # Volume
                        1655974799999,      # Kline close time
                        "24.85074442",      # Quote asset volume
                        2283,               # Number of trades
                        "1171.64000000",    # Taker buy base asset volume
                        "12.71225884",      # Taker buy quote asset volume
                        "0"                 # Unused field, ignore
                    ]
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException
        """
        return self._ws_api_request_sync("klines", False, params)


    def ws_get_uiKlines(self, **params):
        """Get klines (candlestick bars) optimized for presentation.

        This request is similar to klines, having the same parameters and response.
        uiKlines return modified kline data, optimized for presentation of candlestick charts.

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#ui-klines

        :param symbol: STRING - Required - Trading symbol
        :type symbol: str
        :param interval: ENUM - Required - Kline interval
        :type interval: str
        :param startTime: INT - Optional - Start time in milliseconds
        :type startTime: int
        :param endTime: INT - Optional - End time in milliseconds
        :type endTime: int
        :param timeZone: STRING - Optional - Default: 0 (UTC)
        :type timeZone: str
        :param limit: INT - Optional - Default 500; max 1000
        :type limit: int

        Supported kline intervals:
            - seconds: 1s
            - minutes: 1m, 3m, 5m, 15m, 30m
            - hours: 1h, 2h, 4h, 6h, 8h, 12h
            - days: 1d, 3d
            - weeks: 1w
            - months: 1M

        Notes:
            - If startTime/endTime not specified, returns most recent klines
            - Supported timeZone values:
                - Hours and minutes (e.g. "-1:00", "05:45")
                - Only hours (e.g. "0", "8", "4")
                - Accepted range is strictly [-12:00 to +14:00] inclusive
            - If timeZone provided, kline intervals are interpreted in that timezone instead of UTC
            - startTime and endTime are always interpreted in UTC, regardless of timeZone

        :returns: API response

        .. code-block:: python

            {
                "id": "b137468a-fb20-4c06-bd6b-625148eec958",
                "result": [
                    [
                        1655971200000,      # Kline open time
                        "0.01086000",       # Open price
                        "0.01086600",       # High price
                        "0.01083600",       # Low price
                        "0.01083800",       # Close price
                        "2290.53800000",    # Volume
                        1655974799999,      # Kline close time
                        "24.85074442",      # Quote asset volume
                        2283,               # Number of trades
                        "1171.64000000",    # Taker buy base asset volume
                        "12.71225884",      # Taker buy quote asset volume
                        "0"                 # Unused field, ignore
                    ]
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException
        """
        return self._ws_api_request_sync("uiKlines", False, params)


    def ws_get_avg_price(self, **params):
        """Get current average price for a symbol.

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#current-average-price

        :param symbol: STRING - Required - Trading symbol
        :type symbol: str

        :returns: Websocket message

        .. code-block:: python
            {
                "mins": 5,                    # Average price interval (in minutes)
                "price": "9.35751834",        # Average price
                "closeTime": 1694061154503    # Last trade time
            }

        Weight: 2
        """
        return self._ws_api_request_sync("avgPrice", False, params)


    def ws_get_ticker(self, **params):
        """Get 24-hour rolling window price change statistics.

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#24hr-ticker-price-change-statistics

        :param symbol: STRING - Optional - Query ticker for a single symbol
        :type symbol: str
        :param symbols: ARRAY of STRING - Optional - Query ticker for multiple symbols
        :type symbols: list
        :param type: ENUM - Optional - Ticker type: FULL (default) or MINI
        :type type: str

        Note:
            - symbol and symbols cannot be used together
            - If no symbol is specified, returns information about all symbols currently trading on the exchange

        Weight:
            Adjusted based on the number of requested symbols:
            - 1-20 symbols: 2
            - 21-100 symbols: 40
            - 101 or more symbols: 80
            - all symbols: 80

        :returns: Websocket message

        For a single symbol with type=FULL:
        .. code-block:: python
            {
                "symbol": "BNBBTC",
                "priceChange": "0.00013900",         # Absolute price change
                "priceChangePercent": "1.020",       # Relative price change in percent
                "weightedAvgPrice": "0.01382453",    # Quote volume divided by volume
                "prevClosePrice": "0.01362800",      # Previous day's close price
                "lastPrice": "0.01376700",           # Latest price
                "lastQty": "1.78800000",            # Latest quantity
                "bidPrice": "0.01376700",           # Best bid price
                "bidQty": "4.64600000",            # Best bid quantity
                "askPrice": "0.01376800",           # Best ask price
                "askQty": "14.31400000",           # Best ask quantity
                "openPrice": "0.01362800",          # Open price 24 hours ago
                "highPrice": "0.01414900",          # Highest price in the last 24 hours
                "lowPrice": "0.01346600",           # Lowest price in the last 24 hours
                "volume": "69412.40500000",         # Trading volume in base asset
                "quoteVolume": "959.59411487",      # Trading volume in quote asset
                "openTime": 1660014164909,          # Open time for 24hr rolling window
                "closeTime": 1660100564909,         # Close time for 24hr rolling window
                "firstId": 194696115,               # First trade ID
                "lastId": 194968287,                # Last trade ID
                "count": 272173                     # Number of trades
            }

        For a single symbol with type=MINI:
        .. code-block:: python
            {
                "symbol": "BNBBTC",
                "openPrice": "0.01362800",
                "highPrice": "0.01414900",
                "lowPrice": "0.01346600",
                "lastPrice": "0.01376700",
                "volume": "69412.40500000",
                "quoteVolume": "959.59411487",
                "openTime": 1660014164909,
                "closeTime": 1660100564909,
                "firstId": 194696115,
                "lastId": 194968287,
                "count": 272173
            }

        """
        return self._ws_api_request_sync("ticker.24hr", False, params)


    def ws_get_trading_day_ticker(self, **params):
        """Price change statistics for a trading day.

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#trading-day-ticker

        :param symbol: STRING - Optional - Query ticker of a single symbol
        :type symbol: str
        :param symbols: ARRAY of STRING - Optional - Query ticker for multiple symbols
        :type symbols: list
        :param timeZone: STRING - Optional - Default: 0 (UTC)
            Supported values:
            - Hours and minutes (e.g. "-1:00", "05:45")
            - Only hours (e.g. "0", "8", "4")
            - Accepted range is strictly [-12:00 to +14:00] inclusive
        :type timeZone: str
        :param type: ENUM - Optional - FULL (default) or MINI
        :type type: str

        :returns: Websocket message

        Response FULL type example:
        {
            "symbol": "BTCUSDT",
            "priceChange": "-83.13000000",           # Absolute price change
            "priceChangePercent": "-0.317",          # Relative price change in percent
            "weightedAvgPrice": "26234.58803036",    # quoteVolume / volume
            "openPrice": "26304.80000000",
            "highPrice": "26397.46000000",
            "lowPrice": "26088.34000000",
            "lastPrice": "26221.67000000",
            "volume": "18495.35066000",              # Volume in base asset
            "quoteVolume": "485217905.04210480",
            "openTime": 1695686400000,
            "closeTime": 1695772799999,
            "firstId": 3220151555,
            "lastId": 3220849281,
            "count": 697727
        }

        Response MINI type example:
        {
            "symbol": "BTCUSDT",
            "openPrice": "26304.80000000",
            "highPrice": "26397.46000000",
            "lowPrice": "26088.34000000",
            "lastPrice": "26221.67000000",
            "volume": "18495.35066000",              # Volume in base asset
            "quoteVolume": "485217905.04210480",     # Volume in quote asset
            "openTime": 1695686400000,
            "closeTime": 1695772799999,
            "firstId": 3220151555,                   # Trade ID of the first trade in the interval
            "lastId": 3220849281,                    # Trade ID of the last trade in the interval
            "count": 697727                          # Number of trades in the interval
        }

        Weight:
            - 4 for each requested symbol
            - Weight caps at 200 once number of symbols > 50
        """
        return self._ws_api_request_sync("ticker.tradingDay", False, params)


    def ws_get_symbol_ticker_window(self, **params):
        """Get rolling window price change statistics.

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#rolling-window-price-change-statistics

        :param symbol: STRING - Optional - Query ticker of a single symbol
        :type symbol: str
        :param symbols: ARRAY of STRING - Optional - Query ticker for multiple symbols
        :type symbols: list
        :param windowSize: STRING - Required - Supported windowSize values:
            - 1h, 2h, 4h, 6h, 12h
            - 1d, 2d, 3d, 4d, 5d, 6d, 7d, 14d, 30d
        :type windowSize: str
        :param type: ENUM - Optional - FULL (default) or MINI
        :type type: str

        :returns: Websocket message

        With symbol parameter:
        .. code-block:: python
            {
                "symbol": "BTCUSDT",
                "priceChange": "-83.13000000",         # Absolute price change
                "priceChangePercent": "-0.317",        # Relative price change in percent
                "weightedAvgPrice": "26234.58803036",  # quoteVolume / volume
                "openPrice": "26304.80000000",
                "highPrice": "26397.46000000",
                "lowPrice": "26088.34000000",
                "lastPrice": "26221.67000000",
                "volume": "18495.35066000",            # Volume in base asset
                "quoteVolume": "485217905.04210480",   # Volume in quote asset
                "openTime": 1695686400000,
                "closeTime": 1695772799999,
                "firstId": 3220151555,                 # Trade ID of first trade in the interval
                "lastId": 3220849281,                  # Trade ID of last trade in the interval
                "count": 697727                        # Number of trades in the interval
            }

        With symbols parameter:
        .. code-block:: python
            [
                {
                    # Same fields as above
                },
                {
                    # Same fields as above for next symbol
                }
            ]

        For MINI type response:
        .. code-block:: python
            {
                "symbol": "BTCUSDT",
                "openPrice": "26304.80000000",
                "highPrice": "26397.46000000",
                "lowPrice": "26088.34000000",
                "lastPrice": "26221.67000000",
                "volume": "18495.35066000",
                "quoteVolume": "485217905.04210480",
                "openTime": 1695686400000,
                "closeTime": 1695772799999,
                "firstId": 3220151555,
                "lastId": 3220849281,
                "count": 697727
            }

        Weight:
            - 4 for each requested symbol
            - Weight caps at 200 once number of symbols > 50
        """
        return self._ws_api_request_sync("ticker", False, params)


    def ws_get_symbol_ticker(self, **params):
        """Get latest price for a symbol or symbols.

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#symbol-price-ticker

        :param symbol: STRING - Optional - Query ticker of a single symbol
        :type symbol: str
        :param symbols: ARRAY of STRING - Optional - Query ticker for multiple symbols
        :type symbols: list

        :returns: Websocket message

        With symbol parameter:
            {
                "symbol": "BNBBTC",
                "price": "0.01361000"
            }

            With symbols parameter:
            [
                {
                    "symbol": "BNBBTC",
                    "price": "0.01361000"
                },
                {
                    "symbol": "BTCUSDT",
                    "price": "23440.91000000"
                }
            ]

        Weight:
            - 1 for a single symbol
            - 2 for up to 20 symbols
            - 40 for 21 to 100 symbols
            - 40 for all symbols
        """
        return self._ws_api_request_sync("ticker.price", False, params)


    def ws_get_orderbook_ticker(self, **params):
        """Get the best price/quantity on the order book for a symbol or symbols.

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#symbol-order-book-ticker

        :param symbol: STRING - Optional - Query ticker of a single symbol
        :type symbol: str
        :param symbols: ARRAY of STRING - Optional - Query ticker for multiple symbols
        :type symbols: list

        :returns: Websocket response

            With symbol parameter:
            {
                "symbol": "BNBBTC",
                "bidPrice": "0.01358000",
                "bidQty": "0.95200000",
                "askPrice": "0.01358100",
                "askQty": "11.91700000"
            }

            With symbols parameter:
            [
                {
                    "symbol": "BNBBTC",
                    "bidPrice": "0.01358000",
                    "bidQty": "0.95200000",
                    "askPrice": "0.01358100",
                    "askQty": "11.91700000"
                },
                {
                    "symbol": "BTCUSDT",
                    "bidPrice": "23440.90000000",
                    "bidQty": "0.00200000",
                    "askPrice": "23440.91000000",
                    "askQty": "0.00200000"
                }
            ]

        Weight:
            - 2 for a single symbol
            - 4 for up to 100 symbols
            - 40 for 101 or more symbols
        """
        return self._ws_api_request_sync("ticker.book", False, params)


    def ws_ping(self, **params):
        """Test connectivity

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#test-connectivity

        :returns: API response

            {
                "id": "922bcc6e-9de8-440d-9e84-7c80933a8d0d",
                "status": 200,
                "result": {},
                "rateLimits": [
                    {
                        "rateLimitType": "REQUEST_WEIGHT",
                        "interval": "MINUTE",
                        "intervalNum": 1,
                        "limit": 6000,
                        "count": 1
                    }
                ]
            }


        Weight: 1
        """
        return self._ws_api_request_sync("ping", False, params)


    def ws_get_time(self, **params):
        """
        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#check-server-time

        :returns: API response with server time

            {
                "id": "187d3cb2-942d-484c-8271-4e2141bbadb1",
                "status": 200,
                "result": {
                    "serverTime": 1656400526260
                },
                "rateLimits": [
                    {
                        "rateLimitType": "REQUEST_WEIGHT",
                        "interval": "MINUTE",
                        "intervalNum": 1,
                        "limit": 6000,
                        "count": 1
                    }
                ]
            }

        Weight: 1
        Data Source: Memory
        """
        return self._ws_api_request_sync("time", False, params)


    def ws_get_exchange_info(self, **params):
        """Query current exchange trading rules, rate limits, and symbol information.

        https://developers.binance.com/docs/binance-spot-api-docs/testnet/web-socket-api/public-api-requests#exchange-information

        :param symbol: str - Filter by single symbol (optional)
        :param symbols: list - Filter by multiple symbols (optional)
        :param permissions: list or str - Filter symbols by permissions (optional)

        :returns: API response containing exchange information including:
            - Rate limits
            - Exchange filters
            - Symbol information including:
                - Status
                - Base/quote assets
                - Order types allowed
                - Filters (price, lot size, etc)
                - Trading permissions
                - Self-trade prevention modes

            Example response:
            {
                "timezone": "UTC",
                "serverTime": 1655969291181,
                "rateLimits": [
                    {
                        "rateLimitType": "REQUEST_WEIGHT",
                        "interval": "MINUTE",
                        "intervalNum": 1,
                        "limit": 6000
                    },
                    ...
                ],
                "exchangeFilters": [],
                "symbols": [
                    {
                        "symbol": "BTCUSDT",
                        "status": "TRADING",
                        "baseAsset": "BTC",
                        "baseAssetPrecision": 8,
                        ...
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        Notes:
            - Only one of symbol, symbols, permissions parameters can be specified
            - Without parameters, displays all symbols with ["SPOT", "MARGIN", "LEVERAGED"] permissions
            - To list all active symbols, explicitly request all permissions
            - Permissions accepts either a list or single permission name (e.g. "SPOT")

        Weight: 20
        Data Source: Memory
        """
        return self._ws_api_request_sync("exchangeInfo", False, params)

    ####################################################
    # WS Futures Endpoints
    ####################################################

    def ws_futures_get_order_book(self, **params):
        """
        Get the order book for a symbol
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/websocket-api
        """
        return self._ws_futures_api_request_sync("depth", False, params)


    def ws_futures_get_all_tickers(self, **params):
        """
        Latest price for a symbol or symbols
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/websocket-api/Symbol-Price-Ticker
        """
        return self._ws_futures_api_request_sync("ticker.price", False, params)


    def ws_futures_get_order_book_ticker(self, **params):
        """
        Best price/qty on the order book for a symbol or symbols.
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/websocket-api/Symbol-Order-Book-Ticker
        """
        return self._ws_futures_api_request_sync("ticker.book", False, params)


    def ws_futures_create_order(self, **params):
        """
        Send in a new order
        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/websocket-api
        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return self._ws_futures_api_request_sync("order.place", True, params)


    def ws_futures_edit_order(self, **params):
        """
        Edit an order
        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/websocket-api/Modify-Order
        """
        return self._ws_futures_api_request_sync("order.modify", True, params)


    def ws_futures_cancel_order(self, **params):
        """
        cancel an order
        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/websocket-api/Cancel-Order
        """
        return self._ws_futures_api_request_sync("order.cancel", True, params)


    def ws_futures_get_order(self, **params):
        """
        Get an order
        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/websocket-api/Query-Order
        """
        return self._ws_futures_api_request_sync("order.status", True, params)


    def ws_futures_v2_account_position(self, **params):
        """
        Get current position information(only symbol that has position or open orders will be returned).
        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/websocket-api/Position-Info-V2
        """
        return self._ws_futures_api_request_sync("v2/account.position", True, params)


    def ws_futures_account_position(self, **params):
        """
        Get current position information.
        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/websocket-api/Position-Information
        """
        return self._ws_futures_api_request_sync("account.position", True, params)


    def ws_futures_v2_account_balance(self, **params):
        """
        Get current account information.
        https://developers.binance.com/docs/derivatives/usds-margined-futures/account/websocket-api#api-description
        """
        return self._ws_futures_api_request_sync("v2/account.balance", True, params)


    def ws_futures_account_balance(self, **params):
        """
        Get current account information.
        https://developers.binance.com/docs/derivatives/usds-margined-futures/account/websocket-api/Futures-Account-Balance
        """
        return self._ws_futures_api_request_sync("account.balance", True, params)


    def ws_futures_v2_account_status(self, **params):
        """
        Get current account information. User in single-asset/ multi-assets mode will see different value, see comments in response section for detail.
        https://developers.binance.com/docs/derivatives/usds-margined-futures/account/websocket-api/Account-Information-V2
        """
        return self._ws_futures_api_request_sync("v2/account.status", True, params)


    def ws_futures_account_status(self, **params):
        """
        Get current account information. User in single-asset/ multi-assets mode will see different value, see comments in response section for detail.
        https://developers.binance.com/docs/derivatives/usds-margined-futures/account/websocket-api/Account-Information
        """
        return self._ws_futures_api_request_sync("account.status", True, params)

    ###############################################
    ### Gift card api
    ###############################################
