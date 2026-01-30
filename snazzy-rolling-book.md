# Python-Binance AI-Friendly Restructuring Plan

## Problem Summary

| Issue | Current State | Impact |
|-------|--------------|--------|
| `client.py` | 17,534 lines, 806 methods | Exceeds AI context limits |
| Code duplication | Same logic in 3 places | Maintenance nightmare |
| Sync mixins | 13,866 lines of dead code | Confusion, wasted space |
| Auto-generated stubs | 500+ placeholder methods | Unmaintainable |

## Architecture Design Principles

This restructuring follows three core principles to ensure AI-friendly development:

### 1. Schema-Driven Development (Strong Typing)

| Aspect | Implementation | AI Benefit |
|--------|----------------|------------|
| **Input** | Pydantic request models with validators | Eliminate `**kwargs`, catch typos at code generation |
| **Output** | Pydantic response models with field docs | AI knows exact field names and types via static analysis |
| **IDE** | Auto-generated `.pyi` stubs | 100% parameter autocompletion |

### 2. Physical & Logical Atomicity

| Aspect | Implementation | AI Benefit |
|--------|----------------|------------|
| **File size** | All modules < 300 lines | Fits in AI context window |
| **Separation** | One file per API domain (spot, futures, etc.) | AI can fully understand each module |
| **Dependencies** | Unidirectional import flow | No confusion from circular references |

### 3. Standardized Layered Contract

| Aspect | Implementation | AI Benefit |
|--------|----------------|------------|
| **Exceptions** | Domain-specific error classes | AI can write precise error handling logic |
| **Metadata** | APIResponse carries rate limit info | Middleware can implement smart retry |
| **Mapping** | Error code → Exception type mapping | Predictable error semantics |

## Target Architecture

```
binance/
├── __init__.py                    # Public exports (unchanged)
├── client.py                      # Thin sync client (~150 lines)
├── client.pyi                     # Type stubs for Client (auto-generated)
├── async_client.py                # Thin async client (~150 lines)
├── async_client.pyi               # Type stubs for AsyncClient (auto-generated)
│
├── _core/                         # Internal infrastructure
│   ├── __init__.py
│   ├── base.py                    # Constants, config (~300 lines)
│   ├── auth.py                    # Signature generation (~150 lines)
│   ├── request_sync.py            # Sync HTTP transport (~150 lines)
│   ├── request_async.py           # Async HTTP transport (~150 lines)
│   ├── response.py                # APIResponse wrapper with metadata (~100 lines)
│   └── exceptions.py              # Standardized exception hierarchy (~200 lines)
│
├── _endpoints/                    # Declarative endpoint definitions
│   ├── __init__.py
│   ├── _base.py                   # Endpoint descriptor class (~200 lines)
│   ├── _generator.py              # Sync/async method generator + pyi export (~200 lines)
│   ├── spot/                      # ~100 endpoints
│   │   ├── general.py             # ping, time, exchange_info
│   │   ├── market.py              # depth, trades, klines, ticker
│   │   ├── trade.py               # orders, OCO, SOR
│   │   └── account.py             # account info, balances
│   ├── margin/                    # ~50 endpoints
│   ├── futures_um/                # ~100 endpoints
│   ├── futures_cm/                # ~50 endpoints
│   ├── options/                   # ~40 endpoints
│   ├── portfolio/                 # ~80 endpoints (PAPI)
│   ├── wallet/                    # ~50 endpoints (SAPI)
│   └── services/                  # ~50 endpoints (gift card, pay, etc.)
│
├── _schemas/                      # Pydantic request/response models
│   ├── __init__.py
│   ├── _base.py                   # Base schema classes (~100 lines)
│   ├── spot.py                    # Spot API schemas (~300 lines)
│   ├── futures.py                 # Futures API schemas (~300 lines)
│   └── common.py                  # Shared types (OrderSide, OrderType, etc.)
│
├── _protocols/                    # Capability protocols for modularity
│   ├── __init__.py
│   ├── market.py                  # KlineProvider, TickerProvider, DepthProvider
│   ├── trade.py                   # OrderExecutor, PositionManager
│   └── account.py                 # BalanceProvider, TransferExecutor
│
├── _mixins/                       # Business logic (pagination, generators)
│   ├── klines.py                  # Historical klines (~250 lines)
│   └── generators.py              # Trade iterators (~150 lines)
│
├── exceptions.py                  # Re-export from _core/exceptions.py (backward compat)
├── enums.py                       # Keep existing
└── ws/                            # Keep existing WebSocket structure
```

## Module Dependency Rules

Unidirectional dependency flow to prevent circular imports:

```
┌─────────────────────────────────────────────────────────────┐
│                      client.py / async_client.py            │
│                         (Public Interface)                  │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                        _protocols/                          │
│               (Capability Protocols - Optional)             │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                        _endpoints/                          │
│               (Declarative Endpoint Definitions)            │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                         _schemas/                           │
│              (Pydantic Request/Response Models)             │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                          _core/                             │
│    (Base Infrastructure: auth, request, response, errors)   │
└─────────────────────────────────────────────────────────────┘

RULE: Each layer can only import from layers BELOW it.
      No upward or lateral imports allowed.
```

## Key Design: Declarative Endpoints

Define each endpoint ONCE, generate both sync and async methods:

```python
# binance/_endpoints/_base.py
from typing import Type, Any, List, Optional
from dataclasses import dataclass, field

@dataclass
class Param:
    name: str
    type_hint: Type                # str, int, float, bool, Decimal
    required: bool = True
    default: Any = None
    doc: str = ""                  # Parameter description
    
    @property
    def json_type(self) -> str:
        """For AI tool schema export"""
        mapping = {str: "string", int: "integer", float: "number", bool: "boolean"}
        return mapping.get(self.type_hint, "string")

@dataclass
class Endpoint:
    name: str                      # Method name: get_klines
    path: str                      # API path: "klines"
    method: str = "get"            # HTTP method
    request_type: RequestType      # API, MARGIN, FUTURES_UM, etc.
    signed: bool = False
    version: int = 1
    params: List[Param] = field(default_factory=list)
    doc: str = ""                  # Method description
    api_doc_url: str = ""          # Binance API documentation URL
    
    # Type information for schema generation
    request_schema: Optional[Type] = None   # Pydantic model for request validation
    response_schema: Optional[Type] = None  # Pydantic model for response parsing
    return_type: str = "dict"               # For .pyi generation (fallback)
    
    # Weight information for rate limiting
    weight: int = 1                         # API weight cost
    weight_param: Optional[str] = None      # Param that affects weight (e.g., "limit")

# binance/_endpoints/spot/market.py
from binance._schemas.spot import KlineRequest, KlineResponse

get_klines = Endpoint(
    name="get_klines",
    path="klines",
    request_type=RequestType.API,
    params=[
        Param("symbol", str, required=True, doc="Trading pair, e.g., BTCUSDT"),
        Param("interval", str, required=True, doc="Kline interval, e.g., 1h, 1d"),
        Param("limit", int, required=False, default=500, doc="Number of results (max 1000)"),
        Param("startTime", int, required=False, doc="Start time in milliseconds"),
        Param("endTime", int, required=False, doc="End time in milliseconds"),
    ],
    doc="Get kline/candlestick bars for a symbol.",
    api_doc_url="https://developers.binance.com/docs/binance-spot-api-docs/rest-api#klinecandlestick-data",
    request_schema=KlineRequest,
    response_schema=KlineResponse,
    return_type="List[Kline]",
    weight=2,
    weight_param="limit",
)

# binance/_endpoints/_generator.py
def generate_sync_method(ep: Endpoint):
    def method(self, **params):
        # Validate params using Pydantic schema if available
        if ep.request_schema:
            validated = ep.request_schema(**params)
            kwargs = validated.model_dump(exclude_none=True)
        else:
            kwargs = ep.build_request_kwargs(**params)
        
        response = getattr(self, REQUEST_MAP[ep.request_type])(
            ep.method, ep.path, signed=ep.signed, **kwargs
        )
        
        # Parse response using schema if available
        if ep.response_schema and isinstance(response.data, (dict, list)):
            return ep.response_schema.model_validate(response.data)
        return response
    
    # Set method metadata for debugging and introspection
    method.__name__ = ep.name
    method.__qualname__ = f"Client.{ep.name}"
    method.__doc__ = _build_docstring(ep)
    method.__module__ = "binance.client"
    method._endpoint = ep  # Preserve endpoint reference for debugging
    
    return method

def generate_async_method(ep: Endpoint):
    async def method(self, **params):
        # Validate params using Pydantic schema if available
        if ep.request_schema:
            validated = ep.request_schema(**params)
            kwargs = validated.model_dump(exclude_none=True)
        else:
            kwargs = ep.build_request_kwargs(**params)
        
        response = await getattr(self, REQUEST_MAP[ep.request_type])(
            ep.method, ep.path, signed=ep.signed, **kwargs
        )
        
        # Parse response using schema if available
        if ep.response_schema and isinstance(response.data, (dict, list)):
            return ep.response_schema.model_validate(response.data)
        return response
    
    # Set method metadata for debugging and introspection
    method.__name__ = ep.name
    method.__qualname__ = f"AsyncClient.{ep.name}"
    method.__doc__ = _build_docstring(ep)
    method.__module__ = "binance.async_client"
    method._endpoint = ep
    
    return method
```

## Strong Typing & Schema Validation

### Design Philosophy: Schema-Driven Development

In AI collaboration environments, ambiguous type inference is the primary cause of logic hallucinations. This project adopts a **Schema-Driven Development** approach to ensure AI agents can write correct code through static analysis alone.

### Request Schema (Input Validation)

Use Pydantic models to define strongly-typed request parameters:

```python
# binance/_schemas/spot.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from decimal import Decimal

class KlineRequest(BaseModel):
    """Request schema for get_klines endpoint"""
    symbol: str = Field(..., description="Trading pair, e.g., BTCUSDT")
    interval: Literal["1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", 
                      "6h", "8h", "12h", "1d", "3d", "1w", "1M"] = Field(
        ..., description="Kline interval"
    )
    limit: int = Field(default=500, ge=1, le=1000, description="Number of results")
    startTime: Optional[int] = Field(default=None, description="Start time in ms")
    endTime: Optional[int] = Field(default=None, description="End time in ms")
    
    @field_validator("symbol")
    @classmethod
    def symbol_uppercase(cls, v: str) -> str:
        return v.upper()

class OrderRequest(BaseModel):
    """Request schema for create_order endpoint"""
    symbol: str = Field(..., description="Trading pair")
    side: Literal["BUY", "SELL"] = Field(..., description="Order side")
    type: Literal["LIMIT", "MARKET", "STOP_LOSS", "STOP_LOSS_LIMIT", 
                  "TAKE_PROFIT", "TAKE_PROFIT_LIMIT", "LIMIT_MAKER"] = Field(
        ..., description="Order type"
    )
    quantity: Optional[Decimal] = Field(default=None, description="Order quantity")
    quoteOrderQty: Optional[Decimal] = Field(default=None, description="Quote quantity")
    price: Optional[Decimal] = Field(default=None, description="Limit price")
    timeInForce: Optional[Literal["GTC", "IOC", "FOK"]] = Field(
        default=None, description="Time in force"
    )
    newClientOrderId: Optional[str] = Field(default=None, description="Client order ID")
```

### Response Schema (Output Parsing)

Define structured response models for AI and IDE comprehension:

```python
# binance/_schemas/spot.py
from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal

class Kline(BaseModel):
    """Single kline/candlestick data"""
    open_time: int
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    close_time: int
    quote_volume: Decimal
    trades: int
    taker_buy_base: Decimal
    taker_buy_quote: Decimal
    
    @classmethod
    def from_list(cls, data: list) -> "Kline":
        """Parse from Binance's list format"""
        return cls(
            open_time=data[0], open=Decimal(data[1]), high=Decimal(data[2]),
            low=Decimal(data[3]), close=Decimal(data[4]), volume=Decimal(data[5]),
            close_time=data[6], quote_volume=Decimal(data[7]), trades=data[8],
            taker_buy_base=Decimal(data[9]), taker_buy_quote=Decimal(data[10]),
        )

class KlineResponse(BaseModel):
    """Response schema for get_klines endpoint"""
    __root__: List[Kline]
    
    @classmethod
    def model_validate(cls, data: list) -> List[Kline]:
        return [Kline.from_list(k) for k in data]

class OrderResponse(BaseModel):
    """Response schema for create_order endpoint"""
    symbol: str
    orderId: int
    orderListId: int
    clientOrderId: str
    transactTime: int
    price: Decimal
    origQty: Decimal
    executedQty: Decimal
    cummulativeQuoteQty: Decimal
    status: str
    timeInForce: str
    type: str
    side: str
    fills: Optional[List[dict]] = None
```

### Backward Compatibility Strategy

Schema validation is **opt-in** to maintain backward compatibility:

```python
# Option 1: Raw dict (existing behavior)
klines = client.get_klines(symbol="BTCUSDT", interval="1h")
# Returns: List[list] - raw API response

# Option 2: Typed response (new behavior, when response_schema is set)
klines = client.get_klines(symbol="BTCUSDT", interval="1h")
# Returns: List[Kline] - parsed Pydantic models

# Accessing raw data when needed
response = client.get_klines(symbol="BTCUSDT", interval="1h", raw=True)
# Returns: APIResponse with .data attribute
```

---

## Error Handling & Metadata Contract

### Design Philosophy: Standardized Layered Contract

The wrapper layer and middleware layer require a highly predictable handoff point. This is achieved through:
1. **Standardized Exception Hierarchy** - Semantic error mapping
2. **Metadata Passthrough Mechanism** - Rate limit information preservation

### Exception Hierarchy

```python
# binance/_core/exceptions.py
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class APIResponse:
    """Wrapper preserving response metadata for middleware decisions"""
    data: Any                               # Parsed JSON response
    status_code: int                        # HTTP status code
    used_weight: Optional[int] = None       # X-MBX-USED-WEIGHT-*
    used_weight_1m: Optional[int] = None    # X-MBX-USED-WEIGHT-1M
    order_count_10s: Optional[int] = None   # X-MBX-ORDER-COUNT-10S
    order_count_1m: Optional[int] = None    # X-MBX-ORDER-COUNT-1M
    order_count_1d: Optional[int] = None    # X-MBX-ORDER-COUNT-1D
    retry_after: Optional[int] = None       # Retry-After header (seconds)
    server_time: Optional[int] = None       # Server timestamp
    
    def __getitem__(self, key):
        """Dict-like access for backward compatibility"""
        return self.data[key]
    
    def __iter__(self):
        """Iterate over data for backward compatibility"""
        return iter(self.data)


class BinanceError(Exception):
    """Base exception for all Binance errors"""
    pass


class BinanceAPIError(BinanceError):
    """API returned an error response"""
    def __init__(self, code: int, message: str, response: Optional[APIResponse] = None):
        self.code = code
        self.message = message
        self.response = response
        super().__init__(f"APIError(code={code}): {message}")


class RateLimitExceeded(BinanceAPIError):
    """
    HTTP 429 or error code -1015: Too many requests.
    
    Middleware can use `retry_after` and `used_weight` to implement
    exponential backoff with precise timing.
    """
    def __init__(self, code: int, message: str, response: Optional[APIResponse] = None):
        super().__init__(code, message, response)
        self.retry_after = response.retry_after if response else None
        self.used_weight = response.used_weight if response else None


class IPBanned(BinanceAPIError):
    """
    HTTP 418: IP has been auto-banned for repeated rate limit violations.
    Requires waiting for ban expiry (usually 2-3 minutes).
    """
    pass


class AuthenticationFailed(BinanceAPIError):
    """
    Error codes -2014, -2015: Invalid API key, signature, or timestamp.
    Should NOT be retried - requires user intervention.
    """
    pass


class InsufficientBalance(BinanceAPIError):
    """
    Error code -2010: Insufficient balance for the requested operation.
    Should NOT be retried without user depositing funds.
    """
    pass


class OrderNotFound(BinanceAPIError):
    """
    Error code -2013: Order does not exist.
    May occur for cancelled orders or wrong orderId.
    """
    pass


class InvalidSymbol(BinanceAPIError):
    """
    Error code -1121: Invalid symbol.
    Symbol may be delisted or incorrectly formatted.
    """
    pass


class OrderWouldTriggerImmediately(BinanceAPIError):
    """
    Error code -2021: Order would immediately trigger.
    Stop order price constraints violated.
    """
    pass
```

### Error Code Mapping

```python
# binance/_core/exceptions.py
ERROR_CODE_MAP: Dict[int, type] = {
    # Rate limiting
    -1003: RateLimitExceeded,      # Too many requests
    -1015: RateLimitExceeded,      # Too many orders
    
    # Authentication
    -2014: AuthenticationFailed,   # API-key format invalid
    -2015: AuthenticationFailed,   # Invalid API-key, IP, or permissions
    
    # Order errors
    -2010: InsufficientBalance,    # Insufficient balance
    -2013: OrderNotFound,          # Order does not exist
    -2021: OrderWouldTriggerImmediately,
    
    # Symbol errors
    -1121: InvalidSymbol,          # Invalid symbol
}

HTTP_STATUS_MAP: Dict[int, type] = {
    418: IPBanned,
    429: RateLimitExceeded,
}

def raise_for_error(response: APIResponse) -> None:
    """Convert API error to appropriate exception type"""
    if response.status_code in HTTP_STATUS_MAP:
        exc_class = HTTP_STATUS_MAP[response.status_code]
        raise exc_class(
            code=response.status_code,
            message=f"HTTP {response.status_code}",
            response=response
        )
    
    if isinstance(response.data, dict) and "code" in response.data:
        code = response.data["code"]
        message = response.data.get("msg", "Unknown error")
        exc_class = ERROR_CODE_MAP.get(code, BinanceAPIError)
        raise exc_class(code=code, message=message, response=response)
```

### Metadata Extraction

```python
# binance/_core/request_sync.py
def _parse_response_headers(headers: dict) -> dict:
    """Extract rate limit metadata from response headers"""
    return {
        "used_weight": _parse_int(headers.get("X-MBX-USED-WEIGHT")),
        "used_weight_1m": _parse_int(headers.get("X-MBX-USED-WEIGHT-1M")),
        "order_count_10s": _parse_int(headers.get("X-MBX-ORDER-COUNT-10S")),
        "order_count_1m": _parse_int(headers.get("X-MBX-ORDER-COUNT-1M")),
        "order_count_1d": _parse_int(headers.get("X-MBX-ORDER-COUNT-1D")),
        "retry_after": _parse_int(headers.get("Retry-After")),
        "server_time": _parse_int(headers.get("X-MBX-SERVER-TIME")),
    }

def _request(self, method: str, path: str, **kwargs) -> APIResponse:
    """Execute HTTP request and return response with metadata"""
    response = self.session.request(method, url, **kwargs)
    metadata = _parse_response_headers(response.headers)
    
    api_response = APIResponse(
        data=response.json() if response.content else None,
        status_code=response.status_code,
        **metadata
    )
    
    raise_for_error(api_response)
    return api_response
```

### Middleware Integration Example

```python
# Example: Rate Limiter middleware using metadata
class RateLimiter:
    def __init__(self, client: Client):
        self.client = client
        self.current_weight = 0
        self.weight_limit = 1200  # Default Binance limit per minute
    
    def execute(self, endpoint: Endpoint, **params) -> APIResponse:
        # Pre-check: estimate weight cost
        estimated_weight = endpoint.weight
        if self.current_weight + estimated_weight > self.weight_limit:
            sleep_time = 60 - (time.time() % 60)
            time.sleep(sleep_time)
            self.current_weight = 0
        
        try:
            response = getattr(self.client, endpoint.name)(**params)
            # Update weight from actual response metadata
            if response.used_weight:
                self.current_weight = response.used_weight
            return response
            
        except RateLimitExceeded as e:
            # Use retry_after from exception for precise backoff
            if e.retry_after:
                time.sleep(e.retry_after)
            else:
                time.sleep(60)  # Default fallback
            return self.execute(endpoint, **params)  # Retry
```

---

## Debugging & Introspection

### Problem: Dynamic Methods Have Poor Stack Traces

Without setting metadata, all 806 dynamically generated methods show the same unhelpful name in stack traces:

```
# Before: Impossible to identify which API failed
Traceback:
  File "_generator.py", line 17, in method   # ← Which method?!
    return self._request(...)
BinanceAPIException: Invalid symbol
```

### Solution: Set Function Metadata

Each generated method must have proper `__name__`, `__doc__`, and `__qualname__`:

```python
def _build_docstring(ep: Endpoint) -> str:
    """Generate docstring from endpoint definition"""
    lines = [ep.doc, ""]
    
    if ep.params:
        lines.append("Args:")
        for p in ep.params:
            required = " (required)" if p.required else ""
            default = "" if p.required else f", default={p.default!r}"
            lines.append(f"    {p.name}: {p.type_hint.__name__}{required}{default}")
            if p.doc:
                lines.append(f"        {p.doc}")
    
    if ep.api_doc_url:
        lines.extend(["", f"API Doc: {ep.api_doc_url}"])
    
    return "\n".join(lines)
```

### Result

```
# After: Clear identification
Traceback:
  File "_generator.py", line 17, in get_klines   # ← Now we know!
    return self._request(...)
BinanceAPIException: Invalid symbol

# help() works properly
>>> help(client.get_klines)
get_klines(symbol, interval, limit=500, ...)
    Get kline/candlestick bars for a symbol.
    
    Args:
        symbol: str (required)
        interval: str (required)
        limit: int, default=500
    
    API Doc: https://developers.binance.com/docs/...

# Debugging: access original endpoint definition
>>> client.get_klines._endpoint.path
'klines'
```

## Type System & AI Compatibility

### Problem: Dynamic Methods Lose Type Information

Dynamically generated methods use `**params`, making IDE autocompletion and AI comprehension impossible:

```python
client.get_klines(???)  # IDE has no idea what parameters are available
```

### Solution 1: Auto-generated Type Stubs (.pyi)

Generate `.pyi` stub files from `Endpoint` definitions for IDE support and AI comprehension:

```python
# binance/_endpoints/_generator.py (extended)
def generate_pyi(endpoints: List[Endpoint], class_name: str) -> str:
    """Generate .pyi stub file from endpoint definitions"""
    lines = ["from typing import List, Optional, Literal, Dict, Any", ""]
    lines.append(f"class {class_name}:")
    
    for ep in endpoints:
        params = ["self"]
        for p in ep.params:
            hint = f"{p.name}: {p.type_hint}"
            if not p.required:
                hint += f" = {p.default!r}"
            params.append(hint)
        
        lines.append(f"    def {ep.name}({', '.join(params)}) -> {ep.return_type}: ...")
    
    return "\n".join(lines)
```

Generated stub example (`client.pyi`):

```python
from typing import List, Optional, Literal, Dict, Any

class Client:
    def get_klines(
        self,
        symbol: str,
        interval: Literal["1m", "5m", "15m", "1h", "4h", "1d"],
        limit: int = 500,
        startTime: Optional[int] = None,
        endTime: Optional[int] = None,
    ) -> List[List]: ...
    
    def futures_create_order(
        self,
        symbol: str,
        side: Literal["BUY", "SELL"],
        type: Literal["LIMIT", "MARKET", "STOP"],
        quantity: Optional[float] = None,
        price: Optional[float] = None,
    ) -> Dict[str, Any]: ...
```

### Solution 2: Capability Protocols

Define protocols for modular, testable code that doesn't depend on concrete `Client` class:

```python
# binance/_protocols/market.py
from typing import Protocol, List

class KlineProvider(Protocol):
    """Any object that can provide kline data"""
    def get_klines(self, symbol: str, interval: str, limit: int = 500) -> List[list]: ...

class TickerProvider(Protocol):
    """Any object that can provide ticker data"""
    def get_ticker(self, symbol: str) -> dict: ...
```

Usage in user code:

```python
# User's strategy code - depends on capability, not concrete class
def run_backtest(data_source: KlineProvider, symbol: str):
    klines = data_source.get_klines(symbol, "1h", limit=1000)
    # ... strategy logic

# Works with real API
run_backtest(Client(key, secret), "BTCUSDT")

# Works with CSV backtest data
run_backtest(CSVDataSource("btc_2024.csv"), "BTCUSDT")

# Works with mock data for testing
run_backtest(MockDataSource(), "BTCUSDT")
```

### Solution 3: AI Tool Schema Export

Extend `Endpoint` to export OpenAI function / Claude tool schemas:

```python
@dataclass
class Endpoint:
    # ... existing fields ...
    
    def to_tool_schema(self) -> dict:
        """Export as OpenAI function / Claude tool schema"""
        return {
            "name": self.name,
            "description": self.doc,
            "parameters": {
                "type": "object",
                "properties": {
                    p.name: {"type": p.json_type, "description": p.doc}
                    for p in self.params
                },
                "required": [p.name for p in self.params if p.required]
            }
        }

# Export all endpoints as tool schemas
def export_all_tools() -> List[dict]:
    return [ep.to_tool_schema() for ep in all_endpoints]
```

## Branch Strategy & Release Plan

### Git Branch Structure

```
main (stable release)
  │
  └── feature/declarative-endpoints (main development branch)
        │
        ├── phase-1-foundation
        ├── phase-2-spot
        ├── phase-3-derivatives
        ├── phase-4-margin-sapi
        └── phase-5-replacement
```

### Workflow

1. **Create main development branch**
   ```bash
   git checkout -b feature/declarative-endpoints
   ```

2. **For each phase, create a sub-branch**
   ```bash
   git checkout feature/declarative-endpoints
   git checkout -b phase-1-foundation
   # ... work on phase 1 ...
   git checkout feature/declarative-endpoints
   git merge phase-1-foundation
   ```

3. **Sync upstream updates regularly**
   ```bash
   git checkout main
   git pull origin main
   git checkout feature/declarative-endpoints
   git merge main  # Resolve conflicts if any
   ```

4. **Merge to main only when all phases complete**
   ```bash
   git checkout main
   git merge feature/declarative-endpoints
   ```

### Version Release Strategy

| Phase Complete | Version Tag | Description |
|----------------|-------------|-------------|
| Phase 1 | `v2.1.0-alpha.1` | Core infrastructure ready |
| Phase 2 | `v2.1.0-alpha.2` | Spot API migrated |
| Phase 3 | `v2.1.0-alpha.3` | Derivatives migrated |
| Phase 4 | `v2.1.0-beta.1` | All APIs migrated, ready for testing |
| Phase 5 | `v2.1.0` | Full release |

**Benefits:**
- `main` branch stays stable for production users
- Early adopters can test alpha/beta versions
- Issues discovered early have limited impact
- Clear rollback path if critical bugs found

## Implementation Phases

### Phase 1: Foundation (Week 1-2)
**Create core infrastructure and endpoint system**

1. Create `binance/_core/` directory:
   - `base.py` - Extract constants from `base_client.py` (lines 22-156)
   - `auth.py` - Extract auth from `base_client.py` (lines 157-250)
   - `request_sync.py` - Refactor from `client_core.py` with metadata extraction
   - `request_async.py` - Refactor from `async_client_core.py` with metadata extraction
   - `response.py` - APIResponse dataclass with metadata fields
   - `exceptions.py` - Standardized exception hierarchy with error code mapping

2. Create `binance/_endpoints/` directory:
   - `_base.py` - Endpoint and Param dataclasses, RequestType enum
   - `_generator.py` - `generate_sync_method()`, `generate_async_method()`, `bind_endpoints_to_class()`
   - `_generator.py` - Add `generate_pyi()` function for type stub generation
   - `_generator.py` - Add `to_tool_schema()` method to Endpoint for AI tool export

3. Create `binance/_schemas/` directory:
   - `_base.py` - Base schema classes and common validators
   - `common.py` - Shared types (OrderSide, OrderType, Interval enums)
   - `spot.py` - Spot API request/response schemas (KlineRequest, OrderRequest, etc.)

4. Create first endpoint module:
   - `spot/general.py` - ping, get_server_time, get_exchange_info (~10 endpoints)

5. Create proof-of-concept thin client that works alongside existing client

6. Create `binance/_protocols/` directory:
   - `market.py` - KlineProvider, TickerProvider, DepthProvider
   - `trade.py` - OrderExecutor, PositionManager
   - `account.py` - BalanceProvider, TransferExecutor

7. Set up type stub generation pipeline:
   - Script to auto-generate `client.pyi` and `async_client.pyi` from endpoints
   - Add to build/CI process

8. Update `binance/exceptions.py` to re-export from `_core/exceptions.py` for backward compatibility

### Phase 2: Spot API Migration (Week 3-4)
**Migrate all spot trading endpoints**

1. `_endpoints/spot/market.py` - ~20 endpoints (depth, trades, klines, ticker)
2. `_endpoints/spot/trade.py` - ~30 endpoints (orders, OCO, SOR)
3. `_endpoints/spot/account.py` - ~15 endpoints (balances, trades history)
4. `_mixins/klines.py` - Historical klines pagination logic
5. `_mixins/generators.py` - aggregate_trade_iter, klines generators
6. Run spot tests to verify parity

### Phase 3: Derivatives Migration (Week 5-6)
**Migrate futures and options endpoints**

1. `_endpoints/futures_um/` - ~100 endpoints (market, trade, account, data)
2. `_endpoints/futures_cm/` - ~50 endpoints
3. `_endpoints/options/` - ~40 endpoints
4. Run derivatives tests

### Phase 4: Margin & SAPI Migration (Week 7-8)
**Migrate margin, wallet, and service endpoints**

1. `_endpoints/margin/` - ~50 endpoints
2. `_endpoints/portfolio/` - ~80 endpoints (PAPI)
3. `_endpoints/wallet/` - ~50 endpoints (deposits, withdrawals)
4. `_endpoints/services/` - ~50 endpoints (gift card, pay, convert, etc.)

### Phase 5: Client Replacement (Week 9-10)
**Replace monolithic clients with thin versions**

1. Replace `client.py` (17,534 → ~150 lines)
2. Replace `async_client.py` (6,777 → ~150 lines)
3. Full integration testing
4. Remove dead code (`binance/mixins/`, old `client_core.py`)
5. Update documentation

## Critical Files

### To Create
| File | Purpose | Lines |
|------|---------|-------|
| `_core/base.py` | Constants, URLs, config | ~300 |
| `_core/auth.py` | HMAC/RSA/Ed25519 signing | ~150 |
| `_core/request_sync.py` | Sync HTTP transport + metadata extraction | ~200 |
| `_core/request_async.py` | Async HTTP transport + metadata extraction | ~200 |
| `_core/response.py` | APIResponse dataclass with metadata | ~100 |
| `_core/exceptions.py` | Standardized exception hierarchy | ~200 |
| `_endpoints/_base.py` | Endpoint descriptor + `to_tool_schema()` | ~250 |
| `_endpoints/_generator.py` | Method generator + `generate_pyi()` | ~200 |
| `_endpoints/spot/*.py` | Spot endpoints | ~600 |
| `_endpoints/futures_um/*.py` | UM Futures | ~400 |
| `_schemas/_base.py` | Base schema classes | ~100 |
| `_schemas/common.py` | Shared types (OrderSide, Interval, etc.) | ~150 |
| `_schemas/spot.py` | Spot API request/response schemas | ~300 |
| `_schemas/futures.py` | Futures API request/response schemas | ~300 |
| `_mixins/klines.py` | Pagination logic | ~250 |
| `_protocols/market.py` | KlineProvider, TickerProvider, DepthProvider | ~80 |
| `_protocols/trade.py` | OrderExecutor, PositionManager | ~60 |
| `_protocols/account.py` | BalanceProvider, TransferExecutor | ~60 |
| `client.pyi` | Type stubs for Client (auto-generated) | ~2000 |
| `async_client.pyi` | Type stubs for AsyncClient (auto-generated) | ~2000 |

### To Modify
| File | Change |
|------|--------|
| `client.py` | 17,534 → ~150 lines |
| `async_client.py` | 6,777 → ~150 lines |
| `__init__.py` | Update imports |

### To Remove (Eventually)
| File | Reason |
|------|--------|
| `binance/mixins/` | Dead code (never imported) |
| `binance/async_mixins/` | Replaced by `_endpoints/` |

## Backward Compatibility

**Must Preserve:**
- All 806 public method names
- All parameter names and defaults
- All return types
- Constructor signatures for Client/AsyncClient
- Constants accessible via `Client.ORDER_TYPE_LIMIT`, etc.
- All public exports in `binance/__init__.py`

**Strategy:**
- Endpoint definitions generate methods with exact same signatures
- Constants inherited through `BaseConfig` class
- Complex methods (klines pagination) kept in mixins with same signatures

## Verification

1. **Unit Tests**: Run existing test suite - must pass 100%
2. **Method Parity**: Script to verify all 806 methods exist on new clients
3. **Type Checking**: pyright/mypy on new codebase
4. **Manual Testing**: Test key workflows (spot order, futures order, klines)

## Success Metrics

### Code Quality Metrics
| Metric | Target |
|--------|--------|
| Max file size | < 300 lines |
| Methods preserved | 806/806 (100%) |
| Test pass rate | 100% |
| Code duplication | 0 (single source of truth) |
| Circular imports | 0 (unidirectional dependency) |

### Type System Metrics
| Metric | Target |
|--------|--------|
| Type stub coverage | 100% methods in .pyi |
| Request schema coverage | Core endpoints (Spot, Futures trade) |
| Response schema coverage | Core endpoints with structured data |
| IDE autocompletion | Full parameter hints via .pyi |

### AI Compatibility Metrics
| Metric | Target |
|--------|--------|
| AI tool export | All endpoints exportable to OpenAI/Claude schema |
| Static analysis | AI can infer field types from schema |
| Parameter validation | Pydantic catches errors before API call |

### Contract & Integration Metrics
| Metric | Target |
|--------|--------|
| Exception semantics | All API errors mapped to domain exceptions |
| Metadata passthrough | Rate limit headers preserved in APIResponse |
| Error recoverability | RateLimitExceeded includes retry_after |
| Backward compatibility | 100% existing code works without changes |
