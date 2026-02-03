# Section 4: Code Generation System

## Overview

Build-time code generation from OpenXAPI specs.

```
OpenXAPI specs (JSON)
        │
        ▼
   Generator (build-time, run once)
        │
        ├──► binance/api/              # Real async methods
        │
        ├──► binance/_schemas/         # msgspec structs
        │
        └──► binance/_meta/            # Endpoint metadata
```

## Generator Structure

```
generator/
├── __init__.py
├── main.py             # Entry point: python -m generator
├── parser.py           # Parse OpenXAPI specs → internal model
├── emitter.py          # Render templates → .py files
├── config.py           # Naming rules, output paths
└── templates/
    ├── endpoint.py.j2  # API method template
    ├── schema.py.j2    # msgspec struct template
    └── meta.py.j2      # Metadata template
```

## Key Design: Build-time Generation

Generated code is **real Python code**, not runtime dynamic binding.

### Benefits

| Benefit | Why |
|---------|-----|
| Full IDE support | Real signatures, autocomplete works |
| Type safety | Explicit parameters, not `**kwargs` |
| Easy debugging | Real function names in stack traces |
| Fast startup | No runtime generation |
| Module-level decoders | Pre-compiled at import time |

## Output Examples

### `binance/api/spot/market.py` (generated)

```python
"""Spot Market API - Generated from OpenXAPI specs"""
from binance._schemas.spot import Kline, OrderBook, Ticker
from binance._core.decoders import get_decoder

# Pre-compiled decoders (module load time)
_kline_list_decoder = get_decoder(list[Kline])
_order_book_decoder = get_decoder(OrderBook)
_ticker_decoder = get_decoder(Ticker)

async def get_klines(
    self,
    symbol: str,
    interval: str,
    limit: int = 500,
    start_time: int | None = None,
    end_time: int | None = None,
) -> list[Kline]:
    """Get kline/candlestick bars for a symbol.

    GET /api/v3/klines
    Weight: 2

    Args:
        symbol: Trading pair (e.g. BTCUSDT)
        interval: Kline interval (e.g. 1h, 1d)
        limit: Number of results (default 500, max 1000)
        start_time: Start time in milliseconds
        end_time: End time in milliseconds

    Returns:
        List of Kline objects
    """
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time

    raw = await self._request_raw("GET", "/api/v3/klines", params)
    return _kline_list_decoder.decode(raw)


async def get_order_book(
    self,
    symbol: str,
    limit: int = 100,
) -> OrderBook:
    """Get order book depth.

    GET /api/v3/depth
    Weight: 5-50 (depends on limit)

    Args:
        symbol: Trading pair (e.g. BTCUSDT)
        limit: Depth limit (5, 10, 20, 50, 100, 500, 1000, 5000)

    Returns:
        OrderBook with bids and asks
    """
    params = {"symbol": symbol, "limit": limit}
    raw = await self._request_raw("GET", "/api/v3/depth", params)
    return _order_book_decoder.decode(raw)
```

### `binance/_meta/endpoints.py` (generated)

```python
"""Endpoint metadata - Generated from OpenXAPI specs"""
import msgspec

class EndpointMeta(msgspec.Struct, frozen=True):
    """Metadata for a single endpoint."""
    name: str
    path: str
    method: str
    weight: int
    signed: bool
    description: str
    params: tuple[str, ...]

ENDPOINTS: dict[str, EndpointMeta] = {
    "get_klines": EndpointMeta(
        name="get_klines",
        path="/api/v3/klines",
        method="GET",
        weight=2,
        signed=False,
        description="Get kline/candlestick bars for a symbol",
        params=("symbol", "interval", "limit", "startTime", "endTime"),
    ),
    "get_order_book": EndpointMeta(
        name="get_order_book",
        path="/api/v3/depth",
        method="GET",
        weight=10,
        signed=False,
        description="Get order book depth",
        params=("symbol", "limit"),
    ),
    # ... more endpoints
}
```

## Generator Templates

### `templates/endpoint.py.j2`

```jinja2
"""{{ module_doc }} - Generated from OpenXAPI specs"""
from binance._schemas.{{ domain }} import {{ schema_imports | join(', ') }}
from binance._core.decoders import get_decoder

# Pre-compiled decoders (module load time)
{% for endpoint in endpoints %}
{% if endpoint.response_schema %}
_{{ endpoint.name }}_decoder = get_decoder({{ endpoint.response_schema }})
{% endif %}
{% endfor %}

{% for endpoint in endpoints %}
async def {{ endpoint.name }}(
    self,
    {% for param in endpoint.params %}
    {{ param.name }}: {{ param.type }}{% if not param.required %} = {{ param.default }}{% endif %},
    {% endfor %}
) -> {{ endpoint.response_type }}:
    """{{ endpoint.description }}

    {{ endpoint.http_method }} {{ endpoint.path }}
    Weight: {{ endpoint.weight }}

    Args:
        {% for param in endpoint.params %}
        {{ param.name }}: {{ param.description }}
        {% endfor %}

    Returns:
        {{ endpoint.response_description }}
    """
    params = {
        {% for param in endpoint.params if param.required %}
        "{{ param.api_name }}": {{ param.name }},
        {% endfor %}
    }
    {% for param in endpoint.params if not param.required %}
    if {{ param.name }} is not None:
        params["{{ param.api_name }}"] = {{ param.name }}
    {% endfor %}

    raw = await self._request_raw("{{ endpoint.http_method }}", "{{ endpoint.path }}", params)
    return _{{ endpoint.name }}_decoder.decode(raw)

{% endfor %}
```

### `templates/schema.py.j2`

```jinja2
"""{{ module_doc }} - Generated from OpenXAPI specs"""
from typing import Annotated
import msgspec
from binance._schemas.common import BaseStruct

{% for struct in structs %}
class {{ struct.name }}(BaseStruct):
    """{{ struct.description }}"""
    {% for field in struct.fields %}
    {{ field.name }}: Annotated[{{ field.type }}, msgspec.Meta(description="{{ field.description }}")]{% if field.default is not none %} = {{ field.default }}{% endif %}

    {% endfor %}

{% endfor %}
```

## Generator Workflow

```bash
# 1. Download specs (one-time)
curl -o specs/spot.json https://raw.githubusercontent.com/openxapi/openxapi/main/binance/spot.json

# 2. Run generator
python -m generator

# Output:
#   ✓ binance/api/spot/general.py      (12 endpoints)
#   ✓ binance/api/spot/market.py       (18 endpoints)
#   ✓ binance/api/spot/trade.py        (25 endpoints)
#   ✓ binance/api/spot/account.py      (15 endpoints)
#   ✓ binance/_schemas/spot.py         (45 structs)
#   ✓ binance/_meta/endpoints.py       (70 endpoint definitions)

# 3. Review and commit generated code
git add binance/api binance/_schemas binance/_meta
git commit -m "Generate Spot API from OpenXAPI specs"
```
