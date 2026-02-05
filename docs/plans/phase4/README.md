# Phase 4: Futures API Implementation

This directory contains the implementation plan for adding USDT-M (umfutures) and COIN-M (cmfutures) Futures API support to the Binance Python wrapper.

## Quick Start

```bash
# Start implementation
# REQUIRED SUB-SKILL: Use superpowers:executing-plans

# Read the overview first
cat docs/plans/phase4/00-overview.md

# Then execute tasks in the order specified below
```

## ⚠️ IMPORTANT: Execution Order

**Execute tasks in this order (schemas before endpoints):**

1. **Task 1** from `01-generate-endpoints.md` - Add config URLs
2. **Tasks 2-5** from `02-generate-schemas.md` - Update spot schemas + create futures schemas FIRST
3. **Tasks 6-8** from `01-generate-endpoints.md` - Create endpoints (they import schemas)
4. **Tasks 9-14** from `03-async-client.md` - Extend AsyncClient
5. **Tasks 15-21** from `04-integration-testing.md` - Integration tests

## Plan Files

| File | Description | Tasks |
|------|-------------|-------|
| [00-overview.md](./00-overview.md) | Prerequisites, architecture, key decisions | - |
| [01-generate-endpoints.md](./01-generate-endpoints.md) | Add config URLs + Create api/futures_um/ and api/futures_cm/ | 1, 6-8 |
| [02-generate-schemas.md](./02-generate-schemas.md) | Update spot schemas + create _schemas/futures.py | 2-5 |
| [03-async-client.md](./03-async-client.md) | Extend AsyncClient with futures methods | 9-14 |
| [04-integration-testing.md](./04-integration-testing.md) | Testnet integration tests | 15-21 |

## Summary

**Goal:** Add USDT-M and COIN-M Futures API with typed returns

**Output Structure:**
```
binance/
├── api/
│   ├── spot/            # Existing (Phase 3)
│   ├── futures_um/      # NEW: USDT-M (/fapi/)
│   └── futures_cm/      # NEW: COIN-M (/dapi/)
├── _schemas/
│   ├── spot.py          # Existing (Phase 3)
│   └── futures.py       # NEW: Futures schemas
└── client.py            # Extended with futures methods
```

**Key Features:**
- 25+ endpoints per API type (UM and CM)
- Typed schemas for all responses
- Position management (leverage, margin type)
- Mark price and funding rate
- Complete trading lifecycle

## Prerequisites

Before starting Phase 4:

1. **Phase 3 complete:** `from binance import AsyncClient` works
2. **Futures specs available:** `specs/openapi/umfutures/` and `specs/openapi/cmfutures/`
3. **Futures testnet keys:** From https://testnet.binancefuture.com/

## API Naming Convention

| API | Method Prefix | Base URL |
|-----|--------------|----------|
| Spot | (none) | /api/v3/ |
| USDT-M Futures | `futures_` | /fapi/v1/ |
| COIN-M Futures | `futures_coin_` | /dapi/v1/ |

**Example:**
```python
# Spot
await client.get_klines(symbol="BTCUSDT", interval="1h")

# USDT-M Futures
await client.futures_get_klines(symbol="BTCUSDT", interval="1h")

# COIN-M Futures
await client.futures_coin_get_klines(symbol="BTCUSD_PERP", interval="1h")
```

## Estimated Scope

- **21 tasks** across 4 plan files
- **~2000 lines** of new code
- **~100 new tests**
- **50+ new endpoints** (25 UM + 25 CM)
