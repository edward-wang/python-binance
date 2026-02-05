# Phase 4: Futures API Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add USDT-M (umfutures) and COIN-M (cmfutures) Futures API support with typed AsyncClient methods, following the same architecture as Phase 3 Spot API.

**Architecture:** Extend the existing HTTPClient to support futures base URLs, create `binance/api/futures_um/` and `binance/api/futures_cm/` endpoint modules with typed returns, add futures-specific schemas to `binance/_schemas/futures.py`, and extend AsyncClient with futures methods.

**Tech Stack:** Same as Phase 3 - msgspec schemas with pre-compiled decoders, aiohttp HTTP client, pytest-asyncio for testing

---

## Prerequisites

Before starting Phase 4, **verify** each prerequisite:

### 1. Phase 3 Complete: Spot API Working

```bash
# Verify Spot API imports and works
python -c "
from binance import AsyncClient
from binance._schemas.spot import Order, Account, TickerPrice
print('✓ Phase 3 Spot API verified')
"
```

### 2. HTTPClient Supports Base URL Override

```bash
# Verify HTTPClient can accept custom base_url
python -c "
from binance._core.http import HTTPClient
client = HTTPClient(base_url='https://testnet.binancefuture.com')
print('✓ HTTPClient base_url override works')
"
```

### 3. Futures Specs Available

```bash
# Verify futures spec files exist
ls specs/openapi/umfutures/get_fapi_v1_klines.yaml \
   specs/openapi/umfutures/post_fapi_v1_order.yaml \
   specs/openapi/cmfutures/get_dapi_v1_klines.yaml \
   specs/openapi/cmfutures/post_dapi_v1_order.yaml
```

**If any prerequisite fails, fix it before proceeding.**

---

## Phase 4 File Structure

**⚠️ Execution Order:** Execute tasks in this order (schemas before endpoints):

| Execution Order | File | Tasks | Description |
|----------------|------|-------|-------------|
| 1 | [01-generate-endpoints.md](./01-generate-endpoints.md) | 1 | Add config URLs |
| 2 | [02-generate-schemas.md](./02-generate-schemas.md) | 2-5 | Update spot schemas + create _schemas/futures.py (MUST be before endpoints) |
| 3 | [01-generate-endpoints.md](./01-generate-endpoints.md) | 6-8 | Create api/futures_um/ and api/futures_cm/ |
| 4 | [03-async-client.md](./03-async-client.md) | 9-14 | Extend AsyncClient with futures methods |
| 5 | [04-integration-testing.md](./04-integration-testing.md) | 15-21 | Integration tests on futures testnet |

---

## Key Design Decisions

### 1. Separate Endpoint Modules for UM and CM

USDT-M and COIN-M have different:
- Base URLs (`/fapi/` vs `/dapi/`)
- Some endpoint differences
- Different testnet URLs

```
binance/api/
├── spot/           # Existing Phase 3
├── futures_um/     # USDT-Margined futures (/fapi/)
│   ├── __init__.py
│   ├── general.py
│   ├── market.py
│   ├── trade.py
│   └── account.py
└── futures_cm/     # COIN-Margined futures (/dapi/)
    ├── __init__.py
    ├── general.py
    ├── market.py
    ├── trade.py
    └── account.py
```

**Why duplication over shared abstraction:**
- Mechanical duplication (only path differs) is easy to maintain
- Direct implementations simplify debugging with explicit call paths
- Allows APIs to diverge independently as Binance evolves
- Follows same pattern as existing Spot API
- Abstraction would add complexity without significant benefit

### 2. Shared Futures Schemas

Most schemas are shared between UM and CM:

```python
# binance/_schemas/futures.py
class FuturesOrder(BaseStruct):
    """Order for both USDT-M and COIN-M futures."""
    ...

class PositionRisk(BaseStruct):
    """Position information."""
    ...

class FundingRate(BaseStruct):
    """Funding rate info."""
    ...
```

### 3. AsyncClient Extension Pattern

Add futures methods with `futures_` prefix for UM and `futures_coin_` prefix for CM:

```python
class AsyncClient:
    # Existing Spot methods...

    # USDT-M Futures (prefix: futures_)
    async def futures_get_klines(...) -> list[FuturesKline]: ...
    async def futures_create_order(...) -> FuturesOrder: ...
    async def futures_get_position_risk(...) -> list[PositionRisk]: ...
    async def futures_set_leverage(...) -> LeverageResult: ...

    # COIN-M Futures (prefix: futures_coin_)
    async def futures_coin_get_klines(...) -> list[FuturesKline]: ...
    async def futures_coin_create_order(...) -> FuturesOrder: ...
    async def futures_coin_get_position_risk(...) -> list[PositionRisk]: ...
```

### 4. HTTPClient with Multiple Base URLs

Extend HTTPClient or create specialized clients:

```python
# Option A: Multiple HTTPClient instances
self._http_spot = HTTPClient(base_url=SPOT_URL)
self._http_futures_um = HTTPClient(base_url=FUTURES_UM_URL)
self._http_futures_cm = HTTPClient(base_url=FUTURES_CM_URL)

# Option B: Pass base_url per request (simpler for now)
async def futures_get_klines(self, ...):
    return await futures_um.get_klines(self._http_futures, ...)
```

---

## Futures API Base URLs

| API | Production | Testnet |
|-----|------------|---------|
| USDT-M (UM) | `https://fapi.binance.com` | `https://testnet.binancefuture.com` |
| COIN-M (CM) | `https://dapi.binance.com` | `https://testnet.binancefuture.com` |

---

## Target Output Structure

```
binance/
├── __init__.py              # Export AsyncClient (unchanged)
├── client.py                # Extended with futures methods
├── _core/
│   ├── config.py            # Add futures URLs
│   └── ...
├── _schemas/
│   ├── common.py            # Existing
│   ├── spot.py              # Existing Phase 3
│   └── futures.py           # NEW: Futures-specific schemas
├── api/
│   ├── spot/                # Existing Phase 3
│   ├── futures_um/          # NEW: USDT-M endpoints
│   │   ├── __init__.py
│   │   ├── general.py
│   │   ├── market.py
│   │   ├── trade.py
│   │   └── account.py
│   └── futures_cm/          # NEW: COIN-M endpoints
│       ├── __init__.py
│       ├── general.py
│       ├── market.py
│       ├── trade.py
│       └── account.py
```

---

## Endpoint Scope (MVP)

Focus on 25 core futures trading endpoints per API type.

### General (3 endpoints)
| Endpoint | Return Type |
|----------|-------------|
| `GET /fapi/v1/ping` | `dict` (empty) |
| `GET /fapi/v1/time` | `ServerTime` |
| `GET /fapi/v1/exchangeInfo` | `FuturesExchangeInfo` |

### Market Data (10 endpoints)
| Endpoint | Return Type |
|----------|-------------|
| `GET /fapi/v1/depth` | `OrderBook` |
| `GET /fapi/v1/trades` | `list[Trade]` |
| `GET /fapi/v1/aggTrades` | `list[AggTrade]` |
| `GET /fapi/v1/klines` | `list[FuturesKline]` |
| `GET /fapi/v1/continuousKlines` | `list[FuturesKline]` |
| `GET /fapi/v1/markPrice` | `MarkPrice \| list[MarkPrice]` |
| `GET /fapi/v1/fundingRate` | `list[FundingRate]` |
| `GET /fapi/v1/ticker/24hr` | `FuturesTicker24h \| list[FuturesTicker24h]` |
| `GET /fapi/v1/ticker/price` | `TickerPrice \| list[TickerPrice]` |
| `GET /fapi/v1/ticker/bookTicker` | `BookTicker \| list[BookTicker]` |

### Trade (7 endpoints)
| Endpoint | Return Type |
|----------|-------------|
| `POST /fapi/v1/order` | `FuturesOrder` |
| `POST /fapi/v1/order/test` | `dict` (empty) |
| `GET /fapi/v1/order` | `FuturesOrder` |
| `DELETE /fapi/v1/order` | `FuturesOrder` |
| `GET /fapi/v1/openOrders` | `list[FuturesOrder]` |
| `DELETE /fapi/v1/allOpenOrders` | `dict` |
| `POST /fapi/v1/batchOrders` | `list[FuturesOrder \| BatchOrderError]` |

### Account/Position (5 endpoints)
| Endpoint | Return Type |
|----------|-------------|
| `GET /fapi/v2/account` | `FuturesAccount` |
| `GET /fapi/v2/balance` | `list[FuturesBalance]` |
| `GET /fapi/v2/positionRisk` | `list[PositionRisk]` |
| `POST /fapi/v1/leverage` | `LeverageResult` |
| `POST /fapi/v1/marginType` | `dict` |

---

## Verification Milestones

| Milestone | Verification |
|-----------|--------------|
| Prerequisites pass | All 3 prerequisite checks pass |
| Endpoints importable | `from binance.api.futures_um import market` |
| Schemas valid | `from binance._schemas.futures import FuturesOrder` |
| AsyncClient has futures | `hasattr(client, 'futures_get_klines')` |
| Unit tests pass | `pytest tests/unit/ -v` |
| Integration tests pass | `pytest tests/integration/test_futures*.py -v` |
| Types check | `mypy binance/ --strict` passes |

---

## Start Implementation

**First**, run the prerequisite verification commands above.

**Then**, begin with [01-generate-endpoints.md](./01-generate-endpoints.md).
