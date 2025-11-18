# Derivative CM Futures

币安币本位合约（Coin-Margined Futures）接口，提供币本位永续和交割合约交易功能 (/dapi)。

### futures_coin_ping()
说明：Test connectivity to the Rest API | [源码](同步 binance/client.py:8112-8118, 异步 binance/async_client.py:2113-2114) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_time()
说明：Test connectivity to the Rest API and get the current server time. | [源码](同步 binance/client.py:8120-8126, 异步 binance/async_client.py:2116-2117) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Check-Server-time)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_exchange_info()
说明：Current exchange trading rules and symbol information | [源码](同步 binance/client.py:8128-8134, 异步 binance/async_client.py:2119-2120) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Exchange-Information)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_order_book(**params)
说明：Get the Order Book for the market | [源码](同步 binance/client.py:8136-8142, 异步 binance/async_client.py:2122-2123) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Order-Book)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_recent_trades(**params)
说明：Get recent trades (up to last 500). | [源码](同步 binance/client.py:8144-8150, 异步 binance/async_client.py:2125-2126) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Recent-Trades-List)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_historical_trades(**params)
说明：Get older market historical trades. | [源码](同步 binance/client.py:8152-8158, 异步 binance/async_client.py:2128-2131) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Old-Trades-Lookup)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_aggregate_trades(**params)
说明：Get compressed, aggregate trades. Trades that fill at the time, from the same order, with the same | [源码](同步 binance/client.py:8160-8167, 异步 binance/async_client.py:2133-2134) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Compressed-Aggregate-Trades-List)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_klines(**params)
说明：Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time. | [源码](同步 binance/client.py:8169-8175, 异步 binance/async_client.py:2136-2137) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Kline-Candlestick-Data)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_continous_klines(**params)
说明：Kline/candlestick bars for a specific contract type. Klines are uniquely identified by their open time. | [源码](同步 binance/client.py:8177-8183, 异步 binance/async_client.py:2139-2142) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Continuous-Contract-Kline-Candlestick-Data)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_index_price_klines(**params)
说明：Kline/candlestick bars for the index price of a pair.. | [源码](同步 binance/client.py:8185-8191, 异步 binance/async_client.py:2144-2147) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Index-Price-Kline-Candlestick-Data)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_premium_index_klines(**params)
说明：Kline/candlestick bars for the index price of a pair.. | [源码](同步 binance/client.py:8193-8199, 异步 binance/async_client.py:2156-2159) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Premium-Index-Kline-Data)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_mark_price_klines(**params)
说明：Kline/candlestick bars for the index price of a pair.. | [源码](同步 binance/client.py:8201-8207, 异步 binance/async_client.py:2149-2152) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Mark-Price-Kline-Candlestick-Data)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_mark_price(**params)
说明：Get Mark Price and Funding Rate | [源码](同步 binance/client.py:8209-8215, 异步 binance/async_client.py:2165-2166) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Index-Price-and-Mark-Price)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_funding_rate(**params)
说明：Get funding rate history | [源码](同步 binance/client.py:8217-8223, 异步 binance/async_client.py:2168-2169) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Get-Funding-Rate-History-of-Perpetual-Futures)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_ticker(**params)
说明：24 hour rolling window price change statistics. | [源码](同步 binance/client.py:8225-8231, 异步 binance/async_client.py:2171-2172) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/24hr-Ticker-Price-Change-Statistics)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_symbol_ticker(**params)
说明：Latest price for a symbol or symbols. | [源码](同步 binance/client.py:8233-8239, 异步 binance/async_client.py:2174-2175) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Symbol-Price-Ticker)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_orderbook_ticker(**params)
说明：Best price/qty on the order book for a symbol or symbols. | [源码](同步 binance/client.py:8241-8247, 异步 binance/async_client.py:2177-2180) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Symbol-Order-Book-Ticker)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_top_longshort_position_ratio(**params)
说明：Get present long to short ratio for top positions of a specific symbol. | [源码](同步 binance/client.py:8249-8254, 异步 暂无对应实现) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Top-Trader-Long-Short-Ratio)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_top_longshort_account_ratio(**params)
说明：Get present long to short ratio for top positions of a specific symbol. | [源码](同步 binance/client.py:8256-8261, 异步 暂无对应实现) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Top-Long-Short-Account-Ratio)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_global_longshort_ratio(**params)
说明：Get present long to short ratio for top positions of a specific symbol. | [源码](同步 binance/client.py:8263-8268, 异步 暂无对应实现) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Long-Short-Ratio)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_taker_buy_sell_volume(**params)
说明：Get present long to short ratio for top positions of a specific symbol. | [源码](同步 binance/client.py:8270-8275, 异步 暂无对应实现) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Taker-Buy-Sell-Volume)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_basis(**params)
说明：Get future basis of a specific symbol | [源码](同步 binance/client.py:8277-8282, 异步 暂无对应实现) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Basis)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_index_price_constituents(**params)
说明：Get index price constituents | [源码](同步 binance/client.py:8284-8290, 异步 binance/async_client.py:2182-2183) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Index-Constituents)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_liquidation_orders(**params)
说明：Get all liquidation orders | [源码](同步 binance/client.py:8292-8300, 异步 binance/async_client.py:2189-2192) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Users-Force-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_open_interest(**params)
说明：Get present open interest of a specific symbol. | [源码](同步 binance/client.py:8302-8308, 异步 binance/async_client.py:2194-2195) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Open-Interest)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_open_interest_hist(**params)
说明：Get open interest statistics of a specific symbol. | [源码](同步 binance/client.py:8310-8318, 异步 binance/async_client.py:2197-2200) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Open-Interest-Statistics)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_leverage_bracket(**params)
说明：Notional and Leverage Brackets | [源码](同步 binance/client.py:8320-8328, 异步 binance/async_client.py:2202-2205) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/account/rest-api/Notional-Bracket-for-Symbol)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_create_order(**params)
说明：Send in a new order. | [源码](同步 binance/client.py:8367-8375, 异步 binance/async_client.py:2227-2230) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_place_batch_order(**params)
说明：Send in new orders. | [源码](同步 binance/client.py:8377-8393, 异步 binance/async_client.py:2232-2242) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Place-Multiple-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_modify_order(**params)
说明：Modify an existing order. Currently only LIMIT order modification is supported. | [源码](同步 binance/client.py:8395-8401, 异步 暂无对应实现) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Modify-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_get_order(**params)
说明：Check an order's status. | [源码](同步 binance/client.py:8403-8409, 异步 binance/async_client.py:2244-2245) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Query-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_get_open_orders(**params)
说明：Get all open orders on a symbol. | [源码](同步 binance/client.py:8411-8417, 异步 binance/async_client.py:2247-2250) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Current-All-Open-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_get_all_orders(**params)
说明：Get all futures account orders; active, canceled, or filled. | [源码](同步 binance/client.py:8419-8427, 异步 binance/async_client.py:2252-2255) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/All-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_cancel_order(**params)
说明：Cancel an active futures order. | [源码](同步 binance/client.py:8429-8437, 异步 binance/async_client.py:2257-2260) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Cancel-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_cancel_all_open_orders(**params)
说明：Cancel all open futures orders | [源码](同步 binance/client.py:8439-8447, 异步 binance/async_client.py:2262-2265) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Cancel-All-Open-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_cancel_orders(**params)
说明：Cancel multiple futures orders | [源码](同步 binance/client.py:8449-8465, 异步 binance/async_client.py:2267-2278) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Cancel-Multiple-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_countdown_cancel_all(**params)
说明：Cancel all open orders of the specified symbol at the end of the specified countdown. | [源码](同步 binance/client.py:8467-8490, 异步 暂无对应实现) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Auto-Cancel-All-Open-Orders)

**核心参数**:
- ✅ **必需**: symbol (str) : required, countdownTime (int) : required
- ☑️ **可选**: recvWindow (int) : optional - the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "symbol": "BTCUSDT", "countdownTime": "100000" }；详见官方文档

### futures_coin_get_open_order(**params)
说明：Get current open order. | [源码](同步 binance/client.py:8492-8500, 异步 暂无对应实现) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Query-Current-Open-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_account_balance(**params)
说明：Get futures account balance | [源码](同步 binance/client.py:8502-8510, 异步 binance/async_client.py:2280-2283) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/account/rest-api/Futures-Account-Balance)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_account(**params)
说明：Get current account information. | [源码](同步 binance/client.py:8512-8520, 异步 binance/async_client.py:2285-2288) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/account/rest-api/Account-Information)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_change_leverage(**params)
说明：Change user's initial leverage of specific symbol market | [源码](同步 binance/client.py:8522-8530, 异步 binance/async_client.py:2290-2293) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Change-Initial-Leverage)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_change_margin_type(**params)
说明：Change the margin type for a symbol | [源码](同步 binance/client.py:8532-8540, 异步 binance/async_client.py:2295-2298) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Change-Margin-Type)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_change_position_margin(**params)
说明：Change the position margin for a symbol | [源码](同步 binance/client.py:8542-8550, 异步 binance/async_client.py:2300-2303) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Modify-Isolated-Position-Margin)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_position_margin_history(**params)
说明：Get position margin change history | [源码](同步 binance/client.py:8552-8560, 异步 binance/async_client.py:2305-2308) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Get-Position-Margin-Change-History)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_position_information(**params)
说明：Get position information | [源码](同步 binance/client.py:8562-8568, 异步 binance/async_client.py:2310-2313) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Position-Information)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_account_trades(**params)
说明：Get trades for the authenticated account and symbol. | [源码](同步 binance/client.py:8570-8576, 异步 binance/async_client.py:2315-2318) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Account-Trade-List)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_income_history(**params)
说明：Get income history for authenticated account | [源码](同步 binance/client.py:8578-8584, 异步 binance/async_client.py:2320-2321) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/account/rest-api/Get-Income-History)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_change_position_mode(**params)
说明：Change user's position mode (Hedge Mode or One-way Mode ) on EVERY symbol | [源码](同步 binance/client.py:8586-8594, 异步 binance/async_client.py:2323-2326) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Change-Position-Mode)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_get_position_mode(**params)
说明：Get user's position mode (Hedge Mode or One-way Mode ) on EVERY symbol | [源码](同步 binance/client.py:8596-8604, 异步 binance/async_client.py:2328-2331) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/account/rest-api/Get-Current-Position-Mode)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_stream_get_listen_key()
说明：参考源码注释 | [源码](同步 binance/client.py:8606-8608, 异步 binance/async_client.py:2333-2337) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_stream_keepalive(listenKey)
说明：参考源码注释 | [源码](同步 binance/client.py:8610-8614, 异步 binance/async_client.py:2339-2343) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_stream_close(listenKey)
说明：参考源码注释 | [源码](同步 binance/client.py:8616-8620, 异步 binance/async_client.py:2381-2385) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_account_order_history_download(**params)
说明：Get Download Id For Futures Order History | [源码](同步 binance/client.py:8622-8652, 异步 binance/async_client.py:2345-2348) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/account/rest-api/Get-Download-Id-For-Futures-Order-History)

**核心参数**:
- ✅ **必需**: startTime (int) : required - Start timestamp in ms, endTime (int) : required - End timestamp in ms
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "avgCostTimestampOfLast30d": 7241837,  # Average time taken for data download in the past 30 days "downloadId": "546975389218332672" } Note: - Request Limitation is 10 times per month, shared by front end download page and rest api - The time between startTime and endTime can not be longer than 1 year；详见官方文档

### futures_coin_accout_order_history_download_link(**params)
说明：Get futures order history download link by Id | [源码](同步 binance/client.py:8654-8693, 异步 暂无对应实现) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/account/rest-api/Get-Futures-Order-History-Download-Link-by-Id)

**核心参数**:
- ✅ **必需**: downloadId (str) : required - Download ID obtained from futures_coin_download_id
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "downloadId": "545923594199212032", "status": "completed",     # Enum：completed，processing "url": "www.binance.com",  # The link is mapped to download id "notified": true,          # ignore "expirationTimestamp": 1645009771000,  # The link would expire after this timestamp "isExpired": null } # OR (Response when server is processing) { "downloadId": "545923594199212032", "status": "processing", "url": "", "notified": false, "expirationTimestamp": -1, "isExpired": null } Note: - Download link expiration: 24h；详见官方文档

### futures_coin_account_trade_history_download(**params)
说明：Get Download Id For Futures Trade History (USER_DATA) | [源码](同步 binance/client.py:8695-8721, 异步 binance/async_client.py:2363-2366) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/account/rest-api/Get-Download-Id-For-Futures-Trade-History)

**核心参数**:
- ✅ **必需**: startTime (int) : required - Start timestamp in ms, endTime (int) : required - End timestamp in ms

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "avgCostTimestampOfLast30d": 7241837,  # Average time taken for data download in the past 30 days "downloadId": "546975389218332672" } Note: - Request Limitation is 5 times per month, shared by front end download page and rest api - The time between startTime and endTime can not be longer than 1 year；详见官方文档

### futures_coin_account_trade_history_download_link(**params)
说明：Get futures trade download link by Id | [源码](同步 binance/client.py:8723-8760, 异步 binance/async_client.py:2372-2375) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/account/rest-api/Get-Futures-Trade-Download-Link-by-Id)

**核心参数**:
- ✅ **必需**: downloadId (str) : required - Download ID obtained from futures_coin_trade_download_id

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "downloadId": "545923594199212032", "status": "completed",     # Enum：completed，processing "url": "www.binance.com",  # The link is mapped to download id "notified": true,          # ignore "expirationTimestamp": 1645009771000,  # The link would expire after this timestamp "isExpired": null } # OR (Response when server is processing) { "downloadId": "545923594199212032", "status": "processing", "url": "", "notified": false, "expirationTimestamp": -1, "isExpired": null } Note: - Download link expiration: 24h；详见官方文档

### futures_coin_v1_get_income_asyn_id(**params)
说明：Placeholder function for GET /dapi/v1/income/asyn/id. | [源码](同步 binance/client.py:14118-14130, 异步 binance/async_client.py:4154-4155) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/account/rest-api/Get-Futures-Transaction-History-Download-Link-by-Id)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_v1_get_order_amendment(**params)
说明：Placeholder function for GET /dapi/v1/orderAmendment. | [源码](同步 binance/client.py:14266-14278, 异步 binance/async_client.py:4209-4210) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Get-Order-Modify-History)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_v1_get_pm_account_info(**params)
说明：Placeholder function for GET /dapi/v1/pmAccountInfo. | [源码](同步 binance/client.py:14334-14346, 异步 binance/async_client.py:4234-4235) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/portfolio-margin-endpoints)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_v1_get_funding_info(**params)
说明：Placeholder function for GET /dapi/v1/fundingInfo. | [源码](同步 binance/client.py:14820-14832, 异步 binance/async_client.py:4423-4424) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/rest-api/Get-Funding-Info)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_v1_get_adl_quantile(**params)
说明：Placeholder function for GET /dapi/v1/adlQuantile. | [源码](同步 binance/client.py:15002-15014, 异步 binance/async_client.py:4488-4489) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Position-ADL-Quantile-Estimation)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_v1_get_income_asyn(**params)
说明：Placeholder function for GET /dapi/v1/income/asyn. | [源码](同步 binance/client.py:15576-15588, 异步 binance/async_client.py:4721-4722) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/account/rest-api/Get-Download-Id-For-Futures-Transaction-History)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_v1_get_commission_rate(**params)
说明：Placeholder function for GET /dapi/v1/commissionRate. | [源码](同步 binance/client.py:16283-16295, 异步 binance/async_client.py:4978-4979) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/account/rest-api/User-Commission-Rate)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_v1_put_order(**params)
说明：Placeholder function for PUT /dapi/v1/order. | [源码](同步 binance/client.py:16391-16403, 异步 binance/async_client.py:5364-5365) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Modify-Order)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_coin_v1_put_batch_orders(**params)
说明：Placeholder function for PUT /dapi/v1/batchOrders. | [源码](同步 binance/client.py:16405-16417, 异步 binance/async_client.py:5021-5022) | [官方文档](https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Modify-Multiple-Orders)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档
