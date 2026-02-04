"""Spot Trading API endpoints.

Generated from OpenAPI specs. Do not edit manually.
"""
from typing import Any

import msgspec

from binance._core.http import HTTPClient
from binance._schemas.spot import Order, QueryOrder, CancelOrderResult

# Pre-compiled decoders for performance
_order_decoder = msgspec.json.Decoder(Order)
_query_order_decoder = msgspec.json.Decoder(QueryOrder)
_query_order_list_decoder = msgspec.json.Decoder(list[QueryOrder])
_cancel_result_decoder = msgspec.json.Decoder(CancelOrderResult)


async def create_order(
    http: HTTPClient,
    symbol: str,
    side: str,
    type: str,
    quantity: str | None = None,
    quote_order_qty: str | None = None,
    price: str | None = None,
    time_in_force: str | None = None,
    new_client_order_id: str | None = None,
    stop_price: str | None = None,
    trailing_delta: int | None = None,
    iceberg_qty: str | None = None,
    new_order_resp_type: str | None = None,
) -> Order:
    """Create a new order.

    Weight: 1
    Requires: Signature (signed=True)

    Tip: Always provide `new_client_order_id` for idempotent order placement.
    If a network error occurs, you can safely retry with the same client ID -
    Binance will reject duplicates, preventing accidental double orders.

    Args:
        symbol: Trading pair (e.g., "BTCUSDT")
        side: Order side ("BUY" or "SELL")
        type: Order type ("LIMIT", "MARKET", etc.)
        quantity: Order quantity
        quote_order_qty: Quote order quantity (for MARKET orders)
        price: Order price (required for LIMIT orders)
        time_in_force: Time in force ("GTC", "IOC", "FOK")
        new_client_order_id: Unique client order ID for idempotency
        stop_price: Stop price for stop orders
        trailing_delta: Trailing delta for trailing stop orders
        iceberg_qty: Iceberg quantity
        new_order_resp_type: Response type ("ACK", "RESULT", "FULL")

    Returns:
        Order with order details (fields vary by response type)
    """
    params: dict[str, Any] = {
        "symbol": symbol,
        "side": side,
        "type": type,
    }
    if quantity is not None:
        params["quantity"] = quantity
    if quote_order_qty is not None:
        params["quoteOrderQty"] = quote_order_qty
    if price is not None:
        params["price"] = price
    if time_in_force is not None:
        params["timeInForce"] = time_in_force
    if new_client_order_id is not None:
        params["newClientOrderId"] = new_client_order_id
    if stop_price is not None:
        params["stopPrice"] = stop_price
    if trailing_delta is not None:
        params["trailingDelta"] = trailing_delta
    if iceberg_qty is not None:
        params["icebergQty"] = iceberg_qty
    if new_order_resp_type is not None:
        params["newOrderRespType"] = new_order_resp_type

    raw = await http.request_raw("POST", "/api/v3/order", signed=True, params=params)
    return _order_decoder.decode(raw)


async def create_test_order(
    http: HTTPClient,
    symbol: str,
    side: str,
    type: str,
    quantity: str | None = None,
    quote_order_qty: str | None = None,
    price: str | None = None,
    time_in_force: str | None = None,
    new_client_order_id: str | None = None,
    stop_price: str | None = None,
    new_order_resp_type: str | None = None,
) -> dict[str, Any]:
    """Test new order creation (does not place order).

    Weight: 1
    Requires: Signature (signed=True)

    Args:
        (Same as create_order)

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
    if quote_order_qty is not None:
        params["quoteOrderQty"] = quote_order_qty
    if price is not None:
        params["price"] = price
    if time_in_force is not None:
        params["timeInForce"] = time_in_force
    if new_client_order_id is not None:
        params["newClientOrderId"] = new_client_order_id
    if stop_price is not None:
        params["stopPrice"] = stop_price
    if new_order_resp_type is not None:
        params["newOrderRespType"] = new_order_resp_type

    return await http.request("POST", "/api/v3/order/test", signed=True, params=params)


async def get_order(
    http: HTTPClient,
    symbol: str,
    order_id: int | None = None,
    orig_client_order_id: str | None = None,
) -> QueryOrder:
    """Check an order's status.

    Weight: 4
    Requires: Signature (signed=True)

    Args:
        symbol: Trading pair
        order_id: Order ID (either this or orig_client_order_id required)
        orig_client_order_id: Original client order ID

    Returns:
        QueryOrder with full order details
    """
    params: dict[str, Any] = {"symbol": symbol}
    if order_id is not None:
        params["orderId"] = order_id
    if orig_client_order_id is not None:
        params["origClientOrderId"] = orig_client_order_id

    raw = await http.request_raw("GET", "/api/v3/order", signed=True, params=params)
    return _query_order_decoder.decode(raw)


async def cancel_order(
    http: HTTPClient,
    symbol: str,
    order_id: int | None = None,
    orig_client_order_id: str | None = None,
    new_client_order_id: str | None = None,
) -> CancelOrderResult:
    """Cancel an active order.

    Weight: 1
    Requires: Signature (signed=True)

    Args:
        symbol: Trading pair
        order_id: Order ID (either this or orig_client_order_id required)
        orig_client_order_id: Original client order ID
        new_client_order_id: New client order ID for the cancel

    Returns:
        CancelOrderResult with canceled order details
    """
    params: dict[str, Any] = {"symbol": symbol}
    if order_id is not None:
        params["orderId"] = order_id
    if orig_client_order_id is not None:
        params["origClientOrderId"] = orig_client_order_id
    if new_client_order_id is not None:
        params["newClientOrderId"] = new_client_order_id

    raw = await http.request_raw("DELETE", "/api/v3/order", signed=True, params=params)
    return _cancel_result_decoder.decode(raw)


async def get_open_orders(
    http: HTTPClient,
    symbol: str | None = None,
) -> list[QueryOrder]:
    """Get all open orders on a symbol or all symbols.

    Weight: 6 for single symbol, 80 for all

    Requires: Signature (signed=True)

    Args:
        symbol: Trading pair (optional)

    Returns:
        List of QueryOrder for open orders
    """
    params: dict[str, Any] = {}
    if symbol is not None:
        params["symbol"] = symbol

    raw = await http.request_raw("GET", "/api/v3/openOrders", signed=True, params=params)
    return _query_order_list_decoder.decode(raw)


async def get_all_orders(
    http: HTTPClient,
    symbol: str,
    order_id: int | None = None,
    start_time: int | None = None,
    end_time: int | None = None,
    limit: int = 500,
) -> list[QueryOrder]:
    """Get all account orders (active, canceled, filled).

    Weight: 20

    Requires: Signature (signed=True)

    Args:
        symbol: Trading pair
        order_id: Start from this order ID
        start_time: Start time in milliseconds
        end_time: End time in milliseconds
        limit: Max results (default 500, max 1000)

    Returns:
        List of QueryOrder
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

    raw = await http.request_raw("GET", "/api/v3/allOrders", signed=True, params=params)
    return _query_order_list_decoder.decode(raw)
