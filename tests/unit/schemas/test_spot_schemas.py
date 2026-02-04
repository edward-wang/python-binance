"""Test spot API schemas including edge cases."""
import msgspec
import pytest

from binance._schemas.spot import (
    ServerTime,
    Order,
    OrderFill,
    CancelOrderResult,
    Account,
    Balance,
    Trade,
    MyTrade,
    OrderBook,
    Kline,
    TickerPrice,
    Ticker24h,
    BookTicker,
    ExchangeInfo,
    Symbol,
    SymbolFilter,
    RateLimit,
    AvgPrice,
    AggTrade,
)


class TestServerTime:
    """Test ServerTime schema."""

    def test_decode_server_time(self):
        """Test basic decoding."""
        data = b'{"serverTime": 1699999999999}'
        result = msgspec.json.decode(data, type=ServerTime)
        assert result.server_time == 1699999999999

    def test_frozen_immutable(self):
        """Test schema is frozen."""
        st = ServerTime(server_time=123)
        with pytest.raises(AttributeError):
            st.server_time = 456


class TestOrder:
    """Test Order schema with response variations."""

    def test_decode_ack_response(self):
        """Test ACK response (minimal fields)."""
        data = b'''{
            "symbol": "BTCUSDT",
            "orderId": 123456,
            "orderListId": -1,
            "clientOrderId": "test123",
            "transactTime": 1699999999999
        }'''
        order = msgspec.json.decode(data, type=Order)
        assert order.symbol == "BTCUSDT"
        assert order.order_id == 123456
        assert order.price is None  # Not in ACK

    def test_decode_result_response(self):
        """Test RESULT response (includes status)."""
        data = b'''{
            "symbol": "BTCUSDT",
            "orderId": 123456,
            "orderListId": -1,
            "clientOrderId": "test123",
            "transactTime": 1699999999999,
            "price": "50000.00",
            "origQty": "0.001",
            "executedQty": "0.001",
            "cummulativeQuoteQty": "50.00",
            "status": "FILLED",
            "timeInForce": "GTC",
            "type": "LIMIT",
            "side": "BUY"
        }'''
        order = msgspec.json.decode(data, type=Order)
        assert order.status == "FILLED"
        assert order.price == "50000.00"

    def test_decode_full_response_with_fills(self):
        """Test FULL response (includes fills)."""
        data = b'''{
            "symbol": "BTCUSDT",
            "orderId": 123456,
            "orderListId": -1,
            "clientOrderId": "test123",
            "transactTime": 1699999999999,
            "price": "50000.00",
            "origQty": "0.001",
            "executedQty": "0.001",
            "cummulativeQuoteQty": "50.00",
            "status": "FILLED",
            "timeInForce": "GTC",
            "type": "MARKET",
            "side": "BUY",
            "fills": [
                {"price": "50000.00", "qty": "0.001", "commission": "0.00001", "commissionAsset": "BTC", "tradeId": 789}
            ]
        }'''
        order = msgspec.json.decode(data, type=Order)
        assert order.fills is not None
        assert len(order.fills) == 1
        assert order.fills[0].trade_id == 789


class TestAccount:
    """Test Account schema."""

    def test_decode_account_with_balances(self):
        """Test decoding with nested balances."""
        data = b'''{
            "makerCommission": 10,
            "takerCommission": 10,
            "buyerCommission": 0,
            "sellerCommission": 0,
            "canTrade": true,
            "canWithdraw": true,
            "canDeposit": true,
            "updateTime": 1699999999999,
            "accountType": "SPOT",
            "balances": [
                {"asset": "BTC", "free": "1.0", "locked": "0.0"},
                {"asset": "USDT", "free": "10000.0", "locked": "0.0"}
            ],
            "permissions": ["SPOT"]
        }'''
        account = msgspec.json.decode(data, type=Account)
        assert account.account_type == "SPOT"
        assert len(account.balances) == 2
        assert account.balances[0].asset == "BTC"

    def test_empty_balances(self):
        """Test with empty balances array."""
        data = b'''{
            "makerCommission": 10,
            "takerCommission": 10,
            "buyerCommission": 0,
            "sellerCommission": 0,
            "canTrade": true,
            "canWithdraw": true,
            "canDeposit": true,
            "updateTime": 1699999999999,
            "accountType": "SPOT",
            "balances": [],
            "permissions": []
        }'''
        account = msgspec.json.decode(data, type=Account)
        assert account.balances == []


class TestSymbolFilter:
    """Test SymbolFilter with different filter types."""

    def test_price_filter(self):
        """Test PRICE_FILTER type."""
        data = b'''{
            "filterType": "PRICE_FILTER",
            "minPrice": "0.01",
            "maxPrice": "1000000.0",
            "tickSize": "0.01"
        }'''
        f = msgspec.json.decode(data, type=SymbolFilter)
        assert f.filter_type == "PRICE_FILTER"
        assert f.min_price == "0.01"
        assert f.tick_size == "0.01"

    def test_lot_size_filter(self):
        """Test LOT_SIZE type."""
        data = b'''{
            "filterType": "LOT_SIZE",
            "minQty": "0.00001",
            "maxQty": "9000.0",
            "stepSize": "0.00001"
        }'''
        f = msgspec.json.decode(data, type=SymbolFilter)
        assert f.filter_type == "LOT_SIZE"
        assert f.step_size == "0.00001"

    def test_min_notional_filter(self):
        """Test MIN_NOTIONAL type."""
        data = b'''{
            "filterType": "MIN_NOTIONAL",
            "minNotional": "10.0",
            "applyToMarket": true,
            "avgPriceMins": 5
        }'''
        f = msgspec.json.decode(data, type=SymbolFilter)
        assert f.min_notional == "10.0"
        assert f.apply_to_market is True

    def test_unknown_fields_ignored(self):
        """Test unknown fields are silently ignored (msgspec default)."""
        data = b'''{
            "filterType": "UNKNOWN_FILTER",
            "unknownField": "value"
        }'''
        f = msgspec.json.decode(data, type=SymbolFilter)
        assert f.filter_type == "UNKNOWN_FILTER"


class TestOrderBook:
    """Test OrderBook schema."""

    def test_decode_order_book(self):
        """Test decoding order book."""
        data = b'''{
            "lastUpdateId": 123456789,
            "bids": [["50000.00", "1.0"], ["49999.00", "2.0"]],
            "asks": [["50001.00", "1.5"], ["50002.00", "3.0"]]
        }'''
        book = msgspec.json.decode(data, type=OrderBook)
        assert book.last_update_id == 123456789
        assert len(book.bids) == 2
        assert book.bids[0] == ["50000.00", "1.0"]

    def test_empty_order_book(self):
        """Test empty bids/asks (illiquid market)."""
        data = b'{"lastUpdateId": 1, "bids": [], "asks": []}'
        book = msgspec.json.decode(data, type=OrderBook)
        assert book.bids == []
        assert book.asks == []


class TestKline:
    """Test Kline schema with from_raw() converter."""

    def test_kline_from_raw(self):
        """Test converting raw kline array to typed Kline."""
        raw = [
            1699999999999,  # open_time
            "50000.00",  # open
            "51000.00",  # high
            "49000.00",  # low
            "50500.00",  # close
            "100.5",  # volume
            1700000003999,  # close_time
            "5025000.00",  # quote_volume
            1500,  # trades
            "60.3",  # taker_buy_base
            "3015000.00",  # taker_buy_quote
        ]
        kline = Kline.from_raw(raw)

        assert kline.open_time == 1699999999999
        assert kline.open == "50000.00"
        assert kline.high == "51000.00"
        assert kline.low == "49000.00"
        assert kline.close == "50500.00"
        assert kline.volume == "100.5"
        assert kline.close_time == 1700000003999
        assert kline.trades == 1500

    def test_kline_is_frozen(self):
        """Test Kline is immutable."""
        kline = Kline.from_raw([0, "1", "2", "3", "4", "5", 0, "6", 0, "7", "8"])
        with pytest.raises(AttributeError):
            kline.close = "9999"

    def test_kline_list_conversion(self):
        """Test converting list of raw klines."""
        raw_klines = [
            [1699999999999, "50000", "51000", "49000", "50500", "100", 1700000003999, "5000", 100, "60", "3000"],
            [1700000003999, "50500", "52000", "50000", "51500", "150", 1700000007999, "7500", 200, "90", "4500"],
        ]
        klines = [Kline.from_raw(k) for k in raw_klines]

        assert len(klines) == 2
        assert klines[0].close == "50500"
        assert klines[1].close == "51500"


class TestTickerVariants:
    """Test ticker schemas."""

    def test_ticker_price(self):
        """Test TickerPrice decoding."""
        data = b'{"symbol": "BTCUSDT", "price": "50000.00"}'
        ticker = msgspec.json.decode(data, type=TickerPrice)
        assert ticker.symbol == "BTCUSDT"
        assert ticker.price == "50000.00"

    def test_ticker_price_list(self):
        """Test list of TickerPrice."""
        data = b'[{"symbol": "BTCUSDT", "price": "50000"}, {"symbol": "ETHUSDT", "price": "3000"}]'
        tickers = msgspec.json.decode(data, type=list[TickerPrice])
        assert len(tickers) == 2

    def test_book_ticker(self):
        """Test BookTicker decoding."""
        data = b'''{
            "symbol": "BTCUSDT",
            "bidPrice": "50000.00",
            "bidQty": "1.0",
            "askPrice": "50001.00",
            "askQty": "2.0"
        }'''
        ticker = msgspec.json.decode(data, type=BookTicker)
        assert ticker.bid_price == "50000.00"


class TestTrade:
    """Test Trade schemas."""

    def test_public_trade(self):
        """Test public Trade decoding."""
        data = b'''{
            "id": 123456,
            "price": "50000.00",
            "qty": "0.001",
            "quoteQty": "50.00",
            "time": 1699999999999,
            "isBuyerMaker": true,
            "isBestMatch": true
        }'''
        trade = msgspec.json.decode(data, type=Trade)
        assert trade.id == 123456
        assert trade.is_buyer_maker is True

    def test_my_trade(self):
        """Test MyTrade (user's trade) decoding."""
        data = b'''{
            "symbol": "BTCUSDT",
            "id": 123456,
            "orderId": 789,
            "orderListId": -1,
            "price": "50000.00",
            "qty": "0.001",
            "quoteQty": "50.00",
            "commission": "0.00001",
            "commissionAsset": "BTC",
            "time": 1699999999999,
            "isBuyer": true,
            "isMaker": false,
            "isBestMatch": true
        }'''
        trade = msgspec.json.decode(data, type=MyTrade)
        assert trade.order_id == 789
        assert trade.commission_asset == "BTC"


class TestDecoderPerformance:
    """Test pre-compiled decoders."""

    def test_precompiled_decoder_works(self):
        """Test that pre-compiled decoders work correctly."""
        decoder = msgspec.json.Decoder(Account)
        data = b'''{
            "makerCommission": 10, "takerCommission": 10,
            "buyerCommission": 0, "sellerCommission": 0,
            "canTrade": true, "canWithdraw": true, "canDeposit": true,
            "updateTime": 1, "accountType": "SPOT",
            "balances": [], "permissions": []
        }'''

        # Decode multiple times with same decoder
        for _ in range(100):
            result = decoder.decode(data)
            assert result.account_type == "SPOT"
