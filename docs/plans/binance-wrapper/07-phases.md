# Section 7: Implementation Phases

## Overview

```
Phase 1: Foundation       → _core/ + generator scaffold
Phase 2: Code Generator   → specs → generated code
Phase 3: Spot API         → spot endpoints + schemas
Phase 4: Futures API      → futures_um, futures_cm
Phase 5: Testing & Polish → tests, docs, cleanup
```

## Phase 1: Foundation

**Goal:** Hand-written infrastructure that generated code depends on.

| Task | Output | Lines |
|------|--------|-------|
| Create `_core/config.py` | URLs, constants | ~100 |
| Create `_core/context.py` | Time offset, global state | ~80 |
| Create `_core/auth.py` | HMAC/RSA/Ed25519 signatures | ~150 |
| Create `_core/http.py` | aiohttp client + connection pool | ~250 |
| Create `_core/exceptions.py` | Full exception hierarchy | ~250 |
| Create `_core/decoders.py` | Pre-compiled msgspec decoders | ~50 |
| Create `_core/formatters.py` | Price/quantity formatting | ~50 |
| Create `_schemas/common.py` | BaseStruct, Literals, Constants | ~150 |
| Setup project structure | pyproject.toml, dependencies | - |

**Dependencies:**

```toml
# pyproject.toml
[project]
name = "binance-wrapper"
version = "0.1.0"
requires-python = ">=3.11"

dependencies = [
    "aiohttp>=3.9",
    "msgspec>=0.18",
    "orjson>=3.9",
    "uvloop>=0.19; sys_platform != 'win32'",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "ruff>=0.2",
    "mypy>=1.8",
]
```

**Milestone:** Working `_core/` that can make authenticated requests.

**Verification:**

```python
from binance._core.http import HTTPClient

async def test_core():
    client = HTTPClient(api_key="...", api_secret="...")
    await client.connect()

    # Test public endpoint
    time = await client._request("GET", "/api/v3/time")
    print(f"Server time: {time['serverTime']}")

    # Test signed endpoint
    account = await client._request("GET", "/api/v3/account", signed=True)
    print(f"Account balances: {len(account['balances'])}")

    await client.close()
```

## Phase 2: Code Generator

**Goal:** Build generator that reads OpenXAPI specs and outputs Python code.

| Task | Output |
|------|--------|
| Download OpenXAPI specs | `specs/spot.json`, `specs/futures_um.json`, etc. |
| Create `generator/parser.py` | Parse OpenXAPI JSON → internal model |
| Create `generator/templates/` | Jinja2 templates for code output |
| Create `generator/emitter.py` | Render templates → .py files |
| Create `generator/main.py` | CLI entry point |
| Create `generator/config.py` | Naming rules, output paths |

**Generator CLI:**

```bash
python -m generator

# Output:
#   ✓ binance/api/spot/general.py      (12 endpoints)
#   ✓ binance/api/spot/market.py       (18 endpoints)
#   ✓ binance/api/spot/trade.py        (25 endpoints)
#   ✓ binance/api/spot/account.py      (15 endpoints)
#   ✓ binance/_schemas/spot.py         (45 structs)
#   ✓ binance/_meta/endpoints.py       (70 endpoint definitions)
```

**Milestone:** Generator that produces valid Python from specs.

**Verification:**

```bash
# Generate code
python -m generator

# Check syntax
python -c "from binance.api.spot import market"

# Check types
mypy binance/api binance/_schemas
```

## Phase 3: Spot API

**Goal:** Complete Spot API with generated code + AsyncClient.

| Task | Output |
|------|--------|
| Generate spot endpoints | `api/spot/*.py` |
| Generate spot schemas | `_schemas/spot.py` |
| Generate spot metadata | `_meta/endpoints.py` |
| Create `client.py` | AsyncClient entry point |
| Manual review & fixes | Fix any generator issues |
| Integration test | Test against Binance testnet |

**AsyncClient structure:**

```python
# binance/client.py
from binance._core.http import HTTPClient
from binance.api.spot import general, market, trade, account

class AsyncClient:
    def __init__(
        self,
        api_key: str = "",
        api_secret: str = "",
        testnet: bool = False,
    ):
        self._http = HTTPClient(api_key, api_secret, testnet)

    async def __aenter__(self):
        await self._http.connect()
        return self

    async def __aexit__(self, *args):
        await self._http.close()

    # Bind generated methods
    ping = general.ping
    get_server_time = general.get_server_time
    get_exchange_info = general.get_exchange_info

    get_klines = market.get_klines
    get_order_book = market.get_order_book
    get_ticker_price = market.get_ticker_price

    create_order = trade.create_order
    cancel_order = trade.cancel_order
    get_order = trade.get_order

    get_account = account.get_account
    get_my_trades = account.get_my_trades
```

**Milestone:** Working Spot API that can place real orders on testnet.

**Verification:**

```python
from binance import AsyncClient
from binance._schemas.common import ORDER_SIDE_BUY, ORDER_TYPE_MARKET

async def test_spot():
    async with AsyncClient(api_key="...", api_secret="...", testnet=True) as client:
        # Market data
        klines = await client.get_klines(symbol="BTCUSDT", interval="1h", limit=10)
        print(f"Got {len(klines)} klines, last close: {klines[-1].close}")

        # Place order (testnet)
        order = await client.create_order(
            symbol="BTCUSDT",
            side=ORDER_SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity="0.001",
        )
        print(f"Order placed: {order.order_id}")
```

## Phase 4: Futures API

**Goal:** Add USDT-M and COIN-M Futures support.

| Task | Output |
|------|--------|
| Generate futures_um endpoints | `api/futures_um/*.py` |
| Generate futures_cm endpoints | `api/futures_cm/*.py` |
| Generate futures schemas | `_schemas/futures.py` |
| Extend AsyncClient | Add futures methods |
| Integration test | Test on futures testnet |

**Extended AsyncClient:**

```python
class AsyncClient:
    # ... spot methods ...

    # Futures UM (USDT-Margined)
    futures_get_klines = futures_um.get_klines
    futures_get_position_risk = futures_um.get_position_risk
    futures_create_order = futures_um.create_order
    futures_cancel_order = futures_um.cancel_order

    # Futures CM (COIN-Margined)
    futures_coin_get_klines = futures_cm.get_klines
    futures_coin_get_position_risk = futures_cm.get_position_risk
    futures_coin_create_order = futures_cm.create_order
```

**Milestone:** Working Futures API for both USDT-M and COIN-M.

## Phase 5: Testing & Polish

**Goal:** Production-ready quality.

| Task | Output |
|------|--------|
| Unit tests | `tests/unit/test_*.py` |
| Integration tests | `tests/integration/` |
| Type checking | `mypy` / `pyright` passes |
| Linting | `ruff` clean |
| Documentation | README, API docs |
| Benchmarks | Performance verification |
| Cleanup | Remove old files |

**Test structure:**

```
tests/
├── unit/
│   ├── test_auth.py
│   ├── test_formatters.py
│   ├── test_exceptions.py
│   └── test_schemas.py
├── integration/
│   ├── test_spot_market.py
│   ├── test_spot_trade.py
│   └── test_futures.py
└── conftest.py
```

**Milestone:** Production-ready wrapper with tests and docs.

## Milestone Summary

| Phase | Milestone | Verification |
|-------|-----------|--------------|
| 1 | `_core/` complete | Can make authenticated request |
| 2 | Generator works | Outputs valid Python from specs |
| 3 | Spot API works | Place order on testnet |
| 4 | Futures API works | Place futures order on testnet |
| 5 | Production ready | Tests pass, types check, docs done |

## Files to Remove (After Phase 5)

| File | Reason |
|------|--------|
| `binance/client.py` (old) | Replaced by new thin client |
| `binance/async_client.py` (old) | Replaced |
| `binance/base_client.py` | Logic moved to `_core/` |
| `binance/client_core.py` | Logic moved to `_core/` |
| `binance/async_client_core.py` | Logic moved to `_core/` |
