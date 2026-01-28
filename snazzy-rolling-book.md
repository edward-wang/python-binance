# Python-Binance AI-Friendly Restructuring Plan

## Problem Summary

| Issue | Current State | Impact |
|-------|--------------|--------|
| `client.py` | 17,534 lines, 806 methods | Exceeds AI context limits |
| Code duplication | Same logic in 3 places | Maintenance nightmare |
| Sync mixins | 13,866 lines of dead code | Confusion, wasted space |
| Auto-generated stubs | 500+ placeholder methods | Unmaintainable |

## Target Architecture

```
binance/
├── __init__.py                    # Public exports (unchanged)
├── client.py                      # Thin sync client (~150 lines)
├── async_client.py                # Thin async client (~150 lines)
│
├── _core/                         # Internal infrastructure
│   ├── __init__.py
│   ├── base.py                    # Constants, config (~300 lines)
│   ├── auth.py                    # Signature generation (~150 lines)
│   ├── request_sync.py            # Sync HTTP transport (~150 lines)
│   └── request_async.py           # Async HTTP transport (~150 lines)
│
├── _endpoints/                    # Declarative endpoint definitions
│   ├── __init__.py
│   ├── _base.py                   # Endpoint descriptor class (~200 lines)
│   ├── _generator.py              # Sync/async method generator (~150 lines)
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
├── _mixins/                       # Business logic (pagination, generators)
│   ├── klines.py                  # Historical klines (~250 lines)
│   └── generators.py              # Trade iterators (~150 lines)
│
├── exceptions.py                  # Keep existing
├── enums.py                       # Keep existing
└── ws/                            # Keep existing WebSocket structure
```

## Key Design: Declarative Endpoints

Define each endpoint ONCE, generate both sync and async methods:

```python
# binance/_endpoints/_base.py
@dataclass
class Endpoint:
    name: str                      # Method name: get_klines
    path: str                      # API path: "klines"
    method: str = "get"            # HTTP method
    request_type: RequestType      # API, MARGIN, FUTURES_UM, etc.
    signed: bool = False
    version: int = 1
    params: List[Param] = field(default_factory=list)
    doc: str = ""

# binance/_endpoints/spot/market.py
get_klines = Endpoint(
    name="get_klines",
    path="klines",
    request_type=RequestType.API,
    params=[
        Param("symbol", str, required=True),
        Param("interval", str, required=True),
        Param("limit", int, default=500),
    ]
)

# binance/_endpoints/_generator.py
def generate_sync_method(ep: Endpoint):
    def method(self, **params):
        kwargs = ep.build_request_kwargs(**params)
        return getattr(self, REQUEST_MAP[ep.request_type])(
            ep.method, ep.path, signed=ep.signed, **kwargs
        )
    return method

def generate_async_method(ep: Endpoint):
    async def method(self, **params):
        kwargs = ep.build_request_kwargs(**params)
        return await getattr(self, REQUEST_MAP[ep.request_type])(
            ep.method, ep.path, signed=ep.signed, **kwargs
        )
    return method
```

## Implementation Phases

### Phase 1: Foundation (Week 1-2)
**Create core infrastructure and endpoint system**

1. Create `binance/_core/` directory:
   - `base.py` - Extract constants from `base_client.py` (lines 22-156)
   - `auth.py` - Extract auth from `base_client.py` (lines 157-250)
   - `request_sync.py` - Refactor from `client_core.py`
   - `request_async.py` - Refactor from `async_client_core.py`

2. Create `binance/_endpoints/` directory:
   - `_base.py` - Endpoint and Param dataclasses, RequestType enum
   - `_generator.py` - `generate_sync_method()`, `generate_async_method()`, `bind_endpoints_to_class()`

3. Create first endpoint module:
   - `spot/general.py` - ping, get_server_time, get_exchange_info (~10 endpoints)

4. Create proof-of-concept thin client that works alongside existing client

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
| `_core/request_sync.py` | Sync HTTP transport | ~150 |
| `_core/request_async.py` | Async HTTP transport | ~150 |
| `_endpoints/_base.py` | Endpoint descriptor | ~200 |
| `_endpoints/_generator.py` | Method generator | ~150 |
| `_endpoints/spot/*.py` | Spot endpoints | ~600 |
| `_endpoints/futures_um/*.py` | UM Futures | ~400 |
| `_mixins/klines.py` | Pagination logic | ~250 |

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

| Metric | Target |
|--------|--------|
| Max file size | < 300 lines |
| Methods preserved | 806/806 (100%) |
| Test pass rate | 100% |
| Code duplication | 0 (single source of truth) |
