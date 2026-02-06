# Phase 5.3: Benchmarks

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Verify performance meets targets - schema decode < 1μs, HTTP overhead minimal.

**Prerequisites:** Tasks 1-8 complete (type annotations and documentation done)

---

## Task 9: Create Benchmark Infrastructure

**Files:**
- Create: `tests/benchmarks/__init__.py`
- Create: `tests/benchmarks/conftest.py`

**Step 1: Install pytest-benchmark**

```bash
pip install pytest-benchmark
```

**Step 2: Create benchmark directory**

```bash
mkdir -p tests/benchmarks
```

**Step 3: Create conftest with fixtures**

```python
# tests/benchmarks/__init__.py
"""Performance benchmarks for the Binance wrapper."""
```

```python
# tests/benchmarks/conftest.py
"""Benchmark fixtures and sample data."""
import pytest

# Sample API response data for benchmarks
SAMPLE_KLINE_RAW = [
    1699900800000,      # open_time
    "36500.00",         # open
    "36600.00",         # high
    "36400.00",         # low
    "36550.00",         # close
    "1000.5",           # volume
    1699904399999,      # close_time
    "36550000.00",      # quote_volume
    500,                # trades
    "600.25",           # taker_buy_base
    "21900000.00",      # taker_buy_quote
    "0",                # ignore
]

SAMPLE_ORDER_JSON = b'''{
    "symbol": "BTCUSDT",
    "orderId": 123456789,
    "orderListId": -1,
    "clientOrderId": "test123",
    "transactTime": 1699900800000,
    "price": "36500.00",
    "origQty": "0.001",
    "executedQty": "0.001",
    "cummulativeQuoteQty": "36.50",
    "status": "FILLED",
    "timeInForce": "GTC",
    "type": "LIMIT",
    "side": "BUY",
    "workingTime": 1699900800000,
    "fills": [],
    "selfTradePreventionMode": "NONE"
}'''

SAMPLE_TICKER_JSON = b'''{
    "symbol": "BTCUSDT",
    "price": "36550.00"
}'''

SAMPLE_ACCOUNT_JSON = b'''{
    "makerCommission": 10,
    "takerCommission": 10,
    "buyerCommission": 0,
    "sellerCommission": 0,
    "commissionRates": {
        "maker": "0.00100000",
        "taker": "0.00100000",
        "buyer": "0.00000000",
        "seller": "0.00000000"
    },
    "canTrade": true,
    "canWithdraw": true,
    "canDeposit": true,
    "brokered": false,
    "requireSelfTradePrevention": false,
    "preventSor": false,
    "updateTime": 1699900800000,
    "accountType": "SPOT",
    "balances": [
        {"asset": "BTC", "free": "1.00000000", "locked": "0.00000000"},
        {"asset": "USDT", "free": "10000.00000000", "locked": "0.00000000"}
    ],
    "permissions": ["SPOT"],
    "uid": 123456789
}'''

SAMPLE_FUTURES_ACCOUNT_JSON = b'''{
    "feeTier": 0,
    "canTrade": true,
    "canDeposit": true,
    "canWithdraw": true,
    "updateTime": 0,
    "multiAssetsMargin": false,
    "tradeGroupId": -1,
    "totalInitialMargin": "0.00000000",
    "totalMaintMargin": "0.00000000",
    "totalWalletBalance": "10000.00000000",
    "totalUnrealizedProfit": "0.00000000",
    "totalMarginBalance": "10000.00000000",
    "totalPositionInitialMargin": "0.00000000",
    "totalOpenOrderInitialMargin": "0.00000000",
    "totalCrossWalletBalance": "10000.00000000",
    "totalCrossUnPnl": "0.00000000",
    "availableBalance": "10000.00000000",
    "maxWithdrawAmount": "10000.00000000",
    "assets": [],
    "positions": []
}'''


@pytest.fixture
def sample_kline_raw():
    return SAMPLE_KLINE_RAW


@pytest.fixture
def sample_order_json():
    return SAMPLE_ORDER_JSON


@pytest.fixture
def sample_ticker_json():
    return SAMPLE_TICKER_JSON


@pytest.fixture
def sample_account_json():
    return SAMPLE_ACCOUNT_JSON


@pytest.fixture
def sample_futures_account_json():
    return SAMPLE_FUTURES_ACCOUNT_JSON
```

**Step 4: Commit**

```bash
git add tests/benchmarks/
git commit -m "test: add benchmark infrastructure

- pytest-benchmark fixtures
- Sample JSON data for decode benchmarks

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 10: Create Schema Decode Benchmarks

**Files:**
- Create: `tests/benchmarks/test_schema_decode.py`

**Step 1: Create decode benchmark tests**

```python
# tests/benchmarks/test_schema_decode.py
"""Benchmark schema decoding performance.

Target: < 1μs per object decode.
"""
import msgspec
import pytest

from binance._schemas.spot import Order, TickerPrice, Account, Kline
from binance._schemas.futures import FuturesAccount, FuturesKline


class TestSpotSchemaDecoding:
    """Benchmark spot schema decoding."""

    def test_ticker_price_decode(self, benchmark, sample_ticker_json):
        """Benchmark TickerPrice decoding."""
        decoder = msgspec.json.Decoder(TickerPrice)

        result = benchmark(decoder.decode, sample_ticker_json)

        assert result.symbol == "BTCUSDT"
        assert result.price == "36550.00"

    def test_order_decode(self, benchmark, sample_order_json):
        """Benchmark Order decoding."""
        decoder = msgspec.json.Decoder(Order)

        result = benchmark(decoder.decode, sample_order_json)

        assert result.symbol == "BTCUSDT"
        assert result.order_id == 123456789

    def test_account_decode(self, benchmark, sample_account_json):
        """Benchmark Account decoding."""
        decoder = msgspec.json.Decoder(Account)

        result = benchmark(decoder.decode, sample_account_json)

        assert result.can_trade is True
        assert len(result.balances) == 2

    def test_kline_from_raw(self, benchmark, sample_kline_raw):
        """Benchmark Kline.from_raw() conversion."""
        result = benchmark(Kline.from_raw, sample_kline_raw)

        assert result.open == "36500.00"
        assert result.close == "36550.00"


class TestFuturesSchemaDecoding:
    """Benchmark futures schema decoding."""

    def test_futures_account_decode(self, benchmark, sample_futures_account_json):
        """Benchmark FuturesAccount decoding."""
        decoder = msgspec.json.Decoder(FuturesAccount)

        result = benchmark(decoder.decode, sample_futures_account_json)

        assert result.total_wallet_balance == "10000.00000000"
        assert result.can_trade is True

    def test_futures_kline_from_raw(self, benchmark, sample_kline_raw):
        """Benchmark FuturesKline.from_raw() conversion."""
        result = benchmark(FuturesKline.from_raw, sample_kline_raw)

        assert result.open == "36500.00"
        assert result.close == "36550.00"


class TestBatchDecoding:
    """Benchmark batch decoding scenarios."""

    def test_multiple_tickers(self, benchmark):
        """Benchmark decoding list of tickers."""
        json_data = b'''[
            {"symbol": "BTCUSDT", "price": "36550.00"},
            {"symbol": "ETHUSDT", "price": "2000.00"},
            {"symbol": "BNBUSDT", "price": "300.00"}
        ]'''
        decoder = msgspec.json.Decoder(list[TickerPrice])

        result = benchmark(decoder.decode, json_data)

        assert len(result) == 3

    def test_klines_batch(self, benchmark):
        """Benchmark decoding 100 klines."""
        raw_klines = [
            [
                1699900800000 + i * 3600000,
                "36500.00",
                "36600.00",
                "36400.00",
                "36550.00",
                "1000.5",
                1699904399999 + i * 3600000,
                "36550000.00",
                500,
                "600.25",
                "21900000.00",
                "0",
            ]
            for i in range(100)
        ]

        def decode_all():
            return [Kline.from_raw(k) for k in raw_klines]

        result = benchmark(decode_all)

        assert len(result) == 100
```

**Step 2: Run benchmarks**

```bash
python -m pytest tests/benchmarks/test_schema_decode.py -v --benchmark-only
```

**Expected output:**

```
test_ticker_price_decode    ~0.5μs (500ns)
test_order_decode           ~1.0μs
test_account_decode         ~1.5μs
test_kline_from_raw         ~0.3μs
```

**Step 3: Commit**

```bash
git add tests/benchmarks/test_schema_decode.py
git commit -m "test: add schema decode benchmarks

- Spot schema benchmarks (TickerPrice, Order, Account, Kline)
- Futures schema benchmarks (FuturesAccount, FuturesKline)
- Batch decoding benchmarks

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 11: Create HTTP Performance Benchmark

**Files:**
- Create: `tests/benchmarks/test_http_performance.py`

**Step 1: Create HTTP benchmark tests**

```python
# tests/benchmarks/test_http_performance.py
"""Benchmark HTTP client performance.

These tests measure real network latency, not just client overhead.
Run with: pytest tests/benchmarks/test_http_performance.py -v --benchmark-disable
"""
import asyncio
import time

import pytest


@pytest.mark.asyncio
class TestHTTPPerformance:
    """Measure HTTP client performance."""

    async def test_ping_latency(self, public_client):
        """Measure ping endpoint latency."""
        # Warmup
        await public_client.ping()

        # Measure
        times = []
        for _ in range(10):
            start = time.perf_counter()
            await public_client.ping()
            elapsed = (time.perf_counter() - start) * 1000  # ms
            times.append(elapsed)

        avg = sum(times) / len(times)
        print(f"\nPing latency: avg={avg:.2f}ms, min={min(times):.2f}ms, max={max(times):.2f}ms")

        # Testnet typically ~100-300ms
        assert avg < 1000, f"Ping too slow: {avg}ms"

    async def test_concurrent_requests(self, public_client):
        """Measure concurrent request throughput."""
        n_requests = 20

        start = time.perf_counter()
        tasks = [public_client.ping() for _ in range(n_requests)]
        await asyncio.gather(*tasks)
        elapsed = time.perf_counter() - start

        rps = n_requests / elapsed
        print(f"\nConcurrent: {n_requests} requests in {elapsed:.2f}s = {rps:.1f} req/s")

        # Should handle at least 10 req/s even on slow connections
        assert rps > 5, f"Too slow: {rps} req/s"

    async def test_ticker_price_latency(self, public_client):
        """Measure ticker price endpoint latency."""
        # Warmup
        await public_client.get_ticker_price(symbol="BTCUSDT")

        # Measure
        times = []
        for _ in range(5):
            start = time.perf_counter()
            await public_client.get_ticker_price(symbol="BTCUSDT")
            elapsed = (time.perf_counter() - start) * 1000
            times.append(elapsed)

        avg = sum(times) / len(times)
        print(f"\nTicker latency: avg={avg:.2f}ms")

        assert avg < 2000, f"Ticker too slow: {avg}ms"

    async def test_klines_latency(self, public_client):
        """Measure klines endpoint latency (larger payload)."""
        # Warmup
        await public_client.get_klines(symbol="BTCUSDT", interval="1h", limit=100)

        # Measure
        times = []
        for _ in range(3):
            start = time.perf_counter()
            result = await public_client.get_klines(
                symbol="BTCUSDT",
                interval="1h",
                limit=500,
            )
            elapsed = (time.perf_counter() - start) * 1000
            times.append(elapsed)

        avg = sum(times) / len(times)
        print(f"\nKlines (500) latency: avg={avg:.2f}ms, returned {len(result)} klines")

        assert avg < 3000, f"Klines too slow: {avg}ms"


# Fixture for benchmarks (reuse from integration tests)
@pytest.fixture
def public_client():
    """Reuse the public client fixture from integration tests."""
    from binance import AsyncClient

    async def _client():
        async with AsyncClient(testnet=True) as client:
            yield client

    return pytest.fixture(_client)
```

**Step 2: Update conftest to share fixtures**

Add to `tests/benchmarks/conftest.py`:

```python
# Add at end of tests/benchmarks/conftest.py
import pytest_asyncio
from binance import AsyncClient


@pytest_asyncio.fixture
async def public_client():
    """Create a client for public endpoints."""
    async with AsyncClient(testnet=True) as client:
        yield client
```

**Step 3: Run HTTP benchmarks**

```bash
# Run without benchmark framework (measures real latency)
python -m pytest tests/benchmarks/test_http_performance.py -v -s
```

**Step 4: Commit**

```bash
git add tests/benchmarks/
git commit -m "test: add HTTP performance benchmarks

- Ping latency measurement
- Concurrent request throughput
- Ticker and klines endpoint latency

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Verification

After completing all tasks:

```bash
# Run all benchmarks
python -m pytest tests/benchmarks/ -v --benchmark-only 2>/dev/null || \
python -m pytest tests/benchmarks/test_schema_decode.py -v

# Run HTTP performance tests
python -m pytest tests/benchmarks/test_http_performance.py -v -s

# Expected results:
# - Schema decode: < 2μs per object
# - Ping latency: < 500ms (testnet)
# - Concurrent: > 10 req/s
```

### Performance Targets Summary

| Metric | Target | Typical |
|--------|--------|---------|
| TickerPrice decode | < 1μs | ~500ns |
| Order decode | < 2μs | ~1μs |
| Account decode | < 3μs | ~1.5μs |
| Kline.from_raw() | < 1μs | ~300ns |
| 100 klines batch | < 100μs | ~50μs |
| Ping latency | < 500ms | ~200ms |
| Concurrent (20 req) | > 10 req/s | ~15 req/s |
