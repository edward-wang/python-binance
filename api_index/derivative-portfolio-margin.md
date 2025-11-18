# Derivative Portfolio Margin

币安组合保证金接口，支持跨资产和跨合约的统一保证金管理 (/papi)。

### papi_get_balance(**params)
说明：Query account balance. | [源码](同步 binance/client.py:9882-9896, 异步 binance/async_client.py:2595-2596) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account)

**核心参数**:
- ✅ **必需**: asset (str) : required
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_rate_limit(**params)
说明：Query User Rate Limit | [源码](同步 binance/client.py:9898-9910, 异步 binance/async_client.py:2599-2600) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Query-User-Rate-Limit)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_stream_get_listen_key()
说明：Start a new user data stream for Portfolio Margin account. | [源码](同步 binance/client.py:9912-9930, 异步 binance/async_client.py:2573-2575) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/user-data-streams/Start-User-Data-Stream)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response { "listenKey": "pM_XXXXXXX" } The stream will close after 60 minutes unless a keepalive is sent. If the account has an active listenKey, that listenKey will be returned and its validity will be extended for 60 minutes. Weight: 1；详见官方文档

### papi_stream_keepalive(listenKey)
说明：Keepalive a user data stream to prevent a time out. | [源码](同步 binance/client.py:9932-9947, 异步 binance/async_client.py:2579-2583) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/user-data-streams/Keepalive-User-Data-Stream)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response {} User data streams will close after 60 minutes. It's recommended to send a ping about every 60 minutes. Weight: 1；详见官方文档

### papi_stream_close(listenKey)
说明：Close out a user data stream. | [源码](同步 binance/client.py:9949-9962, 异步 binance/async_client.py:2587-2591) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/user-data-streams/Close-User-Data-Stream)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response {} Weight: 1；详见官方文档

### papi_get_account(**params)
说明：Query account information. | [源码](同步 binance/client.py:9964-9975, 异步 binance/async_client.py:2603-2604) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Account-Information)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_margin_max_borrowable(**params)
说明：Query margin max borrow. | [源码](同步 binance/client.py:9977-9993, 异步 binance/async_client.py:2606-2609) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Margin-Max-Borrow)

**核心参数**:
- ✅ **必需**: asset (str) : required
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_margin_max_withdraw(**params)
说明：Query margin max borrow. | [源码](同步 binance/client.py:9995-10011, 异步 binance/async_client.py:2611-2614) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Query-Margin-Max-Withdraw)

**核心参数**:
- ✅ **必需**: asset (str) : required
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_position_risk(**params)
说明：Query margin max borrow. | [源码](同步 binance/client.py:10013-10029, 异步 binance/async_client.py:2616-2619) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Query-UM-Position-Information)

**核心参数**:
- ✅ **必需**: symbol (str) : required
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_cm_position_risk(**params)
说明：Query margin max borrow. | [源码](同步 binance/client.py:10031-10047, 异步 binance/async_client.py:2621-2624) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Query-CM-Position-Information)

**核心参数**:
- ✅ **必需**: asset (str) : required
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_set_um_leverage(**params)
说明：Query margin max borrow. | [源码](同步 binance/client.py:10049-10066, 异步 binance/async_client.py:2626-2629) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Change-UM-Initial-Leverage)

**核心参数**:
- ✅ **必需**: asset (str) : required, leverage (int) : required
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_set_cm_leverage(**params)
说明：Query margin max borrow. | [源码](同步 binance/client.py:10068-10085, 异步 binance/async_client.py:2631-2634) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Change-CM-Initial-Leverage)

**核心参数**:
- ✅ **必需**: asset (str) : required, leverage (int) : required
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_change_um_position_side_dual(**params)
说明：Change user's position mode (Hedge Mode or One-way Mode ) on EVERY symbol in UM. | [源码](同步 binance/client.py:10087-10103, 异步 binance/async_client.py:2636-2639) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Change-UM-Position-Mode)

**核心参数**:
- ✅ **必需**: dualSidePosition (str) : required
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_change_cm_position_side_dual(**params)
说明：Change user's position mode (Hedge Mode or One-way Mode ) on EVERY symbol in CM. | [源码](同步 binance/client.py:10105-10121, 异步 暂无对应实现) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Change-CM-Position-Mode)

**核心参数**:
- ✅ **必需**: dualSidePosition (str) : required
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_position_side_dual(**params)
说明：Get user's position mode (Hedge Mode or One-way Mode ) on EVERY symbol in UM. | [源码](同步 binance/client.py:10123-10136, 异步 binance/async_client.py:2641-2644) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-UM-Current-Position-Mode)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_cm_position_side_dual(**params)
说明：Get user's position mode (Hedge Mode or One-way Mode ) on EVERY symbol in CM. | [源码](同步 binance/client.py:10138-10151, 异步 binance/async_client.py:2646-2649) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-CM-Current-Position-Mode)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_leverage_bracket(**params)
说明：Query UM notional and leverage brackets. | [源码](同步 binance/client.py:10153-10169, 异步 binance/async_client.py:2651-2654) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/UM-Notional-and-Leverage-Brackets)

**核心参数**:
- ☑️ **可选**: symbol (str) : optional, recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_cm_leverage_bracket(**params)
说明：Query CM notional and leverage brackets. | [源码](同步 binance/client.py:10171-10187, 异步 binance/async_client.py:2656-2659) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/CM-Notional-and-Leverage-Brackets)

**核心参数**:
- ☑️ **可选**: symbol (str) : optional, recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_api_trading_status(**params)
说明：Portfolio Margin UM Trading Quantitative Rules Indicators. | [源码](同步 binance/client.py:10189-10205, 异步 binance/async_client.py:2661-2664) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Portfolio-Margin-UM-Trading-Quantitative-Rules-Indicators)

**核心参数**:
- ☑️ **可选**: symbol (str) : optional, recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_comission_rate(**params)
说明：Get User Commission Rate for UM. | [源码](同步 binance/client.py:10207-10223, 异步 binance/async_client.py:2666-2669) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-User-Commission-Rate-for-UM)

**核心参数**:
- ✅ **必需**: symbol (str) : required
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_cm_comission_rate(**params)
说明：Get User Commission Rate for CM. | [源码](同步 binance/client.py:10225-10241, 异步 binance/async_client.py:2671-2674) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-User-Commission-Rate-for-CM)

**核心参数**:
- ✅ **必需**: symbol (str) : required
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_margin_margin_loan(**params)
说明：Query margin loan record. | [源码](同步 binance/client.py:10243-10259, 异步 binance/async_client.py:2676-2679) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Query-Margin-Loan-Record)

**核心参数**:
- ✅ **必需**: asset (str) : required
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_margin_repay_loan(**params)
说明：Query margin repay record. | [源码](同步 binance/client.py:10261-10277, 异步 binance/async_client.py:2681-2684) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Query-Margin-repay-Record)

**核心参数**:
- ✅ **必需**: asset (str) : required
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_repay_futures_switch(**params)
说明：Query Auto-repay-futures Status. | [源码](同步 binance/client.py:10279-10292, 异步 binance/async_client.py:2686-2689) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-Auto-repay-futures-Status)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_repay_futures_switch(**params)
说明：Change Auto-repay-futures Status. | [源码](同步 binance/client.py:10294-10310, 异步 binance/async_client.py:2691-2694) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Change-Auto-repay-futures-Status)

**核心参数**:
- ✅ **必需**: autoRepay (str) : required
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_margin_interest_history(**params)
说明：Get Margin Borrow/Loan Interest History. | [源码](同步 binance/client.py:10312-10325, 异步 binance/async_client.py:2696-2699) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-Margin-BorrowLoan-Interest-History)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_repay_futures_negative_balance(**params)
说明：Repay futures Negative Balance. | [源码](同步 binance/client.py:10327-10340, 异步 binance/async_client.py:2701-2704) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Repay-futures-Negative-Balance)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_portfolio_interest_history(**params)
说明：Query interest history of negative balance for portfolio margin. | [源码](同步 binance/client.py:10342-10355, 异步 binance/async_client.py:2706-2709) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Query-Portfolio-Margin-Negative-Balance-Interest-History)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_portfolio_negative_balance_exchange_record(**params)
说明：Query user negative balance auto exchange record. | [源码](同步 binance/client.py:10358-10371, 异步 binance/async_client.py:2712-2715) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Query-User-Negative-Balance-Auto-Exchange-Record)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_fund_auto_collection(**params)
说明：Fund collection for Portfolio Margin. | [源码](同步 binance/client.py:10373-10386, 异步 binance/async_client.py:2718-2721) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Fund-Auto-collection)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_fund_asset_collection(**params)
说明：Transfers specific asset from Futures Account to Margin account. | [源码](同步 binance/client.py:10388-10401, 异步 binance/async_client.py:2723-2726) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Fund-Collection-by-Asset)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_bnb_transfer(**params)
说明：Transfer BNB in and out of UM. | [源码](同步 binance/client.py:10403-10414, 异步 binance/async_client.py:2728-2731) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/BNB-transfer)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_income_history(**params)
说明：Get UM Income History. | [源码](同步 binance/client.py:10416-10427, 异步 binance/async_client.py:2733-2736) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-UM-Income-History)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_cm_income_history(**params)
说明：Get CM Income History. | [源码](同步 binance/client.py:10429-10440, 异步 binance/async_client.py:2738-2741) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-CM-Income-History)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_account(**params)
说明：Get current UM account asset and position information. | [源码](同步 binance/client.py:10442-10453, 异步 binance/async_client.py:2743-2746) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-UM-Account-Detail)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_account_v2(**params)
说明：Get current UM account asset and position information. | [源码](同步 binance/client.py:10455-10468, 异步 binance/async_client.py:2748-2751) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-UM-Account-Detail-V2)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_cm_account(**params)
说明：Get current CM account asset and position information. | [源码](同步 binance/client.py:10470-10481, 异步 binance/async_client.py:2753-2756) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-CM-Account-Detail)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_account_config(**params)
说明：Query UM Futures account configuration. | [源码](同步 binance/client.py:10483-10496, 异步 binance/async_client.py:2758-2761) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-UM-Futures-Account-Config)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_symbol_config(**params)
说明：Get current UM account symbol configuration. | [源码](同步 binance/client.py:10498-10511, 异步 binance/async_client.py:2763-2766) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-UM-Futures-Symbol-Config)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_trade_asyn(**params)
说明：Get download id for UM futures trade history. | [源码](同步 binance/client.py:10513-10524, 异步 binance/async_client.py:2768-2771) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-Download-Id-For-UM-Futures-Trade-History)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_trade_asyn_id(**params)
说明：Get UM futures trade download link by Id. | [源码](同步 binance/client.py:10526-10539, 异步 binance/async_client.py:2773-2776) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-UM-Futures-Trade-Download-Link-by-Id)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_order_asyn(**params)
说明：Get download id for UM futures order history. | [源码](同步 binance/client.py:10541-10552, 异步 binance/async_client.py:2778-2781) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-Download-Id-For-UM-Futures-Order-History)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_order_asyn_id(**params)
说明：Get UM futures order download link by Id. | [源码](同步 binance/client.py:10554-10567, 异步 binance/async_client.py:2783-2786) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-UM-Futures-Order-Download-Link-by-Id)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_income_asyn(**params)
说明：Get download id for UM futures transaction history. | [源码](同步 binance/client.py:10569-10580, 异步 binance/async_client.py:2788-2791) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-Download-Id-For-UM-Futures-Transaction-History)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_income_asyn_id(**params)
说明：Get UM futures Transaction download link by Id. | [源码](同步 binance/client.py:10582-10595, 异步 binance/async_client.py:2793-2796) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-UM-Futures-Transaction-Download-Link-by-Id)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_ping(**params)
说明：Test connectivity to the Rest API. | [源码](同步 binance/client.py:10599-10607, 异步 binance/async_client.py:2798-2799) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/market-data)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_create_um_order(**params)
说明：Place new UM order. | [源码](同步 binance/client.py:10611-10621, 异步 binance/async_client.py:2803-2815) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_create_um_conditional_order(**params)
说明：Place new UM Conditional order. | [源码](同步 binance/client.py:10623-10635, 异步 binance/async_client.py:2817-2829) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/New-UM-Conditional-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_create_cm_order(**params)
说明：Place new CM order. | [源码](同步 binance/client.py:10637-10647, 异步 binance/async_client.py:2831-2843) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/New-CM-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_create_cm_conditional_order(**params)
说明：Place new CM Conditional order. | [源码](同步 binance/client.py:10649-10661, 异步 binance/async_client.py:2845-2857) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/New-CM-Conditional-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_create_margin_order(**params)
说明：New Margin Order. | [源码](同步 binance/client.py:10663-10673, 异步 binance/async_client.py:2859-2871) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/New-Margin-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_margin_loan(**params)
说明：Apply for a margin loan. | [源码](同步 binance/client.py:10675-10683, 异步 binance/async_client.py:2873-2883) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Margin-Account-Borrow)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_repay_loan(**params)
说明：Repay for a margin loan. | [源码](同步 binance/client.py:10685-10693, 异步 binance/async_client.py:2885-2895) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Margin-Account-Repay)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_margin_order_oco(**params)
说明：Send in a new OCO for a margin account. | [源码](同步 binance/client.py:10695-10705, 异步 binance/async_client.py:2897-2907) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Margin-Account-New-OCO)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_cancel_um_order(**params)
说明：Cancel an active UM LIMIT order. | [源码](同步 binance/client.py:10707-10715, 异步 binance/async_client.py:2909-2919) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-UM-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_cancel_um_all_open_orders(**params)
说明：Cancel an active UM LIMIT order. | [源码](同步 binance/client.py:10717-10727, 异步 binance/async_client.py:2921-2931) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-All-UM-Open-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_cancel_um_conditional_order(**params)
说明：Cancel UM Conditional Order. | [源码](同步 binance/client.py:10729-10739, 异步 binance/async_client.py:2933-2943) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-UM-Conditional-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_cancel_um_conditional_all_open_orders(**params)
说明：Cancel All UM Open Conditional Orders. | [源码](同步 binance/client.py:10741-10751, 异步 binance/async_client.py:2945-2955) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-All-UM-Open-Conditional-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_cancel_cm_order(**params)
说明：Cancel an active CM LIMIT order. | [源码](同步 binance/client.py:10753-10761, 异步 binance/async_client.py:2957-2967) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-CM-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_cancel_cm_all_open_orders(**params)
说明：Cancel an active CM LIMIT order. | [源码](同步 binance/client.py:10763-10773, 异步 binance/async_client.py:2969-2979) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-All-CM-Open-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_cancel_cm_conditional_order(**params)
说明：Cancel CM Conditional Order. | [源码](同步 binance/client.py:10775-10785, 异步 binance/async_client.py:2981-2991) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-CM-Conditional-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_cancel_cm_conditional_all_open_orders(**params)
说明：Cancel All CM Open Conditional Orders. | [源码](同步 binance/client.py:10787-10797, 异步 binance/async_client.py:2993-3003) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-All-CM-Open-Conditional-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_cancel_margin_order(**params)
说明：Cancel Margin Account Order. | [源码](同步 binance/client.py:10799-10809, 异步 binance/async_client.py:3005-3015) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-Margin-Account-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_cancel_margin_order_list(**params)
说明：Cancel Margin Account OCO Orders. | [源码](同步 binance/client.py:10811-10821, 异步 binance/async_client.py:3017-3027) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-Margin-Account-OCO-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_cancel_margin_all_open_orders(**params)
说明：Cancel Margin Account All Open Orders on a Symbol. | [源码](同步 binance/client.py:10823-10833, 异步 binance/async_client.py:3029-3039) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-Margin-Account-All-Open-Orders-on-a-Symbol)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_modify_um_order(**params)
说明：Order modify function, currently only LIMIT order modification is supported, modified orders will be reordered in the match queue. | [源码](同步 binance/client.py:10835-10843, 异步 binance/async_client.py:3041-3049) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Modify-UM-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_modify_cm_order(**params)
说明：Order modify function, currently only LIMIT order modification is supported, modified orders will be reordered in the match queue. | [源码](同步 binance/client.py:10845-10853, 异步 binance/async_client.py:3051-3059) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Modify-CM-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_order(**params)
说明：Check an UM order's status. | [源码](同步 binance/client.py:10855-10863, 异步 binance/async_client.py:3061-3069) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-UM-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_all_orders(**params)
说明：Get all account UM orders; active, canceled, or filled. | [源码](同步 binance/client.py:10865-10873, 异步 binance/async_client.py:3071-3081) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-UM-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_open_order(**params)
说明：Query current UM open order. | [源码](同步 binance/client.py:10875-10883, 异步 binance/async_client.py:3083-3093) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Current-UM-Open-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_open_orders(**params)
说明：Get all open orders on a symbol. | [源码](同步 binance/client.py:10885-10893, 异步 binance/async_client.py:3095-3105) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-Current-UM-Open-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_conditional_all_orders(**params)
说明：Query All UM Conditional Orders. | [源码](同步 binance/client.py:10895-10905, 异步 binance/async_client.py:3107-3117) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-UM-Conditional-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_conditional_open_orders(**params)
说明：Get all open conditional orders on a symbol. | [源码](同步 binance/client.py:10907-10917, 异步 binance/async_client.py:3119-3129) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-Current-UM-Open-Conditional-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_conditional_open_order(**params)
说明：Query Current UM Open Conditional Order. | [源码](同步 binance/client.py:10919-10929, 异步 binance/async_client.py:3131-3141) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Current-UM-Open-Conditional-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_conditional_order_history(**params)
说明：Get all open conditional orders on a symbol. | [源码](同步 binance/client.py:10931-10941, 异步 binance/async_client.py:3143-3153) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-UM-Conditional-Order-History)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_cm_order(**params)
说明：Check an CM order's status. | [源码](同步 binance/client.py:10943-10951, 异步 binance/async_client.py:3155-3163) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-CM-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_cm_all_orders(**params)
说明：Get all account CM orders; active, canceled, or filled. | [源码](同步 binance/client.py:10953-10961, 异步 binance/async_client.py:3165-3175) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-CM-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_cm_open_order(**params)
说明：Query current CM open order. | [源码](同步 binance/client.py:10963-10971, 异步 binance/async_client.py:3177-3187) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Current-CM-Open-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_cm_open_orders(**params)
说明：Get all open orders on a symbol. | [源码](同步 binance/client.py:10973-10981, 异步 binance/async_client.py:3189-3199) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-Current-CM-Open-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_cm_conditional_all_orders(**params)
说明：Query All CM Conditional Orders. | [源码](同步 binance/client.py:10983-10993, 异步 binance/async_client.py:3201-3211) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-CM-Conditional-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_cm_conditional_open_orders(**params)
说明：Get all open conditional orders on a symbol. | [源码](同步 binance/client.py:10995-11005, 异步 binance/async_client.py:3213-3223) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-Current-CM-Open-Conditional-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_cm_conditional_open_order(**params)
说明：Query Current UM Open Conditional Order. | [源码](同步 binance/client.py:11007-11017, 异步 binance/async_client.py:3225-3235) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Current-CM-Open-Conditional-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_cm_conditional_order_history(**params)
说明：Get all open conditional orders on a symbol. | [源码](同步 binance/client.py:11019-11029, 异步 binance/async_client.py:3237-3247) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-CM-Conditional-Order-History)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_force_orders(**params)
说明：Query User's UM Force Orders. | [源码](同步 binance/client.py:11031-11039, 异步 binance/async_client.py:3249-3259) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Users-UM-Force-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_cm_force_orders(**params)
说明：Query User's CM Force Orders. | [源码](同步 binance/client.py:11041-11049, 异步 binance/async_client.py:3261-3271) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Users-CM-Force-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_order_amendment(**params)
说明：Get order modification history. | [源码](同步 binance/client.py:11051-11061, 异步 binance/async_client.py:3273-3283) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-UM-Modify-Order-History)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_cm_order_amendment(**params)
说明：Get order modification history. | [源码](同步 binance/client.py:11063-11073, 异步 binance/async_client.py:3285-3295) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-CM-Modify-Order-History)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_margin_force_orders(**params)
说明：Query user's margin force orders. | [源码](同步 binance/client.py:11075-11085, 异步 binance/async_client.py:3297-3307) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Users-Margin-Force-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_user_trades(**params)
说明：Get trades for a specific account and UM symbol. | [源码](同步 binance/client.py:11087-11095, 异步 binance/async_client.py:3309-3319) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/UM-Account-Trade-List)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_cm_user_trades(**params)
说明：Get trades for a specific account and CM symbol. | [源码](同步 binance/client.py:11097-11105, 异步 binance/async_client.py:3321-3331) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/CM-Account-Trade-List)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_adl_quantile(**params)
说明：Query UM Position ADL Quantile Estimation. | [源码](同步 binance/client.py:11107-11115, 异步 binance/async_client.py:3333-3343) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/UM-Position-ADL-Quantile-Estimation)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_cm_adl_quantile(**params)
说明：Query CM Position ADL Quantile Estimation. | [源码](同步 binance/client.py:11117-11125, 异步 binance/async_client.py:3345-3355) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/CM-Position-ADL-Quantile-Estimation)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_set_um_fee_burn(**params)
说明：Change user's BNB Fee Discount for UM Futures (Fee Discount On or Fee Discount Off ) on EVERY symbol. | [源码](同步 binance/client.py:11127-11135, 异步 binance/async_client.py:3357-3367) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Toggle-BNB-Burn-On-UM-Futures-Trade)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_um_fee_burn(**params)
说明：Get user's BNB Fee Discount for UM Futures (Fee Discount On or Fee Discount Off). | [源码](同步 binance/client.py:11137-11145, 异步 binance/async_client.py:3369-3379) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Get-UM-Futures-BNB-Burn-Status)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_margin_order(**params)
说明：Query Margin Account Order. | [源码](同步 binance/client.py:11147-11155, 异步 binance/async_client.py:3381-3391) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Margin-Account-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_margin_open_orders(**params)
说明：Query Current Margin Open Order. | [源码](同步 binance/client.py:11157-11167, 异步 binance/async_client.py:3393-3403) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Current-Margin-Open-Order)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_margin_all_orders(**params)
说明：Query All Margin Account Orders. | [源码](同步 binance/client.py:11169-11179, 异步 binance/async_client.py:3405-3415) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-Margin-Account-Orders)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_margin_order_list(**params)
说明：Retrieves a specific OCO based on provided optional parameters. | [源码](同步 binance/client.py:11181-11191, 异步 binance/async_client.py:3417-3427) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Margin-Account-OCO)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_margin_all_order_list(**params)
说明：Query all OCO for a specific margin account based on provided optional parameters. | [源码](同步 binance/client.py:11193-11203, 异步 binance/async_client.py:3429-3439) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Margin-Account-all-OCO)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_margin_open_order_list(**params)
说明：Query Margin Account's Open OCO. | [源码](同步 binance/client.py:11205-11215, 异步 binance/async_client.py:3441-3451) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Margin-Account-Open-OCO)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_margin_my_trades(**params)
说明：Margin Account Trade List. | [源码](同步 binance/client.py:11217-11227, 异步 binance/async_client.py:3453-3463) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Margin-Account-Trade-List)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_get_margin_repay_debt(**params)
说明：Repay debt for a margin loan. | [源码](同步 binance/client.py:11229-11239, 异步 binance/async_client.py:3465-3475) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Margin-Account-Repay-Debt)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### papi_v1_post_ping(**params)
说明：Placeholder function for POST /papi/v1/ping. | [源码](同步 binance/client.py:14704-14714, 异步 binance/async_client.py:4372-4373) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档
