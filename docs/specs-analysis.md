# OpenAPI Spec Analysis

Analysis of `specs/openapi/spot/*.yaml` files to catalog all patterns for parser design.

**Total files analyzed:** 382 spot endpoint specs

---

## Response Type Patterns

### 1. Object Response ($ref)
**Example:** `get_api_v3_time.yaml`
```yaml
responses:
  "200":
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/GetTimeV3Resp'
```
**Parser action:** Extract schema name from $ref, generate typed return `TimeResp`.

### 2. Array of Objects (items.$ref)
**Example:** `get_api_v3_trades.yaml`
```yaml
GetTradesV3Resp:
  items:
    $ref: '#/components/schemas/GetTradesV3RespItem'
  type: array
```
**Parser action:** Extract item type from items.$ref, generate `list[TradeItem]` return.

### 3. Raw Array (items.oneOf)
**Example:** `get_api_v3_klines.yaml`
```yaml
schema:
  items:
    items:
      oneOf:
        - type: integer
          format: int64
        - type: string
    type: array
  type: array
```
**Parser action:** Recursively resolve to `list[list[int | str]]`. No schema class needed.

### 4. Response oneOf (array or object)
**Example:** `get_api_v3_ticker_24hr.yaml`
```yaml
SpotGetTicker24hrV3Resp:
  oneOf:
    - type: array
      items:
        $ref: '#/components/schemas/SpotGetTicker24hrV3RespItem'
    - $ref: '#/components/schemas/SpotGetTicker24hrV3RespItem'
```
**Parser action:** Return `list[Item] | Item` or use simpler `list[Item]` (API behavior).

### 5. Object with Nested Array Properties
**Example:** `get_api_v3_depth.yaml`
```yaml
GetDepthV3Resp:
  properties:
    bids:
      items:
        items:
          type: string
        type: array
      type: array
    asks:
      # same structure
    lastUpdateId:
      format: int64
      type: integer
  type: object
```
**Parser action:** Generate Struct with `bids: list[list[str]]`, `asks: list[list[str]]`.

---

## Parameter Patterns

### 1. Required Query Parameter
```yaml
- in: query
  name: symbol
  required: true
  schema:
    default: ""
    type: string
```

### 2. Optional with Default
```yaml
- in: query
  name: limit
  schema:
    default: 500
    maximum: 1000
    type: integer
```

### 3. Enum Parameter
**Example:** `get_api_v3_ticker_24hr.yaml`
```yaml
- in: query
  name: type
  schema:
    default: ""
    enum:
      - FULL
      - MINI
    type: string
```
**Parser action:** Generate `Literal["FULL", "MINI"]` type annotation.

### 4. Int64 Format
```yaml
- in: query
  name: startTime
  schema:
    format: int64
    type: integer
```
**Parser action:** Map to Python `int` (Python ints are arbitrary precision).

### 5. Timestamp Parameter (signed indicator)
```yaml
- in: query
  name: timestamp
  required: true
  schema:
    format: int64
    type: integer
```
**Parser action:** Skip in generated params (auto-added by client). Mark endpoint as signed.

---

## Request Body Patterns (POST/PUT)

### requestBody with $ref
**Example:** `post_api_v3_order.yaml`
```yaml
requestBody:
  content:
    application/x-www-form-urlencoded:
      schema:
        $ref: '#/components/schemas/SpotCreateOrderV3Req'
  required: true
```

**Request schema structure:**
```yaml
SpotCreateOrderV3Req:
  properties:
    symbol:
      type: string
    side:
      type: string
    timestamp:
      format: int64
      type: integer
    # ... more fields
  required:
    - symbol
    - side
    - type
    - timestamp
  type: object
```
**Parser action:** Extract properties from schema, exclude `timestamp`/`signature`, merge with query params.

---

## Security Patterns

### 1. Public Endpoint (no security)
No `security` section in operation. Examples:
- `/api/v3/time`
- `/api/v3/klines`
- `/api/v3/depth`

### 2. Signed Endpoint
**Primary indicator:** `security` section present
```yaml
security:
  - ApiKey: []
```

**Secondary indicator:** Required `timestamp` parameter

**Tertiary indicator:** POST/PUT with requestBody schema

**Example:** `get_api_v3_account.yaml`, `post_api_v3_order.yaml`

### 3. Security Schemes Definition
```yaml
securitySchemes:
  ApiKey:
    in: header
    name: X-MBX-APIKEY
    type: apiKey
```

---

## Schema Patterns

### 1. Flat Object
```yaml
GetTimeV3Resp:
  properties:
    serverTime:
      format: int64
      type: integer
  type: object
```

### 2. Nested Object
**Example:** `get_api_v3_account.yaml`
```yaml
GetAccountV3Resp:
  properties:
    commissionRates:
      properties:
        maker:
          type: string
        taker:
          type: string
      type: object
    # ... more fields
  type: object
```
**Parser action:** For now, generate inline nested structure or flatten.

### 3. Object with Array Property
```yaml
GetAccountV3Resp:
  properties:
    balances:
      items:
        properties:
          asset:
            type: string
          free:
            type: string
          locked:
            type: string
        type: object
      type: array
  type: object
```
**Parser action:** Generate property with `list[dict]` or nested Struct if reused.

### 4. Array Property with Nested Array Items (fills)
**Example:** `post_api_v3_order.yaml`
```yaml
fills:
  type: array
  items:
    type: object
    properties:
      price:
        type: string
      qty:
        type: string
```

### 5. Large Schema (many properties)
**Example:** `get_api_v3_exchangeInfo.yaml` - SpotSymbolFilter with 20+ properties
**Parser action:** Generate all properties, let msgspec handle optional fields.

---

## Edge Cases Found

| Edge Case | Example File | Handling |
|-----------|--------------|----------|
| Empty description fields | Most files | Use empty string or operationId |
| format: int64 on integers | Many files | Map to Python `int` |
| Multiple schemas in one file | `post_api_v3_order.yaml` | Parse all, deduplicate by name |
| Response $ref to array schema | `get_api_v3_trades.yaml` | Check if schema.type == "array" |
| No response schema (inline) | N/A | Return `dict[str, Any]` |
| Schema name conflicts | GetOrderResp, PostOrderResp | Use override file or auto-suffix |
| Inline object in array items | `post_api_v3_order.yaml` (fills) | Generate inline or skip |
| Default empty string | Many params | Treat as `None` for optional |

---

## Missing Patterns (Expected but not found)

| Pattern | Status | Notes |
|---------|--------|-------|
| `x-weight` rate limit extension | **Not found** | Not in spot specs; default to weight=1 |
| Response codes 201/202 | **Not found** | All use 200; support in parser anyway |
| anyOf types | **Not found** | Only oneOf used; handle same way |
| $ref in parameters | **Rare** | Most parameters inline; handle if found |

---

## Pattern Coverage Mapping

| Pattern | Covered in Task |
|---------|-----------------|
| Object response ($ref) | Task 7, 8 |
| Array response (items.$ref) | Task 7, 8 |
| Raw array (oneOf) | Task 7 (resolve_type) |
| Required params | Task 6 |
| Optional with default | Task 6 |
| Enum params → Literal | Task 6 |
| requestBody params | Task 8 |
| Public endpoints | Task 5 (is_signed_endpoint) |
| Signed endpoints | Task 5 (is_signed_endpoint) |
| Nested objects | Task 7 |
| Schema deduplication | Task 9 |

---

## Naming Analysis

### Schema Name Patterns
| Original Name | Smart Inference | Notes |
|--------------|-----------------|-------|
| `GetTimeV3Resp` | `Time` | Strip Get, V3, Resp |
| `GetTradesV3Resp` | `Trade` | + singular |
| `GetTradesV3RespItem` | `TradeItem` | Keep Item suffix |
| `SpotCreateOrderV3Resp` | `CreateOrder` | Strip Spot, V3, Resp |
| `SpotGetTicker24hrV3Resp` | `Ticker24hr` | Strip Spot, Get, V3, Resp |
| `GetDepthV3Resp` | `OrderBook` | **Override needed** (semantic) |

### Operation ID Patterns
| Operation ID | Method Name |
|--------------|-------------|
| `GetTimeV3` | `get_time` |
| `GetKlinesV3` | `get_klines` |
| `CreateOrderV3` | `create_order` |
| `GetTicker24hrV3` | `get_ticker_24hr` |

---

## Recommendations

1. **Default weight to 1** - No x-weight extension found
2. **Support response codes 200, 201, 202, default** - Future-proof
3. **Generate Literal types for enums ≤ 20 values** - Improves type safety
4. **Skip inline nested objects initially** - Can add later if needed
5. **Use overrides.yaml for semantic renames** - Depth → OrderBook
