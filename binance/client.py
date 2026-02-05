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

    # ============ USDT-M Futures Trade Endpoints (Signed) ============

    async def futures_create_order(
        self,
        symbol: str,
        side: str,
        type: str,
        quantity: str | None = None,
        price: str | None = None,
        time_in_force: str | None = None,
        reduce_only: bool | None = None,
        new_client_order_id: str | None = None,
        stop_price: str | None = None,
        position_side: str | None = None,
        close_position: bool | None = None,
        activation_price: str | None = None,
        callback_rate: str | None = None,
        working_type: str | None = None,
        price_protect: bool | None = None,
        new_order_resp_type: str | None = None,
    ) -> FuturesOrder:
        """Create a new USDT-M futures order.

        Weight: 1
        Requires: Signature

        Args:
            symbol: Trading pair (e.g., "BTCUSDT")
            side: BUY or SELL
            type: LIMIT, MARKET, STOP, STOP_MARKET, TAKE_PROFIT,
                  TAKE_PROFIT_MARKET, TRAILING_STOP_MARKET
            quantity: Order quantity
            price: Limit price
            time_in_force: GTC, IOC, FOK, GTX
            reduce_only: Reduce position only
            new_client_order_id: Custom order ID for idempotency
            stop_price: Stop price
            position_side: LONG, SHORT, or BOTH (hedge mode)
            close_position: Close all position
            activation_price: For TRAILING_STOP_MARKET
            callback_rate: For TRAILING_STOP_MARKET
            working_type: MARK_PRICE or CONTRACT_PRICE
            price_protect: Price protection
            new_order_resp_type: ACK or RESULT

        Returns:
            FuturesOrder with order details

        Tip:
            Always provide `new_client_order_id` for idempotent order placement.
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.trade.create_order(
            http,
            symbol=symbol,
            side=side,
            type=type,
            quantity=quantity,
            price=price,
            time_in_force=time_in_force,
            reduce_only=reduce_only,
            new_client_order_id=new_client_order_id,
            stop_price=stop_price,
            position_side=position_side,
            close_position=close_position,
            activation_price=activation_price,
            callback_rate=callback_rate,
            working_type=working_type,
            price_protect=price_protect,
            new_order_resp_type=new_order_resp_type,
        )

    async def futures_create_test_order(
        self,
        symbol: str,
        side: str,
        type: str,
        quantity: str | None = None,
        price: str | None = None,
        time_in_force: str | None = None,
    ) -> dict[str, Any]:
        """Test USDT-M futures order creation (no actual order placed).

        Weight: 1
        Requires: Signature

        Returns:
            Empty dict on success
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.trade.create_test_order(
            http,
            symbol=symbol,
            side=side,
            type=type,
            quantity=quantity,
            price=price,
            time_in_force=time_in_force,
        )

    async def futures_get_order(
        self,
        symbol: str,
        order_id: int | None = None,
        orig_client_order_id: str | None = None,
    ) -> FuturesOrder:
        """Query USDT-M futures order status.

        Weight: 1
        Requires: Signature

        Returns:
            FuturesOrder with current status
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.trade.get_order(
            http,
            symbol=symbol,
            order_id=order_id,
            orig_client_order_id=orig_client_order_id,
        )

    async def futures_cancel_order(
        self,
        symbol: str,
        order_id: int | None = None,
        orig_client_order_id: str | None = None,
    ) -> FuturesOrder:
        """Cancel an active USDT-M futures order.

        Weight: 1
        Requires: Signature

        Returns:
            FuturesOrder with canceled status
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.trade.cancel_order(
            http,
            symbol=symbol,
            order_id=order_id,
            orig_client_order_id=orig_client_order_id,
        )

    async def futures_cancel_all_open_orders(
        self,
        symbol: str,
    ) -> dict[str, Any]:
        """Cancel all open USDT-M futures orders on a symbol.

        Weight: 1
        Requires: Signature

        Returns:
            Success response
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.trade.cancel_all_open_orders(http, symbol=symbol)

    async def futures_get_open_orders(
        self,
        symbol: str | None = None,
    ) -> list[FuturesOrder]:
        """Get all open USDT-M futures orders.

        Weight: 1-40 depending on symbol
        Requires: Signature

        Returns:
            List of open FuturesOrder objects
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.trade.get_open_orders(http, symbol=symbol)

    async def futures_get_all_orders(
        self,
        symbol: str,
        order_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 500,
    ) -> list[FuturesOrder]:
        """Get all USDT-M futures orders (active, canceled, filled).

        Weight: 5
        Requires: Signature

        Returns:
            List of FuturesOrder objects
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.trade.get_all_orders(
            http,
            symbol=symbol,
            order_id=order_id,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    async def futures_create_batch_orders(
        self,
        orders: list[dict[str, Any]],
    ) -> list[FuturesOrder | BatchOrderError]:
        """Place multiple USDT-M futures orders in a single request.

        Weight: 5
        Requires: Signature

        Note: Each order in the response can be either a FuturesOrder (success)
        or a BatchOrderError (failure). Check for 'code' attribute to detect errors.

        Args:
            orders: List of order dicts (max 5). Each dict should contain:
                - symbol: Trading pair (required)
                - side: BUY or SELL (required)
                - type: Order type (required)
                - quantity: Order quantity (required for most types)
                - price: Limit price (required for LIMIT orders)
                - positionSide: LONG, SHORT, or BOTH (optional)
                - timeInForce: GTC, IOC, FOK (optional)

        Returns:
            List of FuturesOrder or BatchOrderError for each order

        Example:
            orders = [
                {"symbol": "BTCUSDT", "side": "BUY", "type": "LIMIT",
                 "quantity": "0.001", "price": "30000", "timeInForce": "GTC"},
            ]
            results = await client.futures_create_batch_orders(orders)
            for result in results:
                if hasattr(result, 'code'):  # BatchOrderError
                    print(f"Failed: {result.msg}")
                else:
                    print(f"Order {result.order_id} placed")
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.trade.create_batch_orders(http, orders=orders)

    # ============ USDT-M Futures Account Endpoints (Signed) ============

    async def futures_get_account(self) -> FuturesAccount:
        """Get USDT-M futures account information.

        Weight: 5
        Requires: Signature

        Returns:
            FuturesAccount with balances and positions
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.account.get_account(http)

    async def futures_get_balance(self) -> list[FuturesBalance]:
        """Get USDT-M futures account balance.

        Weight: 5
        Requires: Signature

        Returns:
            List of FuturesBalance objects
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.account.get_balance(http)

    async def futures_get_position_risk(
        self,
        symbol: str | None = None,
    ) -> list[PositionRisk]:
        """Get USDT-M futures position information.

        Weight: 5
        Requires: Signature

        Args:
            symbol: Trading pair (optional, returns all if not specified)

        Returns:
            List of PositionRisk objects
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.account.get_position_risk(http, symbol=symbol)

    async def futures_set_leverage(
        self,
        symbol: str,
        leverage: int,
    ) -> LeverageResult:
        """Change USDT-M futures leverage.

        Weight: 1
        Requires: Signature

        Args:
            symbol: Trading pair
            leverage: Target leverage (1-125)

        Returns:
            LeverageResult with new leverage and max notional
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.account.set_leverage(http, symbol=symbol, leverage=leverage)

    async def futures_set_margin_type(
        self,
        symbol: str,
        margin_type: str,
    ) -> dict[str, Any]:
        """Change USDT-M futures margin type.

        Weight: 1
        Requires: Signature

        Args:
            symbol: Trading pair
            margin_type: ISOLATED or CROSSED

        Returns:
            Success response
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.account.set_margin_type(http, symbol=symbol, margin_type=margin_type)

    async def futures_get_my_trades(
        self,
        symbol: str,
        order_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        from_id: int | None = None,
        limit: int = 500,
    ) -> list[FuturesMyTrade]:
        """Get USDT-M futures trades for account.

        Weight: 5
        Requires: Signature

        Returns:
            List of FuturesMyTrade objects
        """
        http = await self._ensure_futures_um_connected()
        return await futures_um.account.get_my_trades(
            http,
            symbol=symbol,
            order_id=order_id,
            start_time=start_time,
            end_time=end_time,
            from_id=from_id,
            limit=limit,
        )

    # ============ COIN-M Futures General Endpoints ============

    async def futures_coin_ping(self) -> dict[str, Any]:
        """Test connectivity to COIN-M Futures API.

        Weight: 1
        """
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.general.ping(http)

    async def futures_coin_get_server_time(self) -> ServerTime:
        """Get COIN-M Futures server time.

        Weight: 1
        """
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.general.get_server_time(http)

    async def futures_coin_get_exchange_info(self) -> FuturesExchangeInfo:
        """Get COIN-M Futures exchange trading rules.

        Weight: 1
        """
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.general.get_exchange_info(http)

    # ============ COIN-M Futures Market Data Endpoints ============

    async def futures_coin_get_order_book(
        self,
        symbol: str,
        limit: int = 500,
    ) -> OrderBook:
        """Get COIN-M futures order book depth."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.market.get_order_book(http, symbol=symbol, limit=limit)

    async def futures_coin_get_trades(
        self,
        symbol: str,
        limit: int = 500,
    ) -> list[Trade]:
        """Get COIN-M futures recent trades."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.market.get_trades(http, symbol=symbol, limit=limit)

    async def futures_coin_get_klines(
        self,
        symbol: str,
        interval: str,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 500,
    ) -> list[FuturesKline]:
        """Get COIN-M futures kline/candlestick bars."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.market.get_klines(
            http,
            symbol=symbol,
            interval=interval,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    @overload
    async def futures_coin_get_mark_price(self, symbol: str) -> MarkPrice: ...
    @overload
    async def futures_coin_get_mark_price(self, symbol: None = None) -> list[MarkPrice]: ...

    async def futures_coin_get_mark_price(
        self,
        symbol: str | None = None,
    ) -> MarkPrice | list[MarkPrice]:
        """Get COIN-M futures mark price and funding rate."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.market.get_mark_price(http, symbol=symbol)

    async def futures_coin_get_funding_rate(
        self,
        symbol: str,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 100,
    ) -> list[FundingRate]:
        """Get COIN-M futures funding rate history."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.market.get_funding_rate(
            http,
            symbol=symbol,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    @overload
    async def futures_coin_get_ticker_24h(self, symbol: str) -> FuturesTicker24h: ...
    @overload
    async def futures_coin_get_ticker_24h(self, symbol: None = None) -> list[FuturesTicker24h]: ...

    async def futures_coin_get_ticker_24h(
        self,
        symbol: str | None = None,
    ) -> FuturesTicker24h | list[FuturesTicker24h]:
        """Get COIN-M futures 24hr ticker."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.market.get_ticker_24h(http, symbol=symbol)

    @overload
    async def futures_coin_get_ticker_price(self, symbol: str) -> TickerPrice: ...
    @overload
    async def futures_coin_get_ticker_price(self, symbol: None = None) -> list[TickerPrice]: ...

    async def futures_coin_get_ticker_price(
        self,
        symbol: str | None = None,
    ) -> TickerPrice | list[TickerPrice]:
        """Get COIN-M futures symbol price ticker."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.market.get_ticker_price(http, symbol=symbol)

    # ============ COIN-M Futures Trade Endpoints (Signed) ============

    async def futures_coin_create_order(
        self,
        symbol: str,
        side: str,
        type: str,
        quantity: str | None = None,
        price: str | None = None,
        time_in_force: str | None = None,
        reduce_only: bool | None = None,
        new_client_order_id: str | None = None,
        stop_price: str | None = None,
        position_side: str | None = None,
        close_position: bool | None = None,
        working_type: str | None = None,
        price_protect: bool | None = None,
        new_order_resp_type: str | None = None,
    ) -> FuturesOrder:
        """Create a new COIN-M futures order.

        Weight: 1
        Requires: Signature
        """
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.trade.create_order(
            http,
            symbol=symbol,
            side=side,
            type=type,
            quantity=quantity,
            price=price,
            time_in_force=time_in_force,
            reduce_only=reduce_only,
            new_client_order_id=new_client_order_id,
            stop_price=stop_price,
            position_side=position_side,
            close_position=close_position,
            working_type=working_type,
            price_protect=price_protect,
            new_order_resp_type=new_order_resp_type,
        )

    async def futures_coin_get_order(
        self,
        symbol: str,
        order_id: int | None = None,
        orig_client_order_id: str | None = None,
    ) -> FuturesOrder:
        """Query COIN-M futures order status."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.trade.get_order(
            http,
            symbol=symbol,
            order_id=order_id,
            orig_client_order_id=orig_client_order_id,
        )

    async def futures_coin_cancel_order(
        self,
        symbol: str,
        order_id: int | None = None,
        orig_client_order_id: str | None = None,
    ) -> FuturesOrder:
        """Cancel an active COIN-M futures order."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.trade.cancel_order(
            http,
            symbol=symbol,
            order_id=order_id,
            orig_client_order_id=orig_client_order_id,
        )

    async def futures_coin_cancel_all_open_orders(
        self,
        symbol: str,
    ) -> dict[str, Any]:
        """Cancel all open COIN-M futures orders on a symbol."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.trade.cancel_all_open_orders(http, symbol=symbol)

    async def futures_coin_get_open_orders(
        self,
        symbol: str | None = None,
    ) -> list[FuturesOrder]:
        """Get all open COIN-M futures orders."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.trade.get_open_orders(http, symbol=symbol)

    async def futures_coin_get_all_orders(
        self,
        symbol: str,
        order_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 500,
    ) -> list[FuturesOrder]:
        """Get all COIN-M futures orders (active, canceled, filled)."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.trade.get_all_orders(
            http,
            symbol=symbol,
            order_id=order_id,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    async def futures_coin_create_batch_orders(
        self,
        orders: list[dict[str, Any]],
    ) -> list[FuturesOrder | BatchOrderError]:
        """Place multiple COIN-M futures orders in a single request.

        Weight: 5
        Requires: Signature

        Args:
            orders: List of order dicts (max 5)

        Returns:
            List of FuturesOrder or BatchOrderError for each order
        """
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.trade.create_batch_orders(http, orders=orders)

    # ============ COIN-M Futures Account Endpoints (Signed) ============

    async def futures_coin_get_account(self) -> FuturesAccount:
        """Get COIN-M futures account information."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.account.get_account(http)

    async def futures_coin_get_balance(self) -> list[FuturesBalance]:
        """Get COIN-M futures account balance."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.account.get_balance(http)

    async def futures_coin_get_position_risk(
        self,
        symbol: str | None = None,
    ) -> list[PositionRisk]:
        """Get COIN-M futures position information."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.account.get_position_risk(http, symbol=symbol)

    async def futures_coin_set_leverage(
        self,
        symbol: str,
        leverage: int,
    ) -> LeverageResult:
        """Change COIN-M futures leverage."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.account.set_leverage(http, symbol=symbol, leverage=leverage)

    async def futures_coin_set_margin_type(
        self,
        symbol: str,
        margin_type: str,
    ) -> dict[str, Any]:
        """Change COIN-M futures margin type."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.account.set_margin_type(http, symbol=symbol, margin_type=margin_type)

    async def futures_coin_get_my_trades(
        self,
        symbol: str,
        order_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        from_id: int | None = None,
        limit: int = 500,
    ) -> list[FuturesMyTrade]:
        """Get COIN-M futures trades for account."""
        http = await self._ensure_futures_cm_connected()
        return await futures_cm.account.get_my_trades(
            http,
            symbol=symbol,
            order_id=order_id,
            start_time=start_time,
            end_time=end_time,
            from_id=from_id,
            limit=limit,
        )
