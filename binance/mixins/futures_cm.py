"""
FuturesCmMixin - CM Futures(币本位合约) API

此 mixin 包含所有 CM Futures(币本位合约) 相关的方法。
"""
from typing import Dict, Any, Optional

# 此 mixin 依赖 ClientCore 提供的请求方法


class FuturesCmMixin:
    """
    CM Futures(币本位合约) API Mixin
    
    此 mixin 提供所有 CM Futures(币本位合约) 相关的方法。
    这些方法依赖 ClientCore 提供的请求基础设施。
    """

    def futures_coin_ping(self):
        """Test connectivity to the Rest API

       https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api

        """
        return self._request_futures_coin_api("get", "ping")


    def futures_coin_time(self):
        """Test connectivity to the Rest API and get the current server time.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Check-Server-time

        """
        return self._request_futures_coin_api("get", "time")


    def futures_coin_exchange_info(self):
        """Current exchange trading rules and symbol information

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Exchange-Information

        """
        return self._request_futures_coin_api("get", "exchangeInfo")


    def futures_coin_order_book(self, **params):
        """Get the Order Book for the market

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Order-Book

        """
        return self._request_futures_coin_api("get", "depth", data=params)


    def futures_coin_recent_trades(self, **params):
        """Get recent trades (up to last 500).

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Recent-Trades-List

        """
        return self._request_futures_coin_api("get", "trades", data=params)


    def futures_coin_historical_trades(self, **params):
        """Get older market historical trades.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Old-Trades-Lookup

        """
        return self._request_futures_coin_api("get", "historicalTrades", data=params)


    def futures_coin_aggregate_trades(self, **params):
        """Get compressed, aggregate trades. Trades that fill at the time, from the same order, with the same
        price will have the quantity aggregated.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Compressed-Aggregate-Trades-List

        """
        return self._request_futures_coin_api("get", "aggTrades", data=params)


    def futures_coin_klines(self, **params):
        """Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Kline-Candlestick-Data

        """
        return self._request_futures_coin_api("get", "klines", data=params)


    def futures_coin_continous_klines(self, **params):
        """Kline/candlestick bars for a specific contract type. Klines are uniquely identified by their open time.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Continuous-Contract-Kline-Candlestick-Data

        """
        return self._request_futures_coin_api("get", "continuousKlines", data=params)


    def futures_coin_index_price_klines(self, **params):
        """Kline/candlestick bars for the index price of a pair..

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Index-Price-Kline-Candlestick-Data

        """
        return self._request_futures_coin_api("get", "indexPriceKlines", data=params)


    def futures_coin_premium_index_klines(self, **params):
        """Kline/candlestick bars for the index price of a pair..

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Premium-Index-Kline-Data

        """
        return self._request_futures_coin_api("get", "premiumIndexKlines", data=params)


    def futures_coin_mark_price_klines(self, **params):
        """Kline/candlestick bars for the index price of a pair..

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Mark-Price-Kline-Candlestick-Data

        """
        return self._request_futures_coin_api("get", "markPriceKlines", data=params)


    def futures_coin_mark_price(self, **params):
        """Get Mark Price and Funding Rate

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Index-Price-and-Mark-Price

        """
        return self._request_futures_coin_api("get", "premiumIndex", data=params)


    def futures_coin_funding_rate(self, **params):
        """Get funding rate history

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Get-Funding-Rate-History-of-Perpetual-Futures

        """
        return self._request_futures_coin_api("get", "fundingRate", data=params)


    def futures_coin_ticker(self, **params):
        """24 hour rolling window price change statistics.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/24hr-Ticker-Price-Change-Statistics

        """
        return self._request_futures_coin_api("get", "ticker/24hr", data=params)


    def futures_coin_symbol_ticker(self, **params):
        """Latest price for a symbol or symbols.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Symbol-Price-Ticker

        """
        return self._request_futures_coin_api("get", "ticker/price", data=params)


    def futures_coin_orderbook_ticker(self, **params):
        """Best price/qty on the order book for a symbol or symbols.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Symbol-Order-Book-Ticker

        """
        return self._request_futures_coin_api("get", "ticker/bookTicker", data=params)


    def futures_coin_top_longshort_position_ratio(self, **params):
        """Get present long to short ratio for top positions of a specific symbol.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Top-Trader-Long-Short-Ratio
        """
        return self._request_futures_coin_data_api("get", "topLongShortPositionRatio", data=params)


    def futures_coin_top_longshort_account_ratio(self, **params):
        """Get present long to short ratio for top positions of a specific symbol.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Top-Long-Short-Account-Ratio
        """
        return self._request_futures_coin_data_api("get", "topLongShortAccountRatio", data=params)


    def futures_coin_global_longshort_ratio(self, **params):
        """Get present long to short ratio for top positions of a specific symbol.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Long-Short-Ratio
        """
        return self._request_futures_coin_data_api("get", "globalLongShortAccountRatio", data=params)


    def futures_coin_taker_buy_sell_volume(self, **params):
        """Get present long to short ratio for top positions of a specific symbol.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Taker-Buy-Sell-Volume
        """
        return self._request_futures_coin_data_api("get", "takerBuySellVol", data=params)


    def futures_coin_basis(self, **params):
        """Get future basis of a specific symbol

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Basis
        """
        return self._request_futures_coin_data_api("get", "basis", data=params)


    def futures_coin_index_price_constituents(self, **params):
        """Get index price constituents

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Index-Constituents

        """
        return self._request_futures_coin_api("get", "constituents", data=params)


    def futures_coin_liquidation_orders(self, **params):
        """Get all liquidation orders

        https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Users-Force-Orders

        """
        return self._request_futures_coin_api(
            "get", "forceOrders", signed=True, data=params
        )


    def futures_coin_open_interest(self, **params):
        """Get present open interest of a specific symbol.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Open-Interest

        """
        return self._request_futures_coin_api("get", "openInterest", data=params)


    def futures_coin_open_interest_hist(self, **params):
        """Get open interest statistics of a specific symbol.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Open-Interest-Statistics

        """
        return self._request_futures_coin_data_api(
            "get", "openInterestHist", data=params
        )


    def futures_coin_leverage_bracket(self, **params):
        """Notional and Leverage Brackets

        https://developers.binance.com/docs/derivatives/coin-margined-futures/account/rest-api/Notional-Bracket-for-Symbol

        """
        return self._request_futures_coin_api(
            "get", "leverageBracket", version=2, signed=True, data=params
        )


    def new_transfer_history(self, **params):
        """Get future account transaction history list

        https://developers.binance.com/docs/wallet/asset/query-user-universal-transfer

        """
        return self._request_margin_api("get", "asset/transfer", True, data=params)


    def funding_wallet(self, **params):
        """ Query Funding Wallet

        https://developers.binance.com/docs/wallet/asset/funding-wallet

        """
        return self._request_margin_api(
            "post", "asset/get-funding-asset", True, data=params
        )


    def get_user_asset(self, **params):
        """ Get user assets, just for positive data

        https://developers.binance.com/docs/wallet/asset/user-assets

        """
        return self._request_margin_api(
            "post", "asset/getUserAsset", True, data=params, version=3
        )


    def universal_transfer(self, **params):
        """Unviversal transfer api accross different binance account types

        https://developers.binance.com/docs/wallet/asset/user-universal-transfer
        """
        return self._request_margin_api(
            "post", "asset/transfer", signed=True, data=params
        )


    def futures_coin_create_order(self, **params):
        """Send in a new order.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return self._request_futures_coin_api("post", "order", True, data=params)


    def futures_coin_place_batch_order(self, **params):
        """Send in new orders.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Place-Multiple-Orders

        To avoid modifying the existing signature generation and parameter order logic,
        the url encoding is done on the special query param, batchOrders, in the early stage.

        """
        for order in params["batchOrders"]:
            if "newClientOrderId" not in order:
                order["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        query_string = urlencode(params)
        query_string = query_string.replace("%27", "%22")
        params["batchOrders"] = query_string[12:]

        return self._request_futures_coin_api("post", "batchOrders", True, data=params)


    def futures_coin_modify_order(self, **params):
        """Modify an existing order. Currently only LIMIT order modification is supported.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Modify-Order

        """
        return self._request_futures_coin_api("put", "order", True, data=params)


    def futures_coin_get_order(self, **params):
        """Check an order's status.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Query-Order

        """
        return self._request_futures_coin_api("get", "order", True, data=params)


    def futures_coin_get_open_orders(self, **params):
        """Get all open orders on a symbol.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Current-All-Open-Orders

        """
        return self._request_futures_coin_api("get", "openOrders", True, data=params)


    def futures_coin_get_all_orders(self, **params):
        """Get all futures account orders; active, canceled, or filled.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/All-Orders

        """
        return self._request_futures_coin_api(
            "get", "allOrders", signed=True, data=params
        )


    def futures_coin_cancel_order(self, **params):
        """Cancel an active futures order.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Cancel-Order

        """
        return self._request_futures_coin_api(
            "delete", "order", signed=True, data=params
        )


    def futures_coin_cancel_all_open_orders(self, **params):
        """Cancel all open futures orders

        https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Cancel-All-Open-Orders

        """
        return self._request_futures_coin_api(
            "delete", "allOpenOrders", signed=True, force_params=True, data=params
        )


    def futures_coin_cancel_orders(self, **params):
        """Cancel multiple futures orders

        https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Cancel-Multiple-Orders

        """
        if params.get("orderidlist"):
            params["orderidlist"] = quote(
                convert_list_to_json_array(params["orderidlist"])
            )
        if params.get("origclientOrderidlist"):
            params["origclientorderidlist"] = quote(
                convert_list_to_json_array(params["origclientorderidlist"])
            )
        return self._request_futures_coin_api(
            "delete", "batchOrders", True, data=params
        )


    def futures_coin_countdown_cancel_all(self, **params):
        """Cancel all open orders of the specified symbol at the end of the specified countdown.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Auto-Cancel-All-Open-Orders

        :param symbol: required
        :type symbol: str
        :param countdownTime: required
        :type countdownTime: int
        :param recvWindow: optional - the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python
        {
            "symbol": "BTCUSDT",
            "countdownTime": "100000"
        }

        """
        return self._request_futures_coin_api(
            "post", "countdownCancelAll", True, data=params
        )


    def futures_coin_get_open_order(self, **params):
        """Get current open order.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Query-Current-Open-Order

        """
        return self._request_futures_coin_api(
            "get", "openOrder", signed=True, data=params
        )


    def futures_coin_account_balance(self, **params):
        """Get futures account balance

        https://developers.binance.com/docs/derivatives/coin-margined-futures/account/rest-api/Futures-Account-Balance

        """
        return self._request_futures_coin_api(
            "get", "balance", signed=True, data=params
        )


    def futures_coin_account(self, **params):
        """Get current account information.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/account/rest-api/Account-Information

        """
        return self._request_futures_coin_api(
            "get", "account", signed=True, data=params
        )


    def futures_coin_change_leverage(self, **params):
        """Change user's initial leverage of specific symbol market

        https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Change-Initial-Leverage

        """
        return self._request_futures_coin_api(
            "post", "leverage", signed=True, data=params
        )


    def futures_coin_change_margin_type(self, **params):
        """Change the margin type for a symbol

        https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Change-Margin-Type

        """
        return self._request_futures_coin_api(
            "post", "marginType", signed=True, data=params
        )


    def futures_coin_change_position_margin(self, **params):
        """Change the position margin for a symbol

        https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Modify-Isolated-Position-Margin

        """
        return self._request_futures_coin_api(
            "post", "positionMargin", True, data=params
        )


    def futures_coin_position_margin_history(self, **params):
        """Get position margin change history

        https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Get-Position-Margin-Change-History

        """
        return self._request_futures_coin_api(
            "get", "positionMargin/history", True, data=params
        )


    def futures_coin_position_information(self, **params):
        """Get position information

        https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Position-Information

        """
        return self._request_futures_coin_api("get", "positionRisk", True, data=params)


    def futures_coin_account_trades(self, **params):
        """Get trades for the authenticated account and symbol.

        https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Account-Trade-List

        """
        return self._request_futures_coin_api("get", "userTrades", True, data=params)


    def futures_coin_income_history(self, **params):
        """Get income history for authenticated account

        https://developers.binance.com/docs/derivatives/coin-margined-futures/account/rest-api/Get-Income-History

        """
        return self._request_futures_coin_api("get", "income", True, data=params)


    def futures_coin_change_position_mode(self, **params):
        """Change user's position mode (Hedge Mode or One-way Mode ) on EVERY symbol

        https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Change-Position-Mode

        """
        return self._request_futures_coin_api(
            "post", "positionSide/dual", True, data=params
        )


    def futures_coin_get_position_mode(self, **params):
        """Get user's position mode (Hedge Mode or One-way Mode ) on EVERY symbol

        https://developers.binance.com/docs/derivatives/coin-margined-futures/account/rest-api/Get-Current-Position-Mode

        """
        return self._request_futures_coin_api(
            "get", "positionSide/dual", True, data=params
        )


    def futures_coin_stream_get_listen_key(self):
        res = self._request_futures_coin_api("post", "listenKey", signed=False, data={})
        return res["listenKey"]


    def futures_coin_stream_keepalive(self, listenKey):
        params = {"listenKey": listenKey}
        return self._request_futures_coin_api(
            "put", "listenKey", signed=False, data=params
        )


    def futures_coin_stream_close(self, listenKey):
        params = {"listenKey": listenKey}
        return self._request_futures_coin_api(
            "delete", "listenKey", signed=False, data=params
        )


    def futures_coin_account_order_history_download(self, **params):
        """Get Download Id For Futures Order History

        https://developers.binance.com/docs/derivatives/coin-margined-futures/account/rest-api/Get-Download-Id-For-Futures-Order-History

        :param startTime: required - Start timestamp in ms
        :type startTime: int
        :param endTime: required - End timestamp in ms
        :type endTime: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "avgCostTimestampOfLast30d": 7241837,  # Average time taken for data download in the past 30 days
                "downloadId": "546975389218332672"
            }

        Note:
            - Request Limitation is 10 times per month, shared by front end download page and rest api
            - The time between startTime and endTime can not be longer than 1 year

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_futures_coin_api(
            "get", "order/asyn", signed=True, data=params
        )


    def futures_coin_accout_order_history_download_link(self, **params):
        """Get futures order history download link by Id

        https://developers.binance.com/docs/derivatives/coin-margined-futures/account/rest-api/Get-Futures-Order-History-Download-Link-by-Id

        :param downloadId: required - Download ID obtained from futures_coin_download_id
        :type downloadId: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "downloadId": "545923594199212032",
                "status": "completed",     # Enum:completed, processing
                "url": "www.binance.com",  # The link is mapped to download id
                "notified": true,          # ignore
                "expirationTimestamp": 1645009771000,  # The link would expire after this timestamp
                "isExpired": null
            }

            # OR (Response when server is processing)
            {
                "downloadId": "545923594199212032",
                "status": "processing",
                "url": "",
                "notified": false,
                "expirationTimestamp": -1,
                "isExpired": null
            }

        Note:
            - Download link expiration: 24h

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_futures_coin_api("get", "order/asyn/id", True, data=params)


    def futures_coin_account_trade_history_download(self, **params):
        """Get Download Id For Futures Trade History (USER_DATA)

        https://developers.binance.com/docs/derivatives/coin-margined-futures/account/rest-api/Get-Download-Id-For-Futures-Trade-History

        :param startTime: required - Start timestamp in ms
        :type startTime: int
        :param endTime: required - End timestamp in ms
        :type endTime: int

        :returns: API response

        .. code-block:: python

            {
                "avgCostTimestampOfLast30d": 7241837,  # Average time taken for data download in the past 30 days
                "downloadId": "546975389218332672"
            }

        Note:
            - Request Limitation is 5 times per month, shared by front end download page and rest api
            - The time between startTime and endTime can not be longer than 1 year

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_futures_coin_api("get", "trade/asyn", True, data=params)


    def futures_coin_account_trade_history_download_link(self, **params):
        """Get futures trade download link by Id

        https://developers.binance.com/docs/derivatives/coin-margined-futures/account/rest-api/Get-Futures-Trade-Download-Link-by-Id

        :param downloadId: required - Download ID obtained from futures_coin_trade_download_id
        :type downloadId: str

        :returns: API response

        .. code-block:: python

            {
                "downloadId": "545923594199212032",
                "status": "completed",     # Enum:completed, processing
                "url": "www.binance.com",  # The link is mapped to download id
                "notified": true,          # ignore
                "expirationTimestamp": 1645009771000,  # The link would expire after this timestamp
                "isExpired": null
            }

            # OR (Response when server is processing)
            {
                "downloadId": "545923594199212032",
                "status": "processing",
                "url": "",
                "notified": false,
                "expirationTimestamp": -1,
                "isExpired": null
            }

        Note:
            - Download link expiration: 24h

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_futures_coin_api("get", "trade/asyn/id", True, data=params)


    def get_all_coins_info(self, **params):
        """Get information of coins (available for deposit and withdraw) for user.

        https://developers.binance.com/docs/wallet/capital

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "coin": "BTC",
                "depositAllEnable": true,
                "withdrawAllEnable": true,
                "name": "Bitcoin",
                "free": "0",
                "locked": "0",
                "freeze": "0",
                "withdrawing": "0",
                "ipoing": "0",
                "ipoable": "0",
                "storage": "0",
                "isLegalMoney": false,
                "trading": true,
                "networkList": [
                    {
                        "network": "BNB",
                        "coin": "BTC",
                        "withdrawIntegerMultiple": "0.00000001",
                        "isDefault": false,
                        "depositEnable": true,
                        "withdrawEnable": true,
                        "depositDesc": "",
                        "withdrawDesc": "",
                        "specialTips": "Both a MEMO and an Address are required to successfully deposit your BEP2-BTCB tokens to Binance.",
                        "name": "BEP2",
                        "resetAddressStatus": false,
                        "addressRegex": "^(bnb1)[0-9a-z]{38}$",
                        "memoRegex": "^[0-9A-Za-z-_]{1,120}$",
                        "withdrawFee": "0.0000026",
                        "withdrawMin": "0.0000052",
                        "withdrawMax": "0",
                        "minConfirm": 1,
                        "unLockConfirm": 0
                    },
                    {
                        "network": "BTC",
                        "coin": "BTC",
                        "withdrawIntegerMultiple": "0.00000001",
                        "isDefault": true,
                        "depositEnable": true,
                        "withdrawEnable": true,
                        "depositDesc": "",
                        "withdrawDesc": "",
                        "specialTips": "",
                        "name": "BTC",
                        "resetAddressStatus": false,
                        "addressRegex": "^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$|^(bc1)[0-9A-Za-z]{39,59}$",
                        "memoRegex": "",
                        "withdrawFee": "0.0005",
                        "withdrawMin": "0.001",
                        "withdrawMax": "0",
                        "minConfirm": 1,
                        "unLockConfirm": 2
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "capital/config/getall", True, data=params
        )


    def get_account_snapshot(self, **params):
        """Get daily account snapshot of specific type.

        https://developers.binance.com/docs/wallet/account/daily-account-snapshoot

        :param type: required. Valid values are SPOT/MARGIN/FUTURES.
        :type type: string
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param limit: optional
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
               "code":200, // 200 for success; others are error codes
               "msg":"", // error message
               "snapshotVos":[
                  {
                     "data":{
                        "balances":[
                           {
                              "asset":"BTC",
                              "free":"0.09905021",
                              "locked":"0.00000000"
                           },
                           {
                              "asset":"USDT",
                              "free":"1.89109409",
                              "locked":"0.00000000"
                           }
                        ],
                        "totalAssetOfBtc":"0.09942700"
                     },
                     "type":"spot",
                     "updateTime":1576281599000
                  }
               ]
            }

        OR

        .. code-block:: python

            {
               "code":200, // 200 for success; others are error codes
               "msg":"", // error message
               "snapshotVos":[
                  {
                     "data":{
                        "marginLevel":"2748.02909813",
                        "totalAssetOfBtc":"0.00274803",
                        "totalLiabilityOfBtc":"0.00000100",
                        "totalNetAssetOfBtc":"0.00274750",
                        "userAssets":[
                           {
                              "asset":"XRP",
                              "borrowed":"0.00000000",
                              "free":"1.00000000",
                              "interest":"0.00000000",
                              "locked":"0.00000000",
                              "netAsset":"1.00000000"
                           }
                        ]
                     },
                     "type":"margin",
                     "updateTime":1576281599000
                  }
               ]
            }

        OR

        .. code-block:: python

            {
               "code":200, // 200 for success; others are error codes
               "msg":"", // error message
               "snapshotVos":[
                  {
                     "data":{
                        "assets":[
                           {
                              "asset":"USDT",
                              "marginBalance":"118.99782335",
                              "walletBalance":"120.23811389"
                           }
                        ],
                        "position":[
                           {
                              "entryPrice":"7130.41000000",
                              "markPrice":"7257.66239673",
                              "positionAmt":"0.01000000",
                              "symbol":"BTCUSDT",
                              "unRealizedProfit":"1.24029054"
                           }
                        ]
                     },
                     "type":"futures",
                     "updateTime":1576281599000
                  }
               ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api("get", "accountSnapshot", True, data=params)


    def disable_fast_withdraw_switch(self, **params):
        """Disable Fast Withdraw Switch

        https://binance-docs.github.io/apidocs/spot/en/#disable-fast-withdraw-switch-user_data

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "post", "disableFastWithdrawSwitch", True, data=params
        )


    def enable_fast_withdraw_switch(self, **params):
        """Enable Fast Withdraw Switch

        https://binance-docs.github.io/apidocs/spot/en/#enable-fast-withdraw-switch-user_data

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "post", "enableFastWithdrawSwitch", True, data=params
        )
