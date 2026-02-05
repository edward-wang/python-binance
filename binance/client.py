"""AsyncClient - Main entry point for Binance API.

This thin wrapper provides typed method signatures for all endpoints.
All methods return msgspec schema types (not raw dicts).

Usage:
    async with AsyncClient(api_key="...", api_secret="...") as client:
        # Market data (public) - returns typed schemas
        klines = await client.get_klines(symbol="BTCUSDT", interval="1h")

        # Account data (signed) - returns Account schema
        account = await client.get_account()
        print(account.balances[0].asset)  # IDE autocomplete works!

        # Trading (signed) - returns Order schema
        order = await client.create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="MARKET",
            quantity="0.001",
        )
        print(order.order_id)  # Typed access

        # Futures API - lazy initialized on first use
        mark_price = await client.futures_get_mark_price(symbol="BTCUSDT")
        print(mark_price.mark_price)
"""
from typing import Any, overload

from binance._core.config import get_base_url
from binance._core.http import HTTPClient
from binance._schemas.spot import (
    Account,
    AggTrade,
    AvgPrice,
    BookTicker,
    CancelOrderResult,
    ExchangeInfo,
    Kline,
    MyTrade,
    Order,
    OrderBook,
    QueryOrder,
    ServerTime,
    Ticker24h,
    TickerPrice,
    Trade,
)
from binance._schemas.futures import (
    FuturesExchangeInfo,
    FuturesKline,
    FuturesOrder,
    FuturesAccount,
    FuturesBalance,
    PositionRisk,
    MarkPrice,
    FundingRate,
    LeverageResult,
    FuturesTicker24h,
    FuturesMyTrade,
    BatchOrderError,
)
from binance.api.spot import account, general, market, trade
from binance.api import futures_um, futures_cm


class AsyncClient:
    """Async client for Binance API.

    Supports Spot, USDT-M Futures, and COIN-M Futures APIs.
    All methods are async and must be awaited.
    Use as async context manager for automatic connection handling.

    All endpoint methods return typed msgspec schemas for type safety.

    Futures clients are lazily initialized on first use to avoid
    unnecessary connections when only using spot API.
    """

    __slots__ = (
        "_http",
        "__http_futures_um",
        "__http_futures_cm",
        "_api_key",
        "_api_secret",
        "_testnet",
        "_timeout",
    )

    def __init__(
        self,
        api_key: str = "",
        api_secret: str = "",
        testnet: bool = False,
        base_url: str | None = None,
        timeout: float = 10.0,
    ) -> None:
        """Initialize AsyncClient.

        Args:
            api_key: Binance API key (required for authenticated endpoints)
            api_secret: Binance API secret (required for signed endpoints)
            testnet: Use testnet URLs if True
            base_url: Override spot base URL (ignores testnet if set)
            timeout: Request timeout in seconds
        """
        # Store for lazy init of futures clients
        self._api_key = api_key
        self._api_secret = api_secret
        self._testnet = testnet
        self._timeout = timeout

        # Spot API - always initialized
        spot_url = base_url or get_base_url("spot", testnet)
        self._http = HTTPClient(
            api_key=api_key,
            api_secret=api_secret,
            base_url=spot_url,
            timeout=timeout,
            time_sync_path="/api/v3/time",  # Spot time sync
        )

        # Futures clients - lazy initialized
        self.__http_futures_um: HTTPClient | None = None
        self.__http_futures_cm: HTTPClient | None = None

    @property
    def _http_futures_um(self) -> HTTPClient:
        """Get USDT-M futures HTTP client (lazy initialized)."""
        if self.__http_futures_um is None:
            self.__http_futures_um = HTTPClient(
                api_key=self._api_key,
                api_secret=self._api_secret,
                base_url=get_base_url("futures_um", self._testnet),
                timeout=self._timeout,
                time_sync_path=None,  # Share offset from spot client
            )
        return self.__http_futures_um

    @property
    def _http_futures_cm(self) -> HTTPClient:
        """Get COIN-M futures HTTP client (lazy initialized)."""
        if self.__http_futures_cm is None:
            self.__http_futures_cm = HTTPClient(
                api_key=self._api_key,
                api_secret=self._api_secret,
                base_url=get_base_url("futures_cm", self._testnet),
                timeout=self._timeout,
                time_sync_path=None,  # Share offset from spot client
            )
        return self.__http_futures_cm

    async def __aenter__(self) -> "AsyncClient":
        """Async context manager entry."""
        await self._http.connect()
        # Futures clients connect lazily on first use
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit."""
        await self.close()

    async def connect(self) -> None:
        """Initialize spot connection pool.

        Futures clients connect lazily on first use.
        Called automatically when using `async with AsyncClient()`.
        Call manually if not using context manager.
        """
        await self._http.connect()

    async def close(self) -> None:
        """Close all connection pools.

        Called automatically when using `async with AsyncClient()`.
        Call manually if not using context manager.
        """
        await self._http.close()
        if self.__http_futures_um is not None:
            await self.__http_futures_um.close()
        if self.__http_futures_cm is not None:
            await self.__http_futures_cm.close()

    async def _ensure_futures_um_connected(self) -> HTTPClient:
        """Ensure USDT-M futures client is connected."""
        client = self._http_futures_um
        if client._session is None:
            await client.connect()
        return client

    async def _ensure_futures_cm_connected(self) -> HTTPClient:
        """Ensure COIN-M futures client is connected."""
        client = self._http_futures_cm
        if client._session is None:
            await client.connect()
        return client

    # ============ General Endpoints ============

    async def ping(self) -> dict[str, Any]:
        """Test connectivity to the Rest API.

        Weight: 1

        Returns:
            Empty dict on success
        """
        return await general.ping(self._http)

    async def get_server_time(self) -> ServerTime:
        """Test connectivity and get current server time.

        Weight: 1

        Returns:
            ServerTime with server_time in milliseconds
        """
        return await general.get_server_time(self._http)

    async def get_exchange_info(
        self,
        symbol: str | None = None,
        symbols: list[str] | None = None,
        permissions: list[str] | None = None,
    ) -> ExchangeInfo:
        """Get current exchange trading rules and symbol information.

        Weight: 20

        Args:
            symbol: Trading pair (e.g., "BTCUSDT")
            symbols: List of trading pairs
            permissions: Filter by permissions

        Returns:
            ExchangeInfo with symbols and rate limits
        """
        return await general.get_exchange_info(
            self._http,
            symbol=symbol,
            symbols=symbols,
            permissions=permissions,
        )

    # ============ Market Data Endpoints ============

    async def get_order_book(
        self,
        symbol: str,
        limit: int = 100,
    ) -> OrderBook:
        """Get order book depth.

        Weight: 5-50 depending on limit

        Args:
            symbol: Trading pair
            limit: Depth limit (5, 10, 20, 50, 100, 500, 1000, 5000)

        Returns:
            OrderBook with bids and asks
        """
        return await market.get_order_book(self._http, symbol=symbol, limit=limit)

    async def get_trades(
        self,
        symbol: str,
        limit: int = 500,
    ) -> list[Trade]:
        """Get recent trades.

        Weight: 10

        Args:
            symbol: Trading pair
            limit: Number of trades (max 1000)

        Returns:
            List of Trade objects
        """
        return await market.get_trades(self._http, symbol=symbol, limit=limit)

    async def get_agg_trades(
        self,
        symbol: str,
        from_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 500,
    ) -> list[AggTrade]:
        """Get aggregated trades.

        Weight: 2

        Returns:
            List of AggTrade objects
        """
        return await market.get_agg_trades(
            self._http,
            symbol=symbol,
            from_id=from_id,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    async def get_klines(
        self,
        symbol: str,
        interval: str,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 500,
    ) -> list[Kline]:
        """Get kline/candlestick bars.

        Weight: 2

        Args:
            symbol: Trading pair (e.g., "BTCUSDT")
            interval: Kline interval (1m, 5m, 15m, 1h, 4h, 1d, etc.)
            start_time: Start time in ms
            end_time: End time in ms
            limit: Number of klines (max 1000)

        Returns:
            List of Kline objects with typed fields (open, high, low, close, volume, etc.)
        """
        return await market.get_klines(
            self._http,
            symbol=symbol,
            interval=interval,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    async def get_avg_price(self, symbol: str) -> AvgPrice:
        """Get current average price.

        Weight: 2

        Returns:
            AvgPrice with mins and price
        """
        return await market.get_avg_price(self._http, symbol=symbol)

    # Ticker endpoints with overloads for type safety
    @overload
    async def get_ticker_24h(self, symbol: str) -> Ticker24h: ...

    @overload
    async def get_ticker_24h(
        self, symbol: None = None, symbols: list[str] | None = None
    ) -> list[Ticker24h]: ...

    async def get_ticker_24h(
        self,
        symbol: str | None = None,
        symbols: list[str] | None = None,
    ) -> Ticker24h | list[Ticker24h]:
        """Get 24hr ticker price change statistics.

        Weight: 1-80 depending on parameters

        Args:
            symbol: Single trading pair (returns Ticker24h)
            symbols: Multiple trading pairs (returns list[Ticker24h])

        Returns:
            Ticker24h if symbol specified, else list[Ticker24h]
        """
        return await market.get_ticker_24h(self._http, symbol=symbol, symbols=symbols)

    @overload
    async def get_ticker_price(self, symbol: str) -> TickerPrice: ...

    @overload
    async def get_ticker_price(
        self, symbol: None = None, symbols: list[str] | None = None
    ) -> list[TickerPrice]: ...

    async def get_ticker_price(
        self,
        symbol: str | None = None,
        symbols: list[str] | None = None,
    ) -> TickerPrice | list[TickerPrice]:
        """Get symbol price ticker.

        Weight: 1-4

        Returns:
            TickerPrice if symbol specified, else list[TickerPrice]
        """
        return await market.get_ticker_price(self._http, symbol=symbol, symbols=symbols)

    @overload
    async def get_book_ticker(self, symbol: str) -> BookTicker: ...

    @overload
    async def get_book_ticker(
        self, symbol: None = None, symbols: list[str] | None = None
    ) -> list[BookTicker]: ...

    async def get_book_ticker(
        self,
        symbol: str | None = None,
        symbols: list[str] | None = None,
    ) -> BookTicker | list[BookTicker]:
        """Get best bid/ask price.

        Weight: 1-4

        Returns:
            BookTicker if symbol specified, else list[BookTicker]
        """
        return await market.get_book_ticker(self._http, symbol=symbol, symbols=symbols)

    # ============ Trade Endpoints (Signed) ============

    async def create_order(
        self,
        symbol: str,
        side: str,
        type: str,
        quantity: str | None = None,
        quote_order_qty: str | None = None,
        price: str | None = None,
        time_in_force: str | None = None,
        new_client_order_id: str | None = None,
        stop_price: str | None = None,
        trailing_delta: int | None = None,
        iceberg_qty: str | None = None,
        new_order_resp_type: str | None = None,
    ) -> Order:
        """Create a new order.

        Weight: 1
        Requires: Signature

        Args:
            symbol: Trading pair
            side: BUY or SELL
            type: Order type (LIMIT, MARKET, STOP_LOSS, etc.)
            quantity: Order quantity
            quote_order_qty: Quote quantity (for MARKET orders)
            price: Limit price
            time_in_force: GTC, IOC, FOK
            new_client_order_id: Custom order ID for idempotency
            stop_price: Stop price for STOP_LOSS orders
            trailing_delta: Trailing delta for trailing stop orders
            iceberg_qty: Iceberg quantity
            new_order_resp_type: ACK, RESULT, or FULL

        Returns:
            Order with order_id, status, fills, etc.

        Tip:
            Always provide `new_client_order_id` for idempotent order placement.
            If a network error occurs, you can safely retry with the same client ID -
            Binance will reject duplicates, preventing accidental double orders.
        """
        return await trade.create_order(
            self._http,
            symbol=symbol,
            side=side,
            type=type,
            quantity=quantity,
            quote_order_qty=quote_order_qty,
            price=price,
            time_in_force=time_in_force,
            new_client_order_id=new_client_order_id,
            stop_price=stop_price,
            trailing_delta=trailing_delta,
            iceberg_qty=iceberg_qty,
            new_order_resp_type=new_order_resp_type,
        )

    async def create_test_order(
        self,
        symbol: str,
        side: str,
        type: str,
        quantity: str | None = None,
        quote_order_qty: str | None = None,
        price: str | None = None,
        time_in_force: str | None = None,
        new_client_order_id: str | None = None,
        stop_price: str | None = None,
        new_order_resp_type: str | None = None,
    ) -> dict[str, Any]:
        """Test new order creation (no actual order placed).

        Weight: 1
        Requires: Signature

        Returns:
            Empty dict on success
        """
        return await trade.create_test_order(
            self._http,
            symbol=symbol,
            side=side,
            type=type,
            quantity=quantity,
            quote_order_qty=quote_order_qty,
            price=price,
            time_in_force=time_in_force,
            new_client_order_id=new_client_order_id,
            stop_price=stop_price,
            new_order_resp_type=new_order_resp_type,
        )

    async def get_order(
        self,
        symbol: str,
        order_id: int | None = None,
        orig_client_order_id: str | None = None,
    ) -> QueryOrder:
        """Query order status.

        Weight: 4
        Requires: Signature

        Args:
            symbol: Trading pair
            order_id: Order ID (use this or orig_client_order_id)
            orig_client_order_id: Client order ID

        Returns:
            QueryOrder with current status
        """
        return await trade.get_order(
            self._http,
            symbol=symbol,
            order_id=order_id,
            orig_client_order_id=orig_client_order_id,
        )

    async def cancel_order(
        self,
        symbol: str,
        order_id: int | None = None,
        orig_client_order_id: str | None = None,
        new_client_order_id: str | None = None,
    ) -> CancelOrderResult:
        """Cancel an active order.

        Weight: 1
        Requires: Signature

        Returns:
            CancelOrderResult with final status
        """
        return await trade.cancel_order(
            self._http,
            symbol=symbol,
            order_id=order_id,
            orig_client_order_id=orig_client_order_id,
            new_client_order_id=new_client_order_id,
        )

    async def get_open_orders(
        self,
        symbol: str | None = None,
    ) -> list[QueryOrder]:
        """Get all open orders.

        Weight: 6 (with symbol) or 80 (without)
        Requires: Signature

        Returns:
            List of open QueryOrder objects
        """
        return await trade.get_open_orders(self._http, symbol=symbol)

    async def get_all_orders(
        self,
        symbol: str,
        order_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 500,
    ) -> list[QueryOrder]:
        """Get all orders (active, canceled, filled).

        Weight: 20
        Requires: Signature

        Returns:
            List of QueryOrder objects
        """
        return await trade.get_all_orders(
            self._http,
            symbol=symbol,
            order_id=order_id,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    # ============ Account Endpoints (Signed) ============

    async def get_account(self) -> Account:
        """Get current account information.

        Weight: 20
        Requires: Signature

        Returns:
            Account with balances and permissions
        """
        return await account.get_account(self._http)

    async def get_my_trades(
        self,
        symbol: str,
        order_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        from_id: int | None = None,
        limit: int = 500,
    ) -> list[MyTrade]:
        """Get trades for a specific account and symbol.

        Weight: 20
        Requires: Signature

        Returns:
            List of MyTrade objects
        """
        return await account.get_my_trades(
            self._http,
            symbol=symbol,
            order_id=order_id,
            start_time=start_time,
            end_time=end_time,
            from_id=from_id,
            limit=limit,
        )

    # ============ USDT-M Futures General Endpoints ============

    async def futures_ping(self) -> dict[str, Any]:
        """Test connectivity to USDT-M Futures API.

        Weight: 1

        Returns:
            Empty dict on success
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.general.ping(http)

    async def futures_get_server_time(self) -> ServerTime:
        """Get USDT-M Futures server time.

        Weight: 1

        Returns:
            ServerTime with server_time in milliseconds
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.general.get_server_time(http)

    async def futures_get_exchange_info(self) -> FuturesExchangeInfo:
        """Get USDT-M Futures exchange trading rules.

        Weight: 1

        Returns:
            FuturesExchangeInfo with symbols and rate limits
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.general.get_exchange_info(http)

    # ============ USDT-M Futures Market Data Endpoints ============

    async def futures_get_order_book(
        self,
        symbol: str,
        limit: int = 500,
    ) -> OrderBook:
        """Get USDT-M futures order book depth.

        Weight: 5-20 depending on limit

        Args:
            symbol: Trading pair (e.g., "BTCUSDT")
            limit: Depth limit (5, 10, 20, 50, 100, 500, 1000)

        Returns:
            OrderBook with bids and asks
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.market.get_order_book(http, symbol=symbol, limit=limit)

    async def futures_get_trades(
        self,
        symbol: str,
        limit: int = 500,
    ) -> list[Trade]:
        """Get USDT-M futures recent trades.

        Weight: 5

        Returns:
            List of Trade objects
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.market.get_trades(http, symbol=symbol, limit=limit)

    async def futures_get_agg_trades(
        self,
        symbol: str,
        from_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 500,
    ) -> list[AggTrade]:
        """Get USDT-M futures aggregated trades.

        Weight: 20

        Returns:
            List of AggTrade objects
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.market.get_agg_trades(
            http,
            symbol=symbol,
            from_id=from_id,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    async def futures_get_klines(
        self,
        symbol: str,
        interval: str,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 500,
    ) -> list[FuturesKline]:
        """Get USDT-M futures kline/candlestick bars.

        Weight: 5

        Args:
            symbol: Trading pair (e.g., "BTCUSDT")
            interval: Kline interval (1m, 5m, 15m, 1h, 4h, 1d, etc.)
            start_time: Start time in ms
            end_time: End time in ms
            limit: Number of klines (max 1500)

        Returns:
            List of FuturesKline objects with typed fields
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.market.get_klines(
            http,
            symbol=symbol,
            interval=interval,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    async def futures_get_continuous_klines(
        self,
        pair: str,
        contract_type: str,
        interval: str,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 500,
    ) -> list[FuturesKline]:
        """Get USDT-M continuous contract klines.

        Weight: 5

        Args:
            pair: Trading pair (e.g., "BTCUSDT")
            contract_type: PERPETUAL, CURRENT_QUARTER, NEXT_QUARTER
            interval: Kline interval

        Returns:
            List of FuturesKline objects
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.market.get_continuous_klines(
            http,
            pair=pair,
            contract_type=contract_type,
            interval=interval,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    @overload
    async def futures_get_mark_price(self, symbol: str) -> MarkPrice: ...
    @overload
    async def futures_get_mark_price(self, symbol: None = None) -> list[MarkPrice]: ...

    async def futures_get_mark_price(
        self,
        symbol: str | None = None,
    ) -> MarkPrice | list[MarkPrice]:
        """Get USDT-M futures mark price and funding rate.

        Weight: 1

        Args:
            symbol: Trading pair (returns single) or None (returns all)

        Returns:
            MarkPrice if symbol specified, else list[MarkPrice]
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.market.get_mark_price(http, symbol=symbol)

    async def futures_get_funding_rate(
        self,
        symbol: str,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 100,
    ) -> list[FundingRate]:
        """Get USDT-M futures funding rate history.

        Weight: 1

        Returns:
            List of FundingRate objects
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.market.get_funding_rate(
            http,
            symbol=symbol,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    @overload
    async def futures_get_ticker_24h(self, symbol: str) -> FuturesTicker24h: ...
    @overload
    async def futures_get_ticker_24h(self, symbol: None = None) -> list[FuturesTicker24h]: ...

    async def futures_get_ticker_24h(
        self,
        symbol: str | None = None,
    ) -> FuturesTicker24h | list[FuturesTicker24h]:
        """Get USDT-M futures 24hr ticker.

        Weight: 1-40 depending on parameters

        Returns:
            FuturesTicker24h if symbol specified, else list
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.market.get_ticker_24h(http, symbol=symbol)

    @overload
    async def futures_get_ticker_price(self, symbol: str) -> TickerPrice: ...
    @overload
    async def futures_get_ticker_price(self, symbol: None = None) -> list[TickerPrice]: ...

    async def futures_get_ticker_price(
        self,
        symbol: str | None = None,
    ) -> TickerPrice | list[TickerPrice]:
        """Get USDT-M futures symbol price ticker.

        Weight: 1-2

        Returns:
            TickerPrice if symbol specified, else list
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.market.get_ticker_price(http, symbol=symbol)

    @overload
    async def futures_get_book_ticker(self, symbol: str) -> BookTicker: ...
    @overload
    async def futures_get_book_ticker(self, symbol: None = None) -> list[BookTicker]: ...

    async def futures_get_book_ticker(
        self,
        symbol: str | None = None,
    ) -> BookTicker | list[BookTicker]:
        """Get USDT-M futures best bid/ask price.

        Weight: 1-2

        Returns:
            BookTicker if symbol specified, else list
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.market.get_book_ticker(http, symbol=symbol)
