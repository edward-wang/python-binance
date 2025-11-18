# Margin Trading

币安保证金交易相关接口，支持全仓和逐仓保证金账户管理、借贷、交易等功能。

### get_system_status()
说明：Get system status detail. | [源码](同步 binance/client.py:2432-2449, 异步 binance/async_client.py:836-837) | [官方文档](https://developers.binance.com/docs/wallet/others/system-status)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "status": 0,        # 0: normal，1：system maintenance "msg": "normal"     # normal or System maintenance. }；详见官方文档

### get_account_status(version=1, **params)
说明：Get account status detail. | [源码](同步 binance/client.py:2451-2474, 异步 binance/async_client.py:841-844) | [官方文档](https://developers.binance.com/docs/wallet/account/account-status)

**核心参数**:
- ℹ️ **未标注**: version : the api version int, recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "data": "Normal" }；详见官方文档

### get_account_api_trading_status(**params)
说明：Fetch account api trading status detail. | [源码](同步 binance/client.py:2476-2546, 异步 binance/async_client.py:848-851) | [官方文档](https://developers.binance.com/docs/wallet/account/account-api-trading-status)

**核心参数**:
- ℹ️ **未标注**: recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "data": {          // API trading status detail "isLocked": false,   // API trading function is locked or not "plannedRecoverTime": 0,  // If API trading function is locked, this is the planned recover time "triggerCondition": { "GCR": 150,  // Number of GTC orders "IFER": 150, // Number of FOK/IOC orders "UFR": 300   // Number of orders }, "indicators": {  // The indicators updated every 30 seconds "BTCUSDT": [  // The symbol { "i": "UFR",  // Unfilled Ratio (UFR) "c": 20,     // Count of all orders "v": 0.05,   // Current UFR value "t": 0.995   // Trigger UFR value }, { "i": "IFER", // IOC/FOK Expiration Ratio (IFER) "c": 20,     // Count of FOK/IOC orders "v": 0.99,   // Current IFER value "t": 0.99    // Trigger IFER value }, { "i": "GCR",  // GTC Cancellation Ratio (GCR) "c": 20,     // Count of GTC orders "v": 0.99,   // Current GCR value "t": 0.99    // Trigger GCR value } ], "ETHUSDT": [ { "i": "UFR", "c": 20, "v": 0.05, "t": 0.995 }, { "i": "IFER", "c": 20, "v": 0.99, "t": 0.99 }, { "i": "GCR", "c": 20, "v": 0.99, "t": 0.99 } ] }, "updateTime": 1547630471725 } }；详见官方文档

### get_account_api_permissions(**params)
说明：Fetch api key permissions. | [源码](同步 binance/client.py:2548-2577, 异步 binance/async_client.py:857-860) | [官方文档](https://developers.binance.com/docs/wallet/account/api-key-permission)

**核心参数**:
- ℹ️ **未标注**: recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "ipRestrict": false, "createTime": 1623840271000, "enableWithdrawals": false,   // This option allows you to withdraw via API. You must apply the IP Access Restriction filter in order to enable withdrawals "enableInternalTransfer": true,  // This option authorizes this key to transfer funds between your master account and your sub account instantly "permitsUniversalTransfer": true,  // Authorizes this key to be used for a dedicated universal transfer API to transfer multiple supported currencies. Each business's own transfer API rights are not affected by this authorization "enableVanillaOptions": false,  //  Authorizes this key to Vanilla options trading "enableReading": true, "enableFutures": false,  //  API Key created before your futures account opened does not support futures API service "enableMargin": false,   //  This option can be adjusted after the Cross Margin account transfer is completed "enableSpotAndMarginTrading": false, // Spot and margin trading "tradingAuthorityExpirationTime": 1628985600000  // Expiration time for spot and margin trading permission }；详见官方文档

### get_dust_assets(**params)
说明：Get assets that can be converted into BNB | [源码](同步 binance/client.py:2579-2606, 异步 binance/async_client.py:864-867) | [官方文档](https://developers.binance.com/docs/wallet/asset/assets-can-convert-bnb)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "details": [ { "asset": "ADA", "assetFullName": "ADA", "amountFree": "6.21",   //Convertible amount "toBTC": "0.00016848",  //BTC amount "toBNB": "0.01777302",  //BNB amount（Not deducted commission fee） "toBNBOffExchange": "0.01741756", //BNB amount（Deducted commission fee） "exchange": "0.00035546" //Commission fee } ], "totalTransferBtc": "0.00016848", "totalTransferBNB": "0.01777302", "dribbletPercentage": "0.02"     //Commission fee }；详见官方文档

### get_dust_log(**params)
说明：Get log of small amounts exchanged for BNB. | [源码](同步 binance/client.py:2608-2678, 异步 binance/async_client.py:871-874) | [官方文档](https://developers.binance.com/docs/wallet/asset/dust-log)

**核心参数**:
- ☑️ **可选**: startTime (int) : optional, endTime (int) : optional
- ℹ️ **未标注**: recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "total": 8,   //Total counts of exchange "userAssetDribblets": [ { "totalTransferedAmount": "0.00132256",   // Total transfered BNB amount for this exchange. "totalServiceChargeAmount": "0.00002699",    //Total service charge amount for this exchange. "transId": 45178372831, "userAssetDribbletDetails": [           //Details of  this exchange. { "transId": 4359321, "serviceChargeAmount": "0.000009", "amount": "0.0009", "operateTime": 1615985535000, "transferedAmount": "0.000441", "fromAsset": "USDT" }, { "transId": 4359321, "serviceChargeAmount": "0.00001799", "amount": "0.0009", "operateTime": "2018-05-03 17:07:04", "transferedAmount": "0.00088156", "fromAsset": "ETH" } ] }, { "operateTime":1616203180000, "totalTransferedAmount": "0.00058795", "totalServiceChargeAmount": "0.000012", "transId": 4357015, "userAssetDribbletDetails": [ { "transId": 4357015, "serviceChargeAmount": "0.00001" "amount": "0.001", "operateTime": 1616203180000, "transferedAmount": "0.00049", "fromAsset": "USDT" }, { "transId": 4357015, "serviceChargeAmount": "0.000002" "amount": "0.0001", "operateTime": 1616203180000, "transferedAmount": "0.00009795", "fromAsset": "ETH" } ] } ] }；详见官方文档

### transfer_dust(**params)
说明：Convert dust assets to BNB. | [源码](同步 binance/client.py:2680-2716, 异步 binance/async_client.py:878-879) | [官方文档](https://developers.binance.com/docs/wallet/asset/dust-transfer)

**核心参数**:
- ℹ️ **未标注**: asset (str) : The asset being converted. e.g: 'ONE', recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "totalServiceCharge":"0.02102542", "totalTransfered":"1.05127099", "transferResult":[ { "amount":"0.03000000", "fromAsset":"ETH", "operateTime":1563368549307, "serviceChargeAmount":"0.00500000", "tranId":2970932918, "transferedAmount":"0.25000000" } ] }；详见官方文档

### get_asset_dividend_history(**params)
说明：Query asset dividend record. | [源码](同步 binance/client.py:2718-2763, 异步 binance/async_client.py:883-886) | [官方文档](https://developers.binance.com/docs/wallet/asset/assets-divided-record)

**核心参数**:
- ☑️ **可选**: asset (str) : optional, startTime (long) : optional, endTime (long) : optional
- ℹ️ **未标注**: recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "rows":[ { "amount":"10.00000000", "asset":"BHFT", "divTime":1563189166000, "enInfo":"BHFT distribution", "tranId":2968885920 }, { "amount":"10.00000000", "asset":"BHFT", "divTime":1563189165000, "enInfo":"BHFT distribution", "tranId":2968885920 } ], "total":2 }；详见官方文档

### make_universal_transfer(**params)
说明：User Universal Transfer | [源码](同步 binance/client.py:2765-2797, 异步 binance/async_client.py:890-893) | [官方文档](https://developers.binance.com/docs/wallet/asset/user-universal-transfer)

**核心参数**:
- ✅ **必需**: type (str (ENUM)) : required, asset (str) : required, amount (str) : required
- ℹ️ **未标注**: recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "tranId":13526853623 }；详见官方文档

### query_universal_transfer_history(**params)
说明：Query User Universal Transfer History | [源码](同步 binance/client.py:2799-2853, 异步 binance/async_client.py:897-900) | [官方文档](https://developers.binance.com/docs/wallet/asset/query-user-universal-transfer)

**核心参数**:
- ✅ **必需**: type (str (ENUM)) : required, size (int) : required - Default 10, Max 100
- ☑️ **可选**: startTime (int) : optional, endTime (int) : optional, current (int) : optional - Default 1
- ℹ️ **未标注**: recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "total":2, "rows":[ { "asset":"USDT", "amount":"1", "type":"MAIN_UMFUTURE" "status": "CONFIRMED", "tranId": 11415955596, "timestamp":1544433328000 }, { "asset":"USDT", "amount":"2", "type":"MAIN_UMFUTURE", "status": "CONFIRMED", "tranId": 11366865406, "timestamp":1544433328000 } ] }；详见官方文档

### get_trade_fee(**params)
说明：Get trade fee. | [源码](同步 binance/client.py:2855-2888, 异步 binance/async_client.py:906-911) | [官方文档](https://developers.binance.com/docs/wallet/asset/trade-fee)

**核心参数**:
- ☑️ **可选**: symbol (str) : optional
- ℹ️ **未标注**: recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python [ { "symbol": "ADABNB", "makerCommission": "0.001", "takerCommission": "0.001" }, { "symbol": "BNBBTC", "makerCommission": "0.001", "takerCommission": "0.001" } ]；详见官方文档

### get_asset_details(**params)
说明：Fetch details on assets. | [源码](同步 binance/client.py:2890-2921, 异步 binance/async_client.py:915-918) | [官方文档](https://developers.binance.com/docs/wallet/asset)

**核心参数**:
- ☑️ **可选**: asset (str) : optional
- ℹ️ **未标注**: recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "CTR": { "minWithdrawAmount": "70.00000000", //min withdraw amount "depositStatus": false,//deposit status (false if ALL of networks' are false) "withdrawFee": 35, // withdraw fee "withdrawStatus": true, //withdraw status (false if ALL of networks' are false) "depositTip": "Delisted, Deposit Suspended" //reason }, "SKY": { "minWithdrawAmount": "0.02000000", "depositStatus": true, "withdrawFee": 0.01, "withdrawStatus": true } }；详见官方文档

### get_spot_delist_schedule(**params)
说明：Get symbols delist schedule for spot | [源码](同步 binance/client.py:2923-2952, 异步 binance/async_client.py:922-925) | [官方文档](https://developers.binance.com/docs/wallet/others/delist-schedule)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional - the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python [ { "delistTime": 1686161202000, "symbols": [ "ADAUSDT", "BNBUSDT" ] }, { "delistTime": 1686222232000, "symbols": [ "ETHUSDT" ] } ]；详见官方文档

### withdraw(**params)
说明：Submit a withdraw request. | [源码](同步 binance/client.py:2956-2997, 异步 binance/async_client.py:929-935) | [官方文档](https://developers.binance.com/docs/wallet/capital/withdraw)

**核心参数**:
- ✅ **必需**: coin (str) : required, amount (decimal) : required, transactionFeeFlag (bool) : required - When making internal transfer, true for returning the fee to the destination account; false for returning the fee back to the departure account. Default false.
- ☑️ **可选**: withdrawOrderId (str) : optional - client id for withdraw, network (str) : optional, address (str) : optional, name (str) : optional - Description of the address, default asset value passed will be used
- ℹ️ **未标注**: addressTag (optional - Secondary address identifier for coins like XRP,XMR etc.), recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "id":"7213fea8e94b4a5593d507237e5a555b" }；详见官方文档

### get_deposit_history(**params)
说明：Fetch deposit history. | [源码](同步 binance/client.py:2999-3055, 异步 binance/async_client.py:939-942) | [官方文档](https://developers.binance.com/docs/wallet/capital/deposite-history)

**核心参数**:
- ☑️ **可选**: coin (str) : optional, startTime (long) : optional, endTime (long) : optional, offset (long) : optional - default:0, limit (long) : optional
- ℹ️ **未标注**: status (int), recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python [ { "amount":"0.00999800", "coin":"PAXG", "network":"ETH", "status":1, "address":"0x788cabe9236ce061e5a892e1a59395a81fc8d62c", "addressTag":"", "txId":"0xaad4654a3234aa6118af9b4b335f5ae81c360b2394721c019b5d1e75328b09f3", "insertTime":1599621997000, "transferType":0, "confirmTimes":"12/12" }, { "amount":"0.50000000", "coin":"IOTA", "network":"IOTA", "status":1, "address":"SIZ9VLMHWATXKV99LH99CIGFJFUMLEHGWVZVNNZXRJJVWBPHYWPPBOSDORZ9EQSHCZAMPVAPGFYQAUUV9DROOXJLNW", "addressTag":"", "txId":"ESBFVQUTPIWQNJSPXFNHNYHSQNTGKRVKPRABQWTAXCDWOAKDKYWPTVG9BGXNVNKTLEJGESAVXIKIZ9999", "insertTime":1599620082000, "transferType":0, "confirmTimes":"1/1" } ]；详见官方文档

### get_withdraw_history(**params)
说明：Fetch withdraw history. | [源码](同步 binance/client.py:3057-3111, 异步 binance/async_client.py:946-949) | [官方文档](https://developers.binance.com/docs/wallet/capital/withdraw-history)

**核心参数**:
- ☑️ **可选**: coin (str) : optional, offset (int) : optional - default:0, limit (int) : optional, startTime (int) : optional - Default: 90 days from current timestamp, endTime (int) : optional - Default: present timestamp
- ℹ️ **未标注**: status (int), recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python [ { "address": "0x94df8b352de7f46f64b01d3666bf6e936e44ce60", "amount": "8.91000000", "applyTime": "2019-10-12 11:12:02", "coin": "USDT", "id": "b6ae22b3aa844210a7041aee7589627c", "withdrawOrderId": "WITHDRAWtest123", // will not be returned if there's no withdrawOrderId for this withdraw. "network": "ETH", "transferType": 0,   // 1 for internal transfer, 0 for external transfer "status": 6, "txId": "0xb5ef8c13b968a406cc62a93a8bd80f9e9a906ef1b3fcf20a2e48573c17659268" }, { "address": "1FZdVHtiBqMrWdjPyRPULCUceZPJ2WLCsB", "amount": "0.00150000", "applyTime": "2019-09-24 12:43:45", "coin": "BTC", "id": "156ec387f49b41df8724fa744fa82719", "network": "BTC", "status": 6, "txId": "60fd9007ebfddc753455f95fafa808c4302c836e4d1eebc5a132c36c1d8ac354" } ]；详见官方文档

### get_deposit_address(coin: str, network: Optional[str] = None, **params)
说明：Fetch a deposit address for a symbol | [源码](同步 binance/client.py:3158-3189, 异步 binance/async_client.py:964-972) | [官方文档](https://developers.binance.com/docs/wallet/capital/deposite-address)

**核心参数**:
- ✅ **必需**: coin (str) : required
- ☑️ **可选**: network (str) : optional
- ℹ️ **未标注**: recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "address": "1HPn8Rx2y6nNSfagQBKy27GB99Vbzg89wv", "coin": "BTC", "tag": "", "url": "https://btc.com/1HPn8Rx2y6nNSfagQBKy27GB99Vbzg89wv" }；详见官方文档

### get_margin_account(**params)
说明：Query cross-margin account details | [源码](同步 binance/client.py:3264-3320, 异步 binance/async_client.py:997-1000) | [官方文档](https://developers.binance.com/docs/margin_trading/account/Query-Cross-Margin-Account-Details)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "borrowEnabled": true, "marginLevel": "11.64405625", "totalAssetOfBtc": "6.82728457", "totalLiabilityOfBtc": "0.58633215", "totalNetAssetOfBtc": "6.24095242", "tradeEnabled": true, "transferEnabled": true, "userAssets": [ { "asset": "BTC", "borrowed": "0.00000000", "free": "0.00499500", "interest": "0.00000000", "locked": "0.00000000", "netAsset": "0.00499500" }, { "asset": "BNB", "borrowed": "201.66666672", "free": "2346.50000000", "interest": "0.00000000", "locked": "0.00000000", "netAsset": "2144.83333328" }, { "asset": "ETH", "borrowed": "0.00000000", "free": "0.00000000", "interest": "0.00000000", "locked": "0.00000000", "netAsset": "0.00000000" }, { "asset": "USDT", "borrowed": "0.00000000", "free": "0.00000000", "interest": "0.00000000", "locked": "0.00000000", "netAsset": "0.00000000" } ] }；详见官方文档

### get_isolated_margin_account(**params)
说明：Query isolated margin account details | [源码](同步 binance/client.py:3322-3433, 异步 binance/async_client.py:1004-1007) | [官方文档](https://developers.binance.com/docs/margin_trading/account/Query-Isolated-Margin-Account-Info)

**核心参数**:
- ☑️ **可选**: symbols : optional up to 5 margin pairs as a comma separated string
- ℹ️ **未标注**: asset (str)

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python If "symbols" is not sent: { "assets":[ { "baseAsset": { "asset": "BTC", "borrowEnabled": true, "borrowed": "0.00000000", "free": "0.00000000", "interest": "0.00000000", "locked": "0.00000000", "netAsset": "0.00000000", "netAssetOfBtc": "0.00000000", "repayEnabled": true, "totalAsset": "0.00000000" }, "quoteAsset": { "asset": "USDT", "borrowEnabled": true, "borrowed": "0.00000000", "free": "0.00000000", "interest": "0.00000000", "locked": "0.00000000", "netAsset": "0.00000000", "netAssetOfBtc": "0.00000000", "repayEnabled": true, "totalAsset": "0.00000000" }, "symbol": "BTCUSDT" "isolatedCreated": true, "marginLevel": "0.00000000", "marginLevelStatus": "EXCESSIVE", // "EXCESSIVE", "NORMAL", "MARGIN_CALL", "PRE_LIQUIDATION", "FORCE_LIQUIDATION" "marginRatio": "0.00000000", "indexPrice": "10000.00000000" "liquidatePrice": "1000.00000000", "liquidateRate": "1.00000000" "tradeEnabled": true } ], "totalAssetOfBtc": "0.00000000", "totalLiabilityOfBtc": "0.00000000", "totalNetAssetOfBtc": "0.00000000" } If "symbols" is sent: { "assets":[ { "baseAsset": { "asset": "BTC", "borrowEnabled": true, "borrowed": "0.00000000", "free": "0.00000000", "interest": "0.00000000", "locked": "0.00000000", "netAsset": "0.00000000", "netAssetOfBtc": "0.00000000", "repayEnabled": true, "totalAsset": "0.00000000" }, "quoteAsset": { "asset": "USDT", "borrowEnabled": true, "borrowed": "0.00000000", "free": "0.00000000", "interest": "0.00000000", "locked": "0.00000000", "netAsset": "0.00000000", "netAssetOfBtc": "0.00000000", "repayEnabled": true, "totalAsset": "0.00000000" }, "symbol": "BTCUSDT" "isolatedCreated": true, "marginLevel": "0.00000000", "marginLevelStatus": "EXCESSIVE", // "EXCESSIVE", "NORMAL", "MARGIN_CALL", "PRE_LIQUIDATION", "FORCE_LIQUIDATION" "marginRatio": "0.00000000", "indexPrice": "10000.00000000" "liquidatePrice": "1000.00000000", "liquidateRate": "1.00000000" "tradeEnabled": true } ] }；详见官方文档

### enable_isolated_margin_account(**params)
说明：Enable isolated margin account for a specific symbol. | [源码](同步 binance/client.py:3435-3456, 异步 binance/async_client.py:1011-1014) | [官方文档](https://developers.binance.com/docs/margin_trading/account/Enable-Isolated-Margin-Account)

**核心参数**:
- ℹ️ **未标注**: symbol, asset (str)

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "success": true, "symbol": "BTCUSDT" }；详见官方文档

### disable_isolated_margin_account(**params)
说明：Disable isolated margin account for a specific symbol. Each trading pair can only | [源码](同步 binance/client.py:3458-3479, 异步 binance/async_client.py:1020-1023) | [官方文档](https://developers.binance.com/docs/margin_trading/account/Disable-Isolated-Margin-Account)

**核心参数**:
- ℹ️ **未标注**: symbol, asset (str)

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "success": true, "symbol": "BTCUSDT" }；详见官方文档

### get_enabled_isolated_margin_account_limit(**params)
说明：Query enabled isolated margin account limit. | [源码](同步 binance/client.py:3481-3497, 异步 binance/async_client.py:1029-1032) | [官方文档](https://developers.binance.com/docs/margin_trading/account/Query-Enabled-Isolated-Margin-Account-Limit)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "enabledAccount": 5, "maxAccount": 20 }；详见官方文档

### get_margin_dustlog(**params)
说明：Query the historical information of user's margin account small-value asset conversion BNB. | [源码](同步 binance/client.py:3499-3568, 异步 binance/async_client.py:1038-1041) | [官方文档](-)

**核心参数**:
- ☑️ **可选**: startTime (long) : optional, endTime (long) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "total": 8, //Total counts of exchange "userAssetDribblets": [ { "operateTime": 1615985535000, "totalTransferedAmount": "0.00132256", // Total transfered BNB amount for this exchange. "totalServiceChargeAmount": "0.00002699", //Total service charge amount for this exchange. "transId": 45178372831, "userAssetDribbletDetails": [ //Details of  this exchange. { "transId": 4359321, "serviceChargeAmount": "0.000009", "amount": "0.0009", "operateTime": 1615985535000, "transferedAmount": "0.000441", "fromAsset": "USDT" }, { "transId": 4359321, "serviceChargeAmount": "0.00001799", "amount": "0.0009", "operateTime": 1615985535000, "transferedAmount": "0.00088156", "fromAsset": "ETH" } ] }, { "operateTime":1616203180000, "totalTransferedAmount": "0.00058795", "totalServiceChargeAmount": "0.000012", "transId": 4357015, "userAssetDribbletDetails": [ { "transId": 4357015, "serviceChargeAmount": "0.00001", "amount": "0.001", "operateTime": 1616203180000, "transferedAmount": "0.00049", "fromAsset": "USDT" }, { "transId": 4357015, "serviceChargeAmount": "0.000002", "amount": "0.0001", "operateTime": 1616203180000, "transferedAmount": "0.00009795", "fromAsset": "ETH" } ] } ] }；详见官方文档

### get_margin_dust_assets(**params)
说明：Get margin assets that can be converted into BNB. | [源码](同步 binance/client.py:3570-3596, 异步 binance/async_client.py:1045-1046) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "details": [ { "asset": "ADA", "assetFullName": "ADA", "amountFree": "6.21", "toBTC": "0.00016848", "toBNB": "0.01777302", "toBNBOffExchange": "0.01741756", "exchange": "0.00035546" } ], "totalTransferBtc": "0.00016848", "totalTransferBNB": "0.01777302", "dribbletPercentage": "0.02" }；详见官方文档

### transfer_margin_dust(**params)
说明：Convert dust assets to BNB. | [源码](同步 binance/client.py:3598-3630, 异步 binance/async_client.py:1050-1051) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "totalServiceCharge":"0.02102542", "totalTransfered":"1.05127099", "transferResult":[ { "amount":"0.03000000", "fromAsset":"ETH", "operateTime":1563368549307, "serviceChargeAmount":"0.00500000", "tranId":2970932918, "transferedAmount":"0.25000000" }, { "amount":"0.09000000", "fromAsset":"LTC", "operateTime":1563368549404, "serviceChargeAmount":"0.01548000", "tranId":2970932918, "transferedAmount":"0.77400000" } ] }；详见官方文档

### get_cross_margin_collateral_ratio(**params)
说明：https://developers.binance.com/docs/margin_trading/market-data | [源码](同步 binance/client.py:3632-3681, 异步 binance/async_client.py:1055-1058) | [官方文档](https://developers.binance.com/docs/margin_trading/market-data)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python [ { "collaterals": [ { "minUsdValue": "0", "maxUsdValue": "13000000", "discountRate": "1" }, { "minUsdValue": "13000000", "maxUsdValue": "20000000", "discountRate": "0.975" }, { "minUsdValue": "20000000", "discountRate": "0" } ], "assetNames": [ "BNX" ] }, { "collaterals": [ { "minUsdValue": "0", "discountRate": "1" } ], "assetNames": [ "BTC", "BUSD", "ETH", "USDT" ] } ]；详见官方文档

### get_small_liability_exchange_assets(**params)
说明：Query the coins which can be small liability exchange | [源码](同步 binance/client.py:3683-3704, 异步 binance/async_client.py:1064-1067) | [官方文档](https://developers.binance.com/docs/margin_trading/trade/Get-Small-Liability-Exchange-Coin-List)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python [ { "asset": "ETH", "interest": "0.00083334", "principal": "0.001", "liabilityAsset": "USDT", "liabilityQty": 0.3552 } ]；详见官方文档

### exchange_small_liability_assets(**params)
说明：Cross Margin Small Liability Exchange | [源码](同步 binance/client.py:3706-3722, 异步 binance/async_client.py:1073-1076) | [官方文档](https://developers.binance.com/docs/margin_trading/trade/Small-Liability-Exchange)

**核心参数**:
- ℹ️ **未标注**: assetNames (array) : The assets list of small liability exchange

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python none；详见官方文档

### get_small_liability_exchange_history(**params)
说明：Get Small liability Exchange History | [源码](同步 binance/client.py:3724-3758, 异步 binance/async_client.py:1082-1085) | [官方文档](https://developers.binance.com/docs/margin_trading/trade/Get-Small-Liability-Exchange-History)

**核心参数**:
- ℹ️ **未标注**: current (int) : Currently querying page. Start from 1. Default:1, size (int) : Default:10, Max:100, startTime (long) : Default: 30 days from current timestamp, endTime : Default: present timestamp, endTIme (long)

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "total": 1, "rows": [ { "asset": "ETH", "amount": "0.00083434", "targetAsset": "BUSD", "targetAmount": "1.37576819", "bizType": "EXCHANGE_SMALL_LIABILITY", "timestamp": 1672801339253 } ] }；详见官方文档

### get_future_hourly_interest_rate(**params)
说明：Get user the next hourly estimate interest | [源码](同步 binance/client.py:3760-3787, 异步 binance/async_client.py:1091-1094) | [官方文档](https://developers.binance.com/docs/margin_trading/borrow-and-repay)

**核心参数**:
- ℹ️ **未标注**: assets (str) : List of assets, separated by commas, up to 20, isIsolated (bool) : for isolated margin or not, "TRUE", "FALSE"

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python [ { "asset": "BTC", "nextHourlyInterestRate": "0.00000571" }, { "asset": "ETH", "nextHourlyInterestRate": "0.00000578" } ]；详见官方文档

### get_margin_capital_flow(**params)
说明：Get cross or isolated margin capital flow | [源码](同步 binance/client.py:3789-3834, 异步 binance/async_client.py:1100-1103) | [官方文档](https://developers.binance.com/docs/margin_trading/account/Query-Cross-Isolated-Margin-Capital-Flow)

**核心参数**:
- ✅ **必需**: symbol (str) : Required when querying isolated data
- ☑️ **可选**: asset (str) : optional, type (string) : optional, endTime (long) : optional
- ℹ️ **未标注**: startTime (long) : Only supports querying the data of the last 90 days, formId (long) : If fromId is set, the data with id > fromId will be returned. Otherwise the latest data will be returned, limit (long) : The number of data items returned each time is limited. Default 500; Max 1000.

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python [ { "id": 123456, "tranId": 123123, "timestamp": 1691116657000, "asset": "USDT, "symbol": "BTCUSDT", "type": "BORROW", "amount": "101" }, { "id": 123457, "tranId": 123124, "timestamp": 1691116658000, "asset": "BTC", "symbol": "BTCUSDT", "type": "REPAY", "amount": "10" } ]；详见官方文档

### get_margin_asset(**params)
说明：Query cross-margin asset | [源码](同步 binance/client.py:3836-3864, 异步 binance/async_client.py:1114-1115) | [官方文档](-)

**核心参数**:
- ℹ️ **未标注**: asset (str) : name of the asset

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "assetFullName": "Binance Coin", "assetName": "BNB", "isBorrowable": false, "isMortgageable": true, "userMinBorrow": "0.00000000", "userMinRepay": "0.00000000" }；详见官方文档

### get_margin_symbol(**params)
说明：Query cross-margin symbol info | [源码](同步 binance/client.py:3866-3896, 异步 binance/async_client.py:1119-1120) | [官方文档](-)

**核心参数**:
- ℹ️ **未标注**: symbol (str) : name of the symbol pair

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "id":323355778339572400, "symbol":"BTCUSDT", "base":"BTC", "quote":"USDT", "isMarginTrade":true, "isBuyAllowed":true, "isSellAllowed":true }；详见官方文档

### get_margin_all_assets(**params)
说明：Get All Margin Assets (MARKET_DATA) | [源码](同步 binance/client.py:3898-3933, 异步 binance/async_client.py:1124-1125) | [官方文档](https://developers.binance.com/docs/margin_trading/market-data/Get-All-Margin-Assets)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python [ { "assetFullName": "USD coin", "assetName": "USDC", "isBorrowable": true, "isMortgageable": true, "userMinBorrow": "0.00000000", "userMinRepay": "0.00000000" }, { "assetFullName": "BNB-coin", "assetName": "BNB", "isBorrowable": true, "isMortgageable": true, "userMinBorrow": "1.00000000", "userMinRepay": "0.00000000" } ]；详见官方文档

### get_margin_all_pairs(**params)
说明：Get All Cross Margin Pairs (MARKET_DATA) | [源码](同步 binance/client.py:3935-3972, 异步 binance/async_client.py:1129-1130) | [官方文档](https://developers.binance.com/docs/margin_trading/market-data/Get-All-Cross-Margin-Pairs)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python [ { "base": "BNB", "id": 351637150141315861, "isBuyAllowed": true, "isMarginTrade": true, "isSellAllowed": true, "quote": "BTC", "symbol": "BNBBTC" }, { "base": "TRX", "id": 351637923235429141, "isBuyAllowed": true, "isMarginTrade": true, "isSellAllowed": true, "quote": "BTC", "symbol": "TRXBTC" } ]；详见官方文档

### create_isolated_margin_account(**params)
说明：Create isolated margin account for symbol | [源码](同步 binance/client.py:3974-4003, 异步 binance/async_client.py:1134-1137) | [官方文档](-)

**核心参数**:
- ℹ️ **未标注**: base (str) : Base asset of symbol, quote (str) : Quote asset of symbol

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "success": true, "symbol": "BTCUSDT" }；详见官方文档

### get_isolated_margin_symbol(**params)
说明：Query isolated margin symbol info | [源码](同步 binance/client.py:4005-4036, 异步 binance/async_client.py:1143-1146) | [官方文档](-)

**核心参数**:
- ℹ️ **未标注**: symbol (str) : name of the symbol pair

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "symbol":"BTCUSDT", "base":"BTC", "quote":"USDT", "isMarginTrade":true, "isBuyAllowed":true, "isSellAllowed":true }；详见官方文档

### get_all_isolated_margin_symbols(**params)
说明：Query isolated margin symbol info for all pairs | [源码](同步 binance/client.py:4038-4076, 异步 binance/async_client.py:1150-1153) | [官方文档](https://developers.binance.com/docs/margin_trading/market-data/Get-All-Isolated-Margin-Symbol)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python [ { "base": "BNB", "isBuyAllowed": true, "isMarginTrade": true, "isSellAllowed": true, "quote": "BTC", "symbol": "BNBBTC" }, { "base": "TRX", "isBuyAllowed": true, "isMarginTrade": true, "isSellAllowed": true, "quote": "BTC", "symbol": "TRXBTC" } ]；详见官方文档

### get_isolated_margin_fee_data(**params)
说明：Get isolated margin fee data collection with any vip level or user's current specific data as https://www.binance.com/en/margin-fee | [源码](同步 binance/client.py:4078-4113, 异步 binance/async_client.py:1159-1162) | [官方文档](https://developers.binance.com/docs/margin_trading/account/Query-Isolated-Margin-Fee-Data)

**核心参数**:
- ☑️ **可选**: symbol (str) : optional
- ℹ️ **未标注**: vipLevel (int) : User's current specific margin data will be returned if vipLevel is omitted

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python [ { "vipLevel": 0, "symbol": "BTCUSDT", "leverage": "10", "data": [ { "coin": "BTC", "dailyInterest": "0.00026125", "borrowLimit": "270" }, { "coin": "USDT", "dailyInterest": "0.000475", "borrowLimit": "2100000" } ] } ]；详见官方文档

### get_isolated_margin_tier_data(**params)
说明：Get isolated margin tier data collection with any tier as https://www.binance.com/en/margin-data | [源码](同步 binance/client.py:4115-4145, 异步 binance/async_client.py:1166-1169) | [官方文档](https://developers.binance.com/docs/margin_trading/market-data/Query-Isolated-Margin-Tier-Data)

**核心参数**:
- ✅ **必需**: symbol (str) : required
- ☑️ **可选**: recvWindow : optional: No more than 60000
- ℹ️ **未标注**: tier (int) : All margin tier data will be returned if tier is omitted

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python [ { "symbol": "BTCUSDT", "tier": 1, "effectiveMultiple": "10", "initialRiskRatio": "1.111", "liquidationRiskRatio": "1.05", "baseAssetMaxBorrowable": "9", "quoteAssetMaxBorrowable": "70000" } ]；详见官方文档

### margin_manual_liquidation(**params)
说明：https://developers.binance.com/docs/margin_trading/trade/Margin-Manual-Liquidation | [源码](同步 binance/client.py:4147-4172, 异步 binance/async_client.py:1173-1176) | [官方文档](https://developers.binance.com/docs/margin_trading/trade/Margin-Manual-Liquidation)

**核心参数**:
- ✅ **必需**: type : required
- ℹ️ **未标注**: symbol (str: When type selected is "ISOLATED", symbol must be filled in)

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response [ { "asset": "ETH", "interest": "0.00083334", "principal": "0.001", "liabilityAsset": "USDT", "liabilityQty": 0.3552 } ]；详见官方文档

### toggle_bnb_burn_spot_margin(**params)
说明：Toggle BNB Burn On Spot Trade And Margin Interest | [源码](同步 binance/client.py:4174-4201, 异步 binance/async_client.py:1180-1183) | [官方文档](https://developers.binance.com/docs/wallet/asset/Toggle-BNB-Burn-On-Spot-Trade-And-Margin-Interest)

**核心参数**:
- ℹ️ **未标注**: spotBNBBurn (bool) : Determines whether to use BNB to pay for trading fees on SPOT, interestBNBBurn (bool) : Determines whether to use BNB to pay for margin loan's interest

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "spotBNBBurn":true, "interestBNBBurn": false }；详见官方文档

### get_bnb_burn_spot_margin(**params)
说明：Get BNB Burn Status | [源码](同步 binance/client.py:4203-4225, 异步 binance/async_client.py:1187-1190) | [官方文档](https://developers.binance.com/docs/margin_trading/account/Get-BNB-Burn-Status)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "spotBNBBurn":true, "interestBNBBurn": false }；详见官方文档

### get_margin_price_index(**params)
说明：Query margin priceIndex | [源码](同步 binance/client.py:4227-4252, 异步 binance/async_client.py:1194-1195) | [官方文档](https://developers.binance.com/docs/margin_trading/market-data/Query-Margin-PriceIndex)

**核心参数**:
- ℹ️ **未标注**: symbol (str) : name of the symbol pair

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "calcTime": 1562046418000, "price": "0.00333930", "symbol": "BNBBTC" }；详见官方文档

### transfer_margin_to_spot(**params)
说明：Execute transfer between cross-margin account and spot account. | [源码](同步 binance/client.py:4254-4284, 异步 binance/async_client.py:1199-1203) | [官方文档](-)

**核心参数**:
- ℹ️ **未标注**: asset (str) : name of the asset, amount (str) : amount to transfer, recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "tranId": 100000001 }；详见官方文档

### transfer_spot_to_margin(**params)
说明：Execute transfer between spot account and cross-margin account. | [源码](同步 binance/client.py:4286-4316, 异步 binance/async_client.py:1207-1211) | [官方文档](-)

**核心参数**:
- ℹ️ **未标注**: asset (str) : name of the asset, amount (str) : amount to transfer, recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "tranId": 100000001 }；详见官方文档

### transfer_isolated_margin_to_spot(**params)
说明：Execute transfer between isolated margin account and spot account. | [源码](同步 binance/client.py:4318-4352, 异步 binance/async_client.py:1215-1220) | [官方文档](-)

**核心参数**:
- ℹ️ **未标注**: asset (str) : name of the asset, symbol (str) : pair symbol, amount (str) : amount to transfer, recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "tranId": 100000001 }；详见官方文档

### transfer_spot_to_isolated_margin(**params)
说明：Execute transfer between spot account and isolated margin account. | [源码](同步 binance/client.py:4354-4388, 异步 binance/async_client.py:1226-1231) | [官方文档](-)

**核心参数**:
- ℹ️ **未标注**: asset (str) : name of the asset, symbol (str) : pair symbol, amount (str) : amount to transfer, recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "tranId": 100000001 }；详见官方文档

### get_isolated_margin_tranfer_history(**params)
说明：Get transfers to isolated margin account. | [源码](同步 binance/client.py:4390-4451, 异步 暂无对应实现) | [官方文档](-)

**核心参数**:
- ✅ **必需**: symbol (str) : pair required
- ☑️ **可选**: transFrom : optional SPOT, ISOLATED_MARGIN str SPOT, ISOLATED_MARGIN, transTo : optional str, startTime (int) : optional, endTime (int) : optional
- ℹ️ **未标注**: asset (str) : name of the asset, current (str) : Currently querying page. Start from 1. Default:1, size (int) : Default:10 Max:100, recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "rows": [ { "amount": "0.10000000", "asset": "BNB", "status": "CONFIRMED", "timestamp": 1566898617000, "txId": 5240372201, "transFrom": "SPOT", "transTo": "ISOLATED_MARGIN" }, { "amount": "5.00000000", "asset": "USDT", "status": "CONFIRMED", "timestamp": 1566888436123, "txId": 5239810406, "transFrom": "ISOLATED_MARGIN", "transTo": "SPOT" } ], "total": 2 }；详见官方文档

### create_margin_loan(**params)
说明：Apply for a loan in cross-margin or isolated-margin account. | [源码](同步 binance/client.py:4453-4487, 异步 binance/async_client.py:1237-1240) | [官方文档](-)

**核心参数**:
- ℹ️ **未标注**: asset (str) : name of the asset, amount (str) : amount to transfer, isIsolated (str) : set to 'TRUE' for isolated margin (default 'FALSE'), symbol (str) : Isolated margin symbol (default blank for cross-margin), recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "tranId": 100000001 }；详见官方文档

### repay_margin_loan(**params)
说明：Repay loan in cross-margin or isolated-margin account. | [源码](同步 binance/client.py:4489-4527, 异步 binance/async_client.py:1244-1247) | [官方文档](-)

**核心参数**:
- ℹ️ **未标注**: asset (str) : name of the asset, amount (str) : amount to transfer, isIsolated (str) : set to 'TRUE' for isolated margin (default 'FALSE'), symbol (str) : Isolated margin symbol (default blank for cross-margin), recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "tranId": 100000001 }；详见官方文档

### create_margin_order(**params)
说明：Post a new order for margin account. | [源码](同步 binance/client.py:4529-4652, 异步 binance/async_client.py:1251-1256) | [官方文档](https://developers.binance.com/docs/margin_trading/trade/Margin-Account-New-Order)

**核心参数**:
- ✅ **必需**: symbol (str) : required, side (str) : required, type (str) : required, quantity (decimal) : required, price (str) : required, timeInForce (str) : required if limit order GTC,IOC,FOK
- ℹ️ **未标注**: isIsolated (str) : set to 'TRUE' for isolated margin (default 'FALSE'), stopPrice (str) : Used with STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, and TAKE_PROFIT_LIMIT orders., newClientOrderId (str) : A unique id for the order. Automatically generated if not sent., icebergQty (str) : Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order., newOrderRespType (str) : Set the response JSON. ACK, RESULT, or FULL; MARKET and LIMIT order types default to, recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response Response ACK: .. code-block:: python { "symbol": "BTCUSDT", "orderId": 28, "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP", "transactTime": 1507725176595 } Response RESULT: .. code-block:: python { "symbol": "BTCUSDT", "orderId": 28, "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP", "transactTime": 1507725176595, "price": "1.00000000", "origQty": "10.00000000", "executedQty": "10.00000000", "cummulativeQuoteQty": "10.00000000", "status": "FILLED", "timeInForce": "GTC", "type": "MARKET", "side": "SELL" } Response FULL: .. code-block:: python { "symbol": "BTCUSDT", "orderId": 28, "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP", "transactTime": 1507725176595, "price": "1.00000000", "origQty": "10.00000000", "executedQty": "10.00000000", "cummulativeQuoteQty": "10.00000000", "status": "FILLED", "timeInForce": "GTC", "type": "MARKET", "side": "SELL", "fills": [ { "price": "4000.00000000", "qty": "1.00000000", "commission": "4.00000000", "commissionAsset": "USDT" }, { "price": "3999.00000000", "qty": "5.00000000", "commission": "19.99500000", "commissionAsset": "USDT" }, { "price": "3998.00000000", "qty": "2.00000000", "commission": "7.99600000", "commissionAsset": "USDT" }, { "price": "3997.00000000", "qty": "1.00000000", "commission": "3.99700000", "commissionAsset": "USDT" }, { "price": "3995.00000000", "qty": "1.00000000", "commission": "3.99500000", "commissionAsset": "USDT" } ] }；详见官方文档

### cancel_margin_order(**params)
说明：Cancel an active order for margin account. | [源码](同步 binance/client.py:4654-4697, 异步 binance/async_client.py:1260-1263) | [官方文档](https://developers.binance.com/docs/margin_trading/trade/Margin-Account-Cancel-Order)

**核心参数**:
- ✅ **必需**: symbol (str) : required
- ℹ️ **未标注**: isIsolated (str) : set to 'TRUE' for isolated margin (default 'FALSE'), orderId (str), origClientOrderId (str), newClientOrderId (str) : Used to uniquely identify this cancel. Automatically generated by default., recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response { "symbol": "LTCBTC", "orderId": 28, "origClientOrderId": "myOrder1", "clientOrderId": "cancelMyOrder1", "transactTime": 1507725176595, "price": "1.00000000", "origQty": "10.00000000", "executedQty": "8.00000000", "cummulativeQuoteQty": "8.00000000", "status": "CANCELED", "timeInForce": "GTC", "type": "LIMIT", "side": "SELL" }；详见官方文档

### cancel_all_open_margin_orders(**params)
说明：Cancels all active orders on a symbol for margin account. | [源码](同步 binance/client.py:4699-4717, 异步 binance/async_client.py:1267-1270) | [官方文档](https://developers.binance.com/docs/margin_trading/trade/Margin-Account-Cancel-All-Open-Orders)

**核心参数**:
- ✅ **必需**: symbol (str) : required
- ℹ️ **未标注**: isIsolated (str) : set to 'TRUE' for isolated margin (default 'FALSE'), recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### set_margin_max_leverage(**params)
说明：Adjust cross margin max leverage | [源码](同步 binance/client.py:4719-4738, 异步 binance/async_client.py:1274-1277) | [官方文档](https://developers.binance.com/docs/margin_trading/account)

**核心参数**:
- ✅ **必需**: maxLeverage (int) : required Can only adjust 3 or 5，Example: maxLeverage=3

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response { "success": true }；详见官方文档

### get_margin_transfer_history(**params)
说明：Query margin transfer history | [源码](同步 binance/client.py:4740-4799, 异步 binance/async_client.py:1281-1284) | [官方文档](https://developers.binance.com/docs/margin_trading/transfer)

**核心参数**:
- ☑️ **可选**: asset (str) : optional, type (str) : optional Transfer Type: ROLL_IN, ROLL_OUT, archived (str) : optional Default: false. Set to true for archived data from 6 months ago
- ℹ️ **未标注**: startTime (str) : earliest timestamp to filter transactions, endTime (str) : Used to uniquely identify this cancel. Automatically generated by default., current (str) : Currently querying page. Start from 1. Default:1, size (int) : Default:10 Max:100, recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response { "rows": [ { "amount": "0.10000000", "asset": "BNB", "status": "CONFIRMED", "timestamp": 1566898617, "txId": 5240372201, "type": "ROLL_IN" }, { "amount": "5.00000000", "asset": "USDT", "status": "CONFIRMED", "timestamp": 1566888436, "txId": 5239810406, "type": "ROLL_OUT" }, { "amount": "1.00000000", "asset": "EOS", "status": "CONFIRMED", "timestamp": 1566888403, "txId": 5239808703, "type": "ROLL_IN" } ], "total": 3 }；详见官方文档

### get_margin_loan_details(**params)
说明：Query loan record | [源码](同步 binance/client.py:4801-4843, 异步 binance/async_client.py:1288-1291) | [官方文档](-)

**核心参数**:
- ✅ **必需**: asset (str) : required
- ℹ️ **未标注**: isolatedSymbol (str) : isolated symbol (if querying isolated margin), txId (str) : the tranId in of the created loan, startTime (str) : earliest timestamp to filter transactions, endTime (str) : Used to uniquely identify this cancel. Automatically generated by default., current (str) : Currently querying page. Start from 1. Default:1, size (int) : Default:10 Max:100, recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response { "rows": [ { "asset": "BNB", "principal": "0.84624403", "timestamp": 1555056425000, //one of PENDING (pending to execution), CONFIRMED (successfully loaned), FAILED (execution failed, nothing happened to your account); "status": "CONFIRMED" } ], "total": 1 }；详见官方文档

### get_margin_repay_details(**params)
说明：Query repay record | [源码](同步 binance/client.py:4845-4893, 异步 binance/async_client.py:1295-1298) | [官方文档](-)

**核心参数**:
- ✅ **必需**: asset (str) : required
- ℹ️ **未标注**: isolatedSymbol (str) : isolated symbol (if querying isolated margin), txId (str) : the tranId in of the created loan, startTime (str), endTime (str) : Used to uniquely identify this cancel. Automatically generated by default., current (str) : Currently querying page. Start from 1. Default:1, size (int) : Default:10 Max:100, recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response { "rows": [ { //Total amount repaid "amount": "14.00000000", "asset": "BNB", //Interest repaid "interest": "0.01866667", //Principal repaid "principal": "13.98133333", //one of PENDING (pending to execution), CONFIRMED (successfully loaned), FAILED (execution failed, nothing happened to your account); "status": "CONFIRMED", "timestamp": 1563438204000, "txId": 2970933056 } ], "total": 1 }；详见官方文档

### get_cross_margin_data(**params)
说明：Query Cross Margin Fee Data (USER_DATA) | [源码](同步 binance/client.py:4895-4927, 异步 binance/async_client.py:1300-1303) | [官方文档](https://developers.binance.com/docs/margin_trading/account/Query-Cross-Margin-Fee-Data)

**核心参数**:
- ℹ️ **未标注**: vipLevel (int) : User's current specific margin data will be returned if vipLevel is omitted, coin (str), recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response (example): [ { "vipLevel": 0, "coin": "BTC", "transferIn": true, "borrowable": true, "dailyInterest": "0.00026125", "yearlyInterest": "0.0953", "borrowLimit": "180", "marginablePairs": [ "BNBBTC", "TRXBTC", "ETHBTC", "BTCUSDT" ] } ]；详见官方文档

### get_margin_interest_history(**params)
说明：Get Interest History (USER_DATA) | [源码](同步 binance/client.py:4929-4972, 异步 binance/async_client.py:1305-1308) | [官方文档](https://developers.binance.com/docs/margin_trading/borrow-and-repay/Get-Interest-History)

**核心参数**:
- ℹ️ **未标注**: asset (str), isolatedSymbol (str) : isolated symbol (if querying isolated margin), startTime (str), endTime (str), current (str) : Currently querying page. Start from 1. Default:1, size (int) : Default:10 Max:100, archived (bool) : Default: false. Set to true for archived data from 6 months ago, recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response { "rows":[ { "isolatedSymbol": "BNBUSDT", // isolated symbol, will not be returned for crossed margin "asset": "BNB", "interest": "0.02414667", "interestAccuredTime": 1566813600000, "interestRate": "0.01600000", "principal": "36.22000000", "type": "ON_BORROW" } ], "total": 1 }；详见官方文档

### get_margin_force_liquidation_rec(**params)
说明：Get Force Liquidation Record (USER_DATA) | [源码](同步 binance/client.py:4974-5015, 异步 binance/async_client.py:1310-1313) | [官方文档](https://developers.binance.com/docs/margin_trading/trade)

**核心参数**:
- ℹ️ **未标注**: startTime (str), endTime (str), isolatedSymbol (str) : isolated symbol (if querying isolated margin), current (str) : Currently querying page. Start from 1. Default:1, size (int) : Default:10 Max:100, recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response { "rows": [ { "avgPrice": "0.00388359", "executedQty": "31.39000000", "orderId": 180015097, "price": "0.00388110", "qty": "31.39000000", "side": "SELL", "symbol": "BNBBTC", "timeInForce": "GTC", "isIsolated": true, "updatedTime": 1558941374745 } ], "total": 1 }；详见官方文档

### get_margin_order(**params)
说明：Query margin accounts order | [源码](同步 binance/client.py:5017-5061, 异步 binance/async_client.py:1315-1318) | [官方文档](https://developers.binance.com/docs/margin_trading/trade/Query-Margin-Account-Order)

**核心参数**:
- ✅ **必需**: symbol (str) : required
- ℹ️ **未标注**: isIsolated (str) : set to 'TRUE' for isolated margin (default 'FALSE'), orderId (str), origClientOrderId (str), recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response { "clientOrderId": "ZwfQzuDIGpceVhKW5DvCmO", "cummulativeQuoteQty": "0.00000000", "executedQty": "0.00000000", "icebergQty": "0.00000000", "isWorking": true, "orderId": 213205622, "origQty": "0.30000000", "price": "0.00493630", "side": "SELL", "status": "NEW", "stopPrice": "0.00000000", "symbol": "BNBBTC", "time": 1562133008725, "timeInForce": "GTC", "type": "LIMIT", "updateTime": 1562133008725 }；详见官方文档

### get_open_margin_orders(**params)
说明：Query margin accounts open orders | [源码](同步 binance/client.py:5063-5110, 异步 binance/async_client.py:1320-1323) | [官方文档](https://developers.binance.com/docs/margin_trading/trade/Query-Margin-Account-Open-Orders)

**核心参数**:
- ☑️ **可选**: symbol (str) : optional
- ℹ️ **未标注**: isIsolated (str) : set to 'TRUE' for isolated margin (default 'FALSE'), recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response [ { "clientOrderId": "qhcZw71gAkCCTv0t0k8LUK", "cummulativeQuoteQty": "0.00000000", "executedQty": "0.00000000", "icebergQty": "0.00000000", "isWorking": true, "orderId": 211842552, "origQty": "0.30000000", "price": "0.00475010", "side": "SELL", "status": "NEW", "stopPrice": "0.00000000", "symbol": "BNBBTC", "time": 1562040170089, "timeInForce": "GTC", "type": "LIMIT", "updateTime": 1562040170089 } ]；详见官方文档

### get_all_margin_orders(**params)
说明：Query all margin accounts orders | [源码](同步 binance/client.py:5112-5171, 异步 binance/async_client.py:1325-1328) | [官方文档](https://developers.binance.com/docs/margin_trading/trade/Query-Margin-Account-All-Orders)

**核心参数**:
- ✅ **必需**: symbol (str) : required
- ☑️ **可选**: orderId (str) : optional, startTime (str) : optional, endTime (str) : optional
- ℹ️ **未标注**: isIsolated (str) : set to 'TRUE' for isolated margin (default 'FALSE'), limit (int) : Default 500; max 1000, recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response [ { "id": 43123876, "price": "0.00395740", "qty": "4.06000000", "quoteQty": "0.01606704", "symbol": "BNBBTC", "time": 1556089977693 }, { "id": 43123877, "price": "0.00395740", "qty": "0.77000000", "quoteQty": "0.00304719", "symbol": "BNBBTC", "time": 1556089977693 }, { "id": 43253549, "price": "0.00428930", "qty": "23.30000000", "quoteQty": "0.09994069", "symbol": "BNBBTC", "time": 1556163963504 } ]；详见官方文档

### get_margin_trades(**params)
说明：Query margin accounts trades | [源码](同步 binance/client.py:5173-5231, 异步 binance/async_client.py:1330-1333) | [官方文档](https://developers.binance.com/docs/margin_trading/trade/Query-Margin-Account-Trade-List)

**核心参数**:
- ✅ **必需**: symbol (str) : required
- ☑️ **可选**: fromId (str) : optional, startTime (str) : optional, endTime (str) : optional
- ℹ️ **未标注**: isIsolated (str) : set to 'TRUE' for isolated margin (default 'FALSE'), limit (int) : Default 500; max 1000, recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response [ { "commission": "0.00006000", "commissionAsset": "BTC", "id": 34, "isBestMatch": true, "isBuyer": false, "isMaker": false, "orderId": 39324, "price": "0.02000000", "qty": "3.00000000", "symbol": "BNBBTC", "time": 1561973357171 }, { "commission": "0.00002950", "commissionAsset": "BTC", "id": 32, "isBestMatch": true, "isBuyer": false, "isMaker": true, "orderId": 39319, "price": "0.00590000", "qty": "5.00000000", "symbol": "BNBBTC", "time": 1561964645345 } ]；详见官方文档

### get_max_margin_loan(**params)
说明：Query max borrow amount for an asset | [源码](同步 binance/client.py:5233-5256, 异步 binance/async_client.py:1335-1338) | [官方文档](-)

**核心参数**:
- ✅ **必需**: asset (str) : required
- ℹ️ **未标注**: isolatedSymbol (str) : isolated symbol (if querying isolated margin), recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response { "amount": "1.69248805" }；详见官方文档

### get_max_margin_transfer(**params)
说明：Query max transfer-out amount | [源码](同步 binance/client.py:5258-5281, 异步 binance/async_client.py:1340-1343) | [官方文档](https://developers.binance.com/docs/margin_trading/transfer/Query-Max-Transfer-Out-Amount)

**核心参数**:
- ✅ **必需**: asset (str) : required
- ℹ️ **未标注**: isolatedSymbol (str) : isolated symbol (if querying isolated margin), recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response { "amount": "3.59498107" }；详见官方文档

### get_margin_delist_schedule(**params)
说明：Get tokens or symbols delist schedule for cross margin and isolated margin | [源码](同步 binance/client.py:5283-5317, 异步 binance/async_client.py:1107-1110) | [官方文档](https://developers.binance.com/docs/margin_trading/market-data/Get-Delist-Schedule)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional - the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python [ { "delistTime": 1686161202000, "crossMarginAssets": [ "BTC", "USDT" ], "isolatedMarginSymbols": [ "ADAUSDT", "BNBUSDT" ] }, { "delistTime": 1686222232000, "crossMarginAssets": [ "ADA" ], "isolatedMarginSymbols": [] } ]；详见官方文档

### create_margin_oco_order(**params)
说明：Post a new OCO trade for margin account. | [源码](同步 binance/client.py:5321-5429, 异步 binance/async_client.py:1347-1350) | [官方文档](https://developers.binance.com/docs/margin_trading/trade/Margin-Account-New-OCO)

**核心参数**:
- ✅ **必需**: symbol (str) : required, side (str) : required, quantity (decimal) : required, price (str) : required, stopPrice (str) : required, stopLimitPrice (str) : If provided, stopLimitTimeInForce is required.
- ℹ️ **未标注**: isIsolated : for isolated margin or not, "TRUE", "FALSE"，default "FALSE", listClientOrderId (str) : A unique id for the list order. Automatically generated if not sent., limitClientOrderId (str) : A unique id for the limit order. Automatically generated if not sent., limitIcebergQty (decimal) : Used to make the LIMIT_MAKER leg an iceberg order., stopClientOrderId (str) : A unique Id for the stop loss/stop loss limit leg. Automatically generated if not sent., stopIcebergQty (decimal) : Used with STOP_LOSS_LIMIT leg to make an iceberg order., stopLimitTimeInForce (str) : Valid values are GTC/FOK/IOC., newOrderRespType (str) : Set the response JSON. ACK, RESULT, or FULL; default: RESULT., sideEffectType (str) : NO_SIDE_EFFECT, MARGIN_BUY, AUTO_REPAY; default NO_SIDE_EFFECT., recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "orderListId": 0, "contingencyType": "OCO", "listStatusType": "EXEC_STARTED", "listOrderStatus": "EXECUTING", "listClientOrderId": "JYVpp3F0f5CAG15DhtrqLp", "transactionTime": 1563417480525, "symbol": "LTCBTC", "marginBuyBorrowAmount": "5",       // will not return if no margin trade happens "marginBuyBorrowAsset": "BTC",    // will not return if no margin trade happens "isIsolated": false,       // if isolated margin "orders": [ { "symbol": "LTCBTC", "orderId": 2, "clientOrderId": "Kk7sqHb9J6mJWTMDVW7Vos" }, { "symbol": "LTCBTC", "orderId": 3, "clientOrderId": "xTXKaGYd4bluPVp78IVRvl" } ], "orderReports": [ { "symbol": "LTCBTC", "orderId": 2, "orderListId": 0, "clientOrderId": "Kk7sqHb9J6mJWTMDVW7Vos", "transactTime": 1563417480525, "price": "0.000000", "origQty": "0.624363", "executedQty": "0.000000", "cummulativeQuoteQty": "0.000000", "status": "NEW", "timeInForce": "GTC", "type": "STOP_LOSS", "side": "BUY", "stopPrice": "0.960664" }, { "symbol": "LTCBTC", "orderId": 3, "orderListId": 0, "clientOrderId": "xTXKaGYd4bluPVp78IVRvl", "transactTime": 1563417480525, "price": "0.036435", "origQty": "0.624363", "executedQty": "0.000000", "cummulativeQuoteQty": "0.000000", "status": "NEW", "timeInForce": "GTC", "type": "LIMIT_MAKER", "side": "BUY" } ] }；详见官方文档

### cancel_margin_oco_order(**params)
说明：Cancel an entire Order List for a margin account. | [源码](同步 binance/client.py:5431-5512, 异步 binance/async_client.py:1352-1355) | [官方文档](https://developers.binance.com/docs/margin_trading/trade/Margin-Account-Cancel-OCO)

**核心参数**:
- ✅ **必需**: symbol (str) : required
- ℹ️ **未标注**: isIsolated : for isolated margin or not, "TRUE", "FALSE"，default "FALSE", orderListId (int) : Either orderListId or listClientOrderId must be provided, listClientOrderId (str) : Either orderListId or listClientOrderId must be provided, newClientOrderId (str) : Used to uniquely identify this cancel. Automatically generated by default., recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "orderListId": 0, "contingencyType": "OCO", "listStatusType": "ALL_DONE", "listOrderStatus": "ALL_DONE", "listClientOrderId": "C3wyj4WVEktd7u9aVBRXcN", "transactionTime": 1574040868128, "symbol": "LTCBTC", "isIsolated": false,       // if isolated margin "orders": [ { "symbol": "LTCBTC", "orderId": 2, "clientOrderId": "pO9ufTiFGg3nw2fOdgeOXa" }, { "symbol": "LTCBTC", "orderId": 3, "clientOrderId": "TXOvglzXuaubXAaENpaRCB" } ], "orderReports": [ { "symbol": "LTCBTC", "origClientOrderId": "pO9ufTiFGg3nw2fOdgeOXa", "orderId": 2, "orderListId": 0, "clientOrderId": "unfWT8ig8i0uj6lPuYLez6", "price": "1.00000000", "origQty": "10.00000000", "executedQty": "0.00000000", "cummulativeQuoteQty": "0.00000000", "status": "CANCELED", "timeInForce": "GTC", "type": "STOP_LOSS_LIMIT", "side": "SELL", "stopPrice": "1.00000000" }, { "symbol": "LTCBTC", "origClientOrderId": "TXOvglzXuaubXAaENpaRCB", "orderId": 3, "orderListId": 0, "clientOrderId": "unfWT8ig8i0uj6lPuYLez6", "price": "3.00000000", "origQty": "10.00000000", "executedQty": "0.00000000", "cummulativeQuoteQty": "0.00000000", "status": "CANCELED", "timeInForce": "GTC", "type": "LIMIT_MAKER", "side": "SELL" } ] }；详见官方文档

### get_margin_oco_order(**params)
说明：Retrieves a specific OCO based on provided optional parameters | [源码](同步 binance/client.py:5514-5558, 异步 binance/async_client.py:1357-1360) | [官方文档](https://developers.binance.com/docs/margin_trading/trade/Query-Margin-Account-OCO)

**核心参数**:
- ℹ️ **未标注**: isIsolated : for isolated margin or not, "TRUE", "FALSE"，default "FALSE", symbol (str) : mandatory for isolated margin, not supported for cross margin, orderListId (int) : Either orderListId or listClientOrderId must be provided, listClientOrderId (str) : Either orderListId or listClientOrderId must be provided, recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response { "orderListId": 27, "contingencyType": "OCO", "listStatusType": "EXEC_STARTED", "listOrderStatus": "EXECUTING", "listClientOrderId": "h2USkA5YQpaXHPIrkd96xE", "transactionTime": 1565245656253, "symbol": "LTCBTC", "isIsolated": false,       // if isolated margin "orders": [ { "symbol": "LTCBTC", "orderId": 4, "clientOrderId": "qD1gy3kc3Gx0rihm9Y3xwS" }, { "symbol": "LTCBTC", "orderId": 5, "clientOrderId": "ARzZ9I00CPM8i3NhmU9Ega" } ] }；详见官方文档

### get_open_margin_oco_orders(**params)
说明：Retrieves open OCO trades | [源码](同步 binance/client.py:5560-5631, 异步 binance/async_client.py:1362-1365) | [官方文档](https://developers.binance.com/docs/margin_trading/trade/Query-Margin-Account-Open-OCO)

**核心参数**:
- ☑️ **可选**: startTime (int) : optional, endTime (int) : optional, limit (int) : optional Default Value: 500; Max Value: 1000
- ℹ️ **未标注**: isIsolated : for isolated margin or not, "TRUE", "FALSE"，default "FALSE", symbol (str) : mandatory for isolated margin, not supported for cross margin, fromId (int) : If supplied, neither startTime or endTime can be provided, recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response [ { "orderListId": 29, "contingencyType": "OCO", "listStatusType": "EXEC_STARTED", "listOrderStatus": "EXECUTING", "listClientOrderId": "amEEAXryFzFwYF1FeRpUoZ", "transactionTime": 1565245913483, "symbol": "LTCBTC", "isIsolated": true,       // if isolated margin "orders": [ { "symbol": "LTCBTC", "orderId": 4, "clientOrderId": "oD7aesZqjEGlZrbtRpy5zB" }, { "symbol": "LTCBTC", "orderId": 5, "clientOrderId": "Jr1h6xirOxgeJOUuYQS7V3" } ] }, { "orderListId": 28, "contingencyType": "OCO", "listStatusType": "EXEC_STARTED", "listOrderStatus": "EXECUTING", "listClientOrderId": "hG7hFNxJV6cZy3Ze4AUT4d", "transactionTime": 1565245913407, "symbol": "LTCBTC", "orders": [ { "symbol": "LTCBTC", "orderId": 2, "clientOrderId": "j6lFOfbmFMRjTYA7rRJ0LP" }, { "symbol": "LTCBTC", "orderId": 3, "clientOrderId": "z0KCjOdditiLS5ekAFtK81" } ] } ]；详见官方文档

### margin_stream_get_listen_key()
说明：Start a new cross-margin data stream and return the listen key | [源码](同步 binance/client.py:5635-5656, 异步 binance/async_client.py:1369-1373) | [官方文档](https://developers.binance.com/docs/margin_trading/trade-data-stream/Start-Margin-User-Data-Stream)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "listenKey": "pqia91ma19a5s61cv6a81va65sdf19v8a65a1a5s61cv6a81va65sdf19v8a65a1" }；详见官方文档

### margin_stream_keepalive(listenKey)
说明：PING a cross-margin data stream to prevent a time out. | [源码](同步 binance/client.py:5658-5678, 异步 binance/async_client.py:1375-1379) | [官方文档](https://developers.binance.com/docs/margin_trading/trade-data-stream/Keepalive-Margin-User-Data-Stream)

**核心参数**:
- ✅ **必需**: listenKey (str) : required

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python {}；详见官方文档

### margin_stream_close(listenKey)
说明：Close out a cross-margin data stream. | [源码](同步 binance/client.py:5680-5700, 异步 binance/async_client.py:1381-1385) | [官方文档](https://developers.binance.com/docs/margin_trading/trade-data-stream/Close-Margin-User-Data-Stream)

**核心参数**:
- ✅ **必需**: listenKey (str) : required

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python {}；详见官方文档

### isolated_margin_stream_get_listen_key(symbol)
说明：Start a new isolated margin data stream and return the listen key | [源码](同步 binance/client.py:5704-5731, 异步 binance/async_client.py:1389-1394) | [官方文档](https://developers.binance.com/docs/margin_trading/trade-data-stream/Start-Isolated-Margin-User-Data-Stream)

**核心参数**:
- ✅ **必需**: symbol (str) : required - symbol for the isolated margin account

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "listenKey":  "T3ee22BIYuWqmvne0HNq2A2WsFlEtLhvWCtItw6ffhhdmjifQ2tRbuKkTHhr" }；详见官方文档

### isolated_margin_stream_keepalive(symbol, listenKey)
说明：PING an isolated margin data stream to prevent a time out. | [源码](同步 binance/client.py:5733-5755, 异步 binance/async_client.py:1396-1400) | [官方文档](https://developers.binance.com/docs/margin_trading/trade-data-stream/Keepalive-Isolated-Margin-User-Data-Stream)

**核心参数**:
- ✅ **必需**: symbol (str) : required - symbol for the isolated margin account, listenKey (str) : required

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python {}；详见官方文档

### isolated_margin_stream_close(symbol, listenKey)
说明：Close out an isolated margin data stream. | [源码](同步 binance/client.py:5757-5779, 异步 binance/async_client.py:1402-1406) | [官方文档](https://developers.binance.com/docs/margin_trading/trade-data-stream/Close-Isolated-Margin-User-Data-Stream)

**核心参数**:
- ✅ **必需**: symbol (str) : required - symbol for the isolated margin account, listenKey (str) : required

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python {}；详见官方文档

### get_simple_earn_flexible_product_list(**params)
说明：Get available Simple Earn flexible product list | [源码](同步 binance/client.py:5783-5829, 异步 binance/async_client.py:1410-1413) | [官方文档](-)

**核心参数**:
- ☑️ **可选**: asset (str) : optional, current (int) : optional - Currently querying page. Start from 1. Default:1, size (int) : optional - Default:10, Max:100
- ℹ️ **未标注**: recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "rows":[ { "asset": "BTC", "latestAnnualPercentageRate": "0.05000000", "tierAnnualPercentageRate": { "0-5BTC": 0.05, "5-10BTC": 0.03 }, "airDropPercentageRate": "0.05000000", "canPurchase": true, "canRedeem": true, "isSoldOut": true, "hot": true, "minPurchaseAmount": "0.01000000", "productId": "BTC001", "subscriptionStartTime": "1646182276000", "status": "PURCHASING" } ], "total": 1 }；详见官方文档

### get_simple_earn_locked_product_list(**params)
说明：Get available Simple Earn flexible product list | [源码](同步 binance/client.py:5831-5879, 异步 binance/async_client.py:1419-1422) | [官方文档](-)

**核心参数**:
- ☑️ **可选**: asset (str) : optional, current (int) : optional - Currently querying page. Start from 1. Default:1, size (int) : optional - Default:10, Max:100
- ℹ️ **未标注**: recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "rows": [ { "projectId": "Axs*90", "detail": { "asset": "AXS", "rewardAsset": "AXS", "duration": 90, "renewable": true, "isSoldOut": true, "apr": "1.2069", "status": "CREATED", "subscriptionStartTime": "1646182276000", "extraRewardAsset": "BNB", "extraRewardAPR": "0.23" }, "quota": { "totalPersonalQuota": "2", "minimum": "0.001" } } ], "total": 1 }；详见官方文档

### subscribe_simple_earn_flexible_product(**params)
说明：Subscribe to a simple earn flexible product | [源码](同步 binance/client.py:5881-5909, 异步 binance/async_client.py:1428-1431) | [官方文档](-)

**核心参数**:
- ✅ **必需**: productId (str) : required, amount (str) : required
- ☑️ **可选**: autoSubscribe (bool) : optional - Default True
- ℹ️ **未标注**: recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "purchaseId": 40607, "success": true }；详见官方文档

### subscribe_simple_earn_locked_product(**params)
说明：Subscribe to a simple earn locked product | [源码](同步 binance/client.py:5911-5940, 异步 binance/async_client.py:1437-1440) | [官方文档](-)

**核心参数**:
- ✅ **必需**: productId (str) : required, amount (str) : required
- ☑️ **可选**: autoSubscribe (bool) : optional - Default True
- ℹ️ **未标注**: recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "purchaseId": 40607, "positionId": "12345", "success": true }；详见官方文档

### redeem_simple_earn_flexible_product(**params)
说明：Redeem a simple earn flexible product | [源码](同步 binance/client.py:5942-5970, 异步 binance/async_client.py:1446-1449) | [官方文档](-)

**核心参数**:
- ✅ **必需**: productId (str) : required
- ☑️ **可选**: amount (str) : optional, redeemAll (bool) : optional - Default False
- ℹ️ **未标注**: recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "redeemId": 40607, "success": true }；详见官方文档

### redeem_simple_earn_locked_product(**params)
说明：Redeem a simple earn locked product | [源码](同步 binance/client.py:5972-5996, 异步 binance/async_client.py:1455-1458) | [官方文档](-)

**核心参数**:
- ✅ **必需**: productId (str) : required
- ℹ️ **未标注**: recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "redeemId": 40607, "success": true }；详见官方文档

### get_simple_earn_flexible_product_position(**params)
说明：https://binance-docs.github.io/apidocs/spot/en/#get-flexible-product-position-user_data | [源码](同步 binance/client.py:5998-6046, 异步 binance/async_client.py:1464-1467) | [官方文档](-)

**核心参数**:
- ☑️ **可选**: asset (str) : optional, current (int) : optional - Currently querying page. Start from 1. Default:1, size (int) : optional - Default:10, Max:100
- ℹ️ **未标注**: recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "rows":[ { "totalAmount": "75.46000000", "tierAnnualPercentageRate": { "0-5BTC": 0.05, "5-10BTC": 0.03 }, "latestAnnualPercentageRate": "0.02599895", "yesterdayAirdropPercentageRate": "0.02599895", "asset": "USDT", "airDropAsset": "BETH", "canRedeem": true, "collateralAmount": "232.23123213", "productId": "USDT001", "yesterdayRealTimeRewards": "0.10293829", "cumulativeBonusRewards": "0.22759183", "cumulativeRealTimeRewards": "0.22759183", "cumulativeTotalRewards": "0.45459183", "autoSubscribe": true } ], "total": 1 }；详见官方文档

### get_simple_earn_locked_product_position(**params)
说明：https://binance-docs.github.io/apidocs/spot/en/#get-locked-product-position-user_data | [源码](同步 binance/client.py:6048-6091, 异步 binance/async_client.py:1473-1476) | [官方文档](-)

**核心参数**:
- ☑️ **可选**: asset (str) : optional, current (int) : optional - Currently querying page. Start from 1. Default:1, size (int) : optional - Default:10, Max:100
- ℹ️ **未标注**: recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "rows":[ { "positionId": "123123", "projectId": "Axs*90", "asset": "AXS", "amount": "122.09202928", "purchaseTime": "1646182276000", "duration": "60", "accrualDays": "4", "rewardAsset": "AXS", "APY": "0.23", "isRenewable": true, "isAutoRenew": true, "redeemDate": "1732182276000" } ], "total": 1 }；详见官方文档

### get_simple_earn_account(**params)
说明：https://binance-docs.github.io/apidocs/spot/en/#simple-account-user_data | [源码](同步 binance/client.py:6093-6119, 异步 binance/async_client.py:1482-1485) | [官方文档](-)

**核心参数**:
- ℹ️ **未标注**: recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "totalAmountInBTC": "0.01067982", "totalAmountInUSDT": "77.13289230", "totalFlexibleAmountInBTC": "0.00000000", "totalFlexibleAmountInUSDT": "0.00000000", "totalLockedInBTC": "0.01067982", "totalLockedInUSDT": "77.13289230" }；详见官方文档

### get_fixed_activity_project_list(**params)
说明：Get Fixed and Activity Project List | [源码](同步 binance/client.py:6123-6173, 异步 binance/async_client.py:1491-1494) | [官方文档](-)

**核心参数**:
- ✅ **必需**: type (str) : required - "ACTIVITY", "CUSTOMIZED_FIXED"
- ☑️ **可选**: asset (str) : optional, status (str) : optional - "ALL", "SUBSCRIBABLE", "UNSUBSCRIBABLE"; default "ALL", sortBy (str) : optional - "START_TIME", "LOT_SIZE", "INTEREST_RATE", "DURATION"; default "START_TIME", current (int) : optional - Currently querying page. Start from 1. Default:1, size (int) : optional - Default:10, Max:100
- ℹ️ **未标注**: recvWindow (int) : the number of milliseconds the request is valid for

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python [ { "asset": "USDT", "displayPriority": 1, "duration": 90, "interestPerLot": "1.35810000", "interestRate": "0.05510000", "lotSize": "100.00000000", "lotsLowLimit": 1, "lotsPurchased": 74155, "lotsUpLimit": 80000, "maxLotsPerUser": 2000, "needKyc": False, "projectId": "CUSDT90DAYSS001", "projectName": "USDT", "status": "PURCHASING", "type": "CUSTOMIZED_FIXED", "withAreaLimitation": False } ]；详见官方文档

### change_fixed_activity_to_daily_position(**params)
说明：Change Fixed/Activity Position to Daily Position | [源码](同步 binance/client.py:6175-6183, 异步 binance/async_client.py:1496-1499) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### get_staking_product_list(**params)
说明：Get Staking Product List | [源码](同步 binance/client.py:6187-6195, 异步 binance/async_client.py:1503-1506) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### purchase_staking_product(**params)
说明：Purchase Staking Product | [源码](同步 binance/client.py:6197-6205, 异步 binance/async_client.py:1508-1511) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### redeem_staking_product(**params)
说明：Redeem Staking Product | [源码](同步 binance/client.py:6207-6215, 异步 binance/async_client.py:1513-1516) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### get_staking_position(**params)
说明：Get Staking Product Position | [源码](同步 binance/client.py:6217-6225, 异步 binance/async_client.py:1518-1521) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### get_staking_purchase_history(**params)
说明：Get Staking Purchase History | [源码](同步 binance/client.py:6227-6235, 异步 binance/async_client.py:1523-1526) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### set_auto_staking(**params)
说明：Set Auto Staking on Locked Staking or Locked DeFi Staking | [源码](同步 binance/client.py:6237-6245, 异步 binance/async_client.py:1528-1531) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### get_personal_left_quota(**params)
说明：Get Personal Left Quota of Staking Product | [源码](同步 binance/client.py:6247-6255, 异步 binance/async_client.py:1533-1536) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### get_staking_asset_us(**params)
说明：Get staking information for a supported asset (or assets) | [源码](同步 binance/client.py:6259-6266, 异步 binance/async_client.py:1540-1542) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### stake_asset_us(**params)
说明：Stake a supported asset. | [源码](同步 binance/client.py:6268-6275, 异步 binance/async_client.py:1546-1550) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### unstake_asset_us(**params)
说明：Unstake a staked asset | [源码](同步 binance/client.py:6277-6284, 异步 binance/async_client.py:1554-1558) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### get_staking_balance_us(**params)
说明：Get staking balance | [源码](同步 binance/client.py:6286-6295, 异步 binance/async_client.py:1562-1566) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### get_staking_history_us(**params)
说明：Get staking history | [源码](同步 binance/client.py:6297-6304, 异步 binance/async_client.py:1570-1574) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### get_staking_rewards_history_us(**params)
说明：Get staking rewards history for an asset(or assets) within a given time range. | [源码](同步 binance/client.py:6306-6315, 异步 binance/async_client.py:1578-1582) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### get_sub_account_list(**params)
说明：Query Sub-account List. | [源码](同步 binance/client.py:6319-6357, 异步 binance/async_client.py:1590-1593) | [官方文档](https://developers.binance.com/docs/sub_account/account-management/Query-Sub-account-List)

**核心参数**:
- ☑️ **可选**: email (str) : optional - Sub-account email, isFreeze (str) : optional, page (int) : optional - Default value: 1, limit (int) : optional - Default value: 1, Max value: 200, recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "subAccounts":[ { "email":"testsub@gmail.com", "isFreeze":false, "createTime":1544433328000 }, { "email":"virtual@oxebmvfonoemail.com", "isFreeze":false, "createTime":1544433328000 } ] }；详见官方文档

### get_sub_account_transfer_history(**params)
说明：Query Sub-account Transfer History. | [源码](同步 binance/client.py:6359-6409, 异步 binance/async_client.py:1595-1598) | [官方文档](https://developers.binance.com/docs/sub_account/asset-management/Query-Sub-account-Spot-Asset-Transfer-History)

**核心参数**:
- ☑️ **可选**: fromEmail (str) : optional, toEmail (str) : optional, startTime (int) : optional, endTime (int) : optional, page (int) : optional - Default value: 1, limit (int) : optional - Default value: 500, recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python [ { "from":"aaa@test.com", "to":"bbb@test.com", "asset":"BTC", "qty":"10", "status": "SUCCESS", "tranId": 6489943656, "time":1544433328000 }, { "from":"bbb@test.com", "to":"ccc@test.com", "asset":"ETH", "qty":"2", "status": "SUCCESS", "tranId": 6489938713, "time":1544433328000 } ]；详见官方文档

### get_sub_account_futures_transfer_history(**params)
说明：Query Sub-account Futures Transfer History. | [源码](同步 binance/client.py:6411-6461, 异步 binance/async_client.py:1600-1603) | [官方文档](https://developers.binance.com/docs/sub_account/asset-management/Query-Sub-account-Futures-Asset-Transfer-History)

**核心参数**:
- ✅ **必需**: email (str) : required, futuresType (int) : required
- ☑️ **可选**: startTime (int) : optional, endTime (int) : optional, page (int) : optional, limit (int) : optional, recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "success":true, "futuresType": 2, "transfers":[ { "from":"aaa@test.com", "to":"bbb@test.com", "asset":"BTC", "qty":"1", "time":1544433328000 }, { "from":"bbb@test.com", "to":"ccc@test.com", "asset":"ETH", "qty":"2", "time":1544433328000 } ] }；详见官方文档

### create_sub_account_futures_transfer(**params)
说明：Execute sub-account Futures transfer | [源码](同步 binance/client.py:6463-6495, 异步 binance/async_client.py:1605-1608) | [官方文档](https://developers.binance.com/docs/sub_account/asset-management/Sub-account-Futures-Asset-Transfer)

**核心参数**:
- ✅ **必需**: fromEmail (str) : required - Sender email, toEmail (str) : required - Recipient email, futuresType (int) : required, asset (str) : required, amount (decimal) : required
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "success":true, "txnId":"2934662589" }；详见官方文档

### get_sub_account_assets(**params)
说明：Fetch sub-account assets | [源码](同步 binance/client.py:6497-6546, 异步 binance/async_client.py:1610-1613) | [官方文档](https://developers.binance.com/docs/sub_account/asset-management/Query-Sub-account-Assets-V4)

**核心参数**:
- ✅ **必需**: email (str) : required
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "balances":[ { "asset":"ADA", "free":10000, "locked":0 }, { "asset":"BNB", "free":10003, "locked":0 }, { "asset":"BTC", "free":11467.6399, "locked":0 }, { "asset":"ETH", "free":10004.995, "locked":0 }, { "asset":"USDT", "free":11652.14213, "locked":0 } ] }；详见官方文档

### query_subaccount_spot_summary(**params)
说明：Query Sub-account Spot Assets Summary (For Master Account) | [源码](同步 binance/client.py:6548-6586, 异步 binance/async_client.py:1615-1618) | [官方文档](https://developers.binance.com/docs/sub_account/asset-management/Query-Sub-account-Spot-Assets-Summary)

**核心参数**:
- ☑️ **可选**: email (str) : optional - Sub account email, page (int) : optional - default 1, size (int) : optional - default 10, max 20, recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "totalCount":2, "masterAccountTotalAsset": "0.23231201", "spotSubUserAssetBtcVoList":[ { "email":"sub123@test.com", "totalAsset":"9999.00000000" }, { "email":"test456@test.com", "totalAsset":"0.00000000" } ] }；详见官方文档

### get_subaccount_deposit_address(**params)
说明：Get Sub-account Deposit Address (For Master Account) | [源码](同步 binance/client.py:6588-6618, 异步 binance/async_client.py:1620-1623) | [官方文档](https://developers.binance.com/docs/sub_account/asset-management/Get-Sub-account-Deposit-Address)

**核心参数**:
- ✅ **必需**: email (str) : required - Sub account email, coin (str) : required
- ☑️ **可选**: network (str) : optional, recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "address":"TDunhSa7jkTNuKrusUTU1MUHtqXoBPKETV", "coin":"USDT", "tag":"", "url":"https://tronscan.org/#/address/TDunhSa7jkTNuKrusUTU1MUHtqXoBPKETV" }；详见官方文档

### get_subaccount_deposit_history(**params)
说明：Get Sub-account Deposit History (For Master Account) | [源码](同步 binance/client.py:6620-6678, 异步 binance/async_client.py:1625-1628) | [官方文档](https://developers.binance.com/docs/sub_account/asset-management/Get-Sub-account-Deposit-History)

**核心参数**:
- ✅ **必需**: email (str) : required - Sub account email
- ☑️ **可选**: coin (str) : optional, status (int) : optional - (0:pending,6: credited but cannot withdraw, 1:success), startTime (int) : optional, endTime (int) : optional, limit (int) : optional, offset (int) : optional - default:0, recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python [ { "amount":"0.00999800", "coin":"PAXG", "network":"ETH", "status":1, "address":"0x788cabe9236ce061e5a892e1a59395a81fc8d62c", "addressTag":"", "txId":"0xaad4654a3234aa6118af9b4b335f5ae81c360b2394721c019b5d1e75328b09f3", "insertTime":1599621997000, "transferType":0, "confirmTimes":"12/12" }, { "amount":"0.50000000", "coin":"IOTA", "network":"IOTA", "status":1, "address":"SIZ9VLMHWATXKV99LH99CIGFJFUMLEHGWVZVNNZXRJJVWBPHYWPPBOSDORZ9EQSHCZAMPVAPGFYQAUUV9DROOXJLNW", "addressTag":"", "txId":"ESBFVQUTPIWQNJSPXFNHNYHSQNTGKRVKPRABQWTAXCDWOAKDKYWPTVG9BGXNVNKTLEJGESAVXIKIZ9999", "insertTime":1599620082000, "transferType":0, "confirmTimes":"1/1" } ]；详见官方文档

### get_subaccount_futures_margin_status(**params)
说明：Get Sub-account's Status on Margin/Futures (For Master Account) | [源码](同步 binance/client.py:6680-6709, 异步 binance/async_client.py:1630-1633) | [官方文档](https://developers.binance.com/docs/sub_account/account-management/Get-Sub-accounts-Status-on-Margin-Or-Futures)

**核心参数**:
- ☑️ **可选**: email (str) : optional - Sub account email, recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python [ { "email":"123@test.com",      // user email "isSubUserEnabled": true,    // true or false "isUserActive": true,        // true or false "insertTime": 1570791523523  // sub account create time "isMarginEnabled": true,     // true or false for margin "isFutureEnabled": true      // true or false for futures. "mobile": 1570791523523      // user mobile number } ]；详见官方文档

### enable_subaccount_margin(**params)
说明：Enable Margin for Sub-account (For Master Account) | [源码](同步 binance/client.py:6711-6738, 异步 binance/async_client.py:1635-1638) | [官方文档](-)

**核心参数**:
- ✅ **必需**: email (str) : required - Sub account email
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "email":"123@test.com", "isMarginEnabled": true }；详见官方文档

### get_subaccount_margin_details(**params)
说明：Get Detail on Sub-account's Margin Account (For Master Account) | [源码](同步 binance/client.py:6740-6807, 异步 binance/async_client.py:1640-1643) | [官方文档](https://developers.binance.com/docs/sub_account/asset-management/Get-Detail-on-Sub-accounts-Margin-Account)

**核心参数**:
- ✅ **必需**: email (str) : required - Sub account email
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "email":"123@test.com", "marginLevel": "11.64405625", "totalAssetOfBtc": "6.82728457", "totalLiabilityOfBtc": "0.58633215", "totalNetAssetOfBtc": "6.24095242", "marginTradeCoeffVo": { "forceLiquidationBar": "1.10000000",  // Liquidation margin ratio "marginCallBar": "1.50000000",        // Margin call margin ratio "normalBar": "2.00000000"             // Initial margin ratio }, "marginUserAssetVoList": [ { "asset": "BTC", "borrowed": "0.00000000", "free": "0.00499500", "interest": "0.00000000", "locked": "0.00000000", "netAsset": "0.00499500" }, { "asset": "BNB", "borrowed": "201.66666672", "free": "2346.50000000", "interest": "0.00000000", "locked": "0.00000000", "netAsset": "2144.83333328" }, { "asset": "ETH", "borrowed": "0.00000000", "free": "0.00000000", "interest": "0.00000000", "locked": "0.00000000", "netAsset": "0.00000000" }, { "asset": "USDT", "borrowed": "0.00000000", "free": "0.00000000", "interest": "0.00000000", "locked": "0.00000000", "netAsset": "0.00000000" } ] }；详见官方文档

### get_subaccount_margin_summary(**params)
说明：Get Summary of Sub-account's Margin Account (For Master Account) | [源码](同步 binance/client.py:6809-6846, 异步 binance/async_client.py:1645-1648) | [官方文档](https://developers.binance.com/docs/sub_account/asset-management/Get-Summary-of-Sub-accounts-Margin-Account)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "totalAssetOfBtc": "4.33333333", "totalLiabilityOfBtc": "2.11111112", "totalNetAssetOfBtc": "2.22222221", "subAccountList":[ { "email":"123@test.com", "totalAssetOfBtc": "2.11111111", "totalLiabilityOfBtc": "1.11111111", "totalNetAssetOfBtc": "1.00000000" }, { "email":"345@test.com", "totalAssetOfBtc": "2.22222222", "totalLiabilityOfBtc": "1.00000001", "totalNetAssetOfBtc": "1.22222221" } ] }；详见官方文档

### enable_subaccount_futures(**params)
说明：Enable Futures for Sub-account (For Master Account) | [源码](同步 binance/client.py:6848-6875, 异步 binance/async_client.py:1650-1653) | [官方文档](https://developers.binance.com/docs/sub_account/account-management/Enable-Futures-for-Sub-account)

**核心参数**:
- ✅ **必需**: email (str) : required - Sub account email
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "email":"123@test.com", "isFuturesEnabled": true  // true or false }；详见官方文档

### get_subaccount_futures_details(**params)
说明：Get Detail on Sub-account's Futures Account (For Master Account) | [源码](同步 binance/client.py:6877-6927, 异步 binance/async_client.py:1655-1658) | [官方文档](https://developers.binance.com/docs/sub_account/asset-management/Get-Detail-on-Sub-accounts-Futures-Account)

**核心参数**:
- ✅ **必需**: email (str) : required - Sub account email
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "email": "abc@test.com", "asset": "USDT", "assets":[ { "asset": "USDT", "initialMargin": "0.00000000", "maintenanceMargin": "0.00000000", "marginBalance": "0.88308000", "maxWithdrawAmount": "0.88308000", "openOrderInitialMargin": "0.00000000", "positionInitialMargin": "0.00000000", "unrealizedProfit": "0.00000000", "walletBalance": "0.88308000" } ], "canDeposit": true, "canTrade": true, "canWithdraw": true, "feeTier": 2, "maxWithdrawAmount": "0.88308000", "totalInitialMargin": "0.00000000", "totalMaintenanceMargin": "0.00000000", "totalMarginBalance": "0.88308000", "totalOpenOrderInitialMargin": "0.00000000", "totalPositionInitialMargin": "0.00000000", "totalUnrealizedProfit": "0.00000000", "totalWalletBalance": "0.88308000", "updateTime": 1576756674610 }；详见官方文档

### get_subaccount_futures_summary(**params)
说明：Get Summary of Sub-account's Futures Account (For Master Account) | [源码](同步 binance/client.py:6929-6981, 异步 binance/async_client.py:1660-1663) | [官方文档](https://developers.binance.com/docs/sub_account/asset-management/Get-Summary-of-Sub-accounts-Futures-Account-V2)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "totalInitialMargin": "9.83137400", "totalMaintenanceMargin": "0.41568700", "totalMarginBalance": "23.03235621", "totalOpenOrderInitialMargin": "9.00000000", "totalPositionInitialMargin": "0.83137400", "totalUnrealizedProfit": "0.03219710", "totalWalletBalance": "22.15879444", "asset": "USDT", "subAccountList":[ { "email": "123@test.com", "totalInitialMargin": "9.00000000", "totalMaintenanceMargin": "0.00000000", "totalMarginBalance": "22.12659734", "totalOpenOrderInitialMargin": "9.00000000", "totalPositionInitialMargin": "0.00000000", "totalUnrealizedProfit": "0.00000000", "totalWalletBalance": "22.12659734", "asset": "USDT" }, { "email": "345@test.com", "totalInitialMargin": "0.83137400", "totalMaintenanceMargin": "0.41568700", "totalMarginBalance": "0.90575887", "totalOpenOrderInitialMargin": "0.00000000", "totalPositionInitialMargin": "0.83137400", "totalUnrealizedProfit": "0.03219710", "totalWalletBalance": "0.87356177", "asset": "USDT" } ] }；详见官方文档

### get_subaccount_futures_positionrisk(**params)
说明：Get Futures Position-Risk of Sub-account (For Master Account) | [源码](同步 binance/client.py:6983-7015, 异步 binance/async_client.py:1665-1668) | [官方文档](https://developers.binance.com/docs/sub_account/account-management/Get-Futures-Position-Risk-of-Sub-account-V2)

**核心参数**:
- ✅ **必需**: email (str) : required - Sub account email
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python [ { "entryPrice": "9975.12000", "leverage": "50",              // current initial leverage "maxNotional": "1000000",      // notional value limit of current initial leverage "liquidationPrice": "7963.54", "markPrice": "9973.50770517", "positionAmount": "0.010", "symbol": "BTCUSDT", "unrealizedProfit": "-0.01612295" } ]；详见官方文档

### make_subaccount_futures_transfer(**params)
说明：Futures Transfer for Sub-account (For Master Account) | [源码](同步 binance/client.py:7017-7047, 异步 binance/async_client.py:1670-1673) | [官方文档](https://developers.binance.com/docs/sub_account/asset-management)

**核心参数**:
- ✅ **必需**: email (str) : required - Sub account email, asset (str) : required - The asset being transferred, e.g., USDT, amount (float) : required - The amount to be transferred, type (int) : required - 1: transfer from subaccount's spot account to its USDT-margined futures account

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "txnId":"2966662589" }；详见官方文档

### make_subaccount_margin_transfer(**params)
说明：Margin Transfer for Sub-account (For Master Account) | [源码](同步 binance/client.py:7049-7077, 异步 binance/async_client.py:1675-1678) | [官方文档](https://developers.binance.com/docs/sub_account/asset-management/Margin-Transfer-for-Sub-account)

**核心参数**:
- ✅ **必需**: email (str) : required - Sub account email, asset (str) : required - The asset being transferred, e.g., USDT, amount (float) : required - The amount to be transferred, type (int) : required - 1: transfer from subaccount's spot account to margin account

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "txnId":"2966662589" }；详见官方文档

### make_subaccount_to_subaccount_transfer(**params)
说明：Transfer to Sub-account of Same Master (For Sub-account) | [源码](同步 binance/client.py:7079-7106, 异步 binance/async_client.py:1680-1683) | [官方文档](https://developers.binance.com/docs/sub_account/asset-management/Transfer-to-Sub-account-of-Same-Master)

**核心参数**:
- ✅ **必需**: toEmail (str) : required - Sub account email, asset (str) : required - The asset being transferred, e.g., USDT, amount (float) : required - The amount to be transferred
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "txnId":"2966662589" }；详见官方文档

### make_subaccount_to_master_transfer(**params)
说明：Transfer to Master (For Sub-account) | [源码](同步 binance/client.py:7108-7133, 异步 binance/async_client.py:1685-1688) | [官方文档](https://developers.binance.com/docs/sub_account/asset-management/Transfer-to-Master)

**核心参数**:
- ✅ **必需**: asset (str) : required - The asset being transferred, e.g., USDT, amount (float) : required - The amount to be transferred
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "txnId":"2966662589" }；详见官方文档

### get_subaccount_transfer_history(**params)
说明：Sub-account Transfer History (For Sub-account) | [源码](同步 binance/client.py:7135-7185, 异步 binance/async_client.py:1690-1693) | [官方文档](https://developers.binance.com/docs/sub_account/asset-management/Sub-account-Transfer-History)

**核心参数**:
- ✅ **必需**: asset (str) : required - The asset being transferred, e.g., USDT
- ☑️ **可选**: type (int) : optional - 1: transfer in, 2: transfer out, startTime (int) : optional, endTime (int) : optional, limit (int) : optional - Default 500, recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python [ { "counterParty":"master", "email":"master@test.com", "type":1,  // 1 for transfer in, 2 for transfer out "asset":"BTC", "qty":"1", "status":"SUCCESS", "tranId":11798835829, "time":1544433325000 }, { "counterParty":"subAccount", "email":"sub2@test.com", "type":2, "asset":"ETH", "qty":"2", "status":"SUCCESS", "tranId":11798829519, "time":1544433326000 } ]；详见官方文档

### make_subaccount_universal_transfer(**params)
说明：Universal Transfer (For Master Account) | [源码](同步 binance/client.py:7187-7220, 异步 binance/async_client.py:1695-1698) | [官方文档](https://developers.binance.com/docs/sub_account/asset-management/Universal-Transfer)

**核心参数**:
- ✅ **必需**: fromAccountType (str) : required - "SPOT","USDT_FUTURE","COIN_FUTURE", toAccountType (str) : required - "SPOT","USDT_FUTURE","COIN_FUTURE", asset (str) : required - The asset being transferred, e.g., USDT, amount (float) : required
- ☑️ **可选**: fromEmail (str) : optional, toEmail (str) : optional, recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "tranId":11945860693 }；详见官方文档

### get_universal_transfer_history(**params)
说明：Universal Transfer (For Master Account) | [源码](同步 binance/client.py:7222-7276, 异步 binance/async_client.py:1700-1703) | [官方文档](https://developers.binance.com/docs/sub_account/asset-management/Query-Universal-Transfer-History)

**核心参数**:
- ☑️ **可选**: fromEmail (str) : optional, toEmail (str) : optional, startTime (int) : optional, endTime (int) : optional, page (int) : optional, limit (int) : optional, recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python [ { "tranId":11945860693, "fromEmail":"master@test.com", "toEmail":"subaccount1@test.com", "asset":"BTC", "amount":"0.1", "fromAccountType":"SPOT", "toAccountType":"COIN_FUTURE", "status":"SUCCESS", "createTimeStamp":1544433325000 }, { "tranId":11945857955, "fromEmail":"master@test.com", "toEmail":"subaccount2@test.com", "asset":"ETH", "amount":"0.2", "fromAccountType":"SPOT", "toAccountType":"USDT_FUTURE", "status":"SUCCESS", "createTimeStamp":1544433326000 } ]；详见官方文档

### transfer_history(**params)
说明：Get future account transaction history list | [源码](同步 binance/client.py:7736-7742, 异步 binance/async_client.py:1855-1858) | [官方文档](-)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### new_transfer_history(**params)
说明：Get future account transaction history list | [源码](同步 binance/client.py:8330-8336, 异步 binance/async_client.py:2207-2210) | [官方文档](https://developers.binance.com/docs/wallet/asset/query-user-universal-transfer)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### funding_wallet(**params)
说明：Query Funding Wallet | [源码](同步 binance/client.py:8338-8346, 异步 binance/async_client.py:2212-2215) | [官方文档](https://developers.binance.com/docs/wallet/asset/funding-wallet)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### get_user_asset(**params)
说明：Get user assets, just for positive data | [源码](同步 binance/client.py:8348-8356, 异步 binance/async_client.py:2217-2220) | [官方文档](https://developers.binance.com/docs/wallet/asset/user-assets)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### universal_transfer(**params)
说明：Unviversal transfer api accross different binance account types | [源码](同步 binance/client.py:8358-8365, 异步 binance/async_client.py:2222-2225) | [官方文档](https://developers.binance.com/docs/wallet/asset/user-universal-transfer)

**核心参数**:
- （源码未提供参数说明）

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### get_all_coins_info(**params)
说明：Get information of coins (available for deposit and withdraw) for user. | [源码](同步 binance/client.py:8762-8837, 异步 binance/async_client.py:2387-2390) | [官方文档](https://developers.binance.com/docs/wallet/capital)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "coin": "BTC", "depositAllEnable": true, "withdrawAllEnable": true, "name": "Bitcoin", "free": "0", "locked": "0", "freeze": "0", "withdrawing": "0", "ipoing": "0", "ipoable": "0", "storage": "0", "isLegalMoney": false, "trading": true, "networkList": [ { "network": "BNB", "coin": "BTC", "withdrawIntegerMultiple": "0.00000001", "isDefault": false, "depositEnable": true, "withdrawEnable": true, "depositDesc": "", "withdrawDesc": "", "specialTips": "Both a MEMO and an Address are required to successfully deposit your BEP2-BTCB tokens to Binance.", "name": "BEP2", "resetAddressStatus": false, "addressRegex": "^(bnb1)[0-9a-z]{38}$", "memoRegex": "^[0-9A-Za-z-_]{1,120}$", "withdrawFee": "0.0000026", "withdrawMin": "0.0000052", "withdrawMax": "0", "minConfirm": 1, "unLockConfirm": 0 }, { "network": "BTC", "coin": "BTC", "withdrawIntegerMultiple": "0.00000001", "isDefault": true, "depositEnable": true, "withdrawEnable": true, "depositDesc": "", "withdrawDesc": "", "specialTips": "", "name": "BTC", "resetAddressStatus": false, "addressRegex": "^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$|^(bc1)[0-9A-Za-z]{39,59}$", "memoRegex": "", "withdrawFee": "0.0005", "withdrawMin": "0.001", "withdrawMax": "0", "minConfirm": 1, "unLockConfirm": 2 } ] }；详见官方文档

### get_account_snapshot(**params)
说明：Get daily account snapshot of specific type. | [源码](同步 binance/client.py:8839-8952, 异步 binance/async_client.py:2392-2395) | [官方文档](https://developers.binance.com/docs/wallet/account/daily-account-snapshoot)

**核心参数**:
- ✅ **必需**: type (string) : required. Valid values are SPOT/MARGIN/FUTURES.
- ☑️ **可选**: startTime (int) : optional, endTime (int) : optional, limit (int) : optional, recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "code":200, // 200 for success; others are error codes "msg":"", // error message "snapshotVos":[ { "data":{ "balances":[ { "asset":"BTC", "free":"0.09905021", "locked":"0.00000000" }, { "asset":"USDT", "free":"1.89109409", "locked":"0.00000000" } ], "totalAssetOfBtc":"0.09942700" }, "type":"spot", "updateTime":1576281599000 } ] } OR .. code-block:: python { "code":200, // 200 for success; others are error codes "msg":"", // error message "snapshotVos":[ { "data":{ "marginLevel":"2748.02909813", "totalAssetOfBtc":"0.00274803", "totalLiabilityOfBtc":"0.00000100", "totalNetAssetOfBtc":"0.00274750", "userAssets":[ { "asset":"XRP", "borrowed":"0.00000000", "free":"1.00000000", "interest":"0.00000000", "locked":"0.00000000", "netAsset":"1.00000000" } ] }, "type":"margin", "updateTime":1576281599000 } ] } OR .. code-block:: python { "code":200, // 200 for success; others are error codes "msg":"", // error message "snapshotVos":[ { "data":{ "assets":[ { "asset":"USDT", "marginBalance":"118.99782335", "walletBalance":"120.23811389" } ], "position":[ { "entryPrice":"7130.41000000", "markPrice":"7257.66239673", "positionAmt":"0.01000000", "symbol":"BTCUSDT", "unRealizedProfit":"1.24029054" } ] }, "type":"futures", "updateTime":1576281599000 } ] }；详见官方文档

### disable_fast_withdraw_switch(**params)
说明：Disable Fast Withdraw Switch | [源码](同步 binance/client.py:8954-8969, 异步 binance/async_client.py:2397-2400) | [官方文档](-)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### enable_fast_withdraw_switch(**params)
说明：Enable Fast Withdraw Switch | [源码](同步 binance/client.py:8971-8986, 异步 binance/async_client.py:2402-2405) | [官方文档](-)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### get_fiat_deposit_withdraw_history(**params)
说明：Get Fiat Deposit/Withdraw History | [源码](同步 binance/client.py:9692-9711, 异步 binance/async_client.py:2518-2521) | [官方文档](-)

**核心参数**:
- ✅ **必需**: transactionType (str) : required - 0-deposit,1-withdraw
- ☑️ **可选**: beginTime (int) : optional, endTime (int) : optional, page (int) : optional - default 1, rows (int) : optional - default 100, max 500, recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### get_fiat_payments_history(**params)
说明：Get Fiat Payments History | [源码](同步 binance/client.py:9713-9734, 异步 binance/async_client.py:2523-2526) | [官方文档](-)

**核心参数**:
- ✅ **必需**: transactionType (str) : required - 0-buy,1-sell
- ☑️ **可选**: beginTime (int) : optional, endTime (int) : optional, page (int) : optional - default 1, rows (int) : optional - default 100, max 500, recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### get_c2c_trade_history(**params)
说明：Get C2C Trade History | [源码](同步 binance/client.py:9738-9786, 异步 binance/async_client.py:2530-2533) | [官方文档](-)

**核心参数**:
- ✅ **必需**: tradeType (str) : required - BUY, SELL
- ☑️ **可选**: startTimestamp : optional, endTimestamp (int) : optional, page (int) : optional - default 1, rows (int) : optional - default 100, max 100, recvWindow (int) : optional
- ℹ️ **未标注**: startTime (int)

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response { "code": "000000", "message": "success", "data": [ { "orderNumber":"20219644646554779648", "advNo": "11218246497340923904", "tradeType": "SELL", "asset": "BUSD", "fiat": "CNY", "fiatSymbol": "￥", "amount": "5000.00000000",  // Quantity (in Crypto) "totalPrice": "33400.00000000", "unitPrice": "6.68", // Unit Price (in Fiat) "orderStatus": "COMPLETED",  // PENDING, TRADING, BUYER_PAYED, DISTRIBUTING, COMPLETED, IN_APPEAL, CANCELLED, CANCELLED_BY_SYSTEM "createTime": 1619361369000, "commission": "0",   // Transaction Fee (in Crypto) "counterPartNickName": "ab***", "advertisementRole": "TAKER" } ], "total": 1, "success": true }；详见官方文档

### get_pay_trade_history(**params)
说明：Get C2C Trade History | [源码](同步 binance/client.py:9790-9809, 异步 binance/async_client.py:2537-2540) | [官方文档](-)

**核心参数**:
- ☑️ **可选**: startTime (int) : optional, endTime (int) : optional, limit (int) : optional - default 100, max 100, recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### get_convert_trade_history(**params)
说明：Get C2C Trade History | [源码](同步 binance/client.py:9813-9832, 异步 binance/async_client.py:2546-2549) | [官方文档](https://developers.binance.com/docs/convert/trade/Get-Convert-Trade-History)

**核心参数**:
- ✅ **必需**: startTime (int) : required - Start Time - 1593511200000, endTime (int) : required - End Time - 1593511200000
- ☑️ **可选**: limit (int) : optional - default 100, max 100, recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### convert_request_quote(**params)
说明：Request a quote for the requested token pairs | [源码](同步 binance/client.py:9834-9856, 异步 binance/async_client.py:2553-2556) | [官方文档](https://developers.binance.com/docs/convert/trade)

**核心参数**:
- ✅ **必需**: fromAsset (str) : required - Asset to convert from - BUSD, toAsset (str) : required - Asset to convert to - BTC
- ☑️ **可选**: recvWindow (int) : optional
- ℹ️ **未标注**: fromAmount (decimal) : EITHER - When specified, it is the amount you will be debited after the conversion, toAmount (decimal) : EITHER - When specified, it is the amount you will be credited after the conversion

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### convert_accept_quote(**params)
说明：Accept the offered quote by quote ID. | [源码](同步 binance/client.py:9858-9874, 异步 binance/async_client.py:2560-2563) | [官方文档](https://developers.binance.com/docs/convert/trade/Accept-Quote)

**核心参数**:
- ✅ **必需**: quoteId (str) : required - 457235734584567
- ☑️ **可选**: recvWindow (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### gift_card_fetch_token_limit(**params)
说明：Verify which tokens are available for you to create Stablecoin-Denominated gift cards | [源码](同步 binance/client.py:13648-13671, 异步 binance/async_client.py:3980-3983) | [官方文档](https://developers.binance.com/docs/gift_card/market-data/Fetch-Token-Limit)

**核心参数**:
- ℹ️ **未标注**: baseToken (str) : The token you want to pay, example: BUSD

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### gift_card_fetch_rsa_public_key(**params)
说明：This API is for fetching the RSA Public Key. This RSA Public key will be used to encrypt the card code. | [源码](同步 binance/client.py:13673-13693, 异步 binance/async_client.py:3987-3990) | [官方文档](https://developers.binance.com/docs/gift_card/market-data/Fetch-RSA-Public-Key)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : The receive window for the request in milliseconds (optional)

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### gift_card_verify(**params)
说明：This API is for verifying whether the Binance Gift Card is valid or not by entering Gift Card Number. | [源码](同步 binance/client.py:13695-13721, 异步 binance/async_client.py:3996-3999) | [官方文档](https://developers.binance.com/docs/gift_card/market-data/Verify-Binance-Gift-Card-by-Gift-Card-Number)

**核心参数**:
- ℹ️ **未标注**: referenceNo (str) : Enter the Gift Card Number

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### gift_card_redeem(**params)
说明：This API is for redeeming a Binance Gift Card. Once redeemed, the coins will be deposited in your funding wallet. | [源码](同步 binance/client.py:13723-13763, 异步 binance/async_client.py:4003-4006) | [官方文档](https://developers.binance.com/docs/gift_card/market-data/Redeem-a-Binance-Gift-Card)

**核心参数**:
- ☑️ **可选**: recvWindow (int) : The receive window for the request in milliseconds (optional)
- ℹ️ **未标注**: code (str) : Redemption code of Binance Gift Card to be redeemed, supports both Plaintext & Encrypted code, externalUid (str) : External unique ID representing a user on the partner platform.

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### gift_card_create(**params)
说明：This API is for creating a Binance Gift Card. | [源码](同步 binance/client.py:13765-13797, 异步 binance/async_client.py:4010-4013) | [官方文档](https://developers.binance.com/docs/gift_card/market-data)

**核心参数**:
- ℹ️ **未标注**: token (str) : The token type contained in the Binance Gift Card, amount (float) : The amount of the token contained in the Binance Gift Card

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### gift_card_create_dual_token(**params)
说明：This API is for creating a dual-token ( stablecoin-denominated) Binance Gift Card. You may create a gift card using USDT as baseToken, that is redeemable to another designated token (faceToken). For example, you can create a fixed-value BTC gift card and pay with 100 USDT plus 1 USDT fee. This gift card can keep the value fixed at 100 USDT before redemption, and will be redeemable to BTC equivalent to 100 USDT upon redemption. | [源码](同步 binance/client.py:13799-13832, 异步 binance/async_client.py:4017-4020) | [官方文档](https://developers.binance.com/docs/gift_card/market-data/Create-a-dual-token-gift-card)

**核心参数**:
- ℹ️ **未标注**: baseToken (str) : The token you want to pay, example: BUSD, faceToken (str) : The token you want to buy, example: BNB. If faceToken = baseToken, it's the same as createCode endpoint., discount (float) : Stablecoin-denominated card discount percentage, Example: 1 for 1% discount. Scale should be less than 6.

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_next_hourly_interest_rate(**params)
说明：Get future hourly interest rate (USER_DATA) | [源码](同步 binance/client.py:13838-13864, 异步 binance/async_client.py:4089-4092) | [官方文档](https://developers.binance.com/docs/margin_trading/borrow-and-repay)

**核心参数**:
- ✅ **必需**: assets (str) : required - List of assets, separated by commas, up to 20, isIsolated (bool) : required - for isolated margin or not, "TRUE", "FALSE"

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python [ { "asset": "BTC", "nextHourlyInterestRate": "0.00000571" }, { "asset": "ETH", "nextHourlyInterestRate": "0.00000578" } ]；详见官方文档

### margin_interest_history(**params)
说明：Get Interest History (USER_DATA) | [源码](同步 binance/client.py:13866-13907, 异步 binance/async_client.py:4098-4101) | [官方文档](https://developers.binance.com/docs/margin_trading/borrow-and-repay/Get-Interest-History)

**核心参数**:
- ☑️ **可选**: asset (str) : optional, isolatedSymbol (str) : optional - isolated symbol, startTime (int) : optional, endTime (int) : optional, current (int) : optional - Currently querying page. Start from 1. Default:1, size (int) : optional - Default:10 Max:100

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "rows": [ { "txId": 1352286576452864727, "interestAccuredTime": 1672160400000, "asset": "USDT", "rawAsset": “USDT”,  // will not be returned for isolated margin "principal": "45.3313", "interest": "0.00024995", "interestRate": "0.00013233", "type": "ON_BORROW", "isolatedSymbol": "BNBUSDT"  // isolated symbol, will not be returned for crossed margin } ], "total": 1 }；详见官方文档

### margin_borrow_repay(**params)
说明：Margin Account Borrow/Repay (MARGIN) | [源码](同步 binance/client.py:13909-13935, 异步 binance/async_client.py:4105-4108) | [官方文档](https://developers.binance.com/docs/margin_trading/borrow-and-repay/Margin-Account-Borrow-Repay)

**核心参数**:
- ✅ **必需**: asset (str) : required, amount (float) : required
- ☑️ **可选**: isIsolated (str) : optional - for isolated margin or not, "TRUE", "FALSE", default "FALSE", symbol (str) : optional - isolated symbol
- ℹ️ **未标注**: type (str - BORROW or REPAY) : str

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { //transaction id "tranId": 100000001 }；详见官方文档

### margin_get_borrow_repay_records(**params)
说明：Query Query borrow/repay records in Margin account (USER_DATA) | [源码](同步 binance/client.py:13937-13980, 异步 binance/async_client.py:4112-4115) | [官方文档](https://developers.binance.com/docs/margin_trading/borrow-and-repay/Query-Borrow-Repay)

**核心参数**:
- ✅ **必需**: asset (str) : required
- ☑️ **可选**: isolatedSymbol (str) : optional - isolated symbol, txId (int) : optional - the tranId in POST /sapi/v1/margin/loan, startTime (int) : optional, endTime (int) : optional, current (int) : optional - Currently querying page. Start from 1. Default:1, size (int) : optional - Default:10 Max:100

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "rows": [ { "type": "AUTO", // AUTO,MANUAL for Cross Margin Borrow; MANUAL，AUTO，BNB_AUTO_REPAY，POINT_AUTO_REPAY for Cross Margin Repay; AUTO，MANUAL for Isolated Margin Borrow/Repay; "isolatedSymbol": "BNBUSDT",     // isolated symbol, will not be returned for crossed margin "amount": "14.00000000",   // Total amount borrowed/repaid "asset": "BNB", "interest": "0.01866667",    // Interest repaid "principal": "13.98133333",   // Principal repaid "status": "CONFIRMED",   //one of PENDING (pending execution), CONFIRMED (successfully execution), FAILED (execution failed, nothing happened to your account); "timestamp": 1563438204000, "txId": 2970933056 } ], "total": 1 }；详见官方文档

### margin_interest_rate_history(**params)
说明：Query Margin Interest Rate History (USER_DATA) | [源码](同步 binance/client.py:13982-14017, 异步 binance/async_client.py:4121-4124) | [官方文档](https://developers.binance.com/docs/margin_trading/borrow-and-repay/Query-Margin-Interest-Rate-History)

**核心参数**:
- ✅ **必需**: asset (str) : required
- ☑️ **可选**: vipLevel (int) : optional, startTime (int) : optional, endTime (int) : optional

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python [ { "asset": "BTC", "dailyInterestRate": "0.00025000", "timestamp": 1611544731000, "vipLevel": 1 }, { "asset": "BTC", "dailyInterestRate": "0.00035000", "timestamp": 1610248118000, "vipLevel": 1 } ]；详见官方文档

### margin_max_borrowable(**params)
说明：Query Max Borrow (USER_DATA) | [源码](同步 binance/client.py:14019-14041, 异步 binance/async_client.py:4128-4131) | [官方文档](https://developers.binance.com/docs/margin_trading/borrow-and-repay/Query-Max-Borrow)

**核心参数**:
- ✅ **必需**: asset (str) : required
- ☑️ **可选**: isolatedSymbol (str) : optional - isolated symbol

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response .. code-block:: python { "amount": "1.69248805", // account's currently max borrowable amount with sufficient system availability "borrowLimit": "60" // max borrowable amount limited by the account level }；详见官方文档

### margin_v1_get_loan_vip_ongoing_orders(**params)
说明：Placeholder function for GET /sapi/v1/loan/vip/ongoing/orders. | [源码](同步 binance/client.py:14090-14102, 异步 binance/async_client.py:4144-4145) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_mining_payment_other(**params)
说明：Placeholder function for GET /sapi/v1/mining/payment/other. | [源码](同步 binance/client.py:14104-14116, 异步 binance/async_client.py:4149-4150) | [官方文档](https://developers.binance.com/docs/mining/rest-api/Extra-Bonus-List)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_simple_earn_flexible_history_subscription_record(**params)
说明：Placeholder function for GET /sapi/v1/simple-earn/flexible/history/subscriptionRecord. | [源码](同步 binance/client.py:14132-14144, 异步 binance/async_client.py:4159-4160) | [官方文档](https://developers.binance.com/docs/simple_earn/history)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_lending_auto_invest_one_off(**params)
说明：Placeholder function for POST /sapi/v1/lending/auto-invest/one-off. | [源码](同步 binance/client.py:14146-14156, 异步 binance/async_client.py:4164-4165) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_broker_sub_account_api_commission_coin_futures(**params)
说明：Placeholder function for POST /sapi/v1/broker/subAccountApi/commission/coinFutures. | [源码](同步 binance/client.py:14158-14170, 异步 binance/async_client.py:4169-4170) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/fee/Change-Sub-Account-CM-Futures-Commission)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_asset_custody_transfer_history(**params)
说明：Placeholder function for GET /sapi/v1/asset/custody/transfer-history. | [源码](同步 binance/client.py:14198-14210, 异步 binance/async_client.py:4184-4185) | [官方文档](https://developers.binance.com/docs/wallet/asset/query-user-delegation)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_broker_sub_account_blvt(**params)
说明：Placeholder function for POST /sapi/v1/broker/subAccount/blvt. | [源码](同步 binance/client.py:14212-14222, 异步 binance/async_client.py:4189-4190) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_sol_staking_sol_redeem(**params)
说明：Placeholder function for POST /sapi/v1/sol-staking/sol/redeem. | [源码](同步 binance/client.py:14224-14236, 异步 binance/async_client.py:4194-4195) | [官方文档](https://developers.binance.com/docs/staking/sol-staking/staking/Redeem-SOL)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_margin_trade_coeff(**params)
说明：Placeholder function for GET /sapi/v1/margin/tradeCoeff. | [源码](同步 binance/client.py:14252-14264, 异步 binance/async_client.py:4204-4205) | [官方文档](https://developers.binance.com/docs/margin_trading/account/Get-Summary-Of-Margin-Account)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_margin_available_inventory(**params)
说明：Placeholder function for GET /sapi/v1/margin/available-inventory. | [源码](同步 binance/client.py:14280-14292, 异步 binance/async_client.py:4214-4215) | [官方文档](https://developers.binance.com/docs/margin_trading/market-data/Query-margin-avaliable-inventory)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_account_api_restrictions_ip_restriction_ip_list(**params)
说明：Placeholder function for POST /sapi/v1/account/apiRestrictions/ipRestriction/ipList. | [源码](同步 binance/client.py:14294-14304, 异步 binance/async_client.py:4219-4220) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v2_get_eth_staking_account(**params)
说明：Placeholder function for GET /sapi/v2/eth-staking/account. | [源码](同步 binance/client.py:14306-14318, 异步 binance/async_client.py:4224-4225) | [官方文档](https://developers.binance.com/docs/staking/eth-staking/account)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_loan_income(**params)
说明：Placeholder function for GET /sapi/v1/loan/income. | [源码](同步 binance/client.py:14320-14332, 异步 binance/async_client.py:4229-4230) | [官方文档](https://developers.binance.com/docs/crypto_loan/stable-rate/market-data)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_managed_subaccount_query_trans_log_for_investor(**params)
说明：Placeholder function for GET /sapi/v1/managed-subaccount/queryTransLogForInvestor. | [源码](同步 binance/client.py:14348-14360, 异步 binance/async_client.py:4239-4240) | [官方文档](https://developers.binance.com/docs/sub_account/managed-sub-account/Query-Managed-Sub-Account-Transfer-Log-Investor)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_dci_product_auto_compound_edit_status(**params)
说明：Placeholder function for POST /sapi/v1/dci/product/auto_compound/edit-status. | [源码](同步 binance/client.py:14362-14374, 异步 binance/async_client.py:4244-4245) | [官方文档](https://developers.binance.com/docs/dual_investment/trade/Change-Auto-Compound-status)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_loan_vip_request_interest_rate(**params)
说明：Placeholder function for GET /sapi/v1/loan/vip/request/interestRate. | [源码](同步 binance/client.py:14390-14402, 异步 binance/async_client.py:4254-4255) | [官方文档](https://developers.binance.com/docs/vip_loan/market-data)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v2_get_loan_flexible_repay_rate(**params)
说明：Placeholder function for GET /sapi/v2/loan/flexible/repay/rate. | [源码](同步 binance/client.py:14418-14430, 异步 binance/async_client.py:4267-4268) | [官方文档](https://developers.binance.com/docs/crypto_loan/flexible-rate/user-information/Check-Collateral-Repay-Rate)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_lending_auto_invest_plan_id(**params)
说明：Placeholder function for GET /sapi/v1/lending/auto-invest/plan/id. | [源码](同步 binance/client.py:14432-14442, 异步 binance/async_client.py:4272-4273) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_loan_adjust_ltv(**params)
说明：Placeholder function for POST /sapi/v1/loan/adjust/ltv. | [源码](同步 binance/client.py:14444-14454, 异步 binance/async_client.py:4277-4278) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_mining_statistics_user_status(**params)
说明：Placeholder function for GET /sapi/v1/mining/statistics/user/status. | [源码](同步 binance/client.py:14456-14468, 异步 binance/async_client.py:4282-4283) | [官方文档](https://developers.binance.com/docs/mining/rest-api/Statistic-List)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_broker_transfer_futures(**params)
说明：Placeholder function for GET /sapi/v1/broker/transfer/futures. | [源码](同步 binance/client.py:14470-14482, 异步 binance/async_client.py:4287-4288) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/asset/Query-Sub-Account-Transfer-History-Futures)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_algo_spot_new_order_twap(**params)
说明：Placeholder function for POST /sapi/v1/algo/spot/newOrderTwap. | [源码](同步 binance/client.py:14484-14496, 异步 binance/async_client.py:4292-4293) | [官方文档](https://developers.binance.com/docs/algo/spot-algo/Time-Weighted-Average-Price-New-Order)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_lending_auto_invest_target_asset_list(**params)
说明：Placeholder function for GET /sapi/v1/lending/auto-invest/target-asset/list. | [源码](同步 binance/client.py:14498-14508, 异步 binance/async_client.py:4297-4298) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_capital_deposit_address_list(**params)
说明：Placeholder function for GET /sapi/v1/capital/deposit/address/list. | [源码](同步 binance/client.py:14510-14522, 异步 binance/async_client.py:4302-4303) | [官方文档](https://developers.binance.com/docs/wallet/capital/deposite-address)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_broker_sub_account_bnb_burn_margin_interest(**params)
说明：Placeholder function for POST /sapi/v1/broker/subAccount/bnbBurn/marginInterest. | [源码](同步 binance/client.py:14524-14536, 异步 binance/async_client.py:4307-4308) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/account/Enable-Or-Disable-BNB-Burn-for-Sub-Account-Margin-Interest)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v2_post_loan_flexible_repay(**params)
说明：Placeholder function for POST /sapi/v2/loan/flexible/repay. | [源码](同步 binance/client.py:14538-14550, 异步 binance/async_client.py:4312-4313) | [官方文档](https://developers.binance.com/docs/crypto_loan/flexible-rate/trade/Flexible-Loan-Repay)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v2_get_loan_flexible_loanable_data(**params)
说明：Placeholder function for GET /sapi/v2/loan/flexible/loanable/data. | [源码](同步 binance/client.py:14552-14564, 异步 binance/async_client.py:4317-4318) | [官方文档](https://developers.binance.com/docs/crypto_loan/flexible-rate/market-data/Get-Flexible-Loan-Assets-Data)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_broker_sub_account_api_permission(**params)
说明：Placeholder function for POST /sapi/v1/broker/subAccountApi/permission. | [源码](同步 binance/client.py:14566-14578, 异步 binance/async_client.py:4322-4323) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/account/Change-Sub-Account-Api-Permission)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_broker_sub_account_api(**params)
说明：Placeholder function for POST /sapi/v1/broker/subAccountApi. | [源码](同步 binance/client.py:14580-14592, 异步 binance/async_client.py:4327-4328) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/account/Create-Api-Key-for-Sub-Account)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_dci_product_positions(**params)
说明：Placeholder function for GET /sapi/v1/dci/product/positions. | [源码](同步 binance/client.py:14594-14606, 异步 binance/async_client.py:4332-4333) | [官方文档](https://developers.binance.com/docs/dual_investment/trade/Get-Dual-Investment-positions)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_convert_limit_cancel_order(**params)
说明：Placeholder function for POST /sapi/v1/convert/limit/cancelOrder. | [源码](同步 binance/client.py:14608-14620, 异步 binance/async_client.py:4337-4338) | [官方文档](https://developers.binance.com/docs/convert/trade/Cancel-Order)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_mining_hash_transfer_config_details_list(**params)
说明：Placeholder function for GET /sapi/v1/mining/hash-transfer/config/details/list. | [源码](同步 binance/client.py:14634-14646, 异步 binance/async_client.py:4347-4348) | [官方文档](https://developers.binance.com/docs/mining/rest-api/Hashrate-Resale-List)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_mining_hash_transfer_profit_details(**params)
说明：Placeholder function for GET /sapi/v1/mining/hash-transfer/profit/details. | [源码](同步 binance/client.py:14648-14660, 异步 binance/async_client.py:4352-4353) | [官方文档](https://developers.binance.com/docs/mining/rest-api/Hashrate-Resale-Detail)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_broker_sub_account(**params)
说明：Placeholder function for GET /sapi/v1/broker/subAccount. | [源码](同步 binance/client.py:14662-14674, 异步 binance/async_client.py:4357-4358) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/account/Query-Sub-Account)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_portfolio_balance(**params)
说明：Placeholder function for GET /sapi/v1/portfolio/balance. | [源码](同步 binance/client.py:14676-14688, 异步 binance/async_client.py:4362-4363) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin-pro/account/Get-Classic-Portfolio-Margin-Balance-Info)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_sub_account_eoptions_enable(**params)
说明：Placeholder function for POST /sapi/v1/sub-account/eoptions/enable. | [源码](同步 binance/client.py:14690-14702, 异步 binance/async_client.py:4367-4368) | [官方文档](https://developers.binance.com/docs/sub_account/account-management/Enable-Options-for-Sub-account)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_loan_loanable_data(**params)
说明：Placeholder function for GET /sapi/v1/loan/loanable/data. | [源码](同步 binance/client.py:14716-14726, 异步 binance/async_client.py:4377-4378) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_eth_staking_wbeth_unwrap(**params)
说明：Placeholder function for POST /sapi/v1/eth-staking/wbeth/unwrap. | [源码](同步 binance/client.py:14728-14738, 异步 binance/async_client.py:4382-4383) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_eth_staking_eth_history_staking_history(**params)
说明：Placeholder function for GET /sapi/v1/eth-staking/eth/history/stakingHistory. | [源码](同步 binance/client.py:14740-14752, 异步 binance/async_client.py:4387-4388) | [官方文档](https://developers.binance.com/docs/staking/eth-staking/history)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_staking_staking_record(**params)
说明：Placeholder function for GET /sapi/v1/staking/stakingRecord. | [源码](同步 binance/client.py:14754-14764, 异步 binance/async_client.py:4392-4393) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_broker_rebate_recent_record(**params)
说明：Placeholder function for GET /sapi/v1/broker/rebate/recentRecord. | [源码](同步 binance/client.py:14766-14778, 异步 binance/async_client.py:4397-4398) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/fee/Query-Spot-Commission-Rebate-Recent-Record)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_loan_vip_collateral_account(**params)
说明：Placeholder function for GET /sapi/v1/loan/vip/collateral/account. | [源码](同步 binance/client.py:14780-14792, 异步 binance/async_client.py:4408-4409) | [官方文档](https://developers.binance.com/docs/vip_loan/user-information/Check-Locked-Value-of-VIP-Collateral-Account)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_algo_spot_open_orders(**params)
说明：Placeholder function for GET /sapi/v1/algo/spot/openOrders. | [源码](同步 binance/client.py:14794-14806, 异步 binance/async_client.py:4413-4414) | [官方文档](https://developers.binance.com/docs/algo/spot-algo/Query-Current-Algo-Open-Orders)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_loan_repay(**params)
说明：Placeholder function for POST /sapi/v1/loan/repay. | [源码](同步 binance/client.py:14808-14818, 异步 binance/async_client.py:4418-4419) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_margin_leverage_bracket(**params)
说明：Placeholder function for GET /sapi/v1/margin/leverageBracket. | [源码](同步 binance/client.py:14834-14846, 异步 binance/async_client.py:4428-4429) | [官方文档](https://developers.binance.com/docs/margin_trading/market-data/Query-Liability-Coin-Leverage-Bracket-in-Cross-Margin-Pro-Mode)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v2_get_portfolio_collateral_rate(**params)
说明：Placeholder function for GET /sapi/v2/portfolio/collateralRate. | [源码](同步 binance/client.py:14848-14860, 异步 binance/async_client.py:4433-4434) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin-pro/market-data/Portfolio-Margin-Pro-Tiered-Collateral-Rate)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v2_post_loan_flexible_adjust_ltv(**params)
说明：Placeholder function for POST /sapi/v2/loan/flexible/adjust/ltv. | [源码](同步 binance/client.py:14862-14874, 异步 binance/async_client.py:4438-4439) | [官方文档](https://developers.binance.com/docs/crypto_loan/flexible-rate/trade/Flexible-Loan-Adjust-LTV)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_convert_order_status(**params)
说明：Placeholder function for GET /sapi/v1/convert/orderStatus. | [源码](同步 binance/client.py:14876-14888, 异步 binance/async_client.py:4443-4444) | [官方文档](https://developers.binance.com/docs/convert/trade/Order-Status)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_broker_sub_account_api_ip_restriction(**params)
说明：Placeholder function for GET /sapi/v1/broker/subAccountApi/ipRestriction. | [源码](同步 binance/client.py:14890-14902, 异步 binance/async_client.py:4448-4449) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/account/Get-IPRestriction-for-Sub-Account-Api-Key)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_dci_product_subscribe(**params)
说明：Placeholder function for POST /sapi/v1/dci/product/subscribe. | [源码](同步 binance/client.py:14904-14916, 异步 binance/async_client.py:4453-4454) | [官方文档](https://developers.binance.com/docs/dual_investment/trade)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_mining_hash_transfer_config_cancel(**params)
说明：Placeholder function for POST /sapi/v1/mining/hash-transfer/config/cancel. | [源码](同步 binance/client.py:14946-14958, 异步 binance/async_client.py:4468-4469) | [官方文档](https://developers.binance.com/docs/mining/rest-api/Cancel-hashrate-resale-configuration)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_broker_sub_account_deposit_hist(**params)
说明：Placeholder function for GET /sapi/v1/broker/subAccount/depositHist. | [源码](同步 binance/client.py:14960-14972, 异步 binance/async_client.py:4473-4474) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/asset/Get-Sub-Account-Deposit-History)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_mining_payment_list(**params)
说明：Placeholder function for GET /sapi/v1/mining/payment/list. | [源码](同步 binance/client.py:14974-14986, 异步 binance/async_client.py:4478-4479) | [官方文档](https://developers.binance.com/docs/mining/rest-api/Earnings-List)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_account_enable_fast_withdraw_switch(**params)
说明：Placeholder function for POST /sapi/v1/account/enableFastWithdrawSwitch. | [源码](同步 binance/client.py:15042-15054, 异步 binance/async_client.py:4506-4507) | [官方文档](https://developers.binance.com/docs/wallet/account/enable-fast-withdraw-switch)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_broker_transfer_futures(**params)
说明：Placeholder function for POST /sapi/v1/broker/transfer/futures. | [源码](同步 binance/client.py:15056-15068, 异步 binance/async_client.py:4511-4512) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/asset/Sub-Account-Transfer-Futures)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_sol_staking_sol_stake(**params)
说明：Placeholder function for POST /sapi/v1/sol-staking/sol/stake. | [源码](同步 binance/client.py:15070-15082, 异步 binance/async_client.py:4522-4523) | [官方文档](https://developers.binance.com/docs/staking/sol-staking/staking)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_loan_borrow(**params)
说明：Placeholder function for POST /sapi/v1/loan/borrow. | [源码](同步 binance/client.py:15084-15094, 异步 binance/async_client.py:4527-4528) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_managed_subaccount_info(**params)
说明：Placeholder function for GET /sapi/v1/managed-subaccount/info. | [源码](同步 binance/client.py:15096-15108, 异步 binance/async_client.py:4532-4533) | [官方文档](https://developers.binance.com/docs/sub_account/managed-sub-account/Query-Managed-Sub-account-List)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_lending_auto_invest_plan_edit_status(**params)
说明：Placeholder function for POST /sapi/v1/lending/auto-invest/plan/edit-status. | [源码](同步 binance/client.py:15110-15120, 异步 binance/async_client.py:4537-4538) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_sol_staking_sol_history_unclaimed_rewards(**params)
说明：Placeholder function for GET /sapi/v1/sol-staking/sol/history/unclaimedRewards. | [源码](同步 binance/client.py:15122-15134, 异步 binance/async_client.py:4542-4543) | [官方文档](https://developers.binance.com/docs/staking/sol-staking/history/Get-Unclaimed-rewards)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_asset_convert_transfer_query_by_page(**params)
说明：Placeholder function for POST /sapi/v1/asset/convert-transfer/queryByPage. | [源码](同步 binance/client.py:15136-15146, 异步 binance/async_client.py:4547-4548) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_sol_staking_sol_history_boost_rewards_history(**params)
说明：Placeholder function for GET /sapi/v1/sol-staking/sol/history/boostRewardsHistory. | [源码](同步 binance/client.py:15148-15160, 异步 binance/async_client.py:4552-4553) | [官方文档](https://developers.binance.com/docs/staking/sol-staking/history/Get-Boost-rewards-History)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_lending_auto_invest_one_off_status(**params)
说明：Placeholder function for GET /sapi/v1/lending/auto-invest/one-off/status. | [源码](同步 binance/client.py:15162-15172, 异步 binance/async_client.py:4557-4558) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_broker_sub_account(**params)
说明：Placeholder function for POST /sapi/v1/broker/subAccount. | [源码](同步 binance/client.py:15174-15186, 异步 binance/async_client.py:4562-4563) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/account)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_asset_ledger_transfer_cloud_mining_query_by_page(**params)
说明：Placeholder function for GET /sapi/v1/asset/ledger-transfer/cloud-mining/queryByPage. | [源码](同步 binance/client.py:15188-15200, 异步 binance/async_client.py:4567-4568) | [官方文档](https://developers.binance.com/docs/wallet/asset/cloud-mining-payment-and-refund-history)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_mining_pub_coin_list(**params)
说明：Placeholder function for GET /sapi/v1/mining/pub/coinList. | [源码](同步 binance/client.py:15202-15214, 异步 binance/async_client.py:4572-4573) | [官方文档](https://developers.binance.com/docs/mining/rest-api/Acquiring-CoinName)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v2_get_loan_flexible_repay_history(**params)
说明：Placeholder function for GET /sapi/v2/loan/flexible/repay/history. | [源码](同步 binance/client.py:15216-15228, 异步 binance/async_client.py:4577-4578) | [官方文档](https://developers.binance.com/docs/crypto_loan/flexible-rate/user-information/Get-Flexible-Loan-Repayment-History)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_capital_deposit_credit_apply(**params)
说明：Placeholder function for POST /sapi/v1/capital/deposit/credit-apply. | [源码](同步 binance/client.py:15242-15254, 异步 binance/async_client.py:4587-4588) | [官方文档](https://developers.binance.com/docs/wallet/capital/one-click-arrival-deposite-apply)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_mining_statistics_user_list(**params)
说明：Placeholder function for GET /sapi/v1/mining/statistics/user/list. | [源码](同步 binance/client.py:15268-15280, 异步 binance/async_client.py:4600-4601) | [官方文档](https://developers.binance.com/docs/mining/rest-api/Account-List)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_mining_worker_detail(**params)
说明：Placeholder function for GET /sapi/v1/mining/worker/detail. | [源码](同步 binance/client.py:15306-15318, 异步 binance/async_client.py:4615-4616) | [官方文档](https://developers.binance.com/docs/mining/rest-api/Request-for-Detail-Miner-List)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_managed_subaccount_fetch_future_asset(**params)
说明：Placeholder function for GET /sapi/v1/managed-subaccount/fetch-future-asset. | [源码](同步 binance/client.py:15320-15332, 异步 binance/async_client.py:4620-4621) | [官方文档](https://developers.binance.com/docs/sub_account/managed-sub-account/Query-Managed-Sub-account-Futures-Asset-Details)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_margin_rate_limit_order(**params)
说明：Placeholder function for GET /sapi/v1/margin/rateLimit/order. | [源码](同步 binance/client.py:15334-15346, 异步 binance/async_client.py:4625-4626) | [官方文档](https://developers.binance.com/docs/margin_trading/trade/Query-Current-Margin-Order-Count-Usage)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_localentity_vasp(**params)
说明：Placeholder function for GET /sapi/v1/localentity/vasp. | [源码](同步 binance/client.py:15348-15360, 异步 binance/async_client.py:4630-4631) | [官方文档](https://developers.binance.com/docs/wallet/travel-rule/onboarded-vasp-list)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_sol_staking_sol_history_rate_history(**params)
说明：Placeholder function for GET /sapi/v1/sol-staking/sol/history/rateHistory. | [源码](同步 binance/client.py:15362-15374, 异步 binance/async_client.py:4635-4636) | [官方文档](https://developers.binance.com/docs/staking/sol-staking/history/Get-BNSOL-Rate-History)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_broker_sub_account_api_ip_restriction(**params)
说明：Placeholder function for POST /sapi/v1/broker/subAccountApi/ipRestriction. | [源码](同步 binance/client.py:15376-15386, 异步 binance/async_client.py:4640-4641) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_broker_transfer(**params)
说明：Placeholder function for GET /sapi/v1/broker/transfer. | [源码](同步 binance/client.py:15388-15400, 异步 binance/async_client.py:4645-4646) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/asset/Query-Sub-Account-Transfer-History-Spot)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_sol_staking_account(**params)
说明：Placeholder function for GET /sapi/v1/sol-staking/account. | [源码](同步 binance/client.py:15402-15414, 异步 binance/async_client.py:4650-4651) | [官方文档](https://developers.binance.com/docs/staking/sol-staking/account)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_account_info(**params)
说明：Placeholder function for GET /sapi/v1/account/info. | [源码](同步 binance/client.py:15416-15428, 异步 binance/async_client.py:4655-4656) | [官方文档](https://developers.binance.com/docs/wallet/account)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_portfolio_repay_futures_switch(**params)
说明：Placeholder function for POST /sapi/v1/portfolio/repay-futures-switch. | [源码](同步 binance/client.py:15430-15442, 异步 binance/async_client.py:4660-4661) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin-pro/account/Change-Auto-repay-futures-Status)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_loan_vip_borrow(**params)
说明：Placeholder function for POST /sapi/v1/loan/vip/borrow. | [源码](同步 binance/client.py:15444-15454, 异步 binance/async_client.py:4665-4666) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v2_get_loan_flexible_ltv_adjustment_history(**params)
说明：Placeholder function for GET /sapi/v2/loan/flexible/ltv/adjustment/history. | [源码](同步 binance/client.py:15456-15468, 异步 binance/async_client.py:4670-4671) | [官方文档](https://developers.binance.com/docs/crypto_loan/flexible-rate/user-information)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_broker_sub_account_futures_summary(**params)
说明：Placeholder function for GET /sapi/v1/broker/subAccount/futuresSummary. | [源码](同步 binance/client.py:15484-15494, 异步 binance/async_client.py:4680-4681) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_broker_sub_account_spot_summary(**params)
说明：Placeholder function for GET /sapi/v1/broker/subAccount/spotSummary. | [源码](同步 binance/client.py:15496-15508, 异步 binance/async_client.py:4685-4686) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/asset/Query-Sub-Account-Spot-Asset-Info)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_sub_account_blvt_enable(**params)
说明：Placeholder function for POST /sapi/v1/sub-account/blvt/enable. | [源码](同步 binance/client.py:15510-15520, 异步 binance/async_client.py:4690-4691) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_algo_spot_historical_orders(**params)
说明：Placeholder function for GET /sapi/v1/algo/spot/historicalOrders. | [源码](同步 binance/client.py:15522-15534, 异步 binance/async_client.py:4695-4696) | [官方文档](https://developers.binance.com/docs/algo/spot-algo/Query-Historical-Algo-Orders)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_loan_vip_repay_history(**params)
说明：Placeholder function for GET /sapi/v1/loan/vip/repay/history. | [源码](同步 binance/client.py:15536-15548, 异步 binance/async_client.py:4700-4701) | [官方文档](https://developers.binance.com/docs/vip_loan/user-information/Get-VIP-Loan-Repayment-History)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_loan_borrow_history(**params)
说明：Placeholder function for GET /sapi/v1/loan/borrow/history. | [源码](同步 binance/client.py:15550-15562, 异步 binance/async_client.py:4705-4706) | [官方文档](https://developers.binance.com/docs/crypto_loan/stable-rate/user-information)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_lending_auto_invest_redeem(**params)
说明：Placeholder function for POST /sapi/v1/lending/auto-invest/redeem. | [源码](同步 binance/client.py:15564-15574, 异步 binance/async_client.py:4710-4711) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_managed_subaccount_deposit(**params)
说明：Placeholder function for POST /sapi/v1/managed-subaccount/deposit. | [源码](同步 binance/client.py:15590-15602, 异步 binance/async_client.py:4726-4727) | [官方文档](https://developers.binance.com/docs/sub_account/managed-sub-account)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_lending_daily_purchase(**params)
说明：Placeholder function for POST /sapi/v1/lending/daily/purchase. | [源码](同步 binance/client.py:15604-15614, 异步 binance/async_client.py:4731-4732) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_delete_sub_account_sub_account_api_ip_restriction_ip_list(**params)
说明：Placeholder function for DELETE /sapi/v1/sub-account/subAccountApi/ipRestriction/ipList. | [源码](同步 binance/client.py:15630-15642, 异步 binance/async_client.py:4741-4742) | [官方文档](https://developers.binance.com/docs/sub_account/api-management/Delete-IP-List-For-a-Sub-account-API-Key)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_copy_trading_futures_user_status(**params)
说明：Placeholder function for GET /sapi/v1/copyTrading/futures/userStatus. | [源码](同步 binance/client.py:15644-15656, 异步 binance/async_client.py:4746-4747) | [官方文档](https://developers.binance.com/docs/copy_trading/future-copy-trading)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### options_v1_get_margin_account(**params)
说明：Placeholder function for GET /eapi/v1/marginAccount. | [源码](同步 binance/client.py:15658-15670, 异步 binance/async_client.py:4751-4752) | [官方文档](https://developers.binance.com/docs/derivatives/option/market-maker-endpoints)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_localentity_withdraw_apply(**params)
说明：Placeholder function for POST /sapi/v1/localentity/withdraw/apply. | [源码](同步 binance/client.py:15719-15731, 异步 binance/async_client.py:4756-4757) | [官方文档](https://developers.binance.com/docs/wallet/travel-rule/withdraw)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_asset_wallet_balance(**params)
说明：Placeholder function for GET /sapi/v1/asset/wallet/balance. | [源码](同步 binance/client.py:15733-15745, 异步 binance/async_client.py:4764-4765) | [官方文档](https://developers.binance.com/docs/wallet/asset/query-user-wallet-balance)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_broker_transfer(**params)
说明：Placeholder function for POST /sapi/v1/broker/transfer. | [源码](同步 binance/client.py:15747-15759, 异步 binance/async_client.py:4769-4770) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/asset)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_lending_customized_fixed_purchase(**params)
说明：Placeholder function for POST /sapi/v1/lending/customizedFixed/purchase. | [源码](同步 binance/client.py:15761-15771, 异步 binance/async_client.py:4774-4775) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_algo_futures_new_order_twap(**params)
说明：Placeholder function for POST /sapi/v1/algo/futures/newOrderTwap. | [源码](同步 binance/client.py:15773-15785, 异步 binance/async_client.py:4779-4780) | [官方文档](https://developers.binance.com/docs/algo/future-algo/Time-Weighted-Average-Price-New-Order)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v2_post_eth_staking_eth_stake(**params)
说明：Placeholder function for POST /sapi/v2/eth-staking/eth/stake. | [源码](同步 binance/client.py:15787-15799, 异步 binance/async_client.py:4784-4785) | [官方文档](https://developers.binance.com/docs/staking/eth-staking/staking)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_loan_flexible_repay_history(**params)
说明：Placeholder function for POST /sapi/v1/loan/flexible/repay/history. | [源码](同步 binance/client.py:15801-15811, 异步 binance/async_client.py:4789-4790) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_lending_auto_invest_index_info(**params)
说明：Placeholder function for GET /sapi/v1/lending/auto-invest/index/info. | [源码](同步 binance/client.py:15813-15823, 异步 binance/async_client.py:4797-4798) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_sol_staking_sol_history_redemption_history(**params)
说明：Placeholder function for GET /sapi/v1/sol-staking/sol/history/redemptionHistory. | [源码](同步 binance/client.py:15825-15837, 异步 binance/async_client.py:4802-4803) | [官方文档](https://developers.binance.com/docs/staking/sol-staking/history/Get-SOL-redemption-history)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_broker_rebate_futures_recent_record(**params)
说明：Placeholder function for GET /sapi/v1/broker/rebate/futures/recentRecord. | [源码](同步 binance/client.py:15839-15851, 异步 binance/async_client.py:4807-4808) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/fee/Query-Futures-Commission-Rebate-Record)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v3_get_broker_sub_account_futures_summary(**params)
说明：Placeholder function for GET /sapi/v3/broker/subAccount/futuresSummary. | [源码](同步 binance/client.py:15853-15865, 异步 binance/async_client.py:4812-4813) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/asset/Query-Sub-Account-Futures-Asset-Info)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_lending_auto_invest_target_asset_roi_list(**params)
说明：Placeholder function for GET /sapi/v1/lending/auto-invest/target-asset/roi/list. | [源码](同步 binance/client.py:15867-15877, 异步 binance/async_client.py:4820-4821) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_broker_universal_transfer(**params)
说明：Placeholder function for GET /sapi/v1/broker/universalTransfer. | [源码](同步 binance/client.py:15879-15891, 异步 binance/async_client.py:4825-4826) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/asset/Query-Universal-Transfer-History)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_loan_collateral_data(**params)
说明：Placeholder function for GET /sapi/v1/loan/collateral/data. | [源码](同步 binance/client.py:15921-15931, 异步 binance/async_client.py:4840-4841) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_loan_repay_history(**params)
说明：Placeholder function for GET /sapi/v1/loan/repay/history. | [源码](同步 binance/client.py:15933-15945, 异步 binance/async_client.py:4845-4846) | [官方文档](https://developers.binance.com/docs/crypto_loan/stable-rate/user-information/Get-Loan-Repayment-History)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_convert_limit_place_order(**params)
说明：Placeholder function for POST /sapi/v1/convert/limit/placeOrder. | [源码](同步 binance/client.py:15947-15959, 异步 binance/async_client.py:4850-4851) | [官方文档](https://developers.binance.com/docs/convert/trade/Place-Order)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_delete_broker_sub_account_api_ip_restriction_ip_list(**params)
说明：Placeholder function for DELETE /sapi/v1/broker/subAccountApi/ipRestriction/ipList. | [源码](同步 binance/client.py:15987-15999, 异步 binance/async_client.py:4865-4866) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/account/Delete-IPRestriction-for-Sub-Account-Api-Key)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_sub_account_virtual_sub_account(**params)
说明：Placeholder function for POST /sapi/v1/sub-account/virtualSubAccount. | [源码](同步 binance/client.py:16001-16013, 异步 binance/async_client.py:4870-4871) | [官方文档](https://developers.binance.com/docs/sub_account/account-management)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_put_localentity_deposit_provide_info(**params)
说明：Placeholder function for PUT /sapi/v1/localentity/deposit/provide-info. | [源码](同步 binance/client.py:16015-16027, 异步 binance/async_client.py:4875-4876) | [官方文档](https://developers.binance.com/docs/wallet/travel-rule/deposit-provide-info)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_portfolio_mint(**params)
说明：Placeholder function for POST /sapi/v1/portfolio/mint. | [源码](同步 binance/client.py:16029-16041, 异步 binance/async_client.py:4880-4881) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin-pro/account/Mint-BFUSD-Portfolio-Margin)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_sol_staking_sol_claim(**params)
说明：Placeholder function for POST /sapi/v1/sol-staking/sol/claim. | [源码](同步 binance/client.py:16057-16069, 异步 binance/async_client.py:4890-4891) | [官方文档](https://developers.binance.com/docs/staking/sol-staking/staking/Claim-Boost-rewards)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_lending_daily_redeem(**params)
说明：Placeholder function for POST /sapi/v1/lending/daily/redeem. | [源码](同步 binance/client.py:16071-16081, 异步 binance/async_client.py:4895-4896) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_mining_hash_transfer_config(**params)
说明：Placeholder function for POST /sapi/v1/mining/hash-transfer/config. | [源码](同步 binance/client.py:16083-16095, 异步 binance/async_client.py:4900-4901) | [官方文档](https://developers.binance.com/docs/mining/rest-api/Hashrate-Resale-Request)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_lending_auto_invest_rebalance_history(**params)
说明：Placeholder function for GET /sapi/v1/lending/auto-invest/rebalance/history. | [源码](同步 binance/client.py:16097-16107, 异步 binance/async_client.py:4905-4906) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_loan_repay_collateral_rate(**params)
说明：Placeholder function for GET /sapi/v1/loan/repay/collateral/rate. | [源码](同步 binance/client.py:16109-16119, 异步 binance/async_client.py:4910-4911) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_mining_payment_uid(**params)
说明：Placeholder function for GET /sapi/v1/mining/payment/uid. | [源码](同步 binance/client.py:16135-16147, 异步 binance/async_client.py:4920-4921) | [官方文档](https://developers.binance.com/docs/mining/rest-api/Mining-Account-Earning)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v2_get_loan_flexible_borrow_history(**params)
说明：Placeholder function for GET /sapi/v2/loan/flexible/borrow/history. | [源码](同步 binance/client.py:16149-16161, 异步 binance/async_client.py:4925-4926) | [官方文档](https://developers.binance.com/docs/crypto_loan/flexible-rate/user-information/Get-Flexible-Loan-Borrow-History)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_capital_contract_convertible_coins(**params)
说明：Placeholder function for GET /sapi/v1/capital/contract/convertible-coins. | [源码](同步 binance/client.py:16163-16173, 异步 binance/async_client.py:4933-4934) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_broker_sub_account_api_permission_vanilla_options(**params)
说明：Placeholder function for POST /sapi/v1/broker/subAccountApi/permission/vanillaOptions. | [源码](同步 binance/client.py:16175-16185, 异步 binance/async_client.py:4938-4939) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_lending_auto_invest_redeem_history(**params)
说明：Placeholder function for GET /sapi/v1/lending/auto-invest/redeem/history. | [源码](同步 binance/client.py:16187-16199, 异步 binance/async_client.py:4943-4944) | [官方文档](https://developers.binance.com/docs/wallet/travel-rule/withdraw-history)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v2_get_localentity_withdraw_history(**params)
说明：Placeholder function for GET /sapi/v2/localentity/withdraw/history. | [源码](同步 binance/client.py:16201-16213, 异步 binance/async_client.py:4948-4949) | [官方文档](https://developers.binance.com/docs/wallet/travel-rule/withdraw-history-v2)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_eth_staking_eth_history_redemption_history(**params)
说明：Placeholder function for GET /sapi/v1/eth-staking/eth/history/redemptionHistory. | [源码](同步 binance/client.py:16215-16227, 异步 binance/async_client.py:4953-4954) | [官方文档](https://developers.binance.com/docs/staking/eth-staking/history/Get-ETH-redemption-history)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_lending_auto_invest_index_user_summary(**params)
说明：Placeholder function for GET /sapi/v1/lending/auto-invest/index/user-summary. | [源码](同步 binance/client.py:16243-16253, 异步 binance/async_client.py:4963-4964) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v2_post_loan_flexible_borrow(**params)
说明：Placeholder function for POST /sapi/v2/loan/flexible/borrow. | [源码](同步 binance/client.py:16255-16267, 异步 binance/async_client.py:4968-4969) | [官方文档](https://developers.binance.com/docs/crypto_loan/flexible-rate/trade)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_loan_vip_repay(**params)
说明：Placeholder function for POST /sapi/v1/loan/vip/repay. | [源码](同步 binance/client.py:16269-16281, 异步 binance/async_client.py:4973-4974) | [官方文档](https://developers.binance.com/docs/vip_loan/trade/VIP-Loan-Repay)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_convert_asset_info(**params)
说明：Placeholder function for GET /sapi/v1/convert/assetInfo. | [源码](同步 binance/client.py:16297-16309, 异步 binance/async_client.py:4983-4984) | [官方文档](https://developers.binance.com/docs/convert/market-data/Query-order-quantity-precision-per-asset)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_broker_universal_transfer(**params)
说明：Placeholder function for POST /sapi/v1/broker/universalTransfer. | [源码](同步 binance/client.py:16323-16335, 异步 binance/async_client.py:4993-4994) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/asset/Universal-Transfer)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_account_disable_fast_withdraw_switch(**params)
说明：Placeholder function for POST /sapi/v1/account/disableFastWithdrawSwitch. | [源码](同步 binance/client.py:16337-16349, 异步 binance/async_client.py:4998-4999) | [官方文档](https://developers.binance.com/docs/wallet/account/disable-fast-withdraw-switch)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_account_api_restrictions_ip_restriction(**params)
说明：Placeholder function for GET /sapi/v1/account/apiRestrictions/ipRestriction. | [源码](同步 binance/client.py:16365-16375, 异步 binance/async_client.py:5011-5012) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_broker_sub_account_bnb_burn_spot(**params)
说明：Placeholder function for POST /sapi/v1/broker/subAccount/bnbBurn/spot. | [源码](同步 binance/client.py:16377-16389, 异步 binance/async_client.py:5016-5017) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/account/Enable-Or-Disable-BNB-Burn-for-Sub-Account-Spot-Margin)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_margin_delist_schedule(**params)
说明：Placeholder function for GET /sapi/v1/margin/delist-schedule. | [源码](同步 binance/client.py:16419-16429, 异步 暂无对应实现) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_broker_sub_account_api_permission_universal_transfer(**params)
说明：Placeholder function for POST /sapi/v1/broker/subAccountApi/permission/universalTransfer. | [源码](同步 binance/client.py:16431-16443, 异步 binance/async_client.py:5029-5030) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/account/Enable-Universal-Transfer-Permission-For-SubAccount-Api-Key)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_loan_ltv_adjustment_history(**params)
说明：Placeholder function for GET /sapi/v1/loan/ltv/adjustment/history. | [源码](同步 binance/client.py:16445-16457, 异步 binance/async_client.py:5037-5038) | [官方文档](https://developers.binance.com/docs/crypto_loan/stable-rate/user-information/Get-Loan-LTV-Adjustment-History)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_localentity_withdraw_history(**params)
说明：Placeholder function for GET /sapi/v1/localentity/withdraw/history. | [源码](同步 binance/client.py:16459-16469, 异步 binance/async_client.py:5042-5043) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v2_post_sub_account_sub_account_api_ip_restriction(**params)
说明：Placeholder function for POST /sapi/v2/sub-account/subAccountApi/ipRestriction. | [源码](同步 binance/client.py:16471-16483, 异步 binance/async_client.py:5047-5048) | [官方文档](https://developers.binance.com/docs/sub_account/api-management/Add-IP-Restriction-for-Sub-Account-API-key)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_broker_sub_account_api_commission_futures(**params)
说明：Placeholder function for GET /sapi/v1/broker/subAccountApi/commission/futures. | [源码](同步 binance/client.py:16499-16511, 异步 binance/async_client.py:5057-5058) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/fee/Query-Sub-Account-UM-Futures-Commission)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_sol_staking_sol_history_staking_history(**params)
说明：Placeholder function for GET /sapi/v1/sol-staking/sol/history/stakingHistory. | [源码](同步 binance/client.py:16513-16525, 异步 binance/async_client.py:5062-5063) | [官方文档](https://developers.binance.com/docs/staking/sol-staking/history)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_delete_algo_spot_order(**params)
说明：Placeholder function for DELETE /sapi/v1/algo/spot/order. | [源码](同步 binance/client.py:16541-16553, 异步 binance/async_client.py:5072-5073) | [官方文档](https://developers.binance.com/docs/algo/spot-algo/Cancel-Algo-Order)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_delete_account_api_restrictions_ip_restriction_ip_list(**params)
说明：Placeholder function for DELETE /sapi/v1/account/apiRestrictions/ipRestriction/ipList. | [源码](同步 binance/client.py:16555-16565, 异步 binance/async_client.py:5080-5081) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_capital_contract_convertible_coins(**params)
说明：Placeholder function for POST /sapi/v1/capital/contract/convertible-coins. | [源码](同步 binance/client.py:16567-16577, 异步 binance/async_client.py:5085-5086) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_managed_subaccount_margin_asset(**params)
说明：Placeholder function for GET /sapi/v1/managed-subaccount/marginAsset. | [源码](同步 binance/client.py:16579-16591, 异步 binance/async_client.py:5090-5091) | [官方文档](https://developers.binance.com/docs/sub_account/managed-sub-account/Query-Managed-Sub-account-Margin-Asset-Details)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_sub_account_sub_account_api_ip_restriction_ip_list(**params)
说明：Placeholder function for POST /sapi/v1/sub-account/subAccountApi/ipRestriction/ipList. | [源码](同步 binance/client.py:16605-16615, 异步 binance/async_client.py:5100-5101) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_broker_sub_account_api_commission(**params)
说明：Placeholder function for POST /sapi/v1/broker/subAccountApi/commission. | [源码](同步 binance/client.py:16617-16629, 异步 binance/async_client.py:5105-5106) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/fee)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_broker_sub_account_margin_summary(**params)
说明：Placeholder function for GET /sapi/v1/broker/subAccount/marginSummary. | [源码](同步 binance/client.py:16645-16657, 异步 binance/async_client.py:5115-5116) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/asset/Query-Sub-Account-Margin-Asset-Info)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_lending_auto_invest_plan_list(**params)
说明：Placeholder function for GET /sapi/v1/lending/auto-invest/plan/list. | [源码](同步 binance/client.py:16659-16669, 异步 binance/async_client.py:5120-5121) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_loan_vip_loanable_data(**params)
说明：Placeholder function for GET /sapi/v1/loan/vip/loanable/data. | [源码](同步 binance/client.py:16671-16683, 异步 binance/async_client.py:5125-5126) | [官方文档](https://developers.binance.com/docs/vip_loan/market-data/Get-Loanable-Assets-Data)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v2_get_loan_flexible_collateral_data(**params)
说明：Placeholder function for GET /sapi/v2/loan/flexible/collateral/data. | [源码](同步 binance/client.py:16685-16697, 异步 binance/async_client.py:5130-5131) | [官方文档](https://developers.binance.com/docs/crypto_loan/flexible-rate/market-data)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_delete_broker_sub_account_api(**params)
说明：Placeholder function for DELETE /sapi/v1/broker/subAccountApi. | [源码](同步 binance/client.py:16699-16711, 异步 binance/async_client.py:5135-5136) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/account/Delete-Sub-Account-Api-Key)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_sol_staking_sol_history_bnsol_rewards_history(**params)
说明：Placeholder function for GET /sapi/v1/sol-staking/sol/history/bnsolRewardsHistory. | [源码](同步 binance/client.py:16713-16725, 异步 binance/async_client.py:5140-5141) | [官方文档](https://developers.binance.com/docs/staking/sol-staking/history/Get-BNSOL-rewards-history)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_convert_limit_query_open_orders(**params)
说明：Placeholder function for GET /sapi/v1/convert/limit/queryOpenOrders. | [源码](同步 binance/client.py:16727-16739, 异步 binance/async_client.py:5145-5146) | [官方文档](https://developers.binance.com/docs/convert/trade/Query-Order)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_managed_subaccount_query_trans_log(**params)
说明：Placeholder function for GET /sapi/v1/managed-subaccount/query-trans-log. | [源码](同步 binance/client.py:16753-16765, 异步 binance/async_client.py:5158-5159) | [官方文档](https://developers.binance.com/docs/sub_account/managed-sub-account/Query-Managed-Sub-Account-Transfer-Log-Trading-Team-Sub)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v2_post_broker_sub_account_api_ip_restriction(**params)
说明：Placeholder function for POST /sapi/v2/broker/subAccountApi/ipRestriction. | [源码](同步 binance/client.py:16767-16779, 异步 binance/async_client.py:5163-5164) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/account/Update-IP-Restriction-for-Sub-Account-API-key-For-Master-Account)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_lending_auto_invest_all_asset(**params)
说明：Placeholder function for GET /sapi/v1/lending/auto-invest/all/asset. | [源码](同步 binance/client.py:16781-16791, 异步 binance/async_client.py:5168-5169) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_spot_delist_schedule(**params)
说明：Placeholder function for GET /sapi/v1/spot/delist-schedule. | [源码](同步 binance/client.py:16807-16819, 异步 binance/async_client.py:5178-5179) | [官方文档](https://developers.binance.com/docs/wallet/asset/spot-delist-schedule)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_account_api_restrictions_ip_restriction(**params)
说明：Placeholder function for POST /sapi/v1/account/apiRestrictions/ipRestriction. | [源码](同步 binance/client.py:16821-16831, 异步 binance/async_client.py:5183-5184) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_dci_product_accounts(**params)
说明：Placeholder function for GET /sapi/v1/dci/product/accounts. | [源码](同步 binance/client.py:16833-16845, 异步 binance/async_client.py:5188-5189) | [官方文档](https://developers.binance.com/docs/dual_investment/trade/Check-Dual-Investment-accounts)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_sub_account_sub_account_api_ip_restriction(**params)
说明：Placeholder function for GET /sapi/v1/sub-account/subAccountApi/ipRestriction. | [源码](同步 binance/client.py:16847-16859, 异步 binance/async_client.py:5193-5194) | [官方文档](https://developers.binance.com/docs/sub_account/api-management)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_sub_account_transaction_statistics(**params)
说明：Placeholder function for GET /sapi/v1/sub-account/transaction-statistics. | [源码](同步 binance/client.py:16861-16873, 异步 binance/async_client.py:5198-5199) | [官方文档](https://developers.binance.com/docs/sub_account/account-management/Query-Sub-account-Transaction-Statistics)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_managed_subaccount_deposit_address(**params)
说明：Placeholder function for GET /sapi/v1/managed-subaccount/deposit/address. | [源码](同步 binance/client.py:16875-16887, 异步 binance/async_client.py:5203-5204) | [官方文档](https://developers.binance.com/docs/sub_account/managed-sub-account/Get-Managed-Sub-account-Deposit-Address)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v2_get_portfolio_account(**params)
说明：Placeholder function for GET /sapi/v2/portfolio/account. | [源码](同步 binance/client.py:16889-16901, 异步 binance/async_client.py:5208-5209) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin-pro/account/Get-Classic-Portfolio-Margin-Account-Info-V2)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_simple_earn_locked_history_redemption_record(**params)
说明：Placeholder function for GET /sapi/v1/simple-earn/locked/history/redemptionRecord. | [源码](同步 binance/client.py:16903-16915, 异步 binance/async_client.py:5213-5214) | [官方文档](https://developers.binance.com/docs/simple_earn/history/Get-Locked-Redemption-Record)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_managed_subaccount_withdraw(**params)
说明：Placeholder function for POST /sapi/v1/managed-subaccount/withdraw. | [源码](同步 binance/client.py:16931-16943, 异步 binance/async_client.py:5223-5224) | [官方文档](https://developers.binance.com/docs/sub_account/managed-sub-account/Withdrawl-Assets-From-The-Managed-Sub-account)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_localentity_deposit_history(**params)
说明：Placeholder function for GET /sapi/v1/localentity/deposit/history. | [源码](同步 binance/client.py:16945-16957, 异步 binance/async_client.py:5228-5229) | [官方文档](https://developers.binance.com/docs/wallet/travel-rule/deposit-history)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_eth_staking_wbeth_wrap(**params)
说明：Placeholder function for POST /sapi/v1/eth-staking/wbeth/wrap. | [源码](同步 binance/client.py:16959-16971, 异步 binance/async_client.py:5233-5234) | [官方文档](https://developers.binance.com/docs/staking/eth-staking/staking/Wrap-BETH)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_simple_earn_locked_set_redeem_option(**params)
说明：Placeholder function for POST /sapi/v1/simple-earn/locked/setRedeemOption. | [源码](同步 binance/client.py:16973-16985, 异步 binance/async_client.py:5238-5239) | [官方文档](https://developers.binance.com/docs/simple_earn/earn/Set-Locked-Redeem-Option)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_broker_sub_account_api_ip_restriction_ip_list(**params)
说明：Placeholder function for POST /sapi/v1/broker/subAccountApi/ipRestriction/ipList. | [源码](同步 binance/client.py:16987-16997, 异步 binance/async_client.py:5243-5244) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_broker_sub_account_api_commission_futures(**params)
说明：Placeholder function for POST /sapi/v1/broker/subAccountApi/commission/futures. | [源码](同步 binance/client.py:16999-17011, 异步 binance/async_client.py:5248-5249) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/fee/Change-Sub-Account-UM-Futures-Commission)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_lending_auto_invest_history_list(**params)
说明：Placeholder function for GET /sapi/v1/lending/auto-invest/history/list. | [源码](同步 binance/client.py:17013-17023, 异步 binance/async_client.py:5256-5257) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_loan_customize_margin_call(**params)
说明：Placeholder function for POST /sapi/v1/loan/customize/margin_call. | [源码](同步 binance/client.py:17025-17035, 异步 binance/async_client.py:5261-5262) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_broker_sub_account_bnb_burn_status(**params)
说明：Placeholder function for GET /sapi/v1/broker/subAccount/bnbBurn/status. | [源码](同步 binance/client.py:17037-17049, 异步 binance/async_client.py:5266-5267) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/account/Get-BNB-Burn-Status-for-Sub-Account)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_managed_subaccount_account_snapshot(**params)
说明：Placeholder function for GET /sapi/v1/managed-subaccount/accountSnapshot. | [源码](同步 binance/client.py:17051-17063, 异步 binance/async_client.py:5271-5272) | [官方文档](https://developers.binance.com/docs/sub_account/managed-sub-account/Query-Managed-Sub-account-Snapshot)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_asset_convert_transfer(**params)
说明：Placeholder function for POST /sapi/v1/asset/convert-transfer. | [源码](同步 binance/client.py:17065-17075, 异步 binance/async_client.py:5276-5277) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_broker_sub_account_api_commission_coin_futures(**params)
说明：Placeholder function for GET /sapi/v1/broker/subAccountApi/commission/coinFutures. | [源码](同步 binance/client.py:17091-17103, 异步 binance/async_client.py:5286-5287) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/fee/Query-Sub-Account-CM-Futures-Commission)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v2_get_broker_sub_account_futures_summary(**params)
说明：Placeholder function for GET /sapi/v2/broker/subAccount/futuresSummary. | [源码](同步 binance/client.py:17105-17115, 异步 binance/async_client.py:5291-5292) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_loan_ongoing_orders(**params)
说明：Placeholder function for GET /sapi/v1/loan/ongoing/orders. | [源码](同步 binance/client.py:17117-17127, 异步 binance/async_client.py:5296-5297) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v2_get_loan_flexible_ongoing_orders(**params)
说明：Placeholder function for GET /sapi/v2/loan/flexible/ongoing/orders. | [源码](同步 binance/client.py:17129-17141, 异步 binance/async_client.py:5301-5302) | [官方文档](https://developers.binance.com/docs/crypto_loan/flexible-rate/user-information/Get-Flexible-Loan-Ongoing-Orders)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_algo_futures_new_order_vp(**params)
说明：Placeholder function for POST /sapi/v1/algo/futures/newOrderVp. | [源码](同步 binance/client.py:17143-17155, 异步 binance/async_client.py:5306-5307) | [官方文档](https://developers.binance.com/docs/algo/future-algo)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_algo_spot_sub_orders(**params)
说明：Placeholder function for GET /sapi/v1/algo/spot/subOrders. | [源码](同步 binance/client.py:17171-17183, 异步 binance/async_client.py:5316-5317) | [官方文档](https://developers.binance.com/docs/algo/spot-algo/Query-Sub-Orders)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_portfolio_redeem(**params)
说明：Placeholder function for POST /sapi/v1/portfolio/redeem. | [源码](同步 binance/client.py:17185-17197, 异步 binance/async_client.py:5321-5322) | [官方文档](https://developers.binance.com/docs/derivatives/portfolio-margin-pro/account/Redeem-BFUSD-Portfolio-Margin)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_lending_auto_invest_plan_add(**params)
说明：Placeholder function for POST /sapi/v1/lending/auto-invest/plan/add. | [源码](同步 binance/client.py:17199-17209, 异步 binance/async_client.py:5326-5327) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_lending_auto_invest_source_asset_list(**params)
说明：Placeholder function for GET /sapi/v1/lending/auto-invest/source-asset/list. | [源码](同步 binance/client.py:17223-17233, 异步 binance/async_client.py:5339-5340) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_margin_all_order_list(**params)
说明：Placeholder function for GET /sapi/v1/margin/allOrderList. | [源码](同步 binance/client.py:17235-17247, 异步 binance/async_client.py:5344-5345) | [官方文档](https://developers.binance.com/docs/margin_trading/trade/Query-Margin-Account-All-OCO)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_eth_staking_eth_redeem(**params)
说明：Placeholder function for POST /sapi/v1/eth-staking/eth/redeem. | [源码](同步 binance/client.py:17249-17261, 异步 binance/async_client.py:5349-5350) | [官方文档](https://developers.binance.com/docs/staking/eth-staking/staking/Redeem-ETH)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_broker_rebate_historical_record(**params)
说明：Placeholder function for GET /sapi/v1/broker/rebate/historicalRecord. | [源码](同步 binance/client.py:17263-17273, 异步 binance/async_client.py:5354-5355) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_simple_earn_locked_history_subscription_record(**params)
说明：Placeholder function for GET /sapi/v1/simple-earn/locked/history/subscriptionRecord. | [源码](同步 binance/client.py:17275-17287, 异步 binance/async_client.py:5359-5360) | [官方文档](https://developers.binance.com/docs/simple_earn/history/Get-Locked-Subscription-Record)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_managed_subaccount_asset(**params)
说明：Placeholder function for GET /sapi/v1/managed-subaccount/asset. | [源码](同步 binance/client.py:17289-17301, 异步 binance/async_client.py:5369-5370) | [官方文档](https://developers.binance.com/docs/sub_account/managed-sub-account/Query-Managed-Sub-account-Asset-Details)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_sol_staking_sol_quota(**params)
说明：Placeholder function for GET /sapi/v1/sol-staking/sol/quota. | [源码](同步 binance/client.py:17303-17315, 异步 binance/async_client.py:5374-5375) | [官方文档](https://developers.binance.com/docs/staking/sol-staking/account/Get-SOL-staking-quota-details)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_loan_vip_renew(**params)
说明：Placeholder function for POST /sapi/v1/loan/vip/renew. | [源码](同步 binance/client.py:17317-17327, 异步 binance/async_client.py:5379-5380) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_managed_subaccount_query_trans_log_for_trade_parent(**params)
说明：Placeholder function for GET /sapi/v1/managed-subaccount/queryTransLogForTradeParent. | [源码](同步 binance/client.py:17329-17341, 异步 binance/async_client.py:5384-5385) | [官方文档](https://developers.binance.com/docs/sub_account/managed-sub-account/Query-Managed-Sub-Account-Transfer-Log-Trading-Team-Master)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_post_sub_account_sub_account_api_ip_restriction(**params)
说明：Placeholder function for POST /sapi/v1/sub-account/subAccountApi/ipRestriction. | [源码](同步 binance/client.py:17343-17353, 异步 binance/async_client.py:5389-5390) | [官方文档](-)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_simple_earn_flexible_history_redemption_record(**params)
说明：Placeholder function for GET /sapi/v1/simple-earn/flexible/history/redemptionRecord. | [源码](同步 binance/client.py:17355-17367, 异步 binance/async_client.py:5394-5395) | [官方文档](https://developers.binance.com/docs/simple_earn/history/Get-Flexible-Redemption-Record)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_broker_sub_account_api(**params)
说明：Placeholder function for GET /sapi/v1/broker/subAccountApi. | [源码](同步 binance/client.py:17369-17381, 异步 binance/async_client.py:5399-5400) | [官方文档](https://developers.binance.com/docs/binance_link/exchange-link/account/Query-Sub-Account-Api-Key)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_convert_exchange_info(**params)
说明：Placeholder function for GET /sapi/v1/convert/exchangeInfo. | [源码](同步 binance/client.py:17412-17424, 异步 binance/async_client.py:5409-5410) | [官方文档](https://developers.binance.com/docs/convert/market-data)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_eth_staking_eth_history_wbeth_rewards_history(**params)
说明：Placeholder function for GET /sapi/v1/eth-staking/eth/history/wbethRewardsHistory. | [源码](同步 binance/client.py:17438-17450, 异步 binance/async_client.py:5419-5420) | [官方文档](https://developers.binance.com/docs/staking/eth-staking/history/Get-WBETH-rewards-history)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_mining_pub_algo_list(**params)
说明：Placeholder function for GET /sapi/v1/mining/pub/algoList. | [源码](同步 binance/client.py:17452-17464, 异步 binance/async_client.py:5424-5425) | [官方文档](https://developers.binance.com/docs/mining/rest-api)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_copy_trading_futures_lead_symbol(**params)
说明：Placeholder function for GET /sapi/v1/copyTrading/futures/leadSymbol. | [源码](同步 binance/client.py:17480-17492, 异步 binance/async_client.py:5434-5435) | [官方文档](https://developers.binance.com/docs/copy_trading/future-copy-trading/Get-Futures-Lead-Trading-Symbol-Whitelist)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_mining_worker_list(**params)
说明：Placeholder function for GET /sapi/v1/mining/worker/list. | [源码](同步 binance/client.py:17494-17506, 异步 binance/async_client.py:5439-5440) | [官方文档](https://developers.binance.com/docs/mining/rest-api/Request-for-Miner-List)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档

### margin_v1_get_dci_product_list(**params)
说明：Placeholder function for GET /sapi/v1/dci/product/list. | [源码](同步 binance/client.py:17508-17520, 异步 binance/async_client.py:5444-5445) | [官方文档](https://developers.binance.com/docs/dual_investment/market-data)

**核心参数**:
- ✅ **必需**: params (dict) : parameters required by the endpoint

**常用值**:
- 源码注释未提供固定枚举值

**返回**:
- API response；详见官方文档
