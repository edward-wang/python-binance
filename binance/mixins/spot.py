"""
SpotMixin - Spot(现货) API

此 mixin 包含所有 Spot(现货) 相关的方法。
"""
from ..enums import HistoricalKlinesType
from typing import Dict, Any, Optional, List
from ..base_client import BaseClient

# 此 mixin 依赖 ClientCore 提供的请求方法


class SpotMixin:
    """
    Spot(现货) API Mixin
    
    此 mixin 提供所有 Spot(现货) 相关的方法。
    这些方法依赖 ClientCore 提供的请求基础设施。
    """

    def get_products(self) -> Dict:
        """Return list of products currently listed on Binance

        Use get_exchange_info() call instead

        :returns: list - List of product dictionaries

        :raises: BinanceRequestException, BinanceAPIException

        """
        products = self._request_website(
            "get",
            "bapi/asset/v2/public/asset-service/product/get-products?includeEtf=true",
        )
        return products


    def get_exchange_info(self) -> Dict:
        """Return rate limits and list of symbols

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/general-endpoints#exchange-information

        :returns: list - List of product dictionaries

        .. code-block:: python

            {
                "timezone": "UTC",
                "serverTime": 1508631584636,
                "rateLimits": [
                    {
                        "rateLimitType": "REQUESTS",
                        "interval": "MINUTE",
                        "limit": 1200
                    },
                    {
                        "rateLimitType": "ORDERS",
                        "interval": "SECOND",
                        "limit": 10
                    },
                    {
                        "rateLimitType": "ORDERS",
                        "interval": "DAY",
                        "limit": 100000
                    }
                ],
                "exchangeFilters": [],
                "symbols": [
                    {
                        "symbol": "ETHBTC",
                        "status": "TRADING",
                        "baseAsset": "ETH",
                        "baseAssetPrecision": 8,
                        "quoteAsset": "BTC",
                        "quotePrecision": 8,
                        "orderTypes": ["LIMIT", "MARKET"],
                        "icebergAllowed": false,
                        "filters": [
                            {
                                "filterType": "PRICE_FILTER",
                                "minPrice": "0.00000100",
                                "maxPrice": "100000.00000000",
                                "tickSize": "0.00000100"
                            }, {
                                "filterType": "LOT_SIZE",
                                "minQty": "0.00100000",
                                "maxQty": "100000.00000000",
                                "stepSize": "0.00100000"
                            }, {
                                "filterType": "MIN_NOTIONAL",
                                "minNotional": "0.00100000"
                            }
                        ]
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """

        return self._get("exchangeInfo")


    def get_symbol_info(self, symbol) -> Optional[Dict]:
        """Return information about a symbol

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/general-endpoints#exchange-information

        :param symbol: required e.g. BNBBTC
        :type symbol: str

        :returns: Dict if found, None if not

        .. code-block:: python

            {
                "symbol": "ETHBTC",
                "status": "TRADING",
                "baseAsset": "ETH",
                "baseAssetPrecision": 8,
                "quoteAsset": "BTC",
                "quotePrecision": 8,
                "orderTypes": ["LIMIT", "MARKET"],
                "icebergAllowed": false,
                "filters": [
                    {
                        "filterType": "PRICE_FILTER",
                        "minPrice": "0.00000100",
                        "maxPrice": "100000.00000000",
                        "tickSize": "0.00000100"
                    }, {
                        "filterType": "LOT_SIZE",
                        "minQty": "0.00100000",
                        "maxQty": "100000.00000000",
                        "stepSize": "0.00100000"
                    }, {
                        "filterType": "MIN_NOTIONAL",
                        "minNotional": "0.00100000"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """

        res = self.get_exchange_info()

        for item in res["symbols"]:
            if item["symbol"] == symbol.upper():
                return item

        return None

    # General Endpoints


    def ping(self) -> Dict:
        """Test connectivity to the Rest API.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/general-endpoints#test-connectivity

        :returns: Empty array

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get("ping")


    def get_server_time(self) -> Dict:
        """Test connectivity to the Rest API and get the current server time.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/general-endpoints#check-server-time

        :returns: Current server time

        .. code-block:: python

            {
                "serverTime": 1499827319559
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get("time")

    # Market Data Endpoints


    def get_all_tickers(self) -> List[Dict[str, str]]:
        """Latest price for all symbols.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints#symbol-price-ticker

        :returns: List of market tickers

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "price": "4.00000200"
                },
                {
                    "symbol": "ETHBTC",
                    "price": "0.07946600"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        response = self._get("ticker/price")
        if isinstance(response, list) and all(isinstance(item, dict) for item in response):
            return response
        raise TypeError("Expected a list of dictionaries")


    def get_orderbook_tickers(self, **params) -> Dict:
        """Best price/qty on the order book for all symbols.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints#symbol-order-book-ticker

        :param symbol: optional
        :type symbol: str
        :param symbols: optional accepted format  ["BTCUSDT","BNBUSDT"] or %5B%22BTCUSDT%22,%22BNBUSDT%22%5D
        :type symbols: str

        :returns: List of order book market entries

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "bidPrice": "4.00000000",
                    "bidQty": "431.00000000",
                    "askPrice": "4.00000200",
                    "askQty": "9.00000000"
                },
                {
                    "symbol": "ETHBTC",
                    "bidPrice": "0.07946700",
                    "bidQty": "9.00000000",
                    "askPrice": "100000.00000000",
                    "askQty": "1000.00000000"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        data = {}
        if "symbol" in params:
            data["symbol"] = params["symbol"]
        elif "symbols" in params:
            data["symbols"] = params["symbols"]
        return self._get(
            "ticker/bookTicker", data=data
        )


    def get_order_book(self, **params) -> Dict:
        """Get the Order Book for the market

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints#order-book

        :param symbol: required
        :type symbol: str
        :param limit:  Default 100; max 1000
        :type limit: int

        :returns: API response

        .. code-block:: python

            {
                "lastUpdateId": 1027024,
                "bids": [
                    [
                        "4.00000000",     # PRICE
                        "431.00000000",   # QTY
                        []                # Can be ignored
                    ]
                ],
                "asks": [
                    [
                        "4.00000200",
                        "12.00000000",
                        []
                    ]
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get("depth", data=params)


    def get_recent_trades(self, **params) -> Dict:
        """Get recent trades (up to last 500).

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints#recent-trades-list

        :param symbol: required
        :type symbol: str
        :param limit:  Default 500; max 1000.
        :type limit: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "id": 28457,
                    "price": "4.00000100",
                    "qty": "12.00000000",
                    "time": 1499865549590,
                    "isBuyerMaker": true,
                    "isBestMatch": true
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get("trades", data=params)


    def get_historical_trades(self, **params) -> Dict:
        """Get older trades.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints#old-trade-lookup

        :param symbol: required
        :type symbol: str
        :param limit:  Default 500; max 1000.
        :type limit: int
        :param fromId:  TradeId to fetch from. Default gets most recent trades.
        :type fromId: str

        :returns: API response

        .. code-block:: python

            [
                {
                    "id": 28457,
                    "price": "4.00000100",
                    "qty": "12.00000000",
                    "time": 1499865549590,
                    "isBuyerMaker": true,
                    "isBestMatch": true
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get(
            "historicalTrades", data=params
        )


    def get_aggregate_trades(self, **params) -> Dict:
        """Get compressed, aggregate trades. Trades that fill at the time,
        from the same order, with the same price will have the quantity aggregated.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints#compressedaggregate-trades-list

        :param symbol: required
        :type symbol: str
        :param fromId:  ID to get aggregate trades from INCLUSIVE.
        :type fromId: str
        :param startTime: Timestamp in ms to get aggregate trades from INCLUSIVE.
        :type startTime: int
        :param endTime: Timestamp in ms to get aggregate trades until INCLUSIVE.
        :type endTime: int
        :param limit:  Default 500; max 1000.
        :type limit: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "a": 26129,         # Aggregate tradeId
                    "p": "0.01633102",  # Price
                    "q": "4.70443515",  # Quantity
                    "f": 27781,         # First tradeId
                    "l": 27781,         # Last tradeId
                    "T": 1498793709153, # Timestamp
                    "m": true,          # Was the buyer the maker?
                    "M": true           # Was the trade the best price match?
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get("aggTrades", data=params)


    def aggregate_trade_iter(self, symbol: str, start_str=None, last_id=None):
        """Iterate over aggregate trade data from (start_time or last_id) to
        the end of the history so far.

        If start_time is specified, start with the first trade after
        start_time. Meant to initialise a local cache of trade data.

        If last_id is specified, start with the trade after it. This is meant
        for updating a pre-existing local trade data cache.

        Only allows start_str or last_id—not both. Not guaranteed to work
        right if you're running more than one of these simultaneously. You
        will probably hit your rate limit.

        See dateparser docs for valid start and end string formats http://dateparser.readthedocs.io/en/latest/

        If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

        :param symbol: Symbol string e.g. ETHBTC
        :type symbol: str
        :param start_str: Start date string in UTC format or timestamp in milliseconds. The iterator will
        return the first trade occurring later than this time.
        :type start_str: str|int
        :param last_id: aggregate trade ID of the last known aggregate trade.
        Not a regular trade ID. See https://binance-docs.github.io/apidocs/spot/en/#compressed-aggregate-trades-list

        :returns: an iterator of JSON objects, one per trade. The format of
        each object is identical to Client.aggregate_trades().

        :type last_id: int
        """
        if start_str is not None and last_id is not None:
            raise ValueError(
                "start_time and last_id may not be simultaneously specified."
            )

        # If there's no last_id, get one.
        if last_id is None:
            # Without a last_id, we actually need the first trade.  Normally,
            # we'd get rid of it. See the next loop.
            if start_str is None:
                trades = self.get_aggregate_trades(symbol=symbol, fromId=0)
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
                    trades = self.get_aggregate_trades(
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
            trades = self.get_aggregate_trades(symbol=symbol, fromId=last_id)
            # fromId=n returns a set starting with id n, but we already have
            # that one. So get rid of the first item in the result set.
            trades = trades[1:]
            if len(trades) == 0:
                return
            for t in trades:
                yield t
            last_id = trades[-1][self.AGG_ID]


    def get_ui_klines(self, **params) -> Dict:
        """Kline/candlestick bars for a symbol with UI enhancements. Klines are uniquely identified by their open time.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints#uiklines

        :param symbol: required
        :type symbol: str
        :param interval: required - The interval for the klines (e.g., 1m, 3m, 5m, etc.)
        :type interval: str
        :param limit: optional - Default 500; max 1000.
        :type limit: int
        :param startTime: optional - Start time in milliseconds
        :type startTime: int
        :param endTime: optional - End time in milliseconds
        :type endTime: int

        :returns: API response

        .. code-block:: python

            [
                [
                    1499040000000,      # Open time
                    "0.01634790",       # Open
                    "0.80000000",       # High
                    "0.01575800",       # Low
                    "0.01577100",       # Close
                    "148976.11427815",  # Volume
                    1499644799999,      # Close time
                    "2434.19055334",    # Quote asset volume
                    308,                # Number of trades
                    "1756.87402397",    # Taker buy base asset volume
                    "28.46694368",      # Taker buy quote asset volume
                    "17928899.62484339" # Can be ignored
                ]
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get("uiKlines", data=params)


    def get_klines(self, **params) -> Dict:
        """Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints#klinecandlestick-data

        :param symbol: required
        :type symbol: str
        :param interval: -
        :type interval: str
        :param limit: - Default 500; max 1000.
        :type limit: int
        :param startTime:
        :type startTime: int
        :param endTime:
        :type endTime: int

        :returns: API response

        .. code-block:: python

            [
                [
                    1499040000000,      # Open time
                    "0.01634790",       # Open
                    "0.80000000",       # High
                    "0.01575800",       # Low
                    "0.01577100",       # Close
                    "148976.11427815",  # Volume
                    1499644799999,      # Close time
                    "2434.19055334",    # Quote asset volume
                    308,                # Number of trades
                    "1756.87402397",    # Taker buy base asset volume
                    "28.46694368",      # Taker buy quote asset volume
                    "17928899.62484339" # Can be ignored
                ]
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get("klines", data=params)

    def _klines(
        self, klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT, **params
    ) -> Dict:
        """Get klines of spot (get_klines) or futures (futures_klines) endpoints.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints#klinecandlestick-data
        https://developers.binance.com/docs/derivatives/option/market-data/Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Index-Price-Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Mark-Price-Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Premium-Index-Kline-Data
        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Index-Price-Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Mark-Price-Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Premium-Index-Kline-Data

        :param klines_type: Historical klines type: SPOT or FUTURES
        :type klines_type: HistoricalKlinesType

        :return: klines, see get_klines

        """
        if "endTime" in params and not params["endTime"]:
            del params["endTime"]

        if HistoricalKlinesType.SPOT == klines_type:
            return self.get_klines(**params)
        elif HistoricalKlinesType.FUTURES == klines_type:
            return self.futures_klines(**params)
        elif HistoricalKlinesType.FUTURES_COIN == klines_type:
            return self.futures_coin_klines(**params)
        elif HistoricalKlinesType.FUTURES_MARK_PRICE == klines_type:
            return self.futures_mark_price_klines(**params)
        elif HistoricalKlinesType.FUTURES_INDEX_PRICE == klines_type:
            return self.futures_index_price_klines(**params)
        elif HistoricalKlinesType.FUTURES_COIN_MARK_PRICE == klines_type:
            return self.futures_coin_mark_price_klines(**params)
        elif HistoricalKlinesType.FUTURES_COIN_INDEX_PRICE == klines_type:
            return self.futures_coin_index_price_klines(**params)
        else:
            raise NotImplementedException(klines_type)

    def _get_earliest_valid_timestamp(
        self,
        symbol,
        interval,
        klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT,
    ):
        """Get the earliest valid open timestamp from Binance

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints#klinecandlestick-data
        https://developers.binance.com/docs/derivatives/option/market-data/Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Index-Price-Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Mark-Price-Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Premium-Index-Kline-Data
        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Index-Price-Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Mark-Price-Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Premium-Index-Kline-Data

        :param symbol: Name of symbol pair e.g. BNBBTC
        :type symbol: str
        :param interval: Binance Kline interval
        :type interval: str
        :param klines_type: Historical klines type: SPOT or FUTURES
        :type klines_type: HistoricalKlinesType

        :return: first valid timestamp

        """
        kline = self._klines(
            klines_type=klines_type,
            symbol=symbol,
            interval=interval,
            limit=1,
            startTime=0,
            endTime=int(time.time() * 1000),
        )
        return kline[0][0]


    def get_historical_klines(
        self,
        symbol,
        interval,
        start_str=None,
        end_str=None,
        limit=None,
        klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT,
    ):
        """Get Historical Klines from Binance

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints#klinecandlestick-data
        https://developers.binance.com/docs/derivatives/option/market-data/Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Index-Price-Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Mark-Price-Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Premium-Index-Kline-Data
        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Index-Price-Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Mark-Price-Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Premium-Index-Kline-Data

        :param symbol: Name of symbol pair e.g. BNBBTC
        :type symbol: str
        :param interval: Binance Kline interval
        :type interval: str
        :param start_str: optional - start date string in UTC format or timestamp in milliseconds
        :type start_str: str|int
        :param end_str: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
        :type end_str: str|int
        :param limit: Default 1000; max 1000.
        :type limit: int
        :param klines_type: Historical klines type: SPOT or FUTURES
        :type klines_type: HistoricalKlinesType

        :return: list of OHLCV values (Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore)

        """
        return self._historical_klines(
            symbol,
            interval,
            start_str=start_str,
            end_str=end_str,
            limit=limit,
            klines_type=klines_type,
        )

    def _historical_klines(
        self,
        symbol,
        interval,
        start_str=None,
        end_str=None,
        limit=None,
        klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT,
    ):
        """Get Historical Klines from Binance (spot or futures)

        See dateparser docs for valid start and end string formats https://dateparser.readthedocs.io/en/latest/

        If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

        :param symbol: Name of symbol pair e.g. BNBBTC
        :type symbol: str
        :param interval: Binance Kline interval
        :type interval: str
        :param start_str: optional - start date string in UTC format or timestamp in milliseconds
        :type start_str: str|int
        :param end_str: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
        :type end_str: None|str|int
        :param limit: Default 1000; max 1000.
        :type limit: int
        :param klines_type: Historical klines type: SPOT or FUTURES
        :type klines_type: HistoricalKlinesType

        :return: list of OHLCV values (Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore)

        """

        initial_limit_set = True
        if limit is None:
            limit = 1000
            initial_limit_set = False

        # init our list
        output_data = []

        # convert interval to useful value in seconds
        timeframe = interval_to_milliseconds(interval)

        # if a start time was passed convert it
        start_ts = convert_ts_str(start_str)

        # establish first available start timestamp
        if start_ts is not None:
            first_valid_ts = self._get_earliest_valid_timestamp(
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
            temp_data = self._klines(
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
            # check if we received less than the required limit and exit the loop
            if not len(temp_data) or len(temp_data) < limit:
                # exit the while loop
                break

            # increment next call by our timeframe
            start_ts = temp_data[-1][0] + timeframe

            # exit loop if we reached end_ts before reaching <limit> klines
            if end_ts and start_ts >= end_ts:
                break

            # sleep after every 3rd call to be kind to the API
            idx += 1
            if idx % 3 == 0:
                time.sleep(1)

        return output_data


    def get_historical_klines_generator(
        self,
        symbol,
        interval,
        start_str=None,
        end_str=None,
        limit=None,
        klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT,
    ):
        """Get Historical Klines generator from Binance

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints#klinecandlestick-data
        https://developers.binance.com/docs/derivatives/option/market-data/Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Index-Price-Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Mark-Price-Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Premium-Index-Kline-Data
        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Index-Price-Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Mark-Price-Kline-Candlestick-Data
        https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Premium-Index-Kline-Data

        :param symbol: Name of symbol pair e.g. BNBBTC
        :type symbol: str
        :param interval: Binance Kline interval
        :type interval: str
        :param start_str: optional - Start date string in UTC format or timestamp in milliseconds
        :type start_str: str|int
        :param end_str: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
        :type end_str: str|int
        :param limit: amount of candles to return per request (default 1000)
        :type limit: int
        :param klines_type: Historical klines type: SPOT or FUTURES
        :type klines_type: HistoricalKlinesType

        :return: generator of OHLCV values

        """

        return self._historical_klines_generator(
            symbol, interval, start_str, end_str, limit, klines_type=klines_type
        )

    def _historical_klines_generator(
        self,
        symbol,
        interval,
        start_str=None,
        end_str=None,
        limit=None,
        klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT,
    ):
        """Get Historical Klines generator from Binance (spot or futures)

        See dateparser docs for valid start and end string formats https://dateparser.readthedocs.io/en/latest/

        If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

        :param symbol: Name of symbol pair e.g. BNBBTC
        :type symbol: str
        :param interval: Binance Kline interval
        :type interval: str
        :param start_str: optional - Start date string in UTC format or timestamp in milliseconds
        :type start_str: str|int
        :param end_str: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
        :type end_str: str|int
        :param klines_type: Historical klines type: SPOT or FUTURES
        :type klines_type: HistoricalKlinesType

        :return: generator of OHLCV values

        """

        initial_limit_set = True
        if limit is None:
            limit = 1000
            initial_limit_set = False

        # convert interval to useful value in seconds
        timeframe = interval_to_milliseconds(interval)

        # if a start time was passed convert it
        start_ts = convert_ts_str(start_str)

        # establish first available start timestamp
        if start_ts is not None:
            first_valid_ts = self._get_earliest_valid_timestamp(
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
            output_data = self._klines(
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

            # set our start timestamp using the last value in the array
            # increment next call by our timeframe
            start_ts = output_data[-1][0] + timeframe

            # exit loop if we reached end_ts before reaching <limit> klines
            if end_ts and start_ts >= end_ts:
                break

            # sleep after every 3rd call to be kind to the API
            idx += 1
            if idx % 3 == 0:
                time.sleep(1)


    def get_avg_price(self, **params):
        """Current average price for a symbol.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints#current-average-price

        :param symbol:
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "mins": 5,
                "price": "9.35751834"
            }
        """
        return self._get("avgPrice", data=params)


    def get_ticker(self, **params):
        """24 hour price change statistics.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints#24hr-ticker-price-change-statistics

        :param symbol:
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "priceChange": "-94.99999800",
                "priceChangePercent": "-95.960",
                "weightedAvgPrice": "0.29628482",
                "prevClosePrice": "0.10002000",
                "lastPrice": "4.00000200",
                "bidPrice": "4.00000000",
                "askPrice": "4.00000200",
                "openPrice": "99.00000000",
                "highPrice": "100.00000000",
                "lowPrice": "0.10000000",
                "volume": "8913.30000000",
                "openTime": 1499783499040,
                "closeTime": 1499869899040,
                "fristId": 28385,   # First tradeId
                "lastId": 28460,    # Last tradeId
                "count": 76         # Trade count
            }

        OR

        .. code-block:: python

            [
                {
                    "priceChange": "-94.99999800",
                    "priceChangePercent": "-95.960",
                    "weightedAvgPrice": "0.29628482",
                    "prevClosePrice": "0.10002000",
                    "lastPrice": "4.00000200",
                    "bidPrice": "4.00000000",
                    "askPrice": "4.00000200",
                    "openPrice": "99.00000000",
                    "highPrice": "100.00000000",
                    "lowPrice": "0.10000000",
                    "volume": "8913.30000000",
                    "openTime": 1499783499040,
                    "closeTime": 1499869899040,
                    "fristId": 28385,   # First tradeId
                    "lastId": 28460,    # Last tradeId
                    "count": 76         # Trade count
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get("ticker/24hr", data=params)


    def get_symbol_ticker(self, **params):
        """Latest price for a symbol or symbols.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints#symbol-price-ticker

        :param symbol:
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "symbol": "LTCBTC",
                "price": "4.00000200"
            }

        OR

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "price": "4.00000200"
                },
                {
                    "symbol": "ETHBTC",
                    "price": "0.07946600"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get("ticker/price", data=params)


    def get_symbol_ticker_window(self, **params):
        """Latest price for a symbol or symbols.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints#rolling-window-price-change-statistics

        :param symbol:
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "symbol": "LTCBTC",
                "price": "4.00000200"
            }

        OR

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "price": "4.00000200"
                },
                {
                    "symbol": "ETHBTC",
                    "price": "0.07946600"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get("ticker", data=params)


    def get_orderbook_ticker(self, **params):
        """Latest price for a symbol or symbols.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints#symbol-order-book-ticker

        :param symbol:
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "symbol": "LTCBTC",
                "bidPrice": "4.00000000",
                "bidQty": "431.00000000",
                "askPrice": "4.00000200",
                "askQty": "9.00000000"
            }

        OR

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "bidPrice": "4.00000000",
                    "bidQty": "431.00000000",
                    "askPrice": "4.00000200",
                    "askQty": "9.00000000"
                },
                {
                    "symbol": "ETHBTC",
                    "bidPrice": "0.07946700",
                    "bidQty": "9.00000000",
                    "askPrice": "100000.00000000",
                    "askQty": "1000.00000000"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get(
            "ticker/bookTicker", data=params
        )

    # Account Endpoints


    def create_order(self, **params):
        """Send in a new order

        Any order with an icebergQty MUST have timeInForce set to GTC.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/trading-endpoints#new-order-trade

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
        :param quoteOrderQty: amount the user wants to spend (when buying) or receive (when selling)
            of the quote asset, applicable to MARKET orders
        :type quoteOrderQty: decimal
        :param price: required
        :type price: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param icebergQty: Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        Response ACK:

        .. code-block:: python

            {
                "symbol":"LTCBTC",
                "orderId": 1,
                "clientOrderId": "myOrder1" # Will be newClientOrderId
                "transactTime": 1499827319559
            }

        Response RESULT:

        .. code-block:: python

            {
                "symbol": "BTCUSDT",
                "orderId": 28,
                "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                "transactTime": 1507725176595,
                "price": "0.00000000",
                "origQty": "10.00000000",
                "executedQty": "10.00000000",
                "cummulativeQuoteQty": "10.00000000",
                "status": "FILLED",
                "timeInForce": "GTC",
                "type": "MARKET",
                "side": "SELL"
            }

        Response FULL:

        .. code-block:: python

            {
                "symbol": "BTCUSDT",
                "orderId": 28,
                "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                "transactTime": 1507725176595,
                "price": "0.00000000",
                "origQty": "10.00000000",
                "executedQty": "10.00000000",
                "cummulativeQuoteQty": "10.00000000",
                "status": "FILLED",
                "timeInForce": "GTC",
                "type": "MARKET",
                "side": "SELL",
                "fills": [
                    {
                        "price": "4000.00000000",
                        "qty": "1.00000000",
                        "commission": "4.00000000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3999.00000000",
                        "qty": "5.00000000",
                        "commission": "19.99500000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3998.00000000",
                        "qty": "2.00000000",
                        "commission": "7.99600000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3997.00000000",
                        "qty": "1.00000000",
                        "commission": "3.99700000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3995.00000000",
                        "qty": "1.00000000",
                        "commission": "3.99500000",
                        "commissionAsset": "USDT"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.SPOT_ORDER_PREFIX + self.uuid22()
        return self._post("order", True, data=params)


    def order_limit(self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params):
        """Send in a new limit order

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/trading-endpoints#new-order-trade

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

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({"type": self.ORDER_TYPE_LIMIT, "timeInForce": timeInForce})
        return self.create_order(**params)


    def order_limit_buy(self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params):
        """Send in a new limit buy order

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/trading-endpoints#new-order-trade

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

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({
            "side": self.SIDE_BUY,
        })
        return self.order_limit(timeInForce=timeInForce, **params)


    def order_limit_sell(self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params):
        """Send in a new limit sell order

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/trading-endpoints#new-order-trade

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

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({"side": self.SIDE_SELL})
        return self.order_limit(timeInForce=timeInForce, **params)


    def order_market(self, **params):
        """Send in a new market order

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/trading-endpoints#new-order-trade

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

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({"type": self.ORDER_TYPE_MARKET})
        return self.create_order(**params)


    def order_market_buy(self, **params):
        """Send in a new market buy order

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/trading-endpoints#new-order-trade

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

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({"side": self.SIDE_BUY})
        return self.order_market(**params)


    def order_market_sell(self, **params):
        """Send in a new market sell order

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/trading-endpoints#new-order-trade

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

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({"side": self.SIDE_SELL})
        return self.order_market(**params)


    def create_oco_order(self, **params):
        """Send in an one-cancels-the-other (OCO) pair, where activation of one order immediately cancels the other.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/trading-endpoints#new-order-list---oco-trade

        An OCO has 2 orders called the above order and below order.
        One of the orders must be a LIMIT_MAKER/TAKE_PROFIT/TAKE_PROFIT_LIMIT order and the other must be STOP_LOSS or STOP_LOSS_LIMIT order.

        Price restrictions:
        If the OCO is on the SELL side:
            LIMIT_MAKER/TAKE_PROFIT_LIMIT price > Last Traded Price > STOP_LOSS/STOP_LOSS_LIMIT stopPrice
            TAKE_PROFIT stopPrice > Last Traded Price > STOP_LOSS/STOP_LOSS_LIMIT stopPrice
        If the OCO is on the BUY side:
            LIMIT_MAKER/TAKE_PROFIT_LIMIT price < Last Traded Price < stopPrice
            TAKE_PROFIT stopPrice < Last Traded Price < STOP_LOSS/STOP_LOSS_LIMIT stopPrice

        Weight: 1

        :param symbol: required
        :type symbol: str
        :param listClientOrderId: Arbitrary unique ID among open order lists. Automatically generated if not sent.
        :type listClientOrderId: str
        :param side: required - BUY or SELL
        :type side: str
        :param quantity: required - Quantity for both orders of the order list
        :type quantity: decimal
        :param aboveType: required - STOP_LOSS_LIMIT, STOP_LOSS, LIMIT_MAKER, TAKE_PROFIT, TAKE_PROFIT_LIMIT
        :type aboveType: str
        :param aboveClientOrderId: Arbitrary unique ID among open orders for the above order
        :type aboveClientOrderId: str
        :param aboveIcebergQty: Note that this can only be used if aboveTimeInForce is GTC
        :type aboveIcebergQty: decimal
        :param abovePrice: Can be used if aboveType is STOP_LOSS_LIMIT, LIMIT_MAKER, or TAKE_PROFIT_LIMIT
        :type abovePrice: decimal
        :param aboveStopPrice: Can be used if aboveType is STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT
        :type aboveStopPrice: decimal
        :param aboveTrailingDelta: See Trailing Stop order FAQ
        :type aboveTrailingDelta: int
        :param aboveTimeInForce: Required if aboveType is STOP_LOSS_LIMIT or TAKE_PROFIT_LIMIT
        :type aboveTimeInForce: str
        :param aboveStrategyId: Arbitrary numeric value identifying the above order within an order strategy
        :type aboveStrategyId: int
        :param aboveStrategyType: Arbitrary numeric value identifying the above order strategy (>= 1000000)
        :type aboveStrategyType: int
        :param belowType: required - STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT
        :type belowType: str
        :param belowClientOrderId: Arbitrary unique ID among open orders for the below order
        :type belowClientOrderId: str
        :param belowIcebergQty: Note that this can only be used if belowTimeInForce is GTC
        :type belowIcebergQty: decimal
        :param belowPrice: Can be used if belowType is STOP_LOSS_LIMIT, LIMIT_MAKER, or TAKE_PROFIT_LIMIT
        :type belowPrice: decimal
        :param belowStopPrice: Can be used if belowType is STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT or TAKE_PROFIT_LIMIT
        :type belowStopPrice: decimal
        :param belowTrailingDelta: See Trailing Stop order FAQ
        :type belowTrailingDelta: int
        :param belowTimeInForce: Required if belowType is STOP_LOSS_LIMIT or TAKE_PROFIT_LIMIT
        :type belowTimeInForce: str
        :param belowStrategyId: Arbitrary numeric value identifying the below order within an order strategy
        :type belowStrategyId: int
        :param belowStrategyType: Arbitrary numeric value identifying the below order strategy (>= 1000000)
        :type belowStrategyType: int
        :param newOrderRespType: Select response format: ACK, RESULT, FULL
        :type newOrderRespType: str
        :param selfTradePreventionMode: The allowed enums is dependent on what is configured on the symbol
        :type selfTradePreventionMode: str
        :param recvWindow: The value cannot be greater than 60000
        :type recvWindow: int
        :param timestamp: required
        :type timestamp: int

        :returns: API response

            {
                "orderListId": 1,
                "contingencyType": "OCO",
                "listStatusType": "EXEC_STARTED",
                "listOrderStatus": "EXECUTING",
                "listClientOrderId": "lH1YDkuQKWiXVXHPSKYEIp",
                "transactionTime": 1710485608839,
                "symbol": "LTCBTC",
                "orders": [
                    {
                        "symbol": "LTCBTC",
                        "orderId": 10,
                        "clientOrderId": "44nZvqpemY7sVYgPYbvPih"
                    },
                    {
                        "symbol": "LTCBTC",
                        "orderId": 11,
                        "clientOrderId": "NuMp0nVYnciDiFmVqfpBqK"
                    }
                ],
                "orderReports": [
                    {
                        "symbol": "LTCBTC",
                        "orderId": 10,
                        "orderListId": 1,
                        "clientOrderId": "44nZvqpemY7sVYgPYbvPih",
                        "transactTime": 1710485608839,
                        "price": "1.00000000",
                        "origQty": "5.00000000",
                        "executedQty": "0.00000000",
                        "origQuoteOrderQty": "0.000000",
                        "cummulativeQuoteQty": "0.00000000",
                        "status": "NEW",
                        "timeInForce": "GTC",
                        "type": "STOP_LOSS_LIMIT",
                        "side": "SELL",
                        "stopPrice": "1.00000000",
                        "workingTime": -1,
                        "icebergQty": "1.00000000",
                        "selfTradePreventionMode": "NONE"
                    },
                    {
                        "symbol": "LTCBTC",
                        "orderId": 11,
                        "orderListId": 1,
                        "clientOrderId": "NuMp0nVYnciDiFmVqfpBqK",
                        "transactTime": 1710485608839,
                        "price": "3.00000000",
                        "origQty": "5.00000000",
                        "executedQty": "0.00000000",
                        "origQuoteOrderQty": "0.000000",
                        "cummulativeQuoteQty": "0.00000000",
                        "status": "NEW",
                        "timeInForce": "GTC",
                        "type": "LIMIT_MAKER",
                        "side": "SELL",
                        "workingTime": 1710485608839,
                        "selfTradePreventionMode": "NONE"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException,
                BinanceOrderMinAmountException, BinanceOrderMinPriceException,
                BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
                BinanceOrderInactiveSymbolException

        """
        if "listClientOrderId" not in params:
            params["listClientOrderId"] = self.SPOT_ORDER_PREFIX + self.uuid22()
        return self._post("orderList/oco", True, data=params)


    def order_oco_buy(self, **params):
        """Send in a new OCO buy order

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/trading-endpoints#new-order-list---oco-trade

        :param symbol: required
        :type symbol: str
        :param listClientOrderId: A unique id for the list order. Automatically generated if not sent.
        :type listClientOrderId: str
        :param quantity: required
        :type quantity: decimal
        :param limitClientOrderId: A unique id for the limit order. Automatically generated if not sent.
        :type limitClientOrderId: str
        :param price: required
        :type price: str
        :param limitIcebergQty: Used to make the LIMIT_MAKER leg an iceberg order.
        :type limitIcebergQty: decimal
        :param stopClientOrderId: A unique id for the stop order. Automatically generated if not sent.
        :type stopClientOrderId: str
        :param stopPrice: required
        :type stopPrice: str
        :param stopLimitPrice: If provided, stopLimitTimeInForce is required.
        :type stopLimitPrice: str
        :param stopIcebergQty: Used with STOP_LOSS_LIMIT leg to make an iceberg order.
        :type stopIcebergQty: decimal
        :param stopLimitTimeInForce: Valid values are GTC/FOK/IOC.
        :type stopLimitTimeInForce: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See OCO order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({"side": self.SIDE_BUY})
        return self.create_oco_order(**params)


    def order_oco_sell(self, **params):
        """Send in a new OCO sell order

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/trading-endpoints#new-order-list---oco-trade

        :param symbol: required
        :type symbol: str
        :param listClientOrderId: A unique id for the list order. Automatically generated if not sent.
        :type listClientOrderId: str
        :param quantity: required
        :type quantity: decimal
        :param limitClientOrderId: A unique id for the limit order. Automatically generated if not sent.
        :type limitClientOrderId: str
        :param price: required
        :type price: str
        :param limitIcebergQty: Used to make the LIMIT_MAKER leg an iceberg order.
        :type limitIcebergQty: decimal
        :param stopClientOrderId: A unique id for the stop order. Automatically generated if not sent.
        :type stopClientOrderId: str
        :param stopPrice: required
        :type stopPrice: str
        :param stopLimitPrice: If provided, stopLimitTimeInForce is required.
        :type stopLimitPrice: str
        :param stopIcebergQty: Used with STOP_LOSS_LIMIT leg to make an iceberg order.
        :type stopIcebergQty: decimal
        :param stopLimitTimeInForce: Valid values are GTC/FOK/IOC.
        :type stopLimitTimeInForce: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See OCO order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({"side": self.SIDE_SELL})
        return self.create_oco_order(**params)


    def create_test_order(self, **params):
        """Test new order creation and signature/recvWindow long. Creates and validates a new order but does not send it into the matching engine.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/trading-endpoints#test-new-order-trade

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

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException


        """
        return self._post("order/test", True, data=params)


    def get_order(self, **params):
        """Check an order's status. Either orderId or origClientOrderId must be sent.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/account-endpoints#query-order-user_data

        :param symbol: required
        :type symbol: str
        :param orderId: The unique order id
        :type orderId: int
        :param origClientOrderId: optional
        :type origClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "symbol": "LTCBTC",
                "orderId": 1,
                "clientOrderId": "myOrder1",
                "price": "0.1",
                "origQty": "1.0",
                "executedQty": "0.0",
                "status": "NEW",
                "timeInForce": "GTC",
                "type": "LIMIT",
                "side": "BUY",
                "stopPrice": "0.0",
                "icebergQty": "0.0",
                "time": 1499827319559
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get("order", True, data=params)


    def get_all_orders(self, **params):
        """Get all account orders; active, canceled, or filled.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/account-endpoints#all-orders-user_data

        :param symbol: required
        :type symbol: str
        :param orderId: The unique order id
        :type orderId: int
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param limit: Default 500; max 1000.
        :type limit: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "orderId": 1,
                    "clientOrderId": "myOrder1",
                    "price": "0.1",
                    "origQty": "1.0",
                    "executedQty": "0.0",
                    "status": "NEW",
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "side": "BUY",
                    "stopPrice": "0.0",
                    "icebergQty": "0.0",
                    "time": 1499827319559
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get("allOrders", True, data=params)


    def cancel_order(self, **params):
        """Cancel an active order. Either orderId or origClientOrderId must be sent.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/trading-endpoints#cancel-order-trade

        :param symbol: required
        :type symbol: str
        :param orderId: The unique order id
        :type orderId: int
        :param origClientOrderId: optional
        :type origClientOrderId: str
        :param newClientOrderId: Used to uniquely identify this cancel. Automatically generated by default.
        :type newClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "symbol": "LTCBTC",
                "origClientOrderId": "myOrder1",
                "orderId": 1,
                "clientOrderId": "cancelMyOrder1"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._delete("order", True, data=params)


    def cancel_all_open_orders(self, **params):
        """
        Cancel all open orders on a symbol.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/trading-endpoints#cancel-all-open-orders-on-a-symbol-trade

        :param symbol: required
        :type symbol: str

        :returns: API response
        """
        return self._delete("openOrders", True, data=params)


    def cancel_replace_order(self, **params):
        """Cancels an existing order and places a new order on the same symbol.

        Filters and Order Count are evaluated before the processing of the cancellation and order placement occurs.

        A new order that was not attempted (i.e. when newOrderResult: NOT_ATTEMPTED), will still increase the order count by 1.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/trading-endpoints#cancel-an-existing-order-and-send-a-new-order-trade

        :param symbol: required
        :type symbol: str
        :param side: required
        :type side: enum
        :param type: required
        :type type: enum
        :param cancelReplaceMode: required - STOP_ON_FAILURE or ALLOW_FAILURE
        :type cancelReplaceMode: enum
        :param timeInForce: optional
        :type timeInForce: enum
        :param quantity: optional
        :type quantity: decimal
        :param quoteOrderQty: optional
        :type quoteOrderQty: decimal
        :param price: optional
        :type price: decimal
        :param cancelNewClientOrderId: optional - Used to uniquely identify this cancel. Automatically generated by default.
        :type cancelNewClientOrderId: str
        :param cancelOrigClientOrderId: optional - Either the cancelOrigClientOrderId or cancelOrderId must be provided. If both are provided, cancelOrderId takes precedence.
        :type cancelOrigClientOrderId: str
        :param cancelOrderId: optional - Either the cancelOrigClientOrderId or cancelOrderId must be provided. If both are provided, cancelOrderId takes precedence.
        :type cancelOrderId: long
        :param newClientOrderId: optional - Used to identify the new order.
        :type newClientOrderId: str
        :param strategyId: optional
        :type strategyId: int
        :param strategyType: optional - The value cannot be less than 1000000.
        :type strategyType: int
        :param stopPrice: optional
        :type stopPrice: decimal
        :param trailingDelta: optional
        :type trailingDelta: long
        :param icebergQty: optional
        :type icebergQty: decimal
        :param newOrderRespType: optional - ACK, RESULT or FULL. MARKET and LIMIT orders types default to FULL; all other orders default to ACK
        :type newOrderRespType: enum
        :param selfTradePreventionMode: optional - EXPIRE_TAKER, EXPIRE_MAKER, EXPIRE_BOTH or NONE.
        :type selfTradePreventionMode: enum
        :param cancelRestrictions: optional - ONLY_NEW or ONLY_PARTIALLY_FILLED
        :type cancelRestrictions: enum
        :param recvWindow: optional - The value cannot be greater than 60000
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            //Both the cancel order placement and new order placement succeeded.
            {
                "cancelResult": "SUCCESS",
                "newOrderResult": "SUCCESS",
                "cancelResponse": {
                    "symbol": "BTCUSDT",
                    "origClientOrderId": "DnLo3vTAQcjha43lAZhZ0y",
                    "orderId": 9,
                    "orderListId": -1,
                    "clientOrderId": "osxN3JXAtJvKvCqGeMWMVR",
                    "transactTime": 1684804350068,
                    "price": "0.01000000",
                    "origQty": "0.000100",
                    "executedQty": "0.00000000",
                    "cummulativeQuoteQty": "0.00000000",
                    "status": "CANCELED",
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "side": "SELL",
                    "selfTradePreventionMode": "NONE"
                },
                "newOrderResponse": {
                    "symbol": "BTCUSDT",
                    "orderId": 10,
                    "orderListId": -1,
                    "clientOrderId": "wOceeeOzNORyLiQfw7jd8S",
                    "transactTime": 1652928801803,
                    "price": "0.02000000",
                    "origQty": "0.040000",
                    "executedQty": "0.00000000",
                    "cummulativeQuoteQty": "0.00000000",
                    "status": "NEW",
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "side": "BUY",
                    "workingTime": 1669277163808,
                    "fills": [],
                    "selfTradePreventionMode": "NONE"

                }
            }
        Similar to POST /api/v3/order, additional mandatory parameters are determined by type.

        Response format varies depending on whether the processing of the message succeeded, partially succeeded, or failed.

        :raises: BinanceRequestException, BinanceAPIException

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.SPOT_ORDER_PREFIX + self.uuid22()
        return self._post("order/cancelReplace", True, data=params)


    def get_open_orders(self, **params):
        """Get all open orders on a symbol.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/account-endpoints#current-open-orders-user_data

        :param symbol: optional
        :type symbol: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "orderId": 1,
                    "clientOrderId": "myOrder1",
                    "price": "0.1",
                    "origQty": "1.0",
                    "executedQty": "0.0",
                    "status": "NEW",
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "side": "BUY",
                    "stopPrice": "0.0",
                    "icebergQty": "0.0",
                    "time": 1499827319559
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get("openOrders", True, data=params)


    def get_open_oco_orders(self, **params):
        """Get all open orders on a symbol.
        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/account-endpoints#query-open-order-lists-user_data
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int
        :returns: API response
        .. code-block:: python
            [
                {
                    "orderListId": 31,
                    "contingencyType": "OCO",
                    "listStatusType": "EXEC_STARTED",
                    "listOrderStatus": "EXECUTING",
                    "listClientOrderId": "wuB13fmulKj3YjdqWEcsnp",
                    "transactionTime": 1565246080644,
                    "symbol": "LTCBTC",
                    "orders": [
                        {
                            "symbol": "LTCBTC",
                            "orderId": 4,
                            "clientOrderId": "r3EH2N76dHfLoSZWIUw1bT"
                        },
                        {
                            "symbol": "LTCBTC",
                            "orderId": 5,
                            "clientOrderId": "Cv1SnyPD3qhqpbjpYEHbd2"
                        }
                    ]
                }
            ]
        :raises: BinanceRequestException, BinanceAPIException
        """
        return self._get("openOrderList", True, data=params)

    # User Stream Endpoints

    def get_account(self, **params):
        """Get current account information.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/account-endpoints#account-information-user_data

        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "makerCommission": 15,
                "takerCommission": 15,
                "buyerCommission": 0,
                "sellerCommission": 0,
                "canTrade": true,
                "canWithdraw": true,
                "canDeposit": true,
                "balances": [
                    {
                        "asset": "BTC",
                        "free": "4723846.89208129",
                        "locked": "0.00000000"
                    },
                    {
                        "asset": "LTC",
                        "free": "4763368.68006011",
                        "locked": "0.00000000"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get("account", True, data=params)


    def get_asset_balance(self, asset=None, **params):
        """Get current asset balance.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/account-endpoints#account-information-user_data

        :param asset: optional - the asset to get the balance of
        :type asset: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: dictionary or None if not found

        .. code-block:: python

            {
                "asset": "BTC",
                "free": "4723846.89208129",
                "locked": "0.00000000"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        res = self.get_account(**params)
        # find asset balance in list of balances
        if "balances" in res:
            if asset:
                for bal in res["balances"]:
                    if bal["asset"].lower() == asset.lower():
                        return bal
            else:
                return res["balances"]
        return None


    def get_my_trades(self, **params):
        """Get trades for a specific symbol.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/account-endpoints#account-trade-list-user_data

        :param symbol: required
        :type symbol: str
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param limit: Default 500; max 1000.
        :type limit: int
        :param fromId: TradeId to fetch from. Default gets most recent trades.
        :type fromId: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "id": 28457,
                    "price": "4.00000100",
                    "qty": "12.00000000",
                    "commission": "10.10000000",
                    "commissionAsset": "BNB",
                    "time": 1499865549590,
                    "isBuyer": true,
                    "isMaker": false,
                    "isBestMatch": true
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get("myTrades", True, data=params)


    def get_current_order_count(self, **params):
        """Displays the user's current order count usage for all intervals.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/account-endpoints#query-unfilled-order-count-user_data

        :returns: API response

        .. code-block:: python
            [

                {
                    "rateLimitType": "ORDERS",
                    "interval": "SECOND",
                    "intervalNum": 10,
                    "limit": 10000,
                    "count": 0
                },
                {
                    "rateLimitType": "ORDERS",
                    "interval": "DAY",
                    "intervalNum": 1,
                    "limit": 20000,
                    "count": 0
                }
            ]

        """
        return self._get("rateLimit/order", True, data=params)


    def get_prevented_matches(self, **params):
        """Displays the list of orders that were expired because of STP.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/account-endpoints#query-prevented-matches-user_data

        :param symbol: required
        :type symbol: str
        :param preventedMatchId: optional
        :type preventedMatchId: int
        :param orderId: optional
        :type orderId: int
        :param fromPreventedMatchId: optional
        :type fromPreventedMatchId: int
        :param limit: optional, Default: 500; Max: 1000
        :type limit: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python
            [
                {
                    "symbol": "BTCUSDT",
                    "preventedMatchId": 1,
                    "takerOrderId": 5,
                    "makerOrderId": 3,
                    "tradeGroupId": 1,
                    "selfTradePreventionMode": "EXPIRE_MAKER",
                    "price": "1.100000",
                    "makerPreventedQuantity": "1.300000",
                    "transactTime": 1669101687094
                }
            ]
        """
        return self._get("myPreventedMatches", True, data=params)


    def get_allocations(self, **params):
        """Retrieves allocations resulting from SOR order placement.

        https://developers.binance.com/docs/binance-spot-api-docs/rest-api/account-endpoints#query-allocations-user_data

        :param symbol: required
        :type symbol: str
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param fromAllocationId: optional
        :type fromAllocationId: int
        :param orderId: optional
        :type orderId: int
        :param limit: optional, Default: 500; Max: 1000
        :type limit: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python
            [
                {
                    "symbol": "BTCUSDT",
                    "allocationId": 0,
                    "allocationType": "SOR",
                    "orderId": 1,
                    "orderListId": -1,
                    "price": "1.00000000",
                    "qty": "5.00000000",
                    "quoteQty": "5.00000000",
                    "commission": "0.00000000",
                    "commissionAsset": "BTC",
                    "time": 1687506878118,
                    "isBuyer": true,
                    "isMaker": false,
                    "isAllocator": false
                }
            ]
        """
        return self._get("myAllocations", True, data=params)


    def get_system_status(self):
        """Get system status detail.

        https://developers.binance.com/docs/wallet/others/system-status

        :returns: API response

        .. code-block:: python

            {
                "status": 0,        # 0: normal, 1:system maintenance
                "msg": "normal"     # normal or System maintenance.
            }

        :raises: BinanceAPIException

        """
        return self._request_margin_api("get", "system/status")


    def get_account_status(self, version=1, **params):
        """Get account status detail.

        https://binance-docs.github.io/apidocs/spot/en/#account-status-sapi-user_data
        https://developers.binance.com/docs/wallet/account/account-status
        :param version: the api version
        :param version: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "data": "Normal"
            }

        """
        if self.tld == "us":
            path = "accountStatus"
        else:
            path = "account/status"
        return self._request_margin_api("get", path, True, version, data=params)


    def get_account_api_trading_status(self, **params):
        """Fetch account api trading status detail.

        https://developers.binance.com/docs/wallet/account/account-api-trading-status

        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "data": {          // API trading status detail
                    "isLocked": false,   // API trading function is locked or not
                    "plannedRecoverTime": 0,  // If API trading function is locked, this is the planned recover time
                    "triggerCondition": {
                            "GCR": 150,  // Number of GTC orders
                            "IFER": 150, // Number of FOK/IOC orders
                            "UFR": 300   // Number of orders
                    },
                    "indicators": {  // The indicators updated every 30 seconds
                         "BTCUSDT": [  // The symbol
                            {
                                "i": "UFR",  // Unfilled Ratio (UFR)
                                "c": 20,     // Count of all orders
                                "v": 0.05,   // Current UFR value
                                "t": 0.995   // Trigger UFR value
                            },
                            {
                                "i": "IFER", // IOC/FOK Expiration Ratio (IFER)
                                "c": 20,     // Count of FOK/IOC orders
                                "v": 0.99,   // Current IFER value
                                "t": 0.99    // Trigger IFER value
                            },
                            {
                                "i": "GCR",  // GTC Cancellation Ratio (GCR)
                                "c": 20,     // Count of GTC orders
                                "v": 0.99,   // Current GCR value
                                "t": 0.99    // Trigger GCR value
                            }
                        ],
                        "ETHUSDT": [
                            {
                                "i": "UFR",
                                "c": 20,
                                "v": 0.05,
                                "t": 0.995
                            },
                            {
                                "i": "IFER",
                                "c": 20,
                                "v": 0.99,
                                "t": 0.99
                            },
                            {
                                "i": "GCR",
                                "c": 20,
                                "v": 0.99,
                                "t": 0.99
                            }
                        ]
                    },
                    "updateTime": 1547630471725
                }
            }

        """
        return self._request_margin_api(
            "get", "account/apiTradingStatus", True, data=params
        )


    def get_account_api_permissions(self, **params):
        """Fetch api key permissions.

        https://developers.binance.com/docs/wallet/account/api-key-permission

        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
               "ipRestrict": false,
               "createTime": 1623840271000,
               "enableWithdrawals": false,   // This option allows you to withdraw via API. You must apply the IP Access Restriction filter in order to enable withdrawals
               "enableInternalTransfer": true,  // This option authorizes this key to transfer funds between your master account and your sub account instantly
               "permitsUniversalTransfer": true,  // Authorizes this key to be used for a dedicated universal transfer API to transfer multiple supported currencies. Each business's own transfer API rights are not affected by this authorization
               "enableVanillaOptions": false,  //  Authorizes this key to Vanilla options trading
               "enableReading": true,
               "enableFutures": false,  //  API Key created before your futures account opened does not support futures API service
               "enableMargin": false,   //  This option can be adjusted after the Cross Margin account transfer is completed
               "enableSpotAndMarginTrading": false, // Spot and margin trading
               "tradingAuthorityExpirationTime": 1628985600000  // Expiration time for spot and margin trading permission
            }

        """
        return self._request_margin_api(
            "get", "account/apiRestrictions", True, data=params
        )


    def get_dust_assets(self, **params):
        """Get assets that can be converted into BNB

        https://developers.binance.com/docs/wallet/asset/assets-can-convert-bnb

        :returns: API response

        .. code-block:: python

            {
                "details": [
                    {
                        "asset": "ADA",
                        "assetFullName": "ADA",
                        "amountFree": "6.21",   //Convertible amount
                        "toBTC": "0.00016848",  //BTC amount
                        "toBNB": "0.01777302",  //BNB amount(Not deducted commission fee)
                        "toBNBOffExchange": "0.01741756", //BNB amount(Deducted commission fee)
                        "exchange": "0.00035546" //Commission fee
                    }
                ],
                "totalTransferBtc": "0.00016848",
                "totalTransferBNB": "0.01777302",
                "dribbletPercentage": "0.02"     //Commission fee
            }

        """
        return self._request_margin_api("post", "asset/dust-btc", True, data=params)


    def get_dust_log(self, **params):
        """Get log of small amounts exchanged for BNB.

        https://developers.binance.com/docs/wallet/asset/dust-log

        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "total": 8,   //Total counts of exchange
                "userAssetDribblets": [
                    {
                        "totalTransferedAmount": "0.00132256",   // Total transfered BNB amount for this exchange.
                        "totalServiceChargeAmount": "0.00002699",    //Total service charge amount for this exchange.
                        "transId": 45178372831,
                        "userAssetDribbletDetails": [           //Details of  this exchange.
                            {
                                "transId": 4359321,
                                "serviceChargeAmount": "0.000009",
                                "amount": "0.0009",
                                "operateTime": 1615985535000,
                                "transferedAmount": "0.000441",
                                "fromAsset": "USDT"
                            },
                            {
                                "transId": 4359321,
                                "serviceChargeAmount": "0.00001799",
                                "amount": "0.0009",
                                "operateTime": "2018-05-03 17:07:04",
                                "transferedAmount": "0.00088156",
                                "fromAsset": "ETH"
                            }
                        ]
                    },
                    {
                        "operateTime":1616203180000,
                        "totalTransferedAmount": "0.00058795",
                        "totalServiceChargeAmount": "0.000012",
                        "transId": 4357015,
                        "userAssetDribbletDetails": [
                            {
                                "transId": 4357015,
                                "serviceChargeAmount": "0.00001"
                                "amount": "0.001",
                                "operateTime": 1616203180000,
                                "transferedAmount": "0.00049",
                                "fromAsset": "USDT"
                            },
                            {
                                "transId": 4357015,
                                "serviceChargeAmount": "0.000002"
                                "amount": "0.0001",
                                "operateTime": 1616203180000,
                                "transferedAmount": "0.00009795",
                                "fromAsset": "ETH"
                            }
                        ]
                    }
                ]
            }

        """
        return self._request_margin_api("get", "asset/dribblet", True, data=params)


    def transfer_dust(self, **params):
        """Convert dust assets to BNB.

        https://developers.binance.com/docs/wallet/asset/dust-transfer

        :param asset: The asset being converted. e.g: 'ONE'
        :type asset: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code-block:: python

            result = client.transfer_dust(asset='ONE')

        :returns: API response

        .. code-block:: python

            {
                "totalServiceCharge":"0.02102542",
                "totalTransfered":"1.05127099",
                "transferResult":[
                    {
                        "amount":"0.03000000",
                        "fromAsset":"ETH",
                        "operateTime":1563368549307,
                        "serviceChargeAmount":"0.00500000",
                        "tranId":2970932918,
                        "transferedAmount":"0.25000000"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api("post", "asset/dust", True, data=params)


    def get_asset_dividend_history(self, **params):
        """Query asset dividend record.

        https://developers.binance.com/docs/wallet/asset/assets-divided-record

        :param asset: optional
        :type asset: str
        :param startTime: optional
        :type startTime: long
        :param endTime: optional
        :type endTime: long
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code-block:: python

            result = client.get_asset_dividend_history()

        :returns: API response

        .. code-block:: python

            {
                "rows":[
                    {
                        "amount":"10.00000000",
                        "asset":"BHFT",
                        "divTime":1563189166000,
                        "enInfo":"BHFT distribution",
                        "tranId":2968885920
                    },
                    {
                        "amount":"10.00000000",
                        "asset":"BHFT",
                        "divTime":1563189165000,
                        "enInfo":"BHFT distribution",
                        "tranId":2968885920
                    }
                ],
                "total":2
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api("get", "asset/assetDividend", True, data=params)


    def make_universal_transfer(self, **params):
        """User Universal Transfer

        https://developers.binance.com/docs/wallet/asset/user-universal-transfer

        :param type: required
        :type type: str (ENUM)
        :param asset: required
        :type asset: str
        :param amount: required
        :type amount: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code-block:: python

            transfer_status = client.make_universal_transfer(params)

        :returns: API response

        .. code-block:: python

            {
                "tranId":13526853623
            }


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "post", "asset/transfer", signed=True, data=params
        )


    def query_universal_transfer_history(self, **params):
        """Query User Universal Transfer History

        https://developers.binance.com/docs/wallet/asset/query-user-universal-transfer

        :param type: required
        :type type: str (ENUM)
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param current: optional - Default 1
        :type current: int
        :param size: required - Default 10, Max 100
        :type size: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code-block:: python

            transfer_status = client.query_universal_transfer_history(params)

        :returns: API response

        .. code-block:: python

            {
                "total":2,
                "rows":[
                    {
                        "asset":"USDT",
                        "amount":"1",
                        "type":"MAIN_UMFUTURE"
                        "status": "CONFIRMED",
                        "tranId": 11415955596,
                        "timestamp":1544433328000
                    },
                    {
                        "asset":"USDT",
                        "amount":"2",
                        "type":"MAIN_UMFUTURE",
                        "status": "CONFIRMED",
                        "tranId": 11366865406,
                        "timestamp":1544433328000
                    }
                ]
            }


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "asset/transfer", signed=True, data=params
        )


    def get_trade_fee(self, **params):
        """Get trade fee.

        https://developers.binance.com/docs/wallet/asset/trade-fee

        :param symbol: optional
        :type symbol: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "symbol": "ADABNB",
                    "makerCommission": "0.001",
                    "takerCommission": "0.001"
                },
                {
                    "symbol": "BNBBTC",
                    "makerCommission": "0.001",
                    "takerCommission": "0.001"
                }
            ]

        """
        if self.tld == "us":
            endpoint = "asset/query/trading-fee"
        else:
            endpoint = "asset/tradeFee"

        return self._request_margin_api("get", endpoint, True, data=params)


    def get_asset_details(self, **params):
        """Fetch details on assets.

        https://developers.binance.com/docs/wallet/asset

        :param asset: optional
        :type asset: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                    "CTR": {
                        "minWithdrawAmount": "70.00000000", //min withdraw amount
                        "depositStatus": false,//deposit status (false if ALL of networks' are false)
                        "withdrawFee": 35, // withdraw fee
                        "withdrawStatus": true, //withdraw status (false if ALL of networks' are false)
                        "depositTip": "Delisted, Deposit Suspended" //reason
                    },
                    "SKY": {
                        "minWithdrawAmount": "0.02000000",
                        "depositStatus": true,
                        "withdrawFee": 0.01,
                        "withdrawStatus": true
                    }
            }

        """
        return self._request_margin_api("get", "asset/assetDetail", True, data=params)


    def get_spot_delist_schedule(self, **params):
        """Get symbols delist schedule for spot

        https://developers.binance.com/docs/wallet/others/delist-schedule

        :param recvWindow: optional - the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python
            [
                {
                    "delistTime": 1686161202000,
                    "symbols": [
                        "ADAUSDT",
                        "BNBUSDT"
                    ]
                },
                {
                    "delistTime": 1686222232000,
                    "symbols": [
                        "ETHUSDT"
                    ]
                }
            ]
        """
        return self._request_margin_api(
            "get", "spot/delist-schedule", True, data=params
        )

    # Withdraw Endpoints


    def withdraw(self, **params):
        """Submit a withdraw request.

        https://developers.binance.com/docs/wallet/capital/withdraw

        Assumptions:

        - You must have Withdraw permissions enabled on your API key
        - You must have withdrawn to the address specified through the website and approved the transaction via email

        :param coin: required
        :type coin: str
        :param withdrawOrderId: optional - client id for withdraw
        :type withdrawOrderId: str
        :param network: optional
        :type network: str
        :param address: optional
        :type address: str
        :type addressTag: optional - Secondary address identifier for coins like XRP,XMR etc.
        :param amount: required
        :type amount: decimal
        :param transactionFeeFlag: required - When making internal transfer, true for returning the fee to the destination account; false for returning the fee back to the departure account. Default false.
        :type transactionFeeFlag: bool
        :param name: optional - Description of the address, default asset value passed will be used
        :type name: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "id":"7213fea8e94b4a5593d507237e5a555b"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "post", "capital/withdraw/apply", True, data=params
        )


    def get_deposit_history(self, **params):
        """Fetch deposit history.

        https://developers.binance.com/docs/wallet/capital/deposite-history

        :param coin: optional
        :type coin: str
        :type status: optional - 0(0:pending,1:success) optional
        :type status: int
        :param startTime: optional
        :type startTime: long
        :param endTime: optional
        :type endTime: long
        :param offset: optional - default:0
        :type offset: long
        :param limit: optional
        :type limit: long
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "amount":"0.00999800",
                    "coin":"PAXG",
                    "network":"ETH",
                    "status":1,
                    "address":"0x788cabe9236ce061e5a892e1a59395a81fc8d62c",
                    "addressTag":"",
                    "txId":"0xaad4654a3234aa6118af9b4b335f5ae81c360b2394721c019b5d1e75328b09f3",
                    "insertTime":1599621997000,
                    "transferType":0,
                    "confirmTimes":"12/12"
                },
                {
                    "amount":"0.50000000",
                    "coin":"IOTA",
                    "network":"IOTA",
                    "status":1,
                    "address":"SIZ9VLMHWATXKV99LH99CIGFJFUMLEHGWVZVNNZXRJJVWBPHYWPPBOSDORZ9EQSHCZAMPVAPGFYQAUUV9DROOXJLNW",
                    "addressTag":"",
                    "txId":"ESBFVQUTPIWQNJSPXFNHNYHSQNTGKRVKPRABQWTAXCDWOAKDKYWPTVG9BGXNVNKTLEJGESAVXIKIZ9999",
                    "insertTime":1599620082000,
                    "transferType":0,
                    "confirmTimes":"1/1"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "capital/deposit/hisrec", True, data=params
        )


    def get_withdraw_history(self, **params):
        """Fetch withdraw history.

        https://developers.binance.com/docs/wallet/capital/withdraw-history

        :param coin: optional
        :type coin: str
        :type status: 0(0:Email Sent,1:Cancelled 2:Awaiting Approval 3:Rejected 4:Processing 5:Failure 6Completed) optional
        :type status: int
        :param offset: optional - default:0
        :type offset: int
        :param limit: optional
        :type limit: int
        :param startTime: optional - Default: 90 days from current timestamp
        :type startTime: int
        :param endTime: optional - Default: present timestamp
        :type endTime: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "address": "0x94df8b352de7f46f64b01d3666bf6e936e44ce60",
                    "amount": "8.91000000",
                    "applyTime": "2019-10-12 11:12:02",
                    "coin": "USDT",
                    "id": "b6ae22b3aa844210a7041aee7589627c",
                    "withdrawOrderId": "WITHDRAWtest123", // will not be returned if there's no withdrawOrderId for this withdraw.
                    "network": "ETH",
                    "transferType": 0,   // 1 for internal transfer, 0 for external transfer
                    "status": 6,
                    "txId": "0xb5ef8c13b968a406cc62a93a8bd80f9e9a906ef1b3fcf20a2e48573c17659268"
                },
                {
                    "address": "1FZdVHtiBqMrWdjPyRPULCUceZPJ2WLCsB",
                    "amount": "0.00150000",
                    "applyTime": "2019-09-24 12:43:45",
                    "coin": "BTC",
                    "id": "156ec387f49b41df8724fa744fa82719",
                    "network": "BTC",
                    "status": 6,
                    "txId": "60fd9007ebfddc753455f95fafa808c4302c836e4d1eebc5a132c36c1d8ac354"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "capital/withdraw/history", True, data=params
        )


    def get_withdraw_history_id(self, withdraw_id, **params):
        """Fetch withdraw history.

        https://binance-docs.github.io/apidocs/spot/en/#withdraw-history-supporting-network-user_data

        :param withdraw_id: required
        :type withdraw_id: str
        :param asset: optional
        :type asset: str
        :type status: 0(0:Email Sent,1:Cancelled 2:Awaiting Approval 3:Rejected 4:Processing 5:Failure 6Completed) optional
        :type status: int
        :param startTime: optional
        :type startTime: long
        :param endTime: optional
        :type endTime: long
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "id":"7213fea8e94b4a5593d507237e5a555b",
                "withdrawOrderId": None,
                "amount": 0.99,
                "transactionFee": 0.01,
                "address": "0x6915f16f8791d0a1cc2bf47c13a6b2a92000504b",
                "asset": "ETH",
                "txId": "0xdf33b22bdb2b28b1f75ccd201a4a4m6e7g83jy5fc5d5a9d1340961598cfcb0a1",
                "applyTime": 1508198532000,
                "status": 4
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        result = self.get_withdraw_history(**params)

        for entry in result:
            if "id" in entry and entry["id"] == withdraw_id:
                return entry

        raise Exception("There is no entry with withdraw id", result)


    def get_deposit_address(self, coin: str, network: Optional[str] = None, **params):
        """Fetch a deposit address for a symbol

        https://developers.binance.com/docs/wallet/capital/deposite-address

        :param coin: required
        :type coin: str
        :param network: optional
        :type network: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "address": "1HPn8Rx2y6nNSfagQBKy27GB99Vbzg89wv",
                "coin": "BTC",
                "tag": "",
                "url": "https://btc.com/1HPn8Rx2y6nNSfagQBKy27GB99Vbzg89wv"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        params["coin"] = coin
        if network:
            params["network"] = network
        return self._request_margin_api(
            "get", "capital/deposit/address", True, data=params
        )

    # User Stream Endpoints


    def stream_get_listen_key(self):
        """Start a new user data stream and return the listen key
        If a stream already exists it should return the same key.
        If the stream becomes invalid a new key is returned.

        Can be used to keep the user stream alive.

        https://binance-docs.github.io/apidocs/spot/en/#listen-key-spot

        :returns: API response

        .. code-block:: python

            {
                "listenKey": "pqia91ma19a5s61cv6a81va65sdf19v8a65a1a5s61cv6a81va65sdf19v8a65a1"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        res = self._post(
            "userDataStream", False, data={}
        )
        return res["listenKey"]


    def stream_keepalive(self, listenKey):
        """PING a user data stream to prevent a time out.

        https://binance-docs.github.io/apidocs/spot/en/#listen-key-spot

        :param listenKey: required
        :type listenKey: str

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        params = {"listenKey": listenKey}
        return self._put(
            "userDataStream", False, data=params
        )


    def stream_close(self, listenKey):
        """Close out a user data stream.

        https://binance-docs.github.io/apidocs/spot/en/#listen-key-spot

        :param listenKey: required
        :type listenKey: str

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        params = {"listenKey": listenKey}
        return self._delete(
            "userDataStream", False, data=params, version=self.PRIVATE_API_VERSION
        )

    
