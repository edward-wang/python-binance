"""Spot API endpoints with typed returns.

Modules:
- general: ping, get_server_time, get_exchange_info
- market: get_klines, get_order_book, get_trades, get_ticker_*
- trade: create_order, cancel_order, get_order
- account: get_account, get_my_trades

All methods return msgspec schema types for type safety.
"""
from binance.api.spot import general, market, trade, account

__all__ = ["general", "market", "trade", "account"]
