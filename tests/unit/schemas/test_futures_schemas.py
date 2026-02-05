"""Test futures API schemas including edge cases."""
import msgspec
import pytest

from binance._schemas.futures import (
    FuturesExchangeInfo,
    FuturesSymbol,
    FuturesKline,
    FuturesOrder,
    FuturesAccount,
    FuturesAsset,
    FuturesBalance,
    AccountPosition,
    PositionRisk,
    MarkPrice,
    FundingRate,
    LeverageResult,
    FuturesTicker24h,
    FuturesMyTrade,
)


def test_futures_schemas_importable():
    """Test that futures schemas can be imported."""
    from binance._schemas.futures import (
        FuturesExchangeInfo,
        FuturesKline,
        FuturesOrder,
        FuturesAccount,
        FuturesAsset,
        FuturesBalance,
        AccountPosition,
        PositionRisk,
        MarkPrice,
        FundingRate,
        LeverageResult,
        FuturesTicker24h,
        FuturesMyTrade,
    )
    assert FuturesExchangeInfo is not None
    assert FuturesKline is not None
    assert FuturesOrder is not None
    assert AccountPosition is not None


class TestFuturesKline:
    """Test FuturesKline schema with from_raw() converter."""

    def test_kline_from_raw(self):
        """Test converting raw kline array to typed FuturesKline."""
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
        kline = FuturesKline.from_raw(raw)

        assert kline.open_time == 1699999999999
        assert kline.open == "50000.00"
        assert kline.high == "51000.00"
        assert kline.low == "49000.00"
        assert kline.close == "50500.00"
        assert kline.volume == "100.5"
        assert kline.close_time == 1700000003999
        assert kline.trades == 1500

    def test_kline_is_frozen(self):
        """Test FuturesKline is immutable."""
        kline = FuturesKline.from_raw([0, "1", "2", "3", "4", "5", 0, "6", 0, "7", "8"])
        with pytest.raises(AttributeError):
            kline.close = "9999"


class TestFuturesOrder:
    """Test FuturesOrder schema."""

    def test_decode_new_order(self):
        """Test decoding new order response."""
        data = b"""{
            "symbol": "BTCUSDT",
            "orderId": 12345678,
            "clientOrderId": "test123",
            "price": "50000.00",
            "origQty": "0.001",
            "executedQty": "0.000",
            "status": "NEW",
            "timeInForce": "GTC",
            "type": "LIMIT",
            "side": "BUY",
            "positionSide": "BOTH",
            "updateTime": 1699999999999
        }"""
        order = msgspec.json.decode(data, type=FuturesOrder)
        assert order.symbol == "BTCUSDT"
        assert order.order_id == 12345678
        assert order.status == "NEW"

    def test_decode_filled_order_with_avg_price(self):
        """Test decoding filled order with average price."""
        data = b"""{
            "symbol": "BTCUSDT",
            "orderId": 12345678,
            "clientOrderId": "test123",
            "price": "0",
            "origQty": "0.001",
            "executedQty": "0.001",
            "status": "FILLED",
            "timeInForce": "GTC",
            "type": "MARKET",
            "side": "BUY",
            "avgPrice": "50123.45",
            "updateTime": 1699999999999
        }"""
        order = msgspec.json.decode(data, type=FuturesOrder)
        assert order.status == "FILLED"
        assert order.avg_price == "50123.45"


class TestPositionRisk:
    """Test PositionRisk schema."""

    def test_decode_position(self):
        """Test decoding position risk."""
        data = b"""{
            "symbol": "BTCUSDT",
            "positionAmt": "0.001",
            "entryPrice": "50000.00",
            "markPrice": "50500.00",
            "unRealizedProfit": "0.50",
            "liquidationPrice": "0",
            "leverage": "20",
            "marginType": "cross",
            "positionSide": "BOTH"
        }"""
        position = msgspec.json.decode(data, type=PositionRisk)
        assert position.symbol == "BTCUSDT"
        assert position.position_amt == "0.001"
        assert position.leverage == "20"
        assert position.margin_type == "cross"

    def test_decode_empty_position(self):
        """Test decoding position with zero amount."""
        data = b"""{
            "symbol": "ETHUSDT",
            "positionAmt": "0",
            "entryPrice": "0.00000000",
            "markPrice": "3000.00",
            "unRealizedProfit": "0.00000000",
            "liquidationPrice": "0",
            "leverage": "10",
            "marginType": "cross",
            "positionSide": "BOTH"
        }"""
        position = msgspec.json.decode(data, type=PositionRisk)
        assert position.position_amt == "0"


class TestMarkPrice:
    """Test MarkPrice schema."""

    def test_decode_mark_price(self):
        """Test decoding mark price response."""
        data = b"""{
            "symbol": "BTCUSDT",
            "markPrice": "50000.00000000",
            "indexPrice": "49995.00000000",
            "lastFundingRate": "0.00010000",
            "nextFundingTime": 1700000000000,
            "time": 1699999999999
        }"""
        mark = msgspec.json.decode(data, type=MarkPrice)
        assert mark.symbol == "BTCUSDT"
        assert mark.mark_price == "50000.00000000"
        assert mark.last_funding_rate == "0.00010000"

    def test_decode_mark_price_with_interest_rate(self):
        """Test decoding mark price with interest rate field."""
        data = b"""{
            "symbol": "BTCUSDT",
            "markPrice": "50000.00",
            "indexPrice": "49995.00",
            "estimatedSettlePrice": "50010.00",
            "lastFundingRate": "0.0001",
            "interestRate": "0.0003",
            "nextFundingTime": 1700000000000,
            "time": 1699999999999
        }"""
        mark = msgspec.json.decode(data, type=MarkPrice)
        assert mark.estimated_settle_price == "50010.00"
        assert mark.interest_rate == "0.0003"


class TestFundingRate:
    """Test FundingRate schema."""

    def test_decode_funding_rate(self):
        """Test decoding funding rate history."""
        data = b"""{
            "symbol": "BTCUSDT",
            "fundingRate": "0.00010000",
            "fundingTime": 1699999999999
        }"""
        rate = msgspec.json.decode(data, type=FundingRate)
        assert rate.symbol == "BTCUSDT"
        assert rate.funding_rate == "0.00010000"

    def test_decode_funding_rate_list(self):
        """Test decoding list of funding rates."""
        data = b"""[
            {"symbol": "BTCUSDT", "fundingRate": "0.0001", "fundingTime": 1699999999999},
            {"symbol": "BTCUSDT", "fundingRate": "0.0002", "fundingTime": 1699996399999}
        ]"""
        rates = msgspec.json.decode(data, type=list[FundingRate])
        assert len(rates) == 2
        assert rates[0].funding_rate == "0.0001"


class TestFuturesAccount:
    """Test FuturesAccount schema."""

    def test_decode_account_with_positions(self):
        """Test decoding account with positions."""
        data = b"""{
            "totalInitialMargin": "100.00000000",
            "totalMaintMargin": "50.00000000",
            "totalWalletBalance": "10000.00000000",
            "totalUnrealizedProfit": "50.00000000",
            "totalMarginBalance": "10050.00000000",
            "totalPositionInitialMargin": "100.00000000",
            "totalOpenOrderInitialMargin": "0.00000000",
            "totalCrossWalletBalance": "10000.00000000",
            "totalCrossUnPnl": "50.00000000",
            "availableBalance": "9900.00000000",
            "maxWithdrawAmount": "9900.00000000",
            "assets": [
                {
                    "asset": "USDT",
                    "walletBalance": "10000.00",
                    "unrealizedProfit": "50.00",
                    "marginBalance": "10050.00",
                    "maintMargin": "50.00",
                    "initialMargin": "100.00",
                    "positionInitialMargin": "100.00",
                    "openOrderInitialMargin": "0.00",
                    "maxWithdrawAmount": "9900.00"
                }
            ],
            "positions": [
                {
                    "symbol": "BTCUSDT",
                    "positionAmt": "0.001",
                    "entryPrice": "50000.00",
                    "unrealizedProfit": "0.05",
                    "leverage": "20",
                    "positionSide": "BOTH",
                    "initialMargin": "2.50",
                    "maintMargin": "1.25",
                    "positionInitialMargin": "2.50",
                    "openOrderInitialMargin": "0.00",
                    "isolated": false
                }
            ]
        }"""
        account = msgspec.json.decode(data, type=FuturesAccount)
        assert account.total_wallet_balance == "10000.00000000"
        assert len(account.assets) == 1
        assert account.assets[0].asset == "USDT"
        assert len(account.positions) == 1
        assert account.positions[0].symbol == "BTCUSDT"


class TestLeverageResult:
    """Test LeverageResult schema."""

    def test_decode_leverage_result(self):
        """Test decoding leverage change result."""
        data = b"""{
            "leverage": 20,
            "maxNotionalValue": "1000000",
            "symbol": "BTCUSDT"
        }"""
        result = msgspec.json.decode(data, type=LeverageResult)
        assert result.leverage == 20
        assert result.max_notional_value == "1000000"
        assert result.symbol == "BTCUSDT"


class TestFuturesExchangeInfo:
    """Test FuturesExchangeInfo schema."""

    def test_decode_exchange_info(self):
        """Test decoding futures exchange info."""
        data = b"""{
            "timezone": "UTC",
            "serverTime": 1699999999999,
            "rateLimits": [
                {"rateLimitType": "REQUEST_WEIGHT", "interval": "MINUTE", "intervalNum": 1, "limit": 2400}
            ],
            "exchangeFilters": [],
            "symbols": [
                {
                    "symbol": "BTCUSDT",
                    "pair": "BTCUSDT",
                    "contractType": "PERPETUAL",
                    "deliveryDate": 4133404800000,
                    "onboardDate": 1569398400000,
                    "status": "TRADING",
                    "maintMarginPercent": "2.5000",
                    "requiredMarginPercent": "5.0000",
                    "baseAsset": "BTC",
                    "quoteAsset": "USDT",
                    "marginAsset": "USDT",
                    "pricePrecision": 2,
                    "quantityPrecision": 3,
                    "baseAssetPrecision": 8,
                    "quotePrecision": 8,
                    "underlyingType": "COIN",
                    "filters": [],
                    "orderTypes": ["LIMIT", "MARKET"],
                    "timeInForce": ["GTC", "IOC"]
                }
            ]
        }"""
        info = msgspec.json.decode(data, type=FuturesExchangeInfo)
        assert info.timezone == "UTC"
        assert len(info.symbols) == 1
        assert info.symbols[0].symbol == "BTCUSDT"
        assert info.symbols[0].contract_type == "PERPETUAL"


class TestFuturesTicker24h:
    """Test FuturesTicker24h schema."""

    def test_decode_ticker(self):
        """Test decoding 24hr ticker."""
        data = b"""{
            "symbol": "BTCUSDT",
            "priceChange": "500.00",
            "priceChangePercent": "1.00",
            "weightedAvgPrice": "50250.00",
            "lastPrice": "50500.00",
            "lastQty": "0.001",
            "openPrice": "50000.00",
            "highPrice": "51000.00",
            "lowPrice": "49500.00",
            "volume": "10000.00",
            "quoteVolume": "500000000.00",
            "openTime": 1699913599999,
            "closeTime": 1699999999999,
            "firstId": 100000,
            "lastId": 200000,
            "count": 100000
        }"""
        ticker = msgspec.json.decode(data, type=FuturesTicker24h)
        assert ticker.symbol == "BTCUSDT"
        assert ticker.price_change == "500.00"
        assert ticker.last_price == "50500.00"


class TestFuturesMyTrade:
    """Test FuturesMyTrade schema."""

    def test_decode_my_trade(self):
        """Test decoding user's futures trade."""
        data = b"""{
            "symbol": "BTCUSDT",
            "id": 123456789,
            "orderId": 987654321,
            "price": "50000.00",
            "qty": "0.001",
            "quoteQty": "50.00",
            "commission": "0.02",
            "commissionAsset": "USDT",
            "time": 1699999999999,
            "buyer": true,
            "maker": false,
            "positionSide": "BOTH",
            "realizedPnl": "0.50"
        }"""
        trade = msgspec.json.decode(data, type=FuturesMyTrade)
        assert trade.symbol == "BTCUSDT"
        assert trade.id == 123456789
        assert trade.buyer is True
        assert trade.maker is False
        assert trade.realized_pnl == "0.50"


class TestFuturesBalance:
    """Test FuturesBalance schema."""

    def test_decode_usdt_m_balance(self):
        """Test decoding USDT-M balance response."""
        data = b"""{
            "accountAlias": "FuXXXXXXWo",
            "asset": "USDT",
            "balance": "10000.00000000",
            "crossWalletBalance": "9900.00000000",
            "availableBalance": "9800.00000000",
            "crossUnPnl": "50.00000000",
            "maxWithdrawAmount": "9800.00000000",
            "marginAvailable": true,
            "updateTime": 1699999999999
        }"""
        balance = msgspec.json.decode(data, type=FuturesBalance)
        assert balance.asset == "USDT"
        assert balance.balance == "10000.00000000"
        assert balance.margin_available is True
        assert balance.max_withdraw_amount == "9800.00000000"

    def test_decode_coin_m_balance(self):
        """Test decoding COIN-M balance response."""
        data = b"""{
            "accountAlias": "CoXXXXXXWo",
            "asset": "BTC",
            "balance": "1.00000000",
            "crossWalletBalance": "0.95000000",
            "availableBalance": "0.90000000",
            "withdrawAvailable": "0.90000000",
            "updateTime": 1699999999999
        }"""
        balance = msgspec.json.decode(data, type=FuturesBalance)
        assert balance.asset == "BTC"
        assert balance.withdraw_available == "0.90000000"
        assert balance.margin_available is None  # COIN-M doesn't have this
