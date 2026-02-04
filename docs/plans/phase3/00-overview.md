# Phase 3: Spot API Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Generate complete Spot API with AsyncClient entry point and verify it works on Binance testnet.

**Architecture:** Use the Phase 2 generator to emit Python code from OpenAPI specs, create a thin AsyncClient wrapper that binds generated methods, and verify with real API calls.

**Tech Stack:** Phase 2 generator, msgspec schemas, aiohttp HTTP client, pytest-asyncio for testing

---

## Prerequisites

Before starting Phase 3, ensure:

1. **Phase 1 Complete:** `binance/_core/` modules exist and work
   - `_core/config.py` - URLs, constants
   - `_core/context.py` - Time offset
   - `_core/auth.py` - Signature generation
   - `_core/http.py` - HTTPClient with connection pooling
   - `_core/exceptions.py` - Exception hierarchy
   - `_core/decoders.py` - Pre-compiled msgspec decoders
   - `_core/formatters.py` - Price/quantity formatting

2. **Phase 2 Complete:** Generator can parse specs and emit code
   - `generator/` package exists
   - `generator/parser.py` - Parse OpenAPI YAML
   - `generator/emitter.py` - Emit Python code from templates
   - `generator/templates/` - Jinja2 templates
   - `python -m generator --help` works

3. **Specs Downloaded:** OpenAPI specs exist in `specs/openapi/spot/`
   - Core endpoints: `get_api_v3_klines.yaml`, `post_api_v3_order.yaml`, etc.

---

## Phase 3 File Structure

This plan is split into multiple files for easier execution:

| File | Tasks | Description |
|------|-------|-------------|
| [01-generate-endpoints.md](./01-generate-endpoints.md) | 1-3 | Run generator, create api/spot/ modules |
| [02-generate-schemas.md](./02-generate-schemas.md) | 4-6 | Generate _schemas/spot.py |
| [03-async-client.md](./03-async-client.md) | 7-9 | Create AsyncClient entry point |
| [04-integration-testing.md](./04-integration-testing.md) | 10-12 | Test on Binance testnet |

---

## Target Output Structure

After Phase 3 completion:

```
binance/
├── __init__.py              # Export AsyncClient
├── client.py                # NEW: AsyncClient entry point
├── _core/                   # Existing from Phase 1
├── _schemas/
│   ├── __init__.py
│   ├── common.py            # Existing
│   └── spot.py              # NEW: Generated spot schemas
├── api/
│   ├── __init__.py          # NEW
│   └── spot/
│       ├── __init__.py      # NEW
│       ├── general.py       # NEW: ping, time, exchange_info
│       ├── market.py        # NEW: klines, depth, trades
│       ├── trade.py         # NEW: orders, cancel
│       └── account.py       # NEW: account, my_trades
└── _meta/
    ├── __init__.py          # NEW
    └── endpoints.py         # NEW: Endpoint definitions
```

---

## Endpoint Scope (MVP)

Focus on core trading endpoints first. Skip SAPI (wallet, sub-account, etc.).

### General (3 endpoints)
- `GET /api/v3/ping` - Test connectivity
- `GET /api/v3/time` - Server time
- `GET /api/v3/exchangeInfo` - Exchange info

### Market Data (8 endpoints)
- `GET /api/v3/depth` - Order book
- `GET /api/v3/trades` - Recent trades
- `GET /api/v3/aggTrades` - Aggregated trades
- `GET /api/v3/klines` - Kline/candlestick data
- `GET /api/v3/avgPrice` - Current average price
- `GET /api/v3/ticker/24hr` - 24hr ticker
- `GET /api/v3/ticker/price` - Price ticker
- `GET /api/v3/ticker/bookTicker` - Best bid/ask

### Trade (6 endpoints)
- `POST /api/v3/order` - New order
- `POST /api/v3/order/test` - Test new order
- `GET /api/v3/order` - Query order
- `DELETE /api/v3/order` - Cancel order
- `GET /api/v3/openOrders` - Current open orders
- `DELETE /api/v3/openOrders` - Cancel all open orders

### Account (3 endpoints)
- `GET /api/v3/account` - Account info
- `GET /api/v3/myTrades` - Account trade list
- `GET /api/v3/rateLimit/order` - Query order count

**Total: 20 core endpoints**

---

## Verification Milestones

| Milestone | Verification |
|-----------|--------------|
| Generator runs | `python -m generator spot` produces files |
| Schemas valid | `python -c "from binance._schemas.spot import *"` |
| Endpoints valid | `python -c "from binance.api.spot import market"` |
| Types check | `mypy binance/api binance/_schemas` passes |
| Client works | Public endpoint call succeeds |
| Signed works | Account endpoint call succeeds |
| Order works | Test order on testnet succeeds |

---

## Start Implementation

Begin with [01-generate-endpoints.md](./01-generate-endpoints.md).
