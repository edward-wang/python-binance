"""COIN-Margined (CM) Futures API endpoints with typed returns.

Modules:
- general: ping, get_server_time, get_exchange_info
- market: get_klines, get_order_book, get_mark_price, get_funding_rate
- trade: create_order, cancel_order, get_order, get_open_orders
- account: get_account, get_balance, get_position_risk, set_leverage

All methods return msgspec schema types for type safety.
Base URL: https://dapi.binance.com (production) / https://testnet.binancefuture.com (testnet)
"""
from binance.api.futures_cm import general, market, trade, account

__all__ = ["general", "market", "trade", "account"]
