# Phase 3: Spot API Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Generate complete Spot API with typed AsyncClient entry point and verify it works on Binance testnet.

**Architecture:** Use the Phase 2 generator to emit Python code from OpenAPI specs, create a thin AsyncClient wrapper that returns **typed msgspec schemas** (not raw dicts), and verify with real API calls.

**Tech Stack:** Phase 2 generator, msgspec schemas with pre-compiled decoders, aiohttp HTTP client, pytest-asyncio for testing

---

## Prerequisites

Before starting Phase 3, **verify** each prerequisite:

### 1. Phase 1 Complete: `binance/_core/`

```bash
# Verify all core modules exist and import
python -c "
from binance._core.config import BASE_URLS
from binance._core.context import context
from binance._core.auth import sign_request
from binance._core.http import HTTPClient
from binance._core.exceptions import BinanceAPIError, raise_for_error
from binance._core.decoders import get_decoder
from binance._core.formatters import format_price, format_quantity
print('✓ Phase 1 core modules verified')
"
```

### 2. Phase 2 Complete: Generator Works

```bash
# Verify generator can parse and emit code (not just --help)
python -c "
from generator.parser import parse_yaml_file, extract_path_and_method
from generator.emitter import render_endpoint
from pathlib import Path

# Test with a real spec file
spec_file = Path('specs/openapi/spot/get_api_v3_time.yaml')
if not spec_file.exists():
    raise FileNotFoundError(f'Spec file not found: {spec_file}')

data = parse_yaml_file(spec_file)
path, method, operation = extract_path_and_method(data)
assert path == '/api/v3/time'
assert method == 'GET'
print('✓ Phase 2 generator verified')
"
```

### 3. Specs Downloaded

```bash
# Verify core spec files exist
ls specs/openapi/spot/get_api_v3_klines.yaml \
   specs/openapi/spot/post_api_v3_order.yaml \
   specs/openapi/spot/get_api_v3_account.yaml
```

**If any prerequisite fails, fix it before proceeding.**

---

## Phase 3 File Structure

| File | Tasks | Description |
|------|-------|-------------|
| [01-generate-endpoints.md](./01-generate-endpoints.md) | 1-4 | Run generator, create api/spot/ with **typed returns** |
| [02-generate-schemas.md](./02-generate-schemas.md) | 5-7 | Generate _schemas/spot.py, decoder integration |
| [03-async-client.md](./03-async-client.md) | 8-11 | Create AsyncClient with typed methods + **unit tests** |
| [04-integration-testing.md](./04-integration-testing.md) | 12-15 | Integration + **error scenario** tests |

---

## Key Design Decisions

### 1. Typed Returns (Not Raw Dicts)

```python
# ✗ BAD: Current plan loses type safety
async def get_account(self) -> dict[str, Any]:
    return await self._http.request(...)

# ✓ GOOD: Return typed schemas
async def get_account(self) -> Account:
    raw = await self._http.request_raw(...)
    return _account_decoder.decode(raw)
```

### 2. Pre-compiled Decoders

```python
# In binance/api/spot/account.py
from binance._schemas.spot import Account
import msgspec

_account_decoder = msgspec.json.Decoder(Account)

async def get_account(http: HTTPClient) -> Account:
    raw = await http.request_raw("GET", "/api/v3/account", signed=True)
    return _account_decoder.decode(raw)
```

### 3. Response Type Variants

Some endpoints return different types based on parameters:

| Endpoint | Single Symbol | No/Multiple Symbols |
|----------|--------------|---------------------|
| `get_ticker_price` | `TickerPrice` | `list[TickerPrice]` |
| `get_ticker_24h` | `Ticker24h` | `list[Ticker24h]` |

Use `@overload` for type safety:
```python
@overload
async def get_ticker_price(self, symbol: str) -> TickerPrice: ...
@overload
async def get_ticker_price(self, symbol: None = None) -> list[TickerPrice]: ...
```

---

## Target Output Structure

```
binance/
├── __init__.py              # Export AsyncClient
├── client.py                # AsyncClient with TYPED methods
├── _core/                   # Existing from Phase 1
├── _schemas/
│   ├── __init__.py
│   ├── common.py            # Existing
│   └── spot.py              # Generated spot schemas
├── api/
│   ├── __init__.py
│   └── spot/
│       ├── __init__.py
│       ├── general.py       # Returns: ServerTime, ExchangeInfo
│       ├── market.py        # Returns: Kline, OrderBook, Trade, etc.
│       ├── trade.py         # Returns: Order, CancelResult
│       └── account.py       # Returns: Account, MyTrade
└── _meta/
    ├── __init__.py
    └── endpoints.py         # Endpoint metadata
```

---

## Endpoint Scope (MVP)

Focus on 20 core trading endpoints. Return **typed schemas**.

### General (3 endpoints)
| Endpoint | Return Type |
|----------|-------------|
| `GET /api/v3/ping` | `dict` (empty) |
| `GET /api/v3/time` | `ServerTime` |
| `GET /api/v3/exchangeInfo` | `ExchangeInfo` |

### Market Data (8 endpoints)
| Endpoint | Return Type |
|----------|-------------|
| `GET /api/v3/depth` | `OrderBook` |
| `GET /api/v3/trades` | `list[Trade]` |
| `GET /api/v3/aggTrades` | `list[AggTrade]` |
| `GET /api/v3/klines` | `list[Kline]` |
| `GET /api/v3/avgPrice` | `AvgPrice` |
| `GET /api/v3/ticker/24hr` | `Ticker24h \| list[Ticker24h]` |
| `GET /api/v3/ticker/price` | `TickerPrice \| list[TickerPrice]` |
| `GET /api/v3/ticker/bookTicker` | `BookTicker \| list[BookTicker]` |

### Trade (6 endpoints)
| Endpoint | Return Type |
|----------|-------------|
| `POST /api/v3/order` | `Order` |
| `POST /api/v3/order/test` | `dict` (empty) |
| `GET /api/v3/order` | `Order` |
| `DELETE /api/v3/order` | `CancelOrderResult` |
| `GET /api/v3/openOrders` | `list[Order]` |
| `DELETE /api/v3/openOrders` | `list[CancelOrderResult]` |

### Account (3 endpoints)
| Endpoint | Return Type |
|----------|-------------|
| `GET /api/v3/account` | `Account` |
| `GET /api/v3/myTrades` | `list[MyTrade]` |
| `GET /api/v3/rateLimit/order` | `list[RateLimitInfo]` |

---

## Verification Milestones

| Milestone | Verification |
|-----------|--------------|
| Prerequisites pass | All 3 prerequisite checks pass |
| Generator runs | `python -m generator spot` produces files |
| Schemas valid | `python -c "from binance._schemas.spot import *"` |
| Endpoints return typed | `get_account()` returns `Account`, not `dict` |
| Unit tests pass | `pytest tests/unit/ -v` (with mocks) |
| Integration tests pass | `pytest tests/integration/ -v` |
| Error tests pass | Invalid symbol raises `InvalidSymbolError` |
| Types check | `mypy binance/ --strict` passes |

---

## Start Implementation

**First**, run the prerequisite verification commands above.

**Then**, begin with [01-generate-endpoints.md](./01-generate-endpoints.md).
