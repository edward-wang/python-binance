# Section 8: Future Work

## Priority Overview

| Priority | Feature | Why |
|----------|---------|-----|
| **P0** | WebSocket Optimization | Real-time data is critical for HFT |
| **P1** | Rate Limiter Middleware | Prevent bans, auto-throttle |
| **P1** | Margin API | Common trading feature |
| **P2** | AI Tool Export | Enable AI trading assistants |
| **P2** | `.pyi` Stub Generation | Enhanced IDE support |
| **P3** | Options API | Less common, add on demand |
| **P3** | Protocol Interfaces | For testing/mocking |

---

## P0: WebSocket Optimization

**Why critical:** Market data arrives via WebSocket first. For HFT, every millisecond counts.

### Scope

| Task | Description |
|------|-------------|
| Tagged Unions | C-level message dispatch |
| orjson parsing | Fast JSON |
| Zero-copy buffer | `memoryview` + `bytearray` ring buffer |
| Connection management | Auto-reconnect, heartbeat |
| Backpressure handling | Don't block on slow consumers |

### Architecture

```
binance/ws/
├── __init__.py
├── client.py           # WebSocket client with zero-copy receive
├── buffer.py           # RingBuffer (memoryview + bytearray)
├── streams.py          # Stream subscription handlers
├── handlers.py         # Message dispatch using Tagged Unions
└── reconnect.py        # Auto-reconnection logic
```

### Zero-Copy Ring Buffer

```python
class RingBuffer:
    """Pre-allocated circular buffer to avoid memory allocation."""

    def __init__(self, capacity: int = 1024 * 1024):  # 1MB
        self._buffer = bytearray(capacity)
        self._view = memoryview(self._buffer)
        self._write_pos = 0
        self._read_pos = 0

    def get_write_buffer(self, size: int) -> memoryview:
        """Get zero-copy view for writing incoming data."""
        return self._view[self._write_pos:self._write_pos + size]

    def get_message(self) -> memoryview | None:
        """Get next message as zero-copy memoryview."""
        # Returns view into buffer, no copy
        ...
```

### Usage

```python
async with client.ws_stream(["btcusdt@kline_1m", "btcusdt@trade"]) as stream:
    async for msg in stream:
        match msg:
            case WsKlineEvent(k=kline) if kline.x:
                await strategy.on_kline(kline)
            case WsTradeEvent(p=price, q=qty):
                await strategy.on_trade(price, qty)
```

---

## P1: Rate Limiter Middleware

**Why important:** Binance bans IPs for rate limit violations.

### Multi-Level Thresholds

```
0%          80%         95%        100%
│── Normal ──│── Warn ───│─ Throttle ─│ Block
             │           │            │
          Warning     Forced       Emergency
          callback    sleep        only
```

### Implementation

```python
class RateLimiter:
    def __init__(
        self,
        weight_limit: int = 1200,
        order_limit: int = 10,
        warn_threshold: float = 0.80,
        throttle_threshold: float = 0.95,
        on_warning: Callable | None = None,
        on_throttle: Callable | None = None,
    ):
        ...

    async def acquire(
        self,
        weight: int,
        is_order: bool = False,
        emergency: bool = False,  # For cancel orders
    ) -> RateLimitLevel:
        """Acquire rate limit capacity with multi-level handling."""
        ...
```

### Features

| Feature | Benefit |
|---------|---------|
| `warn_threshold` (80%) | Strategy can reduce activity |
| `throttle_threshold` (95%) | Progressive delay |
| `emergency=True` | Cancel orders always allowed |
| `update_from_headers()` | Sync with server's view |

---

## P1: Margin API

### Structure

```
binance/api/margin/
├── __init__.py
├── cross.py        # Cross margin
├── isolated.py     # Isolated margin
└── account.py      # Margin account
```

### Key Endpoints

- Borrow/repay
- Transfer to/from margin
- Margin account info
- Margin orders

---

## P2: AI Tool Export

**Foundation already laid:** `Annotated[type, msgspec.Meta(description=...)]`

### Implementation

```python
# binance/_meta/tools.py
def export_openai_tools() -> list[dict]:
    """Export endpoints as OpenAI function calling schema."""
    return [
        {
            "type": "function",
            "function": {
                "name": ep.name,
                "description": ep.description,
                "parameters": msgspec.json.schema(ep.request_schema),
            }
        }
        for ep in ENDPOINTS.values()
    ]

def export_claude_tools() -> list[dict]:
    """Export endpoints as Claude tool use schema."""
    return [
        {
            "name": ep.name,
            "description": ep.description,
            "input_schema": msgspec.json.schema(ep.request_schema),
        }
        for ep in ENDPOINTS.values()
    ]
```

### Usage

```python
# With OpenAI
tools = client.export_openai_tools()
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Buy 0.001 BTC"}],
    tools=tools,
)

# With Claude
tools = client.export_claude_tools()
response = anthropic.messages.create(
    model="claude-3-opus",
    messages=[...],
    tools=tools,
)
```

---

## P2: `.pyi` Stub Generation

### Generator Addition

```python
def generate_client_stub(endpoints: list[Endpoint]) -> str:
    """Generate client.pyi from endpoint definitions."""
    lines = ["class AsyncClient:"]

    for ep in endpoints:
        params = ", ".join(
            f"{p.name}: {p.type}" + ("" if p.required else f" = {p.default}")
            for p in ep.params
        )
        lines.append(f"    async def {ep.name}(self, {params}) -> {ep.response_type}: ...")

    return "\n".join(lines)
```

### Output

```python
# binance/client.pyi
class AsyncClient:
    async def get_klines(self, symbol: str, interval: str, limit: int = 500) -> list[Kline]: ...
    async def create_order(self, symbol: str, side: OrderSide, ...) -> OrderResponse: ...
```

---

## P3: Options API

```
binance/api/options/
├── __init__.py
├── market.py      # Option chains, prices
├── trade.py       # Buy/sell options
└── account.py     # Positions, Greeks
```

---

## P3: Protocol Interfaces

For testing with mock implementations.

```python
# binance/_protocols/market.py
from typing import Protocol

class KlineProvider(Protocol):
    async def get_klines(self, symbol: str, interval: str, limit: int = 500) -> list[Kline]: ...

# Usage in strategy (testable)
async def run_strategy(market: KlineProvider):
    klines = await market.get_klines("BTCUSDT", "1h")
    ...

# Real
await run_strategy(client)

# Test
await run_strategy(MockMarket(predefined_klines))
```

---

## Roadmap

```
MVP Complete
     │
     ▼
┌─────────────────────────────────────────┐
│ P0: WebSocket Optimization              │
│     - Tagged Unions, zero-copy, orjson  │
└─────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│ P1: Rate Limiter + Margin API           │
│     - Multi-level warnings, margin      │
└─────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│ P2: AI Export + .pyi Stubs              │
│     - OpenAI/Claude tools, IDE support  │
└─────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│ P3: Options API + Protocols             │
│     - European options, testing support │
└─────────────────────────────────────────┘
```
