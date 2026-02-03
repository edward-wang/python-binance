# Section 2: Target Architecture

## Directory Structure

```
python-binance-agent/
│
├── specs/                          # OpenXAPI spec files (one-time download)
│   ├── spot.json
│   ├── futures_um.json
│   ├── futures_cm.json
│   └── margin.json
│
├── generator/                      # Code generator (we build this)
│   ├── __init__.py
│   ├── main.py                     # Entry point: python -m generator
│   ├── parser.py                   # Parse OpenXAPI specs
│   ├── emitter.py                  # Output Python code
│   ├── templates/                  # Jinja2 templates
│   │   ├── endpoint.py.j2
│   │   ├── schema.py.j2
│   │   └── client.py.j2
│   └── config.py                   # Naming rules, output paths
│
├── binance/                        # Generated + hand-written wrapper
│   ├── __init__.py                 # Public exports
│   ├── client.py                   # AsyncClient entry (~150 lines)
│   │
│   ├── _core/                      # Hand-written infrastructure
│   │   ├── __init__.py
│   │   ├── config.py               # URLs, constants
│   │   ├── context.py              # Time offset, global state
│   │   ├── auth.py                 # Signatures (HMAC/RSA/Ed25519)
│   │   ├── http.py                 # aiohttp + connection pool
│   │   ├── exceptions.py           # Exception hierarchy
│   │   ├── decoders.py             # Pre-compiled msgspec decoders
│   │   └── formatters.py           # Price/quantity formatting
│   │
│   ├── api/                        # Generated async methods
│   │   ├── __init__.py
│   │   ├── spot/
│   │   │   ├── __init__.py
│   │   │   ├── general.py          # ping, time, exchange_info
│   │   │   ├── market.py           # klines, depth, ticker
│   │   │   ├── trade.py            # orders, cancel, OCO
│   │   │   └── account.py          # balances, history
│   │   ├── futures_um/
│   │   │   ├── __init__.py
│   │   │   ├── market.py
│   │   │   ├── trade.py
│   │   │   └── account.py
│   │   └── futures_cm/
│   │       └── ...
│   │
│   ├── _schemas/                   # Generated msgspec structs
│   │   ├── __init__.py
│   │   ├── common.py               # BaseStruct, Literals, Constants
│   │   ├── spot.py                 # Spot request/response
│   │   ├── futures.py              # Futures request/response
│   │   └── ws.py                   # WebSocket Tagged Unions (future)
│   │
│   ├── _meta/                      # Generated metadata
│   │   ├── __init__.py
│   │   ├── endpoints.py            # Endpoint definitions
│   │   └── weights.py              # Weight mapping for rate limiter
│   │
│   ├── enums.py                    # Keep existing
│   ├── helpers.py                  # Keep existing
│   └── ws/                         # Keep existing (future optimization)
│
├── tests/
│   ├── unit/
│   └── integration/
│
└── docs/
    └── plans/
        └── binance-wrapper/        # This design document
```

## Hand-written vs Generated

| Hand-written | Generated |
|--------------|-----------|
| `_core/*` (auth, http, exceptions, context) | `api/spot/*`, `api/futures_um/*`, etc. |
| `_schemas/common.py` | `_schemas/spot.py`, `_schemas/futures.py` |
| `generator/*` | `_meta/endpoints.py`, `_meta/weights.py` |
| `client.py` (thin wrapper) | |

## Module Dependencies

```
client.py (entry point)
    │
    ├── api/spot/*.py (generated methods)
    │   │
    │   ├── _schemas/spot.py (msgspec structs)
    │   │   │
    │   │   └── _schemas/common.py (base, literals)
    │   │
    │   └── _core/decoders.py (pre-compiled)
    │
    └── _core/http.py (HTTP client)
        │
        ├── _core/auth.py (signatures)
        │   │
        │   └── _core/context.py (time offset)
        │
        ├── _core/config.py (URLs)
        │
        └── _core/exceptions.py (error handling)
```

**Rule:** Each layer can only import from layers below it. No circular imports.
