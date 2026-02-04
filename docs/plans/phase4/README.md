# Phase 4: Futures API Implementation

This directory contains the implementation plan for adding USDT-M (umfutures) and COIN-M (cmfutures) Futures API support to the Binance Python wrapper.

## Quick Start

```bash
# Start implementation
# REQUIRED SUB-SKILL: Use superpowers:executing-plans

# Read the overview first
cat docs/plans/phase4/00-overview.md

# Then execute tasks in order
```

## Plan Files

| File | Description | Tasks |
|------|-------------|-------|
| [00-overview.md](./00-overview.md) | Prerequisites, architecture, key decisions | - |
| [01-generate-endpoints.md](./01-generate-endpoints.md) | Create api/futures_um/ and api/futures_cm/ | 1-4 |
| [02-generate-schemas.md](./02-generate-schemas.md) | Create _schemas/futures.py | 5-7 |
| [03-async-client.md](./03-async-client.md) | Extend AsyncClient with futures methods | 8-11 |
| [04-integration-testing.md](./04-integration-testing.md) | Testnet integration tests | 12-18 |

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

- **18 tasks** across 4 plan files
- **~2000 lines** of new code
- **~100 new tests**
- **50+ new endpoints** (25 UM + 25 CM)
