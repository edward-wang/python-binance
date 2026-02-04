"""Binance Python Wrapper

High-performance, async-only Python wrapper for Binance API with typed returns.

Usage:
    from binance import AsyncClient

    async with AsyncClient(api_key="...", api_secret="...") as client:
        # Get market data - returns typed schemas
        ticker = await client.get_ticker_price(symbol="BTCUSDT")
        print(ticker.price)  # IDE autocomplete works!

        # Get account info
        account = await client.get_account()
        for balance in account.balances:
            if float(balance.free) > 0:
                print(f"{balance.asset}: {balance.free}")

        # Place order
        order = await client.create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="MARKET",
            quantity="0.001",
        )
        print(f"Order {order.order_id} status: {order.status}")
"""

__version__ = "2.0.0"

# Main client (new typed API)
from binance.client import AsyncClient

# Exceptions and enums (preserved)
from binance.exceptions import *  # noqa
from binance.enums import *  # noqa

__all__ = [
    "__version__",
    "AsyncClient",
]
