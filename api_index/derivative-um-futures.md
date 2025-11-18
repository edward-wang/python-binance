# Derivative UM Futures

币安U本位合约（USDT-Margined Futures）接口，提供永续合约和交割合约交易功能 (/fapi)。

### futures_ping()
说明：Test connectivity to the Rest API | [源码](同步 binance/client.py:7280-7286, 异步 binance/async_client.py:1707-1708) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_time()
说明：Test connectivity to the Rest API and get the current server time. | [源码](同步 binance/client.py:7288-7294, 异步 binance/async_client.py:1710-1711) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Check-Server-Time)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_exchange_info()
说明：Current exchange trading rules and symbol information | [源码](同步 binance/client.py:7296-7302, 异步 binance/async_client.py:1713-1714) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Exchange-Information)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_order_book(**params)
说明：Get the Order Book for the market | [源码](同步 binance/client.py:7304-7310, 异步 binance/async_client.py:1716-1717) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Order-Book)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_recent_trades(**params)
说明：Get recent trades (up to last 500). | [源码](同步 binance/client.py:7312-7318, 异步 binance/async_client.py:1719-1720) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Recent-Trades-List)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_historical_trades(**params)
说明：Get older market historical trades. | [源码](同步 binance/client.py:7320-7326, 异步 binance/async_client.py:1722-1723) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Old-Trades-Lookup)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_aggregate_trades(**params)
说明：Get compressed, aggregate trades. Trades that fill at the time, from the same order, with the same | [源码](同步 binance/client.py:7328-7335, 异步 binance/async_client.py:1725-1726) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Compressed-Aggregate-Trades-List)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_klines(**params)
说明：Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time. | [源码](同步 binance/client.py:7337-7343, 异步 binance/async_client.py:1728-1729) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Kline-Candlestick-Data)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_mark_price_klines(**params)
说明：Kline/candlestick bars for the mark price of a symbol. Klines are uniquely identified by their open time. | [源码](同步 binance/client.py:7345-7351, 异步 binance/async_client.py:1731-1732) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Mark-Price-Kline-Candlestick-Data)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_index_price_klines(**params)
说明：Kline/candlestick bars for the index price of a symbol. Klines are uniquely identified by their open time. | [源码](同步 binance/client.py:7353-7359, 异步 binance/async_client.py:1736-1737) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Index-Price-Kline-Candlestick-Data)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_premium_index_klines(**params)
说明：Premium index kline bars of a symbol.l. Klines are uniquely identified by their open time. | [源码](同步 binance/client.py:7361-7367, 异步 binance/async_client.py:1741-1742) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Premium-Index-Kline-Data)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_continuous_klines(**params)
说明：Kline/candlestick bars for a specific contract type. Klines are uniquely identified by their open time. | [源码](同步 binance/client.py:7369-7375, 异步 binance/async_client.py:1746-1747) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Continuous-Contract-Kline-Candlestick-Data)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_historical_klines()
说明：Get historical futures klines from Binance | [源码](同步 binance/client.py:7377-7403, 异步 binance/async_client.py:1749-1759) | [官方文档](-)

**核心参数**:
- ☑️ **可选**: end_str (str|int) : optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
- ℹ️ **未标注**: symbol (str) : Name of symbol pair e.g. BNBBTC, interval (str) : Binance Kline interval, start_str (str|int) : Start date string in UTC format or timestamp in milliseconds, limit (int) : Default None (fetches full range in batches of max 1000 per request). To limit the number of rows, pass an integer.

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_historical_mark_price_klines()
说明：Get historical futures mark price klines from Binance | [源码](同步 binance/client.py:7405-7431, 异步 暂无对应实现) | [官方文档](-)

**核心参数**:
- ☑️ **可选**: end_str (str|int) : optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
- ℹ️ **未标注**: symbol (str) : Name of symbol pair e.g. BNBBTC, interval (str) : Binance Kline interval, start_str (str|int) : Start date string in UTC format or timestamp in milliseconds, limit (int) : Default None (fetches full range in batches of max 1000 per request). To limit the number of rows, pass an integer.

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_historical_klines_generator()
说明：Get historical futures klines generator from Binance | [源码](同步 binance/client.py:7433-7457, 异步 binance/async_client.py:1761-1770) | [官方文档](-)

**核心参数**:
- ☑️ **可选**: end_str (str|int) : optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
- ℹ️ **未标注**: symbol (str) : Name of symbol pair e.g. BNBBTC, interval (str) : Binance Kline interval, start_str (str|int) : Start date string in UTC format or timestamp in milliseconds

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_mark_price(**params)
说明：Get Mark Price and Funding Rate | [源码](同步 binance/client.py:7459-7465, 异步 binance/async_client.py:1772-1773) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Mark-Price)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_funding_rate(**params)
说明：Get funding rate history | [源码](同步 binance/client.py:7467-7473, 异步 binance/async_client.py:1775-1776) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_top_longshort_account_ratio(**params)
说明：Get present long to short ratio for top accounts of a specific symbol. | [源码](同步 binance/client.py:7475-7482, 异步 binance/async_client.py:1778-1781) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Top-Long-Short-Account-Ratio)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_top_longshort_position_ratio(**params)
说明：Get present long to short ratio for top positions of a specific symbol. | [源码](同步 binance/client.py:7484-7491, 异步 binance/async_client.py:1783-1786) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Top-Trader-Long-Short-Ratio)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_global_longshort_ratio(**params)
说明：Get present global long to short ratio of a specific symbol. | [源码](同步 binance/client.py:7493-7500, 异步 binance/async_client.py:1788-1791) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Long-Short-Ratio)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_taker_longshort_ratio(**params)
说明：Get taker buy to sell volume ratio of a specific symbol | [源码](同步 binance/client.py:7502-7509, 异步 binance/async_client.py:1793-1796) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Taker-BuySell-Volume)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_basis(**params)
说明：Get future basis of a specific symbol | [源码](同步 binance/client.py:7511-7518, 异步 暂无对应实现) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Basis)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_ticker(**params)
说明：24 hour rolling window price change statistics. | [源码](同步 binance/client.py:7520-7526, 异步 binance/async_client.py:1798-1799) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/24hr-Ticker-Price-Change-Statistics)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_symbol_ticker(**params)
说明：Latest price for a symbol or symbols. | [源码](同步 binance/client.py:7528-7534, 异步 binance/async_client.py:1801-1802) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Symbol-Price-Ticker)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_orderbook_ticker(**params)
说明：Best price/qty on the order book for a symbol or symbols. | [源码](同步 binance/client.py:7536-7542, 异步 binance/async_client.py:1804-1805) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Symbol-Order-Book-Ticker)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_delivery_price(**params)
说明：Get latest price for a symbol or symbols | [源码](同步 binance/client.py:7544-7550, 异步 暂无对应实现) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Delivery-Price)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_index_price_constituents(**params)
说明：Get index price constituents | [源码](同步 binance/client.py:7552-7558, 异步 binance/async_client.py:1807-1808) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Index-Constituents)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_insurance_fund_balance_snapshot(**params)
说明：Get Insurance Fund Balance Snapshot | [源码](同步 binance/client.py:7560-7566, 异步 暂无对应实现) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Insurance-Fund-Balance)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_liquidation_orders(**params)
说明：Get all liquidation orders | [源码](同步 binance/client.py:7568-7574, 异步 binance/async_client.py:1814-1817) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Users-Force-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_api_trading_status(**params)
说明：Get quantitative trading rules for order placement, such as Unfilled Ratio (UFR), Good-Til-Canceled Ratio (GCR), | [源码](同步 binance/client.py:7576-7661, 异步 binance/async_client.py:1819-1822) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Futures-Trading-Quantitative-Rules-Indicators)

**核心参数**:
- ☑️ **可选**: symbol (str) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "indicators": { // indicator: quantitative rules indicators, value: user's indicators value, triggerValue: trigger indicator value threshold of quantitative rules. "BTCUSDT": [ { "isLocked": true, "plannedRecoverTime": 1545741270000, "indicator": "UFR",  // Unfilled Ratio (UFR) "value": 0.05,  // Current value "triggerValue": 0.995  // Trigger value }, { "isLocked": true, "plannedRecoverTime": 1545741270000, "indicator": "IFER",  // IOC/FOK Expiration Ratio (IFER) "value": 0.99,  // Current value "triggerValue": 0.99  // Trigger value }, { "isLocked": true, "plannedRecoverTime": 1545741270000, "indicator": "GCR",  // GTC Cancellation Ratio (GCR) "value": 0.99,  // Current value "triggerValue": 0.99  // Trigger value }, { "isLocked": true, "plannedRecoverTime": 1545741270000, "indicator": "DR",  // Dust Ratio (DR) "value": 0.99,  // Current value "triggerValue": 0.99  // Trigger value } ], "ETHUSDT": [ { "isLocked": true, "plannedRecoverTime": 1545741270000, "indicator": "UFR", "value": 0.05, "triggerValue": 0.995 }, { "isLocked": true, "plannedRecoverTime": 1545741270000, "indicator": "IFER", "value": 0.99, "triggerValue": 0.99 }, { "isLocked": true, "plannedRecoverTime": 1545741270000, "indicator": "GCR", "value": 0.99, "triggerValue": 0.99 } { "isLocked": true, "plannedRecoverTime": 1545741270000, "indicator": "DR", "value": 0.99, "triggerValue": 0.99 } ] }, "updateTime": 1545741270000 }；详见官方文档

### futures_commission_rate(**params)
说明：Get Futures commission rate | [源码](同步 binance/client.py:7663-7686, 异步 binance/async_client.py:1824-1827) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/User-Commission-Rate)

**核心参数**:
- ✅ **必需**: symbol (str) : required

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "symbol": "BTCUSDT", "makerCommissionRate": "0.0002",  // 0.02% "takerCommissionRate": "0.0004"   // 0.04% }；详见官方文档

### futures_adl_quantile_estimate(**params)
说明：Get Position ADL Quantile Estimate | [源码](同步 binance/client.py:7688-7694, 异步 binance/async_client.py:1829-1832) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Position-ADL-Quantile-Estimation)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_open_interest(**params)
说明：Get present open interest of a specific symbol. | [源码](同步 binance/client.py:7696-7702, 异步 binance/async_client.py:1834-1835) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Open-Interest)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_index_info(**params)
说明：Get index_info | [源码](同步 binance/client.py:7704-7710, 异步 binance/async_client.py:1837-1838) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Composite-Index-Symbol-Information)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_open_interest_hist(**params)
说明：Get open interest statistics of a specific symbol. | [源码](同步 binance/client.py:7712-7718, 异步 binance/async_client.py:1840-1843) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Open-Interest-Statistics)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_leverage_bracket(**params)
说明：Notional and Leverage Brackets | [源码](同步 binance/client.py:7720-7726, 异步 binance/async_client.py:1845-1848) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Notional-and-Leverage-Brackets)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_account_transfer(**params)
说明：Execute transfer between spot account and futures account. | [源码](同步 binance/client.py:7728-7734, 异步 binance/async_client.py:1850-1853) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_loan_borrow_history(**params)
说明：参考源码注释 | [源码](同步 binance/client.py:7744-7747, 异步 binance/async_client.py:1860-1863) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_loan_repay_history(**params)
说明：参考源码注释 | [源码](同步 binance/client.py:7749-7752, 异步 binance/async_client.py:1865-1868) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_loan_wallet(**params)
说明：参考源码注释 | [源码](同步 binance/client.py:7754-7757, 异步 binance/async_client.py:1870-1873) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_cross_collateral_adjust_history(**params)
说明：参考源码注释 | [源码](同步 binance/client.py:7759-7762, 异步 binance/async_client.py:1875-1878) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_cross_collateral_liquidation_history(**params)
说明：参考源码注释 | [源码](同步 binance/client.py:7764-7767, 异步 binance/async_client.py:1880-1883) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_loan_interest_history(**params)
说明：参考源码注释 | [源码](同步 binance/client.py:7769-7772, 异步 binance/async_client.py:1885-1888) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_create_order(**params)
说明：Send in a new order. | [源码](同步 binance/client.py:7774-7782, 异步 binance/async_client.py:1890-1893) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_limit_order(**params)
说明：Send in a new futures limit order. | [源码](同步 binance/client.py:7784-7793, 异步 binance/async_client.py:1895-1904) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_market_order(**params)
说明：Send in a new futures market order. | [源码](同步 binance/client.py:7795-7804, 异步 binance/async_client.py:1906-1915) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_limit_buy_order(**params)
说明：Send in a new futures limit buy order. | [源码](同步 binance/client.py:7807-7817, 异步 binance/async_client.py:1918-1928) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_limit_sell_order(**params)
说明：Send in a new futures limit sell order. | [源码](同步 binance/client.py:7819-7829, 异步 binance/async_client.py:1930-1940) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_market_buy_order(**params)
说明：Send in a new futures market buy order. | [源码](同步 binance/client.py:7831-7841, 异步 binance/async_client.py:1942-1952) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_market_sell_order(**params)
说明：Send in a new futures market sell order. | [源码](同步 binance/client.py:7843-7853, 异步 binance/async_client.py:1954-1964) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_modify_order(**params)
说明：Modify an existing order. Currently only LIMIT order modification is supported. | [源码](同步 binance/client.py:7855-7861, 异步 binance/async_client.py:1966-1972) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Modify-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_create_test_order(**params)
说明：Testing order request, this order will not be submitted to matching engine | [源码](同步 binance/client.py:7863-7869, 异步 binance/async_client.py:1974-1975) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/New-Order-Test)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_place_batch_order(**params)
说明：Send in new orders. | [源码](同步 binance/client.py:7871-7888, 异步 binance/async_client.py:1977-1987) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Place-Multiple-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_get_order(**params)
说明：Check an order's status. | [源码](同步 binance/client.py:7890-7896, 异步 binance/async_client.py:1989-1990) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Query-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_get_open_orders(**params)
说明：Get all open orders on a symbol. | [源码](同步 binance/client.py:7898-7904, 异步 binance/async_client.py:1992-1993) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Current-All-Open-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_get_all_orders(**params)
说明：Get all futures account orders; active, canceled, or filled. | [源码](同步 binance/client.py:7906-7912, 异步 binance/async_client.py:1995-1996) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/All-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_cancel_order(**params)
说明：Cancel an active futures order. | [源码](同步 binance/client.py:7914-7920, 异步 binance/async_client.py:1998-1999) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Cancel-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_cancel_all_open_orders(**params)
说明：Cancel all open futures orders | [源码](同步 binance/client.py:7922-7928, 异步 binance/async_client.py:2001-2004) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Cancel-All-Open-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_cancel_orders(**params)
说明：Cancel multiple futures orders | [源码](同步 binance/client.py:7930-7946, 异步 binance/async_client.py:2006-2017) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Cancel-Multiple-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_countdown_cancel_all(**params)
说明：Cancel all open orders of the specified symbol at the end of the specified countdown. | [源码](同步 binance/client.py:7948-7971, 异步 binance/async_client.py:2019-2022) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Auto-Cancel-All-Open-Orders)

**核心参数**:
- ✅ **必需**: symbol (str) : required, countdownTime (int) : required
- ☑️ **可选**: recvWindow (int) : optional - the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "symbol": "BTCUSDT", "countdownTime": "100000" }；详见官方文档

### futures_account_balance(**params)
说明：Get futures account balance | [源码](同步 binance/client.py:7973-7979, 异步 binance/async_client.py:2024-2027) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Futures-Account-Balance-V3)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_account(**params)
说明：Get current account information. | [源码](同步 binance/client.py:7981-7987, 异步 binance/async_client.py:2029-2032) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Account-Information-V2)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_change_leverage(**params)
说明：Change user's initial leverage of specific symbol market | [源码](同步 binance/client.py:7989-7995, 异步 binance/async_client.py:2034-2035) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Change-Initial-Leverage)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_change_margin_type(**params)
说明：Change the margin type for a symbol | [源码](同步 binance/client.py:7997-8003, 异步 binance/async_client.py:2037-2038) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Change-Margin-Type)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_change_position_margin(**params)
说明：Change the position margin for a symbol | [源码](同步 binance/client.py:8005-8011, 异步 binance/async_client.py:2040-2043) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Modify-Isolated-Position-Margin)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_position_margin_history(**params)
说明：Get position margin change history | [源码](同步 binance/client.py:8013-8021, 异步 binance/async_client.py:2045-2048) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Get-Position-Margin-Change-History)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_position_information(**params)
说明：Get position information | [源码](同步 binance/client.py:8023-8029, 异步 binance/async_client.py:2050-2053) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Position-Information-V3)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_account_trades(**params)
说明：Get trades for the authenticated account and symbol. | [源码](同步 binance/client.py:8031-8037, 异步 binance/async_client.py:2055-2056) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Account-Trade-List)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_income_history(**params)
说明：Get income history for authenticated account | [源码](同步 binance/client.py:8039-8045, 异步 binance/async_client.py:2058-2059) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Get-Income-History)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_change_position_mode(**params)
说明：Change position mode for authenticated account | [源码](同步 binance/client.py:8047-8053, 异步 binance/async_client.py:2061-2064) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Change-Position-Mode)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_get_position_mode(**params)
说明：Get position mode for authenticated account | [源码](同步 binance/client.py:8055-8061, 异步 binance/async_client.py:2066-2069) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_change_multi_assets_mode(multiAssetsMargin: bool)
说明：Change user's Multi-Assets mode (Multi-Assets Mode or Single-Asset Mode) on Every symbol | [源码](同步 binance/client.py:8063-8070, 异步 binance/async_client.py:2071-2075) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Change-Multi-Assets-Mode)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_get_multi_assets_mode()
说明：Get user's Multi-Assets mode (Multi-Assets Mode or Single-Asset Mode) on Every symbol | [源码](同步 binance/client.py:8072-8078, 异步 binance/async_client.py:2077-2080) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_stream_get_listen_key()
说明：参考源码注释 | [源码](同步 binance/client.py:8080-8082, 异步 binance/async_client.py:2082-2086) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_stream_keepalive(listenKey)
说明：参考源码注释 | [源码](同步 binance/client.py:8084-8086, 异步 binance/async_client.py:2088-2092) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_stream_close(listenKey)
说明：参考源码注释 | [源码](同步 binance/client.py:8088-8092, 异步 binance/async_client.py:2094-2098) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_account_config(**params)
说明：Get futures account configuration | [源码](同步 binance/client.py:8095-8101, 异步 binance/async_client.py:2101-2104) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Account-Config)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_symbol_config(**params)
说明：Get current account symbol configuration | [源码](同步 binance/client.py:8103-8109, 异步 binance/async_client.py:2106-2109) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Symbol-Config)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_historical_data_link(**params)
说明：Get Future TickLevel Orderbook Historical Data Download Link. | [源码](同步 binance/client.py:14047-14088, 异步 binance/async_client.py:4139-4140) | [官方文档](https://developers.binance.com/docs/derivatives/futures-data/market-data)

**核心参数**:
- ✅ **必需**: symbol (str) : STRING - Required - Symbol name, e.g. BTCUSDT or BTCUSD_PERP, dataType (str) : ENUM - Required - Data type:, startTime (int) : LONG - Required - Start time in milliseconds, endTime (int) : LONG - Required - End time in milliseconds, timestamp (int) : LONG - Required - Current timestamp in milliseconds
- ☑️ **可选**: recvWindow (int) : LONG - Optional - Number of milliseconds after timestamp the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "data": [ { "day": "2023-06-30", "url": "" } ] }；详见官方文档

### futures_v1_get_order_asyn(**params)
说明：Placeholder function for GET /fapi/v1/order/asyn. | [源码](同步 binance/client.py:14184-14196, 异步 binance/async_client.py:4179-4180) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Get-Download-Id-For-Futures-Order-History)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_v1_get_trade_asyn(**params)
说明：Placeholder function for GET /fapi/v1/trade/asyn. | [源码](同步 binance/client.py:14376-14388, 异步 binance/async_client.py:4249-4250) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Get-Download-Id-For-Futures-Trade-History)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_v1_get_funding_info(**params)
说明：Placeholder function for GET /fapi/v1/fundingInfo. | [源码](同步 binance/client.py:14404-14416, 异步 binance/async_client.py:4259-4260) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-Info)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_v1_get_income_asyn_id(**params)
说明：Placeholder function for GET /fapi/v1/income/asyn/id. | [源码](同步 binance/client.py:14918-14930, 异步 binance/async_client.py:4458-4459) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Get-Futures-Transaction-History-Download-Link-by-Id)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_v1_get_pm_account_info(**params)
说明：Placeholder function for GET /fapi/v1/pmAccountInfo. | [源码](同步 binance/client.py:14988-15000, 异步 binance/async_client.py:4483-4484) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/portfolio-margin-endpoints)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_v1_put_batch_order(**params)
说明：Placeholder function for PUT /fapi/v1/batchOrder. | [源码](同步 binance/client.py:15256-15266, 异步 binance/async_client.py:4592-4593) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_v1_post_batch_order(**params)
说明：Placeholder function for POST /fapi/v1/batchOrder. | [源码](同步 binance/client.py:15282-15292, 异步 binance/async_client.py:4605-4606) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_v1_get_trade_asyn_id(**params)
说明：Placeholder function for GET /fapi/v1/trade/asyn/id. | [源码](同步 binance/client.py:15616-15628, 异步 binance/async_client.py:4736-4737) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Get-Futures-Trade-Download-Link-by-Id)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_v1_put_batch_orders(**params)
说明：Placeholder function for PUT /fapi/v1/batchOrders. | [源码](同步 binance/client.py:15893-15905, 异步 binance/async_client.py:4830-4831) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Modify-Multiple-Orders)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_v1_get_convert_exchange_info(**params)
说明：Placeholder function for GET /fapi/v1/convert/exchangeInfo. | [源码](同步 binance/client.py:15961-15973, 异步 binance/async_client.py:4855-4856) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/convert)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_v1_get_order_amendment(**params)
说明：Placeholder function for GET /fapi/v1/orderAmendment. | [源码](同步 binance/client.py:16043-16055, 异步 binance/async_client.py:4885-4886) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Get-Order-Modify-History)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_v1_get_income_asyn(**params)
说明：Placeholder function for GET /fapi/v1/income/asyn. | [源码](同步 binance/client.py:16121-16133, 异步 binance/async_client.py:4915-4916) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Get-Download-Id-For-Futures-Transaction-History)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_v1_get_fee_burn(**params)
说明：Placeholder function for GET /fapi/v1/feeBurn. | [源码](同步 binance/client.py:16229-16241, 异步 binance/async_client.py:4958-4959) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Get-BNB-Burn-Status)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_v1_get_asset_index(**params)
说明：Placeholder function for GET /fapi/v1/assetIndex. | [源码](同步 binance/client.py:16351-16363, 异步 binance/async_client.py:5003-5004) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Multi-Assets-Mode-Asset-Index)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_v1_get_rate_limit_order(**params)
说明：Placeholder function for GET /fapi/v1/rateLimit/order. | [源码](同步 binance/client.py:16485-16497, 异步 binance/async_client.py:5052-5053) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Query-Rate-Limit)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_v1_get_open_order(**params)
说明：Placeholder function for GET /fapi/v1/openOrder. | [源码](同步 binance/client.py:16527-16539, 异步 binance/async_client.py:5067-5068) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Query-Current-Open-Order)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_v1_post_fee_burn(**params)
说明：Placeholder function for POST /fapi/v1/feeBurn. | [源码](同步 binance/client.py:16631-16643, 异步 binance/async_client.py:5110-5111) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Toggle-BNB-Burn-On-Futures-Trade)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_v1_post_convert_accept_quote(**params)
说明：Placeholder function for POST /fapi/v1/convert/acceptQuote. | [源码](同步 binance/client.py:16793-16805, 异步 binance/async_client.py:5173-5174) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/convert/Accept-Quote)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_v1_get_order_asyn_id(**params)
说明：Placeholder function for GET /fapi/v1/order/asyn/id. | [源码](同步 binance/client.py:16917-16929, 异步 binance/async_client.py:5218-5219) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Get-Futures-Order-History-Download-Link-by-Id)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_v1_post_convert_get_quote(**params)
说明：Placeholder function for POST /fapi/v1/convert/getQuote. | [源码](同步 binance/client.py:17157-17169, 异步 binance/async_client.py:5311-5312) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/convert/Send-quote-request)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_v1_delete_batch_order(**params)
说明：Placeholder function for DELETE /fapi/v1/batchOrder. | [源码](同步 binance/client.py:17426-17436, 异步 binance/async_client.py:5414-5415) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### futures_v1_get_convert_order_status(**params)
说明：Placeholder function for GET /fapi/v1/convert/orderStatus. | [源码](同步 binance/client.py:17522-17534, 异步 binance/async_client.py:5449-5450) | [官方文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/convert/Order-Status)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档
