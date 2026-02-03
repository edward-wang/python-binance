# Section 5: Schemas (`_schemas/`)

High-performance request/response models using msgspec.

## Structure

```
binance/_schemas/
├── __init__.py
├── common.py          # Base class, Literals + Constants
├── spot.py            # Spot request/response (generated)
├── futures.py         # Futures request/response (generated)
├── margin.py          # Margin request/response (generated)
└── ws.py              # WebSocket Tagged Unions (future)
```

## Why msgspec?

| Aspect | Pydantic v2 | msgspec |
|--------|-------------|---------|
| Serialization | ~1M ops/sec | ~5M ops/sec |
| Memory | Higher | Lower (`__slots__` built-in) |
| Validation | Rich, detailed | Fast, essential |
| JSON parsing | Separate step | Built-in `msgspec.json` |

## `_schemas/common.py` (hand-written)

```python
"""Common types shared across all APIs"""
import msgspec
from typing import Literal

# ============ Base Class ============

class BaseStruct(msgspec.Struct, rename="camel", frozen=True, omit_defaults=True):
    """Base class for all schemas.

    - rename="camel": auto-convert snake_case ↔ camelCase
    - frozen=True: immutable, hashable
    - omit_defaults=True: skip None/default fields in serialization
    """
    pass

# ============ Order Side ============

OrderSide = Literal["BUY", "SELL"]

ORDER_SIDE_BUY: OrderSide = "BUY"
ORDER_SIDE_SELL: OrderSide = "SELL"

# ============ Order Type ============

OrderType = Literal[
    "LIMIT", "MARKET", "STOP_LOSS", "STOP_LOSS_LIMIT",
    "TAKE_PROFIT", "TAKE_PROFIT_LIMIT", "LIMIT_MAKER"
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

# ============ Kline Interval ============

Interval = Literal[
    "1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h",
    "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"
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
```

## `_schemas/spot.py` (generated)

```python
"""Spot API schemas - Generated from OpenXAPI specs"""
from typing import Annotated
import msgspec
from binance._schemas.common import BaseStruct, OrderSide, OrderType

# ============ Request Schemas ============

class KlineRequest(BaseStruct):
    """Request parameters for get_klines endpoint."""
    symbol: Annotated[str, msgspec.Meta(description="Trading pair, e.g. BTCUSDT")]
    interval: Annotated[str, msgspec.Meta(description="Kline interval, e.g. 1h")]
    limit: Annotated[int, msgspec.Meta(description="Number of results")] = 500
    start_time: Annotated[int | None, msgspec.Meta(description="Start time in ms")] = None
    end_time: Annotated[int | None, msgspec.Meta(description="End time in ms")] = None

class OrderRequest(BaseStruct):
    """Request parameters for create_order endpoint."""
    symbol: Annotated[str, msgspec.Meta(description="Trading pair")]
    side: Annotated[OrderSide, msgspec.Meta(description="Order side: BUY or SELL")]
    type: Annotated[OrderType, msgspec.Meta(description="Order type")]
    quantity: Annotated[str | None, msgspec.Meta(description="Order quantity")] = None
    quote_order_qty: Annotated[str | None, msgspec.Meta(description="Quote quantity")] = None
    price: Annotated[str | None, msgspec.Meta(description="Limit price")] = None
    time_in_force: Annotated[str | None, msgspec.Meta(description="Time in force")] = None
    new_client_order_id: Annotated[str | None, msgspec.Meta(description="Client order ID")] = None

# ============ Response Schemas ============

class Kline(BaseStruct):
    """Kline/candlestick data."""
    open_time: int
    open: float          # float for fast calculations
    high: float
    low: float
    close: float
    volume: float
    close_time: int
    quote_volume: float
    trades: int
    taker_buy_base: float
    taker_buy_quote: float

class OrderResponse(BaseStruct):
    """Response from create_order endpoint."""
    symbol: str
    order_id: int
    order_list_id: int
    client_order_id: str
    transact_time: int
    price: str           # Keep as string (from API)
    orig_qty: str
    executed_qty: str
    status: str
    type: str
    side: str
```

## Numeric Type Strategy

**For HFT performance, use `float` for market data, `str` for orders.**

| Data Type | Use Case | Type |
|-----------|----------|------|
| Market data (klines, depth, trades) | `float` | Fast parsing & calculation |
| Strategy calculations | `float` | Hardware accelerated |
| Order request params | `str` | API precision requirement |
| Order response values | `str` | Keep as returned |

### Float → String at Order Time

```python
from binance._core.formatters import format_price, format_quantity

# Strategy calculation (all float, fast)
current_price = kline.close  # float
target_price = current_price * 1.001  # float

# Only at order submission (format once)
order = await client.create_order(
    symbol="BTCUSDT",
    side=ORDER_SIDE_BUY,
    type=ORDER_TYPE_LIMIT,
    price=format_price(target_price, tick_size=0.01),      # "50050.05"
    quantity=format_quantity(0.001234, step_size=0.00001), # "0.00123"
)
```

## `_schemas/ws.py` (future - Tagged Unions)

For WebSocket message handling with automatic dispatch.

```python
"""WebSocket message schemas using Tagged Unions.

msgspec auto-dispatches based on "e" (event type) field at C level.
"""
import msgspec
from typing import Union

# ============ WebSocket Base ============

class WsBaseStruct(msgspec.Struct, rename="camel", frozen=True):
    """Base for WebSocket messages."""
    pass

# ============ Kline Event ============

class WsKlineData(WsBaseStruct):
    """Kline data nested in WsKlineEvent."""
    t: int           # kline start time
    T: int           # kline close time
    s: str           # symbol
    i: str           # interval
    o: float         # open
    h: float         # high
    l: float         # low
    c: float         # close
    v: float         # volume
    x: bool          # is kline closed

class WsKlineEvent(msgspec.Struct, tag_field="e", tag="kline"):
    """Kline/candlestick update event."""
    s: str           # symbol
    k: WsKlineData   # kline data

# ============ Depth Event ============

class WsDepthEvent(msgspec.Struct, tag_field="e", tag="depthUpdate"):
    """Order book depth update event."""
    s: str           # symbol
    U: int           # first update ID
    u: int           # final update ID
    b: list[list]    # bids
    a: list[list]    # asks

# ============ Trade Event ============

class WsTradeEvent(msgspec.Struct, tag_field="e", tag="trade"):
    """Individual trade event."""
    s: str           # symbol
    p: float         # price
    q: float         # quantity
    T: int           # trade time
    m: bool          # is buyer maker

# ============ Tagged Union ============

SpotWsMessage = Union[WsKlineEvent, WsDepthEvent, WsTradeEvent]

# Pre-compiled decoder for hot path
spot_ws_decoder = msgspec.json.Decoder(SpotWsMessage)
```

## Pre-compiled Decoders

```python
# binance/_core/decoders.py
"""Pre-compiled msgspec decoders for high-frequency endpoints."""
import msgspec
from typing import TypeVar

T = TypeVar("T")

_DECODERS: dict[type, msgspec.json.Decoder] = {}

def get_decoder(schema_type: type[T]) -> msgspec.json.Decoder[T]:
    """Get or create a pre-compiled decoder for the given type."""
    if schema_type not in _DECODERS:
        _DECODERS[schema_type] = msgspec.json.Decoder(schema_type)
    return _DECODERS[schema_type]
```

## Key Design Decisions

| Decision | Choice | Benefit |
|----------|--------|---------|
| Base class | `msgspec.Struct` with `rename="camel"` | Auto snake_case ↔ camelCase |
| Immutability | `frozen=True` | Hashable, thread-safe |
| Enums | `Literal` + Constants | Type safety + performance |
| Field naming | All snake_case | Pythonic, consistent |
| Numeric types | `float` for market data, `str` for orders | HFT performance |
| Decoders | Centralized, pre-compiled | Faster hot-path parsing |
| Serialization | `omit_defaults=True` | Smaller payloads |
| Descriptions | `Annotated[type, msgspec.Meta(...)]` | Dual purpose: docstring + AI schema |
| WebSocket | Tagged Unions | C-level dispatch, type-safe |
