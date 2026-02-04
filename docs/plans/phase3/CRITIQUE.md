# Phase 3 Plan Critique

## 严重架构风险

### 1. Schema-Endpoint 断层 (Critical)

**问题:** 生成的 `_schemas/spot.py` 完全没有被使用。所有 endpoint 返回 `dict[str, Any]`。

```python
# 当前设计 - 类型信息丢失
async def get_account(self) -> dict[str, Any]:
    return await account.get_account(self._http)

# 用户必须手动解析
result = await client.get_account()
balance = result["balances"][0]["free"]  # 无类型提示，容易出错
```

**影响:**
- msgspec schemas 完全浪费
- 无法利用 IDE 自动补全
- 运行时错误而非编译时错误
- 后期修复需要改所有 method signatures

**修复:** Endpoint 应返回 typed schemas:
```python
async def get_account(self) -> Account:
    raw = await self._http.request_raw("GET", "/api/v3/account", signed=True)
    return msgspec.json.decode(raw, type=Account)
```

### 2. Generator 依赖 - 单点故障 (High)

**问题:** Plan 假设 Phase 2 generator 完美工作，无验证步骤。

**缺失:**
- Task 1 仅检查 `--help`，不验证实际输出
- 无 generator 输出校验
- 无手动实现后备方案

**影响:** 如果 generator 有 bug，整个 Phase 3 卡住。

### 3. AsyncClient 设计缺陷 (High)

**3.1 `__slots__` 过于严格:**
```python
__slots__ = ("_http",)  # 无法添加新属性
```
后期添加 `_rate_limiter`, `_logger` 等需要重构。

**3.2 方法绑定冗余:**
```python
# client.py 中每个方法都是 thin wrapper
async def get_klines(self, symbol, interval, ...) -> list[list[Any]]:
    return await market.get_klines(self._http, symbol, interval, ...)
```
- 20 个 endpoints = 20 次重复
- 参数签名变化需要同步两处
- 违反 DRY 原则

**3.3 无 Futures 扩展考虑:**
- 当前设计只支持 Spot
- 添加 Futures 需要大量重构或创建新 Client 类

### 4. HTTPClient 紧耦合 (Medium)

**问题:** AsyncClient 直接依赖 HTTPClient 具体实现。

```python
self._http = HTTPClient(...)  # 硬依赖
```

**影响:**
- 无法 mock HTTP 层做单元测试
- 无法替换 HTTP 实现
- 测试必须依赖网络

---

## 遗漏的边缘 Case

### 1. API 响应变体

| Endpoint | 单一 Symbol | 多个/无 Symbol |
|----------|------------|----------------|
| `get_ticker_price` | `{symbol, price}` | `[{symbol, price}, ...]` |
| `get_ticker_24h` | `{...}` | `[{...}, ...]` |
| `get_book_ticker` | `{...}` | `[{...}, ...]` |

**当前返回类型:** `dict[str, Any] | list[dict[str, Any]]` - 用户无法知道何时返回哪种。

### 2. 参数验证缺失

- 必填参数 (symbol, side, type) 无运行时验证
- Enum 值 (BUY/SELL, LIMIT/MARKET) 无验证
- 数值范围 (limit 1-1000) 无验证

### 3. 订单边缘情况未测试

- `POST_ONLY` 订单被拒绝 (会立即成交时)
- 自成交防护 (STP) 触发
- 最小名义价值不足 (`MIN_NOTIONAL` filter)
- 步长精度错误 (`LOT_SIZE` filter)
- `ICEBERG` 订单最小数量

### 4. 网络错误场景

- 请求中途连接断开
- DNS 解析失败
- SSL 证书错误
- 代理超时

### 5. 并发场景

- 同时发送多个订单
- 连接池耗尽
- Rate limit 触发后的排队

---

## 测试覆盖不足

### 1. 单元测试缺失 (Critical)

| 模块 | 当前覆盖 | 缺失 |
|------|---------|------|
| `api/spot/general.py` | ❌ 无 | 参数构建、签名标记 |
| `api/spot/market.py` | ❌ 无 | 参数序列化、默认值处理 |
| `api/spot/trade.py` | ❌ 无 | signed=True 验证 |
| `api/spot/account.py` | ❌ 无 | 参数过滤 |
| `_schemas/spot.py` | ⚠️ 仅解码 | 缺少可选字段、额外字段、类型强转 |

**Plan 仅依赖集成测试，无法离线运行。**

### 2. 错误路径测试缺失

```python
# 需要但缺失的测试
def test_invalid_symbol_raises_error():
    with pytest.raises(InvalidSymbolError):
        await client.get_klines(symbol="INVALID", interval="1h")

def test_missing_required_param_raises_error():
    with pytest.raises(TypeError):
        await client.create_order(symbol="BTCUSDT")  # 缺少 side, type
```

### 3. Mock 测试缺失

当前所有测试都需要网络连接，无法:
- CI 中快速运行
- 测试特定错误场景
- 验证请求参数正确性

### 4. 并发测试缺失

```python
# 需要但缺失
async def test_concurrent_requests():
    tasks = [client.get_ticker_price(symbol=s) for s in symbols]
    results = await asyncio.gather(*tasks)
```

---

## 可能导致重构的地方

### 1. 返回类型从 dict 改为 Schema (100% 会发生)

当用户要求类型安全时:
```python
# 需要修改所有 20+ 方法
- async def get_account(self) -> dict[str, Any]:
+ async def get_account(self) -> Account:
```

### 2. 添加 Futures 支持

当前 AsyncClient 硬编码 Spot，添加 Futures 选项:
- 修改 `__init__` 参数
- 添加 base_url 切换逻辑
- 或创建 `FuturesClient` 子类

### 3. 添加中间件/Hook 支持

用户需要:
- 请求日志
- 响应缓存
- Rate limit 预检

当前架构不支持，需要重构 HTTPClient 或 AsyncClient。

### 4. 方法绑定方式

当前手动写 20 个 wrapper methods，后续:
- 添加新 endpoint 需要改两处
- 考虑用 `__getattr__` 动态绑定或 descriptor

---

## 改进建议 (按优先级)

### P0 - 必须修复

1. **Endpoint 返回 typed schemas**
   - 修改 `api/spot/*.py` 返回 msgspec structs
   - 使用 `_core/decoders.py` 预编译 decoder

2. **添加 generator 输出验证**
   - Task 1 增加: 生成一个文件并验证语法
   - 添加 generator smoke test

3. **添加单元测试 for generated code**
   - Mock HTTPClient
   - 验证参数构建
   - 验证 signed 标记

### P1 - 应该修复

4. **添加错误场景测试**
   - Invalid symbol
   - Missing required params
   - Rate limit response

5. **修改返回类型文档**
   - 明确说明 single vs array 响应

6. **放宽 `__slots__`**
   - 或改用常规属性

### P2 - 可以改进

7. **添加 Protocol for HTTPClient**
   - 便于 mock 测试

8. **考虑动态方法绑定**
   - 减少代码重复

9. **添加请求 ID 追踪**
   - 便于调试

---

## 需要更新的 Plan 文件

| 文件 | 修改内容 |
|------|---------|
| `00-overview.md` | 添加 Prerequisites 验证步骤 |
| `01-generate-endpoints.md` | 添加 generator 输出验证、typed returns |
| `02-generate-schemas.md` | 添加 decoder 集成、更多 schema 测试 |
| `03-async-client.md` | 使用 typed returns、添加单元测试 |
| `04-integration-testing.md` | 添加错误场景测试、Mock 测试 |
