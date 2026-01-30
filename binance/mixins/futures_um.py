"""
FuturesUmMixin - UM Futures(U本位合约) API

此 mixin 包含所有 UM Futures(U本位合约) 相关的方法。
"""
from ..enums import HistoricalKlinesType
from typing import Dict, Any, Optional

# 此 mixin 依赖 ClientCore 提供的请求方法


class FuturesUmMixin:
    """
    UM Futures(U本位合约) API Mixin
    
    此 mixin 提供所有 UM Futures(U本位合约) 相关的方法。
    这些方法依赖 ClientCore 提供的请求基础设施。
    """

    def futures_ping(self):
        """Test connectivity to the Rest API

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api

        """
        return self._request_futures_api("get", "ping")


    def futures_time(self):
        """Test connectivity to the Rest API and get the current server time.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Check-Server-Time

        """
        return self._request_futures_api("get", "time")


    def futures_exchange_info(self):
        """Current exchange trading rules and symbol information

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Exchange-Information

        """
        return self._request_futures_api("get", "exchangeInfo")


    def futures_order_book(self, **params):
        """Get the Order Book for the market

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Order-Book

        """
        return self._request_futures_api("get", "depth", data=params)


    def futures_recent_trades(self, **params):
        """Get recent trades (up to last 500).

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Recent-Trades-List

        """
        return self._request_futures_api("get", "trades", data=params)


    def futures_historical_trades(self, **params):
        """Get older market historical trades.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Old-Trades-Lookup

        """
        return self._request_futures_api("get", "historicalTrades", data=params)


    def futures_aggregate_trades(self, **params):
        """Get compressed, aggregate trades. Trades that fill at the time, from the same order, with the same
        price will have the quantity aggregated.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Compressed-Aggregate-Trades-List

        """
        return self._request_futures_api("get", "aggTrades", data=params)


    def futures_klines(self, **params):
        """Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Kline-Candlestick-Data

        """
        return self._request_futures_api("get", "klines", data=params)


    def futures_mark_price_klines(self, **params):
        """Kline/candlestick bars for the mark price of a symbol. Klines are uniquely identified by their open time.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Mark-Price-Kline-Candlestick-Data

        """
        return self._request_futures_api("get", "markPriceKlines", data=params)


    def futures_index_price_klines(self, **params):
        """Kline/candlestick bars for the index price of a symbol. Klines are uniquely identified by their open time.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Index-Price-Kline-Candlestick-Data

        """
        return self._request_futures_api("get", "indexPriceKlines", data=params)


    def futures_premium_index_klines(self, **params):
        """Premium index kline bars of a symbol.l. Klines are uniquely identified by their open time.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Premium-Index-Kline-Data

        """
        return self._request_futures_api("get", "premiumIndexKlines", data=params)


    def futures_continuous_klines(self, **params):
        """Kline/candlestick bars for a specific contract type. Klines are uniquely identified by their open time.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Continuous-Contract-Kline-Candlestick-Data

        """
        return self._request_futures_api("get", "continuousKlines", data=params)


    def futures_historical_klines(
        self, symbol: str, interval :str, start_str, end_str=None, limit=None
    ):
        """Get historical futures klines from Binance

        :param symbol: Name of symbol pair e.g. BNBBTC
        :type symbol: str
        :param interval: Binance Kline interval
        :type interval: str
        :param start_str: Start date string in UTC format or timestamp in milliseconds
        :type start_str: str|int
        :param end_str: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
        :type end_str: str|int
        :param limit: Default None (fetches full range in batches of max 1000 per request). To limit the number of rows, pass an integer.
        :type limit: int

        :return: list of OHLCV values (Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore)

        """
        return self._historical_klines(
            symbol,
            interval,
            start_str,
            end_str=end_str,
            limit=limit,
            klines_type=HistoricalKlinesType.FUTURES,
        )


    def futures_historical_mark_price_klines(
        self, symbol: str, interval: str, start_str, end_str=None, limit=None
    ):
        """Get historical futures mark price klines from Binance

        :param symbol: Name of symbol pair e.g. BNBBTC
        :type symbol: str
        :param interval: Binance Kline interval
        :type interval: str
        :param start_str: Start date string in UTC format or timestamp in milliseconds
        :type start_str: str|int
        :param end_str: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
        :type end_str: str|int
        :param limit: Default None (fetches full range in batches of max 1000 per request). To limit the number of rows, pass an integer.
        :type limit: int

        :return: list of OHLCV values (Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore)

        """
        return self._historical_klines(
            symbol,
            interval,
            start_str,
            end_str=end_str,
            limit=limit,
            klines_type=HistoricalKlinesType.FUTURES_MARK_PRICE,
        )


    def futures_historical_klines_generator(
        self, symbol, interval, start_str, end_str=None
    ):
        """Get historical futures klines generator from Binance

        :param symbol: Name of symbol pair e.g. BNBBTC
        :type symbol: str
        :param interval: Binance Kline interval
        :type interval: str
        :param start_str: Start date string in UTC format or timestamp in milliseconds
        :type start_str: str|int
        :param end_str: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
        :type end_str: str|int

        :return: generator of OHLCV values

        """

        return self._historical_klines_generator(
            symbol,
            interval,
            start_str,
            end_str=end_str,
            klines_type=HistoricalKlinesType.FUTURES,
        )


    def futures_mark_price(self, **params):
        """Get Mark Price and Funding Rate

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Mark-Price

        """
        return self._request_futures_api("get", "premiumIndex", data=params)


    def futures_funding_rate(self, **params):
        """Get funding rate history

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History

        """
        return self._request_futures_api("get", "fundingRate", data=params)


    def futures_top_longshort_account_ratio(self, **params):
        """Get present long to short ratio for top accounts of a specific symbol.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Top-Long-Short-Account-Ratio
        """
        return self._request_futures_data_api(
            "get", "topLongShortAccountRatio", data=params
        )


    def futures_top_longshort_position_ratio(self, **params):
        """Get present long to short ratio for top positions of a specific symbol.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Top-Trader-Long-Short-Ratio
        """
        return self._request_futures_data_api(
            "get", "topLongShortPositionRatio", data=params
        )


    def futures_global_longshort_ratio(self, **params):
        """Get present global long to short ratio of a specific symbol.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Long-Short-Ratio
        """
        return self._request_futures_data_api(
            "get", "globalLongShortAccountRatio", data=params
        )


    def futures_taker_longshort_ratio(self, **params):
        """Get taker buy to sell volume ratio of a specific symbol

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Taker-BuySell-Volume
        """
        return self._request_futures_data_api(
            "get", "takerlongshortRatio", data=params
        )


    def futures_basis(self, **params):
        """Get future basis of a specific symbol

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Basis
        """
        return self._request_futures_data_api(
            "get", "basis", data=params
        )


    def futures_ticker(self, **params):
        """24 hour rolling window price change statistics.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/24hr-Ticker-Price-Change-Statistics

        """
        return self._request_futures_api("get", "ticker/24hr", data=params)


    def futures_symbol_ticker(self, **params):
        """Latest price for a symbol or symbols.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Symbol-Price-Ticker

        """
        return self._request_futures_api("get", "ticker/price", data=params)


    def futures_orderbook_ticker(self, **params):
        """Best price/qty on the order book for a symbol or symbols.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Symbol-Order-Book-Ticker

        """
        return self._request_futures_api("get", "ticker/bookTicker", data=params)


    def futures_delivery_price(self, **params):
        """Get latest price for a symbol or symbols

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Delivery-Price

        """
        return self._request_futures_data_api("get", "delivery-price", data=params)


    def futures_index_price_constituents(self, **params):
        """Get index price constituents

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Index-Constituents

        """
        return self._request_futures_api("get", "constituents", data=params)


    def futures_insurance_fund_balance_snapshot(self, **params):
        """Get Insurance Fund Balance Snapshot

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Insurance-Fund-Balance

        """
        return self._request_futures_api("get", "insuranceBalance", data=params)


    def futures_liquidation_orders(self, **params):
        """Get all liquidation orders

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Users-Force-Orders

        """
        return self._request_futures_api("get", "forceOrders", signed=True, data=params)


    def futures_api_trading_status(self, **params):
        """Get quantitative trading rules for order placement, such as Unfilled Ratio (UFR), Good-Til-Canceled Ratio (GCR),
        Immediate-or-Cancel (IOC) & Fill-or-Kill (FOK) Expire Ratio (IFER), among others.
        https://www.binance.com/en/support/faq/binance-futures-trading-quantitative-rules-4f462ebe6ff445d4a170be7d9e897272

        https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Futures-Trading-Quantitative-Rules-Indicators

        :param symbol: optional
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "indicators": { // indicator: quantitative rules indicators, value: user's indicators value, triggerValue: trigger indicator value threshold of quantitative rules.
                    "BTCUSDT": [
                        {
                            "isLocked": true,
                            "plannedRecoverTime": 1545741270000,
                            "indicator": "UFR",  // Unfilled Ratio (UFR)
                            "value": 0.05,  // Current value
                            "triggerValue": 0.995  // Trigger value
                        },
                        {
                            "isLocked": true,
                            "plannedRecoverTime": 1545741270000,
                            "indicator": "IFER",  // IOC/FOK Expiration Ratio (IFER)
                            "value": 0.99,  // Current value
                            "triggerValue": 0.99  // Trigger value
                        },
                        {
                            "isLocked": true,
                            "plannedRecoverTime": 1545741270000,
                            "indicator": "GCR",  // GTC Cancellation Ratio (GCR)
                            "value": 0.99,  // Current value
                            "triggerValue": 0.99  // Trigger value
                        },
                        {
                            "isLocked": true,
                            "plannedRecoverTime": 1545741270000,
                            "indicator": "DR",  // Dust Ratio (DR)
                            "value": 0.99,  // Current value
                            "triggerValue": 0.99  // Trigger value
                        }
                    ],
                    "ETHUSDT": [
                        {
                            "isLocked": true,
                            "plannedRecoverTime": 1545741270000,
                            "indicator": "UFR",
                            "value": 0.05,
                            "triggerValue": 0.995
                        },
                        {
                            "isLocked": true,
                            "plannedRecoverTime": 1545741270000,
                            "indicator": "IFER",
                            "value": 0.99,
                            "triggerValue": 0.99
                        },
                        {
                            "isLocked": true,
                            "plannedRecoverTime": 1545741270000,
                            "indicator": "GCR",
                            "value": 0.99,
                            "triggerValue": 0.99
                        }
                        {
                            "isLocked": true,
                            "plannedRecoverTime": 1545741270000,
                            "indicator": "DR",
                            "value": 0.99,
                            "triggerValue": 0.99
                        }
                    ]
                },
                "updateTime": 1545741270000
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_futures_api(
            "get", "apiTradingStatus", signed=True, data=params
        )


    def futures_commission_rate(self, **params):
        """Get Futures commission rate

        https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/User-Commission-Rate

        :param symbol: required
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "symbol": "BTCUSDT",
                "makerCommissionRate": "0.0002",  // 0.02%
                "takerCommissionRate": "0.0004"   // 0.04%
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_futures_api(
            "get", "commissionRate", signed=True, data=params
        )


    def futures_adl_quantile_estimate(self, **params):
        """Get Position ADL Quantile Estimate

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Position-ADL-Quantile-Estimation

        """
        return self._request_futures_api("get", "adlQuantile", signed=True, data=params)


    def futures_open_interest(self, **params):
        """Get present open interest of a specific symbol.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Open-Interest

        """
        return self._request_futures_api("get", "openInterest", data=params)


    def futures_index_info(self, **params):
        """Get index_info

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Composite-Index-Symbol-Information

        """
        return self._request_futures_api("get", "indexInfo", data=params)


    def futures_open_interest_hist(self, **params):
        """Get open interest statistics of a specific symbol.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Open-Interest-Statistics

        """
        return self._request_futures_data_api("get", "openInterestHist", data=params)


    def futures_leverage_bracket(self, **params):
        """Notional and Leverage Brackets

        https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Notional-and-Leverage-Brackets

        """
        return self._request_futures_api("get", "leverageBracket", True, data=params)


    def futures_account_transfer(self, **params):
        """Execute transfer between spot account and futures account.

        https://binance-docs.github.io/apidocs/futures/en/#new-future-account-transfer

        """
        return self._request_margin_api("post", "futures/transfer", True, data=params)


    def transfer_history(self, **params):
        """Get future account transaction history list

        https://binance-docs.github.io/apidocs/futures/en/#get-future-account-transaction-history-list-user_data

        """
        return self._request_margin_api("get", "futures/transfer", True, data=params)


    def futures_loan_borrow_history(self, **params):
        return self._request_margin_api(
            "get", "futures/loan/borrow/history", True, data=params
        )


    def futures_loan_repay_history(self, **params):
        return self._request_margin_api(
            "get", "futures/loan/repay/history", True, data=params
        )


    def futures_loan_wallet(self, **params):
        return self._request_margin_api(
            "get", "futures/loan/wallet", True, data=params, version=2
        )


    def futures_cross_collateral_adjust_history(self, **params):
        return self._request_margin_api(
            "get", "futures/loan/adjustCollateral/history", True, data=params
        )


    def futures_cross_collateral_liquidation_history(self, **params):
        return self._request_margin_api(
            "get", "futures/loan/liquidationHistory", True, data=params
        )


    def futures_loan_interest_history(self, **params):
        return self._request_margin_api(
            "get", "futures/loan/interestHistory", True, data=params
        )


    def futures_create_order(self, **params):
        """Send in a new order.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return self._request_futures_api("post", "order", True, data=params)


    def futures_limit_order(self, **params):
        """Send in a new futures limit order.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        params["type"] = "LIMIT"
        return self._request_futures_api("post", "order", True, data=params)


    def futures_market_order(self, **params):
        """Send in a new futures market order.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        params["type"] = "MARKET"
        return self._request_futures_api("post", "order", True, data=params)



    def futures_limit_buy_order(self, **params):
        """Send in a new futures limit buy order.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        params["side"] = "BUY"
        params["type"] = "LIMIT"
        return self._request_futures_api("post", "order", True, data=params)


    def futures_limit_sell_order(self, **params):
        """Send in a new futures limit sell order.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        params["side"] = "SELL"
        params["type"] = "LIMIT"
        return self._request_futures_api("post", "order", True, data=params)


    def futures_market_buy_order(self, **params):
        """Send in a new futures market buy order.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        params["side"] = "BUY"
        params["type"] = "MARKET"
        return self._request_futures_api("post", "order", True, data=params)


    def futures_market_sell_order(self, **params):
        """Send in a new futures market sell order.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        params["side"] = "SELL"
        params["type"] = "MARKET"
        return self._request_futures_api("post", "order", True, data=params)


    def futures_modify_order(self, **params):
        """Modify an existing order. Currently only LIMIT order modification is supported.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Modify-Order

        """
        return self._request_futures_api("put", "order", True, data=params)


    def futures_create_test_order(self, **params):
        """Testing order request, this order will not be submitted to matching engine

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/New-Order-Test

        """
        return self._request_futures_api("post", "order/test", True, data=params)


    def futures_place_batch_order(self, **params):
        """Send in new orders.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Place-Multiple-Orders

        To avoid modifying the existing signature generation and parameter order logic,
        the url encoding is done on the special query param, batchOrders, in the early stage.

        """
        for order in params["batchOrders"]:
            if "newClientOrderId" not in order:
                order["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        query_string = urlencode(params)
        query_string = query_string.replace("%27", "%22")
        params["batchOrders"] = query_string[12:]
        return self._request_futures_api(
            "post", "batchOrders", True, data=params, force_params=True
        )


    def futures_get_order(self, **params):
        """Check an order's status.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Query-Order

        """
        return self._request_futures_api("get", "order", True, data=params)


    def futures_get_open_orders(self, **params):
        """Get all open orders on a symbol.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Current-All-Open-Orders

        """
        return self._request_futures_api("get", "openOrders", True, data=params)


    def futures_get_all_orders(self, **params):
        """Get all futures account orders; active, canceled, or filled.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/All-Orders

        """
        return self._request_futures_api("get", "allOrders", True, data=params)


    def futures_cancel_order(self, **params):
        """Cancel an active futures order.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Cancel-Order

        """
        return self._request_futures_api("delete", "order", True, data=params)


    def futures_cancel_all_open_orders(self, **params):
        """Cancel all open futures orders

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Cancel-All-Open-Orders

        """
        return self._request_futures_api("delete", "allOpenOrders", True, data=params)


    def futures_cancel_orders(self, **params):
        """Cancel multiple futures orders

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Cancel-Multiple-Orders

        """
        if params.get("orderidlist"):
            params["orderidlist"] = quote(
                convert_list_to_json_array(params["orderidlist"])
            )
        if params.get("origclientorderidlist"):
            params["origclientorderidlist"] = quote(
                convert_list_to_json_array(params["origclientorderidlist"])
            )
        return self._request_futures_api(
            "delete", "batchOrders", True, force_params=True, data=params
        )


    def futures_countdown_cancel_all(self, **params):
        """Cancel all open orders of the specified symbol at the end of the specified countdown.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Auto-Cancel-All-Open-Orders

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
        return self._request_futures_api(
            "post", "countdownCancelAll", True, data=params
        )


    def futures_account_balance(self, **params):
        """Get futures account balance

        https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Futures-Account-Balance-V3

        """
        return self._request_futures_api("get", "balance", True, 3, data=params)


    def futures_account(self, **params):
        """Get current account information.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Account-Information-V2

        """
        return self._request_futures_api("get", "account", True, 2, data=params)


    def futures_change_leverage(self, **params):
        """Change user's initial leverage of specific symbol market

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Change-Initial-Leverage

        """
        return self._request_futures_api("post", "leverage", True, data=params)


    def futures_change_margin_type(self, **params):
        """Change the margin type for a symbol

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Change-Margin-Type

        """
        return self._request_futures_api("post", "marginType", True, data=params)


    def futures_change_position_margin(self, **params):
        """Change the position margin for a symbol

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Modify-Isolated-Position-Margin

        """
        return self._request_futures_api("post", "positionMargin", True, data=params)


    def futures_position_margin_history(self, **params):
        """Get position margin change history

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Get-Position-Margin-Change-History

        """
        return self._request_futures_api(
            "get", "positionMargin/history", True, data=params
        )


    def futures_position_information(self, **params):
        """Get position information

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Position-Information-V3

        """
        return self._request_futures_api("get", "positionRisk", True, 3, data=params)


    def futures_account_trades(self, **params):
        """Get trades for the authenticated account and symbol.

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Account-Trade-List

        """
        return self._request_futures_api("get", "userTrades", True, data=params)


    def futures_income_history(self, **params):
        """Get income history for authenticated account

        https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Get-Income-History

        """
        return self._request_futures_api("get", "income", True, data=params)


    def futures_change_position_mode(self, **params):
        """Change position mode for authenticated account

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Change-Position-Mode

        """
        return self._request_futures_api("post", "positionSide/dual", True, data=params)


    def futures_get_position_mode(self, **params):
        """Get position mode for authenticated account

        https://binance-docs.github.io/apidocs/futures/en/#get-current-position-mode-user_data

        """
        return self._request_futures_api("get", "positionSide/dual", True, data=params)


    def futures_change_multi_assets_mode(self, multiAssetsMargin: bool):
        """Change user's Multi-Assets mode (Multi-Assets Mode or Single-Asset Mode) on Every symbol

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Change-Multi-Assets-Mode

        """
        params = {"multiAssetsMargin": "true" if multiAssetsMargin else "false"}
        return self._request_futures_api("post", "multiAssetsMargin", True, data=params)


    def futures_get_multi_assets_mode(self):
        """Get user's Multi-Assets mode (Multi-Assets Mode or Single-Asset Mode) on Every symbol

        https://binance-docs.github.io/apidocs/futures/en/#get-current-multi-assets-mode-user_data

        """
        return self._request_futures_api("get", "multiAssetsMargin", True, data={})


    def futures_stream_get_listen_key(self):
        res = self._request_futures_api("post", "listenKey", signed=False, data={})
        return res["listenKey"]


    def futures_stream_keepalive(self, listenKey):
        params = {"listenKey": listenKey}
        return self._request_futures_api("put", "listenKey", signed=False, data=params)


    def futures_stream_close(self, listenKey):
        params = {"listenKey": listenKey}
        return self._request_futures_api(
            "delete", "listenKey", signed=False, data=params
        )

    # new methods

    def futures_account_config(self, **params):
        """Get futures account configuration
        https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Account-Config
        """
        return self._request_futures_api(
            "get", "accountConfig", signed=True, version=1, data=params
        )


    def futures_symbol_config(self, **params):
        """Get current account symbol configuration
        https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Symbol-Config
        """
        return self._request_futures_api(
            "get", "symbolConfig", signed=True, version=1, data=params
        )

    
