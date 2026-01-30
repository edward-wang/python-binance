"""
MarginMixin - Margin(杠杆) API

此 mixin 包含所有 Margin(杠杆) 相关的方法。
"""
from typing import Dict, Any, Optional

# 此 mixin 依赖 ClientCore 提供的请求方法


class MarginMixin:
    """
    Margin(杠杆) API Mixin
    
    此 mixin 提供所有 Margin(杠杆) 相关的方法。
    这些方法依赖 ClientCore 提供的请求基础设施。
    """

    def get_margin_account(self, **params):
        """Query cross-margin account details

        https://developers.binance.com/docs/margin_trading/account/Query-Cross-Margin-Account-Details

        :returns: API response

        .. code-block:: python

            {
                "borrowEnabled": true,
                "marginLevel": "11.64405625",
                "totalAssetOfBtc": "6.82728457",
                "totalLiabilityOfBtc": "0.58633215",
                "totalNetAssetOfBtc": "6.24095242",
                "tradeEnabled": true,
                "transferEnabled": true,
                "userAssets": [
                    {
                        "asset": "BTC",
                        "borrowed": "0.00000000",
                        "free": "0.00499500",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00499500"
                    },
                    {
                        "asset": "BNB",
                        "borrowed": "201.66666672",
                        "free": "2346.50000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "2144.83333328"
                    },
                    {
                        "asset": "ETH",
                        "borrowed": "0.00000000",
                        "free": "0.00000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00000000"
                    },
                    {
                        "asset": "USDT",
                        "borrowed": "0.00000000",
                        "free": "0.00000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00000000"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api("get", "margin/account", True, data=params)


    def get_isolated_margin_account(self, **params):
        """Query isolated margin account details

        https://developers.binance.com/docs/margin_trading/account/Query-Isolated-Margin-Account-Info

        :param symbols: optional up to 5 margin pairs as a comma separated string
        :type asset: str

        .. code:: python

            account_info = client.get_isolated_margin_account()
            account_info = client.get_isolated_margin_account(symbols="BTCUSDT,ETHUSDT")

        :returns: API response

        .. code-block:: python

            If "symbols" is not sent:

                {
                "assets":[
                    {
                        "baseAsset":
                        {
                        "asset": "BTC",
                        "borrowEnabled": true,
                        "borrowed": "0.00000000",
                        "free": "0.00000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00000000",
                        "netAssetOfBtc": "0.00000000",
                        "repayEnabled": true,
                        "totalAsset": "0.00000000"
                        },
                        "quoteAsset":
                        {
                        "asset": "USDT",
                        "borrowEnabled": true,
                        "borrowed": "0.00000000",
                        "free": "0.00000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00000000",
                        "netAssetOfBtc": "0.00000000",
                        "repayEnabled": true,
                        "totalAsset": "0.00000000"
                        },
                        "symbol": "BTCUSDT"
                        "isolatedCreated": true,
                        "marginLevel": "0.00000000",
                        "marginLevelStatus": "EXCESSIVE", // "EXCESSIVE", "NORMAL", "MARGIN_CALL", "PRE_LIQUIDATION", "FORCE_LIQUIDATION"
                        "marginRatio": "0.00000000",
                        "indexPrice": "10000.00000000"
                        "liquidatePrice": "1000.00000000",
                        "liquidateRate": "1.00000000"
                        "tradeEnabled": true
                    }
                    ],
                    "totalAssetOfBtc": "0.00000000",
                    "totalLiabilityOfBtc": "0.00000000",
                    "totalNetAssetOfBtc": "0.00000000"
                }

            If "symbols" is sent:

                {
                "assets":[
                    {
                        "baseAsset":
                        {
                        "asset": "BTC",
                        "borrowEnabled": true,
                        "borrowed": "0.00000000",
                        "free": "0.00000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00000000",
                        "netAssetOfBtc": "0.00000000",
                        "repayEnabled": true,
                        "totalAsset": "0.00000000"
                        },
                        "quoteAsset":
                        {
                        "asset": "USDT",
                        "borrowEnabled": true,
                        "borrowed": "0.00000000",
                        "free": "0.00000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00000000",
                        "netAssetOfBtc": "0.00000000",
                        "repayEnabled": true,
                        "totalAsset": "0.00000000"
                        },
                        "symbol": "BTCUSDT"
                        "isolatedCreated": true,
                        "marginLevel": "0.00000000",
                        "marginLevelStatus": "EXCESSIVE", // "EXCESSIVE", "NORMAL", "MARGIN_CALL", "PRE_LIQUIDATION", "FORCE_LIQUIDATION"
                        "marginRatio": "0.00000000",
                        "indexPrice": "10000.00000000"
                        "liquidatePrice": "1000.00000000",
                        "liquidateRate": "1.00000000"
                        "tradeEnabled": true
                    }
                    ]
                }

        """
        return self._request_margin_api(
            "get", "margin/isolated/account", True, data=params
        )


    def enable_isolated_margin_account(self, **params):
        """Enable isolated margin account for a specific symbol.

        https://developers.binance.com/docs/margin_trading/account/Enable-Isolated-Margin-Account

        :param symbol:
        :type asset: str

        :returns: API response

        .. code-block:: python

            {
              "success": true,
              "symbol": "BTCUSDT"
            }


        """
        return self._request_margin_api(
            "post", "margin/isolated/account", True, data=params
        )


    def disable_isolated_margin_account(self, **params):
        """Disable isolated margin account for a specific symbol. Each trading pair can only
        be deactivated once every 24 hours.

        https://developers.binance.com/docs/margin_trading/account/Disable-Isolated-Margin-Account

        :param symbol:
        :type asset: str

        :returns: API response

        .. code-block:: python

            {
              "success": true,
              "symbol": "BTCUSDT"
            }

        """
        return self._request_margin_api(
            "delete", "margin/isolated/account", True, data=params
        )


    def get_enabled_isolated_margin_account_limit(self, **params):
        """Query enabled isolated margin account limit.

        https://developers.binance.com/docs/margin_trading/account/Query-Enabled-Isolated-Margin-Account-Limit

        :returns: API response

        .. code-block:: python
            {
                "enabledAccount": 5,
                "maxAccount": 20
            }

        """
        return self._request_margin_api(
            "get", "margin/isolated/accountLimit", True, data=params
        )


    def get_margin_dustlog(self, **params):
        """
        Query the historical information of user's margin account small-value asset conversion BNB.

        https://binance-docs.github.io/apidocs/spot/en/#margin-dustlog-user_data

        :param startTime: optional
        :type startTime: long
        :param endTime: optional
        :type endTime: long

        :returns: API response

        .. code-block:: python
            {
                "total": 8, //Total counts of exchange
                "userAssetDribblets": [
                    {
                        "operateTime": 1615985535000,
                        "totalTransferedAmount": "0.00132256", // Total transfered BNB amount for this exchange.
                        "totalServiceChargeAmount": "0.00002699", //Total service charge amount for this exchange.
                        "transId": 45178372831,
                        "userAssetDribbletDetails": [ //Details of  this exchange.
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
                                "operateTime": 1615985535000,
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
                                "serviceChargeAmount": "0.00001",
                                "amount": "0.001",
                                "operateTime": 1616203180000,
                                "transferedAmount": "0.00049",
                                "fromAsset": "USDT"
                            },
                            {
                                "transId": 4357015,
                                "serviceChargeAmount": "0.000002",
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
        return self._request_margin_api("get", "margin/dribblet", True, data=params)


    def get_margin_dust_assets(self, **params):
        """Get margin assets that can be converted into BNB.

        https://binance-docs.github.io/apidocs/spot/en/#margin-dustlog-user_data

        :returns: API response

        .. code-block:: python
            {
                "details": [
                    {
                        "asset": "ADA",
                        "assetFullName": "ADA",
                        "amountFree": "6.21",
                        "toBTC": "0.00016848",
                        "toBNB": "0.01777302",
                        "toBNBOffExchange": "0.01741756",
                        "exchange": "0.00035546"
                    }
                ],
                "totalTransferBtc": "0.00016848",
                "totalTransferBNB": "0.01777302",
                "dribbletPercentage": "0.02"
            }

        """
        return self._request_margin_api("get", "margin/dust", True, data=params)


    def transfer_margin_dust(self, **params):
        """Convert dust assets to BNB.

        https://binance-docs.github.io/apidocs/spot/en/#dust-transfer-trade

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
                    },
                    {
                        "amount":"0.09000000",
                        "fromAsset":"LTC",
                        "operateTime":1563368549404,
                        "serviceChargeAmount":"0.01548000",
                        "tranId":2970932918,
                        "transferedAmount":"0.77400000"
                    }
                ]
            }

        """
        return self._request_margin_api("post", "margin/dust", True, data=params)


    def get_cross_margin_collateral_ratio(self, **params):
        """
        https://developers.binance.com/docs/margin_trading/market-data

        :param none

        :returns: API response

        .. code-block:: python
            [
              {
                "collaterals": [
                  {
                    "minUsdValue": "0",
                    "maxUsdValue": "13000000",
                    "discountRate": "1"
                  },
                  {
                    "minUsdValue": "13000000",
                    "maxUsdValue": "20000000",
                    "discountRate": "0.975"
                  },
                  {
                    "minUsdValue": "20000000",
                    "discountRate": "0"
                  }
                ],
                "assetNames": [
                  "BNX"
                ]
              },
              {
                "collaterals": [
                  {
                    "minUsdValue": "0",
                    "discountRate": "1"
                  }
                ],
                "assetNames": [
                  "BTC",
                  "BUSD",
                  "ETH",
                  "USDT"
                ]
              }
            ]
        """
        return self._request_margin_api(
            "get", "margin/crossMarginCollateralRatio", True, data=params
        )


    def get_small_liability_exchange_assets(self, **params):
        """Query the coins which can be small liability exchange

        https://developers.binance.com/docs/margin_trading/trade/Get-Small-Liability-Exchange-Coin-List

        :returns: API response

        .. code-block:: python
            [
                {
                  "asset": "ETH",
                  "interest": "0.00083334",
                  "principal": "0.001",
                  "liabilityAsset": "USDT",
                  "liabilityQty": 0.3552
                }
            ]

        """
        return self._request_margin_api(
            "get", "margin/exchange-small-liability", True, data=params
        )


    def exchange_small_liability_assets(self, **params):
        """Cross Margin Small Liability Exchange

        https://developers.binance.com/docs/margin_trading/trade/Small-Liability-Exchange

        :param assetNames: The assets list of small liability exchange
        :type assetNames: array

        :returns: API response

        .. code-block:: python
        none

        """
        return self._request_margin_api(
            "post", "margin/exchange-small-liability", True, data=params
        )


    def get_small_liability_exchange_history(self, **params):
        """Get Small liability Exchange History

        https://developers.binance.com/docs/margin_trading/trade/Get-Small-Liability-Exchange-History

        :param current: Currently querying page. Start from 1. Default:1
        :type current: int
        :param size: Default:10, Max:100
        :type size: int
        :param startTime: Default: 30 days from current timestamp
        :type startTime: long
        :param endTime: Default: present timestamp
        :type endTIme: long

        :returns: API response

        .. code-block:: python
            {
                "total": 1,
                "rows": [
                  {
                    "asset": "ETH",
                    "amount": "0.00083434",
                    "targetAsset": "BUSD",
                    "targetAmount": "1.37576819",
                    "bizType": "EXCHANGE_SMALL_LIABILITY",
                    "timestamp": 1672801339253
                  }
                ]
            }

        """
        return self._request_margin_api(
            "get", "margin/exchange-small-liability-history", True, data=params
        )


    def get_future_hourly_interest_rate(self, **params):
        """Get user the next hourly estimate interest

        https://developers.binance.com/docs/margin_trading/borrow-and-repay

        :param assets: List of assets, separated by commas, up to 20
        :type assets: str
        :param isIsolated: for isolated margin or not, "TRUE", "FALSE"
        :type isIsolated: bool

        :returns: API response

        .. code-block:: python
            [
                {
                    "asset": "BTC",
                    "nextHourlyInterestRate": "0.00000571"
                },
                {
                    "asset": "ETH",
                    "nextHourlyInterestRate": "0.00000578"
                }
            ]

        """
        return self._request_margin_api(
            "get", "margin/next-hourly-interest-rate", True, data=params
        )


    def get_margin_capital_flow(self, **params):
        """Get cross or isolated margin capital flow

        https://developers.binance.com/docs/margin_trading/account/Query-Cross-Isolated-Margin-Capital-Flow

        :param asset: optional
        :type asset: str
        :param symbol: Required when querying isolated data
        :type symbol: str
        :param type: optional
        :type type: string
        :param startTime: Only supports querying the data of the last 90 days
        :type startTime: long
        :param endTime: optional
        :type endTime: long
        :param formId: If fromId is set, the data with id > fromId will be returned. Otherwise the latest data will be returned
        :type formId: long
        :param limit: The number of data items returned each time is limited. Default 500; Max 1000.
        :type limit: long

        :returns: API response

        .. code-block:: python
            [
              {
                "id": 123456,
                "tranId": 123123,
                "timestamp": 1691116657000,
                "asset": "USDT,
                "symbol": "BTCUSDT",
                "type": "BORROW",
                "amount": "101"
              },
              {
                "id": 123457,
                "tranId": 123124,
                "timestamp": 1691116658000,
                "asset": "BTC",
                "symbol": "BTCUSDT",
                "type": "REPAY",
                "amount": "10"
              }
            ]

        """
        return self._request_margin_api("get", "margin/capital-flow", True, data=params)


    def get_margin_asset(self, **params):
        """Query cross-margin asset

        https://binance-docs.github.io/apidocs/spot/en/#query-margin-asset-market_data

        :param asset: name of the asset
        :type asset: str

        .. code-block:: python

            asset_details = client.get_margin_asset(asset='BNB')

        :returns: API response

        .. code-block:: python

            {
                "assetFullName": "Binance Coin",
                "assetName": "BNB",
                "isBorrowable": false,
                "isMortgageable": true,
                "userMinBorrow": "0.00000000",
                "userMinRepay": "0.00000000"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api("get", "margin/asset", data=params)


    def get_margin_symbol(self, **params):
        """Query cross-margin symbol info

        https://binance-docs.github.io/apidocs/spot/en/#query-cross-margin-pair-market_data

        :param symbol: name of the symbol pair
        :type symbol: str

        .. code:: python

            pair_details = client.get_margin_symbol(symbol='BTCUSDT')

        :returns: API response

        .. code-block:: python

            {
                "id":323355778339572400,
                "symbol":"BTCUSDT",
                "base":"BTC",
                "quote":"USDT",
                "isMarginTrade":true,
                "isBuyAllowed":true,
                "isSellAllowed":true
            }


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api("get", "margin/pair", data=params)


    def get_margin_all_assets(self, **params):
        """Get All Margin Assets (MARKET_DATA)

        https://developers.binance.com/docs/margin_trading/market-data/Get-All-Margin-Assets

        .. code:: python

            margin_assets = client.get_margin_all_assets()

        :returns: API response

        .. code-block:: python

            [
                {
                    "assetFullName": "USD coin",
                    "assetName": "USDC",
                    "isBorrowable": true,
                    "isMortgageable": true,
                    "userMinBorrow": "0.00000000",
                    "userMinRepay": "0.00000000"
                },
                {
                    "assetFullName": "BNB-coin",
                    "assetName": "BNB",
                    "isBorrowable": true,
                    "isMortgageable": true,
                    "userMinBorrow": "1.00000000",
                    "userMinRepay": "0.00000000"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api("get", "margin/allAssets", data=params)


    def get_margin_all_pairs(self, **params):
        """Get All Cross Margin Pairs (MARKET_DATA)

        https://developers.binance.com/docs/margin_trading/market-data/Get-All-Cross-Margin-Pairs

        .. code:: python

            margin_pairs = client.get_margin_all_pairs()

        :returns: API response

        .. code-block:: python

            [
                {
                    "base": "BNB",
                    "id": 351637150141315861,
                    "isBuyAllowed": true,
                    "isMarginTrade": true,
                    "isSellAllowed": true,
                    "quote": "BTC",
                    "symbol": "BNBBTC"
                },
                {
                    "base": "TRX",
                    "id": 351637923235429141,
                    "isBuyAllowed": true,
                    "isMarginTrade": true,
                    "isSellAllowed": true,
                    "quote": "BTC",
                    "symbol": "TRXBTC"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api("get", "margin/allPairs", data=params)


    def create_isolated_margin_account(self, **params):
        """Create isolated margin account for symbol

        https://binance-docs.github.io/apidocs/spot/en/#create-isolated-margin-account-margin

        :param base: Base asset of symbol
        :type base: str
        :param quote: Quote asset of symbol
        :type quote: str

        .. code:: python

            pair_details = client.create_isolated_margin_account(base='USDT', quote='BTC')

        :returns: API response

        .. code-block:: python

            {
                "success": true,
                "symbol": "BTCUSDT"
            }


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "post", "margin/isolated/create", signed=True, data=params
        )


    def get_isolated_margin_symbol(self, **params):
        """Query isolated margin symbol info

        https://binance-docs.github.io/apidocs/spot/en/#query-isolated-margin-symbol-user_data

        :param symbol: name of the symbol pair
        :type symbol: str

        .. code:: python

            pair_details = client.get_isolated_margin_symbol(symbol='BTCUSDT')

        :returns: API response

        .. code-block:: python

            {
            "symbol":"BTCUSDT",
            "base":"BTC",
            "quote":"USDT",
            "isMarginTrade":true,
            "isBuyAllowed":true,
            "isSellAllowed":true
            }


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "margin/isolated/pair", signed=True, data=params
        )


    def get_all_isolated_margin_symbols(self, **params):
        """Query isolated margin symbol info for all pairs

        https://developers.binance.com/docs/margin_trading/market-data/Get-All-Isolated-Margin-Symbol

        .. code:: python

            pair_details = client.get_all_isolated_margin_symbols()

        :returns: API response

        .. code-block:: python

            [
                {
                    "base": "BNB",
                    "isBuyAllowed": true,
                    "isMarginTrade": true,
                    "isSellAllowed": true,
                    "quote": "BTC",
                    "symbol": "BNBBTC"
                },
                {
                    "base": "TRX",
                    "isBuyAllowed": true,
                    "isMarginTrade": true,
                    "isSellAllowed": true,
                    "quote": "BTC",
                    "symbol": "TRXBTC"
                }
            ]


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "margin/isolated/allPairs", signed=True, data=params
        )


    def get_isolated_margin_fee_data(self, **params):
        """Get isolated margin fee data collection with any vip level or user's current specific data as https://www.binance.com/en/margin-fee

        https://developers.binance.com/docs/margin_trading/account/Query-Isolated-Margin-Fee-Data

        :param vipLevel: User's current specific margin data will be returned if vipLevel is omitted
        :type vipLevel: int
        :param symbol: optional
        :type symbol: str

        :returns: API response

        .. code-block:: python
            [
                {
                    "vipLevel": 0,
                    "symbol": "BTCUSDT",
                    "leverage": "10",
                    "data": [
                        {
                            "coin": "BTC",
                            "dailyInterest": "0.00026125",
                            "borrowLimit": "270"
                        },
                        {
                            "coin": "USDT",
                            "dailyInterest": "0.000475",
                            "borrowLimit": "2100000"
                        }
                    ]
                }
            ]
        """
        return self._request_margin_api(
            "get", "margin/isolatedMarginData", True, data=params
        )


    def get_isolated_margin_tier_data(self, **params):
        """Get isolated margin tier data collection with any tier as https://www.binance.com/en/margin-data

        https://developers.binance.com/docs/margin_trading/market-data/Query-Isolated-Margin-Tier-Data

        :param symbol: required
        :type symbol: str
        :param tier: All margin tier data will be returned if tier is omitted
        :type tier: int
        :param recvWindow: optional: No more than 60000
        :type recvWindow:

        :returns: API response

        .. code-block:: python
            [
                {
                    "symbol": "BTCUSDT",
                    "tier": 1,
                    "effectiveMultiple": "10",
                    "initialRiskRatio": "1.111",
                    "liquidationRiskRatio": "1.05",
                    "baseAssetMaxBorrowable": "9",
                    "quoteAssetMaxBorrowable": "70000"
                }
            ]

        """
        return self._request_margin_api(
            "get", "margin/isolatedMarginTier", True, data=params
        )


    def margin_manual_liquidation(self, **params):
        """

        https://developers.binance.com/docs/margin_trading/trade/Margin-Manual-Liquidation



        :param type: required
        :type symbol: str: When type selected is "ISOLATED", symbol must be filled in

        :returns: API response

            [
                {
                    "asset": "ETH",
                    "interest": "0.00083334",
                    "principal": "0.001",
                    "liabilityAsset": "USDT",
                    "liabilityQty": 0.3552
                }
            ]

        """
        return self._request_margin_api(
            "post", "margin/manual-liquidation", True, data=params
        )


    def toggle_bnb_burn_spot_margin(self, **params):
        """Toggle BNB Burn On Spot Trade And Margin Interest

        https://developers.binance.com/docs/wallet/asset/Toggle-BNB-Burn-On-Spot-Trade-And-Margin-Interest

        :param spotBNBBurn: Determines whether to use BNB to pay for trading fees on SPOT
        :type spotBNBBurn: bool
        :param interestBNBBurn: Determines whether to use BNB to pay for margin loan's interest
        :type interestBNBBurn: bool

        .. code:: python

            response = client.toggle_bnb_burn_spot_margin()

        :returns: API response

        .. code-block:: python

            {
               "spotBNBBurn":true,
               "interestBNBBurn": false
            }


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api("post", "bnbBurn", signed=True, data=params)


    def get_bnb_burn_spot_margin(self, **params):
        """Get BNB Burn Status

        https://developers.binance.com/docs/margin_trading/account/Get-BNB-Burn-Status

        .. code:: python

            status = client.get_bnb_burn_spot_margin()

        :returns: API response

        .. code-block:: python

            {
               "spotBNBBurn":true,
               "interestBNBBurn": false
            }


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api("get", "bnbBurn", signed=True, data=params)


    def get_margin_price_index(self, **params):
        """Query margin priceIndex

        https://developers.binance.com/docs/margin_trading/market-data/Query-Margin-PriceIndex

        :param symbol: name of the symbol pair
        :type symbol: str

        .. code:: python

            price_index_details = client.get_margin_price_index(symbol='BTCUSDT')

        :returns: API response

        .. code-block:: python

            {
                "calcTime": 1562046418000,
                "price": "0.00333930",
                "symbol": "BNBBTC"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api("get", "margin/priceIndex", data=params)


    def transfer_margin_to_spot(self, **params):
        """Execute transfer between cross-margin account and spot account.

        https://binance-docs.github.io/apidocs/spot/en/#cross-margin-account-transfer-margin

        :param asset: name of the asset
        :type asset: str
        :param amount: amount to transfer
        :type amount: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code-block:: python

            transfer = client.transfer_margin_to_spot(asset='BTC', amount='1.1')

        :returns: API response

        .. code-block:: python

            {
                "tranId": 100000001
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        params["type"] = 2
        return self._request_margin_api(
            "post", "margin/transfer", signed=True, data=params
        )


    def transfer_spot_to_margin(self, **params):
        """Execute transfer between spot account and cross-margin account.

        https://binance-docs.github.io/apidocs/spot/en/#cross-margin-account-transfer-margin

        :param asset: name of the asset
        :type asset: str
        :param amount: amount to transfer
        :type amount: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code-block:: python

            transfer = client.transfer_spot_to_margin(asset='BTC', amount='1.1')

        :returns: API response

        .. code-block:: python

            {
                "tranId": 100000001
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        params["type"] = 1
        return self._request_margin_api(
            "post", "margin/transfer", signed=True, data=params
        )


    def transfer_isolated_margin_to_spot(self, **params):
        """Execute transfer between isolated margin account and spot account.

        https://binance-docs.github.io/apidocs/spot/en/#isolated-margin-account-transfer-margin

        :param asset: name of the asset
        :type asset: str
        :param symbol: pair symbol
        :type symbol: str
        :param amount: amount to transfer
        :type amount: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code-block:: python

            transfer = client.transfer_isolated_margin_to_spot(asset='BTC',
                                                                symbol='ETHBTC', amount='1.1')

        :returns: API response

        .. code-block:: python

            {
                "tranId": 100000001
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        params["transFrom"] = "ISOLATED_MARGIN"
        params["transTo"] = "SPOT"
        return self._request_margin_api(
            "post", "margin/isolated/transfer", signed=True, data=params
        )


    def transfer_spot_to_isolated_margin(self, **params):
        """Execute transfer between spot account and isolated margin account.

        https://binance-docs.github.io/apidocs/spot/en/#isolated-margin-account-transfer-margin

        :param asset: name of the asset
        :type asset: str
        :param symbol: pair symbol
        :type symbol: str
        :param amount: amount to transfer
        :type amount: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code-block:: python

            transfer = client.transfer_spot_to_isolated_margin(asset='BTC',
                                                                symbol='ETHBTC', amount='1.1')

        :returns: API response

        .. code-block:: python

            {
                "tranId": 100000001
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        params["transFrom"] = "SPOT"
        params["transTo"] = "ISOLATED_MARGIN"
        return self._request_margin_api(
            "post", "margin/isolated/transfer", signed=True, data=params
        )


    def get_isolated_margin_tranfer_history(self, **params):
        """Get transfers to isolated margin account.

        https://binance-docs.github.io/apidocs/spot/en/#get-isolated-margin-transfer-history-user_data

        :param asset: name of the asset
        :type asset: str
        :param symbol: pair required
        :type symbol: str
        :param transFrom: optional SPOT, ISOLATED_MARGIN
        :param transFrom: str SPOT, ISOLATED_MARGIN
        :param transTo: optional
        :param transTo: str
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param current: Currently querying page. Start from 1. Default:1
        :type current: str
        :param size: Default:10 Max:100
        :type size: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code-block:: python

            transfer = client.transfer_spot_to_isolated_margin(symbol='ETHBTC')

        :returns: API response

        .. code-block:: python

            {
              "rows": [
                {
                  "amount": "0.10000000",
                  "asset": "BNB",
                  "status": "CONFIRMED",
                  "timestamp": 1566898617000,
                  "txId": 5240372201,
                  "transFrom": "SPOT",
                  "transTo": "ISOLATED_MARGIN"
                },
                {
                  "amount": "5.00000000",
                  "asset": "USDT",
                  "status": "CONFIRMED",
                  "timestamp": 1566888436123,
                  "txId": 5239810406,
                  "transFrom": "ISOLATED_MARGIN",
                  "transTo": "SPOT"
                }
              ],
              "total": 2
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "margin/isolated/transfer", signed=True, data=params
        )


    def create_margin_loan(self, **params):
        """Apply for a loan in cross-margin or isolated-margin account.

        https://binance-docs.github.io/apidocs/spot/en/#margin-account-borrow-margin

        :param asset: name of the asset
        :type asset: str
        :param amount: amount to transfer
        :type amount: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param symbol: Isolated margin symbol (default blank for cross-margin)
        :type symbol: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code-block:: python

            transaction = client.margin_create_loan(asset='BTC', amount='1.1')

            transaction = client.margin_create_loan(asset='BTC', amount='1.1',
                                                    isIsolated='TRUE', symbol='ETHBTC')

        :returns: API response

        .. code-block:: python

            {
                "tranId": 100000001
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api("post", "margin/loan", signed=True, data=params)


    def repay_margin_loan(self, **params):
        """Repay loan in cross-margin or isolated-margin account.

        If amount is more than the amount borrowed, the full loan will be repaid.

        https://binance-docs.github.io/apidocs/spot/en/#margin-account-repay-margin

        :param asset: name of the asset
        :type asset: str
        :param amount: amount to transfer
        :type amount: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param symbol: Isolated margin symbol (default blank for cross-margin)
        :type symbol: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code-block:: python

            transaction = client.margin_repay_loan(asset='BTC', amount='1.1')

            transaction = client.margin_repay_loan(asset='BTC', amount='1.1',
                                                    isIsolated='TRUE', symbol='ETHBTC')

        :returns: API response

        .. code-block:: python

            {
                "tranId": 100000001
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "post", "margin/repay", signed=True, data=params
        )


    def create_margin_order(self, **params):
        """Post a new order for margin account.

        https://developers.binance.com/docs/margin_trading/trade/Margin-Account-New-Order

        :param symbol: required
        :type symbol: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param side: required
        :type side: str
        :param type: required
        :type type: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param stopPrice: Used with STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, and TAKE_PROFIT_LIMIT orders.
        :type stopPrice: str
        :param timeInForce: required if limit order GTC,IOC,FOK
        :type timeInForce: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param icebergQty: Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
        :type icebergQty: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; MARKET and LIMIT order types default to
            FULL, all other orders default to ACK.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        Response ACK:

        .. code-block:: python

            {
                "symbol": "BTCUSDT",
                "orderId": 28,
                "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                "transactTime": 1507725176595
            }

        Response RESULT:

        .. code-block:: python

            {
                "symbol": "BTCUSDT",
                "orderId": 28,
                "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                "transactTime": 1507725176595,
                "price": "1.00000000",
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
                "price": "1.00000000",
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

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException,
            BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
            BinanceOrderInactiveSymbolException

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.SPOT_ORDER_PREFIX + self.uuid22()
        return self._request_margin_api(
            "post", "margin/order", signed=True, data=params
        )


    def cancel_margin_order(self, **params):
        """Cancel an active order for margin account.

        Either orderId or origClientOrderId must be sent.

        https://developers.binance.com/docs/margin_trading/trade/Margin-Account-Cancel-Order

        :param symbol: required
        :type symbol: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param orderId:
        :type orderId: str
        :param origClientOrderId:
        :type origClientOrderId: str
        :param newClientOrderId: Used to uniquely identify this cancel. Automatically generated by default.
        :type newClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "symbol": "LTCBTC",
                "orderId": 28,
                "origClientOrderId": "myOrder1",
                "clientOrderId": "cancelMyOrder1",
                "transactTime": 1507725176595,
                "price": "1.00000000",
                "origQty": "10.00000000",
                "executedQty": "8.00000000",
                "cummulativeQuoteQty": "8.00000000",
                "status": "CANCELED",
                "timeInForce": "GTC",
                "type": "LIMIT",
                "side": "SELL"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "delete", "margin/order", signed=True, data=params
        )


    def cancel_all_open_margin_orders(self, **params):
        """
        Cancels all active orders on a symbol for margin account.

        https://developers.binance.com/docs/margin_trading/trade/Margin-Account-Cancel-All-Open-Orders

        :param symbol: required
        :type symbol: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int
        :returns: API response

        :raises: BinanceRequestException, BinanceAPIException
        """
        return self._request_margin_api(
            "delete", "margin/openOrders", signed=True, data=params
        )


    def set_margin_max_leverage(self, **params):
        """Adjust cross margin max leverage

        https://developers.binance.com/docs/margin_trading/account

        :param maxLeverage: required Can only adjust 3 or 5, Example: maxLeverage=3
        :type maxLeverage: int

        :returns: API response

            {
                "success": true
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "post", "margin/max-leverage", signed=True, data=params
        )


    def get_margin_transfer_history(self, **params):
        """Query margin transfer history

        https://developers.binance.com/docs/margin_trading/transfer

        :param asset: optional
        :type asset: str
        :param type: optional Transfer Type: ROLL_IN, ROLL_OUT
        :type type: str
        :param archived: optional Default: false. Set to true for archived data from 6 months ago
        :type archived: str
        :param startTime: earliest timestamp to filter transactions
        :type startTime: str
        :param endTime: Used to uniquely identify this cancel. Automatically generated by default.
        :type endTime: str
        :param current: Currently querying page. Start from 1. Default:1
        :type current: str
        :param size: Default:10 Max:100
        :type size: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "rows": [
                    {
                        "amount": "0.10000000",
                        "asset": "BNB",
                        "status": "CONFIRMED",
                        "timestamp": 1566898617,
                        "txId": 5240372201,
                        "type": "ROLL_IN"
                    },
                    {
                        "amount": "5.00000000",
                        "asset": "USDT",
                        "status": "CONFIRMED",
                        "timestamp": 1566888436,
                        "txId": 5239810406,
                        "type": "ROLL_OUT"
                    },
                    {
                        "amount": "1.00000000",
                        "asset": "EOS",
                        "status": "CONFIRMED",
                        "timestamp": 1566888403,
                        "txId": 5239808703,
                        "type": "ROLL_IN"
                    }
                ],
                "total": 3
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "margin/transfer", signed=True, data=params
        )


    def get_margin_loan_details(self, **params):
        """Query loan record

        txId or startTime must be sent. txId takes precedence.

        https://binance-docs.github.io/apidocs/spot/en/#query-loan-record-user_data

        :param asset: required
        :type asset: str
        :param isolatedSymbol: isolated symbol (if querying isolated margin)
        :type isolatedSymbol: str
        :param txId: the tranId in of the created loan
        :type txId: str
        :param startTime: earliest timestamp to filter transactions
        :type startTime: str
        :param endTime: Used to uniquely identify this cancel. Automatically generated by default.
        :type endTime: str
        :param current: Currently querying page. Start from 1. Default:1
        :type current: str
        :param size: Default:10 Max:100
        :type size: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "rows": [
                    {
                        "asset": "BNB",
                        "principal": "0.84624403",
                        "timestamp": 1555056425000,
                        //one of PENDING (pending to execution), CONFIRMED (successfully loaned), FAILED (execution failed, nothing happened to your account);
                        "status": "CONFIRMED"
                    }
                ],
                "total": 1
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api("get", "margin/loan", signed=True, data=params)


    def get_margin_repay_details(self, **params):
        """Query repay record

        txId or startTime must be sent. txId takes precedence.

        https://binance-docs.github.io/apidocs/spot/en/#query-repay-record-user_data

        :param asset: required
        :type asset: str
        :param isolatedSymbol: isolated symbol (if querying isolated margin)
        :type isolatedSymbol: str
        :param txId: the tranId in of the created loan
        :type txId: str
        :param startTime:
        :type startTime: str
        :param endTime: Used to uniquely identify this cancel. Automatically generated by default.
        :type endTime: str
        :param current: Currently querying page. Start from 1. Default:1
        :type current: str
        :param size: Default:10 Max:100
        :type size: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "rows": [
                    {
                        //Total amount repaid
                        "amount": "14.00000000",
                        "asset": "BNB",
                        //Interest repaid
                        "interest": "0.01866667",
                        //Principal repaid
                        "principal": "13.98133333",
                        //one of PENDING (pending to execution), CONFIRMED (successfully loaned), FAILED (execution failed, nothing happened to your account);
                        "status": "CONFIRMED",
                        "timestamp": 1563438204000,
                        "txId": 2970933056
                    }
                ],
                "total": 1
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api("get", "margin/repay", signed=True, data=params)


    def get_cross_margin_data(self, **params):
        """Query Cross Margin Fee Data (USER_DATA)

        https://developers.binance.com/docs/margin_trading/account/Query-Cross-Margin-Fee-Data

        :param vipLevel: User's current specific margin data will be returned if vipLevel is omitted
        :type vipLevel: int
        :param coin
        :type coin: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int
        :returns: API response (example):
            [
                {
                    "vipLevel": 0,
                    "coin": "BTC",
                    "transferIn": true,
                    "borrowable": true,
                    "dailyInterest": "0.00026125",
                    "yearlyInterest": "0.0953",
                    "borrowLimit": "180",
                    "marginablePairs": [
                        "BNBBTC",
                        "TRXBTC",
                        "ETHBTC",
                        "BTCUSDT"
                    ]
                }
            ]
        """
        return self._request_margin_api(
            "get", "margin/crossMarginData", signed=True, data=params
        )


    def get_margin_interest_history(self, **params):
        """Get Interest History (USER_DATA)

        https://developers.binance.com/docs/margin_trading/borrow-and-repay/Get-Interest-History

        :param asset:
        :type asset: str
        :param isolatedSymbol: isolated symbol (if querying isolated margin)
        :type isolatedSymbol: str
        :param startTime:
        :type startTime: str
        :param endTime:
        :type endTime: str
        :param current: Currently querying page. Start from 1. Default:1
        :type current: str
        :param size: Default:10 Max:100
        :type size: int
        :param archived: Default: false. Set to true for archived data from 6 months ago
        :type archived: bool
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "rows":[
                    {
                        "isolatedSymbol": "BNBUSDT", // isolated symbol, will not be returned for crossed margin
                        "asset": "BNB",
                        "interest": "0.02414667",
                        "interestAccuredTime": 1566813600000,
                        "interestRate": "0.01600000",
                        "principal": "36.22000000",
                        "type": "ON_BORROW"
                    }
                ],
                "total": 1
            }


        """
        return self._request_margin_api(
            "get", "margin/interestHistory", signed=True, data=params
        )


    def get_margin_force_liquidation_rec(self, **params):
        """Get Force Liquidation Record (USER_DATA)

        https://developers.binance.com/docs/margin_trading/trade

        :param startTime:
        :type startTime: str
        :param endTime:
        :type endTime: str
        :param isolatedSymbol: isolated symbol (if querying isolated margin)
        :type isolatedSymbol: str
        :param current: Currently querying page. Start from 1. Default:1
        :type current: str
        :param size: Default:10 Max:100
        :type size: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "rows": [
                    {
                        "avgPrice": "0.00388359",
                        "executedQty": "31.39000000",
                        "orderId": 180015097,
                        "price": "0.00388110",
                        "qty": "31.39000000",
                        "side": "SELL",
                        "symbol": "BNBBTC",
                        "timeInForce": "GTC",
                        "isIsolated": true,
                        "updatedTime": 1558941374745
                    }
                ],
                "total": 1
            }

        """
        return self._request_margin_api(
            "get", "margin/forceLiquidationRec", signed=True, data=params
        )


    def get_margin_order(self, **params):
        """Query margin accounts order

        Either orderId or origClientOrderId must be sent.

        For some historical orders cummulativeQuoteQty will be < 0, meaning the data is not available at this time.

        https://developers.binance.com/docs/margin_trading/trade/Query-Margin-Account-Order

        :param symbol: required
        :type symbol: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param orderId:
        :type orderId: str
        :param origClientOrderId:
        :type origClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "clientOrderId": "ZwfQzuDIGpceVhKW5DvCmO",
                "cummulativeQuoteQty": "0.00000000",
                "executedQty": "0.00000000",
                "icebergQty": "0.00000000",
                "isWorking": true,
                "orderId": 213205622,
                "origQty": "0.30000000",
                "price": "0.00493630",
                "side": "SELL",
                "status": "NEW",
                "stopPrice": "0.00000000",
                "symbol": "BNBBTC",
                "time": 1562133008725,
                "timeInForce": "GTC",
                "type": "LIMIT",
                "updateTime": 1562133008725
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api("get", "margin/order", signed=True, data=params)


    def get_open_margin_orders(self, **params):
        """Query margin accounts open orders

        If the symbol is not sent, orders for all symbols will be returned in an array (cross-margin only).

        If querying isolated margin orders, both the isIsolated='TRUE' and symbol=symbol_name must be set.

        When all symbols are returned, the number of requests counted against the rate limiter is equal to the number
        of symbols currently trading on the exchange.

        https://developers.binance.com/docs/margin_trading/trade/Query-Margin-Account-Open-Orders

        :param symbol: optional
        :type symbol: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            [
                {
                    "clientOrderId": "qhcZw71gAkCCTv0t0k8LUK",
                    "cummulativeQuoteQty": "0.00000000",
                    "executedQty": "0.00000000",
                    "icebergQty": "0.00000000",
                    "isWorking": true,
                    "orderId": 211842552,
                    "origQty": "0.30000000",
                    "price": "0.00475010",
                    "side": "SELL",
                    "status": "NEW",
                    "stopPrice": "0.00000000",
                    "symbol": "BNBBTC",
                    "time": 1562040170089,
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "updateTime": 1562040170089
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "margin/openOrders", signed=True, data=params
        )


    def get_all_margin_orders(self, **params):
        """Query all margin accounts orders

        If orderId is set, it will get orders >= that orderId. Otherwise most recent orders are returned.

        For some historical orders cummulativeQuoteQty will be < 0, meaning the data is not available at this time.

        https://developers.binance.com/docs/margin_trading/trade/Query-Margin-Account-All-Orders

        :param symbol: required
        :type symbol: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param orderId: optional
        :type orderId: str
        :param startTime: optional
        :type startTime: str
        :param endTime: optional
        :type endTime: str
        :param limit: Default 500; max 1000
        :type limit: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            [
                {
                    "id": 43123876,
                    "price": "0.00395740",
                    "qty": "4.06000000",
                    "quoteQty": "0.01606704",
                    "symbol": "BNBBTC",
                    "time": 1556089977693
                },
                {
                    "id": 43123877,
                    "price": "0.00395740",
                    "qty": "0.77000000",
                    "quoteQty": "0.00304719",
                    "symbol": "BNBBTC",
                    "time": 1556089977693
                },
                {
                    "id": 43253549,
                    "price": "0.00428930",
                    "qty": "23.30000000",
                    "quoteQty": "0.09994069",
                    "symbol": "BNBBTC",
                    "time": 1556163963504
                }
            ]


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "margin/allOrders", signed=True, data=params
        )


    def get_margin_trades(self, **params):
        """Query margin accounts trades

        If fromId is set, it will get orders >= that fromId. Otherwise most recent orders are returned.

        https://developers.binance.com/docs/margin_trading/trade/Query-Margin-Account-Trade-List

        :param symbol: required
        :type symbol: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param fromId: optional
        :type fromId: str
        :param startTime: optional
        :type startTime: str
        :param endTime: optional
        :type endTime: str
        :param limit: Default 500; max 1000
        :type limit: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            [
                {
                    "commission": "0.00006000",
                    "commissionAsset": "BTC",
                    "id": 34,
                    "isBestMatch": true,
                    "isBuyer": false,
                    "isMaker": false,
                    "orderId": 39324,
                    "price": "0.02000000",
                    "qty": "3.00000000",
                    "symbol": "BNBBTC",
                    "time": 1561973357171
                }, {
                    "commission": "0.00002950",
                    "commissionAsset": "BTC",
                    "id": 32,
                    "isBestMatch": true,
                    "isBuyer": false,
                    "isMaker": true,
                    "orderId": 39319,
                    "price": "0.00590000",
                    "qty": "5.00000000",
                    "symbol": "BNBBTC",
                    "time": 1561964645345
                }
            ]


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "margin/myTrades", signed=True, data=params
        )


    def get_max_margin_loan(self, **params):
        """Query max borrow amount for an asset

        https://binance-docs.github.io/apidocs/spot/en/#query-max-borrow-user_data

        :param asset: required
        :type asset: str
        :param isolatedSymbol: isolated symbol (if querying isolated margin)
        :type isolatedSymbol: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "amount": "1.69248805"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "margin/maxBorrowable", signed=True, data=params
        )


    def get_max_margin_transfer(self, **params):
        """Query max transfer-out amount

        https://developers.binance.com/docs/margin_trading/transfer/Query-Max-Transfer-Out-Amount

        :param asset: required
        :type asset: str
        :param isolatedSymbol: isolated symbol (if querying isolated margin)
        :type isolatedSymbol: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "amount": "3.59498107"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "margin/maxTransferable", signed=True, data=params
        )


    def get_margin_delist_schedule(self, **params):
        """Get tokens or symbols delist schedule for cross margin and isolated margin

        https://developers.binance.com/docs/margin_trading/market-data/Get-Delist-Schedule

        :param recvWindow: optional - the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python
            [
                {
                    "delistTime": 1686161202000,
                    "crossMarginAssets": [
                        "BTC",
                        "USDT"
                    ],
                    "isolatedMarginSymbols": [
                        "ADAUSDT",
                        "BNBUSDT"
                    ]
                },
                {
                    "delistTime": 1686222232000,
                    "crossMarginAssets": [
                        "ADA"
                    ],
                    "isolatedMarginSymbols": []
                }
            ]
        """
        return self._request_margin_api(
            "get", "/margin/delist-schedule", signed=True, data=params
        )

    # Margin OCO


    def create_margin_oco_order(self, **params):
        """Post a new OCO trade for margin account.

        https://developers.binance.com/docs/margin_trading/trade/Margin-Account-New-OCO


        :param symbol: required
        :type symbol: str
        :param isIsolated: for isolated margin or not, "TRUE", "FALSE", default "FALSE"
        :type symbol: str
        :param listClientOrderId: A unique id for the list order. Automatically generated if not sent.
        :type listClientOrderId: str
        :param side: required
        :type side: str
        :param quantity: required
        :type quantity: decimal
        :param limitClientOrderId: A unique id for the limit order. Automatically generated if not sent.
        :type limitClientOrderId: str
        :param price: required
        :type price: str
        :param limitIcebergQty: Used to make the LIMIT_MAKER leg an iceberg order.
        :type limitIcebergQty: decimal
        :param stopClientOrderId: A unique Id for the stop loss/stop loss limit leg. Automatically generated if not sent.
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
        :param sideEffectType: NO_SIDE_EFFECT, MARGIN_BUY, AUTO_REPAY; default NO_SIDE_EFFECT.
        :type sideEffectType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "orderListId": 0,
                "contingencyType": "OCO",
                "listStatusType": "EXEC_STARTED",
                "listOrderStatus": "EXECUTING",
                "listClientOrderId": "JYVpp3F0f5CAG15DhtrqLp",
                "transactionTime": 1563417480525,
                "symbol": "LTCBTC",
                "marginBuyBorrowAmount": "5",       // will not return if no margin trade happens
                "marginBuyBorrowAsset": "BTC",    // will not return if no margin trade happens
                "isIsolated": false,       // if isolated margin
                "orders": [
                    {
                        "symbol": "LTCBTC",
                        "orderId": 2,
                        "clientOrderId": "Kk7sqHb9J6mJWTMDVW7Vos"
                    },
                    {
                        "symbol": "LTCBTC",
                        "orderId": 3,
                        "clientOrderId": "xTXKaGYd4bluPVp78IVRvl"
                    }
                ],
                "orderReports": [
                    {
                        "symbol": "LTCBTC",
                        "orderId": 2,
                        "orderListId": 0,
                        "clientOrderId": "Kk7sqHb9J6mJWTMDVW7Vos",
                        "transactTime": 1563417480525,
                        "price": "0.000000",
                        "origQty": "0.624363",
                        "executedQty": "0.000000",
                        "cummulativeQuoteQty": "0.000000",
                        "status": "NEW",
                        "timeInForce": "GTC",
                        "type": "STOP_LOSS",
                        "side": "BUY",
                        "stopPrice": "0.960664"
                    },
                    {
                        "symbol": "LTCBTC",
                        "orderId": 3,
                        "orderListId": 0,
                        "clientOrderId": "xTXKaGYd4bluPVp78IVRvl",
                        "transactTime": 1563417480525,
                        "price": "0.036435",
                        "origQty": "0.624363",
                        "executedQty": "0.000000",
                        "cummulativeQuoteQty": "0.000000",
                        "status": "NEW",
                        "timeInForce": "GTC",
                        "type": "LIMIT_MAKER",
                        "side": "BUY"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException,
            BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
            BinanceOrderInactiveSymbolException

        """
        return self._request_margin_api(
            "post", "margin/order/oco", signed=True, data=params
        )


    def cancel_margin_oco_order(self, **params):
        """Cancel an entire Order List for a margin account.

        https://developers.binance.com/docs/margin_trading/trade/Margin-Account-Cancel-OCO

        :param symbol: required
        :type symbol: str
        :param isIsolated: for isolated margin or not, "TRUE", "FALSE", default "FALSE"
        :type symbol: str
        :param orderListId: Either orderListId or listClientOrderId must be provided
        :type orderListId: int
        :param listClientOrderId: Either orderListId or listClientOrderId must be provided
        :type listClientOrderId: str
        :param newClientOrderId: Used to uniquely identify this cancel. Automatically generated by default.
        :type newClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "orderListId": 0,
                "contingencyType": "OCO",
                "listStatusType": "ALL_DONE",
                "listOrderStatus": "ALL_DONE",
                "listClientOrderId": "C3wyj4WVEktd7u9aVBRXcN",
                "transactionTime": 1574040868128,
                "symbol": "LTCBTC",
                "isIsolated": false,       // if isolated margin
                "orders": [
                    {
                        "symbol": "LTCBTC",
                        "orderId": 2,
                        "clientOrderId": "pO9ufTiFGg3nw2fOdgeOXa"
                    },
                    {
                        "symbol": "LTCBTC",
                        "orderId": 3,
                        "clientOrderId": "TXOvglzXuaubXAaENpaRCB"
                    }
                ],
                "orderReports": [
                    {
                        "symbol": "LTCBTC",
                        "origClientOrderId": "pO9ufTiFGg3nw2fOdgeOXa",
                        "orderId": 2,
                        "orderListId": 0,
                        "clientOrderId": "unfWT8ig8i0uj6lPuYLez6",
                        "price": "1.00000000",
                        "origQty": "10.00000000",
                        "executedQty": "0.00000000",
                        "cummulativeQuoteQty": "0.00000000",
                        "status": "CANCELED",
                        "timeInForce": "GTC",
                        "type": "STOP_LOSS_LIMIT",
                        "side": "SELL",
                        "stopPrice": "1.00000000"
                    },
                    {
                        "symbol": "LTCBTC",
                        "origClientOrderId": "TXOvglzXuaubXAaENpaRCB",
                        "orderId": 3,
                        "orderListId": 0,
                        "clientOrderId": "unfWT8ig8i0uj6lPuYLez6",
                        "price": "3.00000000",
                        "origQty": "10.00000000",
                        "executedQty": "0.00000000",
                        "cummulativeQuoteQty": "0.00000000",
                        "status": "CANCELED",
                        "timeInForce": "GTC",
                        "type": "LIMIT_MAKER",
                        "side": "SELL"
                    }
                ]
            }

        """
        return self._request_margin_api(
            "delete", "margin/orderList", signed=True, data=params
        )


    def get_margin_oco_order(self, **params):
        """Retrieves a specific OCO based on provided optional parameters

        https://developers.binance.com/docs/margin_trading/trade/Query-Margin-Account-OCO

        :param isIsolated: for isolated margin or not, "TRUE", "FALSE", default "FALSE"
        :type symbol: str
        :param symbol: mandatory for isolated margin, not supported for cross margin
        :type symbol: str
        :param orderListId: Either orderListId or listClientOrderId must be provided
        :type orderListId: int
        :param listClientOrderId: Either orderListId or listClientOrderId must be provided
        :type listClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "orderListId": 27,
                "contingencyType": "OCO",
                "listStatusType": "EXEC_STARTED",
                "listOrderStatus": "EXECUTING",
                "listClientOrderId": "h2USkA5YQpaXHPIrkd96xE",
                "transactionTime": 1565245656253,
                "symbol": "LTCBTC",
                "isIsolated": false,       // if isolated margin
                "orders": [
                    {
                        "symbol": "LTCBTC",
                        "orderId": 4,
                        "clientOrderId": "qD1gy3kc3Gx0rihm9Y3xwS"
                    },
                    {
                        "symbol": "LTCBTC",
                        "orderId": 5,
                        "clientOrderId": "ARzZ9I00CPM8i3NhmU9Ega"
                    }
                ]
            }

        """
        return self._request_margin_api(
            "get", "margin/orderList", signed=True, data=params
        )


    def get_open_margin_oco_orders(self, **params):
        """Retrieves open OCO trades

        https://developers.binance.com/docs/margin_trading/trade/Query-Margin-Account-Open-OCO

        :param isIsolated: for isolated margin or not, "TRUE", "FALSE", default "FALSE"
        :type symbol: str
        :param symbol: mandatory for isolated margin, not supported for cross margin
        :type symbol: str
        :param fromId: If supplied, neither startTime or endTime can be provided
        :type fromId: int
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param limit: optional Default Value: 500; Max Value: 1000
        :type limit: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            [
                {
                    "orderListId": 29,
                    "contingencyType": "OCO",
                    "listStatusType": "EXEC_STARTED",
                    "listOrderStatus": "EXECUTING",
                    "listClientOrderId": "amEEAXryFzFwYF1FeRpUoZ",
                    "transactionTime": 1565245913483,
                    "symbol": "LTCBTC",
                    "isIsolated": true,       // if isolated margin
                    "orders": [
                        {
                            "symbol": "LTCBTC",
                            "orderId": 4,
                            "clientOrderId": "oD7aesZqjEGlZrbtRpy5zB"
                        },
                        {
                            "symbol": "LTCBTC",
                            "orderId": 5,
                            "clientOrderId": "Jr1h6xirOxgeJOUuYQS7V3"
                        }
                    ]
                },
                {
                    "orderListId": 28,
                    "contingencyType": "OCO",
                    "listStatusType": "EXEC_STARTED",
                    "listOrderStatus": "EXECUTING",
                    "listClientOrderId": "hG7hFNxJV6cZy3Ze4AUT4d",
                    "transactionTime": 1565245913407,
                    "symbol": "LTCBTC",
                    "orders": [
                        {
                            "symbol": "LTCBTC",
                            "orderId": 2,
                            "clientOrderId": "j6lFOfbmFMRjTYA7rRJ0LP"
                        },
                        {
                            "symbol": "LTCBTC",
                            "orderId": 3,
                            "clientOrderId": "z0KCjOdditiLS5ekAFtK81"
                        }
                    ]
                }
            ]

        """
        return self._request_margin_api(
            "get", "margin/openOrderList", signed=True, data=params
        )

    # Cross-margin


    def margin_stream_get_listen_key(self):
        """Start a new cross-margin data stream and return the listen key
        If a stream already exists it should return the same key.
        If the stream becomes invalid a new key is returned.

        Can be used to keep the stream alive.

        https://developers.binance.com/docs/margin_trading/trade-data-stream/Start-Margin-User-Data-Stream

        :returns: API response

        .. code-block:: python

            {
                "listenKey": "pqia91ma19a5s61cv6a81va65sdf19v8a65a1a5s61cv6a81va65sdf19v8a65a1"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        res = self._request_margin_api("post", "userDataStream", signed=False, data={})
        return res["listenKey"]


    def margin_stream_keepalive(self, listenKey):
        """PING a cross-margin data stream to prevent a time out.

        https://developers.binance.com/docs/margin_trading/trade-data-stream/Keepalive-Margin-User-Data-Stream

        :param listenKey: required
        :type listenKey: str

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        params = {"listenKey": listenKey}
        return self._request_margin_api(
            "put", "userDataStream", signed=False, data=params
        )


    def margin_stream_close(self, listenKey):
        """Close out a cross-margin data stream.

        https://developers.binance.com/docs/margin_trading/trade-data-stream/Close-Margin-User-Data-Stream

        :param listenKey: required
        :type listenKey: str

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        params = {"listenKey": listenKey}
        return self._request_margin_api(
            "delete", "userDataStream", signed=False, data=params
        )

    # Isolated margin


    def isolated_margin_stream_get_listen_key(self, symbol):
        """Start a new isolated margin data stream and return the listen key
        If a stream already exists it should return the same key.
        If the stream becomes invalid a new key is returned.

        Can be used to keep the stream alive.

        https://developers.binance.com/docs/margin_trading/trade-data-stream/Start-Isolated-Margin-User-Data-Stream

        :param symbol: required - symbol for the isolated margin account
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "listenKey":  "T3ee22BIYuWqmvne0HNq2A2WsFlEtLhvWCtItw6ffhhdmjifQ2tRbuKkTHhr"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        params = {"symbol": symbol}
        res = self._request_margin_api(
            "post", "userDataStream/isolated", signed=False, data=params
        )
        return res["listenKey"]


    def isolated_margin_stream_keepalive(self, symbol, listenKey):
        """PING an isolated margin data stream to prevent a time out.

        https://developers.binance.com/docs/margin_trading/trade-data-stream/Keepalive-Isolated-Margin-User-Data-Stream

        :param symbol: required - symbol for the isolated margin account
        :type symbol: str
        :param listenKey: required
        :type listenKey: str

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        params = {"symbol": symbol, "listenKey": listenKey}
        return self._request_margin_api(
            "put", "userDataStream/isolated", signed=False, data=params
        )


    def isolated_margin_stream_close(self, symbol, listenKey):
        """Close out an isolated margin data stream.

        https://developers.binance.com/docs/margin_trading/trade-data-stream/Close-Isolated-Margin-User-Data-Stream

        :param symbol: required - symbol for the isolated margin account
        :type symbol: str
        :param listenKey: required
        :type listenKey: str

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        params = {"symbol": symbol, "listenKey": listenKey}
        return self._request_margin_api(
            "delete", "userDataStream/isolated", signed=False, data=params
        )

    # Simple Earn Endpoints


    def get_simple_earn_flexible_product_list(self, **params):
        """Get available Simple Earn flexible product list

        https://binance-docs.github.io/apidocs/spot/en/#get-simple-earn-flexible-product-list-user_data

        :param asset: optional
        :type asset: str
        :param current: optional - Currently querying page. Start from 1. Default:1
        :type current: int
        :param size: optional - Default:10, Max:100
        :type size: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
               "rows":[
                   {
                       "asset": "BTC",
                       "latestAnnualPercentageRate": "0.05000000",
                       "tierAnnualPercentageRate": {
                       "0-5BTC": 0.05,
                       "5-10BTC": 0.03
                   },
                       "airDropPercentageRate": "0.05000000",
                       "canPurchase": true,
                       "canRedeem": true,
                       "isSoldOut": true,
                       "hot": true,
                       "minPurchaseAmount": "0.01000000",
                       "productId": "BTC001",
                       "subscriptionStartTime": "1646182276000",
                       "status": "PURCHASING"
                   }
               ],
               "total": 1
           }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "simple-earn/flexible/list", signed=True, data=params
        )


    def get_simple_earn_locked_product_list(self, **params):
        """Get available Simple Earn flexible product list

        https://binance-docs.github.io/apidocs/spot/en/#get-simple-earn-locked-product-list-user_data

        :param asset: optional
        :type asset: str
        :param current: optional - Currently querying page. Start from 1. Default:1
        :type current: int
        :param size: optional - Default:10, Max:100
        :type size: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
               "rows": [
                   {
                       "projectId": "Axs*90",
                       "detail": {
                           "asset": "AXS",
                           "rewardAsset": "AXS",
                           "duration": 90,
                           "renewable": true,
                           "isSoldOut": true,
                           "apr": "1.2069",
                           "status": "CREATED",
                           "subscriptionStartTime": "1646182276000",
                           "extraRewardAsset": "BNB",
                           "extraRewardAPR": "0.23"
                       },
                       "quota": {
                           "totalPersonalQuota": "2",
                           "minimum": "0.001"
                       }
                   }
               ],
               "total": 1
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "simple-earn/locked/list", signed=True, data=params
        )


    def subscribe_simple_earn_flexible_product(self, **params):
        """Subscribe to a simple earn flexible product

        https://binance-docs.github.io/apidocs/spot/en/#subscribe-locked-product-trade

        :param productId: required
        :type productId: str
        :param amount: required
        :type amount: str
        :param autoSubscribe: optional - Default True
        :type autoSubscribe: bool
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
               "purchaseId": 40607,
               "success": true
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "post", "simple-earn/flexible/subscribe", signed=True, data=params
        )


    def subscribe_simple_earn_locked_product(self, **params):
        """Subscribe to a simple earn locked product

        https://binance-docs.github.io/apidocs/spot/en/#subscribe-locked-product-trade

        :param productId: required
        :type productId: str
        :param amount: required
        :type amount: str
        :param autoSubscribe: optional - Default True
        :type autoSubscribe: bool
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
               "purchaseId": 40607,
               "positionId": "12345",
               "success": true
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "post", "simple-earn/locked/subscribe", signed=True, data=params
        )


    def redeem_simple_earn_flexible_product(self, **params):
        """Redeem a simple earn flexible product

        https://binance-docs.github.io/apidocs/spot/en/#redeem-flexible-product-trade

        :param productId: required
        :type productId: str
        :param amount: optional
        :type amount: str
        :param redeemAll: optional - Default False
        :type redeemAll: bool
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

           {
               "redeemId": 40607,
               "success": true
           }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "post", "simple-earn/flexible/redeem", signed=True, data=params
        )


    def redeem_simple_earn_locked_product(self, **params):
        """Redeem a simple earn locked product

        https://binance-docs.github.io/apidocs/spot/en/#redeem-locked-product-trade

        :param productId: required
        :type productId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

           {
               "redeemId": 40607,
               "success": true
           }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "post", "simple-earn/locked/redeem", signed=True, data=params
        )


    def get_simple_earn_flexible_product_position(self, **params):
        """

        https://binance-docs.github.io/apidocs/spot/en/#get-flexible-product-position-user_data

        :param asset: optional
        :type asset: str
        :param current: optional - Currently querying page. Start from 1. Default:1
        :type current: int
        :param size: optional - Default:10, Max:100
        :type size: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

           {
               "rows":[
                   {
                       "totalAmount": "75.46000000",
                       "tierAnnualPercentageRate": {
                       "0-5BTC": 0.05,
                       "5-10BTC": 0.03
                   },
                       "latestAnnualPercentageRate": "0.02599895",
                       "yesterdayAirdropPercentageRate": "0.02599895",
                       "asset": "USDT",
                       "airDropAsset": "BETH",
                       "canRedeem": true,
                       "collateralAmount": "232.23123213",
                       "productId": "USDT001",
                       "yesterdayRealTimeRewards": "0.10293829",
                       "cumulativeBonusRewards": "0.22759183",
                       "cumulativeRealTimeRewards": "0.22759183",
                       "cumulativeTotalRewards": "0.45459183",
                       "autoSubscribe": true
                   }
               ],
               "total": 1
           }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "simple-earn/flexible/position", signed=True, data=params
        )


    def get_simple_earn_locked_product_position(self, **params):
        """

        https://binance-docs.github.io/apidocs/spot/en/#get-locked-product-position-user_data

        :param asset: optional
        :type asset: str
        :param current: optional - Currently querying page. Start from 1. Default:1
        :type current: int
        :param size: optional - Default:10, Max:100
        :type size: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

           {
               "rows":[
                   {
                       "positionId": "123123",
                       "projectId": "Axs*90",
                       "asset": "AXS",
                       "amount": "122.09202928",
                       "purchaseTime": "1646182276000",
                       "duration": "60",
                       "accrualDays": "4",
                       "rewardAsset": "AXS",
                       "APY": "0.23",
                       "isRenewable": true,
                       "isAutoRenew": true,
                       "redeemDate": "1732182276000"
                   }
               ],
               "total": 1
           }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "simple-earn/locked/position", signed=True, data=params
        )


    def get_simple_earn_account(self, **params):
        """

        https://binance-docs.github.io/apidocs/spot/en/#simple-account-user_data

        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

           {
               "totalAmountInBTC": "0.01067982",
               "totalAmountInUSDT": "77.13289230",
               "totalFlexibleAmountInBTC": "0.00000000",
               "totalFlexibleAmountInUSDT": "0.00000000",
               "totalLockedInBTC": "0.01067982",
               "totalLockedInUSDT": "77.13289230"
           }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "simple-earn/account", signed=True, data=params
        )

    # Lending Endpoints


    def get_fixed_activity_project_list(self, **params):
        """Get Fixed and Activity Project List

        https://binance-docs.github.io/apidocs/spot/en/#get-fixed-and-activity-project-list-user_data

        :param asset: optional
        :type asset: str
        :param type: required - "ACTIVITY", "CUSTOMIZED_FIXED"
        :type type: str
        :param status: optional - "ALL", "SUBSCRIBABLE", "UNSUBSCRIBABLE"; default "ALL"
        :type status: str
        :param sortBy: optional - "START_TIME", "LOT_SIZE", "INTEREST_RATE", "DURATION"; default "START_TIME"
        :type sortBy: str
        :param current: optional - Currently querying page. Start from 1. Default:1
        :type current: int
        :param size: optional - Default:10, Max:100
        :type size: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "asset": "USDT",
                    "displayPriority": 1,
                    "duration": 90,
                    "interestPerLot": "1.35810000",
                    "interestRate": "0.05510000",
                    "lotSize": "100.00000000",
                    "lotsLowLimit": 1,
                    "lotsPurchased": 74155,
                    "lotsUpLimit": 80000,
                    "maxLotsPerUser": 2000,
                    "needKyc": False,
                    "projectId": "CUSDT90DAYSS001",
                    "projectName": "USDT",
                    "status": "PURCHASING",
                    "type": "CUSTOMIZED_FIXED",
                    "withAreaLimitation": False
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "lending/project/list", signed=True, data=params
        )


    def change_fixed_activity_to_daily_position(self, **params):
        """Change Fixed/Activity Position to Daily Position

        https://binance-docs.github.io/apidocs/spot/en/#change-fixed-activity-position-to-daily-position-user_data

        """
        return self._request_margin_api(
            "post", "lending/positionChanged", signed=True, data=params
        )

    # Staking Endpoints


    def get_staking_product_list(self, **params):
        """Get Staking Product List

        https://binance-docs.github.io/apidocs/spot/en/#get-staking-product-list-user_data

        """
        return self._request_margin_api(
            "get", "staking/productList", signed=True, data=params
        )


    def purchase_staking_product(self, **params):
        """Purchase Staking Product

        https://binance-docs.github.io/apidocs/spot/en/#purchase-staking-product-user_data

        """
        return self._request_margin_api(
            "post", "staking/purchase", signed=True, data=params
        )


    def redeem_staking_product(self, **params):
        """Redeem Staking Product

        https://binance-docs.github.io/apidocs/spot/en/#redeem-staking-product-user_data

        """
        return self._request_margin_api(
            "post", "staking/redeem", signed=True, data=params
        )


    def get_staking_position(self, **params):
        """Get Staking Product Position

        https://binance-docs.github.io/apidocs/spot/en/#get-staking-product-position-user_data

        """
        return self._request_margin_api(
            "get", "staking/position", signed=True, data=params
        )


    def get_staking_purchase_history(self, **params):
        """Get Staking Purchase History

        https://binance-docs.github.io/apidocs/spot/en/#get-staking-history-user_data

        """
        return self._request_margin_api(
            "get", "staking/purchaseRecord", signed=True, data=params
        )


    def set_auto_staking(self, **params):
        """Set Auto Staking on Locked Staking or Locked DeFi Staking

        https://binance-docs.github.io/apidocs/spot/en/#set-auto-staking-user_data

        """
        return self._request_margin_api(
            "post", "staking/setAutoStaking", signed=True, data=params
        )


    def get_personal_left_quota(self, **params):
        """Get Personal Left Quota of Staking Product

        https://binance-docs.github.io/apidocs/spot/en/#get-personal-left-quota-of-staking-product-user_data

        """
        return self._request_margin_api(
            "get", "staking/personalLeftQuota", signed=True, data=params
        )

    # US Staking Endpoints


    def get_staking_asset_us(self, **params):
        """Get staking information for a supported asset (or assets)

        https://docs.binance.us/#get-staking-asset-information

        """
        assert self.tld == "us", "Endpoint only available on binance.us"
        return self._request_margin_api("get", "staking/asset", True, data=params)


    def stake_asset_us(self, **params):
        """Stake a supported asset.

        https://docs.binance.us/#stake-asset

        """
        assert self.tld == "us", "Endpoint only available on binance.us"
        return self._request_margin_api("post", "staking/stake", True, data=params)


    def unstake_asset_us(self, **params):
        """Unstake a staked asset

        https://docs.binance.us/#unstake-asset

        """
        assert self.tld == "us", "Endpoint only available on binance.us"
        return self._request_margin_api("post", "staking/unstake", True, data=params)


    def get_staking_balance_us(self, **params):
        """Get staking balance

        https://docs.binance.us/#get-staking-balance

        """
        assert self.tld == "us", "Endpoint only available on binance.us"
        return self._request_margin_api(
            "get", "staking/stakingBalance", True, data=params
        )


    def get_staking_history_us(self, **params):
        """Get staking history

        https://docs.binance.us/#get-staking-history

        """
        assert self.tld == "us", "Endpoint only available on binance.us"
        return self._request_margin_api("get", "staking/history", True, data=params)


    def get_staking_rewards_history_us(self, **params):
        """Get staking rewards history for an asset(or assets) within a given time range.

        https://docs.binance.us/#get-staking-rewards-history

        """
        assert self.tld == "us", "Endpoint only available on binance.us"
        return self._request_margin_api(
            "get", "staking/stakingRewardsHistory", True, data=params
        )

    # Sub Accounts


    def get_sub_account_list(self, **params):
        """Query Sub-account List.

        https://developers.binance.com/docs/sub_account/account-management/Query-Sub-account-List

        :param email: optional - Sub-account email
        :type email: str
        :param isFreeze: optional
        :type isFreeze: str
        :param page: optional - Default value: 1
        :type page: int
        :param limit: optional - Default value: 1, Max value: 200
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "subAccounts":[
                    {
                        "email":"testsub@gmail.com",
                        "isFreeze":false,
                        "createTime":1544433328000
                    },
                    {
                        "email":"virtual@oxebmvfonoemail.com",
                        "isFreeze":false,
                        "createTime":1544433328000
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api("get", "sub-account/list", True, data=params)


    def get_sub_account_transfer_history(self, **params):
        """Query Sub-account Transfer History.

        https://developers.binance.com/docs/sub_account/asset-management/Query-Sub-account-Spot-Asset-Transfer-History

        :param fromEmail: optional
        :type fromEmail: str
        :param toEmail: optional
        :type toEmail: str
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param page: optional - Default value: 1
        :type page: int
        :param limit: optional - Default value: 500
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "from":"aaa@test.com",
                    "to":"bbb@test.com",
                    "asset":"BTC",
                    "qty":"10",
                    "status": "SUCCESS",
                    "tranId": 6489943656,
                    "time":1544433328000
                },
                {
                    "from":"bbb@test.com",
                    "to":"ccc@test.com",
                    "asset":"ETH",
                    "qty":"2",
                    "status": "SUCCESS",
                    "tranId": 6489938713,
                    "time":1544433328000
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "sub-account/sub/transfer/history", True, data=params
        )


    def get_sub_account_futures_transfer_history(self, **params):
        """Query Sub-account Futures Transfer History.

        https://developers.binance.com/docs/sub_account/asset-management/Query-Sub-account-Futures-Asset-Transfer-History

        :param email: required
        :type email: str
        :param futuresType: required
        :type futuresType: int
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param page: optional
        :type page: int
        :param limit: optional
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "success":true,
                "futuresType": 2,
                "transfers":[
                    {
                        "from":"aaa@test.com",
                        "to":"bbb@test.com",
                        "asset":"BTC",
                        "qty":"1",
                        "time":1544433328000
                    },
                    {
                        "from":"bbb@test.com",
                        "to":"ccc@test.com",
                        "asset":"ETH",
                        "qty":"2",
                        "time":1544433328000
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "sub-account/futures/internalTransfer", True, data=params
        )


    def create_sub_account_futures_transfer(self, **params):
        """Execute sub-account Futures transfer

        https://developers.binance.com/docs/sub_account/asset-management/Sub-account-Futures-Asset-Transfer

        :param fromEmail: required - Sender email
        :type fromEmail: str
        :param toEmail: required - Recipient email
        :type toEmail: str
        :param futuresType: required
        :type futuresType: int
        :param asset: required
        :type asset: str
        :param amount: required
        :type amount: decimal
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

           {
                "success":true,
                "txnId":"2934662589"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "post", "sub-account/futures/internalTransfer", True, data=params
        )


    def get_sub_account_assets(self, **params):
        """Fetch sub-account assets

        https://developers.binance.com/docs/sub_account/asset-management/Query-Sub-account-Assets-V4

        :param email: required
        :type email: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "balances":[
                    {
                        "asset":"ADA",
                        "free":10000,
                        "locked":0
                    },
                    {
                        "asset":"BNB",
                        "free":10003,
                        "locked":0
                    },
                    {
                        "asset":"BTC",
                        "free":11467.6399,
                        "locked":0
                    },
                    {
                        "asset":"ETH",
                        "free":10004.995,
                        "locked":0
                    },
                    {
                        "asset":"USDT",
                        "free":11652.14213,
                        "locked":0
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "sub-account/assets", True, data=params, version=4
        )


    def query_subaccount_spot_summary(self, **params):
        """Query Sub-account Spot Assets Summary (For Master Account)

        https://developers.binance.com/docs/sub_account/asset-management/Query-Sub-account-Spot-Assets-Summary

        :param email: optional - Sub account email
        :type email: str
        :param page: optional - default 1
        :type page: int
        :param size: optional - default 10, max 20
        :type size: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

           {
                "totalCount":2,
                "masterAccountTotalAsset": "0.23231201",
                "spotSubUserAssetBtcVoList":[
                    {
                        "email":"sub123@test.com",
                        "totalAsset":"9999.00000000"
                    },
                    {
                        "email":"test456@test.com",
                        "totalAsset":"0.00000000"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "sub-account/spotSummary", True, data=params
        )


    def get_subaccount_deposit_address(self, **params):
        """Get Sub-account Deposit Address (For Master Account)

        https://developers.binance.com/docs/sub_account/asset-management/Get-Sub-account-Deposit-Address

        :param email: required - Sub account email
        :type email: str
        :param coin: required
        :type coin: str
        :param network: optional
        :type network: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

           {
                "address":"TDunhSa7jkTNuKrusUTU1MUHtqXoBPKETV",
                "coin":"USDT",
                "tag":"",
                "url":"https://tronscan.org/#/address/TDunhSa7jkTNuKrusUTU1MUHtqXoBPKETV"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "capital/deposit/subAddress", True, data=params
        )


    def get_subaccount_deposit_history(self, **params):
        """Get Sub-account Deposit History (For Master Account)

        https://developers.binance.com/docs/sub_account/asset-management/Get-Sub-account-Deposit-History

        :param email: required - Sub account email
        :type email: str
        :param coin: optional
        :type coin: str
        :param status: optional - (0:pending,6: credited but cannot withdraw, 1:success)
        :type status: int
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param limit: optional
        :type limit: int
        :param offset: optional - default:0
        :type offset: int
        :param recvWindow: optional
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
            "get", "capital/deposit/subHisrec", True, data=params
        )


    def get_subaccount_futures_margin_status(self, **params):
        """Get Sub-account's Status on Margin/Futures (For Master Account)

        https://developers.binance.com/docs/sub_account/account-management/Get-Sub-accounts-Status-on-Margin-Or-Futures

        :param email: optional - Sub account email
        :type email: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

           [
                {
                    "email":"123@test.com",      // user email
                    "isSubUserEnabled": true,    // true or false
                    "isUserActive": true,        // true or false
                    "insertTime": 1570791523523  // sub account create time
                    "isMarginEnabled": true,     // true or false for margin
                    "isFutureEnabled": true      // true or false for futures.
                    "mobile": 1570791523523      // user mobile number
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api("get", "sub-account/status", True, data=params)


    def enable_subaccount_margin(self, **params):
        """Enable Margin for Sub-account (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#enable-margin-for-sub-account-for-master-account

        :param email: required - Sub account email
        :type email: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

           {

                "email":"123@test.com",

                "isMarginEnabled": true

            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "post", "sub-account/margin/enable", True, data=params
        )


    def get_subaccount_margin_details(self, **params):
        """Get Detail on Sub-account's Margin Account (For Master Account)

        https://developers.binance.com/docs/sub_account/asset-management/Get-Detail-on-Sub-accounts-Margin-Account

        :param email: required - Sub account email
        :type email: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                  "email":"123@test.com",
                  "marginLevel": "11.64405625",
                  "totalAssetOfBtc": "6.82728457",
                  "totalLiabilityOfBtc": "0.58633215",
                  "totalNetAssetOfBtc": "6.24095242",
                  "marginTradeCoeffVo":
                        {
                            "forceLiquidationBar": "1.10000000",  // Liquidation margin ratio
                            "marginCallBar": "1.50000000",        // Margin call margin ratio
                            "normalBar": "2.00000000"             // Initial margin ratio
                        },
                  "marginUserAssetVoList": [
                      {
                          "asset": "BTC",
                          "borrowed": "0.00000000",
                          "free": "0.00499500",
                          "interest": "0.00000000",
                          "locked": "0.00000000",
                          "netAsset": "0.00499500"
                      },
                      {
                          "asset": "BNB",
                          "borrowed": "201.66666672",
                          "free": "2346.50000000",
                          "interest": "0.00000000",
                          "locked": "0.00000000",
                          "netAsset": "2144.83333328"
                      },
                      {
                          "asset": "ETH",
                          "borrowed": "0.00000000",
                          "free": "0.00000000",
                          "interest": "0.00000000",
                          "locked": "0.00000000",
                          "netAsset": "0.00000000"
                      },
                      {
                          "asset": "USDT",
                          "borrowed": "0.00000000",
                          "free": "0.00000000",
                          "interest": "0.00000000",
                          "locked": "0.00000000",
                          "netAsset": "0.00000000"
                      }
                  ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "sub-account/margin/account", True, data=params
        )


    def get_subaccount_margin_summary(self, **params):
        """Get Summary of Sub-account's Margin Account (For Master Account)

        https://developers.binance.com/docs/sub_account/asset-management/Get-Summary-of-Sub-accounts-Margin-Account

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "totalAssetOfBtc": "4.33333333",
                "totalLiabilityOfBtc": "2.11111112",
                "totalNetAssetOfBtc": "2.22222221",
                "subAccountList":[
                    {
                        "email":"123@test.com",
                        "totalAssetOfBtc": "2.11111111",
                        "totalLiabilityOfBtc": "1.11111111",
                        "totalNetAssetOfBtc": "1.00000000"
                    },
                    {
                        "email":"345@test.com",
                        "totalAssetOfBtc": "2.22222222",
                        "totalLiabilityOfBtc": "1.00000001",
                        "totalNetAssetOfBtc": "1.22222221"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "sub-account/margin/accountSummary", True, data=params
        )


    def enable_subaccount_futures(self, **params):
        """Enable Futures for Sub-account (For Master Account)

        https://developers.binance.com/docs/sub_account/account-management/Enable-Futures-for-Sub-account

        :param email: required - Sub account email
        :type email: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {

                "email":"123@test.com",

                "isFuturesEnabled": true  // true or false

            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "post", "sub-account/futures/enable", True, data=params
        )


    def get_subaccount_futures_details(self, **params):
        """Get Detail on Sub-account's Futures Account (For Master Account)

        https://developers.binance.com/docs/sub_account/asset-management/Get-Detail-on-Sub-accounts-Futures-Account

        :param email: required - Sub account email
        :type email: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "email": "abc@test.com",
                "asset": "USDT",
                "assets":[
                    {
                        "asset": "USDT",
                        "initialMargin": "0.00000000",
                        "maintenanceMargin": "0.00000000",
                        "marginBalance": "0.88308000",
                        "maxWithdrawAmount": "0.88308000",
                        "openOrderInitialMargin": "0.00000000",
                        "positionInitialMargin": "0.00000000",
                        "unrealizedProfit": "0.00000000",
                        "walletBalance": "0.88308000"
                     }
                ],
                "canDeposit": true,
                "canTrade": true,
                "canWithdraw": true,
                "feeTier": 2,
                "maxWithdrawAmount": "0.88308000",
                "totalInitialMargin": "0.00000000",
                "totalMaintenanceMargin": "0.00000000",
                "totalMarginBalance": "0.88308000",
                "totalOpenOrderInitialMargin": "0.00000000",
                "totalPositionInitialMargin": "0.00000000",
                "totalUnrealizedProfit": "0.00000000",
                "totalWalletBalance": "0.88308000",
                "updateTime": 1576756674610
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "sub-account/futures/account", True, data=params, version=2
        )


    def get_subaccount_futures_summary(self, **params):
        """Get Summary of Sub-account's Futures Account (For Master Account)

        https://developers.binance.com/docs/sub_account/asset-management/Get-Summary-of-Sub-accounts-Futures-Account-V2

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "totalInitialMargin": "9.83137400",
                "totalMaintenanceMargin": "0.41568700",
                "totalMarginBalance": "23.03235621",
                "totalOpenOrderInitialMargin": "9.00000000",
                "totalPositionInitialMargin": "0.83137400",
                "totalUnrealizedProfit": "0.03219710",
                "totalWalletBalance": "22.15879444",
                "asset": "USDT",
                "subAccountList":[
                    {
                        "email": "123@test.com",
                        "totalInitialMargin": "9.00000000",
                        "totalMaintenanceMargin": "0.00000000",
                        "totalMarginBalance": "22.12659734",
                        "totalOpenOrderInitialMargin": "9.00000000",
                        "totalPositionInitialMargin": "0.00000000",
                        "totalUnrealizedProfit": "0.00000000",
                        "totalWalletBalance": "22.12659734",
                        "asset": "USDT"
                    },
                    {
                        "email": "345@test.com",
                        "totalInitialMargin": "0.83137400",
                        "totalMaintenanceMargin": "0.41568700",
                        "totalMarginBalance": "0.90575887",
                        "totalOpenOrderInitialMargin": "0.00000000",
                        "totalPositionInitialMargin": "0.83137400",
                        "totalUnrealizedProfit": "0.03219710",
                        "totalWalletBalance": "0.87356177",
                        "asset": "USDT"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "sub-account/futures/accountSummary", True, data=params, version=2
        )


    def get_subaccount_futures_positionrisk(self, **params):
        """Get Futures Position-Risk of Sub-account (For Master Account)

        https://developers.binance.com/docs/sub_account/account-management/Get-Futures-Position-Risk-of-Sub-account-V2

        :param email: required - Sub account email
        :type email: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "entryPrice": "9975.12000",
                    "leverage": "50",              // current initial leverage
                    "maxNotional": "1000000",      // notional value limit of current initial leverage
                    "liquidationPrice": "7963.54",
                    "markPrice": "9973.50770517",
                    "positionAmount": "0.010",
                    "symbol": "BTCUSDT",
                    "unrealizedProfit": "-0.01612295"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "sub-account/futures/positionRisk", True, data=params, version=2
        )


    def make_subaccount_futures_transfer(self, **params):
        """Futures Transfer for Sub-account (For Master Account)

        https://developers.binance.com/docs/sub_account/asset-management

        :param email: required - Sub account email
        :type email: str
        :param asset: required - The asset being transferred, e.g., USDT
        :type asset: str
        :param amount: required - The amount to be transferred
        :type amount: float
        :param type: required - 1: transfer from subaccount's spot account to its USDT-margined futures account
                                2: transfer from subaccount's USDT-margined futures account to its spot account
                                3: transfer from subaccount's spot account to its COIN-margined futures account
                                4: transfer from subaccount's COIN-margined futures account to its spot account
        :type type: int

        :returns: API response

        .. code-block:: python

            {
                "txnId":"2966662589"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "post", "sub-account/futures/transfer", True, data=params
        )


    def make_subaccount_margin_transfer(self, **params):
        """Margin Transfer for Sub-account (For Master Account)

        https://developers.binance.com/docs/sub_account/asset-management/Margin-Transfer-for-Sub-account

        :param email: required - Sub account email
        :type email: str
        :param asset: required - The asset being transferred, e.g., USDT
        :type asset: str
        :param amount: required - The amount to be transferred
        :type amount: float
        :param type: required - 1: transfer from subaccount's spot account to margin account
                                2: transfer from subaccount's margin account to its spot account
        :type type: int

        :returns: API response

        .. code-block:: python

            {
                "txnId":"2966662589"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "post", "sub-account/margin/transfer", True, data=params
        )


    def make_subaccount_to_subaccount_transfer(self, **params):
        """Transfer to Sub-account of Same Master (For Sub-account)

        https://developers.binance.com/docs/sub_account/asset-management/Transfer-to-Sub-account-of-Same-Master

        :param toEmail: required - Sub account email
        :type toEmail: str
        :param asset: required - The asset being transferred, e.g., USDT
        :type asset: str
        :param amount: required - The amount to be transferred
        :type amount: float
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "txnId":"2966662589"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "post", "sub-account/transfer/subToSub", True, data=params
        )


    def make_subaccount_to_master_transfer(self, **params):
        """Transfer to Master (For Sub-account)

        https://developers.binance.com/docs/sub_account/asset-management/Transfer-to-Master

        :param asset: required - The asset being transferred, e.g., USDT
        :type asset: str
        :param amount: required - The amount to be transferred
        :type amount: float
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "txnId":"2966662589"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "post", "sub-account/transfer/subToMaster", True, data=params
        )


    def get_subaccount_transfer_history(self, **params):
        """Sub-account Transfer History (For Sub-account)

        https://developers.binance.com/docs/sub_account/asset-management/Sub-account-Transfer-History

        :param asset: required - The asset being transferred, e.g., USDT
        :type asset: str
        :param type: optional - 1: transfer in, 2: transfer out
        :type type: int
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param limit: optional - Default 500
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
              {
                "counterParty":"master",
                "email":"master@test.com",
                "type":1,  // 1 for transfer in, 2 for transfer out
                "asset":"BTC",
                "qty":"1",
                "status":"SUCCESS",
                "tranId":11798835829,
                "time":1544433325000
              },
              {
                "counterParty":"subAccount",
                "email":"sub2@test.com",
                "type":2,
                "asset":"ETH",
                "qty":"2",
                "status":"SUCCESS",
                "tranId":11798829519,
                "time":1544433326000
              }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "sub-account/transfer/subUserHistory", True, data=params
        )


    def make_subaccount_universal_transfer(self, **params):
        """Universal Transfer (For Master Account)

        https://developers.binance.com/docs/sub_account/asset-management/Universal-Transfer

        :param fromEmail: optional
        :type fromEmail: str
        :param toEmail: optional
        :type toEmail: str
        :param fromAccountType: required - "SPOT","USDT_FUTURE","COIN_FUTURE"
        :type fromAccountType: str
        :param toAccountType: required - "SPOT","USDT_FUTURE","COIN_FUTURE"
        :type toAccountType: str
        :param asset: required - The asset being transferred, e.g., USDT
        :type asset: str
        :param amount: required
        :type amount: float
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "tranId":11945860693
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "post", "sub-account/universalTransfer", True, data=params
        )


    def get_universal_transfer_history(self, **params):
        """Universal Transfer (For Master Account)

        https://developers.binance.com/docs/sub_account/asset-management/Query-Universal-Transfer-History

        :param fromEmail: optional
        :type fromEmail: str
        :param toEmail: optional
        :type toEmail: str
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param page: optional
        :type page: int
        :param limit: optional
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
              {
                "tranId":11945860693,
                "fromEmail":"master@test.com",
                "toEmail":"subaccount1@test.com",
                "asset":"BTC",
                "amount":"0.1",
                "fromAccountType":"SPOT",
                "toAccountType":"COIN_FUTURE",
                "status":"SUCCESS",
                "createTimeStamp":1544433325000
              },
              {
                "tranId":11945857955,
                "fromEmail":"master@test.com",
                "toEmail":"subaccount2@test.com",
                "asset":"ETH",
                "amount":"0.2",
                "fromAccountType":"SPOT",
                "toAccountType":"USDT_FUTURE",
                "status":"SUCCESS",
                "createTimeStamp":1544433326000
              }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api(
            "get", "sub-account/universalTransfer", True, data=params
        )

    
