# Phase 5.2: Documentation

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create comprehensive README.md with installation, quick start, and usage examples.

**Prerequisites:** Tasks 1-4 complete (type annotations done)

---

## Task 5: Create README.md Quick Start

**Files:**
- Create: `README.md`

**Step 1: Check if README exists**

```bash
ls -la README* 2>/dev/null
# Note: README.rst may exist (legacy) - we'll create README.md
```

**Step 2: Create README.md with quick start**

```markdown
# Binance Python Wrapper

High-performance async Python client for Binance Spot and Futures APIs.

## Features

- **Async-first**: Built on aiohttp with connection pooling
- **Type-safe**: Full typing with msgspec schemas
- **Fast**: Pre-compiled JSON decoders, orjson serialization
- **Complete**: Spot + USDT-M + COIN-M Futures support

## Installation

```bash
pip install python-binance
```

## Quick Start

```python
import asyncio
from binance import AsyncClient

async def main():
    async with AsyncClient() as client:
        # Get Bitcoin price
        ticker = await client.get_ticker_price(symbol="BTCUSDT")
        print(f"BTC: ${ticker.price}")

asyncio.run(main())
```

## Authentication

```python
async with AsyncClient(
    api_key="your_api_key",
    api_secret="your_api_secret",
) as client:
    # Access authenticated endpoints
    account = await client.get_account()
    print(f"BTC Balance: {account.balances[0].free}")
```

## Testnet

```python
# Use Binance testnet for development
async with AsyncClient(
    api_key="testnet_key",
    api_secret="testnet_secret",
    testnet=True,
) as client:
    # All requests go to testnet
    await client.create_order(
        symbol="BTCUSDT",
        side="BUY",
        type="MARKET",
        quantity="0.001",
    )
```

## Spot API Examples

### Market Data

```python
# Klines (candlesticks)
klines = await client.get_klines(
    symbol="BTCUSDT",
    interval="1h",
    limit=100,
)
for k in klines:
    print(f"{k.open_time}: O={k.open} H={k.high} L={k.low} C={k.close}")

# Order book
depth = await client.get_order_book(symbol="BTCUSDT", limit=10)
print(f"Best bid: {depth.bids[0]}")
print(f"Best ask: {depth.asks[0]}")

# 24h ticker
ticker = await client.get_ticker_24h(symbol="BTCUSDT")
print(f"24h change: {ticker.price_change_percent}%")
```

### Trading

```python
# Place limit order
order = await client.create_order(
    symbol="BTCUSDT",
    side="BUY",
    type="LIMIT",
    quantity="0.001",
    price="50000.00",
    time_in_force="GTC",
)
print(f"Order ID: {order.order_id}")

# Check order status
status = await client.get_order(
    symbol="BTCUSDT",
    order_id=order.order_id,
)
print(f"Status: {status.status}")

# Cancel order
cancelled = await client.cancel_order(
    symbol="BTCUSDT",
    order_id=order.order_id,
)
print(f"Cancelled: {cancelled.order_id}")
```

### Account

```python
# Account info
account = await client.get_account()
for balance in account.balances:
    if float(balance.free) > 0:
        print(f"{balance.asset}: {balance.free}")

# Trade history
trades = await client.get_my_trades(symbol="BTCUSDT", limit=10)
for trade in trades:
    print(f"{trade.time}: {trade.side} {trade.qty} @ {trade.price}")
```

## Futures API Examples

### USDT-M Futures

```python
# Mark price and funding rate
mark = await client.futures_get_mark_price(symbol="BTCUSDT")
print(f"Mark: {mark.mark_price}, Funding: {mark.last_funding_rate}")

# Position info
positions = await client.futures_get_position_risk(symbol="BTCUSDT")
for pos in positions:
    print(f"{pos.symbol}: {pos.position_amt} @ {pos.entry_price}")

# Set leverage
result = await client.futures_set_leverage(symbol="BTCUSDT", leverage=10)
print(f"Leverage set to {result.leverage}x")

# Place futures order
order = await client.futures_create_order(
    symbol="BTCUSDT",
    side="BUY",
    type="MARKET",
    quantity="0.001",
)
print(f"Futures order: {order.order_id}")
```

### COIN-M Futures

```python
# COIN-M uses different symbols (e.g., BTCUSD_PERP)
klines = await client.futures_coin_get_klines(
    symbol="BTCUSD_PERP",
    interval="1h",
    limit=10,
)

order = await client.futures_coin_create_order(
    symbol="BTCUSD_PERP",
    side="BUY",
    type="MARKET",
    quantity="1",  # 1 contract
)
```

## Error Handling

```python
from binance._core.exceptions import (
    BinanceAPIError,
    InvalidSymbolError,
    RateLimitError,
)

try:
    await client.get_order_book(symbol="INVALID")
except InvalidSymbolError as e:
    print(f"Invalid symbol: {e.message}")
except RateLimitError as e:
    print(f"Rate limited: {e.message}")
except BinanceAPIError as e:
    print(f"API error {e.code}: {e.message}")
```

## Concurrent Requests

```python
import asyncio

# Fetch multiple symbols concurrently
symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
tasks = [client.get_ticker_price(symbol=s) for s in symbols]
results = await asyncio.gather(*tasks)

for ticker in results:
    print(f"{ticker.symbol}: {ticker.price}")
```

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `api_key` | `""` | API key for authenticated endpoints |
| `api_secret` | `""` | API secret for signing |
| `testnet` | `False` | Use testnet URLs |
| `timeout` | `10.0` | Request timeout in seconds |

## Type Safety

All responses are typed msgspec structs:

```python
from binance._schemas.spot import Order, Account, Kline
from binance._schemas.futures import FuturesOrder, PositionRisk

# IDE autocomplete works
order: Order = await client.create_order(...)
print(order.order_id)  # Typed as int
print(order.status)    # Typed as str
```

## Requirements

- Python 3.11+
- aiohttp
- msgspec
- orjson

## License

MIT
```

**Step 3: Verify README renders correctly**

```bash
# Check markdown syntax
head -100 README.md
```

**Step 4: Commit**

```bash
git add README.md
git commit -m "docs: add comprehensive README.md

- Installation and quick start
- Spot API examples (market data, trading, account)
- Futures API examples (USDT-M and COIN-M)
- Error handling patterns
- Configuration options

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 6: Add Usage Examples Directory

**Files:**
- Create: `examples/__init__.py`
- Create: `examples/spot_market_data.py`
- Create: `examples/futures_trading.py`

**Step 1: Create examples directory**

```bash
mkdir -p examples
```

**Step 2: Create spot market data example**

```python
# examples/spot_market_data.py
"""Example: Fetching spot market data."""
import asyncio

from binance import AsyncClient


async def main() -> None:
    async with AsyncClient() as client:
        # Get server time
        time = await client.get_server_time()
        print(f"Server time: {time.server_time}")

        # Get ticker prices
        btc = await client.get_ticker_price(symbol="BTCUSDT")
        eth = await client.get_ticker_price(symbol="ETHUSDT")
        print(f"BTC: ${btc.price}")
        print(f"ETH: ${eth.price}")

        # Get klines
        klines = await client.get_klines(
            symbol="BTCUSDT",
            interval="1h",
            limit=5,
        )
        print("\nRecent 1h candles:")
        for k in klines:
            print(f"  {k.open_time}: O={k.open} C={k.close}")

        # Get order book
        depth = await client.get_order_book(symbol="BTCUSDT", limit=5)
        print(f"\nOrder book (top 5):")
        print(f"  Bids: {depth.bids[:3]}")
        print(f"  Asks: {depth.asks[:3]}")


if __name__ == "__main__":
    asyncio.run(main())
```

**Step 3: Create futures trading example**

```python
# examples/futures_trading.py
"""Example: Futures trading on testnet.

Requires BINANCE_FUTURES_TESTNET_API_KEY and BINANCE_FUTURES_TESTNET_API_SECRET
environment variables.
"""
import asyncio
import os

from binance import AsyncClient


async def main() -> None:
    api_key = os.environ.get("BINANCE_FUTURES_TESTNET_API_KEY", "")
    api_secret = os.environ.get("BINANCE_FUTURES_TESTNET_API_SECRET", "")

    if not api_key or not api_secret:
        print("Set BINANCE_FUTURES_TESTNET_API_KEY and BINANCE_FUTURES_TESTNET_API_SECRET")
        return

    async with AsyncClient(
        api_key=api_key,
        api_secret=api_secret,
        testnet=True,
    ) as client:
        # Get mark price
        mark = await client.futures_get_mark_price(symbol="BTCUSDT")
        print(f"Mark price: {mark.mark_price}")
        print(f"Funding rate: {mark.last_funding_rate}")

        # Get account info
        account = await client.futures_get_account()
        print(f"\nAccount balance: {account.total_wallet_balance} USDT")
        print(f"Available: {account.available_balance} USDT")

        # Get positions
        positions = await client.futures_get_position_risk(symbol="BTCUSDT")
        for pos in positions:
            if float(pos.position_amt) != 0:
                print(f"\nPosition: {pos.position_amt} @ {pos.entry_price}")
                print(f"Unrealized PnL: {pos.un_realized_profit}")

        # Set leverage (safe level)
        leverage = await client.futures_set_leverage(symbol="BTCUSDT", leverage=1)
        print(f"\nLeverage: {leverage.leverage}x")

        # Place test order (doesn't execute)
        result = await client.futures_create_test_order(
            symbol="BTCUSDT",
            side="BUY",
            type="LIMIT",
            quantity="0.001",
            price="50000",
            time_in_force="GTC",
        )
        print(f"Test order result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
```

**Step 4: Create __init__.py**

```python
# examples/__init__.py
"""Example scripts for the Binance Python wrapper."""
```

**Step 5: Run examples to verify they work**

```bash
# Public example (no auth needed)
python examples/spot_market_data.py
# Expected: Prints BTC/ETH prices, klines, order book
```

**Step 6: Commit**

```bash
git add examples/
git commit -m "docs: add usage examples

- spot_market_data.py: Public market data fetching
- futures_trading.py: Futures testnet trading example

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 7: Update Package Metadata

**Files:**
- Modify: `pyproject.toml`

**Step 1: Read current pyproject.toml**

```bash
cat pyproject.toml
```

**Step 2: Update project metadata**

Ensure these fields are set:

```toml
[project]
name = "python-binance"
version = "2.0.0"
description = "High-performance async Python client for Binance APIs"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.11"
keywords = ["binance", "cryptocurrency", "trading", "api", "async"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Office/Business :: Financial :: Investment",
    "Typing :: Typed",
]

[project.urls]
Homepage = "https://github.com/sammchardy/python-binance"
Documentation = "https://github.com/sammchardy/python-binance#readme"
Repository = "https://github.com/sammchardy/python-binance"
```

**Step 3: Commit**

```bash
git add pyproject.toml
git commit -m "chore: update package metadata

- Add description, keywords, classifiers
- Link to README.md
- Set version 2.0.0

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 8: Create CHANGELOG Entry

**Files:**
- Create or modify: `CHANGELOG.md`

**Step 1: Create CHANGELOG.md**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2026-02-06

### Added
- **Async-only client**: New `AsyncClient` with typed returns
- **Type safety**: All responses return msgspec structs, not dicts
- **Futures support**: USDT-M and COIN-M Futures APIs
- **Pre-compiled decoders**: Fast JSON parsing with msgspec
- **Connection pooling**: Efficient HTTP connection reuse

### Changed
- Minimum Python version: 3.11+
- Removed sync client (use `asyncio.run()` instead)
- All methods return typed schemas instead of raw dicts

### API Methods

#### Spot
- `ping()`, `get_server_time()`, `get_exchange_info()`
- `get_klines()`, `get_order_book()`, `get_ticker_price()`, `get_ticker_24h()`
- `create_order()`, `cancel_order()`, `get_order()`, `get_open_orders()`
- `get_account()`, `get_my_trades()`

#### USDT-M Futures
- `futures_ping()`, `futures_get_server_time()`, `futures_get_exchange_info()`
- `futures_get_klines()`, `futures_get_mark_price()`, `futures_get_funding_rate()`
- `futures_create_order()`, `futures_cancel_order()`, `futures_get_order()`
- `futures_get_account()`, `futures_get_balance()`, `futures_get_position_risk()`
- `futures_set_leverage()`, `futures_set_margin_type()`

#### COIN-M Futures
- `futures_coin_ping()`, `futures_coin_get_exchange_info()`
- `futures_coin_get_klines()`, `futures_coin_get_mark_price()`
- `futures_coin_create_order()`, `futures_coin_get_account()`

### Schemas

New typed response schemas in `binance._schemas`:
- `spot.py`: `Order`, `Account`, `Kline`, `OrderBook`, `TickerPrice`, etc.
- `futures.py`: `FuturesOrder`, `FuturesAccount`, `PositionRisk`, `MarkPrice`, etc.
```

**Step 2: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs: add CHANGELOG.md for v2.0.0

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Verification

After completing all tasks:

```bash
# README exists and is readable
head -50 README.md

# Examples run without errors
python examples/spot_market_data.py

# Package metadata is valid
python -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['name'])"

# Expected output: python-binance
```
