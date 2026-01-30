"""
OptionsMixin - Options(期权)

此 mixin 包含所有 Options(期权) 相关的方法。
"""
from typing import Dict, Any, Optional

# 此 mixin 依赖 ClientCore 提供的请求方法


class OptionsMixin:
    """
    Options(期权) API Mixin
    
    此 mixin 提供所有 Options(期权) 相关的方法。
    这些方法依赖 AsyncClientCore 或 ClientCore 提供的请求基础设施。
    """

    def options_ping(self):
        """Test connectivity

        https://developers.binance.com/docs/derivatives/option/market-data/Test-Connectivity

        """
        return self._request_options_api("get", "ping")


    def options_time(self):
        """Get server time

        https://developers.binance.com/docs/derivatives/option/market-data

        """
        return self._request_options_api("get", "time")


    def options_info(self):
        """Get current trading pair info

        https://binance-docs.github.io/apidocs/voptions/en/#get-current-trading-pair-info

        """
        return self._request_options_api("get", "optionInfo")


    def options_exchange_info(self):
        """Get current limit info and trading pair info

        https://developers.binance.com/docs/derivatives/option/market-data/Exchange-Information

        """
        return self._request_options_api("get", "exchangeInfo")


    def options_index_price(self, **params):
        """Get the spot index price

        https://developers.binance.com/docs/derivatives/option/market-data/Symbol-Price-Ticker

        :param underlying: required - Spot pair(Option contract underlying asset)- BTCUSDT
        :type underlying: str

        """
        return self._request_options_api("get", "index", data=params)


    def options_price(self, **params):
        """Get the latest price

        https://developers.binance.com/docs/derivatives/option/market-data/24hr-Ticker-Price-Change-Statistics

        :param symbol: optional - Option trading pair - BTC-200730-9000-C
        :type symbol: str

        """
        return self._request_options_api("get", "ticker", data=params)


    def options_mark_price(self, **params):
        """Get the latest mark price

        https://developers.binance.com/docs/derivatives/option/market-data/Option-Mark-Price

        :param symbol: optional - Option trading pair - BTC-200730-9000-C
        :type symbol: str

        """
        return self._request_options_api("get", "mark", data=params)


    def options_order_book(self, **params):
        """Depth information

        https://developers.binance.com/docs/derivatives/option/market-data/Order-Book

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param limit: optional - Default:100 Max:1000.Optional value:[10, 20, 50, 100, 500, 1000] - 100
        :type limit: int

        """
        return self._request_options_api("get", "depth", data=params)


    def options_klines(self, **params):
        """Candle data

        https://developers.binance.com/docs/derivatives/option/market-data/Kline-Candlestick-Data

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param interval: required - Time interval - 5m
        :type interval: str
        :param startTime: optional - Start Time - 1592317127349
        :type startTime: int
        :param endTime: optional - End Time - 1592317127349
        :type endTime: int
        :param limit: optional - Number of records Default:500 Max:1500 - 500
        :type limit: int

        """
        return self._request_options_api("get", "klines", data=params)


    def options_recent_trades(self, **params):
        """Recently completed Option trades

        https://developers.binance.com/docs/derivatives/option/market-data/Recent-Trades-List

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param limit: optional - Number of records Default:100 Max:500 - 100
        :type limit: int

        """
        return self._request_options_api("get", "trades", data=params)


    def options_historical_trades(self, **params):
        """Query trade history

        https://developers.binance.com/docs/derivatives/option/market-data/Old-Trades-Lookup

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param fromId: optional - The deal ID from which to return. The latest deal record is returned by default - 1592317127349
        :type fromId: int
        :param limit: optional - Number of records Default:100 Max:500 - 100
        :type limit: int

        """
        return self._request_options_api("get", "historicalTrades", data=params)

    # Account and trading interface endpoints


    def options_account_info(self, **params):
        """Account asset info (USER_DATA)

        https://developers.binance.com/docs/derivatives/option/account

        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api("get", "account", signed=True, data=params)


    def options_get_bill(self, **params):
        """Get account funding flows

        https://developers.binance.com/docs/derivatives/option/account/Account-Funding-Flow

        :param currency: required
        :type currency: str
        :param recordId: optional
        :type recordId: int
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param limit: optional
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response
        """
        return self._request_options_api("get", "bill", signed=True, data=params)


    def options_funds_transfer(self, **params):
        """Funds transfer (USER_DATA)

        https://binance-docs.github.io/apidocs/voptions/en/#funds-transfer-user_data

        :param currency: required - Asset type - USDT
        :type currency: str
        :param type: required - IN: Transfer from spot account to option account OUT: Transfer from option account to spot account - IN
        :type type: str (ENUM)
        :param amount: required - Amount - 10000
        :type amount: float
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api("post", "transfer", signed=True, data=params)


    def options_positions(self, **params):
        """Option holdings info (USER_DATA)

        https://developers.binance.com/docs/derivatives/option/trade/Option-Position-Information

        :param symbol: optional - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api("get", "position", signed=True, data=params)


    def options_exercise_record(self, **params):
        """
        Get account exercise records.

        https://developers.binance.com/docs/derivatives/option/trade/User-Exercise-Record

        :param symbol: optional
        :type symbol: str
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param limit: optional
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response
        """
        return self._request_options_api("get", "exerciseRecord", signed=True, data=params)


    def options_bill(self, **params):
        """Account funding flow (USER_DATA)

        https://binance-docs.github.io/apidocs/voptions/en/#account-funding-flow-user_data

        :param currency: required - Asset type - USDT
        :type currency: str
        :param recordId: optional - Return the recordId and subsequent data, the latest data is returned by default - 100000
        :type recordId: int
        :param startTime: optional - Start Time - 1593511200000
        :type startTime: int
        :param endTime: optional - End Time - 1593511200000
        :type endTime: int
        :param limit: optional - Number of result sets returned Default:100 Max:1000 - 100
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api("post", "bill", signed=True, data=params)


    def options_place_order(self, **params):
        """Option order (TRADE)

        https://developers.binance.com/docs/derivatives/option/trade

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param side: required - Buy/sell direction: SELL, BUY - BUY
        :type side: str (ENUM)
        :param type: required - Order Type: LIMIT, MARKET - LIMIT
        :type type: str (ENUM)
        :param quantity: required - Order Quantity - 3
        :type quantity: float
        :param price: optional - Order Price - 1000
        :type price: float
        :param timeInForce: optional - Time in force method(Default GTC) - GTC
        :type timeInForce: str (ENUM)
        :param reduceOnly: optional - Reduce Only (Default false) - false
        :type reduceOnly: bool
        :param postOnly: optional - Post Only (Default false) - false
        :type postOnly: bool
        :param newOrderRespType: optional - "ACK", "RESULT", Default "ACK" - ACK
        :type newOrderRespType: str (ENUM)
        :param clientOrderId: optional - User-defined order ID cannot be repeated in pending orders - 10000
        :type clientOrderId: str
        :param recvWindow: optional
        :type recvWindow: int

        """
        if "clientOrderId" not in params:
            params["clientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return self._request_options_api("post", "order", signed=True, data=params)


    def options_place_batch_order(self, **params):
        """Place Multiple Option orders (TRADE)

        https://developers.binance.com/docs/derivatives/option/trade/Place-Multiple-Orders

        :param orders: required - order list. Max 5 orders - [{"symbol":"BTC-210115-35000-C","price":"100","quantity":"0.0001","side":"BUY","type":"LIMIT"}]
        :type orders: list
        :param recvWindow: optional
        :type recvWindow: int

        """
        for order in params["batchOrders"]:
            if "newClientOrderId" not in order:
                order["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return self._request_options_api(
            "post", "batchOrders", signed=True, data=params
        )


    def options_cancel_order(self, **params):
        """Cancel Option order (TRADE)

        https://developers.binance.com/docs/derivatives/option/trade/Cancel-Option-Order

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param orderId: optional - Order ID - 4611875134427365377
        :type orderId: str
        :param clientOrderId: optional - User-defined order ID - 10000
        :type clientOrderId: str
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api("delete", "order", signed=True, data=params)


    def options_cancel_batch_order(self, **params):
        """Cancel Multiple Option orders (TRADE)

        https://developers.binance.com/docs/derivatives/option/trade/Cancel-Multiple-Option-Orders

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param orderIds: optional - Order ID - [4611875134427365377,4611875134427365378]
        :type orderId: list
        :param clientOrderIds: optional - User-defined order ID - ["my_id_1","my_id_2"]
        :type clientOrderIds: list
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api(
            "delete", "batchOrders", signed=True, data=params
        )


    def options_cancel_all_orders(self, **params):
        """Cancel all Option orders (TRADE)

        https://developers.binance.com/docs/derivatives/option/trade/Cancel-all-Option-orders-on-specific-symbol

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api(
            "delete", "allOpenOrders", signed=True, data=params
        )


    def options_query_order(self, **params):
        """Query Option order (TRADE)

        https://developers.binance.com/docs/derivatives/option/trade/Query-Single-Order

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param orderId: optional - Order ID - 4611875134427365377
        :type orderId: str
        :param clientOrderId: optional - User-defined order ID - 10000
        :type clientOrderId: str
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api("get", "order", signed=True, data=params)


    def options_query_pending_orders(self, **params):
        """Query current pending Option orders (TRADE)

        https://developers.binance.com/docs/derivatives/option/trade/Query-Current-Open-Option-Orders

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param orderId: optional - Returns the orderId and subsequent orders, the most recent order is returned by default - 100000
        :type orderId: str
        :param startTime: optional - Start Time - 1593511200000
        :type startTime: int
        :param endTime: optional - End Time - 1593511200000
        :type endTime: int
        :param limit: optional - Number of result sets returned Default:100 Max:1000 - 100
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api("get", "openOrders", signed=True, data=params)


    def options_query_order_history(self, **params):
        """Query Option order history (TRADE)

        https://developers.binance.com/docs/derivatives/option/trade/Query-Option-Order-History

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param orderId: optional - Returns the orderId and subsequent orders, the most recent order is returned by default - 100000
        :type orderId: str
        :param startTime: optional - Start Time - 1593511200000
        :type startTime: int
        :param endTime: optional - End Time - 1593511200000
        :type endTime: int
        :param limit: optional - Number of result sets returned Default:100 Max:1000 - 100
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api(
            "get", "historyOrders", signed=True, data=params
        )


    def options_user_trades(self, **params):
        """Option Trade List (USER_DATA)

        https://developers.binance.com/docs/derivatives/option/trade/Account-Trade-List

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param fromId: optional - Trade id to fetch from. Default gets most recent trades. - 4611875134427365376
        :type fromId: int
        :param startTime: optional - Start Time - 1593511200000
        :type startTime: int
        :param endTime: optional - End Time - 1593511200000
        :type endTime: int
        :param limit: optional - Number of result sets returned Default:100 Max:1000 - 100
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api("get", "userTrades", signed=True, data=params)

    ####################################################
    # Options - Market Maker Block Trade
    ####################################################


    def options_create_block_trade_order(self, **params):
        """New Block Trade Order (TRADE)

        https://developers.binance.com/docs/derivatives/option/market-maker-block-trade

        :param liquidity: required - Taker or Maker
        :type liquidity: str
        :param symbol: required - Option trading pair, e.g BTC-200730-9000-C
        :type symbol: str
        :param side: required - BUY or SELL
        :type side: str
        :param price: required - Order Price
        :type price: float
        :param quantity: required - Order Quantity
        :type quantity: float
        :param recvWindow: optional - The value cannot be greater than 60000
        :type recvWindow: int

        :returns: API response

        .. code-block:: python
            {
                "blockTradeSettlementKey": "3668822b8-1baa-6a2f-adb8-d3de6289b361",
                "expireTime": 1730171888109,
                "liquidity": "TAKER",
                "status": "RECEIVED",
                "legs": [
                    {
                        "symbol": "BNB-241101-700-C",
                        "side": "BUY",
                        "quantity": "1.2",
                        "price": "2.8"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException
        """
        return self._request_options_api(
            "post", "block/order/create", signed=True, data=params
        )


    def options_cancel_block_trade_order(self, **params):
        """Cancel Block Trade Order (TRADE)

        https://developers.binance.com/docs/derivatives/option/market-maker-block-trade/Cancel-Block-Trade-Order

        :param blockOrderMatchingKey: required - Block Order Matching Key
        :type blockOrderMatchingKey: str
        :param recvWindow: optional - The value cannot be greater than 60000
        :type recvWindow: int

        :returns: API response

        .. code-block:: python
            {}

        :raises: BinanceRequestException, BinanceAPIException
        """
        return self._request_options_api(
            "delete", "block/order/create", signed=True, data=params
        )


    def options_extend_block_trade_order(self, **params):
        """Extend Block Trade Order (TRADE)

        Extends a block trade expire time by 30 mins from the current time.

        https://developers.binance.com/docs/derivatives/option/market-maker-block-trade/Extend-Block-Trade-Order

        :param blockOrderMatchingKey: required - Block Order Matching Key
        :type blockOrderMatchingKey: str
        :param recvWindow: optional - The value cannot be greater than 60000
        :type recvWindow: int

        :returns: API response

        .. code-block:: python
            {
                "blockTradeSettlementKey": "3668822b8-1baa-6a2f-adb8-d3de6289b361",
                "expireTime": 1730172007000,
                "liquidity": "TAKER",
                "status": "RECEIVED",
                "createTime": 1730170088111,
                "legs": [
                    {
                        "symbol": "BNB-241101-700-C",
                        "side": "BUY",
                        "quantity": "1.2",
                        "price": "2.8"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException
        """
        return self._request_options_api(
            "put", "block/order/create", signed=True, data=params
        )


    def options_get_block_trade_orders(self, **params):
        """Query Block Trade Order (TRADE)

        Check block trade order status.

        https://developers.binance.com/docs/derivatives/option/market-maker-block-trade/Query-Block-Trade-Order

        :param blockOrderMatchingKey: optional - Returns specific block trade for this key
        :type blockOrderMatchingKey: str
        :param endTime: optional
        :type endTime: int
        :param startTime: optional
        :type startTime: int
        :param underlying: optional
        :type underlying: str
        :param recvWindow: optional - The value cannot be greater than 60000
        :type recvWindow: int

        :returns: API response

        .. code-block:: python
            [
                {
                    "blockTradeSettlementKey": "7d046e6e-a429-4335-ab9d-6a681febcde5",
                    "expireTime": 1730172115801,
                    "liquidity": "TAKER",
                    "status": "RECEIVED",
                    "createTime": 1730170315803,
                    "legs": [
                        {
                            "symbol": "BNB-241101-700-C",
                            "side": "BUY",
                            "quantity": "1.2",
                            "price": "2.8"
                        }
                    ]
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException
        """
        return self._request_options_api(
            "get", "block/order/orders", signed=True, data=params
        )


    def options_accept_block_trade_order(self, **params):
        """Accept Block Trade Order (TRADE)

        Accept a block trade order.

        https://developers.binance.com/docs/derivatives/option/market-maker-block-trade/Accept-Block-Trade-Order

        :param blockOrderMatchingKey: required - Block Order Matching Key
        :type blockOrderMatchingKey: str
        :param recvWindow: optional - The value cannot be greater than 60000
        :type recvWindow: int

        :returns: API response

        .. code-block:: python
            {
                "blockTradeSettlementKey": "7d046e6e-a429-4335-ab9d-6a681febcde5",
                "expireTime": 1730172115801,
                "liquidity": "MAKER",
                "status": "ACCEPTED",
                "createTime": 1730170315803,
                "legs": [
                    {
                        "symbol": "BNB-241101-700-C",
                        "side": "SELL",
                        "quantity": "1.2",
                        "price": "2.8"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException
        """
        return self._request_options_api(
            "post", "block/order/execute", signed=True, data=params
        )


    def options_get_block_trade_order(self, **params):
        """Query Block Trade Details (USER_DATA)

        Query block trade details; returns block trade details from counterparty's perspective.

        https://developers.binance.com/docs/derivatives/option/market-maker-block-trade/Query-Block-Trade-Detail

        :param blockOrderMatchingKey: required - Block Order Matching Key
        :type blockOrderMatchingKey: str
        :param recvWindow: optional - The value cannot be greater than 60000
        :type recvWindow: int

        :returns: API response

        .. code-block:: python
            {
                "blockTradeSettlementKey": "12b96c28-ba05-8906-c89t-703215cfb2e6",
                "expireTime": 1730171860460,
                "liquidity": "MAKER",
                "status": "RECEIVED",
                "createTime": 1730170060462,
                "legs": [
                    {
                        "symbol": "BNB-241101-700-C",
                        "side": "SELL",
                        "quantity": "1.66",
                        "price": "20"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException
        """
        return self._request_options_api(
            "get", "block/order/execute", signed=True, data=params
        )


    def options_account_get_block_trades(self, **params):
        """Account Block Trade List (USER_DATA)

        Gets block trades for a specific account.

        https://developers.binance.com/docs/derivatives/option/market-maker-block-trade/Account-Block-Trade-List

        :param endTime: optional
        :type endTime: int
        :param startTime: optional
        :type startTime: int
        :param underlying: optional
        :type underlying: str
        :param recvWindow: optional - The value cannot be greater than 60000
        :type recvWindow: int

        :returns: API response

        .. code-block:: python
            [
                {
                    "parentOrderId": "4675011431944499201",
                    "crossType": "USER_BLOCK",
                    "legs": [
                        {
                            "createTime": 1730170445600,
                            "updateTime": 1730170445600,
                            "symbol": "BNB-241101-700-C",
                            "orderId": "4675011431944499203",
                            "orderPrice": 2.8,
                            "orderQuantity": 1.2,
                            "orderStatus": "FILLED",
                            "executedQty": 1.2,
                            "executedAmount": 3.36,
                            "fee": 0.336,
                            "orderType": "PREV_QUOTED",
                            "orderSide": "BUY",
                            "id": "1125899906900937837",
                            "tradeId": 1,
                            "tradePrice": 2.8,
                            "tradeQty": 1.2,
                            "tradeTime": 1730170445600,
                            "liquidity": "TAKER",
                            "commission": 0.336
                        }
                    ],
                    "blockTradeSettlementKey": "7d085e6e-a229-2335-ab9d-6a581febcd25"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException
        """
        return self._request_options_api(
            "get", "block/user-trades", signed=True, data=params
        )

    # Fiat Endpoints

