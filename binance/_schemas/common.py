"""Common types shared across all APIs.

This module defines:
- BaseStruct: Base class for all msgspec schemas
- Literal types: Type-safe enums without enum overhead
- Constants: Named values for Literals

Design decisions:
- Literal + Constants pattern for type safety AND performance
- rename="camel" for automatic snake_case ↔ camelCase
- frozen=True for immutability and hashability
- omit_defaults=True for smaller payloads
"""
from typing import Literal

import msgspec

# ============ Base Class ============


class BaseStruct(msgspec.Struct, rename="camel", frozen=True, omit_defaults=True):
    """Base class for all schemas.

    Features:
    - rename="camel": auto-convert snake_case ↔ camelCase
    - frozen=True: immutable, hashable, thread-safe
    - omit_defaults=True: skip None/default fields in serialization
    """

    pass


# ============ Order Side ============

OrderSide = Literal["BUY", "SELL"]

ORDER_SIDE_BUY: OrderSide = "BUY"
ORDER_SIDE_SELL: OrderSide = "SELL"


# ============ Order Type ============

OrderType = Literal[
    "LIMIT",
    "MARKET",
    "STOP_LOSS",
    "STOP_LOSS_LIMIT",
    "TAKE_PROFIT",
    "TAKE_PROFIT_LIMIT",
    "LIMIT_MAKER",
]

ORDER_TYPE_LIMIT: OrderType = "LIMIT"
ORDER_TYPE_MARKET: OrderType = "MARKET"
ORDER_TYPE_STOP_LOSS: OrderType = "STOP_LOSS"
ORDER_TYPE_STOP_LOSS_LIMIT: OrderType = "STOP_LOSS_LIMIT"
ORDER_TYPE_TAKE_PROFIT: OrderType = "TAKE_PROFIT"
ORDER_TYPE_TAKE_PROFIT_LIMIT: OrderType = "TAKE_PROFIT_LIMIT"
ORDER_TYPE_LIMIT_MAKER: OrderType = "LIMIT_MAKER"


# ============ Time In Force ============

TimeInForce = Literal["GTC", "IOC", "FOK"]

TIME_IN_FORCE_GTC: TimeInForce = "GTC"
TIME_IN_FORCE_IOC: TimeInForce = "IOC"
TIME_IN_FORCE_FOK: TimeInForce = "FOK"


# ============ Order Status ============

OrderStatus = Literal[
    "NEW",
    "PARTIALLY_FILLED",
    "FILLED",
    "CANCELED",
    "PENDING_CANCEL",
    "REJECTED",
    "EXPIRED",
]

ORDER_STATUS_NEW: OrderStatus = "NEW"
ORDER_STATUS_PARTIALLY_FILLED: OrderStatus = "PARTIALLY_FILLED"
ORDER_STATUS_FILLED: OrderStatus = "FILLED"
ORDER_STATUS_CANCELED: OrderStatus = "CANCELED"
ORDER_STATUS_REJECTED: OrderStatus = "REJECTED"
ORDER_STATUS_EXPIRED: OrderStatus = "EXPIRED"


# ============ Kline Interval ============

Interval = Literal[
    "1s",
    "1m",
    "3m",
    "5m",
    "15m",
    "30m",
    "1h",
    "2h",
    "4h",
    "6h",
    "8h",
    "12h",
    "1d",
    "3d",
    "1w",
    "1M",
]

INTERVAL_1S: Interval = "1s"
INTERVAL_1M: Interval = "1m"
INTERVAL_3M: Interval = "3m"
INTERVAL_5M: Interval = "5m"
INTERVAL_15M: Interval = "15m"
INTERVAL_30M: Interval = "30m"
INTERVAL_1H: Interval = "1h"
INTERVAL_2H: Interval = "2h"
INTERVAL_4H: Interval = "4h"
INTERVAL_6H: Interval = "6h"
INTERVAL_8H: Interval = "8h"
INTERVAL_12H: Interval = "12h"
INTERVAL_1D: Interval = "1d"
INTERVAL_3D: Interval = "3d"
INTERVAL_1W: Interval = "1w"
INTERVAL_1MONTH: Interval = "1M"
