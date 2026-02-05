"""USDT-M Futures Trade API endpoints."""
from typing import Any

import msgspec

from binance._core.http import HTTPClient
from binance._schemas.futures import FuturesOrder, BatchOrderError

# Pre-compiled decoders
_order_decoder = msgspec.json.Decoder(FuturesOrder)
_order_list_decoder = msgspec.json.Decoder(list[FuturesOrder])
_batch_order_error_decoder = msgspec.json.Decoder(BatchOrderError)


async def create_order(
    http: HTTPClient,
    symbol: str,
    side: str,
    type: str,
    quantity: str | None = None,
    price: str | None = None,
    time_in_force: str | None = None,
    reduce_only: bool | None = None,
    new_client_order_id: str | None = None,
    stop_price: str | None = None,
    position_side: str | None = None,
    close_position: bool | None = None,
    activation_price: str | None = None,
    callback_rate: str | None = None,
    working_type: str | None = None,
    price_protect: bool | None = None,
    new_order_resp_type: str | None = None,
) -> FuturesOrder:
    """Create a new futures order.

    Weight: 1
    Requires: Signature

    Args:
        symbol: Trading pair (e.g., "BTCUSDT")
        side: BUY or SELL
        type: LIMIT, MARKET, STOP, STOP_MARKET, TAKE_PROFIT, TAKE_PROFIT_MARKET,
              TRAILING_STOP_MARKET
        quantity: Order quantity
        price: Limit price (required for LIMIT orders)
        time_in_force: GTC, IOC, FOK, GTX
        reduce_only: Reduce position only (cannot be sent with closePosition)
        new_client_order_id: Custom order ID for idempotency
        stop_price: Stop price for STOP/TAKE_PROFIT orders
        position_side: LONG, SHORT, or BOTH (for hedge mode)
        close_position: Close all position (for STOP orders)
        activation_price: Activation price for TRAILING_STOP_MARKET
        callback_rate: Callback rate for TRAILING_STOP_MARKET
        working_type: MARK_PRICE or CONTRACT_PRICE
        price_protect: Price protection
        new_order_resp_type: ACK or RESULT

    Returns:
        FuturesOrder with order details

    Tip:
        Always provide `new_client_order_id` for idempotent order placement.
    """
    params: dict[str, Any] = {
        "symbol": symbol,
        "side": side,
        "type": type,
    }
    if quantity is not None:
        params["quantity"] = quantity
    if price is not None:
        params["price"] = price
    if time_in_force is not None:
        params["timeInForce"] = time_in_force
    if reduce_only is not None:
        params["reduceOnly"] = str(reduce_only).lower()
    if new_client_order_id is not None:
        params["newClientOrderId"] = new_client_order_id
    if stop_price is not None:
        params["stopPrice"] = stop_price
    if position_side is not None:
        params["positionSide"] = position_side
    if close_position is not None:
        params["closePosition"] = str(close_position).lower()
    if activation_price is not None:
        params["activationPrice"] = activation_price
    if callback_rate is not None:
        params["callbackRate"] = callback_rate
    if working_type is not None:
        params["workingType"] = working_type
    if price_protect is not None:
        params["priceProtect"] = str(price_protect).lower()
    if new_order_resp_type is not None:
        params["newOrderRespType"] = new_order_resp_type

    raw = await http.request_raw("POST", "/fapi/v1/order", signed=True, params=params)
    return _order_decoder.decode(raw)


async def create_test_order(
    http: HTTPClient,
    symbol: str,
    side: str,
    type: str,
    quantity: str | None = None,
    price: str | None = None,
    time_in_force: str | None = None,
) -> dict[str, Any]:
    """Test new order creation (no actual order placed).

    Weight: 1
    Requires: Signature

    Returns:
        Empty dict on success
    """
    params: dict[str, Any] = {
        "symbol": symbol,
        "side": side,
        "type": type,
    }
    if quantity is not None:
        params["quantity"] = quantity
    if price is not None:
        params["price"] = price
    if time_in_force is not None:
        params["timeInForce"] = time_in_force

    return await http.request("POST", "/fapi/v1/order/test", signed=True, params=params)


async def get_order(
    http: HTTPClient,
    symbol: str,
    order_id: int | None = None,
    orig_client_order_id: str | None = None,
) -> FuturesOrder:
    """Query order status.

    Weight: 1
    Requires: Signature

    Args:
        symbol: Trading pair
        order_id: Order ID (use this or orig_client_order_id)
        orig_client_order_id: Client order ID

    Returns:
        FuturesOrder with current status
    """
    params: dict[str, Any] = {"symbol": symbol}
    if order_id is not None:
        params["orderId"] = order_id
    if orig_client_order_id is not None:
        params["origClientOrderId"] = orig_client_order_id

    raw = await http.request_raw("GET", "/fapi/v1/order", signed=True, params=params)
    return _order_decoder.decode(raw)


async def cancel_order(
    http: HTTPClient,
    symbol: str,
    order_id: int | None = None,
    orig_client_order_id: str | None = None,
) -> FuturesOrder:
    """Cancel an active order.

    Weight: 1
    Requires: Signature

    Returns:
        FuturesOrder with canceled status
    """
    params: dict[str, Any] = {"symbol": symbol}
    if order_id is not None:
        params["orderId"] = order_id
    if orig_client_order_id is not None:
        params["origClientOrderId"] = orig_client_order_id

    raw = await http.request_raw("DELETE", "/fapi/v1/order", signed=True, params=params)
    return _order_decoder.decode(raw)


async def cancel_all_open_orders(
    http: HTTPClient,
    symbol: str,
) -> dict[str, Any]:
    """Cancel all open orders on a symbol.

    Weight: 1
    Requires: Signature

    Returns:
        Success response
    """
    params: dict[str, Any] = {"symbol": symbol}
    return await http.request("DELETE", "/fapi/v1/allOpenOrders", signed=True, params=params)


async def get_open_orders(
    http: HTTPClient,
    symbol: str | None = None,
) -> list[FuturesOrder]:
    """Get all open orders.

    Weight: 1-40 depending on symbol
    Requires: Signature

    Returns:
        List of open FuturesOrder objects
    """
    params: dict[str, Any] = {}
    if symbol is not None:
        params["symbol"] = symbol

    raw = await http.request_raw("GET", "/fapi/v1/openOrders", signed=True, params=params)
    return _order_list_decoder.decode(raw)


async def get_all_orders(
    http: HTTPClient,
    symbol: str,
    order_id: int | None = None,
    start_time: int | None = None,
    end_time: int | None = None,
    limit: int = 500,
) -> list[FuturesOrder]:
    """Get all account orders (active, canceled, filled).

    Weight: 5
    Requires: Signature

    Returns:
        List of FuturesOrder objects
    """
    params: dict[str, Any] = {"symbol": symbol}
    if order_id is not None:
        params["orderId"] = order_id
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if limit != 500:
        params["limit"] = limit

    raw = await http.request_raw("GET", "/fapi/v1/allOrders", signed=True, params=params)
    return _order_list_decoder.decode(raw)


async def create_batch_orders(
    http: HTTPClient,
    orders: list[dict[str, Any]],
) -> list[FuturesOrder | BatchOrderError]:
    """Place multiple orders in a single request.

    Weight: 5
    Requires: Signature

    Note: Each order in the response can be either a FuturesOrder (success)
    or a BatchOrderError (failure). Check for 'code' field to detect errors.

    Args:
        orders: List of order dicts (max 5). Each dict should contain:
            - symbol: Trading pair (required)
            - side: BUY or SELL (required)
            - type: Order type (required)
            - quantity: Order quantity (required for most types)
            - price: Limit price (required for LIMIT orders)
            - positionSide: LONG, SHORT, or BOTH (optional)
            - timeInForce: GTC, IOC, FOK (optional)
            - reduceOnly: true/false (optional)
            - stopPrice: Stop price (for STOP orders)

    Returns:
        List of FuturesOrder or BatchOrderError for each order

    Example:
        orders = [
            {"symbol": "BTCUSDT", "side": "BUY", "type": "LIMIT",
             "quantity": "0.001", "price": "30000", "timeInForce": "GTC"},
            {"symbol": "BTCUSDT", "side": "SELL", "type": "LIMIT",
             "quantity": "0.001", "price": "35000", "timeInForce": "GTC"},
        ]
        results = await create_batch_orders(http, orders)
        for result in results:
            if isinstance(result, BatchOrderError):
                print(f"Order failed: {result.code} - {result.msg}")
            else:
                print(f"Order placed: {result.order_id}")
    """
    import orjson

    # Binance requires batchOrders as a JSON string, not a list
    params: dict[str, Any] = {
        "batchOrders": orjson.dumps(orders).decode(),
    }
    raw = await http.request("POST", "/fapi/v1/batchOrders", signed=True, params=params)

    # Manually decode the union type - check for 'code' field to detect errors
    results: list[FuturesOrder | BatchOrderError] = []
    for item in raw:
        if "code" in item:
            # Error response
            results.append(msgspec.convert(item, BatchOrderError))
        else:
            # Success response
            results.append(msgspec.convert(item, FuturesOrder))
    return results
