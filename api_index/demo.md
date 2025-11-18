### create_order(symbol, side, type, **kwargs)
创建订单 | [源码](同步 binance/client.py:1316, 异步 binance/async_client.py:707-710) | [官方文档](https://developers.binance.com/docs/binance-spot-api-docs/rest-api/trading-endpoints#new-order-trade)

**核心参数**:
- ✅ **必需**: `symbol: str`, `side: str`, `type: str`, `quantity: Decimal` (或 `quoteOrderQty: Decimal`)
- ⚠️ **LIMIT 订单额外必需**: `price: str`, `timeInForce: str`
- 💡 **冰山订单**: 使用 `icebergQty` 时，`timeInForce` 必须为 `'GTC'`

**常用值**:
- `side`: `'BUY'` | `'SELL'`
- `type`: `'MARKET'` | `'LIMIT'` | `'STOP_LOSS'` | `'TAKE_PROFIT'` ...
- `timeInForce`: `'GTC'` | `'IOC'` | `'FOK'`

**返回**: `{'orderId': int, 'status': str, 'executedQty': str, ...}`